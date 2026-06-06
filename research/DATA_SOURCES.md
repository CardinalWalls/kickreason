# DATA SOURCES — real, free WC2022 resources per layer

> **We are not a bet demo.** Betting/CLV is **one** of six professional domains. The product is the
> compiler: **one verified MiroMind trace, re-read into each domain's own metric.** This file is the
> data spine for that — per layer: **source → link → access → acceptance criteria → status.** Ready to
> paste into `TASKS.md`. Every source below was checked to exist and be free (2026-06-05).

## The six professional domains → our product layers

| # | Professional domain | What they grade on | Our layer |
|---|---|---|---|
| 1 | Quant prediction / pro betting (Starlizard, Smartodds; bench = Pinnacle) | **CLV / Brier** (not hit-rate) | **ODDS / CALIBRATION** |
| 2 | Data suppliers (Sportradar, Opta/Stats Perform, StatsBomb, SkillCorner, Impect) | stable IDs + advanced metrics + latency/accuracy SLA | **STATS** + **MAGIC-MOMENT** |
| 3 | Commentary / media narrative (broadcasters, Guardian/Athletic, Opta Analyst, Tifo) | citable facts, named sources, speed, story-hooks | **NARRATIVE** |
| 4 | **Traffic / growth / fan-engagement** (FotMob/OneFootball, club social, SEO, fantasy) | **CTR · retention · dwell · push-reach · virality** | **TRAFFIC** *(new — see decision below)* |
| 5 | Betting operators / trading desks (bet365, DraftKings) | low-latency official data, risk, in-play pricing | (counterparty to #1 — not a build target) |
| 6 | Club analysis/scouting + integrity + academia | signing ROI · anomaly precision · published Brier | RECRUITMENT / INTEGRITY (B2B, later) |

**The through-line:** the same trace that prices a match (1) is the stat pack (2), the story hook (3),
and the moment that gets distributed (4). Produce once, re-read into each domain's metric — that is the
compiler, and the wedge is that **every re-read carries a published, self-graded accuracy number** (in
plain words: we show our score where the whole industry hides it).

---

## Layer-by-layer catalog

**Status:** ✅ HAVE (in `lib2022/`) · ✓ VERIFIED (confirmed free, not yet pulled) · ⬜ TO-BUILD

### Layer 1 — ODDS / CALIBRATION  (domain 1)
| Source | Link | Access | Acceptance criteria | Status |
|---|---|---|---|---|
| FiveThirtyEight WC2022 SPI (per-match 1X2 + xG) | 538 GitHub `data/` / Kaggle `kutlukatalay/2022-fifa-world-cup-predictions` | merged | model favourite-Brier **0.2399** computed; our model must beat it | ✅ HAVE `forecast_538.json` |
| World Football Elo (pre-WC ratings) | eloratings.net | merged | per-match win-expectancy, Brier **0.2911** | ✅ HAVE `odds_baseline.json` |
| martj42 international results 1872–2026 (results + goalscorers + shootouts) | Kaggle `martj42/international-football-results-from-1872-to-2017` | `kaggle datasets download` | retrain Elo on full international history (not just 32 static ratings); ratings reproduce, then grade | ✓ VERIFIED |
| Real **market** closing odds — OddsPortal WC2022 results pages | oddsportal.com/football/world/world-cup-2022/results/ | scrape (JS, hard) — hero matches first | real closing 1X2 for ≥ the hero matches → true CLV vs Pinnacle-style line | ⬜ TO-BUILD (hard) |
| Real **market** — Betfair historical exchange | historicdata.betfair.com (register) | register + download | closing exchange price + traded volume for hero matches → CLV | ⬜ TO-BUILD |
| 10 hand-sourced market cases | — | — | the only real-market anchor we hold today | ✅ HAVE `../seed-resolved.json` |
| ⚠️ football-data.co.uk | — | — | **NOT a WC source** (leagues only) — do not rely | n/a |

### Layer 2 — STATS  (domain 2)
| Source | Link | Access | Acceptance criteria | Status |
|---|---|---|---|---|
| StatsBomb Open Data (events, xG, OBV-able, lineups, 360) | github.com/statsbomb/open-data (comp 43 / season 106) | pulled | xG/possession/passing per match, all 64, sourced | ✅ HAVE `lib2022/` |
| FBref WC2022 (Opta-derived season tables) | fbref.com/en/comps/1/2022/ | scrape / `soccerdata` pkg (historical, frozen post-Jan-2026) | cross-check StatsBomb xG vs FBref/Opta xG per hero match (provider-divergence view) | ✓ VERIFIED |
| FIFA Training Centre — TSG + Enhanced Football Intelligence | fifatrainingcentre.com/en/fwc2022/ | free web / PDF | official post-match metrics (15,000+ pts/game: line-breaks, phases of play) per hero match | ✓ VERIFIED |

### Layer 3 — MAGIC-MOMENT / EVENT-TRUTH  (domain 2)
| Source | Link | Access | Acceptance criteria | Status |
|---|---|---|---|---|
| StatsBomb events (goals/scorer/minute/xG + shot freeze-frames) | as above | pulled | every goal w/ minute+player+xG; 360 frame available, all 64 | ✅ HAVE |
| Fjelstul World Cup Database (1930–2022: goals, penalties, bookings, subs, squads) | github.com/jfjelstul/worldcup (CSV/JSON/SQLite, CC-BY-SA) | GitHub download | independent cross-validation of goals/cards/subs vs StatsBomb (catch capture errors) | ✓ VERIFIED |

### Layer 4 — NARRATIVE  (domain 3)
| Source | Link | Access | Acceptance criteria | Status |
|---|---|---|---|---|
| **Guardian Open Platform API** (full article body text, named bylines) | open-platform.theguardian.com | **free key**, 5,000 calls/day, full text | ≥5 sourced full-text WC2022 articles per hero match, stored w/ byline+URL+date — the legal pipeline | ✓ VERIFIED (the narrative unlock) |
| Opta Analyst WC2022 articles | theanalyst.com | free web fetch | structured tactical analysis per hero match, named-source | ✓ VERIFIED |
| MiroMind hero traces | — | API | sourced storylines (Saudi-Arg, Morocco run, final) | ✅ HAVE `runs/narrative-*.json` |
| ⚠️ The Athletic | — | paywalled | **not a pipeline** — do not scrape | n/a |

### Layer 5 — TRAFFIC / GROWTH / FAN-ENGAGEMENT  (domain 4 — NEW)
> The layer our model is missing. Graded on engagement, not correctness. **2022 > 2026 for prototyping
> it:** X/Reddit live APIs are now paid, so **historical dumps are the only realistic access** — and 2022
> has them. The trigger is shared with MAGIC-MOMENT (a goal fires both); the metric is different.

| Source | Link | Access | Acceptance criteria | Status |
|---|---|---|---|---|
| WC2022 tweets + sentiment dumps | Kaggle `konradb/qatar-world-cup-2022-tweets` (primary, 124k, +followers), `deepeshnigamdata/...` (100k), `tirendazacademy/...` (labelled, opening day) | `kaggle datasets download` | **DONE** — 224k tweets → per-day volume/reach + hero hourly spike. Saudi-Arg: 91% of day's tweets in the goal hour, Saudi mentions overtake Argentina | ✅ HAVE `lib2022/traffic/` |
| Google Trends | trends.google.com / `pytrends` | free | search-interest time-series; corroborate spikes | ⬜ pytrends **BLOCKED** by Google → manual CSV export fallback (`build_trends.py`) |
| YouTube official highlight view counts | YouTube Data API v3 | free quota | per-highlight views/likes = "did the moment travel" metric | ✓ VERIFIED |
| FIFA official audience/reach report (≈5bn reach) | inside.fifa.com | free PDF | tournament-level reach benchmarks (context, not per-match) | ✓ VERIFIED |
| ⚠️ X/Twitter & Reddit **live** APIs | — | **paid now** | use historical dumps instead — this is why 2022 is the slice | n/a |

---

## The one decision: TRAFFIC as a 5th layer, or merge into MAGIC-MOMENT?

**Recommendation: a distinct 5th layer.** They share a *trigger* but not a *metric*:
- **MAGIC-MOMENT** answers *"what happened and did it matter?"* — event truth, graded by xG / win-prob swing. Profession: editor/clipper. Data: event + 360.
- **TRAFFIC** answers *"did people engage, and how do we distribute it?"* — graded by CTR / retention / push-reach / virality. Profession: growth/social/product. Data: sentiment / trends / play-counts.

Merging would collapse two different metrics and two different buyers into one box and lose the engagement
grade — the very thing domain 4 lives on. Keep them separate, wired by the shared event trigger
(MAGIC-MOMENT = the source moment → TRAFFIC = distribution + engagement on it).

## Net: four layers already have REAL free 2022 data to land on
ODDS (538 + Elo + martj42) · STATS (StatsBomb + FBref + FIFA TSG) · MAGIC-MOMENT (StatsBomb + Fjelstul) ·
NARRATIVE (Guardian API + Opta Analyst). TRAFFIC has real dumps too (Kaggle tweets + Trends + YouTube).
**Only true remaining gap:** real-market closing odds at scale (OddsPortal/Betfair scrape) for genuine CLV.
