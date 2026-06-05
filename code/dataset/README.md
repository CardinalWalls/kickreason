# What this dataset is (the plain version I owed you)

**In one line:** a small pile of *past* World Cup / Euro / Copa matches with their real results
and, where we found them, the pre-match betting odds. That's it. It is **not** a MiroMind track
record, and it can't be one. Here's why, then what it's actually for.

## Why it can't be a MiroMind "track record"

MiroMind is a web-research agent: it already knows who won the 2022 final — it's in its training
data and one search away. So asking it to "forecast" a past match isn't forecasting; it just
looks up the answer and writes a confident number. That's **lookahead certainty**, and it's
exactly why real forecasting benchmarks (FutureX, ForecastBench) only grade matches that
*haven't happened yet*. A real MiroMind track record can only be built **forward**: lock a
forecast before kickoff, wait, grade it. (The World Cup starts ~June 11.)

So anything in here that reads like "MiroMind predicted this" is wrong — see the corrections in
the files below.

## What this dataset is actually for

The honest, useful half — the part you build on past data with **no agent involved**:

- Take each past match's closing odds → strip the bookmaker margin ("de-vig") → that's the
  **market's own probability**.
- Score those against what actually happened (Brier score / calibration) → now you know how good
  the *market* is. That's the number a MiroMind forecast would later have to beat.
- Building it also exercises the scoring pipeline end-to-end, so when real *forward* forecasts
  arrive, the grader already works.

In the three-track plan ([../brainstorm/kickoracle/06-the-honest-reset.md](../brainstorm/kickoracle/06-the-honest-reset.md)),
this is **track 1: the market baseline + the scoring rig.** Nothing more.

## The files, plainly

| File | What it literally is | Honest role |
|---|---|---|
| [seed-resolved.md](seed-resolved.md) · [.json](seed-resolved.json) | 10 past matches: result + (7 of them) pre-match odds + a source | The market baseline + scoring data. **Not** agent forecasts. |
| [questions.md](questions.md) | A list of the kinds of WC questions people bet on, and who'd care | A map of the problem space. Its "where the trace fits" column **guesses at API behavior we don't have yet** — read those as open questions, not answers. |
| [hero-demo.md](hero-demo.md) | A hand-written walkthrough of one past final | A **mockup** for a possible demo. Not a MiroMind output; contaminated by lookahead. **On hold** until a real forward-test. |

## The open questions (these matter more than the files)

1. How does the MiroMind API actually behave on a forecasting question? (unknown until we run it)
2. Can MiroFlow's retrieval be date-restricted? (decides whether an agent backtest is even valid)
3. Forward-test on the live World Cup (clean) vs. an info-controlled backtest (only if #2 works).

A research pass on the data and on #2 is running now.

## How to check this

Open [seed-resolved.json](seed-resolved.json), take any row's result, confirm it against its
source. The odds are "as-sourced" and rough; the scores and dates are firm. **Nothing here is a
MiroMind forecast** — it's the market's history, used to build the baseline a real forecast must beat.
