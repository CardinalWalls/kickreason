# Proof of MiroMind API usage

_Auto-scanned from `dataset/runs/` + `graph/graph.json`. Re-run `python3 dataset/api_usage.py`._

## Totals (what we have actually run)

- **36 real API calls** captured (29 ok, 7 throttled/HTTP-429, 0 other-failed)
- **12,249,422 tokens** of deep research
- **~80 minutes** of agent run-time
- **268 web searches**, **139 pages fetched**, **1,690 sources retrieved**

## Rate-limit proof (we probed the live ceiling)

- **7 calls were rejected with HTTP 429** `{"error":"QPS limit exceeded","limit":5}` during a concurrency=12 burst.
- This is hard evidence the hosted API enforces a **live 5 requests/sec limit** — the 429s are a feature of the proof, not a bug: they show we actually hit the server, not a mock.
- The throttled calls are counted as attempts but **excluded from the `ok` set** (and they carry no token usage, so they don't inflate totals).

## Every call (receipts)

| call | sec | tokens | search | fetch | sources | status |
|---|--:|--:|--:|--:|--:|:--:|
| `euro24-final-leakprobe.json` | 435 | 3,658,231 | 57 | 28 | 287 | ✓ |
| `exp-batch.json:batch` | 84 | 81,326 | 6 | 3 | 38 | ✓ |
| `exp-batch.json:single` | 271 | 972,924 | 32 | 7 | 152 | ✓ |
| `exp-concurrency.json#0` | 3 | 0 | 0 | 0 | 0 | 429 |
| `exp-concurrency.json#1` | 6 | 5,675 | 0 | 0 | 0 | ✓ |
| `exp-concurrency.json#2` | 6 | 5,631 | 0 | 0 | 0 | ✓ |
| `exp-concurrency.json#3` | 4 | 0 | 0 | 0 | 0 | 429 |
| `exp-concurrency.json#4` | 3 | 0 | 0 | 0 | 0 | 429 |
| `exp-concurrency.json#5` | 3 | 0 | 0 | 0 | 0 | 429 |
| `exp-concurrency.json#6` | 9 | 5,956 | 0 | 0 | 0 | ✓ |
| `exp-concurrency.json#7` | 10 | 6,040 | 0 | 0 | 0 | ✓ |
| `exp-concurrency.json#8` | 4 | 0 | 0 | 0 | 0 | 429 |
| `exp-concurrency.json#9` | 3 | 0 | 0 | 0 | 0 | 429 |
| `exp-concurrency.json#10` | 6 | 5,661 | 0 | 0 | 0 | ✓ |
| `exp-concurrency.json#11` | 3 | 0 | 0 | 0 | 0 | 429 |
| `exp-fullmodel-advance.json` | 291 | 218,790 | 13 | 5 | 81 | ✓ |
| `exp-fullmodel-match.json` | 224 | 233,737 | 12 | 2 | 77 | ✓ |
| `exp-fullmodel-prop.json` | 101 | 108,916 | 7 | 0 | 41 | ✓ |
| `exp-update-latency.json` | 0 | 2,759,042 | 0 | 0 | 123 | ✓ |
| `narrative-sau-arg-2022.json` | 63 | 29,268 | 6 | 0 | 0 | ✓ |
| `narrative-usa-advance.json` | 415 | 110,650 | 4 | 5 | 35 | ✓ |
| `probe-advance-terse.json` | 323 | 1,781,101 | 41 | 13 | 200 | ✓ |
| `probe-match-full.json` | 52 | 88,430 | 8 | 0 | 76 | ✓ |
| `probe-match-fullmodel.json` | 228 | 184,315 | 9 | 3 | 78 | ✓ |
| `probe-match-terse.json` | 110 | 0 | 5 | 4 | 32 | ✓ |
| `probe-prop-terse.json` | 140 | 0 | 5 | 2 | 21 | ✓ |
| `wc26-golden-boot.json` | 260 | 89,691 | 3 | 5 | 20 | ✓ |
| `wc26-spain-final.json` | 73 | 28,258 | 3 | 1 | 9 | ✓ |
| `wc26-usa-advance.json` | 734 | 939,625 | 14 | 32 | 100 | ✓ |
| `wc26-winner.json` | 222 | 209,761 | 4 | 7 | 36 | ✓ |
| `graph.json:champion` | 85 | 318,872 | 14 | 7 | 84 | ✓ |
| `graph.json:france_final` | 82 | 49,728 | 4 | 1 | 33 | ✓ |
| `graph.json:france_match` | 345 | 189,576 | 6 | 11 | 52 | ✓ |
| `graph.json:spain_final` | 117 | 152,612 | 10 | 2 | 78 | ✓ |
| `graph.json:spain_match` | 16 | 15,606 | 2 | 0 | 10 | ✓ |
| `graph.json:star_fitness` | 87 | 0 | 3 | 1 | 27 | ✓ |

## Files scanned

- `runs/euro24-final-leakprobe.json` — 1 call
- `runs/exp-batch.json` — 2 calls (batch vs single)
- `runs/exp-concurrency.json` — 12 attempts (concurrency probe: 5 ok / 7 HTTP-429 throttled — hit live 5-QPS limit)
- `runs/exp-fullmodel-advance.json` — 1 call
- `runs/exp-fullmodel-match.json` — 1 call
- `runs/exp-fullmodel-prop.json` — 1 call
- `runs/exp-fullmodel-summary.json` — aggregate (skipped to avoid double-count)
- `runs/exp-update-latency.json` — 1 call
- `runs/narrative-sau-arg-2022.json` — 1 call
- `runs/narrative-usa-advance.json` — 1 call
- `runs/probe-advance-terse.json` — 1 call
- `runs/probe-match-full.json` — 1 call
- `runs/probe-match-fullmodel.json` — 1 call
- `runs/probe-match-terse.json` — 1 call
- `runs/probe-prop-terse.json` — 1 call
- `runs/probe-summary.json` — aggregate (skipped to avoid double-count)
- `runs/wc26-golden-boot.json` — 1 call
- `runs/wc26-spain-final.json` — 1 call
- `runs/wc26-usa-advance.json` — 1 call
- `runs/wc26-winner.json` — 1 call
- `graph/graph.json` — 6 calls (graph nodes)

_Tokens=0 means the call returned no usage block (e.g. the empty-content returns, throttled 429s, or graph nodes saved without usage). Latency still proves the call ran._