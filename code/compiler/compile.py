#!/usr/bin/env python3
"""
compile.py — the bootstrap compiler entrypoint.

Eats ONE human<->AI conversation transcript and compiles it into a structured,
audited, MiroVerse-aligned interaction trajectory — the artifact MiroVerse's
static QA corpus structurally lacks (no human-in-the-loop, no time-decay, no audit).

Pipeline (each step tagged DET=zero-LLM, LLM=one MiroMind call, HUMAN):
  0 segment transcript into turns                         DET
  1 label @markers (intent/reject/open/decision/trust)    DET   (intent-ledger labeling gate)
  2 auto-wire concept graph                               DET   (gbrain link-extraction)
  3 parse ## Facts / ## Timeline fences                   DET   (gbrain facts-fence)
  4 Change-Classify each intent unit                      DET   (wow-harness)
  5 (optional) MiroMind enrichment of open questions      LLM   (api.miromind.ai, SSE)
  6 trajectory stats (regressions + drift proxy)          DET   (gbrain trajectory.ts)
  7 freeze -> vN-final via hedge scanner                  DET   (wow-harness plan-lock)
  8 emit gate_pack state-file FIRST, then the artifact    DET   (wow-harness state ordering)

Run:
  python3 compiler/compile.py                       # deterministic only (fast)
  python3 compiler/compile.py --miro                # + one MiroMind enrichment call (slow)
"""
import argparse
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import extract as E
import wow as W
import trust as T

SCHEMA_VERSION = 1
TURN_RE = re.compile(r'^---turn\s+role=(\w+)\s+ts=(\S+).*?---\s*$', re.M)
URL_RE = re.compile(r'https?://[^\s\)\]\}"\'>]+')

# @marker grammar (the 意图萃取 the human/上升端 performs as the record is kept)
M_INTENT  = re.compile(r'^@intent:\s*(.+)$', re.M)
M_REJECT  = re.compile(r'^@reject:\s*(.+?)(?:\s*::\s*(.+))?$', re.M)
M_OPEN    = re.compile(r'^@open:\s*(.+)$', re.M)
M_DECIDE  = re.compile(r'^@decision:\s*(.+?)(?:\s*::\s*selected=(\S+))?(?:\s*::\s*record=(\S+))?$', re.M)
M_TRUST   = re.compile(r'^@trust:\s*(.+)$', re.M)
M_STEP    = re.compile(r'^@step:\s*(.+?)(?:\s*::\s*(.+))?$', re.M)


def step_sources(s):
    """All resolvable source URLs on a step, from either the list-of-dicts form
    (deterministic) or the single-url form (miromind fetch). Returns [url, ...]."""
    urls = []
    for src in (s.get("sources") or []):
        u = src.get("url") if isinstance(src, dict) else src
        if u:
            urls.append(u)
    if s.get("url"):
        urls.append(s["url"])
    return urls


def step_verdict(s):
    """HONEST grounding label for a ReAct step. We do NOT claim 'verified' (no real
    second-source agreement check is performed). We only state what we can check:

      "sourced"   — step has >=1 resolvable source URL AND a non-empty observation/
                    snippet (we found a source *and* captured what it said).
      "unsourced" — no resolvable source, OR a source with nothing captured
                    (e.g. a web_search that returned no results, or prose that merely
                    name-drops a URL without an observation). This is NOT a failure;
                    it just means the step is not grounded enough to audit.
    """
    has_src = bool(step_sources(s))
    has_obs = bool((s.get("observation") or "").strip())
    return "sourced" if (has_src and has_obs) else "unsourced"


def _b(v):
    return {"true": True, "false": False, "null": None, "none": None}.get(str(v).strip().lower(), None)


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def parse_trust(line):
    d = {"decision_id": None, "initial_judgment": None, "ai_advice": None,
         "final_judgment": None, "ai_correct": None, "switched": None,
         "agreed": None, "rationale_expanded": None, "note": None}
    for kv in line.split(";"):
        if "=" not in kv:
            continue
        k, v = kv.split("=", 1)
        k, v = k.strip(), v.strip()
        if k == "id": d["decision_id"] = v
        elif k == "initial": d["initial_judgment"] = _num(v)
        elif k == "advice": d["ai_advice"] = _num(v)
        elif k == "final": d["final_judgment"] = _num(v)
        elif k == "ai_correct": d["ai_correct"] = _b(v)
        elif k == "switched": d["switched"] = _b(v)
        elif k == "agreed": d["agreed"] = _b(v)
        elif k == "expanded": d["rationale_expanded"] = _b(v)
        elif k == "note": d["note"] = v
    return d


def segment(text):
    turns, marks = [], list(TURN_RE.finditer(text))
    for i, m in enumerate(marks):
        start = m.end()
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        body = text[start:end].strip()
        turns.append({"idx": i + 1, "role": m.group(1), "ts": m.group(2), "body": body})
    return turns


def detect_regressions(facts):
    """gbrain trajectory.ts: >=10% consecutive drop per metric over time."""
    series = {}
    for f in facts:
        if f.get("claim_metric") and f.get("claim_value") is not None and f.get("valid_from"):
            series.setdefault(f["claim_metric"], []).append((f["valid_from"], f["claim_value"]))
    regs = []
    for metric, pts in series.items():
        pts.sort()
        for (d0, v0), (d1, v1) in zip(pts, pts[1:]):
            if v0 and v1 < v0 * 0.9:
                regs.append({"metric": metric, "from_value": v0, "from_date": d0,
                             "to_value": v1, "to_date": d1,
                             "delta_pct": round((v1 - v0) / v0 * 100, 1)})
    return regs


def drift_proxy(turn_concepts):
    """Lexical drift proxy (no embeddings available): mean Jaccard DISTANCE between
    consecutive turns' concept sets. Honest stand-in for gbrain computeDriftScore
    (1 - mean cosine of consecutive embeddings); null with <3 points."""
    sets = [set(c) for c in turn_concepts if c]
    if len(sets) < 3:
        return None
    dists = []
    for a, b in zip(sets, sets[1:]):
        u = a | b
        dists.append(1 - (len(a & b) / len(u)) if u else 0.0)
    return round(sum(dists) / len(dists), 3)


def compile_transcript(path, use_miro=False):
    raw = open(path, encoding="utf-8").read()
    turns = segment(raw)

    pages, edges, facts, decisions, steps = [], [], [], [], []
    intent = {"stable_intent": [], "rejected_directions": [], "open_questions": [], "operator_entries": []}
    concept_seen = {}
    turn_concept_slugs = []

    for tn in turns:
        slug = f"turns/{tn['idx']:02d}-{tn['role']}"
        body = tn["body"]
        title = " ".join(re.sub(r'[@#*`\[\]]', ' ', body).split()[:9])
        pages.append({
            "slug": slug, "type": f"turn:{tn['role']}", "title": title,
            "compiled_truth": body, "content_hash": hashlib.sha1(body.encode()).hexdigest()[:12],
            "effective_date": tn["ts"], "effective_date_source": "turn_ts",
        })
        # 1. markers
        for mt in M_INTENT.findall(body):
            intent["stable_intent"].append(mt.strip())
        for txt, reason in M_REJECT.findall(body):
            intent["rejected_directions"].append(
                {"what": txt.strip(), "reason": (reason or "").strip() or None, "turn": slug})
        for mt in M_OPEN.findall(body):
            intent["open_questions"].append(mt.strip())
        for goal, sel, rec in M_DECIDE.findall(body):
            intent["operator_entries"].append(
                {"ts": tn["ts"], "goal": goal.strip(), "selected": sel or slug, "record": rec or None})
        for tl in M_TRUST.findall(body):
            decisions.append(parse_trust(tl))
        for thought, obs in M_STEP.findall(body):
            st = {"step_id": f"{slug}#s", "thought": thought.strip(),
                  "action": "research", "observation": (obs or "").strip(),
                  "sources": [{"url": u} for u in URL_RE.findall(body)][:6],
                  "source_layer": "deterministic"}
            st["verdict"] = step_verdict(st)   # honest: "sourced" iff source AND observation
            steps.append(st)
        # 2. graph
        concepts, t_edges = E.wire_edges(slug, body)
        edges.extend(t_edges)
        cslugs = []
        for cslug, name, _, _ in concepts:
            cslugs.append(cslug)
            if cslug not in concept_seen:
                concept_seen[cslug] = name
        turn_concept_slugs.append(cslugs)
        # 3. fences
        ffacts, _ = E.parse_facts_fence(body)
        for f in ffacts:
            f["entity_slug"] = slug
            facts.append(f)

    # concept pages (实体注册: each named object becomes a page)
    for cslug, name in concept_seen.items():
        pages.append({"slug": cslug, "type": "concept", "title": name,
                      "compiled_truth": "", "effective_date_source": "derived"})

    # 4. classify intents
    classified = [{"intent": s, "change_classification": W.classify_change(s)}
                  for s in intent["stable_intent"]]

    # 5. optional MiroMind enrichment (ONE call)
    miro_block = None
    if use_miro and intent["open_questions"]:
        try:
            import miro
            q = ("In <=120 words, research this open question and cite sources: "
                 + intent["open_questions"][0])
            r = miro.call(q)
            for s in r["steps"]:
                s["source_layer"] = "miromind"
                s["verdict"] = step_verdict(s)   # honest: a keyword-only/empty search is "unsourced", not "pass"
                steps.append(s)
            miro_block = {"question": intent["open_questions"][0],
                          "answer": r["content"][:1200], "sources": r["sources"][:12],
                          "usage": r["usage"]}
        except Exception as ex:                       # slowness/timeout is expected — degrade honestly
            miro_block = {"error": f"{type(ex).__name__}: {ex}",
                          "note": "MiroMind deep-research is slow (9+ min); deterministic artifact stands without it"}

    # 6. trajectory stats
    regs = detect_regressions(facts)
    drift = drift_proxy(turn_concept_slugs)

    # 7. freeze (hedge scan over the assembled intent ledger)
    ledger_text = "\n".join(intent["stable_intent"]
                            + [r["what"] for r in intent["rejected_directions"]])
    frz = W.freeze(SCHEMA_VERSION, ledger_text)

    # trust metrics
    trust_summary = T.summarize(decisions)

    # 8. gate_pack — entry satisfied iff frozen AND we have facts + graph
    blockers = []
    if not frz["frozen"]:
        blockers.append(f"residual decision entropy: {frz['residual_entropy']}")
    if not facts:
        blockers.append("no grounded facts extracted")
    open_q = intent["open_questions"]
    escalation, msg = "auto", ""
    if open_q:
        escalation = "needs_user_clarification"
        msg = "Open question(s) need your call: " + " | ".join(open_q)
    gp = W.gate_pack(
        stage="compile/v%d" % SCHEMA_VERSION,
        entry_satisfied=(not blockers),
        blockers=blockers,
        required_artifact="trajectory-bootstrap.md",
        required_next="human review (上升端)",
        escalation=escalation, message_for_user=msg,
    )

    index = {
        "schema_version": SCHEMA_VERSION,
        "source_transcript": os.path.relpath(path, HERE),
        "counts": {"turns": len(turns), "pages": len(pages), "edges": len(edges),
                   "facts": len(facts), "decisions": len(decisions), "steps": len(steps),
                   "concepts": len(concept_seen),
                   "steps_sourced": sum(1 for s in steps if s.get("verdict") == "sourced"),
                   "steps_unsourced": sum(1 for s in steps if s.get("verdict") == "unsourced")},
        "intent_ledger": intent,
        "classified_intents": classified,
        "pages": pages, "edges": edges, "facts": facts, "steps": steps,
        "decisions": decisions, "trust_summary": trust_summary,
        "trajectory_stats": {"regressions": regs, "drift_proxy": drift},
        "freeze": frz, "gate_pack": gp,
        "miromind_enrichment": miro_block,
    }
    return index


# ── rendering ────────────────────────────────────────────────────────────────
def render_md(ix):
    L = []
    P = L.append
    gp = ix["gate_pack"]
    c = ix["counts"]
    P("# Trajectory — bootstrap compile of this conversation\n")
    P(f"> schema_version {ix['schema_version']} · source `{ix['source_transcript']}` · "
      f"freeze **{ix['freeze']['tag'] or 'UNFROZEN'}**\n")
    P(f"> turns {c['turns']} · concepts {c['concepts']} · edges {c['edges']} · "
      f"facts {c['facts']} · steps {c['steps']} "
      f"({c.get('steps_sourced',0)} sourced / {c.get('steps_unsourced',0)} unsourced) · "
      f"decisions {c['decisions']}\n")

    P("\n## gate_pack (wow-harness — emitted first)\n")
    P("```json")
    P(json.dumps(gp, ensure_ascii=False, indent=2))
    P("```\n")

    P("## Intent ledger (intent-ledger + wow-harness)\n")
    P("**Stable intent**")
    for s in ix["intent_ledger"]["stable_intent"]:
        cl = next((x["change_classification"] for x in ix["classified_intents"] if x["intent"] == s), "")
        P(f"- [{cl}] {s}")
    P("\n**Rejected directions** (the negative-space memory)")
    for r in ix["intent_ledger"]["rejected_directions"]:
        P(f"- ~~{r['what']}~~" + (f" — {r['reason']}" if r["reason"] else ""))
    P("\n**Open questions**")
    for q in ix["intent_ledger"]["open_questions"]:
        P(f"- {q}")
    P("\n**Operator entries**")
    for o in ix["intent_ledger"]["operator_entries"]:
        P(f"- {o['ts']} — {o['goal']} (selected: {o['selected']})")

    P("\n## Concept graph (gbrain self-wiring, zero-LLM)\n")
    typed = [e for e in ix["edges"] if e["link_type"] != "mentions"]
    P(f"_{len(typed)} typed concept→concept edges (of {len(ix['edges'])} total; rest are turn→concept `mentions`)_\n")
    for e in typed:
        P(f"- `{e['from_slug']}` —**{e['link_type']}**→ `{e['to_slug']}`  ·  _{e['context']}_")

    P("\n## Fact timeline (gbrain ## Facts fence)\n")
    P("<!--- gbrain:facts:begin -->")
    P("| # | claim | kind | confidence | visibility | notability | valid_from | valid_until | source | context | claim_metric | claim_value |")
    P("|---|-------|------|------------|------------|------------|------------|-------------|--------|---------|--------------|-------------|")
    for f in ix["facts"]:
        P(f"| {f['row']} | {f['claim']} | {f['kind']} | {f['confidence']} | {f['visibility']} | "
          f"{f['notability']} | {f.get('valid_from') or ''} | {f.get('valid_until') or ''} | "
          f"{f.get('source') or ''} | {f.get('context') or ''} | {f.get('claim_metric') or ''} | "
          f"{'' if f.get('claim_value') is None else f['claim_value']} |")
    P("<!--- gbrain:facts:end -->\n")
    P(f"_trajectory: regressions={len(ix['trajectory_stats']['regressions'])}, "
      f"drift_proxy={ix['trajectory_stats']['drift_proxy']}_\n")

    P("## ReAct steps (MiroVerse-aligned)\n")
    P("_verdict legend (honest): **sourced** = the step has a resolvable source URL "
      "AND a captured observation; **unsourced** = no resolvable source, or a source "
      "with nothing captured (e.g. an empty search). `sourced` means auditable, NOT "
      "independently verified — no second-source agreement check is performed._\n")
    for s in ix["steps"]:
        src = s.get("sources") or ([{"url": s.get("url")}] if s.get("url") else [])
        P(f"- [{s.get('source_layer','?')}] **{s.get('action')}** — {s.get('thought','')[:90]} "
          f"→ _{(s.get('observation') or '')[:80]}_  ·  verdict=`{s.get('verdict')}`  ·  {len(src)} src")

    P("\n## Did the human stay in charge? (plain count)\n")
    ts = ix["trust_summary"]
    P("```json")
    P(json.dumps(ts, ensure_ascii=False, indent=2))
    P("```")
    P(f"\n**Read in one line:** across this conversation you **caught the AI being wrong and "
      f"overrode it {ts['good_catches__overrode_ai_when_ai_was_wrong']} times**, and relied on "
      f"the AI when it was right **{ts['good_trust__relied_on_ai_when_ai_was_right']} time(s)** — "
      f"and you agreed-without-looking **{ts['times_human_agreed_without_looking']} times**. "
      f"That is the point: showing the reasoning is what let you catch the AI. "
      f"({ts['decisions_with_no_confirmed_answer_yet']} decisions had no confirmed answer yet, so we didn't score them.)\n")

    if ix["miromind_enrichment"]:
        P("## MiroMind enrichment (the one LLM call)\n")
        P("```json")
        P(json.dumps(ix["miromind_enrichment"], ensure_ascii=False, indent=2)[:2000])
        P("```")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("transcript", nargs="?",
                    default=os.path.join(HERE, "input", "this-conversation.transcript.md"))
    ap.add_argument("--miro", action="store_true", help="fire one (slow) MiroMind enrichment call")
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    args = ap.parse_args()

    ix = compile_transcript(args.transcript, use_miro=args.miro)
    os.makedirs(args.out, exist_ok=True)
    # state-file-before-artifact (wow-harness ordering): gate_pack FIRST
    json.dump(ix["gate_pack"], open(os.path.join(args.out, "gate_pack.json"), "w"),
              ensure_ascii=False, indent=2)
    json.dump(ix, open(os.path.join(args.out, "trajectory-bootstrap.index.json"), "w"),
              ensure_ascii=False, indent=2)
    open(os.path.join(args.out, "trajectory-bootstrap.md"), "w").write(render_md(ix))

    c = ix["counts"]
    print(f"compiled {c['turns']} turns → {c['concepts']} concepts, {c['edges']} edges, "
          f"{c['facts']} facts, {c['steps']} steps, {c['decisions']} decisions")
    print(f"freeze: {ix['freeze']['tag'] or 'UNFROZEN ' + str(ix['freeze']['residual_entropy'])}")
    print(f"gate_pack.entry_satisfied={ix['gate_pack']['entry_satisfied']} "
          f"escalation={ix['gate_pack']['escalation']}")
    print(f"artifacts → {os.path.relpath(args.out, HERE)}/ "
          f"(gate_pack.json, trajectory-bootstrap.index.json, trajectory-bootstrap.md)")


if __name__ == "__main__":
    main()
