#!/usr/bin/env bash
# verify.sh — the EXTERNAL verdict owner (contract-loop: "the controller must not
# ask the worker whether the contract passed"). Re-checks the emitted artifact
# against the evidence policy and writes contract-result.json. Zero-LLM.
set -u
HERE="$(cd "$(dirname "$0")" && pwd)"
IX="${1:-$HERE/out/trajectory-bootstrap.index.json}"
OUT="$HERE/out/contract-result.json"

python3 - "$IX" "$OUT" <<'PY'
import json, sys, re
ix_path, out_path = sys.argv[1], sys.argv[2]
ix = json.load(open(ix_path))
failures = []

# C1 schema_version present and == 1
if ix.get("schema_version") != 1:
    failures.append("schema_version != 1")

# C2 every fact with a source is dated; every claim non-empty
for f in ix.get("facts", []):
    if not f.get("claim"):
        failures.append(f"fact row {f.get('row')} has empty claim")
    if f.get("source") and not f.get("valid_from"):
        failures.append(f"fact row {f.get('row')} sourced but undated")

# C3 every ReAct step that claims a verdict 'sourced' must carry >=1 resolvable source
#    AND a non-empty observation (honest grounding: a source we actually captured).
#    "sourced" means auditable, NOT independently verified. We never emit "verified".
def _step_srcs(s):
    urls = []
    for src in (s.get("sources") or []):
        u = src.get("url") if isinstance(src, dict) else src
        if u:
            urls.append(u)
    if s.get("url"):
        urls.append(s["url"])
    return urls
for s in ix.get("steps", []):
    if s.get("verdict") not in ("sourced", "unsourced"):
        failures.append(f"step {s.get('step_id')} has stale/unknown verdict {s.get('verdict')!r} (expect sourced|unsourced)")
        continue
    if s.get("verdict") == "sourced":
        if not _step_srcs(s):
            failures.append(f"step {s.get('step_id')} verdict=sourced with no resolvable source")
        if not (s.get("observation") or "").strip():
            failures.append(f"step {s.get('step_id')} verdict=sourced with empty observation")

# C4 trust contract: escalation != auto REQUIRES a non-empty message_for_user
gp = ix.get("gate_pack", {})
if gp.get("escalation") != "auto" and not gp.get("message_for_user"):
    failures.append("gate_pack escalation != auto but message_for_user empty")

# C5 appropriate-reliance honesty: any decision with ai_correct set must have agreed set
for d in ix.get("decisions", []):
    if d.get("ai_correct") is not None and d.get("agreed") is None:
        failures.append(f"decision {d.get('decision_id')} has ai_correct but no agreed (can't score reliance)")

verdict = "pass" if not failures else "fail"
json.dump({"verdict": verdict, "failures": failures,
           "checked": {"facts": len(ix.get("facts", [])), "steps": len(ix.get("steps", [])),
                       "decisions": len(ix.get("decisions", []))}},
          open(out_path, "w"), ensure_ascii=False, indent=2)
print(f"contract verdict: {verdict}  ({len(failures)} failures)")
for x in failures:
    print("  -", x)
sys.exit(0 if verdict == "pass" else 1)
PY
