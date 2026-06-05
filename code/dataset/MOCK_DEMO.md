# MOCK demo render — the 60s, as it appears on screen

Grounded in our REAL captured run `dataset/runs/wc26-usa-advance.json` (90% call, 100 real sources).
**REAL** = pulled from that run. **[MOCK]** = will be the live pipeline output (WF1) — labeled honestly, not faked.
Follows `CONTRACT.md`. One thread: CHAMPION graph → zoom to "Will the USMNT advance from Group D?"

---

### 0–8s · MiroMind generates the trace  *(REAL)*
> **Q: Will the USMNT advance from Group D at the 2026 World Cup?**
> `mirothinker-1-7-deepresearch` is researching…
> 🔎 41 web searches · 📄 32 pages read · reading **FIFA.com**, **ESPN**, **NYT/The Athletic**, **FIFA World Ranking**, **BetMGM/DraftKings**…

*(on screen: real source URLs streaming — fifa.com/…/group-d-focus, espn.com/soccer/…, nytimes.com/athletic/…)*

### 8–24s · The compiler extracts decision nodes from the trace  *(REAL evidence; extraction [MOCK] until WF1 lands)*
> Raw thinking → discrete, sourced **decision nodes**:

| node | judgment | dir | source (tier) |
|---|---|---|---|
| **seeding** | USA top seed (D1), FIFA #16 — highest-ranked in group | ▲ | FIFA ranking · usatoday (T1/T2) |
| **host-advantage** | all 3 group games effectively home (LA, Seattle, LA) | ▲ | FIFA.com Group D (T1) |
| **format-safety-net** | top-2 **+ 8 best 3rd-place** advance; ~4–5 pts often enough | ▲ | FIFA qualify/tie-breakers (T1) |
| **recent-form (H2H)** | 2025: lost Turkey 1–2, beat Australia 2–1, beat Paraguay 2–1 | ◼ | ESPN match · Boston Herald (T2) |
| **market-anchor** | BetMGM **–1000 (≈90.9%)**, DraftKings **–750 (≈88.2%)** | ▲ | NYT/Athletic (T2) |

### 24–34s · Nodes build the forecast graph  *(REAL number, computed from nodes)*
```
CHAMPION (2026)
  └─ … path …
     └─ USMNT advance Group D  →  90%   ◀ computed from the 5 nodes above (anchored to the –1000/–750 market)
```
> **One graph, three business views of the SAME nodes:**
> • **FAN:** "USA ~90% to reach the knockouts — home crowd in LA & Seattle, and a forgiving new 48-team format."
> • **ANALYST:** the 5 nodes above, each with its source — fully auditable.
> • **MOVING-LINE:** nodes ranked by value; market anchor –1000/–750; watch for the one that moves.

### 34–46s · A news event re-runs ONE node — the "doctor"  *([MOCK] update; live via `graph_build.py --update`)*
> ⚡ **BREAKING (Jun 9):** Pulisic limps out of training.
> → **recent-form / key-player node re-fires** → USMNT-advance **90% → 86%**
> → propagates up the CHAMPION graph (marked ⚠️ stale, re-aggregated)
> → **the betting market hasn't moved yet.** ← *the window where intel has value*

### 46–55s · Which node mattered? — value from 回溯 (backtest)  *(REAL past cases)*
> From `seed-resolved.json` (10 resolved results): the market was **87% on Argentina** before **Saudi Arabia beat them**; **68% on Germany** before **Japan beat them**. The headline number was worthless; the **signal that moved** was everything.
> → So we weight **live decision-node intel**, and grade every call **forward** against the **closing line (CLV)**.

### 55–60s · The proof / tagline
> **Every number traces to FIFA.com · ESPN · the betting market — locked before kickoff, graded after.**
> *"Predictions that show their work, keep score, and move before the market does."*
> proof badges: FIFA · Opta · Polymarket · ESPN · Pinnacle

---

**Status of this mock:** the *trace, sources, 90% number, market odds, and backtest cases are REAL* (from disk). The *node-extraction render and the live update are [MOCK]* — WF1 replaces them with the live pipeline, WF2 confirms the API can do the re-run fast enough. Nothing here is a faked accuracy claim.
