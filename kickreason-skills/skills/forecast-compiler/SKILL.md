---
name: forecast-compiler
description: >-
  Turn a deep-research trace into STRUCTURED debatable forecast nodes — each one the answer,
  the why, the strongest counter-case, and what-would-change-it — and wire them into a node
  DAG you can update on news. Use whenever research output needs structuring into forecast
  nodes, a forecast graph, a "debatable node", or when breaking news should re-run ONE node
  and propagate "stale" up to its parents (the doctor). Structuring is a second step because
  the research model returns prose, not JSON.
---

# forecast-compiler — trace → debatable nodes → DAG

Extracts forecast nodes from a (mostly-thinking) MiroMind trace and renders each as a debatable node:
the answer + the *why* + the strongest counter-case + what-would-change-it, with source tiers. Wires the
DAG (champion ← path ← match ← sub-nodes) and runs the news "doctor" (re-run one node, propagate up).

## Procedure
1. **Extract deterministically** (post-hoc). The model won't self-structure — asking for a JSON fence
   yields `prob=None`. A node = (evidence event) + (thinking span around it) + (probability delta) + sources.
2. **Detect debatable** nodes — flag when the trace *hedges without resolving*, when claim-vs-negation
   retrieval pulls comparably-credible sources, or when the lean *diverges from the de-vigged market*.
   Keep these; drop settled nodes. See `references/debatable-detection.md`.
3. **Build the DAG** + dependency edges. On news, re-run only the sick node and mark its parents `stale`,
   then re-grade and propagate (the doctor).

## Run
```bash
python3 scripts/node_extract.py     # trace → contract nodes
python3 scripts/graph_build.py --update   # news → re-run one node → propagate stale up
```

## Output
A set of debatable-node objects (per the node contract) + a DAG with propagation. Each node carries
answer · why · counter-case · what-would-change-it · sources · `_unpriced` flag (breaking news the line
hasn't absorbed).

## References
`references/node-contract.md` (the node schema) · `references/debatable-detection.md`
