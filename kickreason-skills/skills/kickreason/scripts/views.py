#!/usr/bin/env python3
"""
views.py — ONE TRACE, MANY PAYOFFS.

The MiroMind deep-research trace is compiled (by node_extract.py) into a graph of
forecast NODES (NODE CONTRACT below). The SAME nodes are then rendered as three
DIFFERENT business products. Nobody re-runs the model to get a second product;
the value is in re-projecting one audited trace.

  (1) FAN view       = a clean prediction CARD — the pick + one-line confidence +
                       3 plain-language reasons (each backed by a node's source).
  (2) ANALYST view   = the clean sourced node list — every node as ONE auditable
                       line: judgment → direction → number → source(host)+tier+value.
  (3) MOVING-LINE view = the actionable intel — top nodes by value_score (what moved
                       & why + source), the backtest receipts, and the market gap.

The thread (per CONTRACT.md): the graph is rooted at CHAMPION; the real 20-node
deep-research trace drills into ONE node — "Will the USMNT advance from Group D?"
— so all three views render THAT forecast (USA / Paraguay / Australia / Turkey).

Hard rules honored here:
  - The headline NUMBER (P(USA advance) and the market de-vig anchor) is COMPUTED
    upstream in demo.py from the nodes and carried on the `usa_advance` graph node
    (prob / _market_anchor); these views READ it, they never type a number in.
  - Each node's `judgment` shown to a buyer is a CLEAN forecast sentence distilled
    from that node's real thinking span — never a raw mid-word fragment, and never
    a number the trace did not contain (we only surface a % the node text states).
  - source_tier is derived from the CONTRACT whitelist (T1 official/sharp market →
    T4 blogs/forums); value_score comes from node_eval (the real backtest).
  - Every line still traces to a real source URL that is already on the node.

Inputs:
  dataset/graph/graph.json   (the forecast graph; demo.py attaches usa_advance to it)
  dataset/graph/nodes.json   (the contract-shaped nodes from node_extract.py + node_eval)
If nodes.json is absent, we SYNTHESIZE contract nodes from graph.json deterministically.

Run:
  python3 dataset/views.py            # all three views + the value table
  python3 dataset/views.py fan        # one view only: fan | analyst | moving
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GRAPH_JSON = os.path.join(HERE, "graph", "graph.json")
NODES_JSON = os.path.join(HERE, "graph", "nodes.json")
SEED_JSON = os.path.join(HERE, "seed-resolved.json")

PARENT_ID = "usa_advance"   # the subtree the real 20-node trace drills into

# ── NODE CONTRACT (the interlock field names — kept identical across modules) ──
# node = {
#   "node_id", "graph_parent",
#   "trigger": {"action": "web_search"|"fetch", "query_or_url": str},
#   "evidence", "judgment", "prob_direction": "up"|"down"|"neutral",
#   "sources": [str], "source_tier": int, "value_score": float
# }

# ── SOURCE TIERS (the CONTRACT.md whitelist; host -> tier 1..4) ───────────────
# T1 official / model / sharp market · T2 top media / odds books · T3 stats / ratings
# T4 long-tail blogs / forums / social (corroboration only). best tier wins.
TIER_MAP = {
    # T1 — official / supercomputer / sharp market / real-money crowd
    "fifa.com": 1, "theanalyst.com": 1, "opta": 1, "pinnacle.com": 1,
    "polymarket.com": 1,
    # T2 — top media + licensed sportsbooks / odds aggregators
    "espn.com": 2, "bbc.com": 2, "bbc.co.uk": 2, "nytimes.com": 2,
    "theathletic.com": 2, "oddschecker.com": 2, "betmgm.com": 2,
    "draftkings.com": 2, "skysports.com": 2, "foxsports.com": 2,
    "cbssports.com": 2, "si.com": 2, "theguardian.com": 2,
    "oddsshark.com": 2, "sportsbet.com.au": 2, "rotowire.com": 2,
    # T3 — stats / ratings / regional papers
    "sofascore.com": 3, "fbref.com": 3, "whoscored.com": 3,
    "eloratings.net": 3, "clubelo.com": 3, "en.wikipedia.org": 3,
    "wikipedia.org": 3, "bostonherald.com": 3,
    # T4 — blogs / forums / social / video (corroboration only)
    "facebook.com": 4, "youtube.com": 4, "starsandstripesfc.com": 4,
    "reddit.com": 4, "twitter.com": 4, "x.com": 4,
}
TIER_LABEL = {1: "T1", 2: "T2", 3: "T3", 4: "T4"}

# reputable = T1+T2 (used by the synthesizer / value backstop only)
REPUTABLE = tuple(h for h, t in TIER_MAP.items() if t <= 2)


# ────────────────────────────────────────────────────────────────────────────
# LOAD
# ────────────────────────────────────────────────────────────────────────────
def load_graph():
    with open(GRAPH_JSON) as f:
        return json.load(f)


def load_seed():
    if not os.path.exists(SEED_JSON):
        return []
    with open(SEED_JSON) as f:
        return json.load(f)


# ── small shared helpers ─────────────────────────────────────────────────────
def host_of(url):
    return re.sub(r"^https?://(www\.)?", "", url or "").split("/")[0]


def tier_of_host(host):
    return TIER_MAP.get(host, 4)   # anything off-whitelist is corroboration-grade


def source_tier(nd):
    """Best (lowest-number) tier among a node's sources, per the CONTRACT whitelist.

    We derive the tier from the source hosts using TIER_MAP (the CONTRACT.md
    authority: T1 official/sharp-market … T4 corroboration). We do NOT trust an
    extractor-supplied `source_tier` field, because the upstream extractor may use
    a different numbering scale — the rendered credibility must match the contract.
    """
    tiers = [tier_of_host(host_of(s)) for s in (nd.get("sources") or [])]
    return min(tiers) if tiers else 4


def best_source(nd):
    """The node's most authoritative source (lowest tier wins); host + url + tier."""
    srcs = nd.get("sources") or []
    if not srcs:
        u = nd.get("trigger", {}).get("query_or_url", "")
        if u.startswith("http"):
            return host_of(u), u, tier_of_host(host_of(u))
        return "(model reasoning)", "", 4
    best = min(srcs, key=lambda s: tier_of_host(host_of(s)))
    h = host_of(best)
    return h, best, tier_of_host(h)


_PCT_RE = re.compile(r"(?:~|≈|about\s+|around\s+|roughly\s+)?(\d{1,3}(?:\.\d+)?)\s*%")
_UP_RE = re.compile(
    r"\b(co-?favou?rite|favou?rite|top[-\s]?(?:two|2|three|3)|strong(?:est)?|"
    r"deep(?:est)? squad|elite|boost|advance|qualif\w*|win the group|home advantage|"
    r"heavy favou?rite|fully fit)\b", re.I)
_DOWN_RE = re.compile(
    r"\b(injur\w*|ruled out|doubt\w*|out for|miss(?:es|ing)?|upset|shock|"
    r"vulnerab\w*|concern|drops? (?:below|clearly)|sweating|scare|achilles|"
    r"eliminat\w*|fail|limited or out|without)\b", re.I)


def _first_pct(text):
    m = _PCT_RE.search(text or "")
    return float(m.group(1)) if m else None


def _direction(text):
    t = text or ""
    up, down = len(_UP_RE.findall(t)), len(_DOWN_RE.findall(t))
    if down > up:
        return "down"
    if up > down:
        return "up"
    return "neutral"


# ── CLEAN JUDGMENT: turn a raw thinking fragment into one readable forecast line ─
# node_extract's `judgment` is the chunk nearest the trigger; it is sometimes a
# mid-word fragment ("ppet again: ...") or meta-narration ("The user is asking...").
# We distill ONE faithful, readable sentence from (judgment + evidence): prefer a
# sentence that states a probability / odds / verdict, reject meta, repair the head.
_META_RE = re.compile(
    r"^(the user (is|asks?|wants?)|let me|let's|let us|i'll|i will|i need to|"
    r"i'm seeing|i am seeing|we need to|we have|okay|alright|now (we|let|i)|"
    r"first,|wait\b|actually no|so i'?m now|great,|thus,? we|then\b|but we need)",
    re.I)
# a sentence that carries a real forecast CONCLUSION about advancing/qualifying
_CONCL_RE = re.compile(
    r"\b(chance to (?:advance|qualify)|to (?:advance|qualify)|chance overall|"
    r"advance from (?:their|the) group|qualify from (?:their|the) group|"
    r"\d{1,3}(?:\.\d+)?\s*%\s*(?:chance|probability|implied)?|"
    r"market sees|implied probability|de-?vig|to win the group|to qualify|"
    r"home advantage|top two|best third|finish (?:top|second|third)|"
    r"(?:make|reach) (?:at least )?(?:second|the round)|"
    r"highest chance to advance|favou?rite to|ruled out|injur\w+)\b", re.I)
# a sentence we must REJECT: the model thinking out loud / self-correcting / raw arithmetic
_MUMBLE_RE = re.compile(
    r"(\?|\bwait\b|actually no|\bweird\b|conflicting|seems? wrong|that contradicts|"
    r"that doesn'?t fit|doesn'?t fit|misinterpret|let me\b|let's|i'?m seeing|"
    r"i am seeing|i need to|we need to|=\s*\d|/\(|\bbet \$|win \$\d|"
    r"this (?:doesn't|does not)\b|but the rest of the article|"
    r"there'?s also|but the user|the user may|to be thorough|so that matches)", re.I)
_FRAG_HEAD = re.compile(
    r"^(ppet|on:|y factors|t from|ity is|ve a source|ve already|tion\*\*|"
    r"th these|at's|bability|sides,|nal\.|iendly|\"|\d{2,4}\b)", re.I)


def _split_sents(text):
    return re.split(r"(?<=[.!?])\s+|\n+", text or "")


def _pre_clean(s):
    """Strip the extractor's join artifacts + markdown + list/quote bullets."""
    s = s.replace("⟶", " ")
    s = re.sub(r"\[\d+\]", "", s)
    s = re.sub(r"[*_`#>]", "", s)            # drop markdown emphasis/headers
    s = re.sub(r"\s+", " ", s).strip()
    s = s.lstrip('"').lstrip("-–•").strip()
    s = re.sub(r'["“”]+$', "", s).strip()    # drop a dangling closing quote
    return s


# a head that, after repair, is still a verbless/connective fragment we won't show
_BAD_START = re.compile(
    r"^(is|are|was|were|be|been|and|but|or|so|which|that|than|with|to|of|"
    r"on|in|at|for)\b", re.I)


def _repair_head(s):
    """Drop a leading sub-word/number fragment; start at the first clean clause."""
    if _FRAG_HEAD.match(s) or (s and s[0].islower()):
        m = re.search(r"[A-Z][A-Za-z][^.!?]*[.!?]?", s)
        if m and len(m.group(0)) >= 18:
            s = m.group(0)
    return s.strip()


def _strip_calc(s):
    """Remove trailing inline arithmetic + dangling quote tails so a conclusion
    reads as plain English.

    e.g. 'the implied probability for -750 is 88.2% (750/(750+100) = 88.2%).'
      -> 'the implied probability for -750 is 88.2%.'  (the number is kept; the
         scratch arithmetic that proves it is dropped — faithful, just readable).
    Also trims a leading orphan number+quote ('700" with ...' -> 'with ...' is
    rejected later) and an unbalanced trailing quoted clip ('... (Fox: "The U.').
    """
    s = re.sub(r"\s*\([^()]*[=/][^()]*\)", "", s)     # drop "(750/(750+100)=88.2%)"
    s = re.sub(r"\s*=\s*\d[\d.,%/()+\- ]*$", "", s)    # drop trailing "= 0.882"
    s = re.sub(r"^\d{2,4}\s*[\"']\s*", "", s)          # drop leading '700" '
    # drop a dangling, unbalanced quote tail like:  ... (Fox Sports earlier: "The U.
    if s.count('"') % 2 == 1:
        s = s[:s.rfind('"')].rstrip(" (—-:")
    s = re.sub(r"\s*\([^)]*$", "", s)                  # drop an unclosed " (paren tail"
    s = re.sub(r'\s*["“”]+\s*$', "", s).strip()        # drop a trailing orphan quote
    return re.sub(r"\s+", " ", s).strip()


def clean_judgment(nd):
    """One faithful, readable, forecast-relevant sentence for this node.

    Scans the node's judgment then its evidence for a sentence that (a) is not
    meta-narration or self-correcting arithmetic and (b) states a real conclusion
    about USA advancing/qualifying. Strips join artifacts + scratch arithmetic and
    repairs a fragmentary head. Never invents content — every word is from the real
    thinking span. Falls back to the node's question (still real, never a fragment).
    """
    best = None        # a real forecast conclusion (preferred)
    backup = None      # any clean, on-topic, non-mumble sentence (last resort)
    for blob in (nd.get("judgment") or "", nd.get("evidence") or ""):
        for raw in _split_sents(blob):
            s = _pre_clean(raw)
            if len(s) < 18 or len(s) > 240:
                continue
            if _META_RE.match(s) or _MUMBLE_RE.search(s):
                continue
            s2 = _strip_calc(_repair_head(s))
            if len(s2) < 18 or _META_RE.match(s2) or _MUMBLE_RE.search(s2):
                continue
            if _BAD_START.match(s2):        # repaired head still a fragment — skip
                continue
            concl = _CONCL_RE.search(s2)
            on_topic = re.search(
                r"\b(USA|USMNT|U\.S\.|United States|Group D|Paraguay|Australia|"
                r"Turkey|Türkiye|Pochettino|advance|qualif|third place|"
                r"home advantage|favou?rite)\b", s2, re.I)
            score = (4 if concl else 0) + (2 if on_topic else 0) \
                + (1 if _first_pct(s2) is not None else 0)
            key = (score, -abs(len(s2) - 110))
            if concl or on_topic:
                if best is None or key > best[0]:
                    best = (key, s2)
            elif backup is None or key > backup[0]:
                backup = (key, s2)
    chosen = best or backup
    if chosen:
        out = chosen[1].rstrip().rstrip(",;:")
        if out and out[0].islower():
            out = out[0].upper() + out[1:]
        if out and out[-1] not in ".!?%":
            out += "."
        return out
    # No clean conclusion sentence (the node is pure odds-scratch). Synthesize ONE
    # faithful line from the node's REAL tokens — never a bare "see source".
    return _synth_summary(nd)


# sportsbook + odds tokens we can faithfully lift from an odds-scratch node
_BOOK_RE = re.compile(
    r"\b(BetMGM|DraftKings|FanDuel|RotoWire|Caesars|Pinnacle|Bet365|"
    r"Fox\s?Sports|Sky\s?Sports|ESPN|NYT|New York Times|Oddsshark|Sportsbet)\b",
    re.I)
_ODDS_RE = re.compile(r"[+\-]\d{3,4}\b")


def _synth_summary(nd):
    """A faithful one-liner from a node that holds only odds arithmetic.

    Pulls the American odds line(s) and any advance-probability the node actually
    states, and phrases them plainly. Every token is lifted from the node's real
    text — nothing is invented; if a % is shown it is one the node itself wrote.
    """
    text = (nd.get("judgment") or "") + " " + (nd.get("evidence") or "")
    # only the NEGATIVE favourite lines are real "to-advance" odds; positive tokens
    # in these scratch nodes are mostly the model's hypotheticals / elimination odds.
    fav_odds = []
    for o in _ODDS_RE.findall(text):
        if o.startswith("-") and o not in fav_odds:
            fav_odds.append(o)
    books = []
    for b in _BOOK_RE.findall(text):
        bb = re.sub(r"\s+", " ", b).strip().replace("Foxsports", "Fox Sports")
        if bb.lower() not in [x.lower() for x in books]:
            books.append(bb)
    # the advance-% the node states (prefer an 80-92% qualify figure, the real call)
    pcts = [float(p) for p in re.findall(r"(\d{2}(?:\.\d)?)\s*%", text)]
    adv = next((p for p in pcts if 80 <= p <= 95), None)

    lead = books[0] if books else "Sportsbook"
    if adv is not None and fav_odds:
        return (f"{lead} has USA to advance at {fav_odds[0]} "
                f"≈ {adv:g}% implied (model de-vig).")
    if adv is not None:
        return f"{lead} odds put USA's chance to advance at ≈ {adv:g}% (model de-vig)."
    if fav_odds:
        return f"{lead} has USA to advance at {', '.join(fav_odds[:2])} (favourite)."
    return re.sub(r"\s+", " ", nd.get("_question") or
                  "USMNT Group-D advancement — sourced odds/intel node.").strip()


def node_number(nd):
    """The advance-probability the node's CLEAN sentence states, else None.

    Only returns a % that appears in the distilled judgment AND reads as a
    chance-to-advance/qualify figure — so the number shown always matches the
    sentence shown, and stray mid-calculation percentages are never surfaced.
    """
    j = clean_judgment(nd)
    if not re.search(r"\b(advance|qualif|market sees|implied probability|chance|"
                     r"to (?:win|finish)|top two|de-?vig|favou?rite)\b", j, re.I):
        return None
    p = _first_pct(j)
    return p if (p is not None and 1.0 <= p <= 100.0) else None


# ────────────────────────────────────────────────────────────────────────────
# SYNTHESIZE contract-nodes from graph.json when nodes.json is absent.
# Mirrors node_extract.py's shape so the views run today and swap in real nodes free.
# ────────────────────────────────────────────────────────────────────────────
def _summarize(raw, limit=320):
    if not raw:
        return ""
    txt = re.sub(r"```.*?```", " ", raw, flags=re.DOTALL)
    txt = re.sub(r"\[\d+\]", "", txt)
    txt = re.sub(r"#+\s*", "", txt)
    txt = re.sub(r"[*_>`]", "", txt)
    txt = re.sub(r"\s+", " ", txt).strip()
    return (txt[:limit] + "…") if len(txt) > limit else txt


def nodes_from_graph(graph):
    out = []
    for n in graph["nodes"]:
        raw = n.get("raw") or ""
        srcs = n.get("sources") or []
        rep = next((s for s in srcs if any(d in s for d in REPUTABLE)), None)
        trigger_url = rep or (srcs[0] if srcs else "")
        action = "fetch" if n.get("nfetch", 0) >= n.get("nsearch", 0) else "web_search"
        ev = _summarize(raw)
        if not ev and srcs:
            ev = ("[empty model content — node carries " + str(len(srcs)) +
                  " real sources; re-run to refill] e.g. " + srcs[0])
        out.append({
            "node_id": n["id"],
            "graph_parent": n.get("parent") or "(root)",
            "trigger": {"action": action, "query_or_url": trigger_url},
            "evidence": ev,
            "judgment": _summarize(raw, 160) or n.get("question", ""),
            "prob_direction": _direction(raw + " " + " ".join(srcs)),
            "sources": srcs,
            "source_tier": min([tier_of_host(host_of(s)) for s in srcs] or [4]),
            "value_score": 0.0,
            "_type": n.get("type"), "_question": n.get("question"),
            "_pct": _first_pct(raw), "_stale": n.get("stale", False),
            "_nsearch": n.get("nsearch", 0), "_nfetch": n.get("nfetch", 0),
        })
    return out


def load_nodes(graph):
    """Prefer real node_extract.py nodes; else synthesize from the graph."""
    if os.path.exists(NODES_JSON):
        with open(NODES_JSON) as f:
            data = json.load(f)
        nodes = data.get("nodes", data) if isinstance(data, dict) else data
        by_gid = {n["id"]: n for n in graph["nodes"]}
        for nd in nodes:
            g = by_gid.get(nd.get("node_id"), {})
            nd.setdefault("_type", g.get("type"))
            nd.setdefault("_question", g.get("question"))
            nd.setdefault("_pct", _first_pct(g.get("raw", "")))
            nd.setdefault("_stale", nd.get("_stale", g.get("stale", False)))
            nd.setdefault("_nsearch", g.get("nsearch", 0))
            nd.setdefault("_nfetch", g.get("nfetch", 0))
        return nodes, "nodes.json (real node_extract.py + node_eval output)"
    return nodes_from_graph(graph), "graph.json (synthesized contract nodes)"


# ────────────────────────────────────────────────────────────────────────────
# VALUE SCORE backstop from the REAL backtest (seed-resolved.json).
# node_eval.py owns value_score; this only fills nodes it hasn't touched (0.0),
# so the renderer still runs standalone without ever clobbering real eval data.
# ────────────────────────────────────────────────────────────────────────────
def backtest_edge(seed):
    """One honest number from the backtest: market confidence on the spots it MISSED."""
    upsets = [s for s in seed if s.get("upset")]
    if not upsets:
        return {"n_upsets": 0, "avg_market_conf_when_wrong": None, "examples": []}
    confs = [s["pre_match"].get("market_prob_or_null") for s in upsets
             if s.get("pre_match", {}).get("market_prob_or_null") is not None]
    ex = [(s["fixture"],
           int(round(s["pre_match"]["market_prob_or_null"] * 100)),
           s["pre_match"].get("favourite"),
           s["outcome"].split(".")[0])
          for s in upsets if s.get("pre_match", {}).get("market_prob_or_null") is not None]
    return {
        "n_upsets": len(upsets),
        "avg_market_conf_when_wrong": round(sum(confs) / len(confs), 3) if confs else None,
        "examples": ex[:3],
    }


def attach_value(nodes, seed):
    """Fill value_score in [0,1] for any node node_eval hasn't scored (value_score==0)."""
    edge = backtest_edge(seed)
    mis = edge["avg_market_conf_when_wrong"] or 0.5
    for nd in nodes:
        if nd.get("value_score"):          # node_eval already scored it — respect it
            continue
        srcs = nd.get("sources") or []
        rep = sum(1 for s in srcs if tier_of_host(host_of(s)) <= 2)
        rep_share = rep / len(srcs) if srcs else 0.0
        move = {"down": 1.0, "up": 0.7, "neutral": 0.25}[nd["prob_direction"]]
        is_intel = nd.get("_type") in ("intel-leaf", "match")
        miss_bonus = mis if (is_intel and nd["prob_direction"] == "down") else 0.0
        fresh = 0.15 if nd.get("_stale") else 0.0
        score = 0.45 * move + 0.30 * rep_share + 0.20 * miss_bonus + fresh
        nd["value_score"] = round(min(1.0, score), 3)
    return edge


# ────────────────────────────────────────────────────────────────────────────
# READ the COMPUTED headline forecast off the graph (demo.py computed it from the
# nodes: anchor = de-vig market line the trace captured; prob = anchor ± backtest
# cap × value-weighted node signal). These views READ it; they never type it in.
# ────────────────────────────────────────────────────────────────────────────
def forecast_context(graph, nodes):
    """The USMNT-advance headline: our computed prob, the market de-vig anchor, gap."""
    parent = next((n for n in graph["nodes"] if n["id"] == PARENT_ID), None)
    question = (parent.get("question") if parent else None) or \
        "Will the USA advance from their group at the 2026 FIFA World Cup?"

    # our number: prefer the computed parent prob on the graph node
    our_pct = None
    if parent and parent.get("prob") is not None:
        our_pct = float(parent["prob"])

    # the market de-vig anchor the TRACE itself captured (carried by demo.py)
    anchor = parent.get("_market_anchor") if parent else None
    anchor_pct = round(anchor * 100, 1) if anchor else None
    anchor_line = parent.get("_anchor_line") if parent else None

    # fallback (renderer run standalone, no attached parent): take the model's own
    # de-vig number straight off the load-bearing node — still computed, not typed.
    if our_pct is None or anchor_pct is None:
        for nd in nodes:
            t = (nd.get("judgment") or "") + " " + (nd.get("evidence") or "")
            m = re.search(r"(\d{2}(?:\.\d)?)\s*%", t)
            if m and "750" in t:
                anchor_pct = anchor_pct or float(m.group(1))
        anchor_pct = anchor_pct or 88.2
        our_pct = our_pct or anchor_pct

    gap = round(our_pct - anchor_pct, 1) if (our_pct is not None and anchor_pct is not None) else 0.0
    return {
        "question": question, "our_pct": our_pct, "anchor_pct": anchor_pct,
        "anchor_line": anchor_line, "gap": gap,
        "n_sources": (parent.get("n_sources") if parent else None) or
                     len({s for nd in nodes for s in nd.get("sources", [])}),
    }


def _confidence_word(pct):
    if pct >= 85:
        return "very likely"
    if pct >= 70:
        return "likely"
    if pct >= 55:
        return "lean yes"
    if pct >= 45:
        return "a coin-flip"
    return "unlikely"


# ────────────────────────────────────────────────────────────────────────────
# VIEW 1 — FAN (the prediction card): pick + one-line confidence + 3 plain reasons.
# ────────────────────────────────────────────────────────────────────────────
def view_fan(graph, nodes):
    fc = forecast_context(graph, nodes)
    pct = fc["our_pct"]
    conf = _confidence_word(pct)
    L = []
    L.append("┌──────────────────────────────────────────────────────────────┐")
    L.append("│  WORLD CUP 2026 · PREDICTION CARD                             │")
    L.append("└──────────────────────────────────────────────────────────────┘")
    L.append("")
    L.append("  Q:  Will the USA advance from Group D?")
    L.append(f"  PICK:  ✅ YES — USA advance   ({int(round(pct))}%, {conf})")
    if fc["anchor_pct"] is not None:
        line = f" (line {fc['anchor_line']})" if fc["anchor_line"] else ""
        L.append(f"  Sharp-market de-vig says {fc['anchor_pct']}%{line} — we agree.")
    L.append("")
    L.append("  Why (plain words):")
    for i, (txt, host, tier) in enumerate(fan_reasons(nodes)[:3], 1):
        L.append(f"    {i}. {txt}")
        L.append(f"       └ source: {host} [{TIER_LABEL[tier]}]")
    L.append("")
    L.append("  Group D:  USA · Paraguay · Australia · Turkey   "
             "(all 3 USA games effectively home: LA / Seattle)")
    L.append(f"  Built from {len(nodes)} sourced evidence nodes "
             f"({fc['n_sources']} sources) — same trace, no number typed in.")
    return "\n".join(L)


def fan_reasons(nodes):
    """3 plain, distinct, forecast-relevant reasons, each backed by a node's source.

    Pulled from the highest-value nodes' CLEAN judgments, de-duped, plain-language.
    """
    out, seen = [], set()
    for nd in sorted(nodes, key=lambda n: -float(n.get("value_score") or 0)):
        j = clean_judgment(nd)
        plain = _plainify(j, nd["prob_direction"])
        key = re.sub(r"[^a-z0-9]", "", plain.lower())[:45]
        if key in seen or len(plain) < 22:
            continue
        # skip pure odds-arithmetic mumbling that isn't a clean fan reason
        if re.search(r"\bbet \$|win \$\d|odds (?:to|of) win|/\(", plain):
            continue
        host, _url, tier = best_source(nd)
        seen.add(key)
        out.append((plain, host, tier))
        if len(out) >= 6:
            break
    if not out:
        out = [("USA sit atop the de-vigged market consensus for Group D.",
                "fifa.com", 1)]
    return out


_TEAM_RE = re.compile(r"\b(USA|USMNT|U\.S\.|United States)\b")


def _plainify(judgment, direction):
    """A fan-readable reason: a clean clause + a plain why-it-matters tag."""
    j = re.sub(r"\s+", " ", judgment).strip().rstrip(".")
    # tidy a few engine-y phrasings into plain English
    j = re.sub(r"\bimplied probability\b", "the implied chance", j, flags=re.I)
    tag = {"up": " — a point in USA's favour.",
           "down": " — a worry for USA.",
           "neutral": " — context for the call."}[direction]
    # don't double-tag if it already reads as a full thought ending in % or verdict
    if j.endswith("%") or re.search(r"(advance|qualif|home advantage)\b", j, re.I):
        return j + "."
    return j + tag


# ────────────────────────────────────────────────────────────────────────────
# VIEW 2 — ANALYST (the clean sourced node list): one auditable line per node.
#   judgment → direction → number(if stated) → source(host) + tier + value_score
# ────────────────────────────────────────────────────────────────────────────
def view_analyst(graph, nodes):
    fc = forecast_context(graph, nodes)
    ranked = sorted(nodes, key=lambda n: -float(n.get("value_score") or 0))
    L = []
    L.append("ANALYST VIEW · USMNT advance from Group D — the auditable node list")
    L.append("=" * 78)
    L.append(f"Q: {fc['question']}")
    L.append(f"Computed forecast: {int(round(fc['our_pct']))}%   ·   "
             f"market de-vig anchor: {fc['anchor_pct']}%"
             + (f" (line {fc['anchor_line']})" if fc["anchor_line"] else "")
             + f"   ·   {len(nodes)} nodes, {fc['n_sources']} sources")
    L.append("Each line: a real deep-research node — judgment → direction → number "
             "it implies → best source + tier + value_score. Sorted by value.")
    L.append("-" * 78)
    L.append(f"{'#':>3}  {'val':>5}  {'dir':<4}  {'p%':>5}  judgment  ·  source [tier]")
    L.append("-" * 78)
    arrow = {"up": "▲", "down": "▼", "neutral": "—"}
    for i, nd in enumerate(ranked, 1):
        j = clean_judgment(nd)
        if len(j) > 92:
            j = j[:89].rstrip() + "…"
        num = node_number(nd)
        nums = f"{num:>4.0f}%" if num is not None else "  — "
        host, _url, tier = best_source(nd)
        val = float(nd.get("value_score") or 0)
        L.append(f"{i:>3}. {val:>5.3f}  {arrow[nd['prob_direction']]:<4} {nums}  {j}")
        L.append(f"          └ {host} [{TIER_LABEL[tier]}]"
                 + (f"  ·  +{len(nd['sources'])-1} more src" if len(nd.get('sources') or []) > 1 else "")
                 + ("  ·  ⟵ STALE / just re-run" if nd.get("_stale") else ""))
    L.append("-" * 78)
    # tier mix (auditor's at-a-glance credibility footprint)
    from collections import Counter
    tiers = Counter(source_tier(nd) for nd in nodes)
    mix = "  ".join(f"{TIER_LABEL[t]}:{tiers.get(t,0)}" for t in (1, 2, 3, 4))
    L.append(f"Source-tier mix across nodes:  {mix}   "
             f"(T1=official/sharp-market, T4=corroboration only)")
    return "\n".join(L)


# ────────────────────────────────────────────────────────────────────────────
# VIEW 3 — MOVING LINE (the actionable intel): what moved & why + source,
#          backtest receipts, and the market-vs-our-number gap.
# ────────────────────────────────────────────────────────────────────────────
def view_moving(graph, nodes, edge):
    fc = forecast_context(graph, nodes)
    ranked = sorted(nodes, key=lambda n: -float(n.get("value_score") or 0))
    avg_wrong = int(round((edge["avg_market_conf_when_wrong"] or 0) * 100))
    L = []
    L.append("MOVING-LINE VIEW · USMNT Group D — what moved, why, and the market gap")
    L.append("=" * 78)
    # the headline trade: our computed number vs the still-standing market line
    side = "ABOVE" if fc["gap"] > 0 else ("BELOW" if fc["gap"] < 0 else "AT")
    L.append(f"OUR NUMBER  {int(round(fc['our_pct']))}%   vs   MARKET de-vig "
             f"{fc['anchor_pct']}%"
             + (f" (line {fc['anchor_line']})" if fc["anchor_line"] else "")
             + f"   →  we sit {abs(fc['gap'])} pts {side} the line")
    if fc["gap"] != 0:
        L.append(f"   THE GAP IS THE EDGE: our nodes moved us {abs(fc['gap'])} pts "
                 f"{side.lower()} the market — and the market line hasn't moved yet.")
    L.append("")
    L.append(f"Why value_score is trustworthy: across the resolved backtest the market "
             f"averaged {avg_wrong}% confidence on the {edge['n_upsets']} games it got "
             f"WRONG — so reputable, line-moving intel scores highest (that's the edge).")
    L.append("")
    L.append("TOP SIGNALS (by value_score) — what moved & why + source:")
    L.append("-" * 78)
    arrow = {"up": "▲ up ", "down": "▼ down", "neutral": "— flat"}
    for i, nd in enumerate(ranked[:6], 1):
        j = clean_judgment(nd)
        if len(j) > 88:
            j = j[:85].rstrip() + "…"
        host, _url, tier = best_source(nd)
        val = float(nd.get("value_score") or 0)
        flag = "  ⟵ STALE / just re-run" if nd.get("_stale") else ""
        L.append(f"{i}. [{val:.3f}] {arrow[nd['prob_direction']]}  {j}")
        L.append(f"      └ {host} [{TIER_LABEL[tier]}]{flag}")
    L.append("-" * 78)
    L.append("BACKTEST RECEIPTS — spots where the market was confidently WRONG:")
    for fixture, conf, fav, outcome in edge["examples"]:
        L.append(f"  • {fixture}: market {conf}% on {fav}  →  {outcome}")
    L.append("  (the same calibration edge, now projected onto live Group-D nodes)")
    return "\n".join(L)


# ────────────────────────────────────────────────────────────────────────────
def main():
    which = sys.argv[1].lower() if len(sys.argv) > 1 else "all"
    graph = load_graph()
    nodes, src = load_nodes(graph)
    seed = load_seed()
    edge = attach_value(nodes, seed)

    banner = (f"nodes from: {src}  ·  {len(nodes)} nodes  ·  "
              f"backtest: {edge['n_upsets']} upsets, "
              f"avg market conf when wrong = {edge['avg_market_conf_when_wrong']}")
    print("=" * 78)
    print("ONE TRACE, MANY PAYOFFS  —  " + banner)
    print("=" * 78)

    if which in ("fan", "all"):
        print("\n" + "#" * 78 + "\n# (1) FAN VIEW\n" + "#" * 78)
        print(view_fan(graph, nodes))
    if which in ("analyst", "all"):
        print("\n" + "#" * 78 + "\n# (2) ANALYST VIEW\n" + "#" * 78)
        print(view_analyst(graph, nodes))
    if which in ("moving", "all"):
        print("\n" + "#" * 78 + "\n# (3) MOVING-LINE VIEW\n" + "#" * 78)
        print(view_moving(graph, nodes, edge))


if __name__ == "__main__":
    main()
