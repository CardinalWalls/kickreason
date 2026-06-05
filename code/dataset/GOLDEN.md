# THE STANDARD — the recognized way to grade a forecast, proven on real resolved cases

> Auto-written by `python3 dataset/golden_template.py`. Every number below is
> **computed**, not typed: the script imports the self-tested `brier` from
> `baseline.py`, points it at games whose outcomes are already known, and lets
> the formula deliver the verdict. We did not invent a scoring method — we adopted
> the recognized one and showed it holds.

## The format: FutureX

**FutureX template: a verifiable future event + a probability committed BEFORE kickoff + automatic Brier grading AFTER it resolves.**

FutureX (arXiv:2508.11987) is the recognized benchmark for forecasting agents —
the one MiroMind's agent topped. Its rule is simple and ungameable: the event must
be *verifiable*, the probability must be committed *before* the event, and grading
is *automatic* once it resolves. No hindsight, no opinion.

## The scoring: Brier

```
Brier = (probability_you_gave - what_actually_happened)^2
  0.00 = perfect      0.25 = coin-flip guess      1.00 = confidently wrong
```

The Brier score (Brier, 1950) is a *proper* scoring rule: your expected score is
only minimised by reporting your honest probability, so you cannot game it by
over- or under-stating confidence. Lower is better. We pair it with calibration
(when you say 60%, it should happen ~60% of the time) and CLV (closing-line value:
did you have the price before the market moved?).

## Proof — the market graded by its OWN Brier on resolved games

Closing price on the favourite vs. what actually happened. The formula, not us,
decides who was right.

| Fixture | Favourite | Market said | Result | Brier (computed) | vs 0.25 coin-flip |
|---|---|---|---:|---:|---|
| Saudi Arabia vs Argentina | Argentina | 87% | **favourite LOST (upset)** | 0.759 | **WORSE** |
| Germany vs Japan | Germany | 68% | **favourite LOST (upset)** | 0.458 | **WORSE** |
| Portugal vs Morocco | Portugal | 60% | **favourite LOST (upset)** | 0.360 | **WORSE** |
| Georgia vs Portugal | Portugal | 74% | **favourite LOST (upset)** | 0.543 | **WORSE** |
| Spain vs England (Euro 2024 final) | Spain | 41% | favourite WON | 0.350 | **WORSE** |

**Mean market Brier on these 5 cases: 0.494.** 5 of 5 scored worse than a 0.25 coin-flip.

### The clearest case: Saudi Arabia vs Argentina

- The market priced Argentina at **87.1%** (≈ −675 American, `implied_prob_american(-675)`).
- Argentina **LOST** 2–1. Actual outcome for the favourite = 0.
- `brier(0.871, 0)` = **0.759** — versus 0.25 for a
  coin-flip and 0.00 for a perfect call.
- The formula proves the market was *confidently wrong*. That is a fact the
  arithmetic produced, not an opinion we asserted.

## Honest scope

- This seed (`seed-resolved.json`) is an **upset highlight-reel on purpose**. It
  proves the *formula* discriminates right from wrong calls; it is NOT the market's
  true long-run Brier (on a full unbiased schedule the market scores far better).
- We grade favourite-side prices only; a full 1X2 de-vig needs all three closing
  prices. The `baseline.py` rig already does the de-vig and is unit-tested.

## Our forward call uses this exact template

Our live USMNT call — *will the USMNT advance from Group D?* — is committed at a
probability **before** the group stage and will be graded by the **same Brier**
after it resolves: identical FutureX format, identical formula, no special pleading.
That is the standard. Everything we ship is gradable by it.

## How to check this

- `python3 dataset/golden_template.py` — re-proves the textbook Brier anchors,
  recomputes every row above from `seed-resolved.json`, rewrites this file.
- `python3 dataset/baseline.py` — the self-tested source of `brier` (prints PASS).
- Sources: FutureX arXiv:2508.11987 · Brier (1950), *Monthly Weather Review* 78(1).
  Per-case resolution sources are listed in `seed-resolved.json`.
