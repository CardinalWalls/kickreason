# What MiroMind Can Sell for FIFA 2026 — by customer and business model

A plain-language answer for a confused founder. The question is not "what can the API do?" It is "who pays us, how, and for what?" Money first.

One fact to hold onto: **one MiroMind call ≈ a 4-minute research agent that returns the market consensus, sourced and self-graded.** That is a *trust* product, not a *speed* product. Every recommendation below follows from that.

---

## 1. The customer map (one table)

Ranked best to worst for **2026 revenue**.

| # | Customer | Who actually PAYS us | Business model | What MiroMind serves them | Real willingness-to-pay (cited) | Edge or table-stakes | Verdict |
|---|----------|----------------------|----------------|----------------------------|-------------------------------|----------------------|---------|
| 1 | **Engaged football fan** (buys a cheap pass for "smarter than my mates" picks) | The fan, directly (Stripe card) | Consumer pass / sub (freemium funnel) | Published, self-graded match cards: a number + sources + a public accuracy ledger; re-run on late team news | The Athletic $7.99/mo or $71.99/yr, profitable 4 quarters; event pass ~$25-39 [pass price UNVERIFIED] | Table-stakes pick + **one real edge: published self-graded accuracy** | **GO (wedge)** |
| 2 | **Fantasy / DFS / props player** (captaincy + player-prop picks) | The player (cheap pass); later DFS apps via affiliate | Consumer "props & captaincy" pass + graded ledger | One trace per high-conviction prop/captaincy call, graded vs Opta box scores, CLV-tracked | RotoWire $11.99-22.99/mo; SaberSim $97-297/mo (optimizer, not us) | Edge = **soccer coverage gap + reasoning transparency**; grading itself is now table-stakes | **MAYBE (narrow GO)** |
| 3 | **Sports bettor via affiliate** (reads a free pick, clicks to a sportsbook) | The sportsbook (CPA / RevShare) | Programmatic SEO + affiliate | Same graded pick pages, monetized by handoff clicks | CPA $50-200/FTD, up to $300+ at peak; RevShare 20-50% NGR | Edge = published ledger as EEAT/trust; pick itself table-stakes | **NO for 2026** (multi-year asset) |
| 4 | **Pro club / national federation** (opponent dossiers, recruitment memos) | The club/federation, or a consultancy reselling | B2B SaaS / RaaS retainer | Auditable, self-graded dossier or transfer second-opinion | Catapult $26.8k ACV/team; add-on likely $5-10k [UNVERIFIED] | Mostly table-stakes; FIFA+Lenovo give 48 teams this **free** in 2026 | **NO for 2026** (slow, 2027+) |
| 5 | **Sportsbook trading desk / syndicate** (pricing feed / signal) | The desk or syndicate, directly | B2B signal/feed license | One pre-kickoff probability + reasoning | Feeds custom-quoted, "millions" — but all welded to **speed + official data** | Below table-stakes (slow, consensus = zero CLV) | **NO** (API is the wrong shape) |

---

## 2. The two or three that actually work

### A. Engaged fan — consumer pass (the strongest)

- **One sentence:** A football fan pays us a small amount for match cards that show their work and publish their own accuracy.
- **Why they pay:** They already pay The Athletic ($7.99/mo, profitable) for "a voice I trust that shows its reasoning." We sell the same thing for the World Cup: a pick, the sourced *why*, and a public scoreboard of how often we were right.
- **The exact product:** ~104 match cards (plus team-news re-runs), each = a calibrated number + 3-5 cited reasons + a row in a public self-graded accuracy ledger that fills in win/loss + Brier after the whistle. The one move free rivals (Forebet, ESPN, FIFA Play Zone) don't make: **re-run on the confirmed lineup and re-publish before kickoff.**
- **Money math (rough):** ~500k tournament visitors × ~3% convert × ~$30 net ≈ **$450k gross for the event** [conversion UNVERIFIED — we have no audience yet]. Net of ~6-9% effective Stripe load at low price points. COGS is trivial: a few hundred 4-minute calls.
- **Honest risk:** **Cold start.** WTP is real but modest, and we have no audience six months out. The "6M subscribers" Athletic stat was a *free newsletter list*, not paid — and even The Athletic leans on ad revenue we won't have. This is a credibility storefront first, a profit center maybe.

### B. Fantasy / DFS / props — the narrow consumer pass

- **One sentence:** A fantasy/props player pays for hand-picked, graded captaincy and player-prop calls on the World Cup.
- **Why they pay:** People already buy RotoWire ($11.99-22.99/mo) and WC tipster passes. Props resolve cleanly against Opta box scores, so we can *forward-grade* every call — the proof the props market values.
- **The exact product:** A few high-conviction cards per matchday ("Mbappé 2+ shots on target — 62%, market implied 48%"), each with sources, reasoning, a self-grade, and a CLV-tracked ledger. **Soccer is a genuine coverage gap** — the strongest graded-ROI rivals (PropsBot, The Lineup) are US-sports only.
- **Money math:** Same shape as the fan pass; one wrapper, a $39 tournament pass or ~$15-25/mo. DFS affiliate CPA ($50-250/depositor) is real but **gated on referral traffic we won't have — model it as 2027 upside, not 2026 revenue.**
- **Honest risk + kill condition:** One call ≈ market consensus, so "edge" only exists in the post-lineup-news window, and it is **unproven**. **Kill condition:** run a 2-3 week pre-tournament CLV pilot on post-lineup props; if closing-line value isn't positive, sell it as honest graded *research/entertainment*, not "alpha." Do **not** position as a DFS optimizer — the API physically cannot price a full slate.

### Why not affiliate (#3), even though the money looks biggest

The CPA dollars are real ($50-300/FTD at World Cup peak) and the API fits fine. But it dies on **distribution, not the API**: (1) DraftKings/FanDuel reject affiliates who can't already prove traffic; (2) a new domain can't rank for competitive betting keywords in 6 months (needs DA 50+, realistic ceiling is ~30); (3) AI Overviews are shrinking organic clicks (~58-61% CTR drop). Real money, two closed gates, a decaying channel = **~zero 2026 revenue.** Build the ledger now; harvest affiliate in 2027-2029.

---

## 3. The wedge — ship the engaged-fan consumer pass first

**Pick: the engaged-fan consumer pass with a published self-graded accuracy ledger.**

**Why this one:**
- **Reachability:** The fan is the *only* customer where audience = payer. No operator onboarding gate (unlike affiliate), no 9-18-month procurement (unlike clubs), no need for traffic we don't have to *get paid* (unlike DFS affiliate).
- **Willingness-to-pay:** Proven and direct — The Athletic is profitable charging fans for trusted, reasoned sports content.
- **MiroMind fit:** Perfect. The product *is* "a number + its sources + a public self-grade." That is literally what one call returns. Slowness doesn't matter (cards are pre-built); the 6-min news latency is a *strength* (re-run on the lineup, publish before kickoff).
- **Consistent with "not a bet demo":** The hero is published, auditable accuracy — a trust/credibility product. No bet is required to make the first dollar.

**What v1 is (2 sentences):** A free World Cup site of self-graded match cards (number + cited reasons + a public running accuracy ledger that updates after each result), with a paid Tournament Pass (~$30) and re-runs on confirmed lineups before kickoff. The fan pays once, by card, for "the only prediction site that publishes how often it's right."

**What it costs us to run:** One ~4-minute call per published card. The whole tournament is ~104 matches plus team-news re-runs — a few hundred to low-thousands of calls over five weeks. At the 5-requests/sec hard cap that is trivially within budget; the binding constraint is wall-clock per call, which doesn't bite because cards are produced ahead of kickoff, not live. **COGS is effectively a rounding error against any pass revenue.**

**The first revenue dollar's path:** Free card ranks/shares → fan reads it, sees the public accuracy ledger, trusts it → hits the paywall for the full slate + lineup re-runs → pays ~$30 via Stripe → we keep ~91-94% after fees. No sportsbook, no operator approval, no in-running data required.

---

## 4. What we are NOT doing (and why)

- **Affiliate as a 2026 revenue engine — NO.** Operators won't onboard a no-traffic domain, new-domain SEO can't rank in time, and AI Overviews are eating the channel. Build the ledger now; affiliate pays out in the 2027-2029 cycle.
- **DFS optimizer SaaS (SaberSim/PropsBot tier) — NO.** A 4-minute-per-call agent cannot price hundreds of props or build thousands of lineups per slate. The API kills this product specifically.
- **DFS affiliate CPA — MAYBE-later (2027).** Real dollars, but gated entirely on depositing referral traffic we won't have during a 5.5-week tournament.
- **Club / federation B2B — MAYBE-later (2027+).** Real recurring budget (Catapult $26.8k/team), but 9-18-month sales cycles, no official data rights, and FIFA+Lenovo give all 48 teams a free opponent-analysis AI this cycle. Pursue year-round *club recruitment* via a consultancy white-label after 2026 — not as a World Cup launch.
- **Sportsbook trading-desk feed — NO.** The API is the structural opposite of what a desk needs: it's slow (4 min vs 15-30s repricing), consensus-by-default (zero CLV by construction), and has no official-data latency edge. The buyer is also the one entity best able to build it in-house.

---

## 5. The blunt truth about the API as a business input

| API trait | Where it **helps** the business | Where it **hurts** the business |
|-----------|--------------------------------|--------------------------------|
| **~4 min per call (slow)** | Fine for pre-built content pages and pre-kickoff cards; production cost, not serving cost, so COGS stays tiny | Disqualifies anything live/in-running and any per-user real-time agent; kills the trading-desk and optimizer products outright |
| **5 requests/sec hard cap** | A non-issue at our scale — the whole tournament is a few hundred to low-thousands of calls | Can never "cover the book" or price a full DFS slate; rules out high-frequency buyers |
| **~6-min news-update latency** | A genuine **strength** for fan/props cards: re-run on the confirmed lineup and re-publish *before* kickoff — the one move static free rivals can't make | Too slow for in-running markets and forfeits the post-news window to desks that move on official feeds ~8s faster than TV |
| **Consensus-by-default (one call ≈ de-vigged market)** | A trustworthy, sourced consensus is exactly what a *fan* wants — perfect for content | It is **not edge**. The only real edge (post-news, pre-correction CLV) is unproven and must be piloted before we ever sell "alpha." Zero CLV = nothing to sell a sharp desk |
| **Self-grading (local + global verifier)** | **The whole wedge.** We publish auditable accuracy where the industry leaves the page empty — this is reader trust *and* the durable EEAT signal | Useless to buyers who don't value transparency (trading desks want a faster number, not an explanation); and if the live grade is mediocre, transparency cuts against us |

**Bottom line:** The API is a *publish-the-truth* engine, not a *beat-the-market-fast* engine. Point it at the customer who pays for trust — the fan — sell a graded picks ledger as the wedge, and treat the bet itself as one optional downstream domain, never the demo.