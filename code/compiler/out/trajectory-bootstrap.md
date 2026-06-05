# Trajectory — bootstrap compile of this conversation

> schema_version 1 · source `input/this-conversation.transcript.md` · freeze **v1-final**

> turns 10 · concepts 16 · edges 49 · facts 11 · steps 5 (0 sourced / 5 unsourced) · decisions 6


## gate_pack (wow-harness — emitted first)

```json
{
  "current_stage": "compile/v1",
  "entry_satisfied": true,
  "blockers": [],
  "required_artifact": "trajectory-bootstrap.md",
  "required_next_role": "human review (上升端)",
  "escalation": "needs_user_clarification",
  "message_for_user": "Open question(s) need your call: which lane fits a trauma-informed survivor agent | which recently-resolved FutureX-style instance to use as the golden example"
}
```

## Intent ledger (intent-ledger + wow-harness)

**Stable intent**
- [implementation] win the MiroMind deep-research lane with reasoning transparency (推理透明), not a black box
- [contract] compile human interaction into a MiroVerse-aligned audited trajectory, maintained by the MiroMind API
- [implementation] the compiler (middle layer) is the product, not the consumer
- [implementation] the golden example is a FutureX-style verifiable prediction (the F1 archetype)
- [implementation] the bootstrap case (building this demo) is the control group
- [implementation] disturbances come from real human or agent interaction, not injected myths
- [implementation] build a bootstrap compiler that eats THIS conversation, learning from wow-harness and gbrain
- [implementation] trust demonstration is a separate track with a real metric under the A2UI philosophy

**Rejected directions** (the negative-space memory)
- ~~Gemini Live two-loop architecture~~ — off-target for the real story; consumer is secondary
- ~~NVDA hold-or-trim golden example~~ — no verifiable ground truth, a golden case needs a resolvable outcome
- ~~the R/T/P (research/test/practice) framing~~ — cosplay; we are actually compiling knowledge through interaction right now
- ~~abstract plan documents~~ — no more plan docs; build the artifact
- ~~the downstream live-chat-agent consumer~~ — a dream, out of scope for now
- ~~the wow-harness launch-article docs as the related reading~~ — wrong; the related article is the TOWOW distributed-harness PDF

**Open questions**
- which lane fits a trauma-informed survivor agent
- which recently-resolved FutureX-style instance to use as the golden example

**Operator entries**
- 2026-06-04T10:30 — confirm hosted MiroMind API and its typed trace (selected: turns/04-ai)
- 2026-06-04T14:00 — build the bootstrap compiler on this conversation (selected: turns/08-ai)

## Concept graph (gbrain self-wiring, zero-LLM)

_9 typed concept→concept edges (of 49 total; rest are turn→concept `mentions`)_

- `tools/gemini-live` —**uses**→ `api/miromind-api`  ·  _Gemini Live …. Best use of the… MiroMind API_
- `api/miromind-api` —**produces**→ `scenes/nvda`  ·  _MiroMind API …uses an OpenAI-compatible SSE stream and emits a typed reasoning_steps trace. I proposed… NVDA_
- `scenes/nvda` —**lacks**→ `data/miroverse`  ·  _NVDA …has no verifiable ground truth — it isn't golden. Find a golden example from the… MiroVerse_
- `data/miroverse` —**lacks**→ `concepts/human-in-the-loop`  ·  _MiroVerse …is gated static QA and lacks… human-in-the-loop_
- `orgs/miromind` —**rejects**→ `tools/wow-harness`  ·  _MiroMind …-like interference with knowledge, not a cosplay of R/T/P. Learn from the… wow-harness_
- `concepts/bootstrap-compiler` —**uses**→ `api/miromind-api`  ·  _bootstrap compiler …uses the… MiroMind API_
- `tools/gbrain` —**produces**→ `tools/wow-harness`  ·  _gbrain …produces the zero-LLM knowledge graph;… wow-harness_
- `concepts/bootstrap-compiler` —**produces**→ `data/miroverse`  ·  _bootstrap compiler …produces the audited 状态/快照 the… MiroVerse_
- `data/miroverse` —**lacks**→ `api/miromind-api`  ·  _MiroVerse …corpus lacks; it uses the… MiroMind API_

## Fact timeline (gbrain ## Facts fence)

<!--- gbrain:facts:begin -->
| # | claim | kind | confidence | visibility | notability | valid_from | valid_until | source | context | claim_metric | claim_value |
|---|-------|------|------------|------------|------------|------------|-------------|--------|---------|--------------|-------------|
| 1 | MiroMind ships a hosted deep-research API at api.miromind.ai | fact | 1.0 | world | high | 2026-06-04 |  | live call | OpenAI-compatible SSE |  |  |
| 2 | The MiroMind API streams a typed reasoning_steps trace | fact | 1.0 | world | high | 2026-06-04 |  | live call | thinking/web_search/fetch_url_content |  |  |
| 3 | MiroThinker context window | fact | 1.0 | world | medium | 2026-06-04 |  | /v1/models | 256K | context_window | 262144.0 |
| 4 | An NVDA deep-research query ran 9+ min and timed out | event | 0.9 | world | medium | 2026-06-04 |  | curl --max-time 560 | 逻辑长征, very thorough | call_minutes | 9.3 |
| 5 | That query ran 77 web_search and 23 fetch steps | event | 1.0 | world | low | 2026-06-04 |  | captured trace | grounded in SEC 10-K + Reuters | search_steps | 77.0 |
| 1 | MiroFlow ranked #1 on the FutureX future-prediction benchmark | fact | 0.95 | world | high | 2025-09-10 |  | arXiv 2508.11987 | golden cases are verifiable predictions | futurex_rank | 1.0 |
| 2 | MiroVerse is gated static QA and lacks human-in-the-loop trajectories | fact | 0.9 | world | high | 2026-06-04 |  | HF dataset card | the data class we produce |  |  |
| 3 | The defensible HCI claim is appropriate reliance (RAIR/RSR), not raw trust | belief | 0.85 | world | high | 2026-06-04 |  | Lee & See 2004; Schemmer 2023 | override-when-wrong, rely-when-right |  |  |
| 1 | wow-harness compiles intent via a fail-closed 9-Gate state machine | fact | 0.9 | world | medium | 2026-06-04 |  | wow-harness lead SKILL | intent compile (降维) |  |  |
| 2 | gbrain wires a knowledge graph with zero LLM calls per page write | fact | 0.95 | world | high | 2026-06-04 |  | gbrain link-extraction.ts | knowledge compile (升维) |  |  |
| 3 | TOWOW frames the loop as 降维换行动 plus 升维做存储, human as 上升端 | belief | 0.9 | world | high | 2026-06-04 |  | 通向智流 distributed-harness article | the compiler is the 升维存储 layer |  |  |
<!--- gbrain:facts:end -->

_trajectory: regressions=0, drift_proxy=0.785_

## ReAct steps (MiroVerse-aligned)

_verdict legend (honest): **sourced** = the step has a resolvable source URL AND a captured observation; **unsourced** = no resolvable source, or a source with nothing captured (e.g. an empty search). `sourced` means auditable, NOT independently verified — no second-source agreement check is performed._

- [deterministic] **research** — research MiroMind API + A2UI + Gemini Live → _two-loop maintained-surface design_  ·  verdict=`unsourced`  ·  0 src
- [deterministic] **research** — verify the MiroMind API live; capture an NVDA trace → _hosted deep-research confirmed, slow_  ·  verdict=`unsourced`  ·  0 src
- [deterministic] **research** — ground the golden example in FutureX + the trust track in HCI → _FutureX verifiable; appropriate reliance_  ·  verdict=`unsourced`  ·  0 src
- [deterministic] **research** — study wow-harness + gbrain + intent-ledger + A2UI; synthesize the compiler spec → _grounded, schemas extracted_  ·  verdict=`unsourced`  ·  0 src
- [deterministic] **research** — build extract/wow/trust/miro/compile and run on this transcript → _artifact emitted_  ·  verdict=`unsourced`  ·  0 src

## Did the human stay in charge? (plain count)

```json
{
  "decisions_logged": 6,
  "times_human_changed_position_after_seeing_ai": 5,
  "times_human_agreed_with_ai": 1,
  "times_human_looked_at_the_reasoning": 6,
  "times_human_agreed_without_looking": 0,
  "good_catches__overrode_ai_when_ai_was_wrong": 3,
  "good_trust__relied_on_ai_when_ai_was_right": 1,
  "decisions_with_no_confirmed_answer_yet": 2,
  "plain_reading": "A healthy collaboration: the human overrides the AI when it's wrong and relies on it when it's right. We only score a decision once the real answer is known; otherwise we say 'no confirmed answer yet'."
}
```

**Read in one line:** across this conversation you **caught the AI being wrong and overrode it 3 times**, and relied on the AI when it was right **1 time(s)** — and you agreed-without-looking **0 times**. That is the point: showing the reasoning is what let you catch the AI. (2 decisions had no confirmed answer yet, so we didn't score them.)
