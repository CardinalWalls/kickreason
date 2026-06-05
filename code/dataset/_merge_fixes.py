#!/usr/bin/env python3
"""
_merge_fixes.py — one-time reconciliation after the wc2022-arc-fix workflow.

  python3 dataset/_merge_fixes.py /path/to/<fix-task>.output

What it does:
  1. Replace the 7 corrected nodes (from the fix workflow) into arc_2022.json by node_id.
  2. Strip helper fields (_verdict / _recheck / _seed_id / _corrections / _unsupported).
  3. PIN the 4 seed-overlap nodes' odds price to the CANONICAL value in seed-resolved.json
     (the project's established anchor that GOLDEN.md already cites), preserving the workflow's
     alternate sourced price in market_prob_basis so nothing is hidden.
  4. Rewrite dataset/arc_2022.json. (Then run arc_build.py — its drift self-check will pass.)
"""
import json, os, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ARC = os.path.join(ROOT, "arc_2022.json")
SEED = os.path.join(ROOT, "seed-resolved.json")
HELPERS = ("_verdict", "_recheck", "_seed_id", "_corrections", "_unsupported")

# arc id -> (seed id, canonical market_prob on the favourite)  [the established anchors]
PIN = {
    "arg-ksa": ("wc2022-grpC-sau-arg", 0.871),
    "ger-jpn": ("wc2022-grpE-ger-jpn", 0.677),
    "mar-por": ("wc2022-qf-por-mar", 0.60),
    "wc2022-winner": ("wc2022-outright-winner", 0.133),
}


def main():
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 dataset/_merge_fixes.py <fix-task-output.json>")
    fix_out = json.load(open(sys.argv[1]))
    fixed = (fix_out.get("result") or fix_out).get("nodes") or []
    fixed_by_id = {n.get("node_id"): n for n in fixed}

    data = json.load(open(ARC))
    nodes = data["nodes"]
    merged = []
    for n in nodes:
        nid = n.get("node_id")
        node = fixed_by_id.get(nid, n)          # prefer the corrected version
        node = {k: v for k, v in node.items() if k not in HELPERS}
        # pin canonical price for the seed-overlap anchors
        if nid in PIN:
            _, canon = PIN[nid]
            pm = node.setdefault("pre_match", {})
            workflow_price = pm.get("market_prob")
            if workflow_price is not None and abs(workflow_price - canon) > 0.005:
                pm["market_prob_basis"] = (pm.get("market_prob_basis", "") +
                    f" [pinned to project-canonical {canon} from seed-resolved.json/GOLDEN.md; "
                    f"workflow re-sourced {workflow_price} — both real, canonical kept for consistency]")
            pm["market_prob"] = canon
            od = (node.get("layers") or {}).get("odds")
            if isinstance(od, dict):
                od["market_prob"] = canon
        merged.append(node)

    data["nodes"] = merged
    data["reconciled"] = {"fixed_nodes": sorted(fixed_by_id), "pinned": sorted(PIN)}
    json.dump(data, open(ARC, "w"), indent=2, ensure_ascii=False)
    print(f"merged {len(fixed_by_id)} corrected nodes; pinned {len(PIN)} anchors; "
          f"wrote {os.path.relpath(ARC, ROOT)} ({len(merged)} nodes)")
    print("next: python3 dataset/arc_build.py")


if __name__ == "__main__":
    main()
