# The forecast-node contract

A node is the atomic unit. Extraction is deterministic and post-hoc (the model returns prose, not JSON).

## Schema
```json
{
  "id": "wc2022-grpC-sau-arg-upset",
  "question": "Will Saudi's high press + offside line break Argentina?",
  "layer": "odds | stats | narrative | magic-moment | traffic",
  "lean": 0.22,                      // our probability
  "confidence": "low | moderate | high",
  "market_implied": 0.13,            // de-vigged closing line (the thing to beat)
  "why": [                           // the layered factors
    {"factor": "tactics", "text": "...", "dir": "+upset", "sources": ["..."]}
  ],
  "counter_case": "Argentina out-create anyone (xG 2.49 on the day).",
  "what_would_change_it": "Argentina drop the line / rotate Messi.",
  "sources": [{"url": "...", "tier": "T1", "title": "..."}],
  "_unpriced": false,                // breaking news the line hasn't absorbed (only these move the forecast)
  "locked_at": "pre_kickoff",
  "graded": {"result": "SAU 2-1 ARG", "market_brier": 0.76}
}
```

## Rules
- A node = (evidence event) + (thinking span around it) + (probability delta) + sources. The intel lives in
  the **thinking**, not the search.
- **Aggregate honestly:** the forecast = the sharp de-vig anchor. Public/odds-echo nodes CONFIRM the line and
  push 0 (counting them double-counts the market). Only `_unpriced` nodes (breaking news) move it, and must
  outweigh a strong prior. Pre-news forecast = the market (one call has no edge); the unpriced injury is the edge.
- Every node carries an Evidence tag + source tiers (see `../../kickreason/references/evidence-levels.md`).
