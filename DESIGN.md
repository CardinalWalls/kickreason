# KickReason Skills — Design

> **Status: DESIGN (for sign-off before build).** This document lays out how the KickReason project
> (the deployed `CardinalWalls/kickreason` codebase) is refactored into a clean set of reusable
> **Claude Code skills**, modeled on the structure + quality of
> [`fantasea-code/xhs-market-radar`](https://github.com/fantasea-code/xhs-market-radar).

---

## 1. What we're building

KickReason is one pipeline: **a forecast question → researched by MiroMind → compiled into debatable
nodes → graded in public → rendered for a reader.** Today that lives as ~30 loose scripts. We refactor it
into **5 well-scoped skills** that each do one job, plus three-layer docs and an evidence trail — so the
system is modular, reusable, and legible to anyone who opens the repo.

**The through-line (borrowed from the reference's best idea):** *evidence-first, no overclaiming.*
xhs-market-radar grades every claim A/B/C and shows source cards. KickReason already lives this — every
number is `REAL` (computed/sourced) or `MOCK` (illustrative), every node carries source tiers, every call
is graded. We formalize that as the repo's **Evidence Levels**, applied in every skill.

---

## 2. Repo structure (mirrors the reference)

```
kickreason-skills/
├─ README.md              ← WHY: the pitch, the north star, the one-line model (bilingual EN / 中文)
├─ PROJECT_GUIDE.md       ← HOW: the end-to-end pipeline, how the 5 skills chain together
├─ LICENSE  ·  .gitignore (secrets + heavy data excluded)
├─ skills/
│  ├─ kickreason/                 ← THE ORCHESTRATOR (question → debatable-node intel report)
│  │  ├─ SKILL.md                 ← WHAT: the workflow that calls the other four
│  │  ├─ agents/                  ← select-important · detect-debatable · argue-both-sides
│  │  └─ references/              ← north-star · intel-desk-standard · layer-model · evidence-levels
│  ├─ miromind-research/          ← THE ENGINE (deep-research API call + trace/source capture)
│  │  ├─ SKILL.md
│  │  ├─ scripts/                 ← miro_client.py  (from compiler/miro.py + narrative.py)
│  │  └─ references/              ← api-reality.md  (verified: slow, 5 QPS, prose-not-JSON)
│  ├─ forecast-compiler/          ← trace → structured debatable nodes (answer+why+counter+what-changes)
│  │  ├─ SKILL.md
│  │  ├─ scripts/                 ← node_extract.py · graph_build.py  (extract + DAG + doctor/propagate)
│  │  └─ references/              ← node-contract.md · debatable-detection.md
│  ├─ forecast-grading/           ← grade nodes: Brier/CLV calibration on resolved results
│  │  ├─ SKILL.md
│  │  ├─ scripts/                 ← baseline.py · golden_template.py · arc_build.py · build_{odds,538}_baseline.py
│  │  └─ references/              ← grading-methodology.md  (calibration, NOT win/loss)
│  └─ wc-data-library/            ← build a graded tournament data library
│     ├─ SKILL.md
│     ├─ scripts/                 ← build_lib2022.py · derive_lib2022.py · build_traffic_layer.py
│     └─ references/              ← data-sources.md  (StatsBomb · 538 · Elo · Guardian · tweets)
├─ examples/              ← a real debatable-node card · a graded scoreboard · the Saudi–Argentina case
├─ evidence/              ← REAL 2022 artifacts proving the loop closes (graded arc Brier 0.262, the 5.9-min update)
├─ research/              ← the deep-research backing (north-star · intel-industry · stakeholder-demand)
└─ docs/                  ← the deployed live-demo site (GitHub Pages serves this folder)
```

**Conventions (from the reference):** skill dirs `kebab-case`; entrypoint `SKILL.md` (uppercase);
scripts `verb_noun`; reference docs descriptive (`debatable-detection.md`); examples `case.language.md`.

---

## 3. The 5 skills — what each does and where it comes from

| Skill | Triggers when… | Does | Built from (current files) |
|---|---|---|---|
| **`kickreason`** | user wants World Cup intel / a forecast / "argue this pick" / a debatable-node report | Orchestrates: research → compile → grade → render the debatable-node report (the product) | `views.py`, `app/`, the north-star + intel-desk docs |
| **`miromind-research`** | any task needs a sourced, multi-step deep-research answer with its trace captured | Calls `api.miromind.ai`, streams the typed trace, captures thinking + web_search + sources; handles 5-QPS + empty-retry | `compiler/miro.py`, `narrative.py`, `ask.py` |
| **`forecast-compiler`** | a research trace needs structuring into forecast nodes / a node DAG | Extracts nodes (answer + why + counter-case + what-would-change-it), wires the DAG, runs the news "doctor" + propagation | `node_extract.py`, `graph_build.py`, `compiler/extract.py` |
| **`forecast-grading`** | a forecast/pick needs grading vs results (Brier/CLV/calibration) | Grades on **calibration**, not win/loss; de-vigs the market; computes Elo + 538 baselines | `baseline.py`, `golden_template.py`, `arc_build.py`, `build_odds_baseline.py`, `build_538_baseline.py` |
| **`wc-data-library`** | building/refreshing a graded World Cup dataset | Pulls StatsBomb (events/xG/360) + Elo + 538 + tweets; derives players/teams/bracket; all `REAL`, sourced | `build_lib2022.py`, `derive_lib2022.py`, `build_traffic_layer.py` |

Chaining (the PROJECT_GUIDE story): **`miromind-research` → `forecast-compiler` → `forecast-grading`**,
with **`wc-data-library`** supplying the resolved truth to grade against, and **`kickreason`** as the
front-door that runs the whole thing and renders it.

---

## 4. Evidence Levels (the no-faking spine, every skill honors it)

Borrowed from the reference's A/B/C grading, tuned to our world:

| Tag | Meaning | Example |
|---|---|---|
| `REAL` | computed or sourced from primary data | Argentina xG 2.49 (StatsBomb); market Brier 0.76 |
| `MODEL` | a labeled model baseline, not the market | Elo 95%, 538 72% |
| `MOCK` | illustrative product mock-up | a 2026 prop price, the "answers-back" copy |
| source tiers | T1 official · T2 sharp market · T3 named analyst · T4 pundit · T5 rumor | per node |

Rule, stated once and inherited by every skill: **never present `MODEL`/`MOCK` as `REAL`; grade on
calibration; show the work.** This is the same auditability the reference enforces with source cards.

---

## 5. Three-layer docs (the reference's strongest move)

- **README.md** = *why* — the pitch ("argue with every pick"), the north star, the one-line model, a project
  map table, and a "safety & scope" section (no betting-edge claims, no mass scraping). **Bilingual EN / 中文.**
- **PROJECT_GUIDE.md** = *how* — the pipeline end-to-end, how to run each skill, how they chain, the data flow.
- **`SKILL.md` (×5)** = *what* — each skill's trigger + procedure (the agent entrypoint).

---

## 6. Build plan (after you sign off on this design)

1. Scaffold the tree (folders + the 5 `SKILL.md` with full frontmatter + procedures).
2. Move the scripts into each skill's `scripts/` (no logic change — just rehome + a thin CLI per skill).
3. Write the `references/` (lift from existing memory/docs: api-reality, node-contract, grading-methodology,
   data-sources, intel-desk-standard).
4. Populate `examples/` (the Saudi–Argentina debatable-node card) and `evidence/` (the graded arc + numbers).
5. README (bilingual) + PROJECT_GUIDE + LICENSE + .gitignore.
6. (Optional) `skill-creator` eval pass on the `kickreason` skill's triggering.

**Open choices for you:** (a) 5 skills as above, or fold grading into the compiler (→ 4)? (b) repo name
`kickreason-skills` ok, or something else? (c) bilingual README yes/no? (d) publish as its own GitHub repo,
or a `/skills` folder inside the existing `kickreason` repo?
