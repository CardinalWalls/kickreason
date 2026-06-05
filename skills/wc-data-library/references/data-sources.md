# Data sources — per layer (source → access → acceptance)

All free, all verified. Every value emitted is `REAL`. Mark any gap honestly.

| Layer | Source | Access | Acceptance |
|---|---|---|---|
| **Results / Stats / Magic-moment** | **StatsBomb Open Data** (comp 43 / season 106; CC-BY-NC) | `build_lib2022.py` (raw JSON from GitHub) | all 64 matches: events + xG + 360; goals w/ minute+xG |
| Player-props | derived from StatsBomb events | `derive_lib2022.py` | 681 players (Golden Boot resolves Mbappé 8 / Messi 7) |
| Stats cross-check | FBref (Opta-derived, historical) | scrape / `soccerdata` | xG cross-check vs StatsBomb |
| Stats (official) | FIFA Training Centre / TSG | free web/PDF | Enhanced Football Intelligence metrics |
| **Odds / calibration** | World Football Elo (eloratings.net) | `build_odds_baseline.py` | per-match win-expectancy, Brier 0.291 |
| Odds / calibration | **FiveThirtyEight SPI** (via Kaggle mirror) | `build_538_baseline.py` | full 1X2 + xG, Brier 0.240 |
| Odds (market) | OddsPortal / Betfair historical | scrape / register | real closing line → CLV (the one gap; 10 hand-sourced cases held) |
| **Narrative** | **Guardian Open Platform API** (free key, full text) | API (5k/day) | sourced storylines per hero match (the legal pipeline) |
| Narrative | Opta Analyst (theanalyst.com) | free web | tactical analysis |
| **Traffic** | Kaggle WC2022 tweet dumps (konradb, deepesh, tirendaz) | `build_traffic_layer.py` | per-day volume/reach + hero moment→spike |
| Traffic | Google Trends (pytrends) | free | ⚠️ often rate-limited → manual CSV fallback |

**Honest gaps:** real *market* closing odds at scale (no clean free dataset — football-data.co.uk excludes
internationals); narrative beyond the hero matches (MiroMind API spend). Everything else lands free + sourced.
