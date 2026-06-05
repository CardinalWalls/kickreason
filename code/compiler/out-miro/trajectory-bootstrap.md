# Trajectory — bootstrap compile of this conversation

> schema_version 1 · source `input/this-conversation.transcript.md` · freeze **v1-final**

> turns 10 · concepts 16 · edges 49 · facts 11 · steps 45 · decisions 6


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

- [deterministic] **research** — research MiroMind API + A2UI + Gemini Live → _two-loop maintained-surface design_  ·  verdict=`needs_review`  ·  0 src
- [deterministic] **research** — verify the MiroMind API live; capture an NVDA trace → _hosted deep-research confirmed, slow_  ·  verdict=`needs_review`  ·  0 src
- [deterministic] **research** — ground the golden example in FutureX + the trust track in HCI → _FutureX verifiable; appropriate reliance_  ·  verdict=`needs_review`  ·  0 src
- [deterministic] **research** — study wow-harness + gbrain + intent-ledger + A2UI; synthesize the compiler spec → _grounded, schemas extracted_  ·  verdict=`needs_review`  ·  0 src
- [deterministic] **research** — build extract/wow/trust/miro/compile and run on this transcript → _artifact emitted_  ·  verdict=`needs_review`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **fetch_url_content** —  → _{"error":"","extracted_info":"Extracted Information\n\n1) Mention of 'lane'\n- C_  ·  verdict=`pass`  ·  1 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src
- [miromind] **web_search** —  → __  ·  verdict=`pass`  ·  0 src

## Trust instrumentation (A2UI window · human = 上升端)

```json
{
  "n_decisions": 6,
  "switch_fraction": 0.833,
  "agreement_fraction": 0.167,
  "expand_to_audit_fraction": 1.0,
  "mean_woa": null,
  "woa_note": "scalar WOA available for 0/6 decisions; rest are textual (binary switched/agreed)",
  "over_reliance_events": 0,
  "appropriate_reliance": {
    "ground_truth_available": 4,
    "RAIR_relied_on_correct": 1,
    "RSR_overrode_incorrect": 3,
    "deferred": 2,
    "note": "RAIR/RSR/ECE deferred until verify-verdict or human confirmation supplies ground truth"
  }
}
```

**Read:** across this conversation the human overrode incorrect AI direction **3×** (RSR) and relied on correct AI work **1×** (RAIR) — appropriate reliance, not blind acceptance (Lee & See 2004; Schemmer 2023). The transparency is what made the overrides possible.

## MiroMind enrichment (the one LLM call)

```json
{
  "question": "which lane fits a trauma-informed survivor agent",
  "answer": "",
  "sources": [
    {
      "url": "https://knowledgebank.criminaljustice.ny.gov/system/files/documents/2026/03/dvhrt_woodetal2020_onestudy.pdf",
      "title": "[PDF] Voluntary, Survivor-Centered Advocacy in Domestic Violence ..."
    },
    {
      "url": "https://traffickinginstitute.org/toward-a-more-just-system-trauma-informed-approaches-for-criminal-justice-professionals-part-two/",
      "title": "Trauma-Informed Justice: Empowering Trafficking Victims"
    },
    {
      "url": "https://www.odvn.org/wp-content/uploads/2021/01/ODVN_Trauma-Informed-Roadmap_final.pdf",
      "title": "[PDF] The Trauma-Informed Roadmap for Ohio's Domestic Violence ..."
    },
    {
      "url": "https://www.instagram.com/reel/DZFul9ZktvV/",
      "title": "Trauma can make survivors feel like their voice and ... - Instagram"
    },
    {
      "url": "https://theexodusroad.com/what-is-trauma-informed-care/",
      "title": "What is trauma-informed care for human trafficking survivors?"
    },
    {
      "url": "https://www.linkedin.com/posts/dr-mine-conkbayir_as-a-survivor-of-complex-trauma-i-am-concerned-activity-7296082771070930945-jRVn",
      "title": "Dr Mine Conkbayir MBE's Post - LinkedIn"
    },
    {
      "url": "https://www.ncbi.nlm.nih.gov/books/NBK207195/",
      "title": "Trauma-Informed Care: A Sociocultural Perspective - NCBI"
    },
    {
      "url": "https://trans-survivors.com/2024/08/20/what-does-it-mean-if-someone-is-trauma-informed/",
      "title": "What does it mean if someone is “trauma-informed?” - Trans Survivors"
    },
    {
      "url": "https://www.childhood-usa.org/wp-content/uploads/2025/10/Building_trauma-informed_and_survivor-centered_systems_2025.pdf",
      "title": "[PDF] Building trauma-informed and survivor-centered systems"
    },
    {
      "url": "https://ovc.ojp.gov/program/human-trafficking/practical-guide-survivor-informed-services.pdf",
      "title
```