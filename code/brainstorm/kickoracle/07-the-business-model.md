# 07 · The business model — solid first (the spine of the whole video)

> This is **our** business, not a teardown of KickOracle (that's [01](01-business-teardown.md)).
> It is written **first and made solid** because everything else — the 60s demo, the intro,
> the full video — is just *showing* this model working. Built on the rich, graded FIFA-2022
> data (`dataset/arc_2022.graded.json`). Anchored on the cases that are at once the most
> **权威 / authoritative** (real odds, real sources, a computed grade) and the most
> **值得回忆 / memorable** (the moments a billion people remember).

---

## 1. The one line

**We sell the World Cup as one living, graded forecast graph** — every match, team, player and
moment is a node; each node is seen through **four professional layers**; and *every layer carries
a real source and, where it's a probability, a real grade.* One deep-research trace produces all
four. The competitor sells a confident number with no "why" and no scorecard. We sell a forecast
you can **audit and then check.**

## 2. The product (what actually ships)

```
                 ONE MiroMind deep-research trace per node
                                  │
                      the COMPILER extracts (the IP)
                                  │
        ┌───────────────┬─────────────────┬────────────────┬───────────────┐
        ▼               ▼                 ▼                ▼
   MAGIC-MOMENT      NARRATIVE          ODDS             STATS
   the star /        the WHY /          calibrated       the hard data
   the drama         the storyline      probability      (xG, shots, set-pieces)
        │               │                 │   + a GRADE     │
        ▼               ▼                 ▼  (Brier/CLV)     ▼
   fans · social    media · creators   bettors · quants  clubs · analysts
   broadcasters     engaged fans       sportsbooks       B2B / data
```

Four industries that today are four separate companies — **produced from one trace, sourced,
graded, and consistent with each other.** That is the product. The compiler that turns a raw
research trace into this maintained, graded graph is the defensible asset (`compiler/`,
`dataset/node_extract.py`, `node_eval.py`, `arc_build.py`).

## 3. The moat (three layers, in order of defensibility)

1. **A verified track record — the one thing the category fakes.** For a product whose entire
   value is *being right*, KickOracle publishes **zero** accuracy: no Brier, no hit rate, no ROI,
   no named humans (see [01 §4](01-business-teardown.md)). We lock a sourced forecast **before**
   kickoff and grade it after with the recognized rig (Brier — a proper, un-gameable scoring rule;
   CLV vs the closing line). This is the same FutureX capability MiroMind's agent **tops**, pointed
   at football. *Proof, not a methodology paragraph.*
2. **Four products from one trace.** Anyone can scrape a score. The moat is that one expensive
   research pass yields four sellable layers at once, each tied to a different buyer — so the unit
   cost of the trace is amortised four ways.
3. **The flywheel.** MiroMind is a prediction company; **MiroVerse holds essentially zero sports
   data** (the gap). Every graded trajectory we emit — a real human-stakes forecast with a
   ground-truth label the scoreboard provides for free — is exactly the training data that gap
   needs. The maintained graph isn't just the product; it's a data asset that compounds.

## 4. The four layers = four revenue lines = four buyers

| Layer | The professional system behind it | Buyer | How it's sold | Graded? |
|---|---|---|---|---|
| **magic_moment** | broadcast / highlights / the star | fans · social · broadcasters | B2C passes, engagement, clip/broadcast licensing | — |
| **narrative** | the commentator / analyst / reporter | media · creators · engaged fans | content + the daily briefing (retention loop) | sourced |
| **odds** | the prediction system (bookmaker de-vig · Opta · markets) | bettors · quants · sportsbooks | the high-value line; the auditable accuracy page | **Brier / CLV** |
| **stats** | the data co (Opta · StatsBomb · FBref) | clubs · analysts · B2B | the REST data feed (enterprise) | sourced |

The competitor already proved willingness-to-pay across these tiers ($3.99–$39.99 fan passes →
$349–$2,390/yr analyst seats → $5K–$25K/mo API; [01 §2](01-business-teardown.md)). We don't need
to re-prove the *pricing* — we need to win the one axis they can't: **published, verified accuracy.**

## 5. The proof — authoritative **and** memorable (the 2022 graded arc)

The pitch isn't "the market is dumb." It's sharper and true: **the market is right on the chalk and
confidently wrong on exactly the moments you remember forever — and our compiler grades both, with
receipts.** The 2022 arc (`dataset/arc_2022.graded.json`, graded by `arc_build.py`) is the evidence.

The hero exhibits — each one is simultaneously 权威 (a real pre-match price + sources + a *computed*
Brier) and 值得回忆 (iconic):

| Moment | The market said | What happened | The grade (computed) |
|---|---|---|---|
| **Saudi Arabia 2–1 Argentina** (Al-Dawsari's 53' curler) | Argentina **87.1%** | favourite **LOST** | **Brier 0.759** — confidently wrong (coin-flip = 0.25) |
| **Germany 1–2 Japan** (Doan & Asano off the bench) | Germany **67.7%** | favourite **LOST** | **Brier 0.459** — confidently wrong |
| **Portugal 0–1 Morocco** (En-Nesyri's header; first African semifinalist) | Portugal **60%** | favourite **LOST** | **Brier 0.360** — confidently wrong |
| **Outright winner** (pre-tournament futures) | Brazil ~20% favourite | **Argentina** (3rd favourite, ~13%) won | favourite eliminated in the QF |
| **Argentina 3–3 France, 4–2 pens** — *the final* | the magic that crowns the arc | Messi's title; Mbappé hat-trick | the moment the whole graph is rooted at |

*(Per-case Brier above is computed by `dataset/golden_template.py` from real sourced odds; the full
arc mean + the nodes where the market was **right** on the favourites are in `dataset/arc_2022.md`
once `arc_build.py` grades the 13-node arc. The arc is a more honest sample than the upset-only seed
— it includes the chalk the market nailed.)*

**Morocco's run is the repeatable-edge story** (the CLV goldmine): the consensus was wrong against
them four rounds running (Belgium #2, Spain, Portugal). That's not one lucky upset — it's a
*pattern a sourced, contrarian signal would have caught*, which is what `node_eval.py` scores.

## 6. Why this beats KickOracle (the wedge, in one breath)

> KickOracle hands you a confident number from a formula frozen weeks ago, shows you no reasoning,
> publishes no accuracy, and has no name on it. We point the agent that **tops FutureX** at the same
> question, **show every source**, **lock the call before kickoff**, **grade it after** — and sell the
> *same trace* to four different buyers. A number is a guess. **A forecast you can audit and check is
> intelligence.**

## 7. The honest constraints (foregrounded, not buried)

- **Seasonality is real.** A World Cup is a ~6-week spike every 4 years with a hard expiry. The
  evergreen answer is the *compiler + the graded-trajectory asset*, which generalises to any league
  and to any FutureX question — football is just the most demo-legible surface.
- **You cannot backtest the agent on 2022** — it already knows the results (lookahead). So **2022
  grades the MARKET and proves the LAYER SYSTEM**; the *agent's* track record is built **forward** on
  2026 (lock before kickoff → grade after). Don't conflate the two.
- **CLV needs two prices.** For historical 2022 nodes we hold a single price, so CLV is marked n/a in
  the arc; **CLV is the live-2026 metric.** Brier is what 2022 proves.
- **The hosted MiroMind API is real but slow** (minutes/call, ~1/6 empty, 5 QPS). So we **prove the
  kernel on one real call** and fill the tournament-scale arc with **real sourced data in the proven
  shape** — never 16k live calls, never an invented number.

## 8. What's real today vs ambition

- **Real & graded:** the 4-layer node (proven on a real MiroMind trace — Saudi–Argentina); the
  scoring rig (`baseline.py`, self-tested); the market grade on 2022 (`golden_template.py`,
  `arc_build.py`); the live pipeline (`serve_demo.py`).
- **Ambition (labeled as such on screen):** "every match of the whole tournament," the 30k-node live
  graph, the four revenue lines at enterprise scale. Shown by the 2026 webpage + the graph, not
  claimed as already-built.

---

**Bottom line.** The business is **the graded forecast graph**: one trace, four products, one
verified scorecard — sold into a category whose incumbent fakes the one thing that matters. The
2022 arc proves the method on the moments everyone remembers; 2026 makes it live. Everything in the
video exists to make *this* legible in three minutes.
