# Deep Research — The North Star (intelligence on the important + debatable questions)

*A plain-language read of the evidence behind a service that does NOT sell the final-result call ("who wins the World Cup?"), but instead (1) surfaces the questions a result actually hinges on, (2) isolates the genuinely contested ones, and (3) serves sourced both-sides expert narrative with a published grade. Smart reader, short on time. Inline [n] citations, Sources list at the end. [UNVERIFIED] flags carried throughout.*

---

## 1. Is the north star sound? (the verdict from evidence)

**Short version: the question-first, debate-first instinct is strongly supported — it is the literal operating doctrine of professional intelligence and forecasting, not a metaphor. The "don't sell the outcome call" instinct is also vindicated by decision theory. But two of the three pillars rest on softer ground than the first, and one core promise ("serve both sides") is an engineering fight against the tool, not a free output.**

### What holds up well

**Professional intelligence really is question-first.** The doctrine is explicit across four independent traditions, each separately verified:

| Tradition | What it says (verified) | Source |
|---|---|---|
| US military (FM 34-2) | A good Priority Intelligence Requirement (1) "asks only one question," (2) focuses on "a specific fact, event, or activity," (3) provides "intelligence required to support a single decision" | [1] |
| CIA Intelligence Cycle | The cycle *begins* with "Planning and Direction"; "Policymakers… initiate requests for intelligence" that drive everything downstream | [2] |
| Corporate competitive intel | Jan Herring's Key Intelligence Topics → Key Intelligence Questions cascade: broad topics decompose into small answerable questions | [3] |
| Cyber threat intel (FIRST.org) | PIRs "must be limited and well-scoped… Less is more"; must answer "the so what… versus simply reporting the news" | [4] |

The strongest academic statement comes from Charles Vandepeer: analysts "need to develop and answer their own questions and assess whether these are the right ones to be asking" [5]. In other words, intelligence failure is often a *question-selection* failure — exactly the north star's first pillar.

**"Don't sell the outcome call" is the Value-of-Information result.** Information is only worth paying for if it could change a decision. The Expected Value of Perfect Information "is always non-negative" and "no other information gathering… can be more valuable" [6]. The corollary: if a deep-research call on "who wins the World Cup?" just echoes the betting market, its added value is ~zero. The doctrine even names the failure mode — FM 34-2 calls "Will the enemy attack?" a "very poor PIR" because it "actually contains four significantly different questions" [1]. "Who wins the World Cup?" is the football version: too big, too compound, already priced.

**The "debatable" filter has a formal home.** A *crux* is "any fact that if [you] believed differently about it, [you] would change [your] conclusion in the overall disagreement"; a *double crux* is "a crux for both parties" [7]. That is the precise definition of "sources disagree / market vs eye-test diverge." And the math agrees on where contestedness peaks: the Brier score's "Uncertainty" term equals p(1−p), maximal at a 50/50 call [8] — a node priced at 92% is "clocklike" and barely worth researching; a node near a coin-flip carries the most information when resolved.

**Demand for the debate (not the result) is proven and large.** ESPN's debate show *First Take* set an all-time annual record in 2025 at 517,000 average viewers; *PTI* averaged 679,000 [9]. A peer-reviewed study of 643,251 tweets across 129 Premier League games found 9.1% of *all* tweets were about VAR (contested-call) incidents, with sharply negative sentiment lasting ~20 minutes [10]. The Columbia Journalism Review's verdict on prediction-market journalism is the single cleanest external validation: markets "price real-life events" but "shouldn't be used as a source of truth"; people come to media to learn *why* the odds sit where they do [11].

### Where it's softer — be honest

- **The doctrine assumes a named decision-maker.** FM 34-2 derives PIRs from "a friendly decision expected to occur" [1]. A bettor, fan, or broadcaster often has *no single crisp decision*. Swapping "tied to a decision" for "tied to the outcome" is a real weakening — outcome-relevance is fuzzier and easier to game [1].
- **Pillar (2) "debatable" needs separate grounding from pillar (1).** Intelligence doctrine cares whether a question is decision-critical, *not* whether it's contested. A PIR can be important and have a clear answer. The "debatable" filter leans on the forecasting/disagreement literature [7][8], not the PIR literature.
- **The third pillar — "serve both cases" — is what the tool fights you on.** The DeepTRACE audit of deep-research agents (GPT-4.5/5, Perplexity, Copilot, Gemini) found they "remain highly one-sided on debate queries," with "citation accuracy ranging from 40–80%" [12]. Serving both sides calibrated is the engineering problem, not a given.
- **"Both sides, structured" buys legibility, not accuracy.** The 50-year intelligence template for this (Analysis of Competing Hypotheses) is widely taught but, per the most rigorous test (~50 analysts), had "no statistically significant effect on confirmation bias" and "may increase judgement inconsistency and error" [13][14]. Sell it as defensible/gradable structure — *not* as a method that makes the call more correct.

**Verdict:** The north star is sound on its first pillar (overwhelmingly), sound on its "don't echo the market" logic (decision theory), real but harder on its "debatable" and "both-sides" pillars, and weakest exactly where it is most differentiated — the published grade (see §6).

---

## 2. The operational definitions (so it's buildable, not a slogan)

### Important question — *detection rule*

A candidate node is **important** only if it passes a four-gate test (the first two gates are the hard ones):

| Gate | Plain rule | Grounding |
|---|---|---|
| **Leverage** | If you flipped the answer, would the parent forecast/decision change materially? Vary it across its plausible range (a "tornado diagram") and measure the swing. Score 0 if the headline is unchanged. | VoI / sensitivity analysis [6][15] |
| **Uncertain** | Is the answer genuinely in doubt now (away from 0/1, ideally near 50/50)? A near-known answer carries ~zero information however big the topic sounds. | Brier "Uncertainty" term [8]; entropy [16] |
| **Resolvable** | Will it have a clean, dated, undisputed answer so the lean can be graded? Tetlock's "Clairvoyance Test": could a clairvoyant "definitively tell you whether your resolution criteria happened?" | Tetlock / Metaculus [17] |
| **Addressable** | Can deep research actually move your view? An irreducible coin-flip (a penalty shootout) is important to the outcome but *not* worth researching. | Rumelt's crux = important AND "something you can actually do something about" [18] |

> **World Cup example.** Bad node: *"Will Brazil win and play well?"* — two questions in one (the direct analogue of doctrine's four-questions-in-one failure [1]). Good node: *"Will Casemiro start the quarter-final given his yellow-card suspension risk?"* — one question, specific actor, a clean dated answer, and it genuinely swings the match model.

**Honest caveat:** combining the four gates into a single multiplied score is *the analyst's construction, not a published VoI formula* [UNVERIFIED as a formula] [15]. Real VoI is an expectation over a payoff model and requires fixing *whose* decision you mean — a node high-leverage for a bettor may be zero-leverage for a broadcaster [6].

### Debatable node — *detection rule*

A node is **debatable** (worth the expensive both-sides treatment) when it clears four gates, in order:

1. **Live** — consensus/market sits ~0.30–0.70, not 0.95/0.05 [8].
2. **Dispersed** — independent credible estimators genuinely disagree (model vs market, panel spread). Ideally the disagreers are each *confident in different directions* (a real contest), not all equally unsure of one number (an "unknown," not a "debate") [19].
3. **Independent & credible** — the disagreement is among multiple sources that formed views independently and clear a liquidity/credibility bar (a thick market, not two traders) [20].
4. **Resolvable & gradeable** — *and* research can move it. Screen OUT "cloud-like," irreducibly random contests — high dispersion there is a *negative* signal of research value [21].

> **World Cup example.** A debatable node: pre-tournament, *"Is England's defence good enough to reach the semi-final?"* where one model leans yes on underlying numbers and the eye-test/press lean no — credible sources confidently split. A *non*-debatable "unknown": *"Who referees the final?"* — uncertain, but not a contest of reasoning.

**Critical caveats:** raw dispersion *over-counts* contestedness — it also captures information asymmetry and forecast bias, not just genuine disagreement [22]. And proving a node is debatable needs *at least two independent estimates*: a lone market price can show liveness (near 0.5) but **not** disagreement. The signal is unavailable from a single source [12][22].

### Expert narrative — *what makes it credible vs a hot take*

Per the trade literature, credible analysis (vs a hot take) comes down to four things: **evidence/data**, **context and not-in-the-heat-of-the-moment timing**, **accountability/transparency** (showing your record), and **balance of reasoning** [23] [PARTIALLY VERIFIED — framework is from trade sources, not peer-reviewed]. The buildable form:

- **Both cases, sourced** — case-for and case-against, each evidence item attached to the side it supports, primary citations named (the Analysis of Competing Hypotheses *structure*) [13].
- **A calibrated lean, never a bare number** — likelihood stated *separately* from confidence (the intelligence-community split) [24].
- **An explicit "what would change our mind."**
- **A published grade after it resolves** — the trust move that converts a take into a payable product (§4) [25].

> **World Cup example.** Not credible: *"England's bottling it again, trust me."* Credible: *"Case for England's defence holding: [StatsBomb xGA, opponent quality]. Case against: [set-piece concessions, full-back injuries]. Lean: 55% they keep ≥1 clean sheet in the knockouts. What flips us: a first-choice centre-back injury. We'll grade this when the QF resolves."*

---

## 3. The whitespace + the demand

### Who serves what today

The market splits into single-function layers. Each is strong at one move and structurally weak at the next [VERIFIED structural framing; the four-gate taxonomy is the analyst's synthesis]:

| Layer | Examples | Picks important Qs? | Isolates debatable? | Both-sides narrative? | Published grade? |
|---|---|---|---|---|---|
| Final-result models | FiveThirtyEight SPI (defunct), Nate Silver's PELE, dratings | No (answers "who wins") | No | No (a number) | **Yes** (Brier, calibration) |
| Raw data | Opta/Stats Perform, StatsBomb | No | No | No ("doesn't come with a manual" [26]) | No |
| Ungraded narrative | The Athletic, Michael Cox tactics, podcasts | **Yes** ("the big questions") | Partly | **Yes** | **No** (no public calibration found) |
| Markets | Polymarket, Betfair, Kalshi | No | The *price* implies it | No ("why" is absent) | **Yes** (reality grades it) |
| Tipsters | Eagle Predict (claims 89.9%), MightyTips | Partly | Partly | Sometimes | **Faked** (cherry-picked) |
| Structured forecasting | Metaculus, Good Judgment Open | **Yes** | Partly | Partly (optional comments) | **Yes** (Brier/Peer) |

**The gap:** *no incumbent does all four — pick the important sub-question, isolate the genuinely contested ones, serve sourced both-sides narrative, AND publish an honest grade after resolution.* The closest threats: Metaculus/Good Judgment Open (have gates 1+4, partial 3, but football is a tiny side category and it's crowd probabilities, not edited essays), and a hypothetical *Athletic + a Brier ledger* (has the narrative, would need the grade) [25][27].

**Two corrections to keep the pitch honest:** the flagship self-grading exemplar, FiveThirtyEight, was *shut down by Disney/ABC in March 2025* — self-grading earned respect but did not save the business [28]. And Nate Silver's PELE keeps independent of *betting* odds for a technical reason, not a branding stance, and *does* ingest Transfermarkt player market values [29] — so "refuses to fold the market in" is overstated.

### Who actually wants intel on the contested questions

Demand for *the argument* is proven and monetized at scale:

- **Subscription analysis works:** The Athletic reached ~5–6M subscribers, was acquired for $550M, and turned its first quarterly profit in Q3 2024 [30][31]. A single analyst + a framework can be a business: Stratechery, ~40,000 paid subscribers at $120/yr [32] (revenue ~$5M is a third-party estimate [UNVERIFIED]).
- **Soccer is a debate-hungry audience right before the demo's tournament:** soccer is "up to 40%" of global sports-podcast listeners [33]; 2026 coverage is led by debate shows (*The Rest Is Football* daily on Netflix; *Football Weekly*) [34].
- **Fantasy "start/sit" is a weekly contested-decision engine** people subscribe for [35].
- **Prediction-market divergence is a ready-made debatable-node detector:** France priced 16.8% (Kalshi) vs 16.0% (Polymarket); "A team priced at 8% on one platform and 9.4% on another is not the same trade" [36].

**How acute / how monetized:** the appetite to *argue* is huge and proven. The appetite to be *held accountable* — the published grade — is the weakest, least-validated pillar (PunditTracker tried grading pundits and did not endure) [37], and demand for serious tactical analysis is real but smaller and slower-to-monetize than mass hot-take content. Two marquee demand numbers in circulation are inflated: 2026 World Cup prediction-market volume is often cited as ~$1.5B, but *realized* winner-contract volume is ~$523M — the larger figures are *forecasts* [36][38]; and the VAR study's "25% of tweets" is a detection *threshold*, not a measured emotional peak [10].

---

## 4. How MiroMind executes it (mechanics + the honest hard part)

### The pipeline (tied to trace channels already captured)

| Step | What happens | Grounding |
|---|---|---|
| **1. Decompose** | One ~4-min MiroMind pass; the planner decomposes the root question into sub-goals. Harvest sub-questions *post-hoc* from the trace (each `search_keywords` cluster and "I need to find out X" thinking span = a candidate node). | Deep-research-agent survey [39]; MiroFlow's own paper confirms "the main agent formulates a detailed execution plan… assigning tasks to sub-agents" [40] |
| **2. Rank important** | Score by *swing*: how much the node's two possible answers move the parent forecast. | "Swing" is the project's mechanic; VoI [6] is the adjacent formal idea |
| **3. Detect debatable** | Three detectors must agree: (a) the trace *hedges without resolving* (a Hedge-to-Verify signal); (b) claim-and-negation retrieval pulls comparably-credible sources, dispersed not peaked; (c) the trace lean *diverges from the de-vigged market*. | SELFDOUBT [41]; "Contradiction to Consensus" [42]; internal eval |
| **4. Both-sides narrative** | Per surviving node: claim-vs-negation retrieval (computational Analysis of Competing Hypotheses), both cases rendered with tiered sources, a calibrated lean, likelihood stated separately from confidence, and "what would change our mind." | ACH [13]; ICD-203 split [24] |
| **5. Grade** | *Before* resolution publish a tight resolution rule per node; *after*, grade the resolvable fact, closing-line value, and calibration across a large pre-registered set. | Metaculus discipline [17]; Brier decomposition [8] |

### The honest hard part: how do you grade a debate without faking resolution?

**Split the uncertainty into two kinds** [43]:

- **Epistemic** (reducible missing knowledge) — this is what a good narrative *reduces*, and it is *gradeable*.
- **Aleatoric** (the match's irreducible coin-flip) — this must be **presented, never fake-resolved**.

A perfectly-reasoned 60% lean on a node that resolves the other way is **not wrong** — outcomes that look "inevitable" in hindsight were not, and a low-probability outcome occurring does not make the forecast bad [44]. So the grade has three separable parts, none of which is "did the single headline call come true":

1. **The resolvable component** — right/wrong on the contested *fact* (did Casemiro actually start?).
2. **Closing-line value** — did the lean move *toward* the market's final price (early-and-right, and leakage-resistant)?
3. **Calibration over many nodes** — Brier decomposed into calibration + discrimination, scored only across a **large, pre-registered** set [8].

**What you can grade:** process, calibration, and the resolvable facts. **What you must present as irreducible:** the genuine coin-flip on the face of every node.

### Named failure modes

- **"Debatable" is a metric → Goodhart-gameable.** You can phrase a near-settled node ambiguously so sources "disagree," or systematically pick easy-to-be-half-right 50/50 nodes [45]. *Mitigation:* pre-register the selection rule; grade calibration over **all** flagged nodes, not a curated subset.
- **Hindsight selection bias.** Choosing *which* calls to showcase after results land makes the scorecard fiction [44]. *Defense:* freeze the timestamped trace and full node set *before* resolution — the discipline, not the code, is load-bearing.
- **Single-event grades are dominated by luck.** One analyst's percentile swung from "top 0.1%" to "~60th" across question sets [46]; single-question scoring perversely rewards lucky overconfidence. The honest grade needs large N and a long horizon — *slow to earn, hard to demo*.
- **Detection signals are noisy.** SELFDOUBT's hedging signal was validated only on QA benchmarks (BBH/GPQA/MMLU-Pro), *not forecasting* [41] — and a forecast trace also hedges for irreducible (aleatoric) reasons. Source-disagreement can be bad retrieval, not real contest: an internal probe found 58/287 sources were the *wrong event* (including a Euro-2025 Women's final mixed into Euro-2024). Bad retrieval masquerades as a debatable node.
- **One pass ≈ consensus, even on sub-questions.** The agent's lean on "does Mbappé start" may just echo the same beat-reporter consensus the market already priced. The value then rests on *selection + legibility*, not a private edge — defensible, but narrower than "we know things the market doesn't."

> **Bleeding-edge-citation risk** [NEW, honest]: three anchor papers (SELFDOUBT [41], Contradiction-to-Consensus [42], MiroFlow [40]) are very recent 2026 preprints — real and on arXiv, but un-peer-reviewed, with author-reported numbers on narrow benchmarks. Treat their effect sizes as directional, not settled.

---

## 5. The FIFA 2026 service, concretely

**The unit is one "debatable-question intel card."** It is *not* an oracle that calls the tournament. One card contains:

| Field | Content |
|---|---|
| **The question** | One specific, dated, resolvable sub-question (passes the §2 importance gates) |
| **Why it's important** | The swing — what in the tournament/match it moves |
| **Why it's debatable** | The divergence (which credible sources split, and how far) |
| **Case for / Case against** | Both sides, each evidence item sourced to primary data |
| **Calibrated lean** | A probability + confidence stated *separately*, in plain words |
| **What would change our mind** | The specific trigger that flips the lean |
| **Resolution rule** | Published *before* the event — tight, "little room for discretion" [17] |
| **Grade (after)** | Resolvable fact ✓/✗, closing-line value, contribution to the running calibration ledger |

### How it would be demonstrated and graded on the real 2022 library

We hold a real 2022 World Cup data library: StatsBomb event + 360 data on all 64 matches, Elo and FiveThirtyEight baselines, hero narratives, and a 224k-tweet traffic layer. That lets us run a **genuine, point-in-time** demonstration:

> **Worked 2022 example.** Pick a node that was *genuinely contested before kickoff* — e.g. pre-quarter-final 2022, *"Will Brazil get past Croatia in 90 minutes?"* Freeze the information state to that timestamp (pre-match Elo/538 probabilities, the press/eye-test split, the market price). Generate the card: case-for (Brazil's attacking numbers, Croatia's age), case-against (Croatia's elite game-management and shootout record), a calibrated lean, and a *pre-committed* resolution rule. Then resolve it against what actually happened (Croatia won on penalties) and grade: the *resolvable facts*, whether the lean had *closing-line value*, and how it contributes to *calibration* across the full set of 2022 nodes. Because the result is known to us but the card is built only from point-in-time inputs, the 224k-tweet layer independently confirms which nodes the *crowd* actually treated as contested in the moment [10].

This is the honest demo: it shows the card *and* the grade, on real data, without claiming we beat the market on the outcome.

---

## 6. Honest risks the research exposed

- **Grading a debate can only ever be partial.** The aleatoric (irreducible) part means a well-reasoned lean that resolves the other way is *not* wrong — yet users and judges will read it as wrong [43][44]. The credibility engine you most need is the one that takes longest to earn.
- **The published grade is the weakest-validated pillar.** Every comparable product (The Athletic, Stratechery, Metaculus, FiveThirtyEight) ultimately *gives the answer*; PunditTracker tried selling graded accountability and didn't endure [37]; and the canonical self-grader, 538, was shut down despite its scorecard [28]. Calibration also *needs volume* (538's was convincing because of thousands of forecasts [25]) — a service of a few deep calls per tournament can be lucky/unlucky and prove little for years.
- **"Debatable" is gameable and over-counts.** Contestedness is a metric (Goodhart) and raw dispersion conflates genuine disagreement with information asymmetry and bias [22][45]. High dispersion can even be a *negative* signal — an irreducible coin-flip research can't crack [21].
- **The tool fights the core promise.** Deep-research agents default to one-sided, overconfident answers on exactly these debate queries (citation accuracy 40–80%) [12]. "Both sides, calibrated" is engineering against the model's grain, not a free output. And the both-sides *structure* (ACH) is not proven to improve accuracy — only legibility [13][14].
- **One pass ≈ consensus.** If MiroMind's lean on a contested sub-node is merely market-consensus quality, the graded *edge* over the market is ~zero — leaving question-selection and narrative quality as the only differentiators, which The Athletic already does well *without an API* [UNVERIFIED for football specifically — no public benchmark of MiroMind on football sub-questions exists].
- **Demand is thinner and softer than the splashiest numbers suggest.** The audience that wants both-sides + grading (forecasting/intel buyers) is smaller and partly served already; the audience that pays most (bettors) wants a pick and an edge, not a calibrated essay; the clearest paid demand (tipsters) is corrupted by affiliate incentives that reward *losing* tips [37][47]; and the marquee creator wins (Goldbridge's Bundesliga rights) are *free-to-air* — proving attention, not direct monetization. Two headline figures often quoted (≈$1.5B market volume; "25% of tweets") were inflated/misread [10][36][38].
- **No structural moat.** Every component is cheap and exists; defensibility rests on execution + grading credibility, and the bundle is assemblable by a credible incumbent (an Athletic + a Brier ledger, or Metaculus turning toward football) [25][27].
- **Decision-anchor weakening.** The PIR doctrine that validates pillar (1) assumes a named decision-maker; substituting "tied to the outcome" for "tied to a decision" is a real, fuzzier weakening for a fan/bettor audience [1].

---

## Sources

1. US Army FM 34-2, Appendix D (Developing Priority Intelligence Requirements) — https://irp.fas.org/doddir/army/fm34-2/Appd.htm
2. CIA, "The Intelligence Cycle" (Factbook on Intelligence, FAS mirror) — https://irp.fas.org/cia/product/facttell/intcycle.htm
3. Jan P. Herring, "Key Intelligence Topics," *Competitive Intelligence Review* 10(2), 1999 — https://onlinelibrary.wiley.com/doi/abs/10.1002/(SICI)1520-6386(199932)10:2%3C4::AID-CIR3%3E3.0.CO;2-C
4. FIRST.org Cyber Threat Intelligence SIG, PIR curriculum — https://www.first.org/global/sigs/cti/curriculum/pir
5. Charles Vandepeer, "Question-Asking in Intelligence Analysis" (ASPJ 2016) — https://www.airuniversity.af.edu/Portals/10/ASPJ_French/journals_E/Volume-07_Issue-4/vandepeer_e.pdf
6. Expected Value of Perfect Information / Value of Information — https://en.wikipedia.org/wiki/Expected_value_of_perfect_information ; https://en.wikipedia.org/wiki/Value_of_information
7. CFAR / LessWrong, Double-Crux — https://www.lesswrong.com/w/double-crux ; https://www.rationality.org/resources/updates/2016/double-crux
8. Brier score (Murphy 1973 decomposition; Uncertainty = p(1−p)) — https://en.wikipedia.org/wiki/Brier_score ; Siegert 2017 QJRMS — https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/qj.2985
9. ESPN Press Room, "ESPN Studio Shows Deliver Records… in 2025" (Jan 2026) — https://espnpressroom.com/us/press-releases/2026/01/espn-studio-shows-deliver-records-multiyear-highs-in-2025/
10. Kolbinger & Knopp, "Video kills the sentiment," *PLOS One* 2020 (e0242728) — https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0242728
11. Columbia Journalism Review interview on prediction markets & journalism — https://www.cjr.org/the-interview/are-prediction-markets-actually-good-for-journalism-kalshi-polymarket-dow-jones-cnn.php
12. DeepTRACE audit, arXiv 2509.04499 — https://arxiv.org/abs/2509.04499
13. Analysis of Competing Hypotheses (Heuer, CIA) — https://en.wikipedia.org/wiki/Analysis_of_competing_hypotheses
14. Dhami et al. 2019, *Applied Cognitive Psychology* 33(6):1080-1090 — https://onlinelibrary.wiley.com/doi/full/10.1002/acp.3550
15. Tornado diagram / one-way sensitivity analysis — https://en.wikipedia.org/wiki/Tornado_diagram ; https://www.treeage.com/tornado-diagram-sensitivity-analysis/
16. "Entropy Application for Forecasting," *Entropy* 2020, 22(6):604 — https://www.mdpi.com/1099-4300/22/6/604
17. Metaculus question-writing guidelines (Clairvoyance Test; "little room for discretion") — https://www.metaculus.com/question-writing/ ; https://www.metaculus.com/question-writing/
18. Richard Rumelt, "The Crux" (BCG Henderson Institute interview) — https://bcghendersoninstitute.com/the-crux-with-richard-rumelt/
19. "Disagreement versus uncertainty: Evidence from distribution forecasts," *J. Banking & Finance* 2016 — https://www.sciencedirect.com/science/article/abs/pii/S0378426615001351
20. Paul C. Tetlock, "Liquidity and Prediction Market Efficiency" (2008) — https://business.columbia.edu/sites/default/files-efs/pubfiles/3098/Tetlock_SSRN_Liquidity_and_Efficiency.pdf
21. Ongaro, "Disagreement-based uncertainty for decision making," *Synthese* 205:211 (2025) — https://link.springer.com/article/10.1007/s11229-025-05039-x ; Tetlock Ten Commandments (Goldilocks zone) — https://goodjudgment.com/philip-tetlocks-10-commandments-of-superforecasting/
22. Diether, Malloy & Scherbina (2002), "Differences of Opinion and the Cross Section of Stock Returns" — https://www.researchgate.net/publication/4913251_Differences_of_Opinion_and_the_Cross_Section_of_Stock_Returns
23. Polymarket credibility cautionary case (NYT/CJR Tow Center) — https://www.cjr.org/tow_center/polymarket-affiliates-are-spreading-misinformation-on-x.php
24. Fox & Ülkümen, "Distinguishing Two Dimensions of Uncertainty" (2011) — https://www.stat.berkeley.edu/~aldous/157/Papers/Fox_Ulkumen.pdf ; ICD 203 likelihood-vs-confidence (project INTEL_DESK.md)
25. FiveThirtyEight, "Checking Our Work" (calibration scorecard) — https://projects.fivethirtyeight.com/checking-our-work/
26. Twenty3, "4 rules for data analytics in football media content" ("doesn't come with a manual") — https://www.twenty3.sport/4-rules-data-analytics-football-media-content/ [URL now 404; quote verified via cache]
27. Metaculus scores FAQ / Good Judgment Open — https://www.metaculus.com/help/scores-faq/ ; https://www.gjopen.com/challenges
28. Poynter / Nieman Lab on FiveThirtyEight shutdown (March 2025) — https://www.poynter.org/commentary/2025/538-disney-abc-layoffs-shut-down-nate-silver/ ; https://www.niemanlab.org/2025/03/fivethirtyeight-is-shutting-down-as-part-of-broader-cuts-at-abc-and-disney/
29. Nate Silver, PELE methodology — https://www.natesilver.net/p/pele-methodology
30. The Athletic (NYT) profitability — https://pressgazette.co.uk/media_business/new-york-times-owned-the-athletic-reports-quarterly-profit-for-first-time/ ; https://www.axios.com/2025/05/20/nyt-athletic-profitable
31. The Athletic — https://en.wikipedia.org/wiki/The_Athletic
32. Stratechery / Ben Thompson — https://blockbuster.thoughtleader.school/p/how-ben-thompson-got-40000-paid-newsletter ; https://en.wikipedia.org/wiki/Ben_Thompson_(analyst)
33. Yahoo Sports, "Podcasting covering the World Cup" (soccer ~40% of sports-podcast listeners) — https://sports.yahoo.com/articles/podcasting-covering-world-cup-110000596.html
34. Netflix Tudum / Hollywood Reporter, *The Rest Is Football* 2026 — https://www.netflix.com/tudum/articles/the-rest-is-football-podcast-release-date-news ; https://www.hollywoodreporter.com/business/business-news/rest-is-football-podcast-netflix-2026-world-cup-1236440841/
35. FantasyPros "Start/Sit" flagship content — https://www.fantasypros.com/content/nfl/start-sit-nfl/
36. Action Network, "Kalshi vs Polymarket odds for the 2026 World Cup" ("not the same trade") — https://www.actionnetwork.com/legal-online-sports-betting/kalshi-vs-polymarket-odds-for-the-2026-world-cup-which-prediction-market-offers-better-value
37. PunditTracker (Ritholtz 2013; WNYC On the Media; Crunchbase) — https://ritholtz.com/2013/02/pundit-tracker/ ; https://www.wnycstudios.org/podcasts/otm/segments/191468-pundit-tracker ; https://www.crunchbase.com/organization/pundittracker
38. DeFi Rate, World Cup prediction-market volume forecast — https://defirate.com/news/forecast-world-cup-prediction-market-volume-could-hit-2-5-billion/
39. "Deep Research Agents: A Systematic Examination And Roadmap," arXiv 2506.18096 — https://arxiv.org/abs/2506.18096
40. "MiroFlow: Towards High-Performance and Robust Open-Source Agent Framework" (MiroMind AI), arXiv 2602.22808 — https://arxiv.org/abs/2602.22808
41. SELFDOUBT (Hedge-to-Verify Ratio), arXiv 2604.06389 — https://arxiv.org/abs/2604.06389 [2026 preprint, un-peer-reviewed]
42. "Contradiction to Consensus" (Biswas & Uzuner), arXiv 2602.18693 — https://arxiv.org/abs/2602.18693 [2026 preprint]
43. Fox & Ülkümen (aleatoric vs epistemic) — see [24]; Hüllermeier & Waegeman, ar5iv 1910.09457 — https://ar5iv.labs.arxiv.org/html/1910.09457
44. LessWrong (Zvi), "Evaluating Predictions in Hindsight" — https://www.lesswrong.com/posts/BthNiWJDagLuf2LN2/evaluating-predictions-in-hindsight
45. Rethink Priorities (Juan Gil, 2021), "Types of specification problems in forecasting" — https://rethinkpriorities.org/publications/types-of-specification-problems-in-forecasting
46. EA Forum (Gregory Lewis, 2020), "Challenges in evaluating forecaster performance" — https://forum.effectivealtruism.org/posts/JsTpuMecjtaG5KHbb/challenges-in-evaluating-forecaster-performance
47. Punter2Pro, "Can betting tipsters be trusted?" (affiliate revenue-share-on-losses) — https://punter2pro.com/can-betting-tipsters-be-trusted/