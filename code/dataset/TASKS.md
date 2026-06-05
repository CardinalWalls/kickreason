# TASKS — parallel backlog to reach INTEL-PROFESSIONAL level

Handoff for multiple agents working at once. **Each lane owns distinct files → no conflicts.**
Pick a lane, read its files, push it. Cross-cutting rules at the bottom.

## The dream (one line)
One living **DAG** of the whole World Cup — every match/team/player/moment a node; each node
seen through **4 business layers** (odds · narrative · magic-moment · stats); **each layer
powered by a REAL professional system**; filled by MiroMind (RAG), graded by the compiler
(Brier/CLV). **Proven on resolved 2022, live for 2026.**

## The bar — what "intel-professional" means (the gap to close)
Naive = one famous fact per layer (what we have now). **Professional = a named real system +
real data + a source + a grade, per layer, repeatable.** Each layer needs its system:
- **ODDS** ← a real prediction model: de-vig of the closing line (Pinnacle no-vig) + **Elo**
  (eloratings.net, `1/(1+10^(-ΔElo/400))`) + optional Poisson/Dixon-Coles. Graded by **Brier + CLV**.
- **STATS** ← real performance data: **xG, shots, possession, PPDA, set-pieces** (FBref/Opta/StatsBomb grade), sourced.
- **NARRATIVE** ← structured analysis from **named outlets** (The Athletic, Opta analyst, Guardian) — not vibes.
- **MAGIC-MOMENT** ← real **event data**: goals/scorers/minutes/shot-xG/key events, from match data.

## DATA SPINE + the 5th layer  → see `dataset/DATA_SOURCES.md` (per layer: source → link → access → acceptance)
**We are NOT a bet demo** — betting is 1 of 6 professional domains; the product is one verified trace re-read
into each domain's metric. The real 2022 library is BUILT: `dataset/lib2022/` (StatsBomb all 64 + 360, derived
players/teams/bracket, Elo + **538** odds baselines, hero narratives). Free 2022 data is confirmed for every
layer: ODDS (538+Elo+martj42) · STATS (StatsBomb+FBref+FIFA TSG) · MAGIC-MOMENT (StatsBomb+Fjelstul) ·
NARRATIVE (**Guardian Open Platform API** = the legal full-text pipeline). **NEW 5th layer = TRAFFIC / growth /
fan-engagement** (CTR/retention/push-reach/virality; data = Kaggle WC2022 tweet+sentiment dumps · Google Trends ·
YouTube views). 2022 beats 2026 for prototyping it (X/Reddit live APIs are paid → historical dumps only).
Only true gap left: real-market closing odds at scale (OddsPortal/Betfair scrape) for genuine CLV.

## Build principle (non-negotiable)
**Prove the kernel for real → mock the scale faithfully.** One real API call must return a
layered sourced node; everything at scale is a *labeled* mock of that proven shape. Never run 16k calls.

## Current honest state
**REAL (runnable, verified):**
- `demo.py` — the loop runs (real trace → nodes → computed forecast 91→88). *Nodes are raw-trace, weak.*
- `api_usage.py` → `API_USAGE.md` — 36 real API calls · 12.2M tokens · 1,690 sources · 7×429.
- `golden_template.py` → `GOLDEN.md` — Brier on resolved 2022 (authoritative grading).
- `serve_demo.py` — live server runs the pipeline on GET /run (http://localhost:8000).
- `narrative_nodes.json` (2022) + `narrative_nodes_2026.json` — real sourced narrative grain.
- `gen_questions_2022.py` → `questions_2022.json` — 8,367 real questions (1,060 valuable).
- `prove_kernel.py` — DONE: **HALF-proven**. Model returns rich, status-conditioned prose covering the grain, but **not clean JSON** (ignores schema) + under-retrieves. Structuring needs a 2nd mechanism (see Lane 1). → `runs/prove-kernel.json`.
**MOCKED / NOT REAL:** `dream.html`, `walkthrough.html` (slideshows, hardcoded); the 30k DAG, 4-layers-per-node, live propagation (modeled only).
**NAIVE / WEAK (must fix):** nodes = raw thinking fragments; hero story = fairy-tale (one upset, no professional systems); forecast adjustment = homemade `ANCHOR_CONVICTION` heuristic (replace with a real model).

---

## LANES (parallel — each owns its files)

### LANE 1 · KERNEL (the hinge — do first)
Owns: `prove_kernel.py`, `CONTRACT.md`.
- **RESULT (runs/prove-kernel.json):** HALF-PROVEN. The model returned rich prose that (a) **covered all four grains** and (b) **conditioned on the status we passed in** (used 88% / 13%, the injury note, even cited Saudi-Argentina) — BUT **ignored the JSON-only contract** (wrote markdown, parse failed) and **under-retrieved** (1 search, 0 fetches). So: *intelligence + conditioning = works; clean one-call machine-structure = does NOT.*
- **✅ PROVEN (2026-06-05):** the fix is **TWO MODELS** — MiroMind researches (prose + real sources) → a format-obedient structuring pass extracts the layered node. `sau_arg_2022` came out **fully valid** (4 layers, 4 real sources) → `runs/kernel-structured.json`; architecture locked in `CONTRACT.md` ("Kernel"). **Remaining research-step fixes:** (1) ensure the research call actually RETRIEVES (`usa_advance` under-captured → 0 sources); (2) sharpen per-layer depth (the `magic_moment` came out generic under a probability-focused prompt).
- **Fix paths (try in order):** (a) **two-step** — research call (prose) → cheap 2nd call "convert this to the exact JSON node"; (b) **function/tool-calling** or **full model** + a strict few-shot example; (c) **compiler extraction** — deterministically/LLM-parse the prose into the layered node (the original compiler role). Also force real retrieval (the prompt read like "format my inputs", not "go research").
- **Done:** a verified path from one node-prompt → a clean **layered, sourced** node + the node schema locked in `CONTRACT.md`.

### LANE 2 · ODDS SYSTEM (professional)
Owns: `forecast.py` (new), `baseline.py`.
- Build a real model: de-vig closing odds + **Elo win-prob** (fetch real eloratings.net values) + optional Poisson. Grade by **Brier + CLV** on resolved 2022. **Delete `ANCHOR_CONVICTION`.**
- **Done:** authoritative per-match number from named sources, graded.

### LANE 3 · STATS SYSTEM (professional)
Owns: `stats_layer.py` (new).
- Pull real performance data (xG, shots, possession, set-pieces) for the hero matches from sourced data (FBref/Opta-grade), structured per node, with source URLs.
- **Done:** stats layer with real metrics + sources per hero node.

### LANE 4 · NARRATIVE SYSTEM (professional)
Owns: `narrative.py`, `narrative_nodes*.json`.
- Upgrade to structured, **named-source** analysis (The Athletic, Opta, Guardian) per node; fix the src=0 capture on the 2022 run; attach real URLs.
- **Done:** narrative layer = sourced, structured storylines per hero node.

### LANE 5 · MAGIC-MOMENT SYSTEM (professional)
Owns: `moment_layer.py` (new).
- Real event data (goals/scorers/minutes/shot-xG/key events) for the hero matches, sourced; the star/highlight angle.
- **Done:** magic-moment layer with real event data + source per hero node.

### LANE 6 · THE DAG
Owns: `dag.py` (new), `graph_*`.
- Build the real dependency graph for ONE hero run (champion → ... → leaves), edges = dependencies, **propagation up**. Attach the 4 layers (from Lanes 2-5) to each node.
- **Done:** a real DAG for one hero run, with propagation + layers.

### LANE 7 · HERO STORY (intel-professional — NOT the fairy-tale)
Owns: `HERO.md`.
- Vehicle: **Morocco's run** (repeatable edge — beat #2 Belgium, Spain, Portugal; consensus wrong 4 rounds → CLV goldmine) OR **Argentina's arc** (lose to Saudi → win it all → the greatest final). Tell it **through the 4 professional systems** — every claim sourced + graded; the edge, not the shock.
- **Done:** `HERO.md` at intel-professional depth; multiple professional systems visible.

### LANE 8 · QUESTION UNIVERSE
Owns: `gen_questions_2022.py` (+ a 2026 variant).
- Tag every question with its `layer`; mark resolved 2022 answers (gradable); build the 2026-forward variant.
- **Done:** universe with valuable subset + layer tags + answers.

### LANE 9 · DEMO PAGES (fancy + animated — kernel-real, scale-mocked)
Owns: the HTML decks + `serve_demo.py` routes.
- AFTER Lanes 1-7: mock the fancy animated pages **grounded in the proven kernel + real layer systems**: story → real layered nodes → DAG → graded → 2026. Wire live to `serve_demo` where possible; **label every mock.**
- **Done:** fancy pages, kernel-real + scale-mocked, honestly labeled.

### LANE 10 · PROOF / EVAL
Owns: `api_usage.py`, `golden_template.py`.
- Keep the API-usage ledger current; grade everything by Brier/CLV; maintain the professional-standard page.
- **Done:** live proof ledger + grading dashboard.

---

## Dependencies (sequencing for the agents)
- **Now / independent:** Lane 1 (kernel), Lanes 2-5 (the four professional systems), Lane 8, Lane 10.
- **After 2-5:** Lane 6 (DAG), Lane 7 (hero story).
- **After 1-7:** Lane 9 (the demo pages).

## Cross-cutting rules (every lane)
1. **No faking** — every number computed or sourced; mocks labeled.
2. **Prove the kernel → mock the scale.**
3. **Each layer = a real professional system** (named system + real data + source + grade).
4. **2022 = proof (resolved); 2026 = product (live).**
5. Respect the API's **5 QPS** limit (token-bucket + 429 retry) and the ~1/6 empty-return (retry once).
6. Keep `serve_demo.py` the single live entry point; pages should pull real data, not hardcode.

## Reference docs
- Story/architecture: memory `system-story-node-compiler`, `dream-demo-layers`, `miromind-prediction-flywheel-facts`, `idea-ledger-fifa-demo`.
- Contract/spec: `CONTRACT.md` · status: `STATUS_DEMO.md` · API facts: `.miroapi`.
