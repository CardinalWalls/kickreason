# The Dream Demo — two artifacts

> **The split (decided):**
> - **WEBPAGE = World Cup 2026 (live product).** Forward-looking; the forecast that updates before kickoff. No result needed. → `demo.html`
> - **VIDEO = World Cup 2022 (past, complete, graded).** The 60s shows the whole loop *including the grade* — which needs resolved results. 2022 is complete + amazing (Saudi stun Argentina, Morocco's run, Messi's final) and we have the data + Brier scores.
> - **Arc:** prove it on a finished tournament (2022, graded) → *"now it's live for 2026"* (cut to the webpage). **Past = proof · future = product.**

## The layer model (the professional spine — applies to both)
One MiroMind trace → the compiler extracts every layer; each is a product for a different professional/buyer. Every node carries a `layer`.

| layer | what | system behind it | buyer |
|---|---|---|---|
| **magic_moment** | the star · the drama · the turning point | highlights / broadcast / the star | fans · social · broadcasters |
| **narrative** | the storyline — *why* | the 解说 / commentator / reporter / pundit | media · creators · engaged fans |
| **odds** | the calibrated probability | the prediction system (bookmaker · Opta · markets) | bettors · quants · sportsbooks |
| **stats** *(etc.)* | the underlying data & pattern | data cos / scouts (Opta · StatsBomb) | clubs · analysts · B2B |

**The moat:** four separate industries today — produced from ONE trace, sourced, graded, consistent.

---

## THE VIDEO — 60s, base = World Cup 2022 (complete, graded)
Title cards (0–6s):
1. **WE GRADED AN ENTIRE WORLD CUP.**
2. **NOT ONLY THE SCORELINE — THE KEY NARRATIVE.**
3. **THEN WE BUILT IT LIVE FOR 2026.**

| t | beat | on screen | asset · status |
|--|--|--|--|
| 0–6 | title cards | the 3 cards | dream deck · ⏳ assemble |
| 6–22 | **the magic moment, three layers deep** | **Al-Dawsari's 53' goal — Saudi 2–1 Argentina (2022)** → **narrative** (offside line, blanked attack) → **odds**: the prediction system said **87% Argentina** → **graded WRONG, Brier 0.76** | `narrative-sau-arg-2022` (🔄) + `golden.html`/`GOLDEN.md` (✅) + scorer/minute in `seed-resolved.json` (✅) |
| 22–34 | the reasoning replays → compiles into nodes (tagged by layer) | live trace streaming → sourced nodes | `walkthrough.html` sc.2–3 (✅) |
| 34–44 | evaluated in different views (the layers as products) | fan / analyst / moving-line | `views.py` / `demo.html` (✅) |
| 44–52 | **more 2022 receipts, graded** | Germany 68%→Japan, Portugal 60%→Morocco · **mean market Brier 0.49 — confidently wrong** | `GOLDEN.md` table (✅) |
| 52–60 | **"now it's live for 2026"** | cut to the webpage: the 2026 forecast that moves before the market | `demo.html` (✅) |

## THE WEBPAGE — World Cup 2026 (live product)
Title: **PREDICT EVERY MATCH OF THE WORLD CUP 2026 · BUILT FOR THE WHOLE TOURNAMENT.**
The live loop on a forward fixture (USMNT advance): trace → nodes → 3 views + steering → injury (unpriced) → 91%→88% below the frozen line. No grade needed (forward); the *2022 video* is the proof that the method works. → `demo.html` (✅) + `walkthrough.html` (✅)

---

## Material inventory
- **Title cards** (video 2022 arc + webpage 2026) — ⏳ build into the dream deck
- **Magic-moment layer (2022)** — ✅ scorers/minutes in `seed-resolved.json`; surface as `layer:magic_moment` nodes
- **Narrative layer** — 🔄 `narrative.py` fetching (`narrative-sau-arg-2022` for the video, `narrative-usa-advance` for the webpage) → `layer:narrative` nodes (also breaks the monoculture)
- **Odds layer + grade** — ✅ `golden.html`/`GOLDEN.md` (2022 Brier table), `baseline.py`, de-vig nodes
- **Loop replay** — ✅ `walkthrough.html`, `demo.py`
- **3 views + steering** — ✅ `demo.html`
- **Whole-tournament graph** — ✅ slice in `graph.json`
- **Proof of API use** — ✅ `API_USAGE.md` (34 calls · 12.1M tokens · 1,655 sources · 7×429)
- **Assembled dream deck** — ⏳ assemble when narrative grain lands (2022 video arc, layer-stacked magic moment, → 2026 webpage)

## Honest scope note
The video grades the **marquee resolved 2022 cases** we have (the famous upsets + the final) — not literally all 64 matches. "Every match / whole tournament" is the **product ambition**, shown by the **2026 webpage + the graph**, not a claim that we already graded all of 2022.
