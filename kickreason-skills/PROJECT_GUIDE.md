# PROJECT GUIDE — how KickReason works end to end

> The *how*. (README = why · each `SKILL.md` = what.)

## The pipeline
```
  question
     │
     ▼
 [miromind-research]  ── deep-research call → trace + sources (prose, ~4 min)
     │
     ▼
 [forecast-compiler] ── extract debatable nodes (answer · why · counter · what-changes) → DAG
     │                         ▲
     ▼                         │ resolved truth
 [forecast-grading]  ───────[ wc-data-library ]   (StatsBomb · Elo · 538 · traffic)
     │
     ▼
 [kickreason]        ── render the node: intel · bet · business · tools · the app card
```

## Running each skill
```bash
# 1. research (the engine) — capture a sourced trace
python3 skills/miromind-research/scripts/narrative.py

# 2. compile — trace → structured debatable nodes → DAG (+ news doctor)
python3 skills/forecast-compiler/scripts/node_extract.py
python3 skills/forecast-compiler/scripts/graph_build.py --update

# 3. grade — calibration, not win/loss
python3 skills/forecast-grading/scripts/baseline.py          # self-test (PASS)
python3 skills/forecast-grading/scripts/golden_template.py   # Brier on resolved 2022
python3 skills/forecast-grading/scripts/build_538_baseline.py

# data — the resolved truth to grade against (run first to seed the library)
python3 skills/wc-data-library/scripts/build_lib2022.py
python3 skills/wc-data-library/scripts/derive_lib2022.py

# 4. render — one node → four desk views
python3 skills/kickreason/scripts/views.py
```
Worked end-to-end example: [`examples/saudi-argentina-node.md`](examples/saudi-argentina-node.md).

## Data flow & Evidence Levels
The forecast = the sharp de-vig anchor. Public/odds-echo nodes *confirm* the line (push 0); only `_unpriced`
nodes (breaking news the market hasn't absorbed) move it. Pre-news forecast = the market; the unpriced injury
is the edge ("we priced it first"). Every value flows tagged `REAL` / `MODEL` / `MOCK`
([evidence-levels.md](skills/kickreason/references/evidence-levels.md)). Grades are computed over a **locked,
pre-registered** set.

## The honest hard parts
- **One call ≈ market consensus** (no edge on a quiet question) → value is question *selection* + *legibility*,
  not a private edge.
- **Grading a debate** → grade calibration + the resolvable component + CLV; present the irreducible coin-flip,
  never fake-resolve it. A 70% call losing is not a miss.
- **Prose, not JSON** → never demand a JSON node in one call; structure post-hoc in `forecast-compiler`.
- **Slow + 5 QPS** → produce ahead of kickoff; the ~6-min news window is a strength (re-run on the lineup),
  not real-time.
