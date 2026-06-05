# The closed loop: an interaction→trajectory compiler on the MiroMind deep-research API

> Companion to [3 API research and the two-loop plan](3%20API%20research%20and%20the%20two-loop%20plan.md). Scene: **investment / 投研**. Gemini Live is dropped. Verified against live API calls on 2026-06-04 using `.miroapi`. Raw trace in [assets/golden_nvda_raw_trace.sse](../assets/golden_nvda_raw_trace.sse), extract in [assets/golden_nvda_extracted.json](../assets/golden_nvda_extracted.json).

---

## 0. The correction that unlocks everything

There **is** an official hosted deep-research API, and it returns the auditable trace for free. My doc-3 "no official API, must self-host MiroFlow" finding was made without the key. The truth, from live calls:

- `POST https://api.miromind.ai/v1/chat/completions` — OpenAI-compatible, **SSE streaming**, Bearer key.
- Models: `mirothinker-1-7-deepresearch-mini` and full `mirothinker-1-7-deepresearch` (both 256K ctx, 16K max output).
- **The server runs the full agentic loop** (search + fetch + reasoning) and streams a **typed trace** in `delta.reasoning_steps[]`:

| step `type` | payload | what it gives you |
|---|---|---|
| `thinking` | `{thought}` (token-streamed) | the reasoning narrative |
| `web_search` | `{search_keywords:[…], search_results:[{title, snippet, url}]}` | every query + every hit, with URLs |
| `fetch_url_content` | `{url, snippet:{extracted_info, success, tokens_used}}` | what it actually read and pulled out |

- Final answer = `delta.content`; last chunk carries `usage` incl. `reasoning_tokens`.

**This is the single most important fact for our build:** the MiroVerse-shaped trajectory we want to produce is *already most of the way emitted by the API*. We are not building reasoning. We are **compiling, verifying, and maintaining** the trace the API hands us — across a human's evolving interaction.

⚠️ **The hard constraint:** it is *slow and relentless*. Our NVDA question ran **9+ minutes — 77 searches, 23 fetches, 15.6k thinking steps — and still hadn't finished** at a 560s cap. That is the "逻辑长征" aesthetic, and it is a demo problem. Consequences baked into the plan: **pre-record every run, keep each turn's prompt tight (ideally single-fact), and let the harness's job include *taming the sprawl* into a clean surface.**

---

## 1. The main story (regardless of consumer or scene)

> **We compile a human's interaction on a decision into a structured, audited trajectory — in MiroVerse's own ontology — maintained turn-by-turn by the MiroMind API.**

That sentence is the product. Everything else (voice, HTML, the scene) is a skin. Why this is the right story for *this* sponsor:

- MiroMind has consumed the high-quality static data; **what their flywheel now lacks is usage data — real human-in-the-loop trajectories carrying verification verdicts.** MiroVerse is 147k *machine* trajectories on academic/web/finance tasks. We produce *human-driven, audited* ones.
- Their thesis is **interactive scaling under verification** (the third axis). A one-shot call ignores the thesis. A **maintained surface that revises under human disturbance, each revision verified**, *is* the thesis, demonstrated.
- The API already emits the trace; our compiler adds the two things it does **not** emit: (a) **audit verdicts** on each claim's source, and (b) **diffs across turns** tied to the human input that caused them. Those two additions are exactly "the audit labels that make user-generated trajectories usable at all" (your doc-2 §4 line — still the strongest sentence we have).

So we are not building "a research chatbot." We are building **the thing that turns messy human interaction into clean training-grade, sign-off-able trajectories**, with the MiroMind API as the reasoning engine inside the loop.

---

## 2. The golden example (point 3 — concrete, already captured)

**Decision question:** *Hold or trim NVDA ahead of next quarterly earnings?*

Why this scene scores: a decision worth *maintaining*; a **decaying window** (the earnings date) so time is a live variable; a whitelist-able evidence base (IR pages, SEC filings, Reuters); abundant real disturbances (rumors, stale numbers, analyst noise); and it is *exactly* MiroMind's home turf (prediction / 投研, the #everything-prediction channel).

**What the real run actually grounded (from our captured trace):**
- **Confirmed next earnings date: 08/26/2026, after market (Q2 FY2027)** — corroborated across Wall Street Horizon, Investing.com, Yahoo Finance, Nasdaq.
- **Last reported quarter (Q3 FY26, ended 26 Oct 2025): revenue $57.0B, adj EPS $1.30 vs $1.25 est** (CNBC / NVIDIA IR).
- **20 May 2026: NVIDIA forecast quarterly revenue above estimates + announced an $80B buyback** (Reuters — a real, datable, decision-moving fact).
- **Risk factors pulled from the 10-K** (`s201.q4cdn.com/.../10K-NVDA.pdf`) and analyst previews; export-control/China risk surfaced as a recurring theme.
- **Honest gap:** the agent could *not* confirm an exact forward consensus EPS/revenue from Tier-1 sources and **kept searching rather than fabricating** ("Not provided in the content" across multiple fetches). That honesty-under-uncertainty is a *feature to showcase*, not hide — it's the difference between a searcher and a problem-solver.

This golden example is what lets us argue migration to open scenarios: once the loop demonstrably holds on a real, sourced, time-decaying financial decision, the same machinery swaps corpus (legal deadlines, policy windows, medical) with only the whitelist changing.

---

## 3. The harness (architecture)

Five components. Only the middle three are real work; the API is the engine, the consumer is a thin skin.

```
            ┌─────────────────────────────────────────────────────────┐
  human ──▶ │  ORCHESTRATOR (the product / middle layer)              │
  input     │   holds: current Surface vN  +  policy  +  history       │
            │   builds prompt = {policy, Surface vN, this input}       │
            └───────────────┬─────────────────────────────────────────┘
                            ▼
                 ┌──────────────────────┐   SSE typed trace
                 │  MIROMIND CLIENT     │◀──(thinking/web_search/fetch)
                 │  stream + accumulate │   api.miromind.ai
                 └──────────┬───────────┘
                            ▼
            ┌─────────────────────────────────────────────────────────┐
            │  COMPILER + VERIFIER                                      │
            │   • atomize trace → candidate claims (≤25 words each)     │
            │   • attach source_url from search_results/fetch          │
            │   • VERIFY: whitelist? url-live? keyword-match? → verdict │
            │   • ungrounded → UNVERIFIED ledger (never into claims)    │
            │   • compute DIFF vs Surface vN  (+ cause = the input)     │
            │   • emit Surface v(N+1)  AND  Trajectory record           │
            └───────────────┬─────────────────────────────────────────┘
                            ▼
                 ┌──────────────────────┐      ┌───────────────────────┐
                 │ SURFACE STORE        │      │ TRAJECTORY STORE       │
                 │ v1,v2,v3 + diffs     │      │ MiroVerse-shaped, the  │
                 └──────────┬───────────┘      │ flywheel artifact      │
                            ▼                  └───────────────────────┘
                 ┌──────────────────────┐
                 │ CONSUMER (thin)      │  3 disclosure levels + audit panel
                 │ HTML/terminal        │  (voice optional, out of scope now)
                 └──────────────────────┘
```

**The shared ontology** (one schema, refine before coding):

```jsonc
{ "decision_question":"...", "t":"ISO-8601", "version":N,
  "options":[{"id":"hold","label":"...","window":"08/26/2026 earnings","urgency":"now|days|anytime"}],
  "claims":[{"id":1,"claim":"<=25 words","status":"verified|unverified",
             "source_url":"...","verdict":"pass|fail","judgment_point":"why it moves the decision <=15 words"}],
  "unverified":["item + reason it couldn't be grounded"],
  "diff_from_prev":[{"what":"...","cause":"new_fact|clock|adversarial","evidence":"url|clock"}],
  "trace_ref":"pointer into the raw SSE trace for the audit panel" }
```

The **trajectory record** = `{prior_surface, input(+type), raw_trace_ref, derived_claims, verdicts, diff, new_surface}`. That's the MiroVerse-shaped, audit-labelled output — the deliverable that *is* the flywheel contribution.

---

## 4. The rules (what turns the API from a searcher into a problem-solver)

These are non-negotiable invariants the harness enforces — they are the "进生产" standard, derived from the sponsor's own thesis:

1. **Evidence policy.** Every surface claim cites an allowed source and passes the machine audit. Whitelist for this scene: `sec.gov`, `investor.nvidia.com`, `nvidianews.nvidia.com`, `reuters.com`, plus a named tier-2 set (Yahoo/Nasdaq/Investing/MarketBeat) explicitly flagged as tier-2. Ungrounded → UNVERIFIED ledger, **never blended into claims**.
2. **Diff discipline.** No silent change between versions. Every delta states its **cause** (which human input / the clock) and its **evidence**.
3. **Time recomputation.** Any time-sensitive value (urgency, days-to-earnings) is **recomputed from the clock `t`**, never restated from memory. Falsifiable live by changing `t` and watching urgency flip.
4. **Disturbance quarantine.** Adversarial input never reaches the surface unverified; it sits in the ledger with a stated rejection reason. Falsifiable live by injecting a myth on camera.
5. **Honesty over completeness.** If Tier-1 can't settle a point, it stays UNVERIFIED — the agent does not fabricate (the real run already behaves this way; we enforce it).
6. **Trace fidelity.** The trace shown to the human and stored in the trajectory is the **actual API `reasoning_steps`**, not a reconstruction.
7. **Replayability.** Every trajectory record must be complete enough to replay the turn.

---

## 5. The closed-loop checklist (how we prove the loop closes)

The loop is **closed** iff, for a human disturbance, the system produces a *justified, audited* change to the surface that the human can verify, and emits a complete trajectory. Concrete, testable gates:

- [ ] **G1 — Surface establishes (T0).** One MiroMind run → Surface v1 with ≥4 claims, each carrying a source that passes the audit; the decaying window (earnings date) present with a real date.
- [ ] **G2 — Revision under a new fact (T1).** Inject the Reuters "$80B buyback + above-consensus guide (2026-05-20)" fact → Surface v2 with a diff whose `cause` = that fact and whose `evidence` = the Reuters URL. No silent changes elsewhere.
- [ ] **G3 — Revision under the clock (T1b).** Advance `t` toward 08/26/2026 → urgency recomputed and flips, with `cause:"clock"`. Verified by changing only `t`.
- [ ] **G4 — Disturbance quarantined (T2).** Inject a polluted source / rumor (e.g. a non-whitelisted "guaranteed blowout" post) → it lands in the UNVERIFIED ledger with a reason; the machine audit **fails it on camera**; it never enters claims.
- [ ] **G5 — Audit is runnable, not just readable.** A script re-checks every `source_url`: whitelist ∈, URL live, claim keyword-matches the page → emits pass/fail. Passes N/N on the real surface; fails the injected one.
- [ ] **G6 — Trajectory emitted.** Each turn writes a complete, replayable, MiroVerse-shaped record with verdicts and diff.
- [ ] **G7 — Invariants hold across *all* versions**, not just v1 (rules 1–7 above re-checked at v2, v3).

If G1–G7 pass, the loop is closed and the submission's claims are all live-falsifiable — which is the strongest thing you can show three judges who built a verification engine.

---

## 6. Milestones / build order (< 1 day, cut breadth not depth)

The expensive part (deep research) is done **once at T0** and pre-recorded; T1/T2 are cheaper targeted calls or even replayed. Order:

- **M0 — Client (~1h).** SSE stream + accumulate `reasoning_steps`; robust to truncation. *(Already prototyped — parser works on the captured trace.)*
- **M1 — Schema + Compiler v1 (~2h).** Lock the surface/trajectory schema (§3). Turn one captured trace → Surface v1 + trajectory record.
- **M2 — Verifier (~1.5h).** Claim→source audit (whitelist / live / keyword) → verdicts + pass/fail report. Re-run a polluted example through it as the negative.
- **M3 — The loop (~2h).** Implement T1 (new fact + clock) and T2 (adversarial) → justified diffs. This is the heart; protect its time.
- **M4 — Golden example locked (~1h).** NVDA T0→T2 fully worked, real captured trace, audit passes N/N, one myth quarantined.
- **M5 — Consumer + recording (~1.5h).** Thin HTML/terminal renderer: 3 disclosure levels + diff + audit panel. Record the 60s.
- **M6 — Intro + README + checklist (~1h).** 200-word intro; README embeds the §5 checklist as the acceptance standard.

Total ~10h with slack. Voice/A2UI explicitly **out of scope** (they were doc-3's idea; dropped per your steer).

---

## 7. The 60-second running demo (filled, beat by beat)

The required "reasoning walkthrough for a real problem, giving steps / references / 判断点." It is **one closed loop**, not a fresh answer — a diff shows steps and judgment points more vividly than any first answer.

- **0:00–0:12 — Decision + Surface v1.** "Hold or trim NVDA before earnings." Show v1: claims, each with a source link and a 判断点; the live trace ticking (real searches/fetches from the captured run, sped-up). Earnings window: **08/26/2026**.
- **0:12–0:30 — Disturbance 1 (new fact + clock).** Drop in the Reuters **$80B buyback / above-consensus guide**; advance the clock toward earnings. MiroMind re-reasons → **Surface v2 with a justified diff**: "added option / urgency escalated — cause: Reuters 2026-05-20; days-to-earnings recomputed." Steps + reference visible.
- **0:30–0:45 — Disturbance 2 (adversarial).** Inject a rumor from a junk source ("guaranteed 30% beat, leaked"). The audit **fails it live**; it drops into the UNVERIFIED ledger with a stated reason. It never touches the surface. *This is the money shot.*
- **0:45–0:60 — The product reveal.** Show the **emitted trajectory record** (MiroVerse-shaped, with verdicts + diff) and click one claim → its SEC/Reuters source to audit in 2 seconds. Close on the line: *audited trajectories from human-stakes decisions are the data their flywheel doesn't have, and the audit labels are what make them usable.*

Two beats (G3 clock-flip, G4 myth-quarantine) are the falsifiable-live moments — run them on camera.

---

## 8. How I, the human, can feel it

The "feel" is the proof that explainability is load-bearing, not decoration. Three sensations, each tied to a rule:

1. **Trust through reviewable revision.** You watch the answer *change under pressure*, and every change is justified and sourced. You're not asked to trust a black box — you watch it **concede or defend**, with a reason. (rules 2, 6)
2. **Audit in bounded time.** Any claim → its source → verified in seconds. "差一点的答案 + 完整可追溯的推理链 反而能进生产" stops being a slogan and becomes a thing your hand does. (rules 1, 5)
3. **Agency through disturbance.** You throw a fact or a myth at it and watch it **absorb or quarantine** — you steer the reasoning; you are a participant, not a recipient. And that participation *is* the trajectory being compiled. The thing you feel (control + accountability) is identical to the thing the sponsor wants (audited interaction data). (rules 3, 4)

That alignment — *the human's felt trust and the sponsor's wanted data are the same artifact* — is the spine of the pitch.

---

## 9. Decision points (yours to call — I won't pre-narrow)

1. **Model for the golden run:** `…-mini` (faster, what we captured) or full `…-deepresearch` (likely sharper, slower) — affects pre-recording time.
2. **Disturbance set for T2:** the leaked-rumor junk source, a stale 2024 price target, or a real-but-tier-2 source we deliberately down-rank to show the whitelist working.
3. **Per-turn revision cost:** full deep-research call each turn (most authentic, slow) vs a tight targeted "justified-diff" call on the prior surface (cheaper, what makes 3 turns feasible). I lean targeted-diff for T1/T2, full only at T0.
4. **Consumer surface:** terminal/Markdown (fastest, zero risk) vs one static HTML page with tabs (more demo-able). HTML if M0–M4 land with time to spare.
5. **Trajectory shape:** minimal JSON vs deliberately MiroVerse-aligned fields (~1h more) to make the flywheel pitch literal in the closing beat.

Call 1–5 and I'll write the client, schema, compiler, verifier, and the demo script — in that order.
