# 05 — The professional standard: how sports-intel & betting pros actually think

> The research gap: KickOracle sells a "prediction," but what does *good* look like to the people who forecast sports for a living? This is the unified mental model + the competence scorecard, so our forecast and track-record clear a knowledgeable person's bar instead of reading as marketing. Cited; claims adversarially verified (24/25 survived 2-of-3 refutation). Read the **Caveats** — several findings lean on a self-interested source.

---

## The headline (one paragraph)

Across **all four** traditions — team-side performance analysts, sharp/quant bettors, bookmaker traders, and Tetlock-style superforecasters — there is **one shared mental model and one shared scorecard.** The mental model: *forecasting is estimating a probability, not picking a winner; you only act when your estimate beats the market's implied (no-vig) probability* — i.e. positive expected value. The scorecard has two pillars: **(1) Closing Line Value (CLV)** — did you beat the efficient closing line? — the gold-standard skill proxy for bettors; and **(2) the difficulty-adjusted Brier score** (a proper scoring rule = calibration + resolution), graded *only after events resolve*, the standard for forecasters. The most important practical fact for us: **CLV reaches statistical significance in ~50 predictions, vs thousands for win-rate** — so it's the *only* honest skill signal that works in a small sample.

---

## 1. The shared mental model — "probability, not winners"

The single primitive every tradition converges on: **translate a judgment into a fine-grained numeric probability, and act only on edge over a reference price.**

- **Tetlock, 6th commandment:** "you have an advantage if you are better than your competitors at separating 60/40 bets from 40/60 — or 55/45 from 45/55." Granularity matters empirically: forecasters who distinguish 70/71/72% beat those who round to "likely." [[GJ]]
- **Buchdahl (sharp-betting authority):** "Holding expected value, not picking winners, is the holy grail for all serious sports bettors." [[POD]]
- Two independent fields (forecasting science, professional betting) arrive at the *same* primitive: a calibrated number + act only on +EV. Picking a winner is amateur framing; **estimating P and comparing it to a price** is the professional one.

**EV, concretely:** edge = your estimated probability − the market's *no-vig* implied probability. You bet (or "have signal") only when that's positive. Implied probability from decimal odds = `1/odds`; the book's prices sum to >100% (the "overround"/vig, ~4.5% at a sharp book), so you must **de-vig** before comparing or your edge is overstated.

## 2. The benchmark — the closing line is the scoreboard

- The **closing line** (price just before kickoff), especially at a sharp, high-limit book (Pinnacle), is "often considered the most accurate representation of a game's true odds" — it has absorbed sharp money and all available information. [[PIN-EMH]]
- Empirically it's *brutally* efficient: across ~398k football games, closing-line implied probabilities track observed outcomes at **r² ≈ 0.997.** [verifier corroboration]
- Mechanism → why timing matters: "As more bets are placed, especially by sharp bettors, sportsbooks adjust their lines… leading to the closing line." So **mispricing edge decays toward kickoff** — early prices are softer (less information), the close is hard. This is the betting analog of "news moves the line."
- Implication for us: **you don't claim to be smarter than the world; you measure yourself against the closing line.** That's the field's agreed yardstick.

## 3. The scorecard, pillar 1 — Closing Line Value (CLV)

- **Definition:** did the price you took beat the closing price? Bet an NFL spread at −2.5 that closes −3.5 → positive CLV. [[PIN-CLV]]
- **Formula (Buchdahl):** `CLV = your decimal odds ÷ closing decimal odds`, using the **no-vig (fair) closing odds** as denominator (de-vig first, or CLV is inflated ~by the margin). [[POD]]
- **Why pros judge by CLV, not win-rate:** CLV's per-bet standard deviation (~0.1) is roughly **10× tighter** than even-money P&L SD (~1.0). So skill shows up in "**perhaps as few as just 50**" bets, vs "**several thousand**" for win/loss to clear the noise. Validation: a ~20,000-bet system showed 3.4% actual profit vs 4.0% expected EV — CLV predicted profitability. [[POD]]
- **It's the anti-tipster test:** CLV is a *statistical* skill signal an outsider can verify, not a flattering W-L log you can cherry-pick.
- **Caveats:** CLV proxies EV only in *liquid* markets; it can be self-generated if your own bets move the line; and a single +CLV bet still loses often (it measures decision quality, not the one result).

## 4. The scorecard, pillar 2 — proper scoring, graded after the fact

- Forecasting science defines competence as **calibration AND resolution together** (Tetlock, 7th commandment: "long-term accuracy requires getting good scores on both"). Calibration = when you say 60% it happens ~60% of the time; resolution/discrimination = you push probabilities away from the base rate when you actually know more.
- Scored with **proper scoring rules** — **Brier score** (Brier 1950; strictly proper; decomposes into calibration + resolution + uncertainty) or **log loss**. Good Judgment's superforecasters sit around **Brier ≈ 0.20–0.25.**
- **Graded only after resolution.** [[FB]] **ForecastBench** (ICLR 2025) is "comprised solely of questions about future events that have no known answer at the time of submission"; models appear on the leaderboard "**50 days after** forecast submission" to allow resolution; performance is "scored using the **difficulty-adjusted Brier score**." This is the academic mirror of CLV — and the direct standard our results-graded product should adopt.

> **Two pillars, same spirit:** CLV (betting) and post-resolution Brier (forecasting) both reward *being calibrated and beating a benchmark over a sample*, and both are designed to be **un-fakeable** — exactly the opposite of a cherry-picked win streak.

## 5. The modeling stack (convergent, well-documented)

What the pros actually compute. We don't need to match this for a demo, but it's the credible vocabulary:

- **Dixon–Coles (1997)** — the foundational scoreline model: team-specific **attack/defence** parameters + **home advantage** in a Poisson framework, plus a **ρ correction** that fixes the four low-scoring lines (0-0, 1-0, 0-1, 1-1) the independent-Poisson underrates. Built explicitly "to exploit potential inefficiencies in the association football betting market," and reported a positive return on 1995–96 odds *(in-sample, single season — see caveats).* [[DC]]
- **FiveThirtyEight SPI** (representative production system): each team gets goal-scale **offensive/defensive ratings** from four directly-comparable metrics (goals, adjusted goals, shot xG, non-shot xG) → a **Poisson match model** with home-field + **days-of-rest** parameters → **10,000-run "hot" Monte Carlo** season simulations (ratings drift within the sim, widening the distribution). [[538]]
- **Expected Goals (xG)** — the analyst workhorse: each shot gets a **0-to-1** probability of becoming a goal from historical similar shots (features: distance, angle, body part, assist type; advanced models add freeze-frame defender/keeper positions). [[HUDL]] **Refuted overreach:** xG is *not* "the most accurate predictor of future performance" (killed 0-3) — it's shooter-blind and ignores non-shot threat.
- Team-strength can equally be **market-implied** (de-vig the odds) — and since the market is ~efficient, that's a strong baseline a model has to beat.

## 6. Sharp vs square — credible vs charlatan

- **Charlatan pattern (the tipster scam):** sells picks, advertises a **win record** → survivorship bias (failed tipsters vanish), cherry-picking, no benchmark, no sample-size honesty.
- **Credible pattern (quant/EV):** measures **CLV and Brier/calibration over large samples**, benchmarks against the closing line, frames everything as EV. "Verify by statistics," not by anecdote.
- The separator is *structural*, and it's the whole point for us: KickOracle's "#1, 90/100 chemistry, trust our frozen formula" is closer to the tipster aesthetic; the move that flips us to the credible side is **showing CLV/Brier against a benchmark over an honest sample.**

---

## 7. THE CREDIBILITY BAR — what our product must clear

Distilled from the verified takeaway. This is the checklist a knowledgeable viewer will (consciously or not) run against our demo.

### MUST satisfy
1. **Lock before kickoff, grade after resolution.** No-known-answer-at-submission, results-graded — the ForecastBench/Good Judgment standard. *(We already do this — 03 track-record + the [`/compiler`](../../compiler/).)*
2. **Frame edge as EV vs the market.** Show our probability *next to the market's no-vig implied probability* — "ARG 48% vs market 44% → +4% edge," not a bare "ARG 48%."
3. **Benchmark against the closing line / show CLV.** The field's agreed yardstick and the **fastest-converging, hardest-to-fake** skill signal (~50 predictions). For a short demo this is the *only* honest skill claim available.
4. **Honest sample sizes + a calibration view.** Short-sample win rates are explicitly *not* credible. Either feature CLV (small-sample valid) or label any Brier as "illustrative, small N," and show a reliability/calibration view, not just a hit count.
5. **Frequent small, sourced updates.** Tetlock's "frequent small updates" + the edge-decays-toward-kickoff dynamic = our "forecast that updates as news arrives, with a reason + source." *(This is exactly [04](04-futurex-and-the-forecast-that-updates.md).)*

### OUT OF SCOPE for a demo (don't fake these)
- Real-money **bankroll / Kelly / fractional-Kelly** staking and risk-of-ruin tooling.
- Operating as a **market maker / originating lines.**
- Guaranteeing efficiency or edge in **illiquid markets** (obscure tennis, UFC prelims).
- **Claiming profit-after-vig.** Even Dixon-Coles/SPI aren't shown to be profitable out-of-sample after costs (open question). We claim *calibration + CLV as a skill signal*, **not** "we beat the bookies for money."

---

## 8. What this changes for our demo (map to 03 / 04)

**Where we're already aligned (and didn't realize how well):**
- **Lock-before-kickoff + grade-after** ([03](03-miromind-fit-and-60s-demo.md) track record, [04](04-futurex-and-the-forecast-that-updates.md) compiler) = *literally* the ForecastBench standard. Our instinct was correct, and now it has a citation.
- **"Forecast that updates with sourced reasons"** ([04](04-futurex-and-the-forecast-that-updates.md)) = Tetlock's frequent-small-updates + market's news-decay. Also correct.

**The one upgrade that matters most — reframe the flex around the market:**
- 03 currently sells "we were right / we show our work." The *sharper, more credible* flex is: **"we post a calibrated probability framed as edge vs the market's price, lock it before the close, and our skill signal is CLV — beating the efficient closing line — which is real in ~50 picks, not a cherry-picked streak."**
- Concretely: add a **market-implied probability** (de-vigged public odds) beside our forecast, and make the track-record metric **CLV first, Brier/calibration second.** This is the single biggest credibility jump available, and it *fits a hackathon* because CLV converges fast — Brier over 5 World Cup matches would be meaningless; CLV over ~50 locked picks is not.

**The honesty that becomes our moat:** because the closing line is ~efficient (r²≈0.997), *consistently* beating it is hard — so we show the **mechanism** (lock → compare to close → compute CLV) and let modest, real numbers stand. That honesty is precisely what KickOracle's empty `/accuracy` page can't show.

---

## Caveats (read these)
- **Source bias:** the CLV / market-efficiency findings lean on **Pinnacle's own educational content** (a sharp book with mild self-interest in branding its line as *the* benchmark) and on Buchdahl via Pinnacle's promotional blog. Mitigated by independent corroboration (VSiN, academic market-efficiency studies, Brier/ForecastBench primaries), but not neutral primaries.
- **Link rot:** FiveThirtyEight shut down (~2023); SPI methodology verified via cached snapshots (substance high-confidence, verbatim medium). Several Pinnacle/Wiley/GJ URLs 403'd and were verified via mirrors.
- **Not a profit claim:** the model findings describe *what the methods are and what their authors reported*; none independently establishes out-of-sample profitability after vig/costs.
- **xG overreach** ("most accurate predictor") was explicitly refuted 0-3 — don't claim it.

## Open questions (worth deciding before building the track record)
1. **What sample size** do we commit to publicly before publishing a Brier/calibration claim, over what rolling window, to avoid looking like cherry-picking?
2. **How exactly do we compute/display CLV** — which closing line is the reference, and how do we de-vig (no-vig closing odds is the technically correct denominator)?
3. **What's the real info-edge decay curve** before kickoff (how much probability mass moves, how fast, after injuries/confirmed lineups)? Drives the "forecast that updates" feature.
4. **Does any DC/SPI-style edge survive in 2026 markets** after vig — i.e., what edge can a demo *honestly* claim vs the closing line? (Likely: little. So sell calibration + CLV-mechanism, not profit.)

## Sources
- [[GJ]] Good Judgment — Tetlock's 10 Commandments of Superforecasting · goodjudgment.com *(primary)*
- [[POD]] Buchdahl, "CLV Demystified" · pinnacleoddsdropper.com *(secondary; promotional)*
- [[PIN-CLV]] Pinnacle — "What is Closing Line Value" · pinnacle.com *(primary; self-interested)*
- [[PIN-EMH]] Pinnacle — "Efficient Market Hypothesis in sports betting" · pinnacle.com *(primary; self-interested)*
- [[FB]] ForecastBench leaderboard + paper (ICLR 2025) · forecastbench.org *(primary)*
- [[DC]] Dixon & Coles 1997, *JRSS C* 46(2):265–280 · doi:10.1111/1467-9876.00065 *(primary)*
- [[538]] "How Our Club Soccer Projections Work" · fivethirtyeight.com *(primary; archived)*
- [[HUDL]] "Expected Goals (xG) Explained" · hudl.com *(primary)*
- Supporting: VSiN (CLV), Brier score (Wikipedia), Kelly criterion (Wikipedia), Stats Perform/Opta, RebelBetting (tipster scams), godsofodds (Pinnacle closing accuracy).
