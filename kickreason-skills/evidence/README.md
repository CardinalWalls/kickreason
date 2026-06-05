# Evidence — the loop closes on a finished tournament (2022)

Proof the pipeline is real, not a slideshow. Every number here is `REAL` — computed by the skills from the
2022 World Cup library (rebuild with `wc-data-library`).

## The graded record
| Claim | Value | Source |
|---|---|---|
| Graded arc Brier (the node set) | **0.262** | `forecast-grading` / arc_build.py |
| FiveThirtyEight favourite-Brier (all 64) | **0.240** | `build_538_baseline.py` |
| Elo favourite-Brier (all 64) | **0.291** | `build_odds_baseline.py` |
| Coin-flip reference | 0.250 | — |
| Market on the famous upsets | 0.494 | golden_template.py |

## The hero (Saudi 2–1 Argentina)
- Argentina **xG 2.49 vs 0.15**, 15 shots to 3, 69% possession — **and lost**. `StatsBomb`
- Al-Dawsari 52' winner: **xG 0.033** — a ~1-in-30 shot. `StatsBomb`
- Pre-match: 538 said 72% Argentina · market 87% · Elo 95% — **all graded wrong**.

## The live update (the doctor)
- News "Brazil striker out, 1h pre-kickoff" → re-ran ONE node → revised **Brazil 50/26/24** in **5.9 min**,
  sourced ESPN. `captured run`

## The traffic layer
- Saudi–Argentina day: **91%** of match-tweets in the goal hour; Saudi mentions overtook Argentina.
- France–Morocco semi drove **236M** follower-reach (the tournament's biggest). `224k-tweet corpus`

*What's MODEL/MOCK is labelled as such wherever it appears; nothing here is.*
