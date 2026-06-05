# Market baseline (track 1) — the rig works; the sample doesn't (yet)

> Auto-written by `python3 dataset/baseline.py`. The scoring math is **self-tested and
> correct** (run it — it prints PASS). But the number below is **not a real baseline**,
> and the script is honest about why. No agent is involved here — this is pure past data.

## What the rig computed on our seed rows

| Fixture | Market said favourite wins | Favourite actually won? |
|---|---|---|
| Saudi Arabia vs Argentina | 87% | NO (upset) |
| Germany vs Japan | 68% | NO (upset) |
| Portugal vs Morocco | 60% | NO (upset) |
| Georgia vs Portugal | 74% | NO (upset) |
| Spain vs England (Euro 2024 final) | 41% | yes |

**Market Brier on these 5 rows: 0.494**  ·  log loss: 1.265
(Brier: 0 = perfect, 0.25 = coin-flip, 1 = confidently wrong.)

## Why this is NOT a real baseline (the honest part)

- **The sample is upset-biased on purpose.** `seed-resolved.json` was hand-picked to
  feature famous upsets. So the market 'looks bad' here (it backed favourites who lost)
  ONLY because we cherry-picked the games it got wrong. On a full, unbiased schedule the
  market scores far better. This number would defame the market — don't quote it.
- **N is tiny (5).** You can't calibrate anything on a handful of games.
- **These are favourite-only prices, not full 1X2.** A proper de-vig needs all three
  match prices (home / draw / away) at the close; the seed has rough, single-side numbers.
- **Rows skipped** (no clean favourite price, or coin-flip/futures): Spain vs Germany (coin-flip / futures); Argentina vs France (World Cup 2022 final) (no clean favourite price); Argentina vs Colombia (Copa America 2024 final) (no clean favourite price); France vs Morocco (World Cup 2022 semi-final) (no clean favourite price); World Cup 2022 outright winner (pre-tournament futures) (coin-flip / futures).

## What a real baseline needs (the dataset to plug in here)

- Full **closing 1X2 odds** for many matches (so we can de-vig properly), paired with results.
- A complete competition or season, **not** a highlight reel — so it's unbiased.
- Candidate sources (being located by the parallel research pass): football-data.co.uk
  closing columns, FiveThirtyEight's published World Cup forecast CSVs (a beatable baseline),
  and historical odds feeds. Swap that file in where `run_on_seed()` reads, and this same,
  already-validated rig produces the real number a MiroMind forecast must beat.

## How to check this

- `python3 dataset/baseline.py` — re-runs the self-test (math correctness) and rewrites this file.
- The Brier/log-loss definitions and the de-vig are in the script, each with a unit test.
