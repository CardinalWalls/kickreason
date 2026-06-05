# lib2022 — the real 2022 FIFA World Cup data library

> Built by `python3 dataset/build_lib2022.py` (fetch) + `python3 dataset/derive_lib2022.py` (aggregate).
> **Every number here is fetched or derived from primary event data — nothing typed by hand.**
> This replaces the old "highlight-reel" state (10 curated cases) with a complete tournament.

## Source
**StatsBomb Open Data** (CC-BY-NC 4.0) — the full 2022 World Cup, competition_id **43** / season_id **106**.
All 64 matches, every on-ball event with StatsBomb **xG**, lineups, and **360 freeze-frames available for all 64**.
Raw mirror: `https://github.com/statsbomb/open-data`. License requires attribution + non-commercial use.

## What's in it (193 MB)

| File / dir | Contents | Rows |
|---|---|---|
| `index.json` | All 64 matches: date, stage, teams, score, stadium, referee, 360-flag | 64 |
| `results.json` | Compact ground truth per match (winner, score, team xG, scorers w/ xG) — **the grading key** | 64 |
| `matches/{id}.json` | Rich per-match record: team xG, shots, SoT, possession proxy, goals (min+player+xG+type), cards, shootout | 64 |
| `events/{id}.json` | **Raw** StatsBomb events — every pass/shot/carry/pressure/duel (the full library) | 234,637 total |
| `lineups/{id}.json` | Starting XI + subs + positions | 64 |
| `players.json` | Per-player tournament totals: goals, xG, shots, SoT, assists, key passes, minutes, apps, cards | 681 |
| `teams.json` | Per-team totals: goals for/against, xG for/against, shots, matches | 32 |
| `bracket.json` | Knockout tree R16 → Final with scores | — |
| `leaders.json` | Ready leaderboards: top scorers, top xG, assists, xG over/under-performers | — |
| `elo_ratings.json` | Pre-tournament World Football Elo for all 32 teams (eloratings.net, ~19 Nov 2022) | 32 |
| `odds_baseline.json` | **ODDS layer** — per-match Elo win-expectancy + favourite prob, self-graded by Brier | 64 |
| `forecast_538.json` | **ODDS/CALIBRATION** — FiveThirtyEight SPI forecast, full 1X2 (prob1/draw/prob2) + 538 xG/SPI, graded | 64 |
| `sources/fivethirtyeight/` | Provenance: 538's `wc_matches.csv` + `wc_forecasts.csv` (via Kaggle mirror) | — |
| `traffic/` | **TRAFFIC layer** — fan-engagement from 224k WC2022 tweets: per-day volume/reach + hero moment→spike | 64 days |

## Coverage by view-layer (see `brainstorm/intel-industry-view-layers.md`)

| Layer | Status | Backed by |
|---|---|---|
| **RESULTS** (grading ground truth) | ✅ **COMPLETE** | official scores, all 64 |
| **STATS** | ✅ **COMPLETE** | xG, shots, possession, 234k events |
| **MAGIC-MOMENT** | ✅ **COMPLETE** | goals/scorers/minutes/xG + 360 freeze-frames |
| **PLAYER-PROPS** | ✅ **COMPLETE** | 681 players, real per-player totals |
| **ODDS / CALIBRATION** (probability) | ✅ **TWO model baselines** (Elo + **538**, all 64) + 10 real-market cases | `odds_baseline.json` · `forecast_538.json`; market: `../seed-resolved.json` |
| **NARRATIVE** (sourced storylines) | 🟡 **HERO matches** | Saudi–Arg + Morocco run + Final (`../runs/narrative-*.json`) |
| **TRAFFIC** (fan-engagement, domain 4) | ✅ **NEW layer** | 224k tweets → per-day volume/reach + hero spike (`traffic/`) |

## The ODDS / CALIBRATION layer — two real model baselines + the market gap
We grade forecasts against **two recognized model baselines** (neither is faked; both self-graded by Brier):

| Baseline | Coverage | Mean favourite Brier | What it is |
|---|---|---|---|
| **Elo win-expectancy** (`odds_baseline.json`, `build_odds_baseline.py`) | 64/64 | **0.2911** | eloratings.net pre-WC ratings → two-way (no draw model) |
| **FiveThirtyEight SPI** (`forecast_538.json`, `build_538_baseline.py`) | 64/64 | **0.2399** | recognized published forecast, full 1X2 incl. draw; also 538 xG/SPI |

538 beats Elo (0.24 < 0.29) because it models draws, and 0.24 is below the 0.25 coin-flip line — a genuinely
good forecast to calibrate against. **Hero escalation:** 538 said Argentina **72%** → real market **87%** →
Elo **95%** → Argentina LOST. All wrong, increasingly confident — the calibration story in one row.

**The market gap (verified, not faked):** there is **no clean free WC2022 market-odds dataset** — confirmed
on Kaggle (`"world cup 2022 betting odds"` → none; the odds sets are club leagues only; `football-data.co.uk`
excludes internationals). Real market closing odds exist only as the **10 hand-sourced cases** in
`../seed-resolved.json`. For true CLV at scale you'd need a paid/scraped odds archive — layer it on later.

## Remaining gap (do not fake)
- **NARRATIVE at scale** — sourced storylines for all 64 (we build hero matches only, via `../narrative.py`
  / `../narrative_heroes.py`; full-tournament narrative = a separate MiroMind API spend).

## Proof it's real (spot-checks the script prints)
- Golden Boot: **Mbappé 8, Messi 7** (correct) · Top xG: **Messi 6.0**.
- Hero match (`matches/3857300.json`): Argentina **2.49 xG / 15 shots / 69% poss** — and **LOST 1–2**;
  Al-Dawsari's 52' winner **xG 0.033**. The upset that broke the 87% market line, in data.

## Use
```python
import json
results = json.load(open("dataset/lib2022/results.json"))   # grade any forecast
hero    = json.load(open("dataset/lib2022/matches/3857300.json"))
players = json.load(open("dataset/lib2022/players.json"))    # player-prop answers
```
