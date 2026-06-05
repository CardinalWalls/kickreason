# MiroMind API — grounded research + the two-loop (Gemini Live × MiroFlow) plan

> Companion to [0 Hackthon rules](0%20Hackthon%20rules.md), [0 Miromind's interests](0%20Miromind's%20interests.md), [1 the API research for brainstorm](1%20the%20API%20research%20for%20brainstorm.md), [2 the trauma idea](2%20the%20trauma%20idea.md), [2 trauma test](2%20trauma%20test.md).
> Date: 2026-06-04. Every external claim below carries a source URL. This corrects a load-bearing error in doc 1.

---

## Part A — What the MiroMind API actually is (the correction)

**There is no official MiroMind / MiroThinker HTTP API.** This single fact changes the build.

What exists, in three layers:

| Layer | What it is | What you get |
|---|---|---|
| **MiroThinker weights** | Open-weights LLM (MIT), text-only. Self-host via SGLang/vLLM. | A *plain chat model*. OpenAI-compatible `/v1/chat/completions`. **No** built-in search, no tools, no typed trace. |
| **Hosted weights (3rd party)** | Chutes / Atlas Cloud / Azure AI Foundry serve the open weights. | Same plain chat model, callable in 5 min. Chutes: base `https://llm.chutes.ai/v1`, model `miromind-ai/MiroThinker-v1.5-235B`, ~$0.30/$1.20 per 1M tok, 256K ctx, 8K max output. |
| **MiroFlow** | The agent **framework** wrapped around the weights. *This* is where deep research lives. | The web-search + URL-fetch + sandboxed-Python loop, up to ~300 tool calls, and the **JSON execution trace** (sources, observations, verdicts) "ready for SFT/DPO." |

### The correction to doc 1, point by point

- ❌ "The API already emits a structured, typed reasoning trace (`thinking`/`web_search`/`fetch_url_content`/…) and a top-level `search_results` array, handed to you for free." → **Not a documented API contract.** That shape is roughly MiroFlow's tool set, but it is produced by **running MiroFlow**, not by a hosted chat call. A bare Chutes call gives you tokens only — no trace, no sources.
- ✅ "OpenAI-compatible, point the SDK at a base_url." → True, but only gets you the *plain LLM* (self-host or Chutes).
- ✅ "256K context." → Confirmed (262,144 tokens). Hosted output capped at 8,192.
- ⚠️ "~600 tool calls." → Version-dependent. v1.0 press said 600; v1.7 config says ~300. It's a **MiroFlow** budget, not an endpoint property.
- ✅ "No structured output / `response_format`; tools are MCP-only; multimodal not on the API; stateless per call." → All confirmed. Multimodal in MiroFlow is *separate* preprocessing tools (Whisper/VQA), not native to MiroThinker. State is carried by MiroFlow, not a session object.
- ⚠️ **"$0 deep research" is misleading.** MiroFlow's tools need paid external keys: **Serper** (search), **Jina** (scrape), **E2B** (sandbox).
- ⚠️ **Geo:** MiroMind suspended its *own* service in mainland China / HK / Macau from **2026-05-12**. Third-party hosts serving the open weights aren't governed by that, but note it.

### The buildable path to real deep-research (no GPU)

MiroFlow's LLM endpoint is configurable (`llm.base_url`). So:

> **Run MiroFlow locally (CPU — it's just orchestration) → point its brain at Chutes-hosted MiroThinker → supply Serper + Jina + E2B keys for the tools.**

That gives you the genuine auditable trace without renting 8 GPUs for the 235B. Setup is `git clone` → `uv sync` → fill `.env` → `uv run main.py trace`. A Gradio frontend ships with it. Expect **minutes per deep-research run**.

**Sources:** miromind.ai/blog/miroflow · github.com/MiroMindAI/MiroFlow · github.com/MiroMindAI/MiroThinker (README, miroflow-tools, miroflow-agent) · huggingface.co/miromind-ai/MiroThinker-v1.5-235B · typingmind.com/guide/chutes/miromind-ai-MiroThinker-v1.5-235B · scmp.com/tech/policy/article/3352778 · arxiv.org/abs/2511.11793.

---

## Part B — Your two-loop idea, evaluated against the real API

Your framing, decoded:

> Gemini Live (≈125K audio context) holds the live conversation **and the current decision surface**; MiroMind's multi-step reasoning **updates that surface** under the **same ontology**; the **human chat trace supplies the decisions and disturbances** fed back into MiroMind.

This is exactly the **"maintained decision surface"** pattern from [2 the trauma idea](2%20the%20trauma%20idea.md) (Steps 1–5) — now with a concrete consumer (voice) and a concrete fast-context store (Gemini's window). It is a *good* articulation. Here is what survives contact with the API and what must change.

### What validates cleanly

- **The latency mismatch is the whole point, and Gemini solves it.** MiroFlow runs for *minutes*; voice must answer in *sub-second*. Gemini 2.5 **native-audio** Live supports **async `NON_BLOCKING` function calling** — the agent keeps talking while your backend runs the slow job, then announces the result on `INTERRUPT` or `WHEN_IDLE`. That seam maps onto your architecture almost exactly. (Use **2.5 native-audio**, *not* 3.1 Flash Live — 3.1 does **not** yet support async tools.)
- **"Same ontology"** = define **one JSON schema** for the decision surface. MiroFlow emits it; Gemini receives it; the renderer draws it. This shared schema *is* your middle layer — the thing doc 2 correctly called "the product."
- **Chat trace → disturbance → MiroMind** = the three turn-input classes from doc 2 Step 2: (1) time decay, (2) new fact, (3) adversarial/myth. The voice conversation is a natural generator of all three.

### What must change from your mental model

- ⚠️ **MiroMind does not update Gemini directly.** Your **orchestrator** runs MiroFlow, gets the revised surface, and *pushes* it into the Live session (system-role text update, or a `WHEN_IDLE` tool response). The two engines never talk; the middle layer carries the shared ontology between them. (Reinforces: the middle layer is the product.)
- ⚠️ **Don't store the full trace in Gemini's window.** The 128K is a *ceiling*; the effective default may be **32K**, and audio burns **~25 tokens/sec**. Keep only the **compact surface** (options + windows + headline claims) in Gemini; keep the full trace + unverified ledger + sources in **your backend**. Progressive disclosure isn't just UX here — it's a context-budget necessity.
- ⚠️ **Per-turn revision ≠ a fresh minutes-long deep-research run.** Doc 2 Step 2 already nailed this: each turn sends `{current surface, new input, policy}` and asks for a **justified diff**. So the expensive full MiroFlow run happens **once at T0** (establishes the auditable surface); T1/T2 are **cheaper targeted verification passes** (a tight MiroThinker call + a couple of scoped searches). This is what makes it buildable in a day.
- ⚠️ **Native-audio output is audio-only** — no JSON in the same response. Render UI via a **schema'd `render_cards(...)` function tool** (your "A2UI-lite"), and enable **output transcription** for captions/logs. Audio-only also means the safe survivor-facing surface is *spoken*; the claims table / audit panel are *rendered cards* for the supporter/auditor. That's your progressive disclosure across modalities.
- ⚠️ **Session caps:** audio-only Live sessions = 15 min, WebSocket connection ≈ 10 min. Use session resumption + context compression even for a demo.

**Sources:** ai.google.dev/gemini-api/docs/live-api · …/live-api/tools · …/live-api/capabilities · …/live-session · …/live-guide · …/models/gemini-2.5-flash-native-audio-preview-12-2025 · …/pricing · cloud.google.com/blog (native-audio Vertex) · discuss.ai.google.dev/t/…/145378 (32K default caveat).

---

## Part C — The shared "decision surface" ontology (one schema, both loops)

Everything hinges on this object. Draft (refine before building):

```jsonc
{
  "decision_question": "string",          // the frame, not a topic
  "t": "ISO-8601",                         // surface timestamp — urgency recomputed from this
  "version": 1,
  "options": [
    { "id": "pep", "label": "...", "expiry": "ISO-8601|null",
      "urgency": "now|days|anytime",       // DERIVED from (expiry - t), never restated from memory
      "live": true }
  ],
  "claims": [
    { "id": 1, "claim": "<=25 words", "status": "verified|unverified",
      "source_url": "Tier-1 only", "judgment_point": "why it moves the decision <=15 words",
      "surface_line": "one trauma-informed sentence <=20 words" }   // the spoken/safe layer
  ],
  "unverified": ["quarantined item + reason"],   // never blended into claims
  "diff_from_prev": [ { "what": "...", "cause": "new_fact|clock|adversarial", "evidence": "url|clock" } ],
  "trace_ref": "id into the full backend trace"   // audit panel pulls from here, not from Gemini
}
```

- **Gemini holds:** `surface_line`s + live options + urgencies (the speakable layer).
- **MiroFlow produces:** `claims` + `source_url`s + `trace_ref` (the auditable layer).
- **The renderer draws** three disclosure levels off the *same* object: spoken sentence → claims table → full trace/audit.

This is the literal embodiment of "same ontology, updated by multi-step reasoning, with the human trace as disturbance."

---

## Part D — The flywheel argument (why MiroMind should care)

Each disturbance→revision cycle emits a record:
`{ prior_surface, input(type), MiroFlow reasoning steps + sources + verdicts, diff, new_surface }`
— and now, uniquely, **aligned to a human voice-conversation trace**.

MiroVerse covers academic/web/finance text trajectories. What it lacks: **audited trajectories from human-stakes, time-decaying decisions, pre-labeled with verification verdicts and paired with real human interaction.** Your strongest sentence, in your words (doc 2 §4):

> *audited trajectories from human-stakes decisions are a domain their data doesn't cover, and the audit labels are what make user-generated trajectories usable at all.*

The two-loop design doesn't just *use* the API — it manufactures the exact data class the sponsor's flywheel is hungry for. That is the pitch.

---

## Part E — Scope & build order for < 1 day (risk-tiered)

The honest risk: MiroFlow + 3 paid keys + Gemini Live (preview) + a renderer, in one day, is a lot. Mitigations: (a) demo is **pre-recorded** anyway (MiroThinker is slow — doc 2 §5), (b) cut **breadth not depth** (doc 2 §4), (c) the per-turn diff is cheap, only T0 is expensive.

**Tier 0 — must-have (this is a complete, winnable submission on its own):**
1. Finalize the **decision-surface schema** (Part C).
2. **One real MiroFlow deep-research run** at T0 on the survivor scene → capture the genuine trace + Tier-1 sources (Probe A/C already prove the content quality). This is your auditable substance.
3. **Middle layer**: given `{surface, input}` → emit revised surface + diff. T1 = clock advance + new fact ("the coworker texted her"); T2 = adversarial myth injected → quarantined with reason.
4. **Verifier script**: re-check every `source_url` against the Tier-1 whitelist + URL-live + keyword match → pass/fail report. (Re-run the broken Probe-B Instagram output through it as the on-camera negative example.)
5. **One consumer surface** rendering the three disclosure levels + the diff. HTML is fine here.

**Tier 1 — the differentiator (do if Tier 0 is solid):**
6. Wire **Gemini Live 2.5 native-audio** as the voice consumer. Two function tools: `submit_fact()` (NON_BLOCKING) and `fetch_decision_surface()` (NON_BLOCKING, WHEN_IDLE) + `render_cards()` (schema'd). **MiroFlow runs are pre-computed/cached**, so the voice never actually waits minutes on camera — it demonstrates the live two-loop UX over real, pre-verified surfaces.

**Tier 2 — stretch:** a genuinely live MiroFlow call mid-demo (high risk; only if rehearsal has slack).

**Video (≤3 min)**: the required 60s walkthrough = **one revision cycle (a diff)**, not a fresh answer — diffs show steps/references/判断点 most vividly. Beats: (1) PEP 72h urgency *recomputed* when the clock advances; (2) an injected myth quarantined live; (3) the verifier failing the Instagram citation and passing the real one. Close on the flywheel sentence.

---

## Part F — Decision points (yours to call — I won't pre-narrow)

1. **Front-end for the demo:** voice (Gemini Live, Tier 1) or HTML-only (Tier 0)? Voice is the memorable differentiator but the risky add; HTML alone is already a complete submission.
2. **MiroFlow access:** (a) MiroFlow-local + Chutes brain + Serper/Jina/E2B keys (real trace, ~minutes, some setup), or (b) pre-run once on `dr.miromind.ai` / the web demo and build the maintenance loop around the captured trace (lowest risk). Either way the *live* novelty is the maintenance loop, not re-running deep research per turn.
3. **Scene:** survivor-with-decaying-windows (validated corpus, strongest flywheel story, highest sensitivity) or the legal-deadline twin (same machinery, swap corpus, lower emotional risk).
4. **Turn count:** the 3-turn minimum (T0/T1/T2) or add a T3 where a second window expires mid-session.
5. **Trajectory logging:** minimal JSON, or MiroVerse-shaped (~1 extra hr, buys the explicit flywheel pitch in the closing 20s).

Call these and the concrete build order (prompts, schema lock, code) follows. Nothing is written until you call them.
