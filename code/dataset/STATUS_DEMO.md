# DEMO STATUS — every corner task you raised

✅ done · 🔄 in progress (parallel now) · 🔶 partial / modeled-not-built · ⏳ pending · 🅿️ parked-by-decision
_Re-derive proof with `python3 dataset/api_usage.py` · run the loop with `python3 dataset/demo.py`._

## A · Foundations (story + standard)
| | corner | evidence |
|--|--|--|
| ✅ | Story = the **compiler** (not a website); FIFA = the surface | `CONTRACT.md`, memory |
| ✅ | **No-faking** enforced (sourced/unsourced, audits) | `compiler/verify.sh`, demo audits |
| ✅ | **MiroFlow**: borrow DAG design now / run engine later | `CONTRACT.md` |
| 🔄 | **Golden standard for the example** (FutureX + Brier/CLV + resolved cases) — *identified, now being built into a scene* | `seed-resolved.json`, `baseline.py` |

## B · The pipeline (the 6-step loop) — runs end-to-end in `demo.py`
| | step | evidence |
|--|--|--|
| ✅ | 1 Trace (real MiroMind run) | `runs/wc26-usa-advance.json` |
| ✅ | 2 Extract nodes from the trace | `node_extract.py` (20 nodes) |
| ✅ | 3 Value each node from 回溯/past upsets | `node_eval.py` |
| ✅ | 4 Forecast = sharp market (honest, no fake edge) | `demo.py` |
| ✅ | 5 Three business views | `views.py` |
| ✅ | 6 Doctor update (injury → 91%→88%, below the line) | `demo.py` step6 |

## C · Proof & API usage (your "most urgent")
| | corner | evidence |
|--|--|--|
| ✅ | **Proof of API use** — 20 calls, 11.0M tokens, ~65 min, 1,465 sources | `api_usage.py` → `API_USAGE.md` |
| 🔄 | Fold concurrency (5-QPS 429s) + batch into the proof | *parallel now* |
| ✅ | 4/4 kill-switches: concurrency (5 QPS), full-model, update-latency, prop-count | `runs/exp-*.json` |
| ✅ | Batch question answered (batch ≈ 48× cheaper) | `runs/exp-batch.json` |
| ✅ | Compiler honest: captures thinking; sourced/unsourced verdicts | `compiler/miro.py`, `compile.py` |

## D · The deliverable (feel-it / the video)
| | corner | evidence |
|--|--|--|
| ✅ | HTML **product page** | `demo.html` |
| ✅ | **Whole-loop walkthrough deck** (click-through, recordable) | `walkthrough.html` |
| ✅ | Demo **contract** (the spec) | `CONTRACT.md` |
| ✅ | Mock render | `MOCK_DEMO.md` |
| 🔄 | **Golden-template opener scene** (resolved case graded by the standard) | *parallel now* |
| 🔄 | Reconcile `DEMO.md` with what `demo.py` actually runs | *parallel now* |
| ⏳ | **The 3-min video itself** — yours to record; the pages are ready | — |

## E · Value & scale (business)
| | corner | evidence |
|--|--|--|
| 🔶 | Trace → 4 value streams — 3 views = the surfaces; SEO-at-scale / betting feed / flywheel ingest = designed not built | `views.py`, research |
| ⏳ | **Diverse users + steering** (inject your concern / add your own bet) — not built yet | — |
| 🔶 | Live 舆情 trigger pipeline — architecture designed, not built | research |
| 🔶 | Scale (tiering + 5-QPS launcher, ~11–16k questions) — modeled, not built | `MARKET_DEPTH.md` |
| ⏳ | **Break the evidence monoculture** (distinct-signal questions) — not done | — |

## F · Research (done)
| | corner | evidence |
|--|--|--|
| ✅ | Whole story (MiroMind DNA, FutureX, flywheel, money) | memory `miromind-prediction-flywheel-facts` |
| ✅ | Intel best-practice + business models | research |
| ✅ | Idea ledger (all your ideas recorded) | memory `idea-ledger-fifa-demo` |

## Honest scoreboard
**Solid & shippable:** the 6-step loop runs, API usage is proven, the compiler is honest, two viewable demos exist.
**The real gaps:** (1) the example needs the golden standard *shown*, not just claimed; (2) steering + the 4 value streams at scale are designed, not built; (3) evidence monoculture; (4) the video isn't recorded.
