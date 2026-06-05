# Golden example, control group, and the HCI-grounded demo

> Corrects [4 closed-loop plan](4%20closed-loop%20plan%20—%20interaction-to-trajectory%20compiler.md): drops NVDA, redefines "golden," reframes build→research/test/practice, adds the control-vs-golden design and HCI grounding. The harness, the 7 rules, the surface schema, and the G1–G7 closed-loop checklist in doc 4 still stand — only the scene, the framing, and the demo change. Verified by web research 2026-06-04.

---

## 0. Two findings that reset the plan

**Finding 1 — what "golden" actually means here.** A golden example must have **verifiable ground truth**. NVDA "hold or trim" has none (it's advice, not a checkable outcome) — that was the right objection. MiroMind's *own* golden cases are **verifiable future-event predictions**, and they live in **FutureX** — the live future-prediction benchmark (ByteDance Seed / Fudan / Stanford / Princeton) that **MiroFlow ranked #1 on (Sept 10, 2025), lifting GPT-5's prediction accuracy ~11%**. FutureX questions resolve against the real outcome *after* the event, by design — that is the property that makes them "golden." Examples from the FutureX paper (arXiv 2508.11987): *"Which team will win the NBA championship in 2026?"*, Tour de France jersey winner, weekly box-office/chart top-N, "Ethereum up or down on date X." Your "F1 race / gold price" instinct was exactly right — that *is* the archetype.

- The branded gold/F1/Super Bowl showcase cases are **not published as citable pages** (only generic mentions + Discord). The citable, verifiable cases are FutureX. *(confirmed: arXiv 2508.11987; miromind blog "tops-futurex-benchmark"; PRNewswire 302566213)*
- **MiroVerse-v0.1 is gated** (login-walled; row fields unverifiable anonymously). What's public: ~147,985 full-trajectory samples, 602K+ tool interactions, **SFT + DPO** formats; sources are **static multi-hop QA (HotpotQA, 2Wiki, MuSiQue), web-navigation/deep-search (WebWalker, WebDancer, WebShaper), science (MegaScience), tables (WikiTables)**. *(confirmed: HF API manifest)*
- **What MiroVerse lacks (our argument, now evidence-backed):** every source is a *static, machine-verifiable QA task with a frozen gold answer* — **no human-in-the-loop, no time-decaying/updatable ground truth, no future-prediction self-grading, no interactive decision.** That is the exact data class our human-interaction trajectories produce.
- **Format anchor:** MiroFlow's public **GAIA validation trace** (73.94% pass@1; runnable example "first country in the XLSX starting with Co → Congo, DRC") is MiroMind's only publicly inspectable full agent trajectory. Align our trajectory *fields* to it (ReAct: thought / action / tool_call / observation + question / answer / metadata), since the MiroVerse rows are gated. *(confirmed: github MiroFlow)*

**Finding 2 — the HCI target is appropriate reliance, not "trust."** The defensible, literature-backed claim a small demo can make:

> **Transparent, evidence-citing reasoning enables *appropriate reliance*: when a flawed source entered, the human correctly overrode the agent; when sources were sound, they relied — relative self-reliance (RSR) and relative AI-reliance (RAIR), not blind acceptance.**

Backed by **Lee & See 2004** (calibrated reliance; misuse/over-trust vs disuse/under-trust), **Schemmer et al. 2023 IUI** (RAIR/RSR metric), and the contrast **Bansal et al. 2021 CHI** (explanations usually just *raise acceptance* — so demonstrating correct override is non-trivial). Validated readouts if we want a number: **Hoffman et al. 2023** Explanation-Satisfaction (8-item) + Trust (8-item) scales; **Madsen & Gregor 2000** "perceived understandability."

---

## 1. The golden example, redefined

**Golden example = a FutureX-style verifiable prediction**, run through MiroMind, maintained as a surface, and ultimately **self-graded against the resolved outcome.** Properties it must have: verifiable ground truth, a **decaying window** (so time is a live variable and the maintained-surface demo is motivated), citable sources, non-expert-friendly (NOT finance).

Recommended instance class: **a sports championship / race outcome** (your F1 archetype) — maximally understandable, unambiguous ground truth, time-decaying, MiroMind's #1-FutureX home turf. Pick a *recently-resolved* event so the demo can reveal the ground truth on camera (resolve the tension between "open enough to revise" and "resolved enough to score" by replaying a real trajectory whose outcome is now known). Exact instance = a decision point (§7).

We do **not** invent the golden example — we take it from MiroMind's ecosystem (FutureX domain), align its trajectory to their GAIA/MiroVerse format, and add the layer they lack: **human interaction + audit verdicts + diffs.**

---

## 2. Control group vs golden example (the experimental spine)

Your instruction: the **bootstrap case — "how we used MiroMind to research and build this very hackathon demo" — is the CONTROL group, not the golden example.** This gives the project a quasi-experimental shape the judges (who built a verification engine) will read instantly.

| | **Control: the bootstrap case** | **Treatment: the golden example** |
|---|---|---|
| Task | Us using MiroMind to research/build this demo | A FutureX-style verifiable prediction |
| Ground truth | None external (ordinary knowledge work) | Yes — the event resolves; self-gradable |
| Disturbances | Real, from our actual interaction (dead-ends, corrections, new constraints we hit while learning Miro) | Real, from human/agent interaction during the maintained surface |
| What it isolates | That the **compiler + interaction interface works** on everyday human-AI research, free of prediction-accuracy confounds | Whether **human reliance was appropriate** (override-when-wrong / rely-when-right), *measurable because truth exists* |
| Role in the demo | Baseline / honesty / "this is real, we ate our own dog food" | The scored showcase; **demoed first** |

Why this is strong: the control proves the *mechanism* (interaction → audited trajectory) on a task with no ground truth — i.e., most real work. The golden case proves the mechanism *plus* lets us score appropriate reliance against truth. Together they say: the method generalizes (control) **and** is verifiable when truth exists (golden). It also literally embodies "we learn from MiroMind and the trace of that human interaction becomes the data" — the control group *is* a trajectory we generated about MiroMind itself.

*(Note: "control vs treatment" here is illustrative/quasi-experimental at demo scale, not a powered study — see §5 honesty caveat.)*

---

## 3. Reframe: research / test / practice (not "build")

You're right — **we are not building a product; we are researching, testing, and practicing what already exists in MiroMind's ecosystem**, and adding the thin missing layer (human-interaction → audited, MiroVerse-aligned trajectory). The milestones change accordingly:

- **R — Research (mostly done).** API verified (hosted deep-research, SSE typed trace); FutureX = the golden-case source; MiroVerse format + its gap; GAIA = format anchor; HCI = appropriate-reliance frame + instruments. *(This doc + doc 4 §0.)*
- **T — Test (the core work).**
  - T1: run the API on the chosen golden prediction with `…-mini`; capture the real trace + sources.
  - T2: align the captured trajectory to the **MiroVerse/GAIA field shape** (ReAct messages + question/answer/metadata); confirm our audit verdicts + diff fields attach cleanly.
  - T3: test that the surface **revises under a real disturbance** and that the audit **catches a bad source** (the appropriate-reliance moment).
  - T4: run the **control (bootstrap) case** — compile our own MiroMind-research interaction into the same trajectory shape.
- **P — Practice.** Rehearse the human-interaction walkthrough; lock the 60s; (optional) run the validated instrument on 1–2 viewers for a real number.

Engineering surface is minimal: an SSE parser (done), a trajectory formatter aligned to MiroVerse/GAIA, an audit check, a diff, and the **human-interaction interface that the demo shows**. The "consumer" *is the 60s demo* — nothing more.

---

## 4. Disturbances come from real interaction (not injected myths)

Per your steer: disturbances are **authentic**, arising from real human/agent interaction — not synthetic myths we plant. Two natural sources:

1. **Golden case:** as the human engages the prediction (asks a follow-up, brings a fact they found, an agent surfaces a new article), the surface revises — and *some* of those inputs are genuinely flawed (a stale number, a low-quality source the human pasted). The audit catches those. The "bad source" the override demo needs is one that *really occurs* in interaction, not one we fabricate.
2. **Control case:** building this demo generated real disturbances — dead-ends, corrections from MiroMind, constraints we discovered (e.g., the API's slowness, MiroVerse being gated). Those are honest disturbances; compiling them is the control trajectory.

This also matches the original seed: *"the trace of human chat history has the decision and disturbance towards MiroMind."*

---

## 5. HCI grounding (maps onto our rules and demo)

Five design principles from the literature, each tied to something concrete:

1. **Target calibrated reliance, not maximal trust** (Lee & See 2004). Success = override-when-wrong + rely-when-right (RAIR/RSR, Schemmer 2023). Frame the demo's win this way.
2. **Let the disturbance produce a visible catch-and-revise.** Observed error → transparent recovery is what the **trust-repair** literature credits with durable, calibrated trust (de Visser 2018; explanation+regret 2021). → maps to our **Rule 2 (diff discipline)** and **Rule 4 (quarantine)**: when the surface revises, it must *state what was wrong and why it changed* — never silently.
3. **Make citations auditable and falsifiable, not just present** (avoid the Bansal 2021 trap where explanations only inflate acceptance). Enable **forward simulation**: "which source drives this claim? what if it's removed?" → maps to **Rule 1 (evidence policy)** + the audit panel. Mental-model accuracy (Hoffman 2023) is the measurable form of "the human understands the reasoning."
4. **Surface uncertainty explicitly** (Zhang/Liao/Bellamy 2020) — the honest-gap behavior we already saw (agent refused to fabricate consensus) is this principle for free. → **Rule 5 (honesty over completeness)**.
5. **Force a moment of engagement** (Buçinca et al. 2021 cognitive forcing): have the human commit a judgment *before* seeing the agent, so reliance is a choice, not a reflex. → a single beat in the demo.

**Defensible claim + readout:** the §0 appropriate-reliance claim, optionally backed by Hoffman's 8-item Explanation-Satisfaction/Trust scale on 1–2 viewers. **Honesty caveat to state in the writeup:** at demo n, results are *directional/illustrative*; the validated instruments + appropriate-reliance framing are what make the claim defensible rather than over-reaching.

---

## 6. The 60-second demo, rebuilt

Required: a reasoning walkthrough on a real problem with steps / references / 判断点. Now on the **golden example**, demoed first, with a **real-interaction disturbance** and an **appropriate-reliance** payoff.

- **0:00–0:10 — The prediction + Surface v1.** A verifiable FutureX-style question (e.g. the championship/race winner). Show v1: the prediction, each supporting claim with a source link and a 判断点, the decaying window (event date), the live trace (real searches/fetches, sped-up).
- **0:10–0:20 — Cognitive-forcing beat.** The human states their own lean *before* trusting the surface (Buçinca 2021) — makes the reliance a visible choice.
- **0:20–0:38 — Real-interaction disturbance → catch-and-revise.** A new input from the interaction (a fact the human brings; or a low-quality source that really showed up). The audit **flags the bad source**; the surface revises with a stated cause + evidence (trust-repair: *what was wrong, why it changed*). The human **correctly overrides** on the bad input and **relies** on the sound revision — RAIR/RSR on camera.
- **0:38–0:50 — Self-grade against ground truth.** Because the event resolved, reveal the **real outcome** and grade the trajectory against it (MiroMind's self-grading-over-time aesthetic; FutureX-style scoring).
- **0:50–0:60 — The product reveal.** Show the emitted **MiroVerse-aligned trajectory** with audit verdicts + diffs + the human-interaction layer, beside the gated-MiroVerse gap: *static QA has no human-in-the-loop, time-decaying, audited trajectories — this is the data class the flywheel lacks.*

The control (bootstrap) case appears in the >60s remainder of the ≤3-min video as the "we ate our own dog food" baseline.

---

## 7. Decision points (never pre-narrowed; obvious errors pre-filtered)

1. **Golden instance.** Pre-filtered: *not* obscure finance (your objection), *not* an unresolved event (can't show ground truth). Remaining: a **recently-resolved sports/race outcome** (your F1 archetype — recommended), an entertainment **top-N** (nice 80%-partial-credit visual), or a resolved crypto up/down (simple but less engaging). Pick the instance.
2. **Model.** Settled per your steer: **`…-mini` for all early/test/practice runs**; reserve full `…-deepresearch` only for the final golden capture if its sharpness is worth the extra minutes.
3. **Per-turn revision cost.** Settled per your steer: **the compiler decides per case** (full deep-research call vs targeted justified-diff) — not pre-set by us. We just make both available.
4. **Consumer.** Settled per your steer: **the 60s demo itself is the consumer** of the compiler. No separate app.
5. **Trajectory shape.** Settled per your steer: **MiroVerse/GAIA-aligned fields + a human-interaction interface** (the disturbance, diff, verdict, and reliance signals layered on the ReAct trajectory).
6. **Open:** do we run the Hoffman instrument on 1–2 viewers for a real number, or keep the claim qualitative? (Cheap; buys a defensible figure.)

Only #1 and #6 are still genuinely open. Call those and the test/practice work is fully specified.

---

## Sources
FutureX: arXiv 2508.11987 · futurex-ai.github.io · miromind.ai/blog (tops-futurex) · PRNewswire 302566213. MiroVerse/GAIA: huggingface.co/datasets/miromind-ai/MiroVerse-v0.1 (gated) · github.com/MiroMindAI/MiroFlow. HCI: Lee & See 2004 (Human Factors 46:50) · Schemmer 2023 (IUI, arXiv 2302.02187) · Bansal 2021 (CHI, arXiv 2006.14779) · Hoffman 2023 (Frontiers Comp Sci 5:1096257) · Madsen & Gregor 2000 · Buçinca 2021 (CSCW, arXiv 2102.09692) · de Visser 2018 (Ergonomics) · Zhang/Liao/Bellamy 2020 (FAccT, arXiv 2001.02114).
