#!/usr/bin/env python3
"""
node_extract.py  (stdlib only)

Reads a real MiroMind deep-research run trace and turns it into a small set of
auditable decision NODES.

Why this exists
---------------
A run trace is ~99.8% "thinking" fragmented into tiny chunks (e.g. "\\nThe ",
"use", "r i"). The forecast-relevant intel lives in the thinking span ADJACENT
to a web_search / fetch event. So we:

  1. walk steps[] in order,
  2. concatenate consecutive "thinking" chunks into coherent SPANS,
  3. for each web_search / fetch event, grab the thinking right before/after it,
  4. emit ONE node per event following the NODE CONTRACT,
  5. keep only the ~12-20 most substantive nodes (longest spans / most sources).

Nothing is hardcoded: trigger, evidence, judgment, sources all come straight
from the real trace. value_score is left at 0.0 for node_eval to fill from the
resolved-results data.

Usage
-----
    python3 node_extract.py [path/to/run.json]

Default trace: dataset/runs/wc26-usa-advance.json
Output:        dataset/graph/nodes.json   (+ prints 3 sample nodes)
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_RUN = os.path.join(HERE, "runs", "wc26-usa-advance.json")
FALLBACK_RUNS = [
    os.path.join(HERE, "runs", "wc26-winner.json"),
    os.path.join(HERE, "runs", "wc26-golden-boot.json"),
]
OUT_PATH = os.path.join(HERE, "graph", "nodes.json")

# How much thinking (in characters) to keep on each side of an event.
PRE_CHARS = 320
POST_CHARS = 220
# How many nodes to keep in the final set.
MAX_NODES = 20
MIN_NODES_FALLBACK = 3  # if a trace is too thin, fall back to another file

# ---------------------------------------------------------------------------
# Direction inference: does the JUDGMENT argue the parent outcome is MORE or
# LESS likely? We match whole words/stems (regex word boundaries, NOT bare
# substrings — the old code matched "out" inside "...advance from their group"
# and "about", flipping a neutral n01 to a false "down"). Negations like
# "no injury"/"not a doubt" cancel a down-signal. Pure description => neutral.
# ---------------------------------------------------------------------------
# Each entry is a regex fragment matched with \b...\b (so "favour" also catches
# "favourite", "struggl" catches "struggle/struggling", etc.).
UP_WORDS = [
    r"boost", r"favou?r\w*", r"advantage", r"advance\w*", r"qualif\w*",
    r"odds-on", r"strong\w*", r"comfortabl\w*", r"easily", r"depth",
    r"good chance", r"high probability", r"well[- ]placed", r"in[- ]form",
    r"healthy", r"\bfit\b", r"top of", r"\blead\w*", r"home (?:field|advantage|game|crowd|soil)",
    r"clear favou?rite\w*",
]
DOWN_WORDS = [
    r"injur\w*", r"doubt\w*", r"miss\w*", r"setback", r"upset\w*",
    r"weak\w*", r"struggl\w*", r"\bfail\w*", r"ruled out", r"sidelin\w*",
    r"suspend\w*", r"suspension", r"eliminat\w*", r"knocked out",
    r"underdog\w*", r"unlikely", r"\brisk\w*", r"concern\w*",
    r"tough group", r"difficult", r"\bloss\b", r"\blost\b",
]
# A down-signal preceded by one of these (within a few words) is cancelled.
_NEGATORS = re.compile(
    r"\b(no|not|never|without|free of|clear of|cleared|denies?|denied|"
    r"avoid\w*|recovered|return\w*|fit again|back to full)\b[\w ,'-]{0,24}$"
)
_UP_RE = re.compile(r"\b(?:%s)" % "|".join(UP_WORDS), re.IGNORECASE)
_DOWN_RE = re.compile(r"\b(?:%s)" % "|".join(DOWN_WORDS), re.IGNORECASE)

# Mapping of run id -> the graph.json parent node it feeds. Best-effort; falls
# back to a slug of the run id so a node ALWAYS records a parent.
PARENT_BY_RUN = {
    "wc26-usa-advance": "usa_advance",
    "wc26-winner": "champion",
    "wc26-golden-boot": "golden_boot",
    "wc26-spain-final": "spain_final",
    "euro24-final-leakprobe": "euro24_final",
}

# ---------------------------------------------------------------------------
# Source whitelist (CONTRACT.md). A node's source_tier = the BEST (lowest
# number) tier among its source URLs. Domain substrings, matched against the
# host. Tier 5 = unranked / long-tail (worse than the T4 corroboration tier).
# ---------------------------------------------------------------------------
_TIER_DOMAINS = {
    1: ["fifa.com", "opta", "theanalyst.com", "pinnacle", "polymarket"],
    2: ["espn.com", "bbc.co", "bbc.com", "nytimes.com", "theathletic",
        "oddschecker", "betmgm", "draftkings"],
    3: ["sofascore", "fbref", "statsbomb", "whoscored", "eloratings",
        "clubelo"],
    4: [],  # long-tail blogs/forums are allowed only as corroboration
}
_UNRANKED_TIER = 5


def _host(url):
    try:
        from urllib.parse import urlparse
        return (urlparse(url).netloc or "").lower()
    except Exception:
        return str(url).lower()


def tier_for_url(url):
    host = _host(url)
    for tier in (1, 2, 3):
        for dom in _TIER_DOMAINS[tier]:
            if dom in host:
                return tier
    return _UNRANKED_TIER  # not on the whitelist -> corroboration-only


def best_tier(sources):
    """Best (lowest-number) tier among a node's sources; 5 if none whitelisted."""
    if not sources:
        return _UNRANKED_TIER
    return min(tier_for_url(u) for u in sources)


# Sentence-ish splitter for pulling a judgment line out of the span.
_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+|\n+")
# Words that mark a forecast-relevant conclusion sentence. STRONG hints (a real
# number / probability / odds) are scored higher so the de-vig line wins.
_JUDGMENT_STRONG = (
    "probability", "implied", "%", "percent", "de-vig", "devig",
    "-750", "-700", "88.2", "0.882", "87.5", "65%",
)
_JUDGMENT_HINTS = (
    "probability", "implied", "odds", "%", "percent", "chance", "likely",
    "advance", "qualify", "expect", "estimate", "favorite", "favourite",
    "should", "we put", "i'd put", "we'd put", "around", "roughly",
    "advantage", "home", "depth", "favored", "favoured", "to win",
)
# Conversational / meta lead-ins to strip so judgment reads as a clean claim.
_LEAD_STRIP = re.compile(
    r"^(?:so |now |ok(?:ay)?[, ]+|well[, ]+|right[, ]+|"
    r"let'?s (?:try to |go |use |examine |check |look|see|recall|compute|"
    r"break this down)[^.:]*[.:]\s*|"
    r"we(?:'ll| will| need to| have| got| can)[^.:]*[.:]\s*|"
    r"i(?:'ll| will| need to|'d| would)[^.:]*[.:]\s*|"
    r"the user (?:is asking|wants|asked)[^.]*\.\s*)",
    re.IGNORECASE,
)
# A judgment is only "real" if it carries a forecast-relevant token, not just
# meta-narration ("the user is asking", "let me break this down").
_FORECAST_TOKEN = re.compile(
    r"\b(?:%s)\b|\d{2,}|%%" % "|".join(
        ["advance", "qualif\\w*", "probabilit\\w*", "odds", "implied", "chance",
         "favou?rite\\w*", "expect\\w*", "estimate\\w*", "injur\\w*", "doubt\\w*",
         "home", "depth", "upset\\w*", "win\\b", "lose\\b", "loss"]),
    re.IGNORECASE,
)
# Bare meta-narration we never want as a judgment.
_META_ONLY = re.compile(
    r"^(?:the user (?:is asking|wants|asked)|let me|let'?s|"
    r"i need to|i should|first[, ]|we need to (?:find|search|compute|recall))",
    re.IGNORECASE,
)


def load_run(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def parent_for_run(run_id):
    if run_id in PARENT_BY_RUN:
        return PARENT_BY_RUN[run_id]
    slug = re.sub(r"[^a-z0-9]+", "_", str(run_id).lower()).strip("_")
    return slug or "root"


def collapse_ws(text):
    """Squash the fragmented thinking back into readable prose."""
    text = text.replace(" ", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{2,}", "\n", text)
    return text.strip()


def thinking_span_before(steps, idx, max_chars):
    """Concatenate consecutive thinking chunks ending just before idx."""
    chunks = []
    total = 0
    j = idx - 1
    while j >= 0 and steps[j].get("action") == "thinking":
        t = steps[j].get("text", "") or ""
        chunks.append(t)
        total += len(t)
        j -= 1
        if total >= max_chars * 3:  # gather extra, trim later
            break
    chunks.reverse()
    joined = "".join(chunks)
    return joined[-max_chars * 3:]  # keep generous tail, trim after collapse


def thinking_span_after(steps, idx, max_chars):
    """Concatenate consecutive thinking chunks starting just after idx."""
    chunks = []
    total = 0
    j = idx + 1
    while j < len(steps) and steps[j].get("action") == "thinking":
        t = steps[j].get("text", "") or ""
        chunks.append(t)
        total += len(t)
        j += 1
        if total >= max_chars * 3:
            break
    return "".join(chunks)[: max_chars * 3]


def trim(text, max_chars):
    text = collapse_ws(text)
    if len(text) <= max_chars:
        return text
    # trim to a word boundary near the limit
    cut = text[:max_chars]
    sp = cut.rfind(" ")
    if sp > max_chars * 0.6:
        cut = cut[:sp]
    return cut.strip() + " ..."


def _count_signal(text, pattern):
    """Count whole-word matches of pattern in text, dropping any whose left
    context is a negator ('no injury', 'cleared of doubt' -> not a down)."""
    n = 0
    for m in pattern.finditer(text):
        left = text[:m.start()]
        if _NEGATORS.search(left):
            continue
        n += 1
    return n


# A judgment that STATES a high probability of the parent outcome (an implied
# % >= 60, or a strong negative moneyline like -700 / -750 / -1000) is itself an
# UP signal — even if it has no lexical up-words — and shouldn't inherit a noisy
# down from the surrounding evidence span.
_PCT_RE = re.compile(r"(\d{2,3}(?:\.\d+)?)\s*%")
_NEG_ML_RE = re.compile(r"(?<![\d])-\s?(\d{3,4})\b")


def _odds_up_signal(text):
    """1 if the text states a high favourite probability/moneyline, else 0."""
    for m in _PCT_RE.finditer(text):
        try:
            if float(m.group(1)) >= 60.0:
                return 1
        except ValueError:
            pass
    # a strong negative moneyline (-300 or stronger) = clear favourite
    for m in _NEG_ML_RE.finditer(text):
        if int(m.group(1)) >= 300:
            return 1
    return 0


def infer_direction(judgment, evidence=""):
    """Direction from what the JUDGMENT argues about the parent outcome.

    Weight the judgment heavily (it IS the forecast claim); the evidence span
    only breaks ties. up = makes parent MORE likely (favourite/home/depth/
    odds-on/advance, OR a stated high favourite probability), down = LESS likely
    (injury/doubt/rest/upset/weakness), pure description = neutral.
    Returns (direction, strength)."""
    ju, ev = judgment or "", evidence or ""
    up = 3 * _count_signal(ju, _UP_RE) + _count_signal(ev, _UP_RE)
    down = 3 * _count_signal(ju, _DOWN_RE) + _count_signal(ev, _DOWN_RE)
    # A high favourite probability stated IN the judgment is a strong up signal.
    up += 3 * _odds_up_signal(ju)
    if up == 0 and down == 0:
        return "neutral", 0
    if up > down:
        return "up", up + down
    if down > up:
        return "down", up + down
    return "neutral", up + down


def clean_sentence(s):
    """Turn a raw thinking sentence into ONE readable, self-contained claim.

    - drop conversational/meta lead-ins ("Let's examine...", "We need to...");
    - repair a sentence that starts mid-clause (lowercase verb with no subject,
      e.g. 'is -750 to advance...' -> 'The US is -750 to advance...');
    - strip a dangling leading fragment before the first capitalised word /
      quote / digit when the head looks like debris ('ppet again: In that...');
    - trim a trailing half-sentence after the last terminator.
    """
    s = collapse_ws(s).strip(" \t\n\"'")
    if not s:
        return ""
    # peel conversational lead-ins (possibly stacked)
    for _ in range(3):
        new = _LEAD_STRIP.sub("", s).strip(" \t\n\"'")
        if new == s:
            break
        s = new
    if not s:
        return ""
    # Repair a clause that starts with a bare verb (no subject): prepend the
    # run's known subject so the line reads as a real claim. Do this BEFORE the
    # debris-cut so we don't mistake the leading verb for junk (e.g. the de-vig
    # candidate 'is -750 to advance...' -> 'The US is -750 to advance...').
    if re.match(r'^(?:is|are|was|were|has|have|sits?|stands?|opens?|comes?)\b',
                s, re.IGNORECASE):
        s = "The US " + s[0].lower() + s[1:]
    # Else, if the head is short lowercase debris ("ppet again:", "y factors."),
    # cut to the first real sentence-start (capital/quote/digit beginning a
    # token). Only fire when the junk prefix is SHORT (<= ~12 chars) so we never
    # chop a real clause.
    elif s[0].islower():
        m2 = re.search(r'(["A-Z]|\b\d)', s)
        if m2 and 0 < m2.start() <= 12:
            s = s[m2.start():].strip(" \t\n\"'")
    # Trim a trailing fragment: keep through the last sentence terminator, but
    # keep a closing ')' / quote that immediately follows it.
    m = re.search(r'.*[.!?]["\')]?', s, re.DOTALL)
    if m and len(m.group(0)) >= 25:
        s = m.group(0)
    s = s.strip()
    # balance a stray opening paren that lost its close at the trim boundary
    if s.count("(") > s.count(")"):
        s = s + ")"
    return s


# Conversational asides / mid-reasoning openers that make a poor handover line.
_ASIDE_OPENER = re.compile(
    r"^(?:actually|wait|hmm|but |however|so |well |right |ok(?:ay)?|"
    r"that'?s for|no[,:]|yes[,:]|let me|let'?s)",
    re.IGNORECASE,
)
# A truncated parenthetical/decimal tail, e.g. "...at -700 (87.)" — half a fact.
_TRUNCATED_TAIL = re.compile(r"\(\s*\d+(?:\.\d*)?\s*\)\s*$|\b\d+\.\)\s*$")


def _looks_like_judgment(s):
    """A real forecast judgment: not pure meta-narration, carries a token,
    and isn't a visibly truncated fragment."""
    if not s or _META_ONLY.match(s):
        return False
    if _TRUNCATED_TAIL.search(s):
        return False
    return bool(_FORECAST_TOKEN.search(s))


def _judgment_quality(s):
    """Cheap readability bonus/penalty so the cleanest forecast line wins ties.
    + stating a probability / odds / favourite claim; - asides & first person."""
    low = s.lower()
    q = 0
    if _PCT_RE.search(s) or _NEG_ML_RE.search(s):
        q += 3
    if re.search(r"\b(advance|qualif\w*|favou?rite\w*|chance|probabilit\w*)\b", low):
        q += 2
    if _ASIDE_OPENER.match(s):
        q -= 3
    if re.search(r"\b(i|we|let'?s|the user)\b", low):
        q -= 2
    if _TRUNCATED_TAIL.search(s):
        q -= 4
    return q


def pick_judgment(pre, post):
    """Find the most forecast-relevant sentence in the adjacent span, then
    clean it into ONE readable claim. Prefers a sentence stating a de-vig /
    probability / odds; falls back to the strongest forecast-relevant line."""
    candidates = []
    for origin, blob in (("post", post), ("pre", pre)):  # conclusion-after first
        for sent in _SENT_SPLIT.split(blob):
            s = collapse_ws(sent)
            if len(s) < 15 or len(s) > 360:
                continue
            low = s.lower()
            strong = sum(1 for h in _JUDGMENT_STRONG if h in low)
            hits = sum(1 for h in _JUDGMENT_HINTS if h in low)
            if not (strong or hits):
                continue
            cleaned = clean_sentence(s)
            if not cleaned:
                continue
            bonus = 1 if origin == "post" else 0
            # signal score (find the right fact) then quality (read cleanly)
            signal = strong * 10 + hits + bonus
            quality = _judgment_quality(cleaned)
            real = _looks_like_judgment(cleaned)
            candidates.append((real, signal, quality,
                               -abs(len(cleaned) - 130), cleaned))
    if not candidates:
        return ""
    # real-judgment lines first, then strongest signal, then cleanest reading
    candidates.sort(reverse=True)
    return candidates[0][-1]


def event_label(step):
    if step.get("action") == "web_search":
        kw = step.get("keywords")
        if isinstance(kw, list):
            return " ; ".join(str(k) for k in kw)
        return str(kw or "")
    return step.get("url", "") or ""


def event_sources(step, run):
    """Source URLs tied to this event. fetch -> its own url; web_search ->
    best-effort match against the run's top-level sources by keyword overlap."""
    if step.get("action") == "fetch":
        u = step.get("url")
        return [u] if u else []
    # web_search: try to map keywords -> top-level source titles/urls
    kw = step.get("keywords") or []
    terms = set()
    for k in kw:
        terms.update(re.findall(r"[a-z0-9]{4,}", str(k).lower()))
    src_list = run.get("sources", []) or []
    scored = []
    for s in src_list:
        url = s.get("url", "") if isinstance(s, dict) else str(s)
        title = s.get("title", "") if isinstance(s, dict) else ""
        hay = (url + " " + title).lower()
        overlap = sum(1 for t in terms if t in hay)
        if overlap:
            scored.append((overlap, url))
    scored.sort(reverse=True)
    return [u for _, u in scored[:2]]


def extract_nodes_by_event(run):
    """LEGACY (fallback): one node per web_search/fetch EVENT, grabbing the thinking
    before/after as evidence. This anchors on the RAW TRACE. Kept as the fallback for
    terse traces that have too few decision points (e.g. the probe-* runs with almost
    no thinking). The default path is now extract_nodes() — decision-point anchored."""
    steps = run.get("steps", []) or []
    run_id = run.get("id", "run")
    parent = parent_for_run(run_id)

    raw_nodes = []
    seq = 0
    for k, step in enumerate(steps):
        action = step.get("action")
        if action not in ("web_search", "fetch"):
            continue
        pre = thinking_span_before(steps, k, PRE_CHARS)
        post = thinking_span_after(steps, k, POST_CHARS)
        pre_t = trim(pre, PRE_CHARS)
        post_t = trim(post, POST_CHARS)

        evidence_parts = [p for p in (pre_t, post_t) if p]
        evidence = "  ⟶  ".join(evidence_parts)
        if not evidence:
            # fetch snippet can still be evidence even with no thinking around it
            snip = step.get("snippet", "")
            evidence = trim(snip, PRE_CHARS) if snip else ""

        judgment = pick_judgment(pre, post)
        # Direction is what the JUDGMENT argues; evidence only breaks ties.
        direction, dir_strength = infer_direction(judgment, evidence)
        sources = event_sources(step, run)
        source_tier = best_tier(sources)

        # A node must hand over a REAL judgment (a forecast claim, not meta
        # narration) AND a real source URL. Otherwise it is garbage; flag it so
        # we can keep the substantive ones and drop the empties.
        real_judgment = _looks_like_judgment(judgment)

        seq += 1
        label = event_label(step)
        node = {
            "node_id": "%s::n%02d" % (run_id, seq),
            "graph_parent": parent,
            "trigger": {"action": action, "query_or_url": label},
            "evidence": evidence,
            "judgment": judgment,
            "prob_direction": direction,
            "sources": sources,
            "source_tier": source_tier,
            "value_score": 0.0,
            # internal scoring fields (stripped before save)
            "_real": bool(real_judgment and sources),
            "_substance": len(collapse_ws(pre)) + len(collapse_ws(post))
            + 200 * len(sources) + 60 * dir_strength
            + (150 if real_judgment else 0)
            + (120 if source_tier <= 2 else 40 if source_tier == 3 else 0),
        }
        raw_nodes.append(node)

    # Prefer nodes that hand over a REAL judgment + a real source; only fall
    # back to thin nodes if too few real ones exist (so the demo never empties).
    real = [n for n in raw_nodes if n["_real"]]
    pool = real if len(real) >= MIN_NODES_FALLBACK else raw_nodes
    # Keep the most substantive, then restore trace order + renumber.
    pool.sort(key=lambda n: n["_substance"], reverse=True)
    kept = pool[:MAX_NODES]
    kept.sort(key=lambda n: int(n["node_id"].split("n")[-1]))
    for i, n in enumerate(kept, 1):
        n["node_id"] = "%s::n%02d" % (run_id, i)
        n.pop("_substance", None)
        n.pop("_real", None)
    return kept


# ===========================================================================
# DECISION-POINT ANCHORING  (the reframe)
# ---------------------------------------------------------------------------
# A node is NOT the raw trace event. A node = a DECISION POINT — a sub-question
# the agent poses to itself BEFORE a reasoning span ("First, let me clarify the
# format…", "I need to search for Spain's squad…", "Let me check the odds…").
# The span that follows (its searches/fetches/sources/conclusion) is that node's
# support. The agent's OPENING PLAN (the decision points stated before it acts)
# becomes the root's depends_on — DAG edges read from the trace, not invented.
# ===========================================================================

# A sentence that POSES a decision/sub-goal. Bare "let me think / let's see /
# recall / reconsider" are NOT decision points (negative lookaheads + _WEAK_DP_RE).
_DP_RE = re.compile(
    r"^\s*(?:"
    r"(?:first|next|now|then|second|third|finally|also)[,]?\s+"
    r"(?:let me|let'?s|i(?:'ll| will| need to| should))"
    r"|let me\s+(?!think\b|see\b|reconsider\b|recall\b)\w+"
    r"|let'?s\s+(?!see\b|think\b)\w+"
    r"|i need to\b|i should\b|i'?ll\b|i will\b|i want to\b|i must\b|i'?d\b"
    r"|to (?:answer|determine|estimate|assess|calculate|compute|find|figure|verify|clarify)\b"
    r")", re.IGNORECASE)

# An action/intent verb makes a decision point STRONG (a real node boundary).
_DP_ACTION_RE = re.compile(
    r"\b(?:search\w*|fetch\w*|open\w*|read\b|check\w*|find\b|look\w*|gather\w*|pull\b|"
    r"calculat\w*|comput\w*|estimat\w*|determin\w*|analy[sz]\w*|assess\w*|evaluat\w*|"
    r"clarif\w*|identif\w*|examin\w*|verif\w*|confirm\w*|compar\w*|review\w*|"
    r"cross[- ]?referenc\w*|get more|approach|break (?:this|it) down|construct\w*|"
    r"map\b|use (?:my|the)\b|do a\b)", re.IGNORECASE)

# Weak (pure-meta) openers: a decision in form but no action — folded into the span.
_WEAK_DP_RE = re.compile(
    r"^\s*(?:let me|let'?s|i'?ll|i will)\s+"
    r"(?:think|see|recall|reconsider|just|note|also note)\b", re.IGNORECASE)

# A "drill-in" decision (open/fetch/read the source we just found) nests UNDER the
# most recent depth-1 decision instead of hanging off the root.
_DRILL_RE = re.compile(
    r"^\s*(?:let me|let'?s|i(?:'ll| will| should|'d| need to))\s+(?:also\s+)?"
    r"(?:open|fetch|read|check|get more|look at|examine|dig|verify|confirm|cross-?reference)\b",
    re.IGNORECASE)


def _dp_strength(sentence):
    """0 = not a decision point; 1 = weak (fold in); 2 = strong (open a node)."""
    s = sentence.strip()
    if not s or not _DP_RE.match(s):
        return 0
    if _WEAK_DP_RE.match(s):
        return 1
    if _DP_ACTION_RE.search(s) or _FORECAST_TOKEN.search(s):
        return 2
    return 1


def _iter_sentences(text):
    """Yield (start_offset, sentence) over the raw reconstructed text. Offsets are
    into `text` so they line up with the inline event offsets from reconstruct()."""
    start = 0
    for m in re.finditer(r"[.!?]+(?=\s|$)|\n+", text):
        end = m.end()
        seg = text[start:end]
        if seg.strip():
            yield start, seg
        start = end
    if start < len(text) and text[start:].strip():
        yield start, text[start:]


def reconstruct(steps):
    """One pass: concatenate the fragmented `thinking` chunks into one prose string,
    and record each web_search/fetch with its CHARACTER OFFSET into that string (the
    event sits between the thinking before and after it). Returns (text, events) with
    events = [(char_offset, step_index, action, step_dict)]. This replaces the old
    thinking_span_before/after neighbour-walk: we own the whole prose and slice it by
    decision point."""
    parts, text_len, events = [], 0, []
    for k, step in enumerate(steps):
        action = step.get("action")
        if action == "thinking":
            t = step.get("text", "") or ""
            parts.append(t)
            text_len += len(t)
        elif action in ("web_search", "fetch"):
            events.append((text_len, k, action, step))
    return "".join(parts), events


def find_decision_points(text):
    """Strong decision-point sentences with their char offsets: [(offset, sentence)]."""
    return [(off, collapse_ws(sent)) for off, sent in _iter_sentences(text)
            if _dp_strength(sent) == 2]


def _root_judgment(content):
    head = collapse_ws(content or "")[:1400]
    return pick_judgment(head, "") or trim(head, 200)


def extract_nodes(run):
    """DECISION-POINT anchored extraction (the default). A node = a decision point the
    agent posed before a reasoning span; the span's searches/fetches/conclusion are its
    support. The opening plan = the root's depends_on (DAG edges from the trace itself).
    Falls back to extract_nodes_by_event() for terse traces with too few decision points
    so the demo never empties.

    Node shape keeps every field the downstream reads (graph_parent UNCHANGED so demo.py
    rollup still works); ADDS question / parent_node / depends_on; trigger now records the
    actions taken inside the span."""
    steps = run.get("steps", []) or []
    run_id = run.get("id", "run")
    graph_parent = parent_for_run(run_id)

    text, events = reconstruct(steps)
    dps = find_decision_points(text)
    if len(dps) < MIN_NODES_FALLBACK:
        return extract_nodes_by_event(run)

    first_ev = events[0][0] if events else len(text)
    root_id = "%s::root" % run_id

    # 1) build raw child records in trace order
    raw = []
    last_d1 = None  # index (into raw) of the most recent depth-1 decision node
    for i, (off, sent) in enumerate(dps):
        end = dps[i + 1][0] if i + 1 < len(dps) else len(text)
        span = text[off:end]
        span_events = [s for (eoff, _a, _act, s) in events if off <= eoff < end]
        srcs = []
        for ev in span_events:
            srcs.extend(event_sources(ev, run))
        sources = list(dict.fromkeys(u for u in srcs if u))
        tier = best_tier(sources)
        judgment = pick_judgment(span, "")
        direction, dir_strength = infer_direction(judgment, span)
        is_plan = off <= first_ev
        is_drill = (not is_plan and last_d1 is not None
                    and bool(_DRILL_RE.match(sent.strip())))
        real = _looks_like_judgment(judgment)
        tier_bonus = 120 if tier <= 2 else 40 if tier == 3 else 0
        substance = (len(collapse_ws(span)) + 200 * len(sources) + 60 * dir_strength
                     + (150 if real else 0) + tier_bonus + (100 if span_events else 0))
        raw.append({
            "question": clean_sentence(sent) or collapse_ws(sent),
            "evidence": trim(span, PRE_CHARS + POST_CHARS),
            "judgment": judgment,
            "prob_direction": direction,
            "sources": sources,
            "source_tier": tier,
            "trigger_label": " | ".join(event_label(e) for e in span_events),
            "is_plan": is_plan,
            "parent_temp": (last_d1 if is_drill else None),  # None => root
            "_real": bool(real or sources),
            "_substance": substance,
        })
        if not is_drill:
            last_d1 = i  # this is a depth-1 node; later drill-ins hang off it

    # 2) selection: always keep the opening plan (the skeleton); fill the rest by
    #    substance, preferring nodes that hand over a real judgment or a source.
    keep = {i for i, r in enumerate(raw) if r["is_plan"]}
    rest = sorted((i for i in range(len(raw)) if i not in keep and raw[i]["_real"]),
                  key=lambda i: raw[i]["_substance"], reverse=True)
    for i in rest:
        if len(keep) >= MAX_NODES:
            break
        keep.add(i)
    if len(keep) < MIN_NODES_FALLBACK:  # thin trace: relax the real-judgment filter
        for i in sorted(range(len(raw)), key=lambda i: raw[i]["_substance"], reverse=True):
            keep.add(i)
            if len(keep) >= MAX_NODES:
                break

    kept_idx = sorted(keep)
    temp_to_final = {ti: "%s::n%02d" % (run_id, n) for n, ti in enumerate(kept_idx, 1)}

    # 3) materialise child nodes; reparent drill-ins whose parent was dropped -> root
    nodes, root_children = [], []
    for ti in kept_idx:
        r = raw[ti]
        pt = r["parent_temp"]
        if pt is None or pt not in temp_to_final:
            parent_node = root_id
            root_children.append(temp_to_final[ti])
        else:
            parent_node = temp_to_final[pt]
        nodes.append({
            "node_id": temp_to_final[ti],
            "graph_parent": graph_parent,                 # UNCHANGED (demo.py rollup)
            "parent_node": parent_node,                   # NEW: intra-trace parent
            "question": r["question"],                    # NEW: the decision point
            "trigger": {"action": "decision", "query_or_url": r["trigger_label"]},
            "evidence": r["evidence"],
            "judgment": r["judgment"],
            "prob_direction": r["prob_direction"],
            "sources": r["sources"],
            "source_tier": r["source_tier"],
            "depends_on": [],                             # filled from parent_node links
            "value_score": 0.0,
        })
    by_id = {nd["node_id"]: nd for nd in nodes}
    for nd in nodes:
        if nd["parent_node"] in by_id:
            by_id[nd["parent_node"]]["depends_on"].append(nd["node_id"])

    # 4) the ROOT node = the run's question; its depends_on = the opening plan
    root_sources = [u for u in dict.fromkeys(
        (s.get("url") if isinstance(s, dict) else s) for s in (run.get("sources") or [])
    ) if u][:3]
    rj = _root_judgment(run.get("content"))
    root = {
        "node_id": root_id,
        "graph_parent": graph_parent,
        "parent_node": graph_parent,
        "question": run.get("q") or "(question)",
        "trigger": {"action": "root", "query_or_url": ""},
        "evidence": trim(collapse_ws(run.get("content") or ""), PRE_CHARS + POST_CHARS),
        "judgment": rj,
        "prob_direction": infer_direction(rj, collapse_ws(run.get("content") or "")[:1400])[0],
        "sources": root_sources,
        "source_tier": best_tier(root_sources),
        "depends_on": root_children,
        "value_score": 0.0,
    }
    return [root] + nodes


def run_with_fallback(primary_path):
    paths = [primary_path] + [p for p in FALLBACK_RUNS if p != primary_path]
    last_run = None
    for p in paths:
        if not os.path.exists(p):
            continue
        run = load_run(p)
        nodes = extract_nodes(run)
        if len(nodes) >= MIN_NODES_FALLBACK:
            return p, run, nodes
        last_run = (p, run, nodes)
    if last_run:
        return last_run
    raise SystemExit("No usable run trace found among: %s" % paths)


def main():
    primary = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_RUN
    used_path, run, nodes = run_with_fallback(primary)

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    out = {
        "source_run": run.get("id"),
        "source_path": used_path,
        "question": run.get("q"),
        "node_count": len(nodes),
        "nodes": nodes,
    }
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    # Summary
    print("node_extract.py")
    print("  source trace : %s" % used_path)
    print("  run id       : %s -> graph_parent '%s'"
          % (run.get("id"), parent_for_run(run.get("id"))))
    print("  nodes emitted: %d  (saved to %s)" % (len(nodes), OUT_PATH))
    dirs = {}
    for n in nodes:
        dirs[n["prob_direction"]] = dirs.get(n["prob_direction"], 0) + 1
    print("  directions   : %s" % dirs)
    with_src = sum(1 for n in nodes if n["sources"])
    print("  nodes w/ src : %d/%d" % (with_src, len(nodes)))
    tiers = {}
    for n in nodes:
        t = n.get("source_tier")
        tiers[t] = tiers.get(t, 0) + 1
    print("  source_tier  : %s  (1=best)" % dict(sorted(tiers.items())))

    print("\n=== 3 SAMPLE NODES ===")
    # show the 3 with the best tier / longest judgment for a good demo
    sample = sorted(
        nodes,
        key=lambda n: (-n.get("source_tier", 9), len(n["judgment"]),
                       len(n["sources"])),
    )[:3]
    for n in sample:
        print(json.dumps(n, indent=2, ensure_ascii=False))
        print()


if __name__ == "__main__":
    main()
