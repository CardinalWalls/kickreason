# MiroMind fit + the 60-second demo

> **Our goal:** a hackathon demo built on MiroMind's deep-research agent, which is strong at **FutureX** (the benchmark for forecasting *real, future, resolvable* events). Question: which slice of KickOracle's business can that agent genuinely power, and what's the tightest 60s demo? This doc answers both.

---

## 1. The key realization

KickOracle has a big machine, but almost none of it needs AI:

- The **SEO lattice, affiliate, games, leaderboard, pricing tiers** = scaffolding. No intelligence required.
- Its **"AI prediction"** is a **frozen 5-input formula** (FIFA rank 35% · chemistry 30% · morale 15% · stability 10% · familiarity 10%). On the **free/public surface** it does *not* do live research and **shows no accuracy or reasoning** — though the richer model + numbers *may* be premium-gated behind the $39.99 pass (we didn't pay, so read "fakes" as **"doesn't expose,"** not a proven absence).

So the *only* part of the business with real AI value is **the prediction + the narrative briefing** — and on its public surface that's exactly the part KickOracle doesn't show.

**A football match outcome is a canonical FutureX item:** a real-world event, in the future, that will resolve to a verifiable result. So the part of KickOracle worth rebuilding is *literally a FutureX task wrapped in a consumer UI.* MiroMind doesn't just replicate KickOracle here — it **fixes its single biggest weakness** (no reasoning, no track record).

---

## 2. Business component → deep-research fit

| KickOracle component | FutureX / deep-research fit | In our 60s demo? |
|---|---|---|
| **Match win-probability prediction** | ★★★ — the core FutureX use case | **YES — centerpiece** |
| **Daily Intelligence Briefing** (injuries, news, "prediction shifts", narrative) | ★★★ — live multi-source research → narrative | **YES — supplies the "why"** |
| **Accuracy / track-record page** | ★★★ — *our wedge*; deep research is auditable + falsifiable | **YES — the differentiator** |
| Head-to-head narrative | ★★☆ — agent can write it | Maybe (one line) |
| Scout reports / tactical alerts | ★★☆ — heavier research output | No (post-MVP) |
| Power rankings | ★☆☆ — derivable, not interesting | No |
| Programmatic SEO content gen | ★☆☆ — possible, but not the point, not demo-able | **No** |
| Affiliate, games, leaderboard, pricing | ✗ — no AI | No |

**Conclusion:** build one thing well — **"the prediction that shows its work and keeps score."**

---

## 3. The pitch (why this beats KickOracle)

From the teardown, KickOracle's fatal gap: *for a product whose whole value is being right, it shows **zero** reasoning and **zero** accuracy, and has **no named humans.*** Trust rests on a "transparent formula" that never publishes a result.

A deep-research agent inverts every one of those weaknesses **for free**, because of how it works:
1. It **cites its sources** → the reasoning is auditable (KickOracle's number has no "why").
2. It can **lock a timestamped prediction before kickoff** → falsifiable, so you can build a *real* accuracy page (KickOracle's `/accuracy` is empty).
3. It does **live research** (today's injuries, lineups, form) → not a formula frozen weeks ago.

> **One-liner:** *KickOracle gives you a confident number. We give you a forecast you can audit — and then check. Same capability that tops FutureX, pointed at the World Cup.*

---

## 4. The 60-second demo

**Name (working):** "The Oracle that shows its work."

**On screen, one match, three things KickOracle can't show:** the number, the sourced reasoning, the locked & scored prediction.

### Script / shot list
| Time | What happens | Voiceover |
|---|---|---|
| **0–8s** | Show a real KickOracle prediction card: "Mexico 55% · chemistry 90/100." | "Every prediction site gives you a confident number. None show you *why* — or whether they were right." |
| **8–18s** | Cut to our app. User clicks a fixture: **Argentina vs Spain**. | "We rebuilt the prediction engine on MiroMind's deep-research agent — the one that tops FutureX, the benchmark for forecasting real future events." |
| **18–42s** | The agent runs **live**, streaming its work: *"reading latest team news… injury reports… last-5 form… probable XIs… venue & altitude…"* → resolves to **ARG 48% / Draw 27% / ESP 25%**, with **3 key factors, each a clickable citation**, and a 2-sentence narrative. | "It researches the match the way an analyst would — live sources, not a formula frozen three weeks ago." |
| **42–54s** | The wedge. Card stamps **"Locked 18:42 · resolves after FT."** Flip to a **Track Record** tab: past calls, ✓/✗ resolved, running **Brier score**. | "Every call is sourced and locked before kickoff. This is the accuracy page KickOracle never publishes." |
| **54–60s** | Logo + tagline. | "A number is a guess. A *forecast you can audit and check* is intelligence." |

**Why this wins a 60s slot:** the *streaming research* is the wow (you literally watch the AI think and gather evidence); the *citations* land the credibility; the *track record* lands the differentiation. All three in one screen.

---

## 5. Build notes (<1 day, honest about reality)

- **MiroMind API reality (from our earlier finding):** there is no clean hosted MiroMind deep-research API — the capability lives in **MiroFlow / MiroThinker (open source)**. For the demo, wrap MiroFlow as the "forecast agent," or if a hosted endpoint now exists, use it. *Verify current state before committing — this is the one technical risk.*
- **Agent contract:** prompt = *"You forecast football matches. Research <A> vs <B> on <date>: current form, injuries, probable lineups, venue, H2H. Output calibrated win/draw/loss probabilities, exactly 3 key factors each with a source URL, and a 2-sentence narrative. Never invent sources."* Force **structured output** (JSON: `{probs, factors[], narrative}`).
- **Demo hygiene (do this):** pre-run ONE match end-to-end and **cache the real agent trace**; replay it if the live network is slow or the venue Wi-Fi dies. Keep a genuine live run ready, but never let the demo depend on it.
- **Track record is cheap and is the differentiator:** log each prediction `{match, probs, lockedAt}` to JSON; seed 5–10 *already-resolved* past matches with real results and compute Brier so the panel looks alive on day one.
- **Stack:** Next.js + Tailwind (mirrors KickOracle's vibe so the "before/after" cut reads instantly). One serverless route that calls the agent and **streams tokens to the UI** — the streaming *is* the demo, don't hide it behind a spinner.

---

## 6. Scope guardrails (so we don't rebuild the farm)

**Build:** one fixture picker → live agent forecast (probs + 3 sourced factors + narrative) → locked card → track-record panel. That's it.

**Explicitly cut:** the SEO lattice, 19 languages, affiliate/commerce, pricing/Stripe, bracket/leaderboard games, the $5K API, power rankings. They're real parts of *KickOracle's* business but add zero to a *MiroMind forecasting* demo.

**If there's spare time (in priority order):** (1) a "daily briefing" generated by the same agent for today's top match; (2) head-to-head two-team compare; (3) let the user type *any* future football question (leans hardest into the FutureX framing).

> **Note on the original survivor-support idea:** if the team still wants that lane, the same engine generalizes — a deep-research agent that forecasts a resolvable future question and shows sourced reasoning is domain-agnostic. The World Cup is just the most *demo-friendly* FutureX surface (visual, time-boxed, universally legible). Decide which framing sells better to *this* audience.
