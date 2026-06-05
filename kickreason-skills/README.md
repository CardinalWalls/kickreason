# KickReason Skills

> **Argue with every pick. All the way to the champion.**
> A World Cup forecasting-intelligence system, packaged as five reusable Claude Code skills.

[Live demo](https://cardinalwalls.github.io/kickreason/) · Proven on 2022 · Live for 2026

---

## What this is
Most prediction tools give you one number and hide the rest. **KickReason** turns every prediction into a
**debatable node** — researched live by MiroMind, shown with its reasoning and sources, argued from both
sides, locked before kickoff, and **graded in public**. We don't sell the bare "who wins" call (one research
pass just echoes the market, where there's no edge); we surface the *important, contested* questions and the
reasoning on them. This repo refactors that pipeline into modular skills.

## Project map
| Skill | Purpose |
|---|---|
| [`skills/kickreason/`](skills/kickreason/) | the orchestrator — question → debatable-node intel report |
| [`skills/miromind-research/`](skills/miromind-research/) | the deep-research engine (trace + sources) |
| [`skills/forecast-compiler/`](skills/forecast-compiler/) | trace → structured nodes → DAG |
| [`skills/forecast-grading/`](skills/forecast-grading/) | calibration / Brier / CLV (not win/loss) |
| [`skills/wc-data-library/`](skills/wc-data-library/) | the graded tournament dataset |
| [`examples/`](examples/) · [`evidence/`](evidence/) · [`docs/`](docs/) | sample output · REAL proof · the research behind it |

See [DESIGN.md](DESIGN.md) for the architecture and [PROJECT_GUIDE.md](PROJECT_GUIDE.md) for how the skills chain.

## How to use
Each skill is a folder with a `SKILL.md` (the entrypoint) + `scripts/` + `references/`. Copy `skills/<name>/`
into your agent's skills directory, or invoke them in sequence:
`miromind-research → forecast-compiler → forecast-grading` (graded against `wc-data-library`), with
`kickreason` as the front door.

## Evidence levels (the no-faking spine)
Every value is tagged: **`REAL`** (computed/sourced), **`MODEL`** (a labelled baseline like Elo/538), or
**`MOCK`** (illustrative). Sources are tiered T1–T5. A model or mock is never shown as real, and forecasts are
graded on **calibration**, not a win/loss tally. See
[`skills/kickreason/references/evidence-levels.md`](skills/kickreason/references/evidence-levels.md).

## Safety & scope
- **Not a betting-edge product.** One research call ≈ the market consensus; we never promise profit. The honest
  value is *published, checkable accuracy* and *legible reasoning* — not a private edge.
- **No mass scraping.** Uses official open data (StatsBomb), free APIs (Guardian), and public archives within
  their terms. Third-party data stays under its source licence (StatsBomb is CC-BY-NC). See [LICENSE](LICENSE).

---

## 中文

> **每一个预测，都可以争辩 —— 一路辩到冠军。**
> 一个世界杯预测情报系统，重构为五个可复用的 Claude Code 技能（skills）。

### 这是什么
大多数预测工具只给一个数字，把过程藏起来。**KickReason** 把每个预测变成一个**可争辩的节点（debatable
node）**：由 MiroMind 实时研究，展示其推理与信源，正反两面都讲，开赛前锁定，并**公开打分**。我们不卖
“谁夺冠”的最终结论（一次研究≈市场共识，没有超额信息）；我们筛出**重要且有争议**的问题，并就此推理。

### 项目地图
见上方英文表格：`kickreason`（编排）· `miromind-research`（研究引擎）· `forecast-compiler`（节点编译）·
`forecast-grading`（校准打分）· `wc-data-library`（已打分的赛事数据集）。

### 证据等级（不造假的脊梁）
每个数值标注：**`REAL`**（计算/有据）· **`MODEL`**（如 Elo/538 基线）· **`MOCK`**（示意）。信源分 T1–T5。
模型或示意值绝不冒充真实；预测按**校准度**打分，而非简单胜负。

### 安全与边界
**不是“稳赚”产品**：一次研究≈市场共识，绝不承诺盈利；价值在于**公开可核验的准确率**与**可读的推理**。
**不做大规模抓取**：使用官方开放数据（StatsBomb）、免费 API（Guardian）与公开存档，遵守各自条款。
