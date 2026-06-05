# 06 — The honest reset

> This **replaces** an earlier draft of mine (`06-scope-freeze-and-3min-video.md`, now deleted)
> that over-reached. That draft "froze" a product scope I was never given — a four-screen
> betting app — and scripted a 3-minute video. Both presuppose things we have **not**
> established. You can't script a demo of MiroMind's reasoning before you know how the MiroMind
> API actually behaves. So this rolls that back and states, plainly, what we know, what we
> don't, and the questions that decide everything.

## The open questions come first — they decide the rest

1. **How does the MiroMind API actually behave on a forecasting question?** Speed, what the
   trace contains, whether the trace is even worth reading. Unknown until we run real questions.
   Everything downstream waits on this.
2. **Can MiroFlow's retrieval be restricted to a date cutoff?** This one build question decides
   whether an *agent backtest* on past matches is even valid (see the constraint below).
3. **Forward-test or backtest?** If retrieval can't be date-controlled, the only honest way to
   claim a MiroMind forecast is to **forward-test on live fixtures** — and the World Cup starts
   ~June 11 (days away), with friendlies live now.
4. **Which problem, which buyer?** Still open, deliberately not guessed.

> A focused research pass on 1–3 (free datasets, baselines, CLV/line-movement data, the leakage
> methodology, and MiroFlow retrieval control) is running now. This file defers the specifics to
> it rather than guessing.

## The constraint that governs everything

**You can't backtest a web-research agent on past matches.** A quant model doesn't know who won
the 2022 final. The MiroMind agent *does* — it's in its weights and one search away. So "forecast
this past match" collapses into "retrieve the result and rationalize a confident number." That's
not ordinary lookahead *bias*; it's lookahead *certainty*. It's the exact reason FutureX and
ForecastBench grade **forward only**, on questions with no known answer at submission.

So the work splits into three honest pieces:

1. **Backtest the rig + market baseline on past data — no agent.** De-vig historical closing odds
   → implied probabilities → Brier/calibration; build and validate the scoring pipeline; establish
   the market baseline a forecast must beat. Past data is perfect for *this* half.
2. **Forward-test the agent on live fixtures — the only clean MiroMind claim.** Lock → wait → grade.
3. **(Optional) Info-controlled agent backtest — only if MiroFlow retrieval can be date-restricted.**

## What this means for the dataset I built

The past-FIFA data in [`../../dataset/`](../../dataset/) is **track 1 only**: the market baseline
and the scoring rig. It is **not** a MiroMind track record and can't become one retrospectively.
The "hero demo" walkthrough is a **mockup**, not evidence. The corrected framing is in the
[dataset README](../../dataset/README.md).

## What we are deliberately NOT doing yet (and why)

- **No video script.** You can't fake a reasoning-demo without the real API behavior. The 60s
  walkthrough waits on a real forward-test trace.
- **No product/app scope.** The "thin four-screen app" was invented and is withdrawn. The unit of
  work right now is the **evaluation** — can MiroMind forecast, measured honestly — not an app.
- **No assumed role for the trace** (product / preview / commentary). Decided after we run it.
