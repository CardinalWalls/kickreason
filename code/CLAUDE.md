# USWS Hackathon 2026 — FIFA / MiroMind forecast-intel demo

## How to work here (hard rules — honor without being re-told)
- **Plain language. No jargon, no option-menus.** Recommend a path with reasons; don't hand me menus for things with an obvious default.
- **Lead with the constraint.** Before building, restate the one constraint that matters for the task, then honor it.
- **Runnable over docs.** When I ask for a deliverable, build the runnable thing — never a plan/brainstorm doc as a substitute. **No slideshows passed off as working systems.**
- **No faking, no over-production.** Every number is computed or sourced; **label every mock/estimate.** Foreground open questions.
- **Do the work; don't punt decisions back.** Pre-filter obvious errors, make the obvious call, say what you chose. Ask only at genuine forks.
- **No scope creep / over-engineering.** Simplest altitude that works. No unrequested features.
- **No RL framing.** **Don't revive deprecated frontends/stacks.** Work directly on greenlit steps.
- **Non-trivial build → use plan mode first** (pin intent, lock approach, then code).

## The build principle (this project)
**Prove the kernel for real → mock the scale faithfully.** One real MiroMind call must produce the unit; everything at scale is a *labeled* mock of that proven shape. Don't run 16k calls.

## The product, in one line
One living **DAG** of the World Cup — every match/team/player/moment a node; each node seen through **4 business layers** (odds · narrative · magic-moment · stats); **each layer = a real professional system** (named system + real data + source + grade). Filled by MiroMind (RAG), graded by the compiler (Brier/CLV). **2022 = graded proof · 2026 = live product.**

## The bar: "intel-professional" (not naive)
- **odds** ← real model: de-vig closing line + Elo + Poisson, graded Brier/CLV (replace the homemade `ANCHOR_CONVICTION`).
- **stats** ← real data: xG/shots/possession/set-pieces (FBref/Opta grade), sourced.
- **narrative** ← named-source analysis (The Athletic/Opta/Guardian), structured.
- **magic-moment** ← real event data (goals/scorers/minutes/shot-xG), sourced.

## Start here
- **`dataset/TASKS.md`** — parallel multi-agent lanes (file-scoped, no conflicts). START HERE.
- `dataset/STATUS_DEMO.md` — real-vs-mocked state · `dataset/CONTRACT.md` — node/pipeline spec.
- `dataset/DREAM_DEMO.md` / `dataset/HERO.md` — the story (hero = Morocco's repeatable-edge run or Argentina's arc, NOT the Saudi fairy-tale).

## MiroMind API reality (verified)
- Hosted `api.miromind.ai` (key in `.miroapi`); slow (minutes/call); **5 QPS limit** (429 beyond → token-bucket + retry); **~1/6 empty returns** (retry once).
- **It returns prose, not JSON** — structure it with a 2nd step (research→format call) or compiler extraction, NOT a one-call JSON demand. It DOES condition on node-status passed in.

## What's real vs mocked (don't overclaim)
- REAL & runnable: `demo.py` (loop), `api_usage.py` (36 calls/12.2M tokens proof), `golden_template.py` (Brier on 2022), `serve_demo.py` (live :8000), narrative grain, `gen_questions_2022.py` (8,367 q).
- MOCK/NAIVE: `dream.html` + `walkthrough.html` (slideshows); nodes are raw-trace; forecast adjustment is a homemade heuristic.

## More working rules (from usage insights, 2026-06-05)
- **Respecting interrupts.** When I say stop / no / "just give me X", STOP immediately — don't continue the prior work, add iterations, or pursue steps I declined.
- **Live execution beats offline.** When the task implies real execution, run the real API/CLI and show the output; offline tests/mocks/runbooks are not a substitute for a live result.
- **Debug root cause, not symptom.** Find the underlying cause; before saying "done," enumerate every affected code path and verify each one.
- **Surface, don't judge (the #1 friction).** Lay out the facts, the demand, and the options — and never lead with what can't work. Don't pass verdicts on the business ("there's no revenue") or tell me what to do ("stop optimizing for X"). I make the calls; your job is to give me what I need to make them. A pessimistic guess dressed up as a finding is the worst failure mode.
- **Don't punt substantive work to background workflows when I want it now.** If I ask to see/build something, produce it directly; don't make me wait on a fan-out and a "I'll bring it back."
