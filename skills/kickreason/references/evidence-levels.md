# Evidence Levels (the no-faking spine)

Every KickReason output carries an evidence tag and source tiers. This is the same auditability the
reference project (`xhs-market-radar`) enforces with A/B/C grades and source cards — tuned to forecasting.
The rule is inherited by **every** skill: never present a model or a mock as real; grade on calibration.

## Value tags
| Tag | Meaning | Example |
|---|---|---|
| `REAL` | computed from primary data, or directly sourced | Argentina xG **2.49** (StatsBomb); market Brier **0.76** |
| `MODEL` | a labelled model baseline — not the live market | Elo **95%**, FiveThirtyEight **72%** |
| `MOCK` | an illustrative product mock-up | a 2026 prop price; the "answers-back" copy in the demo |

## Source tiers (rate the source AND the claim separately)
| Tier | Source | Example |
|---|---|---|
| T1 — official | the primary record / observer | club injury statement; published team sheet; StatsBomb event |
| T2 — sharp market | the crowd-corrected price | sharpest book's de-vigged closing line |
| T3 — named analyst | a reporter/analyst with a track record | a named beat reporter at the training ground |
| T4 — pundit | opinion, no special access | a TV-panel "they look tired" take |
| T5 — rumor | anonymous / unconfirmed | a single anonymous social post |

**"Confirmed" = independent, not louder.** Ten sites copying one wire story is one source.

## The hard rule
- A `MODEL` or `MOCK` value is never rendered as `REAL`.
- Forecasts are graded on **calibration** (do our 70%s happen ~70%?), never a win/loss tally.
- Show the work: every node carries its sources; "cites every source" requires source-verification, because
  deep-research agents cite the wrong source 20–60% of the time.
