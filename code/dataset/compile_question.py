#!/usr/bin/env python3
"""
compile_question.py — THE COMPILER, refactored for the NORTH STAR.

NORTH STAR: use MiroMind to predict/reason, NOT for the final result. Aim at the
IMPORTANT, DEBATABLE questions; ship a DEBATABLE NODE + EXPERT NARRATIVE as intel.

This is the whole north-star loop in one runnable:
  important question -> MiroMind researches + reasons (sources) -> COMPILE the answer
  into a debatable intel node:
    { question, position, narrative (the expert WHY),
      arguments:[{claim, source}], counterpoint (strongest case against),
      what_would_change, confidence, resolvable + resolves_when, sources }

  python3 dataset/compile_question.py "Was Morocco's 2022 run a repeatable blueprint or variance?"
  python3 dataset/compile_question.py --from runs/ask-1.json   # compile an existing trace

Stdlib only. Saves to dataset/nodes/<slug>.json and prints the node.
"""
import json, os, re, socket, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "nodes")
API_URL = "https://api.miromind.ai/v1/chat/completions"
MODEL = os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini")

sys.path.insert(0, HERE)
import node_extract  # the decision-point segmenter: reads the trace's decision tree

# The north-star prompt: NOT "who wins". An important, debatable question answered as an
# intelligence brief — a position, the sourced WHY, the strongest counterpoint, what would
# change it — ending with a JSON fence the compiler can parse into the node.
SYSTEM = (
    "You are building ONE node of a champion-rooted World Cup 2026 forecast graph, per our node "
    "CONTRACT. Research it (current form, tactics, data, market odds); reason in steps; cite REAL "
    "sources. Be sharp and concrete — NO abstract scores or made-up weights.\n\n"
    "Answer the node through the FOUR CONTRACT LAYERS — each a CONCRETE, SOURCED view (not a vibe, not "
    "a percentage you invent):\n"
    "  - odds:         the calibrated probability + its basis — a real number from the de-vigged market "
    "line or a named supercomputer (e.g. 'Spain ~24% / +420, ESPN model'), with the source\n"
    "  - stats:        ONE hard underlying data point/pattern — xG, a rating, a form metric, a specific "
    "number — with the source\n"
    "  - narrative:    the storyline / the WHY in one sharp line — from a named outlet — with the source\n"
    "  - magic_moment: for a MATCH, the decisive moment/star to watch (or, once resolved, the goal that "
    "turned it); for the CUP, the defining storyline/star — with the source\n"
    "Give a single PROBABILITY (0-100) for THIS node's question + a prob_direction (up/down/neutral vs the market).\n"
    "Then DECOMPOSE into the CHILD QUESTIONS this node depends on (the DAG edges — a parent spawns its children).\n"
    "Strongest COUNTERPOINT + WHAT WOULD CHANGE IT.\n"
    "After a short sharp narrative, END with one fenced block exactly:\n"
    "```json\n"
    '{"probability": <0-100>, "prob_direction": "up|down|neutral", "position": "<one sharp line>",'
    ' "layers": {"odds":{"text":"<calibrated prob + basis>","source":"https://..."},'
    ' "stats":{"text":"<one hard data point>","source":"https://..."},'
    ' "narrative":{"text":"<the why, one line>","source":"https://..."},'
    ' "magic_moment":{"text":"<star/decisive moment>","source":"https://..."}},'
    ' "depends_on": ["<child sub-question>", "...3-6 children"],'
    ' "counterpoint": "<strongest case against>", "what_would_change": "<evidence that flips it>",'
    ' "confidence": "low|medium|high", "resolvable": true|false, "resolves_when": "<when/how>"}\n'
    "```\n"
    "Every source must be a real URL you actually used. Never invent one. Each layer's text must "
    "carry a real figure or a named source, not an abstract weight."
)


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    return open(p).readline().strip() if os.path.exists(p) else os.environ.get("MIROMIND_API_KEY", "")


def ground_2022():
    """The real 2022 evidence that REGULATES the reasoning (a prior/base rate, not a cold guess)."""
    try:
        s = json.load(open(os.path.join(HERE, "arc_2022.graded.json")))["summary"]
        wrong = "; ".join(s.get("confidently_wrong_fixtures", [])[:4]); mb = s.get("mean_market_brier")
    except Exception:
        wrong = "Saudi 1-2 Argentina; Germany 1-2 Japan; Morocco beat Spain; Portugal 0-1 Morocco"; mb = 0.26
    return ("REAL 2022 WORLD CUP EVIDENCE — use this as your prior / base rates; do not ignore it:\n"
            "- The pre-tournament FAVOURITE did NOT win: the market's top pick (Brazil ~13%) went out in the "
            "quarter-final; the champion, Argentina, was only the 3rd favourite. Do NOT just pick the favourite.\n"
            f"- The market was CONFIDENTLY WRONG on the marquee upsets (we graded it: mean Brier {mb}): {wrong} — "
            "compact, well-organised sides beat possession favourites.\n"
            "- The champion managed KNOCKOUT VARIANCE (Argentina won the final on penalties; late goals decided ties). "
            "Weight squad depth + penalty/extra-time resilience, not only group form.\n"
            "Let these 2022 lessons REGULATE your 2026 reasoning and your depends_on decomposition.")


def stream_call(question, timeout, grounding=None):
    msgs = [{"role": "system", "content": SYSTEM}]
    if grounding:
        msgs.append({"role": "user", "content": grounding})
    msgs.append({"role": "user", "content": question})
    print("\n----- THE PROMPT (regulates MiroMind's reasoning into a node) -----", flush=True)
    print("[system] 6 layers (odds/stats/narrative/magic/actionable/calibration) + forced depends_on decomposition", flush=True)
    if grounding:
        print("[grounding — real 2022 evidence]\n" + grounding, flush=True)
    print(f"[question] {question}\n----- end prompt -----", flush=True)
    body = json.dumps({"model": MODEL, "messages": msgs}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {load_key()}", "Content-Type": "application/json"})
    content = ""
    steps, sources = [], []          # steps = the TRACE (thinking + actions, in order)
    nsearch = nfetch = 0
    usage = None
    t0 = time.time()
    print(f"\nQ: {question}\n— MiroMind researching (live) —", flush=True)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                delta = (obj.get("choices") or [{}])[0].get("delta", {})
                for s in delta.get("reasoning_steps", []):
                    t = s.get("type")
                    if t == "thinking":
                        # the decision points live here — capture, don't drop
                        steps.append({"action": "thinking",
                                      "text": str(s.get("thought", ""))[:400]})
                    elif t == "web_search":
                        nsearch += 1
                        ws = s.get("web_search") or {}
                        kw = ws.get("search_keywords", [])
                        steps.append({"action": "web_search", "keywords": kw})
                        print(f"  search: {', '.join(kw) if isinstance(kw, list) else kw}", flush=True)
                        for r in ws.get("search_results", []):
                            if r.get("url"):
                                sources.append({"url": r["url"], "title": r.get("title", "")})
                    elif t == "fetch_url_content":
                        nfetch += 1
                        fu = s.get("fetch_url_content") or {}
                        u = fu.get("url")
                        steps.append({"action": "fetch", "url": u,
                                      "snippet": str(fu.get("snippet", ""))[:240]})
                        if u:
                            sources.append({"url": u, "title": "(fetched)"})
                if delta.get("content"):
                    content += delta["content"]
                if obj.get("usage"):
                    usage = obj["usage"]
    except Exception as e:  # noqa: BLE001
        if not (isinstance(e, (socket.timeout, TimeoutError)) or "timed out" in str(e).lower()):
            print(f"  error: {type(e).__name__}: {e}", flush=True)
    seen, flat = set(), []            # unique source URLs (flat) for the node.sources field
    for s in sources:
        u = s.get("url")
        if u and u not in seen:
            seen.add(u); flat.append(u)
    return {"content": content, "steps": steps, "sources": sources, "sources_flat": flat,
            "usage": usage, "nsearch": nsearch, "nfetch": nfetch,
            "elapsed_s": round(time.time() - t0, 1)}


def parse_fence(text):
    m = re.findall(r"```json\s*(.*?)```", text, re.DOTALL) or re.findall(r"```\s*(\{.*?\})\s*```", text, re.DOTALL)
    for b in reversed(m):
        try:
            return json.loads(b.strip())
        except json.JSONDecodeError:
            continue
    return {}


def slug(q):
    return re.sub(r"[^a-z0-9]+", "-", q.lower()).strip("-")[:48] or "question"


def compile_node(question, res):
    """THE COMPILE STEP: the research TRACE -> a debatable intel node whose STRUCTURE
    (the decision tree + the depends_on DAG edges) is READ FROM THE TRACE — the decision
    points the agent posed before each reasoning span — not coerced from a JSON fence
    MiroMind never reliably emits. The prose is kept as the narrative (the WHY). A fence,
    if one ever appears, is folded in as a bonus for the one thing the trace can't give:
    the 4 sourced CONTRACT layers."""
    text = res["content"]
    fence = parse_fence(text)                          # harmless bonus; never depended on
    narrative = re.sub(r"```json.*?```", "", text, flags=re.DOTALL).strip()

    # Read the decision tree out of the trace (the reframe). A node = a decision point.
    run = {"id": slug(question), "q": question, "content": text,
           "steps": res.get("steps") or [], "sources": res.get("sources") or []}
    tree = node_extract.extract_nodes(run)             # [root, *decision-point children]
    root = tree[0] if tree else {}
    children = tree[1:] if tree else []
    by_id = {n["node_id"]: n for n in children}
    # depends_on = the child DECISION-POINT QUESTIONS (the DAG edges, from the trace)
    dep_questions = [by_id[cid]["question"] for cid in root.get("depends_on", []) if cid in by_id]

    flat_sources = res.get("sources_flat")
    if flat_sources is None:                           # --from cached run: derive from sources
        flat_sources = list(dict.fromkeys(
            (s.get("url") if isinstance(s, dict) else s) for s in (res.get("sources") or [])))
        flat_sources = [u for u in flat_sources if u]
    node = {
        "id": slug(question),
        "question": question,
        "position": root.get("judgment") or fence.get("position") or "(see narrative)",
        "probability": fence.get("probability"),       # a number, only if a fence carried one
        "prob_direction": root.get("prob_direction") or fence.get("prob_direction"),
        "narrative": narrative,                         # the expert WHY, prose
        "layers": fence.get("layers") or {},           # 4 CONTRACT layers — fence-only (best effort)
        "depends_on": dep_questions or fence.get("depends_on") or [],  # DAG edges FROM THE TRACE
        "nodes": tree,                                 # the decision tree, READ FROM THE TRACE
        "arguments": fence.get("arguments") or [],     # legacy field (kept for back-compat)
        "counterpoint": fence.get("counterpoint") or "",
        "what_would_change": fence.get("what_would_change") or "",
        "confidence": fence.get("confidence") or "medium",
        "resolvable": fence.get("resolvable"),
        "resolves_when": fence.get("resolves_when") or "",
        "sources": flat_sources,
        "_meta": {"elapsed_s": res.get("elapsed_s"), "nsearch": res.get("nsearch"),
                  "nfetch": res.get("nfetch"), "n_sources": len(flat_sources),
                  "tokens": (res.get("usage") or {}).get("total_tokens"),
                  "n_decision_nodes": len(children),
                  "structured_from_trace": bool(children),
                  "parsed_fence": bool(fence)},
    }
    return node


def main():
    grounded = "--ground" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--ground"]
    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    os.makedirs(OUT, exist_ok=True)
    if args and args[0] == "--from":
        run = json.load(open(os.path.join(HERE, args[1])))
        q = run.get("q") or run.get("question") or "(unknown question)"
        res = {"content": run.get("answer") or run.get("content") or "", "sources": run.get("sources") or [],
               "steps": run.get("steps") or [],   # the TRACE, from the cached run
               "usage": run.get("usage"), "nsearch": run.get("n_search", 0), "nfetch": run.get("n_fetch", 0),
               "elapsed_s": run.get("elapsed_s", 0)}
    else:
        q = " ".join(args).strip() or "Who will win the 2026 FIFA World Cup, and why?"
        if not load_key():
            print("NO API KEY (.miroapi).", flush=True); raise SystemExit(2)
        grounding = ground_2022() if grounded else None
        res = stream_call(q, timeout, grounding)
        if not res["content"]:
            print("  (empty — retry once)", flush=True)
            res = stream_call(q, timeout, grounding)
    node = compile_node(q, res)
    path = os.path.join(OUT, node["id"] + ".json")
    json.dump(node, open(path, "w"), indent=2, ensure_ascii=False)
    m = node["_meta"]
    print(f"\n=== DEBATABLE INTEL NODE ({m['elapsed_s']}s · {m['n_sources']} sources "
          f"· decision_nodes={m['n_decision_nodes']} · from_trace={m['structured_from_trace']}) ===")
    print(f"POSITION    : {str(node['position'])[:140]}")
    print(f"DEPENDS_ON  : {len(node['depends_on'])} child decision points (DAG edges READ FROM THE TRACE)")
    for c in node["depends_on"][:8]:
        print(f"   → {str(c)[:96]}")
    if node["layers"]:
        print(f"LAYERS      : {len(node['layers'])} filled (from a JSON fence, if present)")
        for k, v in node["layers"].items():
            print(f"   {k:13s}: {str((v or {}).get('text',''))[:80]}")
    print(f"COUNTERPOINT: {node['counterpoint'][:120]}")
    print(f"CONFIDENCE  : {node['confidence']} · resolvable={node['resolvable']}")
    print(f"saved -> {os.path.relpath(path, HERE)}")


if __name__ == "__main__":
    main()
