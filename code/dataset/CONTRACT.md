# Demo Contract — the spec every stage conforms to

One contract so the **mock** (for the video, now) and the **real pipeline** (WF1/WF2) produce the *same shape*. Each stage: input → output → which engine makes it → the proof rule.

> Thread for the demo: the graph is rooted at **CHAMPION**; we zoom into one real node — **"Will the USMNT advance from Group D?"** — because we have the richest real trace for it (90% call, 100 real sources). Host-nation question = audience-relevant for a US-hosted World Cup.

## Pipeline stages

| # | Stage | Input | Output (schema) | Engine | Proof rule |
|---|-------|-------|-----------------|--------|-----------|
| 0 | **Question** | a node question | `{node_id, question, graph_parent}` | us | — |
| 1 | **Trace** | question | MiroMind SSE trace: `steps[{action:thinking\|web_search\|fetch, text\|keywords\|url\|snippet}]` + `content` + `sources[]` | **MiroMind API** (`mirothinker-1-7-deepresearch-mini`) | every claim must carry a source URL |
| 2 | **Nodes** | trace | `node[]` (see NODE schema) | **compiler** (`node_extract.py`; thinking-capture from `miro.py`) | each node.sources ⊆ trace sources; whitelisted source ⇒ higher trust |
| 3 | **Graph** | nodes | `graph.json` node with `prob` **computed from its child nodes** | graph assembly | prob is derived, never hardcoded |
| 4 | **Views** | graph + nodes | 3 renders (fan / analyst / moving-line) of the SAME nodes | `views.py` | each view cites the same underlying sources |
| 5 | **Update (doctor)** | a news event + one node | re-run that node → new prob → propagate `stale` up | `graph_build.py --update` | before/after both sourced + timestamped |
| 6 | **Value (回溯)** | nodes + `seed-resolved.json` | `value_score[0..1]` per node | `node_eval.py` | scored from real resolved past results |

## NODE schema (the contract every module uses)
```json
{ "node_id": "...", "graph_parent": "usa_advance",
  "trigger": {"action": "web_search|fetch", "query_or_url": "..."},
  "evidence": "the thinking span around the trigger (summarized)",
  "judgment": "the forecast-relevant conclusion",
  "prob_direction": "up|down|neutral",
  "sources": ["https://..."],
  "source_tier": 1,
  "layer": "magic_moment|narrative|odds|stats",
  "value_score": 0.0 }
```

## Kernel — how a node is built (PROVEN 2026-06-05)
**TWO MODELS, not one** — because MiroMind will NOT emit structured output (verified 3×: it ignored a JSON contract AND named markdown headers; it always writes its own free-form report).
1. **Research = MiroMind.** Prompt the node + `current_status` as a genuine *research* task → rich, sourced, status-conditioned PROSE (sau_arg_2022 returned 14 real sources). It is the researcher, never the structurer.
2. **Structure = a format-obedient model** (StructuredOutput / Haiku-class). It extracts the prose → the layered node: `probability`, `direction` (vs `moved_from`), and the 4 layers each `{text, source_url}` where every `source_url` is taken from the REAL retrieved sources (never invented). **PROVEN:** `sau_arg_2022` → a fully valid layered, sourced node (`runs/kernel-structured.json`).
- Rule: never ask MiroMind for JSON/headers. The research prompt MUST actually retrieve (a probability-only framing under-captures sources, e.g. `usa_advance` got 0 — structurer then honestly flags `all_sources_real=false`).
- Kernel output schema = the layered node above (4 layers × {text, source_url}); the flat `layer`-tagged node below is the graph/extract granularity.

## Authoritative-source whitelist (the "fancy with proof" layer)
Node value and on-screen credibility scale with source tier. (Tiers seen live in our real USMNT run are marked ✓.)

- **Tier 1 — official / model / sharp market:** FIFA.com ✓ (fixtures, rankings, draw, tie-breakers), Opta / The Analyst (supercomputer probs), Pinnacle (sharp closing line / CLV), Polymarket (real-money crowd), FIFA World Ranking ✓.
- **Tier 2 — top media / odds aggregators:** ESPN ✓, BBC Sport, NYT / The Athletic ✓, Oddschecker, BetMGM ✓ / DraftKings ✓.
- **Tier 3 — stats / ratings:** Sofascore, FBref / StatsBomb, WhoScored, eloratings.net / clubelo.
- **Tier 4 — long-tail blogs / forums:** allowed as corroboration only; never the sole source of a node.

Rule: a node's `source_tier` = best tier among its sources; `value_score` weights tier × prob_direction-magnitude × signal-class-historical-edge (from 回溯).

## Where each engine plugs in
- **MiroMind hosted API** → Stage 1 (the trace) and Stage 5 (the re-run). Slow (minutes), ~1/6 empty (retry).
- **Compiler** (`compiler/` + `dataset/node_extract.py`, `node_eval.py`, `views.py`) → Stages 2,3,4,6. This is the IP.
- **MiroFlow** (self-hostable open-source; arXiv 2602.22808; github.com/MiroMindAI/MiroFlow) → the **production engine for Stage 1 + 5 at scale**, and it maps 1:1 onto our idea: MiroFlow IS a *directed agent graph of nodes* (Control/Agent/Foundation tiers) with sub-agents, custom MCP tools, and parallel/sequential deps. It returns a `trajectory` with `tool_calls_data` — **more granular and easier for the compiler to extract nodes from** than the hosted flat SSE. Three unlocks vs the hosted API:
  1. **Cost / concurrency** — self-host on one RTX 4090, no per-call fee, our own parallelism → defuses the concurrency kill-switch; breaks even ~5–10k nodes.
  2. **Valid backtest (回溯)** — a date-restricted-retrieval custom tool runs an agent backtest *without lookahead leakage* — the thing we couldn't do before, and how we score node value honestly.
  3. **Control** — custom sub-agent prompts + tools (live odds feeds, FIFA data, our source whitelist).
  - **DECISION — two layers, do NOT conflate:**
    - **BORROW MiroFlow's DESIGN now** (free, zero infra): our forecast-graph *is* its agent-graph; **align our node + trajectory schema to its `trajectory` / `tool_calls_data` ontology** so the graded trajectories we emit are MiroVerse-ingestion-ready (the flywheel); use its **planner → sub-agent** decomposition as the pattern for how a parent node spawns its child nodes (`depends_on`). This shapes the compiler + this contract *today*.
    - **RUN MiroFlow's ENGINE later** (self-host on a 4090): only at scale + for the date-restricted backtest. The **60s demo uses the hosted API** — no infra to stand up now.
  - Unknowns: hosted↔MiroFlow trace-ontology parity, native batch, hosted pricing (service@miromind.ai).

## Honesty rules (non-negotiable)
- Forecast numbers are **computed from nodes**, never typed in.
- Labels say **"sourced & inspectable"** unless a real second-source check ran (then "verified").
- Accuracy is graded **forward only** (lock before kickoff → grade after) by result + closing-line value (CLV) — the standard FutureX itself uses, the thing KickOracle fakes.
- Anything not yet computed live is labeled **[MOCK]** in the render.
