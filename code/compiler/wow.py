"""
wow.py — the 意图萃取 / 降维换行动 layer, ported from wow-harness (the intent-compile
reference) and the intent-ledger contract loop.

  - Change Classification (policy|contract|implementation)  <- wow-harness lead SKILL
  - hedge-word scanner + vN-final freeze                     <- wow-harness plan-lock SKILL
  - gate_pack emitted on EVERY compile step                  <- wow-harness lead gate_pack
  - escalation channel (message_for_user required != auto)   <- wow-harness bug-triage state file

TOWOW mapping: 降维换行动 — turn high-dim intent into a low-dim, decision-complete,
executable form; the freeze is "no residual decision entropy for the executor".
"""
import re

# ── Change Classification (wow-harness): sets the structure floor per intent-unit ──
_POLICY_RE   = re.compile(r'\b(rule|policy|principle|must|never|always|constraint|invariant|boundary|ethic)\b', re.I)
_CONTRACT_RE = re.compile(r'\b(schema|interface|api|format|ontology|field|protocol|seam|contract|trajectory shape)\b', re.I)
def classify_change(text):
    if _POLICY_RE.search(text):
        return "policy"
    if _CONTRACT_RE.search(text):
        return "contract"
    return "implementation"

# ── plan-lock hedge-word scanner (wow-harness): residual decision entropy ──
# Verbatim hedge set from wow-harness plan-lock SKILL, plus the project's own.
HEDGE_PATTERNS = [
    r'需确认', r'待定', r'\bTBD\b', r'复用或重定义', r'参考.{0,6}模式', r'大概在', r'应该是',
    r'\bmaybe\b', r'\bprobably\b', r'\bsomehow\b', r'\bfigure out\b', r'\bplaceholder\b',
    r'\bone of\b.*\bor\b', r'\bdecide later\b', r'\bsome (?:scene|instance|metric)\b',
]
_HEDGE_RE = re.compile('|'.join(HEDGE_PATTERNS), re.I)
def scan_hedges(text):
    """Return list of hedge spans. Empty list = freezeable to vN-final."""
    return [m.group(0) for m in _HEDGE_RE.finditer(text)]

def freeze(version, text):
    """plan-lock freeze: tag vN-final only at zero residual decision entropy."""
    hedges = scan_hedges(text)
    if hedges:
        return {"frozen": False, "tag": None, "residual_entropy": hedges}
    return {"frozen": True, "tag": f"v{version}-final", "residual_entropy": []}

# ── gate_pack (wow-harness lead): the mandatory state-pack, emitted first ──
def gate_pack(stage, entry_satisfied, blockers, required_artifact, required_next,
              escalation="auto", message_for_user=""):
    if escalation != "auto" and not message_for_user:
        message_for_user = "[escalation set but no message provided — INVALID per wow-harness contract]"
    return {
        "current_stage": stage,
        "entry_satisfied": bool(entry_satisfied),
        "blockers": blockers,
        "required_artifact": required_artifact,
        "required_next_role": required_next,
        "escalation": escalation,                       # auto|needs_owner|needs_user_clarification|out_of_scope
        "message_for_user": message_for_user,           # REQUIRED iff escalation != auto
    }
