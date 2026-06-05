# KickOracle research — index

Reverse-engineering of [kickoracle.com](https://kickoracle.com) (an independent, FIFA-unaffiliated AI prediction site for World Cup 2026), done to inform **our** hackathon demo. Researched 2026-06-04.

## What's here
| File | What it is |
|---|---|
| [01-business-teardown.md](01-business-teardown.md) | The full business teardown — what it is, how it makes money, growth engine, moat, risks, clone playbook. |
| [02-programmatic-seo-and-intent-routing.md](02-programmatic-seo-and-intent-routing.md) | **"Teach me"** deep-dive on the thousands-of-long-tail-pages → revenue-routing play. *Genuinely impressive, but NOT our goal.* |
| [03-miromind-fit-and-60s-demo.md](03-miromind-fit-and-60s-demo.md) | **← the point.** Which part of this business MiroMind deep-research (FutureX) can actually power, and the 60-second demo design. |
| [04-futurex-and-the-forecast-that-updates.md](04-futurex-and-the-forecast-that-updates.md) | The two ideas *under* the demo, in plain words: why MiroMind can forecast (FutureX), the "forecast that updates" idea, and where the [`/compiler`](../../compiler/) fits as the **track-record milestone** (later, not day-one). |
| [05-the-professional-standard.md](05-the-professional-standard.md) | **The research gap you flagged** — how sports-intel & betting pros actually think (probability-not-winners, EV, CLV, calibration/Brier), the cited **credibility bar** our forecast must clear, and what it changes for the demo. |
| [06-the-honest-reset.md](06-the-honest-reset.md) | **← read this.** The honest reset: why you can't backtest a web-research agent on past matches (lookahead certainty), the three honest tracks (baseline-on-past / forward-test-agent / info-controlled backtest), and the open questions. Replaces an earlier over-reaching scope/video draft. |
| [99-appendix-raw-research.md](99-appendix-raw-research.md) | Raw, verbatim findings from the 8 research probes — so none of the research is lost. |

**The dataset** these point at lives in [`../../dataset/`](../../dataset/) — past results + odds
(the market baseline / scoring rig), a problem-space map of question types, and a demo mockup. It
is **not** a MiroMind track record (see the dataset README for why).

## The one-paragraph verdict
KickOracle is a clever, near-zero-COGS, time-boxed funnel: programmatic-SEO traffic → free tools + daily-briefing email → a $39.99 pass (plus aspirational $349–$2,390/yr Scout seats and a $5K–$25K API priced as anchors). Its "AI" is a **frozen 5-input formula**, and — critically — it **publishes zero accuracy numbers and names zero humans.** That gap is our opening.

## What it means for us
Most of KickOracle's machine (SEO lattice, affiliate, games, pricing tiers) is scaffolding we don't need. **The only part with real AI value is the prediction + the narrative briefing — and KickOracle fakes it.** That is exactly what a deep-research agent that's good at **FutureX** (forecasting real, resolvable future events) does for real. See [03](03-miromind-fit-and-60s-demo.md).
