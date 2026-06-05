# The questions that make money (a problem-space map)

> **Caveat up front:** the "where a MiroMind trace fits" column (product / preview / commentary)
> **guesses at how the MiroMind API behaves** — which we don't actually know yet. Treat that
> column as open questions, not commitments. This file is a map of what people bet on and who'd
> care, not a product spec. See [README](README.md).

This is the catalog. Real, money-bearing World Cup 2026 prediction questions, sorted by **who is asking** — because the same match throws off three different questions depending on whether a fan, a sharp, or a data buyer is paying.

Every question below is **concrete and resolvable**: it has a single right answer once the match is played, settled against an official source. For each one we also say the part that matters to our business — **where a MiroMind reasoning trace fits**:

- **product** — the trace *is* what they buy (the audited reasoning chain is the deliverable).
- **preview** — a short teaser of the reasoning ("watch it think") that pulls them toward the paid thing.
- **commentary** — the trace is raw material distilled into a readable "why we picked X" explainer wrapped around a number.

> The trace is slow (a verified run hit 9+ minutes, 77 searches, ~15.6k thinking steps and still timed out at a 560s cap — the "逻辑长征"). So the raw firehose is almost never the product. It is the evidence behind a fast page. (Source: live API run, 2026-06-04; see [the trace-as-product trade-off](#what-we-are-not-claiming).)

---

## Segment 1 — FAN

**Standard of intel:** plausibility plus a story. A fan does not demand a verified track record or a calibrated probability — they want *a number to argue with* and a one-line reason they can repeat. Willingness to pay is near-zero; the money is in volume, ad/affiliate, and the free→paid funnel. The trace they value is a one-line "why" plus about three factors and a shareable headline — never the full 15k-step chain.

| Question (concrete, resolvable) | Who pays & how it makes money | Data needed | Resolves on (source of truth) | Trace fit |
|---|---|---|---|---|
| Who wins the World Cup? (e.g. Spain to lift the trophy) | Free reader, monetised by affiliate/futures sign-ups; the single most-bet futures market | Title odds (Spain/France co-favourites ~+450–+500, England ~+650), form, draw path | Official FIFA result of the **July 19 2026 final at MetLife Stadium** | **commentary** — they want a confident headline + 3 reasons, not the chain; distil the trace into a one-screen "why Spain" |
| Will the USA get out of their group? | Free reader; "my country" sentiment money drives sign-ups — a deep USMNT run is the upside case behind the ~$4.4B *top end* of EKG's $2.3–4.3B handle projection | Group draw, opponents, form; 48-team format sends top 2 + 8 best 3rd-placed (32 of 48) through | Official FIFA group standings (points, then goal difference, goals for, head-to-head) | **commentary** — a shareable yes/no + a few factors; trace is the source, not the page |
| Does [my country] win their opener? (1X2 / match result) | Free reader; one of the highest-volume single-match markets, biggest on a host's group-stage opener | Lineups, injuries, recent results | Official FIFA **90-minute** result (knockout extra-time handling varies by book) | **commentary** — one-line "why home win" with 3 factors *(the 2026 group draw / exact opener matchups are not confirmed in our sources — don't name a fixture until the draw is verified)* |
| Does Mbappé win the Golden Boot? | Free reader; star-name futures market, popular pre-tournament | Golden Boot odds (Mbappé ~+600, Kane ~+700, Haaland ~+1400), penalties, expected run depth | Official FIFA top scorer: most goals (no shootout goals); tiebreak assists → fewer minutes → shared | **commentary** — name-led story; trace explains why his team's run + penalties matter |
| Over or under 2.5 goals in this match? | Free reader; a top-3 single-game market, loved by people who won't pick a side | Team scoring/conceding rates, stage (cagey knockouts) | Official FIFA total goals in regulation (extra time/penalties excluded unless stated) | **preview** — "watch it pull both teams' scoring rates" is a clean 60-second teaser |
| Build me a bracket / fill the Round of 32 | Free reader; bracket pools are the highest-engagement social product (pool participation at multi-year highs) | Group projections, seedings, the new Round-of-32 path | Official FIFA bracket as matches resolve | **preview** — a fast "watch it reason through one group" hook into a paid full bracket |

> For the fan, the trace is mostly **invisible**: it does the homework, the page shows a number and three reasons. The only place a fan *sees* the trace is the **preview** — the "watch the AI think" hook.

---

## Segment 2 — EXPERT / SEMI-PRO

**Standard of intel:** Closing Line Value (CLV — your odds versus the closing line at a sharp book like Pinnacle). Two different sample-size facts get conflated, so keep them separate: (1) CLV is the *fast* skill signal — it reaches significance in roughly **~50 picks** (per [05](../brainstorm/kickoracle/05-the-professional-standard.md)) because it grades decision quality, not lucky outcomes; (2) the **~500+ bets over 6+ months, losses included** figure is the *expert's verification demand on a published win/loss record* — what they need to see before they trust a raw hit-rate. We lead with CLV precisely because the win-rate sample takes far longer. This crowd wants the *full sourced chain*, a per-pick grade against the closing line, and an export they can audit. Medium willingness to pay (~$20–200/mo). This is the segment the MiroMind self-grading trace is sized for: losses shown, pick frozen before kickoff, every pick graded.

| Question (concrete, resolvable) | Who pays & how it makes money | Data needed | Resolves on (source of truth) | Trace fit |
|---|---|---|---|---|
| Is [player] anytime goalscorer +EV vs the line? | $20–200/mo subscriber; THE most popular prop and the core same-game-parlay leg — heavy public name-bias inflates star prices | Player role/minutes, matchup, set-piece & penalty duty, line vs sharp price | Operator's **Opta/Stats-Perform-style** stat feed; data source *varies by book* (a real settlement risk) | **product** — the audited "why we think the line is wrong" chain *is* the edge they pay for |
| Does [team] win its group at this price? | Subscriber; "better prices than outright," shaped by draw, goal difference, and path — softer than the headline winner market | Group draw, projected paths, goal-difference scenarios, 3rd-place wildcard math | Official FIFA final group standings | **product** — the sourced reasoning + CLV grade is the deliverable |
| Alt-line / correct-score value on this match? | Subscriber; high-overround, low-liquidity markets with soft tail pricing = the most realistic edge | Score-distribution model, team styles, stage scoring patterns | Official FIFA regulation final score | **product** — they're buying the model's reasoning behind a contrarian tail price |
| Will [team] advance from the group (to-qualify)? | Subscriber; lower-tier group games carry stale, less-efficient lines | Schedule, rest, motivation, third-place tiebreak scenarios | Official FIFA group standings (advancement) | **product** — full chain + per-pick grade |
| Shots-on-target / cards / assists prop edge? | Prop specialist; thin per-leg liquidity, stale numbers — the segment's best hunting ground | Player tendencies, referee profile, matchup, line shopping | Operator/Opta-style stat feed (resolution source varies by book) | **product** — the auditable reasoning is the whole value; thin markets reward homework |
| Did our locked pick beat the closing line? (CLV scorecard) | Subscriber; CLV is the gold-standard skill metric — this *is* the retention product | Our timestamped pick odds vs the closing line at a sharp book | Closing line (e.g. Pinnacle) + the official match result | **product** — the **self-grading record** (pick frozen pre-kickoff, losses included) is the trace's home turf |

> For the expert, the trace is the **product**: a source-cited chain plus a permanent, exportable, loss-included graded ledger. This is exactly the verifiable track record a fake-it competitor cannot honestly produce.

---

## Segment 3 — INSTITUTION / DATA BUYER

**Standard of intel:** independently auditable *methodology and provenance* — not per-match prose. The governing principle is "if it's not documented, it didn't happen." The benchmark is the regulated/audited world (e.g. accredited data feeds and manipulation-resistant settlement indices) — *though the specific accreditation/settlement examples a pitch might cite (IBIA/eCOGRA for Opta, CF Benchmarks for Kalshi) are **not yet verified in our research and need a source before use**.* High willingness to pay, low volume — a B2B feed/API where the **self-grading audit chain is the licensed product itself**. (The specific B2B price tier is a positioning assumption, not a verified figure — see the not-claiming box.)

| Question (concrete, resolvable) | Who pays & how it makes money | Data needed | Resolves on (source of truth) | Trace fit |
|---|---|---|---|---|
| A calibrated win probability per team, diffable against closing odds | Media/app/book buyer; licensed probability feed | Model probabilities + closing market odds, time-stamped | Official FIFA results, scored after each match | **product** — the documented, auditable methodology + probability *is* the feed |
| A graded, source-cited reasoning trace per published pick (audit trail) | Compliance-sensitive buyer; the audit trail is the deliverable | The full typed trace (thinking → web_search → fetch → verified answer) + outcome | Official FIFA result attached as the automatic label | **product** — the raw audited chain is precisely what this buyer licenses |
| How is each market scored? (methodology documentation) | Institutional buyer; "undocumented methodology is not defensible" | Per-question grading rules (0-1 accuracy, F1, ranking partial-credit, volatility-adjusted numeric) | The documented scoring spec, mirrored on FutureX's metric definitions | **commentary** — a written methodology doc *around* the traces, not a single number |
| Where did each settled outcome come from? (provenance) | Data/integrity buyer; provenance is the value | Resolution source per market (FIFA result/standings; operator stat feed for props) | Named official source per market, recorded at settlement | **product** — the trace's visible source URLs are the provenance record |
| A pipeline of verified prediction trajectories + auto-labels (flywheel feed) | Research/training partner; trajectories + ground-truth labels are training/eval data | Full trajectories (≈ MiroVerse shape: trace + verified answer) + match outcome | Match scoreboard = a **free, automatic ground-truth label** | **product** — the trace + auto-label is literally the asset; note trace data is CC-BY-NC-4.0, commercial use needs a license, so this is a **partnership**, not silent monetisation |

> For the institution, the trace is the **product and the audit trail at once** — and a self-resolving one, because a match's outcome annotates the trajectory for free. That is the honest core of the "flywheel" story.

---

## What we are NOT claiming {#what-we-are-not-claiming}

> **Read this before quoting any number above.**

- **Not claiming profit after the book's cut (vig).** "Edge" here means a line looks mispriced relative to our reasoning — not a guaranteed return after the operator's hold. Same-game parlays in particular carry a ~20–35%+ hold versus ~5% on straight bets; they are high-revenue for books and low-edge for bettors.
- **Not claiming the headline markets are beatable.** The outright winner and the big prediction-market contracts are near-efficient (near-zero vig at the top). *(One volume figure floating around — Polymarket's winner event at ~$1.58B — is marked **uncertain** in our research: it's a raw event total from one snapshot and conflicts with smaller aggregated figures; don't quote a single volume number without a fresh, timestamped pull.)* Realistic edge lives in **thin, stale markets** — niche player props, lower-tier group games, alt-lines, correct score — which are also the messiest to resolve.
- **Not claiming we have a real CLV example yet.** The whole expert pitch leans on Closing Line Value, but **no row in our dataset carries an actual our-odds-vs-closing-line CLV number.** The seed-resolved events show "the market priced the eventual winner at X% and a locked pick disagreed and won" — a *favourite-vs-market* story, not a logged CLV. Producing one real, labelled CLV example (our timestamped pick price vs the sharp closing line) is open next-work, not done.
- **Not claiming clean auto-resolution everywhere.** Match results, standings, and the winner resolve cleanly on official FIFA data. **Player props do not**: settlement depends on the operator's stat provider, which varies by book — a genuine resolution risk, not a solved problem. Golden Boot betting rules (dead-heat) may also differ from FIFA's award rules.
- **Not claiming the raw trace is the consumer product.** It is multi-minute and sprawling; it cannot be streamed live in a demo. It is the evidence backbone (product for experts/institutions, commentary fuel for fans), not a firehose we hand a casual buyer.
- **Not claiming a particular B2B price, a finished track record, or that MiroMind already accepts our traces.** The institutional price tier is a positioning assumption; the flywheel contribution path needs a license conversation (service@miromind.ai); MiroMind's #1 FutureX ranking was late-2025/early-2026 and is **not** current as of mid-2026.

## How to check this

Every market, price, format fact, and resolution rule above traces to the project knowledge base, which carries primary sources for each claim. To verify a row: (1) the **market type and resolution source** come from the betting-market and resolution facts (Polymarket/Kalshi pages, FIFA rules, BetMGM/Covers/FOX guides, Opta/Stats Perform); (2) the **odds and tournament facts** (co-favourites, format, dates) come from the tournament facts (FOX Sports, FanDuel, Wikipedia, FIFA); (3) the **trace behaviour and grading metrics** come from the live MiroMind API run (2026-06-04) and the FutureX paper (arXiv 2508.11987). Anything we could not source is flagged in the box above rather than asserted.
