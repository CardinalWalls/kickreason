# Grading methodology — calibration, not win/loss

The accuracy page is the moat: you can *check* a published score; you can't check a blank page. But it only
works if the score is computed honestly. The core mistake to avoid: a naïve win/loss tally.

## Why win/loss is the wrong scoreboard
A 70% call is **supposed** to lose ~30% of the time. Judging a single locked call by whether the headline
came true rewards lucky overconfidence and punishes honest probabilities. A perfectly-reasoned 60% lean that
resolves the other way is **not wrong**.

## What we grade instead
Three separable parts, over a **locked, pre-registered** set of calls:
1. **The resolvable component** — right/wrong on the contested *fact* (did Casemiro actually start?).
2. **Calibration** — the Brier score decomposed into calibration + resolution; the reliability curve ("when
   we say 70%, it happens ~70%"). Brier = mean of `(p − outcome)²`; 0.25 = a coin-flip; lower is better.
3. **Closing-Line Value** — did the lean move *toward* the market's final de-vigged price (early-and-right,
   leakage-resistant)?

## Two kinds of uncertainty
- **Epistemic** (reducible missing knowledge) — this is what good research *reduces*; it is gradeable.
- **Aleatoric** (the match's irreducible coin-flip, e.g. a penalty shootout) — **present it, never
  fake-resolve it.**

## Failure modes to defend against
- **"Debatable" is Goodhart-gameable** → pre-register the selection rule; grade calibration over **all**
  flagged nodes, not a curated subset.
- **Hindsight selection** → freeze the timestamped trace and full node set *before* resolution.
- **Single-event grades are dominated by luck** → need large N and a long horizon (slow to earn, hard to demo).

## Baselines to beat (2022, verified REAL)
FiveThirtyEight favourite-Brier **0.240** · Elo **0.291** · graded arc **0.262** · coin-flip 0.250 ·
market on the famous upsets 0.494. The de-vigged closing line is the gold-standard probability label.
`scripts/baseline.py` holds the self-tested `brier()`.
