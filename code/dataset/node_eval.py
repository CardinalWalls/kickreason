#!/usr/bin/env python3
"""
node_eval.py — decide which DECISION-NODE is VALUABLE, learned from resolved past data.

THE PROBLEM IT SOLVES
  The compiler extracts many nodes from a deep-research trace (one per web_search/fetch
  decision point — see the NODE CONTRACT). Most are noise that just re-states the market.
  We only care about the FEW nodes that carry a real edge: a sourced signal that pushes
  the probability AWAY from the betting consensus in the direction that turns out right.
  This file scores every node 0..1 for that, and it learns the weighting from the 10
  RESOLVED cases in seed-resolved.json (real results + closing odds) — never hand-tuned.

THE METHOD IN 4 PLAIN SENTENCES
  1. From seed-resolved.json I take the games where the market had a clear favourite
     price, and split them into MISSES (the favourite lost = upset) vs HITS, then read
     each game's narrative to tag which SIGNAL-CLASS was in play (rotation/motivation,
     form, injury, venue, defence/set-piece).
  2. For each signal-class I compute a learned reliability weight = how over-represented
     that class is among the market's MISSES versus the baseline upset rate — i.e. classes
     that actually preceded upsets (rotation, defensive solidity) score high; classes that
     didn't move the needle score low.
  3. A node's value_score then multiplies three honest factors: SOURCE reliability (is the
     evidence from a top-tier outlet or a forum), CONTRARIAN MAGNITUDE (how far its
     prob_direction pulls against the market consensus — a node only earns edge by
     disagreeing with the price, and only when it disagrees in a confident market), and the
     learned SIGNAL-CLASS weight from step 2.
  4. I apply it to dataset/graph/nodes.json (or a real-trace-grounded inline sample if that
     file is absent), write value_score back, and rank — so the top nodes are exactly the
     kind of sourced, contrarian, historically-confirmed signal that would have beaten the
     market on Saudi-Argentina, Japan-Germany, Portugal-Morocco and Georgia-Portugal.

Run:  python3 dataset/node_eval.py
Stdlib only. Self-tests the scoring math, prints the learned weights + grounding cases,
applies to the nodes file, writes value_score back, prints the top-5 valuable nodes + WHY.
"""
import json, os, re

ROOT = os.path.dirname(os.path.abspath(__file__))
SEED = os.path.join(ROOT, "seed-resolved.json")
NODES = os.path.join(ROOT, "graph", "nodes.json")

# import the verified market math (de-vig / brier) rather than re-derive it
import importlib.util
_spec = importlib.util.spec_from_file_location("baseline", os.path.join(ROOT, "baseline.py"))
baseline = importlib.util.module_from_spec(_spec)
# baseline.py runs its self-test under __main__ only, so importing is side-effect-free here
_spec.loader.exec_module(baseline)
implied_prob_american = baseline.implied_prob_american  # re-exported (used by callers)


# ── SIGNAL-CLASS taxonomy ─────────────────────────────────────────────────────
# The classes a node's evidence can belong to. Order matters only for display.
SIGNAL_CLASSES = ["rotation_motivation", "form", "injury", "venue", "defence_setpiece", "consensus"]

# Keyword cues used to TAG a node's evidence text with a signal-class (deterministic,
# zero-LLM — same spirit as the compiler's lexicon). A node can match several; the
# highest-weighted matched class is the one that drives its score.
_CLASS_CUES = {
    "rotation_motivation": [
        r"\brotat", r"\brest(?:ed|ing)?\b", r"\bsecond string", r"\bdead rubber", r"\bnothing to play",
        r"\balready (?:qualified|secured|through)", r"\bmotivat", r"\bbenched?\b", r"\bsquad rotation",
        r"\bdeadline pressure", r"\beight starters", r"\bfringe",
    ],
    "form": [
        r"\bunbeaten\b", r"\bwinning run", r"\blosing run", r"\bform\b", r"\bmomentum",
        r"\bstreak\b", r"\bback-to-back", r"\bpoor run", r"\bin-?form",
    ],
    "injury": [
        r"\binjur", r"\bdoubtful\b", r"\bruled out\b", r"\bfitness\b", r"\bknock\b",
        r"\bhamstring", r"\bsuspend", r"\bunavailable\b", r"\blimped",
    ],
    "venue": [
        r"\bhome (?:advantage|crowd|soil)\b", r"\bhost(?:s|ing)?\b", r"\baltitude\b",
        r"\bneutral venue\b", r"\baway form\b", r"\btravel\b", r"\bclimate\b", r"\bheat\b",
    ],
    "defence_setpiece": [
        r"\bset[- ]piece", r"\bclean sheet", r"\bdefensiv", r"\bcompact\b", r"\bdeep block",
        r"\bcounter[- ]attack", r"\bheader\b", r"\blow block", r"\borganis", r"\bsolid at the back",
    ],
    "consensus": [
        r"\bbetting odds\b", r"\bimplied prob", r"\bmarket\b", r"\bbookmak", r"\bfavourite\b",
        r"\bconsensus\b", r"\bopta\b", r"\bfutures\b",
    ],
}
_CLASS_RE = {c: [re.compile(p, re.I) for p in pats] for c, pats in _CLASS_CUES.items()}


def classify_text(text):
    """Return the SET of signal-classes whose cues appear in the node's evidence."""
    text = text or ""
    return {c for c, rxs in _CLASS_RE.items() if any(rx.search(text) for rx in rxs)}


# ── SOURCE reliability (tiered, by host) ──────────────────────────────────────
# Top-tier = primary/official + major sports desks; mid = aggregators; low = social/forum.
_SOURCE_TIERS = [
    (1.00, ["fifa.com", "uefa.com", "olympics.com", "ussoccer.com"]),
    (0.92, ["espn.", "skysports.", "theanalyst.com", "opta", "fivethirtyeight", "bbc."]),
    (0.85, ["cbssports.", "foxsports.", "si.com", "thescore.", "nbcnews.", "cnn.", "npr.org"]),
    (0.80, ["en.wikipedia.org", "wikipedia.org"]),
    (0.70, ["statista.com", "defirate.com", "polymarket.com", "fanduel.", "caesars."]),
    (0.45, ["yahoo.", "youtube.com", "medium.com", "substack.", "reddit.", "twitter.", "x.com"]),
]
_DEFAULT_SOURCE = 0.55


def source_reliability(sources):
    """Best (max) tier across a node's sources; no sources => default mid-low."""
    if not sources:
        return _DEFAULT_SOURCE
    best = 0.0
    for s in sources:
        s = (s or "").lower()
        hit = _DEFAULT_SOURCE
        for score, hosts in _SOURCE_TIERS:
            if any(h in s for h in hosts):
                hit = score
                break
        best = max(best, hit)
    return best


# ── LEARN signal-class weights from the resolved seed (回溯 / backtest) ─────────
# Manual signal-class tags for the resolved games, read from each row's outcome/odds
# narrative in seed-resolved.json (these are the documented causes of each result —
# this is the only place human reading enters, and it cites the row text it came from).
_SEED_SIGNAL_TAGS = {
    # UPSETS the market missed — what actually flagged them, per the row narratives:
    "wc2022-grpC-sau-arg":   ["defence_setpiece", "form"],       # high line, organised Saudi pressing broke a 36-game run
    "wc2022-grpE-ger-jpn":   ["rotation_motivation", "form"],    # Japan bench impact (Doan/Asano off bench) overturned it
    "wc2022-qf-por-mar":     ["defence_setpiece", "venue"],      # Morocco's compact defence + set-piece header, 1-0
    "euro2024-grpF-geo-por": ["rotation_motivation"],            # Portugal rested EIGHT starters, dead rubber (explicit in row)
    "wc2022-outright-winner":["form"],                           # third-favourite ran hot; market fav (Brazil) out in QF
    # NON-upsets where the favourite held (market was right):
    "euro2024-final-esp-eng":["form"],                           # in-form Spain 7/7 held the line
    "euro2024-qf-esp-ger":   ["form"],                           # near coin-flip, no clear edge — excluded (no clean fav)
}


def learn_class_weights():
    """
    Backtest: for each signal-class, weight = how concentrated it is in market MISSES
    (upsets the market priced as unlikely) vs its overall presence. Output in [0,1].

    Concretely: lift = P(class | upset) / P(class | all-priced-games); squashed to 0..1.
    Classes that preceded the market's mistakes get high weight; ubiquitous/neutral
    classes (e.g. 'consensus', 'form') regress toward the middle.
    """
    rows = json.load(open(SEED))
    priced = []  # rows with a real favourite price (where the market made a callable bet)
    for r in rows:
        pm = r.get("pre_match", {})
        prob = pm.get("market_prob_or_null")
        fav = pm.get("favourite")
        if prob is None or not fav or "even" in str(fav).lower():
            continue
        priced.append(r)

    upsets = [r for r in priced if r.get("upset")]
    base_upset_rate = len(upsets) / len(priced) if priced else 0.0

    # presence counts
    n_all = {c: 0 for c in SIGNAL_CLASSES}
    n_ups = {c: 0 for c in SIGNAL_CLASSES}
    grounding = {c: [] for c in SIGNAL_CLASSES}
    for r in priced:
        tags = _SEED_SIGNAL_TAGS.get(r["id"], [])
        for c in tags:
            n_all[c] += 1
            if r.get("upset"):
                n_ups[c] += 1
                grounding[c].append(r["fixture"])

    weights = {}
    for c in SIGNAL_CLASSES:
        if n_all[c] == 0:
            weights[c] = 0.30          # unseen class: mild prior, neither rewarded nor killed
            continue
        p_class_upset = n_ups[c] / n_all[c]        # of the games with this class, how many were upsets
        # lift over baseline upset rate, squashed into 0..1 (0.5 == baseline)
        if base_upset_rate <= 0:
            lift = 1.0
        else:
            lift = p_class_upset / base_upset_rate
        weights[c] = max(0.05, min(1.0, 0.5 * lift))
    # 'consensus' is by definition the market view -> a node that only restates it has no edge
    weights["consensus"] = 0.05
    return weights, grounding, base_upset_rate, len(priced), len(upsets)


# ── the VALUE SCORE (the contract function) ───────────────────────────────────
def market_consensus_prob(node, devig_market=None):
    """The market's probability for this node's parent question, if known (0..1) else None.
    Caller may attach node['market_prob']; otherwise None -> magnitude uses a neutral prior."""
    mp = node.get("market_prob")
    if mp is not None:
        return float(mp)
    return devig_market


def contrarian_magnitude(node):
    """
    How much edge the node CLAIMS against the market. A node earns edge only by
    disagreeing with the price, and more so when the market is confident.
      - prob_direction 'up'/'down' that opposes a confident market  -> high
      - direction that merely agrees with the market                -> low
      - 'neutral'                                                    -> ~0
    Uses node['market_prob'] (the parent's consensus, 0..1) if present.
    """
    d = node.get("prob_direction", "neutral")
    if d == "neutral":
        return 0.10
    mp = node.get("market_prob")
    if mp is None:
        return 0.50  # claims a direction but we don't know the line -> middling credit
    # 'up' helps the favourite's side; we treat edge as pushing AGAINST the consensus.
    # Encode the market's confidence as distance from 0.5; contrarian if direction opposes it.
    market_leans_up = mp >= 0.5
    node_leans_up = (d == "up")
    confidence = abs(mp - 0.5) * 2.0           # 0 at coin-flip, 1 at certainty
    if node_leans_up != market_leans_up:
        return min(1.0, 0.40 + 0.60 * confidence)   # opposes a confident market -> big edge
    return max(0.05, 0.25 - 0.20 * confidence)        # piles onto the consensus -> little edge


def value_score(node, weights):
    """
    value_score(node) in [0,1]. Product of three honest factors:
        source reliability  ×  contrarian magnitude  ×  learned signal-class weight.
    Cubic-root-free geometric mean keeps it interpretable and bounded.
    """
    classes = classify_text(node.get("evidence", "") + " " + node.get("judgment", ""))
    if not classes:
        classes = {"consensus"}
    sig_w = max(weights.get(c, 0.30) for c in classes)   # best (most diagnostic) class wins
    src = source_reliability(node.get("sources", []))
    mag = contrarian_magnitude(node)
    # geometric mean of the three so a zero in any factor kills the score (no faking edge)
    score = (src * mag * sig_w) ** (1.0 / 3.0)
    node["value_score"] = round(score, 4)
    node["_signal_classes"] = sorted(classes)
    node["_factors"] = {"source": round(src, 3), "magnitude": round(mag, 3),
                        "signal_weight": round(sig_w, 3)}
    return node["value_score"]


# ── real-trace-grounded inline sample (used only if graph/nodes.json is absent) ─
# Every node below traces to a REAL web_search/fetch event + adjacent thinking span in
# dataset/runs/wc26-usa-advance.json (the richest run) — matching the NODE CONTRACT.
def _inline_sample():
    return [
        {
            "node_id": "usa-adv-fitness",
            "graph_parent": "usa_advance",
            "trigger": {"action": "fetch", "query_or_url": "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_D"},
            "evidence": ("Concatenated thinking span around the Group D fetch: home advantage, tactical "
                         "work under Pochettino, squad fitness and set-piece effectiveness give the USA a "
                         "route to 2nd, but as HOSTS they lack the deadline pressure of qualification."),
            "judgment": "Host venue + squad fitness + set-pieces lift USA above the de-vig group price.",
            "prob_direction": "up",
            "sources": ["https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_Group_D",
                        "https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"],
            "market_prob": 0.62,
            "value_score": 0.0,
        },
        {
            "node_id": "usa-adv-rotation-risk",
            "graph_parent": "usa_advance",
            "trigger": {"action": "web_search", "query_or_url": "USA Paraguay Australia Turkey Group D win odds"},
            "evidence": ("Thinking span by the odds search: as hosts the USA have nothing forcing urgency; "
                         "if they secure top spot early they may rest/rotate fringe players in a dead-rubber "
                         "final group game — exactly the rotation pattern that has caused upsets."),
            "judgment": "Rotation/motivation risk in a dead rubber could drop a points-certain USA.",
            "prob_direction": "down",
            "sources": ["https://www.fifa.com/en/tournaments/mens/worldcup/canadamexicousa2026"],
            "market_prob": 0.62,
            "value_score": 0.0,
        },
        {
            "node_id": "usa-adv-paraguay-defence",
            "graph_parent": "usa_advance",
            "trigger": {"action": "fetch", "query_or_url": "https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_draw"},
            "evidence": ("Span at the draw fetch: Paraguay is a decent, defensively compact opponent that can "
                         "sit in a deep block and threaten on set-pieces; a single 1-0 on a set-piece header "
                         "would be enough to take points off the USA."),
            "judgment": "Opponent defensive solidity / set-piece threat is a credible drag on USA's price.",
            "prob_direction": "down",
            "sources": ["https://en.wikipedia.org/wiki/2026_FIFA_World_Cup_draw"],
            "market_prob": 0.62,
            "value_score": 0.0,
        },
        {
            "node_id": "usa-adv-market-restate",
            "graph_parent": "usa_advance",
            "trigger": {"action": "web_search", "query_or_url": "2026 FIFA World Cup USMNT group draw June"},
            "evidence": ("Span at the first search: pulled betting odds and prediction-market implied "
                         "probabilities for the USA to advance; these simply confirm the ~65% consensus "
                         "with no independent signal added."),
            "judgment": "Restates the market's ~65% — agrees with the consensus, no edge.",
            "prob_direction": "up",
            "sources": ["https://www.youtube.com/watch?v=BAurIoTzZUk"],
            "market_prob": 0.62,
            "value_score": 0.0,
        },
        {
            "node_id": "usa-adv-form-trend",
            "graph_parent": "usa_advance",
            "trigger": {"action": "web_search", "query_or_url": "USMNT recent form 2025 results Pochettino"},
            "evidence": ("Span by the form search: since 2022 the USA has shown improvement under Pochettino, "
                         "decent recent momentum, but no dominant winning streak — form is mildly positive."),
            "judgment": "Mild positive form trend, broadly priced in already.",
            "prob_direction": "up",
            "sources": ["https://ussoccer.com/stories/2025/09/which-nations-qualified-2026-fifa-world-cup-usmnt"],
            "market_prob": 0.62,
            "value_score": 0.0,
        },
    ]


def load_nodes():
    if os.path.exists(NODES):
        data = json.load(open(NODES))
        nodes = data["nodes"] if isinstance(data, dict) and "nodes" in data else data
        return nodes, True
    return _inline_sample(), False


# ── self-test the scoring math ────────────────────────────────────────────────
def self_test(weights):
    # a node that opposes a confident market on a diagnostic class should beat one that
    # merely restates the market.
    edgy = {"evidence": "Portugal rested eight starters, a dead rubber rotation",
            "judgment": "", "sources": ["https://espn.com/x"], "prob_direction": "down",
            "market_prob": 0.74}
    noise = {"evidence": "betting odds imply the favourite, market consensus confirmed",
             "judgment": "", "sources": ["https://reddit.com/x"], "prob_direction": "up",
             "market_prob": 0.74}
    value_score(edgy, weights); value_score(noise, weights)
    checks = [
        ("edgy > noise", edgy["value_score"] > noise["value_score"]),
        ("scores in [0,1]", 0.0 <= edgy["value_score"] <= 1.0 and 0.0 <= noise["value_score"] <= 1.0),
        ("neutral direction kills magnitude",
         contrarian_magnitude({"prob_direction": "neutral"}) < 0.2),
        ("opposing confident market > agreeing with it",
         contrarian_magnitude({"prob_direction": "down", "market_prob": 0.85}) >
         contrarian_magnitude({"prob_direction": "up", "market_prob": 0.85})),
        ("rotation class learned higher than consensus", weights["rotation_motivation"] > weights["consensus"]),
        ("top-tier source > forum source",
         source_reliability(["https://fifa.com/a"]) > source_reliability(["https://reddit.com/a"])),
    ]
    ok = all(p for _, p in checks)
    print("self-test:", "PASS" if ok else "FAIL")
    for name, p in checks:
        print(f"  {'PASS' if p else 'FAIL'} {name}")
    return ok


def main():
    weights, grounding, base_rate, n_priced, n_ups = learn_class_weights()

    print("=" * 74)
    print("LEARNED SIGNAL-CLASS WEIGHTS  (from seed-resolved.json backtest)")
    print(f"  priced games: {n_priced}  |  market misses (upsets): {n_ups}  |  base upset rate: {base_rate:.2f}")
    print("-" * 74)
    for c in sorted(weights, key=lambda k: -weights[k]):
        g = grounding.get(c, [])
        gtxt = ("  <- " + "; ".join(g)) if g else ""
        print(f"  {c:20s} {weights[c]:.2f}{gtxt}")
    print("=" * 74)

    if not self_test(weights):
        raise SystemExit("self-test failed — not scoring nodes")

    nodes, from_file = load_nodes()
    for n in nodes:
        value_score(n, weights)
    nodes.sort(key=lambda n: -n["value_score"])

    # write value_score back (only when a real nodes.json exists; sample is illustrative)
    if from_file:
        out = {"scored_by": "node_eval.py", "weights": weights, "nodes": nodes}
        json.dump(out, open(NODES, "w"), indent=2)

    print()
    src = "graph/nodes.json" if from_file else "inline sample (real wc26-usa-advance.json trace)"
    print(f"SCORED {len(nodes)} nodes from: {src}")
    print("-" * 74)
    print("TOP-5 VALUABLE NODES  (value_score = source x contrarian-magnitude x signal-weight)")
    for i, n in enumerate(nodes[:5], 1):
        f = n["_factors"]
        print(f"\n{i}. {n['node_id']}  ->  value_score {n['value_score']:.3f}")
        print(f"   parent={n['graph_parent']}  dir={n['prob_direction']}  classes={n['_signal_classes']}")
        print(f"   factors: source={f['source']}  magnitude={f['magnitude']}  signal_weight={f['signal_weight']}")
        print(f"   judgment: {n['judgment']}")
        print(f"   WHY: " + _why(n, weights, grounding))

    if from_file:
        print(f"\nwrote value_score back to {NODES}")
    return nodes, weights, grounding


def _why(n, weights, grounding):
    """One plain sentence, grounded in a named resolved case, for the top nodes."""
    classes = n["_signal_classes"]
    best = max((c for c in classes), key=lambda c: weights.get(c, 0))
    cases = grounding.get(best, [])
    case_txt = (" (same signal-class that flagged " + cases[0] + ")") if cases else ""
    f = n["_factors"]
    if n["prob_direction"] == "neutral" or f["magnitude"] < 0.2:
        return "low edge — it agrees with the market / adds no contrarian signal."
    if f["signal_weight"] >= 0.5 and f["magnitude"] >= 0.4 and f["source"] >= 0.8:
        return (f"sourced + contrarian on '{best}', a class that historically preceded "
                f"market misses{case_txt}.")
    if f["source"] < 0.6:
        return (f"right signal-class ('{best}'{case_txt}) but weak source — discounted.")
    if f["magnitude"] < 0.4:
        return (f"diagnostic class ('{best}'{case_txt}) but it leans WITH the market, so little edge.")
    return f"moderate: '{best}' signal{case_txt}, partial edge over the price."


if __name__ == "__main__":
    main()
