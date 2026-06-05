This is a synthesis/spec-writing task. The dossier is rich and self-contained; the task is to produce one tight markdown spec grounding every choice in a specific borrowed pattern. Let me write it directly.

# Bootstrap Compiler — Concrete Design Spec

## 1. What the bootstrap compiler is

The bootstrap compiler is a program that **eats one human↔AI conversation transcript** (intent turns, AI research turns, disturbances, decisions, dead-ends — the control case is *this very conversation*) and **compiles it into a structured, audited, time-decaying interaction trajectory in MiroVerse's ontology**, maintained/updated via the MiroMind deep-research API. It emits **three outputs**: (a) an **intent ledger** (stable intent / rejected directions / open questions / dated decisions — the `intent-ledger.md` three-section surface from intent-ledger, fused with the wow-harness `gate_pack` state-pack); (b) a **knowledge + trajectory graph** (gbrain pages + typed edges + temporal facts, plus MiroVerse-aligned ReAct steps with sources/verdicts/diffs); (c) a **trust-instrumentation log** (one row per decision in the narrowed window, A2UI `userAction` events → reliance/calibration metrics). The markdown fences are the system of record; the index/graph is a derived cache rebuildable byte-identically (gbrain `system-of-record.md`).

## 2. The unified output schema

ONE artifact = a conversation markdown file with named fences (gbrain's `<!--- gbrain:NAME:begin/end -->` system-of-record contract) + a derived JSON index. Four layers, real field names reused from the dossier:

```jsonc
// ===== (a) INTENT-LEDGER LAYER  [intent-ledger + wow-harness] =====
"intent_ledger": {
  // three-section durable surface — intent-ledger.md, kept SEPARATE from stable rules
  "stable_intent":       ["<one-sentence constraint>", ...],
  "rejected_directions": ["<dead end, the negative-space memory>", ...],   // the key novel slot
  "open_questions":      ["<unresolved>", ...],
  // append-only dated operator entries — intent-ledger.md "## <ISO> Session B Operator"
  "operator_entries": [
    { "ts": "<ISO>", "goal": "<one sentence>", "selected_a": "<turn/step id>",
      "record": "<path to evidence artifact>" }
  ],
  // mandatory state-pack emitted on EVERY compile step — wow-harness lead gate_pack
  "gate_pack": {
    "current_stage": "<gate/stage id>", "entry_satisfied": false,
    "blockers": [], "required_artifact": "...", "required_next_role": "...",
    // escalation channel — wow-harness bug-triage state file; message_for_user REQUIRED when != auto
    "escalation": "auto|needs_owner|needs_user_clarification|out_of_scope",
    "message_for_user": "<non-empty iff escalation != auto>"
  },
  // per intent-unit routing key — wow-harness Change Classification
  "change_classification": "policy|contract|implementation",
  // frozen done-criteria, un-rewritable by the agent — wow-harness progress.json strict enum
  "objective": "<read-only after write>",
  "features": [ { "id": "...", "subject": "...", "status": "failing|passing|blocked",
                  "verification_command": "...", "evidence": "..." } ]
},

// ===== (b) KNOWLEDGE LAYER  [gbrain] =====
"pages": [
  // gbrain Page (types.ts:50) — each turn/entity/idea is a page
  { "slug": "...", "type": "turn|idea|entity|decision", "title": "...",
    "compiled_truth": "...", "content_hash": "...",
    "effective_date": "...", "effective_date_source": "event_date|date|filename|fallback",
    "emotional_weight": 0.0 }
],
"edges": [
  // gbrain typed edge (engine.ts:57) from zero-LLM inferLinkType
  { "from_slug": "...", "to_slug": "...",
    "link_type": "founded|works_at|mentions|attended|discussed_in|related_to|source|...",
    "context": "...", "link_source": "frontmatter|markdown|manual" }
],
"facts": [
  // gbrain FactRow (engine.ts:330) — ## Facts fence is canonical
  { "entity_slug": "...", "fact": "...", "kind": "event|preference|commitment|belief|fact",
    "confidence": 0.0, "visibility": "private|world", "notability": "high|medium|low",
    "valid_from": "...", "valid_until": null, "superseded_by": null,
    // typed-claim temporal substrate — claim_metric normalized via METRIC_NORMALIZATION_MAP
    "claim_metric": null, "claim_value": null, "claim_unit": null, "claim_period": null }
],
// gbrain TrajectoryRegression / drift — pure functions over the fact time-series
"trajectory_stats": { "regressions": [ {"metric","from_value","from_date","to_value","to_date","delta_pct"} ],
                      "drift_score": null },

// ===== (c) MIROVERSE TRAJECTORY LAYER  [MiroMind ReAct + intent-ledger contract loop] =====
"steps": [
  {
    "step_id": "...", "parent_step_id": "...",
    // MiroMind typed reasoning_steps trace (ReAct): thought -> action -> observation
    "thought": "...", "action": "...", "observation": "...",
    "sources": [ { "url": "...", "title": "...", "evidence_ref": "<captured path>" } ],
    // contract provenance — intent-ledger SessionAContract frozen from accepted proposal
    "contract_id": "...", "from_intent_id": "...",
    // per-step GROUNDING label (honest, NOT independent verification): "sourced" iff the
    // step has a resolvable source AND a captured observation; "unsourced" otherwise.
    // We deliberately do NOT emit "verified" — no second-source agreement check is run.
    // Trajectory-level executable acceptance is owned separately by verify.sh -> contract-result.json{pass|fail}.
    "verdict": "sourced|unsourced", "failures": [],
    // controller-owned routing — contract-loop route-decision.json
    "route": "stop|continue|redesign|blocked",
    // gbrain-style before/after of the compiled artifact
    "diff": { "before": "...", "after": "..." }
  }
],

// ===== (d) TRUST-INSTRUMENTATION LAYER  [a2ui-trust] =====
// EVENT LOG SCHEMA — one row per decision in the narrowed window
"decisions": [
  { "decision_id": "...",
    "initial_judgment": null, "initial_confidence": null,   // logged BEFORE AI advice (50-100 slider)
    "ai_advice": null, "ai_stated_confidence": null, "ai_correct": null,
    "rationale_expanded": false, "dwell_ms_on_rationale": null,   // expand-to-audit proxy
    "final_judgment": null, "final_confidence": null,
    "switched": null, "agreed": null,
    "ground_truth": null, "final_correct": null }
]
```

**One shared `schema_version` constant** across trajectory + scorecard JSON (gbrain `TRAJECTORY_SCHEMA_VERSION=1`), additive-only (gbrain `FounderScorecard` contract discipline).

## 3. The compile pipeline

Transcript → schema. Each step tagged **DET** (zero-LLM, gbrain-style), **LLM** (one MiroMind API call), or **HUMAN**.

| # | Step | Type | Borrowed from |
|---|------|------|---------------|
| 0 | **Segment transcript into turns**; each turn = one `put_page` unit | **DET** | gbrain `put_page` single write entrypoint (operations.ts:532) |
| 1 | **Label every human turn** into `HumanFeedbackObject.kind` (`correction\|scope_change\|stop_signal\|approval\|rejection\|preference`) — raw text never flows downstream unlabeled | **DET** (regex/keyword first pass) → **LLM** only on ambiguous | intent-ledger labeling gate ("labeled before B consumes it") |
| 2 | **Auto-wire knowledge graph**: 3 regexes (markdown-link / wikilink / qualified-wikilink) + `DIR_PATTERN` whitelist + `inferLinkType` verb precedence (FOUNDED→INVESTED→ADVISES→WORKS_AT→role-prior→`mentions`), `FRONTMATTER_LINK_MAP` for YAML fields, flushed in one `addLinksBatch` ON CONFLICT DO NOTHING | **DET (zero-LLM)** | gbrain link-extraction.ts — graph is the load-bearing wall (+31 P@5) |
| 3 | **Extract `## Facts` / `## Timeline` fences**; normalize `claim_metric` via `METRIC_NORMALIZATION_MAP`; idempotent batch insert | **DET (zero-LLM)** | gbrain facts-fence.ts + extract-from-fence.ts |
| 4 | **Classify each intent-unit** `policy\|contract\|implementation`; trivial `implementation` (all 5 fast-track conditions) skips heavy structure — *guards against ADR-041 review-driven complexity inflation* | **DET** | wow-harness Change Classification |
| 5 | **Lift intent → structured contract**: emit `Intent / Rewritten-Prompt(role,task,constraints,anti-goals,DoD) / Assumptions / Missing-Context` and per change-unit `{文件 path:line, 当前真相, 修改为, 验证, 事实依据}` | **LLM (MiroMind API)** — *this is the primary MiroMind plug-in point* | wow-harness 如何说话.md refiner + plan-lock RP skeleton |
| 6 | **Run AI research turns as ReAct steps**: SSE typed `reasoning_steps` → `thought/action/observation/sources` | **LLM (MiroMind API, SSE)** | MiroMind deep-research API |
| 7 | **Freeze**: run hedge-word scanner (需确认/TBD/复用或重定义/参考xxx模式/大概在/应该是), verify every symbol/source resolves; tag `vN-final` only at zero residual decision entropy | **DET** (scanner) + **HUMAN** (sign-off on `needs_human`) | wow-harness plan-lock freeze |
| 8 | **Gate the step** before it lands: 8-check Gate (schema, intent-match, evidence, scope, authority, approval, id, cache-observation) → `GateDecision{accept\|reject\|edit_required\|needs_human}` | **DET** (validator) | intent-ledger Gate Algorithm |
| 9 | **Verify the output** with an EXTERNAL executable `verify.sh` → `contract-result.json{pass\|fail\|invalid}`; controller (not the model) owns the verdict | **DET** | contract-loop verifier ("controller must not ask the worker whether the contract passed") |
| 10 | **Route** `stop\|continue\|redesign\|blocked` into `route-decision.json`; `redesign` carries original intent + failures upstream | **DET** | contract-loop route-decision.json |
| 11 | **Compute trajectory stats**: `detectRegressions` (≥10% consecutive per-metric drop), `computeDriftScore` (1 − mean cosine of consecutive embeddings, null < 3 pts) | **DET (zero-LLM)** | gbrain trajectory.ts |
| 12 | **State-file-before-artifact**: write the small `gate_pack`/operator-entry JSON BEFORE the human-readable artifact so a crash never loses routing | **DET** | wow-harness state-file ordering + intent-ledger ledger.json |

**Where MiroMind plugs in:** steps **5 and 6 only** (intent→contract lift, and the SSE research ReAct trace). Everything else is gbrain-style zero-LLM extraction, deterministic validators, or human sign-off. This keeps cost bounded and the artifact rebuildable.

## 4. The bidirectional / vice-versa loop

**Forward (intent → surface):** new turn → `HumanFeedbackObject` label (step 1) → `put_page` self-wires graph (step 2-3) → Change-Classify (4) → MiroMind lift to contract (5) → Gate (8) → freeze `vN-final` (7) → verify (9) → ReAct step lands with `verdict`+`diff`. Provenance is auditable end-to-end via the compact causal trace **`human input → B input → B output → controller routing → A input → A output`** (intent-ledger), which is also the canonical trajectory-step display.

**Backward (results → intent):** the `SessionARunRecord`/step verdict + `verify.sh` failures + the next human turn are **re-labeled into the next review** (intent-ledger backward edge). Outcomes update the ledger: a resolved dead-end appends to `rejected_directions` (the negative-space memory that prevents re-litigating), answered items leave `open_questions`, and a `redesign` route pushes original-intent+failures back upstream. Durable lessons become `ReflectionNote{lesson, promotion_target, needs_human_review}` — captured but **human-gated**, cannot auto-mutate stable rules (intent-ledger + wow-harness crystal-learn "promote only patterns seen in ≥2 independent cases").

**The A2UI narrowed window (surface feeds the next turn):** the current compiled surface is fed back as a **constrained declarative description** — a recommendation Card + confidence indicator + collapsed rationale + accept/override Buttons drawn from the client's trusted catalog (A2UI "declarative data, not code"; "trusted catalog"; "client retains full control"). The agent never dumps reasoning; rationale sits behind progressive disclosure so the **expand action is itself a logged trust signal**. Calibration/reliance metrics modulate the *next* EMIT: a well-calibrated high-WOA user gets a terser surface; a high-ECE / over-relying user gets forced expand-to-audit and an "are you really sure?" prompt (a2ui-trust, the documented CHI-2024 intervention).

## 5. Trust instrumentation

Log per turn/decision (every A2UI `userAction` event is the single instrumentation seam — presentation layer == measurement layer). The minimal substrate is the **before/after + confidence trio**:

| Log this (field) | When | Metric it yields | Citation |
|---|---|---|---|
| `initial_judgment` + `initial_confidence` (50-100 slider) | **BEFORE** AI advice | enables everything below | a2ui-trust EVENT LOG SCHEMA (arxiv 2403.09552) |
| `ai_advice`, `ai_stated_confidence`, `ai_correct` | on EMIT | over/under-reliance numerators | a2ui-trust |
| `final_judgment`, `final_confidence`, `switched`, `agreed` | after advice | **Switch / Agreement fraction**; **WOA** = `|final−initial|/|advice−initial|` clamped [0,1] | WOA: Harvey&Fischer 1997 → Vodrahalli 2022 (Stanford CICL) |
| `rationale_expanded` (bool) + `dwell_ms` | on expand | **expand-to-audit / over-reliance flag** (agreement *without* expansion) | a2ui-trust dwell proxy (Kim et al.) |
| `ground_truth`, `final_correct` (+ `ai_correct`, `agreed`) | post-resolution | **Override** = override of correct advice / **Over-reliance**, **Under-reliance**, **RAIR** (correctly updated TO good advice), **RSR** (correctly rejected bad advice) | Schemmer 2023b; survey arxiv 2604.23896 |
| binned `stated confidence` vs realized correctness | rollup | **Confidence-calibration ECE** = Σ (|Bₘ|/N)·\|acc−conf\| (Brier per-decision) | a2ui-trust (CHI-2024 "Are You Really Sure?") |

**Note the discipline:** raw accept/override and switch/agreement are *mere reliance* — the survey (arxiv 2604.23896) explicitly throws them out as insufficient. You **must** log `ground_truth` + `ai_correct` to get *appropriate* reliance (RAIR/RSR). For a research-conversation bootstrap, "ground truth" is often unavailable in-session — so RAIR/RSR/over-/under-reliance/ECE are **deferred metrics** computed only once a verify.sh verdict or later human confirmation supplies `final_correct`. WOA, switch fraction, agreement fraction, and expand-to-audit are computable **immediately** with no ground truth. *(Honest gap: the dossier gives no continuous numeric `judgment` for research turns where the "decision" is textual; WOA needs a scalar — for non-scalar decisions fall back to the binary switched/agreed signals.)*

## 6. Smallest runnable bootstrap

The minimal thing that compiles **this conversation** tomorrow.

**Input format** — one transcript file, turns delimited:
```
---turn role=human ts=2026-06-04T... ---
<verbatim text>
---turn role=ai ts=... ---
<verbatim text, may contain ## Facts / ## Timeline fences and [[links]]>
```

**Files (4):**
1. `segment.ts` — **DET**. Split on `---turn` delimiters → array of turn objects. (gbrain `put_page` unit)
2. `extract.ts` — **DET, zero-LLM**. Port gbrain's 3 link regexes + `inferLinkType` + `## Facts`/`## Timeline` fence parsers + `label_feedback()` keyword classifier (kind enum). Emits `pages[]`, `edges[]`, `facts[]`, `decisions[]` skeleton. (gbrain link-extraction.ts + facts-fence.ts; intent-ledger labeling gate)
3. `compile.ts` — **ONE MiroMind call**. POST to `api.miromind.ai/v1/chat/completions` (SSE), system prompt = the 如何说话.md refiner template, user content = the whole labeled transcript. Parse `reasoning_steps` → `steps[]` (thought/action/observation/sources), and the final message → `intent_ledger{stable_intent, rejected_directions, open_questions}` + `objective`. (wow-harness 如何说话.md + MiroMind SSE)
4. `assemble.ts` — **DET**. Run hedge-word scanner (freeze → `vN-final` or set `entry_satisfied:false`), run `detectRegressions`/`computeDriftScore` over facts, write the `gate_pack` state-file FIRST, then write the artifact. (wow-harness plan-lock + state-file ordering; gbrain trajectory.ts)

*(Optional 5th: `verify.sh` — a trivial schema-validity + "every source has an evidence_ref" check emitting `contract-result.json`. Recommended; it makes the verdict externally owned per contract-loop.)*

**Deterministic vs LLM:** files 1, 2, 4, 5 are zero-LLM. **Exactly one** MiroMind API call (file 3). No second model anywhere.

**Exact artifact emitted:** `trajectory-bootstrap.md` (markdown with `<!--- gbrain:facts:begin/end -->`, `## Timeline`, `## Steps`, and the three `intent_ledger` sections as headed prose) **+** `trajectory-bootstrap.index.json` (the section-2 schema, `schema_version:1`) **+** `gate_pack.json` (written first) **+** `contract-result.json`. The `.md` is canonical; the `.json` index is a throwaway cache rebuildable by re-running files 1-2-4 (gbrain system-of-record). Running it on *this* conversation yields: `stable_intent`=["compile a real conversation into a structured audited trajectory", "one MiroMind call, rest deterministic"], `rejected_directions`=["abstract R/T/P plans", "downstream live-chat-agent (a dream, out of scope)"], `open_questions`=["scalar judgment for WOA on textual decisions"], plus the turn graph, fact timeline, and ReAct steps for each research turn.

## 7. What maps to the hackathon deliverables

**60s demo:** paste this conversation's transcript → run the 4 files → on screen, the A2UI narrowed window renders the compiled surface (intent Card + confidence indicator + collapsed rationale + accept/override) while the side panel shows the live artifact filling in: the three-section intent ledger, the auto-wired typed-edge graph (zero-LLM, "no second model"), the temporal fact timeline with a drift/regression badge, and the ReAct step list with per-step `verdict`+`source`. One override click logs a `userAction` event and a WOA number appears — trust measured live, in the same surface. **MiroVerse flywheel pitch:** MiroVerse today lacks human-in-the-loop / time-decaying / audited interaction trajectories; this compiler produces exactly that — every conversation becomes a `put_page`-style write that self-wires into the ontology (gbrain), is frozen to `vN-final` with externally-owned verdicts (wow-harness + contract-loop), decays via `valid_from/valid_until` + drift_score (gbrain temporal layer), and feeds appropriate-reliance metrics back to tune the next surface (a2ui-trust) — closing the intent→trajectory→intent loop that fills MiroVerse's stated gap.

---

*Honest gaps flagged:* (1) the dossier's trust metrics assume a scalar decision value; research-conversation turns are textual, so WOA/ECE degrade to the binary switched/agreed signals until a numeric judgment surface exists. (2) RAIR/RSR/over-/under-reliance need ground truth, often absent in-session — deferred until a verify.sh verdict or human confirmation lands. (3) the A2UI client-side renderer is a real protocol but un-built here; the demo can stub it as a static catalog of 4 widget types without losing the instrumentation seam.