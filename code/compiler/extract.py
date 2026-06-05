"""
extract.py — the DETERMINISTIC (zero-LLM) compile layer.

This is the 升维存储 / 实体注册 half of the bootstrap compiler, ported faithfully
from gbrain (the knowledge-compile reference):
  - link regexes + inferLinkType verb-precedence  <- gbrain src/core/link-extraction.ts
  - the `<!--- gbrain:facts:begin -->` fence       <- gbrain src/core/facts-fence.ts
  - parseTimelineEntries                            <- gbrain src/core/link-extraction.ts

gbrain assumes pages are AUTHORED with [[wikilinks]]; a raw conversation isn't, so
we add one honest addition: a curated domain CONCEPT_LEXICON (the same idea as
gbrain's DIR_PATTERN whitelist) that recognizes this project's entities and lets the
graph self-wire from prose. Everything here is pure + zero-LLM, so the artifact is
rebuildable byte-for-byte (gbrain system-of-record contract).

TOWOW mapping: this file is 实体注册 (slices -> named objects with identity/relations)
+ 关系切面 (a concept only needs to know its neighbors).
"""
import re
from collections import OrderedDict

# ── Concept lexicon (实体注册: the named objects this conversation is "about") ──
# slug -> list of surface aliases. Short/ambiguous aliases ("Miro") are ordered
# after their longer forms so the longest match wins.
CONCEPT_LEXICON = OrderedDict([
    ("orgs/miromind",            ["MiroMind AI", "MiroMind", "Miro"]),
    ("api/miromind-api",         ["mirothinker-1-7-deepresearch-mini", "mirothinker-1-7-deepresearch",
                                  "api.miromind.ai", "MiroMind API", "deep-research API", "hosted API"]),
    ("models/mirothinker",       ["MiroThinker"]),
    ("tools/miroflow",           ["MiroFlow"]),
    ("data/miroverse",           ["MiroVerse"]),
    ("bench/futurex",            ["FutureX"]),
    ("tools/gbrain",             ["gbrain", "knowledge-brain", "GBrain"]),
    ("tools/wow-harness",        ["wow-harness", "WoW harness", "Ways-of-Working", "wow harness"]),
    ("concepts/towow",           ["通向智流", "分布式 Harness", "distributed harness", "TOWOW", "ToWow"]),
    ("concepts/a2ui",            ["A2UI"]),
    ("tools/gemini-live",        ["gemini-2.5-flash-native-audio", "Gemini Live", "Gemini"]),
    ("concepts/decision-surface",["maintained decision surface", "decision surface", "maintained surface"]),
    ("concepts/trajectory",      ["MiroVerse-aligned trajectory", "audited trajectory", "trajectory"]),
    ("concepts/intent-ledger",   ["intent ledger", "intent-ledger"]),
    ("concepts/appropriate-reliance", ["appropriate reliance", "RAIR", "RSR", "over-reliance"]),
    ("concepts/human-in-the-loop",["human-in-the-loop", "上升端", "human in the loop"]),
    ("concepts/dimension-loop",  ["降维", "升维", "dimension loop"]),
    ("concepts/bootstrap-compiler",["bootstrap compiler", "the compiler", "compiler"]),
    ("scenes/nvda",              ["Nvidia", "NVDA"]),
    ("scenes/trauma",            ["survivor", "trauma"]),
    ("concepts/hci-trust",       ["weight-of-advice", "trust calibration", "Hoffman", "Lee & See"]),
])

# Precompiled alias matchers (longest-alias-first within each concept).
_ASCII = re.compile(r'[A-Za-z]')
def _alias_re(alias):
    # word-boundary match for ascii aliases; substring for CJK.
    if _ASCII.search(alias):
        return re.compile(r'(?<![A-Za-z0-9])' + re.escape(alias) + r'(?![A-Za-z0-9])', re.I)
    return re.compile(re.escape(alias))
_LEXICON_MATCHERS = [(slug, a, _alias_re(a)) for slug, aliases in CONCEPT_LEXICON.items() for a in aliases]

# ── gbrain link regexes (ported verbatim in spirit) ──────────────────────────
DIR_PATTERN = (r'(?:concepts|orgs|api|models|tools|data|bench|scenes|people|turns)')
WIKILINK_RE = re.compile(r'\[\[(' + DIR_PATTERN + r'\/[^|\]#]+?)(?:#[^|\]]*?)?(?:\|([^\]]+?))?\]\]')
ENTITY_REF_RE = re.compile(r'\[([^\]]+)\]\((?:\.\.\/)*(' + DIR_PATTERN + r'\/[^)\s]+?)(?:\.md)?\)')

# ── inferLinkType verb precedence (gbrain link-extraction.ts), domain-adapted ──
# Conversation relationships, not VC relationships. Precedence top->bottom.
_VERB_RULES = [
    ("supersedes",  re.compile(r'\b(supersed\w*|replaces?|corrects?|overrid\w*|reframes?)\b', re.I)),
    ("rejects",     re.compile(r'\b(reject\w*|dropp?ed|drop|ruled out|vetoe?d?|abandon\w*|out of scope|no longer|cosplay)\b', re.I)),
    ("lacks",       re.compile(r"\b(lacks?|lacking|missing|does(?:n'?t| not) (?:have|cover)|has no|the gap|structurally cannot)\b", re.I)),
    ("produces",    re.compile(r'\b(produces?|produc\w*|emits?|emit|generates?|outputs?|returns?|yields?|compiles? (?:into|to))\b', re.I)),
    ("uses",        re.compile(r'\b(uses?|calls?|runs?|invok\w*|points? at|built on|powered by|via the|plug(?:s)? in)\b', re.I)),
    ("grounds",     re.compile(r'\b(cites?|grounded in|sourced? (?:from|in)|references?|evidence|verified by|confirmed)\b', re.I)),
    ("maps_to",     re.compile(r'\b(maps? to|maps? onto|corresponds? to|aligns? with|equivalent to|=)\b', re.I)),
]

def infer_link_type(context):
    """Deterministic regex heuristics, no LLM. gbrain inferLinkType analogue."""
    for t, rx in _VERB_RULES:
        if rx.search(context):
            return t
    return "mentions"

# ── Facts fence (gbrain facts-fence.ts) ──────────────────────────────────────
FACTS_FENCE_BEGIN = '<!--- gbrain:facts:begin -->'
FACTS_FENCE_END   = '<!--- gbrain:facts:end -->'
_KIND = {"event", "preference", "commitment", "belief", "fact"}
_VIS  = {"private", "world"}
_NOTE = {"high", "medium", "low"}

def parse_facts_fence(body):
    """Parse a `## Facts` fence. 10-col or 14-col (typed-claim) — gbrain contract."""
    b = body.find(FACTS_FENCE_BEGIN)
    e = body.find(FACTS_FENCE_END, b + len(FACTS_FENCE_BEGIN)) if b != -1 else -1
    facts, warnings = [], []
    if b == -1 or e == -1:
        return facts, warnings
    inner = body[b + len(FACTS_FENCE_BEGIN):e]
    saw_header = False
    seen = set()
    for line in inner.split('\n'):
        if not line.strip():
            continue
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if not saw_header:
            low = [c.lower() for c in cells]
            if 'claim' in low and 'kind' in low:
                saw_header = True
            continue
        if set(''.join(cells)) <= set('-: '):   # separator row
            continue
        if len(cells) < 9:
            warnings.append(f"FACTS_TABLE_MALFORMED: {len(cells)} cells")
            continue
        cells += [''] * (14 - len(cells))
        (num, claim, kind, conf, vis, note, vfrom, vuntil, src, ctx,
         cmetric, cvalue, cunit, cperiod) = cells[:14]
        try:
            row = int(num)
        except ValueError:
            continue
        if row in seen or kind.lower() not in _KIND or vis.lower() not in _VIS or note.lower() not in _NOTE:
            continue
        seen.add(row)
        struck = claim.startswith('~~') and claim.endswith('~~')
        try:
            cv = float(cvalue.replace(',', '')) if cvalue else None
        except ValueError:
            cv = None
        facts.append({
            "row": row, "claim": claim.strip('~'), "kind": kind.lower(),
            "confidence": float(conf) if conf else None,
            "visibility": vis.lower(), "notability": note.lower(),
            "valid_from": vfrom or None, "valid_until": vuntil or None,
            "source": src or None, "context": ctx or None, "active": not struck,
            "claim_metric": cmetric or None, "claim_value": cv,
            "claim_unit": cunit or None, "claim_period": cperiod or None,
        })
    return facts, warnings

# ── Timeline parser (gbrain parseTimelineEntries) ────────────────────────────
TIMELINE_LINE_RE = re.compile(r'^\s*-?\s*\*\*(\d{4}-\d{2}-\d{2})\*\*\s*[|\-–—]+\s*(.+?)\s*$')
def parse_timeline(content):
    out = []
    for line in content.split('\n'):
        m = TIMELINE_LINE_RE.match(line)
        if m and 1 <= int(m.group(1)[5:7]) <= 12:
            out.append({"date": m.group(1), "summary": m.group(2).strip()})
    return out

# ── Concept recognition + edge wiring (实体注册 + 关系切面) ────────────────────
def find_concepts(text):
    """Return [(slug, name, start, end)] of concept mentions, longest-match, no overlap."""
    hits = []
    for slug, alias, rx in _LEXICON_MATCHERS:
        for m in rx.finditer(text):
            hits.append((m.start(), m.end(), slug, alias))
    # also honor explicit [[links]] (authored structure wins)
    for m in WIKILINK_RE.finditer(text):
        hits.append((m.start(), m.end(), m.group(1), (m.group(2) or m.group(1))))
    hits.sort(key=lambda h: (h[0], -(h[1] - h[0])))
    chosen, last_end = [], -1
    for s, e, slug, name in hits:
        if s >= last_end:
            chosen.append((slug, name, s, e))
            last_end = e
    return chosen

# Strip STRUCTURED regions before graph extraction (gbrain stripCodeBlocks analogue):
# facts fences, HTML comments, markdown table rows, and @marker directive lines are
# parsed elsewhere — they must NOT generate prose edges (the "gbrain:facts" marker
# literally contains the word "gbrain", which would mis-wire the graph).
_FENCE_BLOCK_RE = re.compile(re.escape(FACTS_FENCE_BEGIN) + r'.*?' + re.escape(FACTS_FENCE_END), re.S)
_HTML_COMMENT_RE = re.compile(r'<!--.*?-->', re.S)
def strip_structured(text):
    text = _FENCE_BLOCK_RE.sub(' ', text)
    text = _HTML_COMMENT_RE.sub(' ', text)
    out = []
    for ln in text.split('\n'):
        s = ln.lstrip()
        if s.startswith('@') or s.startswith('|'):       # directives + table rows
            out.append('')
        else:
            out.append(ln)
    return '\n'.join(out)

def wire_edges(turn_slug, text, gap=120):
    """
    Emit edges: (a) turn -> concept (mentions); (b) concept -> concept typed by the
    text STRICTLY BETWEEN two adjacent mentions (gbrain per-edge verb inference,
    domain-adapted). Structured regions are stripped first.
    """
    prose = strip_structured(text)
    concepts = find_concepts(prose)
    edges, seen = [], set()
    def add(frm, to, typ, ctx):
        if frm == to:
            return
        k = (frm, to, typ)
        if k in seen:
            return
        seen.add(k)
        edges.append({"from_slug": frm, "to_slug": to, "link_type": typ,
                      "context": ctx[:160].replace('\n', ' ').strip(), "link_source": "markdown"})
    for slug, name, s, e in concepts:
        add(turn_slug, slug, "mentions", f"mentioned: {name}")
    # adjacent concept pairs only; infer from the text BETWEEN them (must be short).
    for a, b in zip(concepts, concepts[1:]):
        between = prose[a[3]:b[2]]
        if 0 <= len(between) <= gap:
            typ = infer_link_type(between)
            if typ != "mentions":
                add(a[0], b[0], typ, f"{a[1]} …{between.strip()}… {b[1]}")
    return concepts, edges
