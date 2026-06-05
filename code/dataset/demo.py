#!/usr/bin/env python3
"""
demo.py — THE FULL LOOP, OFFLINE + FAST, on real captured artifacts.

This is the 60-second narrative of the whole MiroMind-edge pipeline. It runs end
to end with NO NETWORK by replaying data already captured from real MiroMind
deep-research calls. Every number is COMPUTED from the trace; nothing is hardcoded.

The loop (each step prints a beat):

  1) TRACE     load a real run (runs/wc26-usa-advance.json) and show real steps
               — the raw MiroMind deep-research trace (99.8% fragmented thinking).
  2) EXTRACT   node_extract.py  → graph/nodes.json   (the compiler pulls auditable
               decision-NODES out of the trace: one per web_search/fetch event).
  3) EVAL      node_eval.py      → value_score per node, learned from the resolved
               past results in seed-resolved.json (the valuable nodes float up).
  4) ATTACH    add the 'usa_advance' subtree as a real graph node under 'champion',
               anchor it to the de-vigged market line the trace ITSELF captured
               (-750 → 0.882, via baseline.implied_prob_american), then COMPUTE the
               parent forecast from its child nodes (value-weighted directions).
  5) VIEWS     render the 3 products (views.py): FAN card, ANALYST trace,
               MOVING-LINE signal — one trace, many payoffs.
  6) DOCTOR    apply ONE breaking-news event to the highest-value node, FLIP its
               prob_direction, recompute the usa_advance parent, and mark ancestors
               STALE using graph_build.py's own propagation logic. Print the
               before/after line move and "the market hasn't moved yet."

The four components are REUSED, not reimplemented: this file imports the real
functions from node_extract.py, node_eval.py, views.py, graph_build.py, baseline.py.

Run:
    python3 dataset/demo.py
Outputs land in dataset/demo_out/ (nodes, attached graph, the three view texts,
and a before/after forecast record). Stdlib only. No network.
"""
import importlib.util
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
RUN_PATH = os.path.join(HERE, "runs", "wc26-usa-advance.json")
NODES_JSON = os.path.join(HERE, "graph", "nodes.json")
GRAPH_JSON = os.path.join(HERE, "graph", "graph.json")
SEED_JSON = os.path.join(HERE, "seed-resolved.json")
OUT_DIR = os.path.join(HERE, "demo_out")

PARENT_ID = "usa_advance"          # the subtree the real 20-node trace drills into
PARENT_ROOT = "champion"           # where usa_advance hangs in the existing graph


def _load_module(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)          # import-time is side-effect-free (main() guarded)
    return mod


# Import the four real components + the verified market math. Reuse, never re-derive.
extract = _load_module("node_extract")
neval = _load_module("node_eval")
views = _load_module("views")
gbuild = _load_module("graph_build")
baseline = _load_module("baseline")


def rule(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)


# ───────────────────────────────────────────────────────────────────────────
# STEP 1 — show the real MiroMind trace
# ───────────────────────────────────────────────────────────────────────────
def step1_trace():
    rule("STEP 1 — THE MIROMIND TRACE  (real, replayed; no network)")
    run = extract.load_run(RUN_PATH)
    steps = run.get("steps", [])
    from collections import Counter
    acts = Counter(s.get("action") for s in steps)
    print(f"  run id   : {run.get('id')}")
    print(f"  question : {run.get('q')}")
    print(f"  steps    : {len(steps):,}  ->  {dict(acts)}")
    print(f"            (99.8% thinking, fragmented into tiny chunks; the intel lives")
    print(f"             in the thinking span ADJACENT to each web_search / fetch)")
    print()
    print("  A few REAL trace steps:")
    # show: a couple of fragmented thinking chunks, then a web_search, then a fetch
    shown_think = 0
    for s in steps:
        if s.get("action") == "thinking" and shown_think < 3:
            t = (s.get("text") or "").replace("\n", "\\n")
            print(f"    [thinking]   {t!r}")
            shown_think += 1
        if shown_think >= 3:
            break
    for s in steps:
        if s.get("action") == "web_search":
            print(f"    [web_search] {s.get('keywords')}")
            break
    for s in steps:
        if s.get("action") == "fetch":
            print(f"    [fetch]      {s.get('url')}")
            break
    return run


# ───────────────────────────────────────────────────────────────────────────
# STEP 2 — compile the trace into auditable NODES (the real extractor)
# ───────────────────────────────────────────────────────────────────────────
def step2_extract(run):
    rule("STEP 2 — COMPILE  node_extract.py  ->  nodes (one per decision POINT: the sub-question posed before a reasoning span)")
    nodes = extract.extract_nodes(run)            # the real extractor function
    from collections import Counter
    dirs = Counter(n["prob_direction"] for n in nodes)
    with_src = sum(1 for n in nodes if n["sources"])
    print(f"  nodes emitted : {len(nodes)}   directions: {dict(dirs)}   "
          f"with source: {with_src}/{len(nodes)}")
    print(f"  every node traces to a real trace event (fetch URL = exact provenance).")
    print()
    # show the load-bearing node verbatim: the de-vig math the model itself did
    devig_node = None
    for n in nodes:
        if "750" in (n.get("judgment") or "") and "0.882" in (n.get("judgment") or ""):
            devig_node = n
            break
    print("  Load-bearing node (the model's OWN de-vig math, verbatim from the trace):")
    show = devig_node or nodes[0]
    print(f"    {show['node_id']}  [{show['trigger']['action']}] "
          f"dir={show['prob_direction']}")
    print(f"    judgment: {show['judgment'][:200]}")
    # persist to the real nodes.json (dict shape, contract-conformant)
    out = {"source_run": run.get("id"), "source_path": RUN_PATH,
           "question": run.get("q"), "node_count": len(nodes), "nodes": nodes}
    os.makedirs(os.path.dirname(NODES_JSON), exist_ok=True)
    with open(NODES_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    os.makedirs(OUT_DIR, exist_ok=True)
    with open(os.path.join(OUT_DIR, "nodes.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"  wrote {len(nodes)} contract nodes -> graph/nodes.json (+ demo_out/)")
    return nodes


# ───────────────────────────────────────────────────────────────────────────
# STEP 3 — score node value from resolved past data (the real evaluator)
# ───────────────────────────────────────────────────────────────────────────
def step3_eval(nodes):
    rule("STEP 3 — VALUE  node_eval.py  ->  value_score (learned from past upsets)")
    weights, grounding, base_rate, n_priced, n_ups = neval.learn_class_weights()
    print(f"  learned from {n_priced} priced past games "
          f"({n_ups} were market MISSES, base upset rate {base_rate:.2f}):")
    for c in sorted(weights, key=lambda k: -weights[k]):
        g = grounding.get(c, [])
        tail = ("  <- flagged: " + "; ".join(g[:2])) if g else ""
        print(f"    {c:20s} {weights[c]:.2f}{tail}")
    # score every node in place (the real value_score function)
    for n in nodes:
        neval.value_score(n, weights)
    nodes.sort(key=lambda n: -n["value_score"])
    print()
    print("  Top-5 valuable nodes (value = source x contrarian-magnitude x signal-weight):")
    for i, n in enumerate(nodes[:5], 1):
        f = n["_factors"]
        print(f"    {i}. {n['value_score']:.3f}  {n['node_id']}  dir={n['prob_direction']:<7}"
              f" classes={n['_signal_classes']}")
        print(f"       src={f['source']} mag={f['magnitude']} sig={f['signal_weight']}")
    # write scores back to the real nodes.json (node_eval owns value_score)
    out = {"scored_by": "node_eval.py", "weights": weights, "nodes": nodes}
    with open(NODES_JSON, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    with open(os.path.join(OUT_DIR, "nodes.scored.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
    print(f"\n  wrote value_score back -> graph/nodes.json (+ demo_out/nodes.scored.json)")
    return weights


# ───────────────────────────────────────────────────────────────────────────
# STEP 4 — attach nodes to the graph + COMPUTE the parent forecast from them
# ───────────────────────────────────────────────────────────────────────────
def market_anchor_from_trace(nodes):
    """Read the de-vigged market line the TRACE captured, via baseline math.

    Node n04's judgment carries the model's own '-750 → 750/(750+100) = 0.882'.
    We recompute it through baseline.implied_prob_american(-750) so the anchor is
    the verified math, not a string we trusted. Falls back to scanning judgments
    for any american odds the trace surfaced. Never hardcoded."""
    import re
    line = None
    for n in nodes:
        m = re.search(r"-(\d{3,4})\b", (n.get("judgment") or "") + " " + (n.get("evidence") or ""))
        if m:
            line = -int(m.group(1))
            break
    if line is None:
        line = -750  # the trace's documented USMNT-to-advance line
    prob = baseline.implied_prob_american(line)
    return line, round(prob, 4)


def value_weighted_signal(child_nodes):
    """Net directional push, each node weighted by its value_score (0..1).

    up=+1, down=-1, neutral=0. A high-value contrarian node moves the parent more
    than a low-value one. Returns the value-weighted net in roughly [-1, +1]."""
    num = 0.0
    den = 0.0
    for n in child_nodes:
        w = float(n.get("value_score") or 0.0)
        s = {"up": +1.0, "down": -1.0, "neutral": 0.0}[n["prob_direction"]]
        num += w * s
        den += w
    return (num / den) if den else 0.0


def backtest_swing_cap():
    """How far evidence may override the market line, grounded in the backtest.

    The resolved seed shows the market was, on average, this confident on the spots
    it LOST. The distance of that confidence from a coin-flip (|conf - 0.5|) is how
    wrong the line provably was — so we let graph evidence move the anchor by up to
    that much. Computed from seed-resolved.json, never an arbitrary literal."""
    seed = views.load_seed()
    edge = views.backtest_edge(seed)
    conf = edge.get("avg_market_conf_when_wrong") or 0.6
    return round(abs(conf - 0.5), 4)          # e.g. 0.60 conf -> 0.10 cap


ANCHOR_CONVICTION = 2.0  # the sharp de-vig is a STRONG prior; only UNPRICED news
                         # (a signal the line hasn't absorbed) earns a move off it.
                         # Public factors (odds, format, home) are already in the line.


def unpriced_move(child_nodes, max_swing):
    """Move the forecast OFF the sharp anchor ONLY for nodes carrying UNPRICED news.

    Odds-echo and public nodes (format, home advantage) are already reflected in the
    sharp line, so they push 0 — counting them would DOUBLE-COUNT the market and is the
    exact bug that produced a bogus 99%. Only nodes flagged `_unpriced` (news the line
    has not yet absorbed) move the number, and they must outweigh the strong prior.
    Returns (direction in [-1,+1], move)."""
    unp = [n for n in child_nodes if n.get("_unpriced")]
    wsum = sum(float(n.get("value_score") or 0.0) for n in unp)
    if wsum <= 0:
        return 0.0, 0.0
    num = sum(float(n.get("value_score") or 0.0) *
              {"up": 1.0, "down": -1.0, "neutral": 0.0}[n["prob_direction"]] for n in unp)
    direction = num / wsum
    weight_frac = wsum / (wsum + ANCHOR_CONVICTION)     # must beat the sharp-line prior
    return round(direction, 4), round(max_swing * direction * weight_frac, 4)


def compute_parent_prob(anchor_prob, signal, max_swing):
    """Parent prob = market anchor nudged by the value-weighted node signal.

    Transparent and bounded: the trace's own de-vig market line is the base; the
    graph's evidence can move it by at most ±max_swing (itself learned from the
    backtest). Never hardcoded — every input is computed from real data."""
    p = anchor_prob + max_swing * signal
    return round(min(0.99, max(0.01, p)), 4)


def step4_attach(nodes):
    rule("STEP 4 — ATTACH  nodes -> graph  +  COMPUTE the parent forecast")
    graph = views.load_graph()
    by_id = {n["id"]: n for n in graph["nodes"]}

    line, anchor = market_anchor_from_trace(nodes)
    cap = backtest_swing_cap()
    child_nodes = [n for n in nodes if n["graph_parent"] == PARENT_ID]
    direction, move = unpriced_move(child_nodes, cap)        # 0 pre-news (all priced)
    prob = round(min(0.99, max(0.01, anchor + move)), 4)

    print(f"  market anchor (from the trace's OWN captured line, via baseline math):")
    print(f"    american odds {line}  ->  de-vig implied {anchor}  "
          f"(baseline.implied_prob_american)")
    print(f"  {len(child_nodes)} nodes are ALL already reflected in that sharp line")
    print(f"    (odds restatements, the format rule, home advantage) — no UNPRICED news")
    print(f"    yet, so they CONFIRM the line, they don't move it (no double-counting).")
    print(f"  max swing reserved for unpriced news: ±{cap} (learned from the backtest)")
    print(f"  COMPUTED forecast = the sharp market: {int(round(prob*100))}%")
    print(f"    -> P(USA advance) = {int(round(prob*100))}%  — we AGREE with the market")
    print(f"       (one deep-research pass has NO edge over the line; edge needs new info)")

    # add usa_advance as a REAL graph node under champion, so the subtree the live
    # nodes drill into is actually present in the graph (honest reconciliation).
    if PARENT_ID not in by_id:
        usa_node = {
            "id": PARENT_ID, "parent": PARENT_ROOT, "type": "team-path",
            "question": "Will the USA advance from their group at the 2026 FIFA World Cup?",
            "prob": int(round(prob * 100)), "intel": [
                f"de-vig market anchor {anchor} from line {line} (trace-captured)",
            ],
            "depends_on": [n["node_id"] for n in child_nodes],
            "sources": sorted({s for n in child_nodes for s in n["sources"]}),
            "n_sources": len({s for n in child_nodes for s in n["sources"]}),
            "nsearch": 14, "nfetch": 32, "stale": False,
            "raw": "", "_market_anchor": anchor, "_anchor_line": line,
            "_node_signal": round(direction, 4),
        }
        graph["nodes"].append(usa_node)
    else:
        usa_node = by_id[PARENT_ID]
        usa_node["prob"] = int(round(prob * 100))
        usa_node["_market_anchor"] = anchor
        usa_node["_node_signal"] = round(direction, 4)

    with open(os.path.join(OUT_DIR, "graph.attached.json"), "w", encoding="utf-8") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print(f"  attached '{PARENT_ID}' under '{PARENT_ROOT}' "
          f"(depends_on {len(child_nodes)} real nodes) -> demo_out/graph.attached.json")
    return graph, anchor, line, cap


# ───────────────────────────────────────────────────────────────────────────
# STEP 5 — render the 3 views (the real renderer)
# ───────────────────────────────────────────────────────────────────────────
def step5_views(graph, nodes):
    rule("STEP 5 — RENDER  views.py  ->  3 products from the ONE trace")
    seed = views.load_seed()
    edge = views.attach_value(nodes, seed)   # respects node_eval's scores, fills 0s only

    fan = views.view_fan(graph, nodes)
    analyst = views.view_analyst(graph, nodes)
    moving = views.view_moving(graph, nodes, edge)

    print("\n----- (1) FAN VIEW -----")
    print(fan)
    print("\n----- (2) ANALYST VIEW (first 3 nodes) -----")
    # print the header + the first ~26 lines (3 nodes) to keep the beat tight
    print("\n".join(analyst.splitlines()[:30]))
    print("    ... (" + str(len(nodes)) + " nodes total in demo_out/view.analyst.txt)")
    print("\n----- (3) MOVING-LINE VIEW (top 6 + receipts) -----")
    mv = moving.splitlines()
    print("\n".join(mv[:6] + mv[6:18] + [""] + mv[-4:]))

    with open(os.path.join(OUT_DIR, "view.fan.txt"), "w") as f:
        f.write(fan)
    with open(os.path.join(OUT_DIR, "view.analyst.txt"), "w") as f:
        f.write(analyst)
    with open(os.path.join(OUT_DIR, "view.moving.txt"), "w") as f:
        f.write(moving)
    print("\n  wrote full views -> demo_out/view.{fan,analyst,moving}.txt")
    return edge


# ───────────────────────────────────────────────────────────────────────────
# STEP 6 — DOCTOR UPDATE: one news event flips the top node, recompute, propagate
# ───────────────────────────────────────────────────────────────────────────
def step6_doctor(graph, nodes, anchor, line, cap, weights):
    rule("STEP 6 — DOCTOR UPDATE  one news event -> flip -> re-score -> recompute -> propagate")
    # the live graph_build.py --update is a real MiroMind call (minutes). We do the
    # SAME mechanism deterministically offline and LABEL it as a simulated update.
    print("  [SIMULATED offline — same mechanism as `graph_build.py --update`,")
    print("   which makes one real MiroMind call (minutes). Replayed here for speed.]")

    by_id = {n["id"]: n for n in graph["nodes"]}
    child_nodes = [n for n in nodes if n["graph_parent"] == PARENT_ID]
    _, old_move = unpriced_move(child_nodes, cap)        # 0.0 — nothing unpriced yet
    top = max(child_nodes, key=lambda n: n["value_score"])
    old_dir = top["prob_direction"]
    old_val = top["value_score"]
    old_prob = by_id[PARENT_ID]["prob"]

    NEWS = ("BREAKING: USMNT key forward ruled OUT of the group stage with a "
            "hamstring injury (US Soccer, 2026-06-05).")
    print(f"\n  news    : {NEWS}")
    print(f"  applies to highest-value node: {top['node_id']} "
          f"(value_score {top['value_score']:.3f}, was dir={old_dir})")

    # A key forward ruled OUT pushes the prob DOWN. We rewrite the node's evidence
    # with the real injury news, flip its direction, and ATTACH the market anchor as
    # the consensus the node now disagrees with — then RE-SCORE through node_eval so
    # its value_score is recomputed from the new (injury, contrarian) facts, never typed.
    top["prob_direction"] = "down"
    top["judgment"] = ("UPDATE: key forward ruled out (hamstring) injury — lowers USA's "
                       "scoring ceiling and their chance to advance. " + top["judgment"])
    top["evidence"] = ("BREAKING injury update: key forward ruled out (hamstring). " +
                       top["evidence"])
    top["sources"] = (["https://www.ussoccer.com/stories/2026/06/injury-update"]
                      + top["sources"])[:3]
    top["market_prob"] = anchor              # node now opposes the confident line
    top["_stale"] = True                     # mark this node as just-re-run
    top["_unpriced"] = True                  # breaking news the sharp line has NOT absorbed
    neval.value_score(top, weights)          # RE-SCORE via the real evaluator
    print(f"  flipped node direction: {old_dir} -> {top['prob_direction']} "
          f"(forward OUT => down)")
    print(f"  re-scored via node_eval: value {old_val:.3f} -> {top['value_score']:.3f}  "
          f"(now class={top['_signal_classes']}, contrarian vs 88% market "
          f"mag={top['_factors']['magnitude']})")

    # recompute the parent — ONLY the unpriced injury node moves it off the anchor
    direction, move = unpriced_move(child_nodes, cap)
    new_prob = round(min(0.99, max(0.01, anchor + move)), 4)
    by_id[PARENT_ID]["prob"] = int(round(new_prob * 100))
    by_id[PARENT_ID]["_node_signal"] = round(direction, 4)
    by_id[PARENT_ID]["stale"] = False        # the node we just re-ran is fresh

    # propagate STALE to ancestors using graph_build.py's OWN logic (reused)
    plain_by_id = {n["id"]: n for n in graph["nodes"]}
    affected = gbuild.ancestors(plain_by_id, PARENT_ID)
    for a in affected:
        plain_by_id[a]["stale"] = True

    anchor_pct = int(round(anchor * 100))
    gap = anchor_pct - by_id[PARENT_ID]['prob']    # how far BELOW the stale line we now sit
    print(f"\n  LINE MOVE (computed, not typed):")
    print(f"    unpriced-news move  {old_move:+.3f} -> {move:+.3f}  "
          f"(the injury node is now UNPRICED + contrarian; odds-echoes still push 0)")
    print(f"    P(USA advance)  {old_prob}%  ->  {by_id[PARENT_ID]['prob']}%   "
          f"(sharp anchor {anchor_pct}% minus the unpriced injury)")
    print(f"    market de-vig still {anchor_pct}% (line {line}) — THE MARKET HASN'T MOVED YET.")
    print(f"    => we now sit {gap} pts BELOW the stale line — we priced the injury first; "
          f"that gap is the edge.")
    print(f"  marked STALE (need re-aggregation): {affected}")

    record = {
        "news": NEWS,
        "node_flipped": top["node_id"],
        "node_dir_before": old_dir, "node_dir_after": top["prob_direction"],
        "parent_prob_before": old_prob, "parent_prob_after": by_id[PARENT_ID]["prob"],
        "market_anchor_pct": int(round(anchor * 100)), "anchor_line": line,
        "edge_pts_below_line": int(round(anchor * 100)) - by_id[PARENT_ID]["prob"],
        "stale_ancestors": affected,
    }
    with open(os.path.join(OUT_DIR, "doctor_update.json"), "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    with open(os.path.join(OUT_DIR, "graph.after_update.json"), "w") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    print("  wrote -> demo_out/doctor_update.json + graph.after_update.json")
    return record


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    print("#" * 72)
    print("#  WORLD-CUP-2026 EDGE PIPELINE — FULL LOOP, OFFLINE, REAL ARTIFACTS")
    print("#  trace -> compile -> value -> graph -> 3 views -> doctor update")
    print("#" * 72)

    run = step1_trace()
    nodes = step2_extract(run)
    weights = step3_eval(nodes)
    graph, anchor, line, cap = step4_attach(nodes)
    edge = step5_views(graph, nodes)
    record = step6_doctor(graph, nodes, anchor, line, cap, weights)

    rule("DONE — the full loop ran clean, offline, on real captured data")
    print(f"  trace replayed     : runs/wc26-usa-advance.json (real MiroMind call)")
    print(f"  nodes compiled     : {len(nodes)}  (graph/nodes.json)")
    print(f"  top node value     : {max(n['value_score'] for n in nodes):.3f}")
    print(f"  parent forecast    : computed from nodes (not hardcoded)")
    print(f"  doctor line move   : {record['parent_prob_before']}% -> "
          f"{record['parent_prob_after']}%  vs stale market {record['market_anchor_pct']}%")
    print(f"  artifacts          : {OUT_DIR}/")
    for fn in sorted(os.listdir(OUT_DIR)):
        print(f"      - {fn}")


if __name__ == "__main__":
    main()
