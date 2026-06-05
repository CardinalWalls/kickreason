---
name: forecast-grading
description: >-
  Grade forecasts and picks on CALIBRATION (Brier, Closing-Line-Value, reliability curve)
  against resolved results — never a naive win/loss tally, because a 70% call is supposed to
  lose ~30% of the time. Use whenever a prediction needs scoring, a public track record or
  accuracy page, a calibration check, or a comparison against market / Elo / FiveThirtyEight
  baselines over a locked, pre-registered set.
---

# forecast-grading — calibration, not win/loss

Scores forecast nodes with proper scoring rules and publishes the result — the honest accuracy page
KickOracle leaves blank. A single 70% call resolving against you is **not** a miss; grade over a locked,
pre-registered set.

## Procedure
1. **De-vig the closing line** → the fair-probability label to grade against.
2. **Grade the resolvable component + calibration.** Brier (decomposed into calibration + resolution),
   reliability curve, and Closing-Line Value (were we early and right?). Present irreducible (coin-flip)
   uncertainty — never fake-resolve it. See `references/grading-methodology.md`.
3. **Compare to baselines** — Elo and FiveThirtyEight, never a single-call hit/miss verdict.

## Run
```bash
python3 scripts/baseline.py            # self-tested brier() — prints PASS
python3 scripts/golden_template.py     # Brier on resolved 2022 cases (authoritative)
python3 scripts/build_odds_baseline.py # Elo win-expectancy baseline, graded
python3 scripts/build_538_baseline.py  # FiveThirtyEight baseline, graded
python3 scripts/arc_build.py           # the graded arc (Brier over the node set)
```

## Output
A calibration report: Brier, reliability curve, CLV, and the KickReason-vs-market-vs-538-vs-Elo table over
the locked set. (Reference numbers on 2022: 538 favourite-Brier 0.240, Elo 0.291, graded arc 0.262.)

## References
`references/grading-methodology.md` — calibration vs resolution; why win/loss is the wrong scoreboard.
