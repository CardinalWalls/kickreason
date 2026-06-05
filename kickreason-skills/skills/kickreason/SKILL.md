---
name: kickreason
description: >-
  Generate World Cup / football forecast INTELLIGENCE as debatable nodes — never a single
  "who wins" number. Use this whenever the user wants a match or tournament forecast, a
  "should I trust this pick" analysis, a debatable-node intel report, an argued both-sides
  call, a scoreline/props breakdown, or anything framed as "KickReason". This is the
  orchestrator: it runs research → compile → grade → render and returns a node the user can
  argue with. Prefer it over a plain answer whenever a football prediction should show its
  reasoning, sources, counter-case, and a public grade.
---

# KickReason — debatable-node football intelligence

Turn a forecast question into a **debatable node**: the answer, the *why* (layered factors), the
strongest **counter-case**, **what would change our mind** — sourced, and graded. Never sell the bare
final result; one call on "who wins" just echoes the market, where there is no edge. The value is the
*important, contested* questions and the reasoning on them.

## Procedure
1. **Frame the question.** Keep only *important* (high-leverage: flip it and the picture changes) AND
   *debatable* (genuinely contested) questions. Filter out the settled and the trivial. See
   `references/north-star.md`.
2. **Research** → run the `miromind-research` skill on the question (trace + sources).
3. **Compile** → run `forecast-compiler` on the trace: answer + why + counter-case + what-would-change-it,
   and place it in the node DAG.
4. **Grade** → run `forecast-grading` (calibration vs results), using `wc-data-library` for resolved truth.
5. **Render** the node for the reader — pick the view: intel briefing · bet card (scoreline/props) ·
   business/attention brief · tools (node-as-API). `scripts/views.py` renders the views.

## Run
```bash
python3 scripts/views.py            # render a node into the four desk views
```

## Output
A debatable-node card: question · lean (number + confidence) · why (layers) · counter-case ·
what-would-change-it · sources (tiered) · grade. The user can challenge the number/a source and lock a take.

## Evidence Levels — honor on every output
Tag every value `REAL` / `MODEL` / `MOCK` with source tiers; never present a model or mock as real; grade
on **calibration, not win/loss**. See `references/evidence-levels.md`.

## References
`references/north-star.md` · `intel-desk-standard.md` · `layer-model.md` · `evidence-levels.md`
