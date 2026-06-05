---
name: wc-data-library
description: >-
  Build a graded World Cup data library from free PRIMARY sources — StatsBomb event data
  (xG, 360), World Football Elo, the FiveThirtyEight forecast, and tweet/engagement dumps —
  with derived per-player / per-team / bracket tables. Use whenever you need real, sourced
  football match data to ground or grade a forecast, to (re)build the tournament dataset, or
  to demonstrate the loop on a finished tournament (2022).
---

# wc-data-library — the graded tournament dataset

Fetches and derives a complete, sourced tournament library (all 64 matches): events + xG + 360, Elo +
FiveThirtyEight odds baselines (graded by Brier), and a fan-engagement layer — every value `REAL`. This is
the resolved truth `forecast-grading` grades against, and the proof the loop closes on a finished
tournament (2022).

## Procedure
1. **Fetch** StatsBomb open data (competition 43 / season 106 = 2022 WC; CC-BY-NC) → events, lineups, 360.
2. **Derive** per-match (xG, shots, goals w/ minute+xG, cards), per-player (681), per-team, bracket.
3. **Baselines** — World Football Elo (eloratings.net) + FiveThirtyEight SPI forecast, each graded by Brier.
4. **Traffic** — tweet-volume/sentiment per match-day + the hero moment→spike (StatsBomb event-aligned).
5. **Emit** `REAL`-tagged tables + a coverage README that marks every gap honestly.

## Run
```bash
python3 scripts/build_lib2022.py        # fetch + derive all 64 matches (events excluded from git)
python3 scripts/derive_lib2022.py       # players / teams / bracket / leaders
python3 scripts/build_traffic_layer.py  # tweet engagement + hero spike (needs the Kaggle dumps)
```

## Output
`lib2022/`: `index.json` · `results.json` · `matches/{id}.json` · `players.json` · `teams.json` ·
`bracket.json` · `odds_baseline.json` (Elo) · `forecast_538.json` · `traffic/`. Hero check: Argentina
2.49 xG vs 0.15 — and lost; Al-Dawsari 52' winner xG 0.033; 538 72% / market 87% / Elo 95% all graded wrong.

## References
`references/data-sources.md` — per-layer source → link → access → acceptance (StatsBomb · 538 · Elo ·
Guardian API · Kaggle tweets · FIFA TSG). The raw 191 MB events dir is git-ignored; regenerate with the builder.
