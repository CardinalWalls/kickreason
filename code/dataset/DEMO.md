# 60-SECOND DEMO — "One trace, many payoffs"

**The claim:** one slow, expensive MiroMind deep-research trace is *compiled* into a
maintained forecast graph, and that single graph pays off as **three different products**
(fan card, analyst trace, betting/intel signal). When news breaks, we re-run *one node*,
not the whole tournament — and we never beat the market on price alone, only when we hold
**unpriced** news first.

This storyboard tracks `dataset/demo.py` beat-for-beat: it runs the WHOLE loop offline on
real captured artifacts and **computes every number** (nothing is typed in). It imports the
real components `node_extract.py`, `node_eval.py`, `views.py`, `graph_build.py`,
`baseline.py` — reuse, never reimplement. Run it: `python3 dataset/demo.py`.

Every beat below names the **real file/artifact** it shows. No mock screens.

---

### 0–10s · STEP 1 — the raw MiroMind trace streams in
**Show:** `dataset/runs/wc26-usa-advance.json` (1.78 MB) scrolling — the captured SSE trace,
replayed with no network via `node_extract.load_run`.
**Say:** "One MiroMind deep-research call: **22,054 steps — 22,008 thinking chunks, 14
web_searches, 32 fetches**. The question is *Will the USMNT advance from their group?* It's
**99.8% raw thinking**, fragmented into tiny chunks. Beautiful, unusable. You can't sell this."
**Real artifact:** `dataset/runs/wc26-usa-advance.json` (id `wc26-usa-advance`; action
counts printed live from the trace by `step1_trace`).

### 10–22s · STEP 2 — COMPILE the trace into auditable nodes (zero extra LLM)
**Show:** `node_extract.extract_nodes(run)` → `dataset/graph/nodes.json` (**20 nodes**,
directions `{up: 19, down: 1}`, source on **20/20**). One node expands to the NODE CONTRACT
`{node_id, trigger:{action,...}, evidence, judgment, prob_direction, sources, value_score}`.
**Say:** "A deterministic compiler stitches the fragmented thinking into spans, anchors each
span to the search/fetch event beside it, and emits **one node per decision point** — every
node traces back to a real fetch URL. No second model call. The fluff is gone; the evidence
is keyed."
**Real artifact:** `dataset/node_extract.py` → `dataset/graph/nodes.json` (+ `demo_out/nodes.json`).
The load-bearing node carries the model's **own de-vig math, verbatim from the trace**.

### 22–32s · STEP 3 — score node VALUE, learned from resolved upsets
**Show:** `node_eval.learn_class_weights()` then `node_eval.value_score` over every node;
the Top-5 by value_score print with their `_factors` (source × contrarian-magnitude × signal-weight).
**Say:** "We learned class weights from **6 priced past games — 5 were market MISSES (base
upset rate 0.83)**. The evaluator floats up the well-sourced, contrarian, down-pushing nodes,
because that's where the market gets it wrong. Scores are written back to `nodes.json`."
**Real artifact:** `dataset/node_eval.py` → `dataset/graph/nodes.json` (+ `demo_out/nodes.scored.json`),
weights learned from `dataset/seed-resolved.json`.

### 32–42s · STEP 4 — ATTACH to the graph + COMPUTE the parent forecast
**Show:** `views.load_graph()`; attach `usa_advance` as a real node under `champion`; the
forecast is computed from the market anchor + the node signal.
**Say:** "We anchor to the **de-vig line the trace itself captured: american −1000 →
implied 0.9091**, via `baseline.implied_prob_american`. All 20 nodes are *already reflected
in that sharp line* (odds restatements, the format rule, home advantage) — so they CONFIRM
it, they don't move it. Counting them again is the double-count bug that fakes a 99%. With
no unpriced news, **the computed forecast = the sharp market: 91%. We AGREE with the line.**
One deep-research pass has no edge — edge needs new info."
**Real artifact:** `dataset/views.py` + `dataset/baseline.py`; output `demo_out/graph.attached.json`.
Max swing reserved for unpriced news is **±0.104**, learned from the backtest.

### 42–50s · STEP 5 — the SAME graph, three business views
**Show:** `views.view_fan` / `view_analyst` / `view_moving` — three panes from the one node set:
- **FAN** — prediction card: **`PICK: ✅ YES — USA advance (91%, very likely)`** + plain reasons.
- **ANALYST** — the auditable trace: each node's trigger + judgment + evidence + source.
- **MOVING-LINE** — nodes ranked by `value_score`: what moved, which way, the source host.
**Say:** "Same trace. Three payoffs. The fan sees a clean pick. The analyst sees the
receipts. The trader sees the signal. We rendered the product three times and never re-ran
the model."
**Real artifact:** `dataset/views.py` → `demo_out/view.{fan,analyst,moving}.txt`.

### 50–60s · STEP 6 — DOCTOR UPDATE: news flips ONE node → recompute → propagate → market frozen
**Show:** `step6_doctor` applies one breaking-news event to the **highest-value node
(`wc26-usa-advance::n18`, value 0.634)**, flips its direction, re-scores it through
`node_eval`, recomputes the parent, and marks ancestors STALE via `graph_build.ancestors`.
*(Labeled SIMULATED offline — same mechanism as the live `graph_build.py --update`, which
makes one real MiroMind call; replayed here for speed.)*
**Say:** "**BREAKING: USMNT key forward ruled OUT of the group stage (hamstring), US Soccer,
2026-06-05.** A forward out pushes DOWN. The node flips up→down and re-scores **0.634 → 0.812**
(now flagged `injury`, contrarian, *unpriced*). It's the only node the sharp line hasn't
absorbed, so it's the only one that moves us: **unpriced-news move +0.000 → −0.030**.
**P(USA advance) 91% → 88%.** The market de-vig is **still 91% (line −1000) — THE MARKET
HASN'T MOVED YET.** We now sit **3 pts BELOW the stale line**. We priced the injury first.
That gap is the edge. `champion` is marked ⚠️STALE."
**Real artifact:** `dataset/graph_build.py` (`ancestors()` stale-propagation) + `dataset/node_eval.py`
(re-score) → `demo_out/doctor_update.json` + `demo_out/graph.after_update.json`.

### Tagline
**"One trace. Three payoffs. We only beat the line when we hold the news first — 88% vs a frozen 91%."**

---

## Files touched on screen (all real, all in repo)
| Beat | Step | File(s) |
|---|---|---|
| 0–10 | 1 TRACE | `dataset/runs/wc26-usa-advance.json` |
| 10–22 | 2 COMPILE | `dataset/node_extract.py` → `dataset/graph/nodes.json` |
| 22–32 | 3 VALUE | `dataset/node_eval.py`, `dataset/seed-resolved.json` |
| 32–42 | 4 ATTACH | `dataset/views.py`, `dataset/baseline.py` → `demo_out/graph.attached.json` |
| 42–50 | 5 VIEWS | `dataset/views.py` → `demo_out/view.{fan,analyst,moving}.txt` |
| 50–60 | 6 DOCTOR | `dataset/graph_build.py`, `dataset/node_eval.py` → `demo_out/doctor_update.json` |

## One-line architecture
`MiroMind trace (slow, raw)` → **`node_extract.py`** (deterministic compile) → `nodes.json`
→ **`node_eval.py`** (value learned from resolved upsets) → **`views.py`** (graph attach + fan/analyst/moving)
→ **`graph_build.py`** (stale-propagation on update), anchored by **`baseline.py`** de-vig against **`seed-resolved.json`**.
All driven end-to-end by **`dataset/demo.py`**, offline, every number computed.
