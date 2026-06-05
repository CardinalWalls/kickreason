#!/usr/bin/env python3
"""
arc_build.py — grade the FIFA-2022 hero arc and assemble the champion-rooted DAG.

Plain version of what this does:
  The parallel research build (workflow wc2022-arc-layers) produced dataset/arc_2022.json:
  13 marquee 2022 nodes (Argentina's title run + Morocco's run + Germany–Japan + the
  outright futures), each seen through 4 sourced professional layers
  (odds · narrative · magic_moment · stats). This script does the DETERMINISTIC part:

    1. GRADE every node's ODDS layer with the recognized rig — Brier on the real
       pre-match market probability vs what actually happened. (Imports the self-tested
       `brier` from baseline.py; no scoring method is invented here.)
    2. ASSEMBLE the champion-rooted DAG (the real tournament dependency tree) and attach
       each node's 4 layers to it.
    3. SELF-CHECK: for the four nodes we also hold in seed-resolved.json, the Brier this
       script computes MUST match the seed's number — so the arc can't silently drift.
    4. Write dataset/arc_2022.graded.json (the served artifact) + a plain dataset/arc_2022.md.

  Honesty (non-negotiable, per the project rules):
    - The odds-layer probabilities are REAL pre-match market prices, sourced in arc_2022.json.
      Nodes with no sourced price are marked "ungraded (no real price found)", never invented.
    - This is the MARKET graded on a real tournament arc — NOT a MiroMind agent track record
      (you can't backtest the agent on past games; it already knows the result). 2022 proves the
      LAYER SYSTEM + the grading; 2026 is the live agent forecast.
    - CLV (closing-line value) needs two prices (entry + close); for historical 2022 nodes we
      hold a single price, so CLV is marked n/a here — it is the LIVE-2026 metric.

Run:  python3 dataset/arc_build.py
"""
import json, os, importlib.util

ROOT = os.path.dirname(os.path.abspath(__file__))
ARC_IN = os.path.join(ROOT, "arc_2022.json")
ARC_OUT = os.path.join(ROOT, "arc_2022.graded.json")
ARC_MD = os.path.join(ROOT, "arc_2022.md")
SEED = os.path.join(ROOT, "seed-resolved.json")

# import the verified, self-tested scoring rig (de-vig / Brier) — don't re-derive it
_spec = importlib.util.spec_from_file_location("baseline", os.path.join(ROOT, "baseline.py"))
baseline = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(baseline)  # importing is side-effect-free (self-test runs under __main__)
brier = baseline.brier

COIN_FLIP = 0.25

# ── the real tournament dependency tree (champion-rooted), edges = parent -> children ──
# Argentina's title run is the spine; France's + Morocco's semifinal subtree hangs off the
# final; Germany–Japan and the outright futures are the marquee-context children of champion.
DAG_EDGES = {
    "champion":   ["arg-fra", "ger-jpn", "wc2022-winner"],
    "arg-fra":    ["arg-cro", "fra-mar"],   # the final depends on both semifinals
    "arg-cro":    ["arg-ned"],              # Argentina SF <- QF
    "arg-ned":    ["arg-aus"],              # QF <- R16
    "arg-aus":    ["arg-ksa", "arg-mex", "arg-pol"],  # R16 <- the group (incl. the Saudi shock)
    "fra-mar":    ["mar-por"],              # France's SF was vs Morocco; Morocco QF
    "mar-por":    ["mar-esp"],              # Morocco QF <- R16
    "mar-esp":    ["mar-bel"],              # Morocco R16 <- the Belgium signal-upset
}
ROOT_LABEL = {
    "id": "champion", "fixture": "Argentina — 2022 World Cup champion",
    "note": "Root of the graph. Third title; Messi's crowning. The arc below is how it was won — "
            "and where the market was confidently wrong on the moments everyone remembers.",
}

# map our arc ids -> the seed-resolved ids that hold the same game (for the drift self-check)
SEED_XCHECK = {
    "arg-ksa": "wc2022-grpC-sau-arg",
    "ger-jpn": "wc2022-grpE-ger-jpn",
    "mar-por": "wc2022-qf-por-mar",
    "wc2022-winner": "wc2022-outright-winner",
}


def grade_node(n):
    """Grade one node's odds layer. Returns the node with a computed `grade` block."""
    pm = n.get("pre_match", {}) or {}
    prob = pm.get("market_prob")
    fav = pm.get("favourite", "")
    won = (n.get("outcome", {}) or {}).get("favourite_won")
    grade = {}
    if prob is None:
        grade = {"graded": False, "reason": "ungraded — no real pre-match price found",
                 "brier": None, "clv": None}
    elif won not in (0, 1):
        grade = {"graded": False, "reason": "ungraded — outcome.favourite_won missing",
                 "brier": None, "clv": None}
    else:
        b = brier(float(prob), int(won))
        prob = float(prob); won = int(won)
        # "confidently wrong" = the market priced a CLEAR favourite (>=0.55) and that favourite LOST.
        # (A near coin-flip that resolved either way is NOT a confident miss — don't overclaim.)
        clear_fav = prob >= 0.55
        confidently_wrong = clear_fav and won == 0
        if clear_fav and won == 1:
            verdict = "market RIGHT — clear favourite held"
        elif confidently_wrong:
            verdict = "market CONFIDENTLY WRONG — clear favourite lost"
        elif won == 1:
            verdict = "near coin-flip — the priced side held"
        else:
            verdict = "near coin-flip — went the other way"
        grade = {
            "graded": True,
            "market_prob": round(prob, 4),
            "favourite": fav,
            "favourite_won": won,
            "brier": round(b, 4),
            "beats_coin_flip": b < COIN_FLIP,
            "clear_favourite": clear_fav,
            "confidently_wrong": confidently_wrong,
            "verdict": verdict,
            "clv": None,
            "clv_note": "n/a — single historical price; CLV (entry vs close) is the live-2026 metric",
        }
    n["grade"] = grade
    # mirror the grade onto the odds layer so the served layer object carries its own score
    ly = n.get("layers", {}) or {}
    od = ly.get("odds")
    if isinstance(od, dict):
        od["grade"] = grade
    return n


def self_check(nodes_by_id):
    """The four overlapping nodes MUST grade to the same Brier as seed-resolved.json."""
    if not os.path.exists(SEED):
        return True, ["(seed-resolved.json absent — skipped drift check)"]
    seed = {r["id"]: r for r in json.load(open(SEED))}
    notes, ok = [], True
    for arc_id, seed_id in SEED_XCHECK.items():
        n = nodes_by_id.get(arc_id)
        s = seed.get(seed_id)
        if not n or not s:
            notes.append(f"  ? {arc_id}: missing in arc or seed — skipped")
            continue
        g = n.get("grade", {})
        if not g.get("graded"):
            notes.append(f"  ? {arc_id}: ungraded in arc — skipped")
            continue
        sp = (s.get("pre_match", {}) or {}).get("market_prob_or_null")
        if sp is None:
            notes.append(f"  ? {arc_id}: seed has no price — skipped")
            continue
        seed_brier = brier(float(sp), 0 if s.get("upset") else 1)
        match = abs(seed_brier - g["brier"]) < 0.02
        ok = ok and match
        notes.append(f"  {'OK ' if match else 'XX '}{arc_id}: arc Brier {g['brier']:.3f} "
                     f"vs seed {seed_brier:.3f} (price {sp})")
    return ok, notes


def build_dag(nodes_by_id):
    """Return a nested champion-rooted tree of the graded nodes (for rendering)."""
    def node_view(nid):
        n = nodes_by_id.get(nid, {})
        return {
            "id": nid,
            "fixture": n.get("fixture", nid),
            "stage": n.get("stage", ""),
            "grade": n.get("grade", {}),
            "layers": n.get("layers", {}),
            "outcome": n.get("outcome", {}),
            "pre_match": n.get("pre_match", {}),
            "children": [node_view(c) for c in DAG_EDGES.get(nid, [])],
        }
    root = dict(ROOT_LABEL)
    root["children"] = [node_view(c) for c in DAG_EDGES["champion"]]
    return root


def summarize(nodes):
    graded = [n for n in nodes if n.get("grade", {}).get("graded")]
    briers = [n["grade"]["brier"] for n in graded]
    mean_b = sum(briers) / len(briers) if briers else None
    wrong = [n for n in graded if n["grade"].get("confidently_wrong")]
    clear = [n for n in graded if n["grade"].get("clear_favourite")]
    return {
        "n_nodes": len(nodes),
        "n_graded": len(graded),
        "n_ungraded": len(nodes) - len(graded),
        "mean_market_brier": round(mean_b, 4) if mean_b is not None else None,
        "n_clear_favourite": len(clear),
        "n_market_confidently_wrong": len(wrong),
        "confidently_wrong_fixtures": [n["fixture"] for n in wrong],
    }


def write_md(nodes, dag, summ, sc_ok, sc_notes):
    L = ["# FIFA 2022 — the whole arc, graded (the dream-demo proof half)",
         "",
         "> Auto-written by `python3 dataset/arc_build.py`. The odds-layer probabilities are REAL "
         "pre-match market prices (sourced in `arc_2022.json`); the Brier is **computed** by the "
         "self-tested rig in `baseline.py`. This is the MARKET graded on a real tournament arc — "
         "**not** a MiroMind agent track record (you can't backtest the agent on past games). "
         "2022 proves the **layer system + the grading**; 2026 is the live agent forecast.",
         ""]
    L.append(f"**{summ['n_nodes']} marquee nodes · {summ['n_graded']} graded · "
             f"mean market Brier {summ['mean_market_brier']} · "
             f"{summ['n_market_confidently_wrong']} where the market was confidently WRONG "
             f"(Brier > 0.25 coin-flip).**")
    L.append("")
    L.append("| Node | Stage | Favourite | Mkt% | Result | Brier | Verdict |")
    L.append("|---|---|---|---:|---|---:|---|")
    for n in nodes:
        g = n.get("grade", {})
        pm = n.get("pre_match", {})
        if g.get("graded"):
            res = "fav WON" if g["favourite_won"] else "**fav LOST**"
            L.append(f"| {n.get('fixture','')} | {n.get('stage','')} | {g['favourite']} | "
                     f"{g['market_prob']*100:.0f}% | {res} | {g['brier']:.3f} | {g['verdict']} |")
        else:
            L.append(f"| {n.get('fixture','')} | {n.get('stage','')} | {pm.get('favourite','')} | "
                     f"— | — | — | {g.get('reason','ungraded')} |")
    L.append("")
    L.append("## Drift self-check (arc Brier vs seed-resolved.json)")
    L.append("")
    L.append("```")
    L.append("PASS" if sc_ok else "FAIL")
    L += sc_notes
    L.append("```")
    L.append("")
    L.append("## The four layers per node")
    L.append("")
    L.append("Every node above carries all four professional layers in `arc_2022.graded.json`:")
    L.append("- **odds** — the prediction system (bookmaker de-vig / Opta), graded by the Brier above.")
    L.append("- **narrative** — named-source storylines (The Athletic / Guardian / Opta) that decided it.")
    L.append("- **magic_moment** — the decisive goal(s): real scorer + minute, the broadcast angle.")
    L.append("- **stats** — hard data (xG / shots / possession / set-pieces), FBref/StatsBomb/Opta-grade.")
    L.append("")
    L.append("## How to check this")
    L.append("- `python3 dataset/arc_build.py` — re-grades from `arc_2022.json`, re-runs the drift "
             "self-check, rewrites this file + `arc_2022.graded.json`.")
    L.append("- `python3 dataset/baseline.py` — the self-tested source of `brier` (prints PASS).")
    L.append("- `python3 dataset/golden_template.py` — the same rig on the upset-only seed (the anchors).")
    open(ARC_MD, "w").write("\n".join(L))


def main():
    if not os.path.exists(ARC_IN):
        raise SystemExit(f"missing {ARC_IN} — run the wc2022-arc-layers workflow first "
                         "(it writes the 13 sourced nodes here).")
    data = json.load(open(ARC_IN))
    nodes = data["nodes"] if isinstance(data, dict) and "nodes" in data else data

    for n in nodes:
        grade_node(n)
    nodes_by_id = {n.get("node_id") or n.get("id"): n for n in nodes}

    sc_ok, sc_notes = self_check(nodes_by_id)
    dag = build_dag(nodes_by_id)
    summ = summarize(nodes)

    out = {"built_by": "arc_build.py", "summary": summ, "dag": dag, "nodes": nodes,
           "self_check": {"passed": sc_ok, "notes": sc_notes},
           "honesty": ("REAL sourced pre-match prices, Brier computed by the self-tested rig. "
                       "Market graded on a real 2022 arc — NOT an agent track record. CLV is the "
                       "live-2026 metric.")}
    json.dump(out, open(ARC_OUT, "w"), indent=2, ensure_ascii=False)
    write_md(nodes, dag, summ, sc_ok, sc_notes)

    print("=" * 70)
    print(f"FIFA 2022 ARC GRADED · {summ['n_nodes']} nodes · {summ['n_graded']} graded")
    print(f"  mean market Brier: {summ['mean_market_brier']}  "
          f"(coin-flip ref = 0.25; lower = market was right)")
    print(f"  market confidently WRONG on {summ['n_market_confidently_wrong']} marquee nodes:")
    for fx in summ["confidently_wrong_fixtures"]:
        print(f"    · {fx}")
    print("-" * 70)
    print("drift self-check vs seed-resolved.json:", "PASS" if sc_ok else "FAIL")
    for ln in sc_notes:
        print(ln)
    if not sc_ok:
        raise SystemExit("drift self-check FAILED — arc Brier disagrees with seed-resolved.json")
    print("-" * 70)
    print(f"wrote {os.path.relpath(ARC_OUT, ROOT)} + {os.path.relpath(ARC_MD, ROOT)}")


if __name__ == "__main__":
    main()
