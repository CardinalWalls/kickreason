# Hero demo — a MOCKUP, on hold (not evidence)

> **Read this first.** This walkthrough hand-writes a reasoning trace for a *past* final. It is
> **not** a MiroMind output, and a real MiroMind run on a past match would be contaminated by
> lookahead certainty (it already knows Spain won). We also haven't run the real API yet. So this
> is only a sketch of what a demo *might* look like — a demo we can honestly build only by
> **forward-testing a live fixture**. See [README](README.md) and
> [../brainstorm/kickoracle/06-the-honest-reset.md](../brainstorm/kickoracle/06-the-honest-reset.md).

> *(Original framing below — kept as a visual sketch, not a claim.)* The pick: Spain to beat
> England in the **Euro 2024 final**. The bookmakers' pre-tournament favourite was **England**.
> Spain won 2-1.

This is the single match we dramatize on camera. Everything below is built from **past, already-resolved facts** in the knowledge base, so every number can be checked against a real source. One honesty note up front, repeated at the bottom: **the reasoning chain here is a *designed* illustration assembled from real, cited facts — it is NOT a live MiroMind run.** We use it to show what a good trace *looks like*; we separately decide later whether a real MiroMind trace is tight enough to show as-is (it tends to be slow and sprawling — see "Why this is a mock-up", below).

---

## 1. The event, and why it's the hero

**UEFA Euro 2024 final — Spain 2-1 England — Olympiastadion, Berlin — 14 July 2024.**
Goals: Nico Williams 47' (off a Lamine Yamal run), Cole Palmer 73' (equaliser off the bench), **Mikel Oyarzabal 86'** (winner, from a Cucurella cross). Spain became the first nation to win four European Championships.
Source: [Sky Sports report](https://www.skysports.com/football/news/26806/13176920/euro-2024-final-spain-2-1-england-mikel-oyarzabal-breaks-englands-hearts-as-spain-clinch-trophy), [Olympics.com](https://www.olympics.com/en/news/euro-2024-final-spain-beats-england-2-1-for-record-fourth-title).

Why this one is the hero, over the World Cup 2022 final and Copa América 2024 final (the two other candidates in the KB):

| Test | Euro 2024 final | Why it matters on camera |
|---|---|---|
| **Resolved cleanly?** | Yes — 2-1, a late legible winner (Oyarzabal 86') | No penalty-shootout asterisk; one team, one number, one ✓/✗ |
| **Was the favourite wrong?** | **Yes** — pre-tournament favourite was **England (+300)**; Spain were 4th-rated (+750) | The whole pitch is "a forecast that beats the public market." This is the cleanest gap. |
| **Visually legible?** | Yes — a final, a trophy, a famous 86th-minute winner | A 60s edit needs an image the room already recognises |
| **Recent + sourced?** | Yes — July 2024, every score/odd/factor sourced in the KB | We can defend every claim live |

> One subtlety to be honest about: by the **morning of the final**, Spain were the in-match favourite (~8/11, roughly 58% implied) because they'd been perfect all tournament. So on the *match line* a Spain pick agreed with the market. The gap we're really beating is the **pre-tournament tournament-winner futures**, where England were the favourite (+300) and Spain only fourth (+750). We say "pre-tournament favourite" on screen, not "underdog on the day" — the story is *the season-long line ranked England above Spain, and the research said Spain before the final*.
>
> **Be precise about what this is and isn't:** this is a *futures-gap* story (our pick vs a months-old tournament-winner price), **not** a closing-line CLV beat (our odds vs the sharp closing line on this match — which would have had Spain favoured). We do not own a real CLV number here; see the honesty box, §7. Sources: pre-tournament futures odds [CBS Sports](https://www.cbssports.com/soccer/news/euro-2024-futures-odds-best-bets-predictions-proven-soccer-expert-reveals-picks-to-win-teams-to-avoid/) (England favourite, Spain 4th); final-day odds (Spain ~8/11) [CBS Sports final preview](https://www.cbssports.com/soccer/news/spain-vs-england-prediction-odds-start-time-uefa-euro-2024-final-picks-july-14-bets-from-soccer-expert/). *(A Washington Post odds page cited in an earlier draft was dropped — it wasn't in our verified source set.)*

---

## 2. The locked question (frozen before kickoff)

This is the exact card we'd freeze at, say, **14:42 local, 14 July 2024**, before the 20:00 kickoff:

```
QUESTION  Who wins the Euro 2024 final, Spain vs England?
TYPE      single-choice (FutureX native type — match winner)
LOCKED    2024-07-14 14:42 CEST  ·  pick frozen, resolves after full time
ANSWER    SPAIN to lift the trophy
CONFIDENCE  ~58% at this lock  →  ~62% by kickoff
            (the PICK is frozen; the probability keeps updating with a
            sourced reason — see the "line moves" beat, §4)
```

What's locked and graded is the **pick** (Spain) and the **timestamp** — that's the falsifiable commitment. The probability is a living number: it reads ~58% here and ticks to ~62% by kickoff as team-news lands (§4). The "edge" being claimed is only the *pre-tournament futures* one (the season-long market ranked England above Spain) — **not** a closing-line CLV beat; on the match line Spain were already favoured.

> **How to check this:** the question is a single-choice "who wins" — the simplest FutureX question type (KB: FutureX answer formats include single-choice match-winner). It resolves on the official UEFA result. The locked timestamp is what makes the later ✓/✗ honest: the pick existed *before* the ball was kicked.

---

## 3. The reasoning chain we SHOW (the trace)

Each step is one beat of an analyst's — or a deep-research agent's — thinking: a thought, a source it would pull, and what that source says. Every fact and source here is from the KB. This is the chain we render on screen as "watch it think."

**Step 1 — Form: who actually arrived in better shape?**
*Pull:* UEFA / Wikipedia tournament record.
*Finding:* Spain came in **perfect, 6 wins from 6**, having beaten host Germany in the quarter-final (2-1 after extra time) and pre-tournament favourites France in the semi-final (2-1). England, by contrast, **stuttered out of Group C** (1-0 Serbia, 1-1 Denmark, 0-0 Slovenia) and needed late knockout drama to advance.
*Source:* [Euro 2024 final, Wikipedia](https://en.wikipedia.org/wiki/UEFA_Euro_2024_final); [Euro 2024 Group C, Wikipedia](https://en.wikipedia.org/wiki/UEFA_Euro_2024_Group_C); [Spain 2-1 Germany QF, Sky Sports](https://www.skysports.com/football/news/11095/13162892/euro-2024-spain-2-1-germany-aet-mikel-merinos-119th-minute-header-dumps-hosts-out-in-epic-quarter-final).
*Weight:* strong for Spain. → nudges the number toward Spain.

**Step 2 — Attacking output: who's been the more dangerous team?**
*Pull:* ESPN / tournament stats.
*Finding:* Going into the final Spain had **scored the most goals (13)** and **created the most chances (~96, up to and including the semi-final)** of any team in the tournament.
*Source:* [ESPN, Spain goals record](https://www.espn.com/soccer/story/_/id/40562354/spain-european-championship-goals-record-title); [Al Jazeera final preview](https://www.aljazeera.com/sports/2024/7/13/spain-vs-england-uefa-euro-2024-final-preview-team-news-start-time).
*Weight:* strong for Spain. → reinforces Spain.

**Step 3 — Key player availability: is the engine room intact?**
*Pull:* team-news / suspension tracker.
*Finding:* Rodri was anchoring the Spain midfield in player-of-the-tournament form (he was later named exactly that). And crucially — see the "line moves" beat below — **two suspended Spain starters, Dani Carvajal and Robin Le Normand, were available again for the final** after sitting out the semi.
*Source:* [ESPN final preview](https://www.espn.com/soccer/story/_/id/40524233/euro-2024-final-preview-spain-vs-england-key-players-predictions-tactics); [Football España, suspension report](https://www.football-espana.net/2024/07/05/spain-suspension-euro-2024-semi-final-france).
*Weight:* strong for Spain. → this is the step that earns the *upgrade* in Step 5.

**Step 4 — The market check: where is the public, and why might it be mispriced?**
*Pull:* pre-tournament odds vs final-day odds.
*Finding:* The **season-long line had England as the outright favourite (+300)** and Spain only fourth (+750) — that price was set before anyone saw Spain go 6-from-6 and England labour through the group. The eve-of-final price had already corrected toward Spain (~8/11), but the *tournament-winner* market we're beating still had England ahead of Spain.
*Source:* [CBS Sports pre-tournament futures](https://www.cbssports.com/soccer/news/euro-2024-futures-odds-best-bets-predictions-proven-soccer-expert-reveals-picks-to-win-teams-to-avoid/); [CBS Sports final-day odds](https://www.cbssports.com/soccer/news/spain-vs-england-prediction-odds-start-time-uefa-euro-2024-final-picks-july-14-bets-from-soccer-expert/).
*Weight:* this is the *edge* — but be precise: it's the gap vs the **season-long futures** price, not a beat of the match's closing line (Spain were the match favourite by kickoff). The form (Steps 1-3) points harder at Spain than the season-long line did. → lock **Spain**.

> **The one-line "why we picked Spain":** Spain were the only team to win every match, scored and created the most, had their midfield anchor in top form and their two suspended starters back — yet the season-long market still ranked England ahead of them. We side with the form.

---

## 4. The "line moves" beat (one concrete update)

Every demo needs one moment where **a piece of news arrives and the number should move** — that's what makes a *live researching* forecast different from a frozen formula.

- **The news (real, sourced):** In the run-up to the final, Spain confirmed that **Dani Carvajal and Robin Le Normand returned from suspension** — both had been forced to sit out the France semi-final and were now available to start the final.
  Source: [Football España](https://www.football-espana.net/2024/07/05/spain-suspension-euro-2024-semi-final-france), [ESPN final preview](https://www.espn.com/soccer/story/_/id/40524233/euro-2024-final-preview-spain-vs-england-key-players-predictions-tactics).
- **How the number should shift:** getting a first-choice right-back and a first-choice centre-back back for the biggest game *strengthens the side that was already favoured by form*. On screen we show the confidence ticking **up** — e.g. from **~58% → ~62%** for Spain — with the citation attached. The point isn't the exact two points; it's that **a real piece of lineup news moved a real number, with a source you can click.**

> **How to check this:** the suspension-and-return is documented in the cited team-news reports; the direction of the move (availability of two starters → small upgrade for the already-favoured side) is the obvious read. We are explicit on camera that the *magnitude* (≈4 points) is illustrative, not a measured CLV figure.

---

## 5. The outcome, and the grade

**Result: Spain 2-1 England.** Nico Williams 47', Palmer 73' (England equaliser), **Oyarzabal 86' winner**.
Source: [Sky Sports report](https://www.skysports.com/football/news/26806/13176920/euro-2024-final-spain-2-1-england-mikel-oyarzabal-breaks-englands-hearts-as-spain-clinch-trophy); [UEFA match page](https://www.uefa.com/uefaeuro/match/2036211--spain-vs-england/).

```
LOCKED CALL   Spain to win   (pick frozen 14:42, before 20:00 kickoff)
REAL RESULT   Spain 2-1 England  (Oyarzabal 86')
GRADE         ✓  CORRECT
MARKET NOTE   Season-long tournament-winner futures favoured England (+300), Spain 4th (+750);
              the locked pick beat that futures line. (NOT a closing-line CLV beat — Spain were
              the match favourite by kickoff.)
```

> This is the whole pitch in one frame: a sourced pick, frozen before kickoff, **graded ✓ against the real scoreboard** — and it disagreed with the season-long favourite and was right. The scoreboard is the grader; no human had to mark it. (KB design judgment: a match outcome is a *free, automatic ground-truth label* — the scoreboard annotates the trace.)

---

## 6. The 60-second storyboard (the "fancy illustration")

Shot-by-shot, what's on screen each beat. The visual job: make the **frozen formula → researched, sourced, graded forecast** contrast land instantly, and end on the green ✓.

| Time | On screen (illustration) | Voiceover |
|---|---|---|
| **0-6s** | A generic prediction card: "England 45% — confident number, no 'why', no track record." A small frozen-formula icon. | "Every prediction site hands you a confident number. None show you *why* — or whether they were right." |
| **6-14s** | Hard cut to our card. Fixture flips up: **SPAIN vs ENGLAND — Euro 2024 final**. A clock stamps **"Pick locked: SPAIN · 14:42, before kickoff."** | "So we locked a real call, before kickoff, and showed our work." |
| **14-26s** | The trace animates in, line by line, as if being researched live: **"form: Spain 6/6, beat Germany & France →"**, **"goals: most in the tournament, 13 →"**, **"Rodri anchoring, in top form →"** — each line drops a clickable source chip (ESPN, UEFA, Sky). | "It read the tournament the way an analyst would — Spain won every game, scored the most, beat the hosts and the favourites. Every line is a source you can click." |
| **26-36s** | **The line-moves beat.** A news ticker slides in: **"Carvajal + Le Normand back from suspension."** The confidence dial visibly ticks **58% → 62%** for Spain; the citation pins next to it. | "Then news lands — two starters back from suspension — and the number moves, with the receipt attached." |
| **36-44s** | Split screen: left = **"Season-long tournament-winner futures: ENGLAND favourite (+300), Spain 4th (+750)."** Right = **our locked pick: SPAIN.** A thin line connects them with the word **"we disagree."** | "The season-long futures still had England on top. We sided with the form, and locked Spain." |
| **44-54s** | Whistle. The scoreboard resolves: **SPAIN 2 - 1 ENGLAND**, "Oyarzabal 86'." A big green **✓** stamps over the locked card. | "Final whistle. Spain win it late. The call we froze before kickoff — correct." |
| **54-60s** | Cut to a Track Record strip: this ✓ joins a row of past resolved calls (the other KB fixtures), running tally visible. Logo + tagline. | "A number is a guess. A forecast you can audit — and then check — is intelligence." |

**Why it works in 60s:** the *streaming trace* is the wow (you watch it gather evidence), the *source chips* are the credibility, the *line-moves dial* shows it's researching and not frozen, and the *green ✓ against the real scoreboard* is the differentiator — the accuracy a frozen-formula competitor never publishes.

---

## 7. Honesty box — why this is a mock-up, and what we test next

- **This trace is a *designed* illustration.** Every fact and source is real and from the knowledge base, but the step order, the wording, and the exact confidence numbers (~58% at lock, the 58→62 move) were **authored by us for legibility** — they are not the output of a live MiroMind run.
- **The "beat the market" claim is a futures-gap, not CLV.** The only market our pick beat is the *pre-tournament tournament-winner futures* (England ahead of Spain). On this match's own line Spain were favoured by kickoff, so there is **no real closing-line CLV number here** — the dataset doesn't own one yet (see `questions.md` → "Not claiming we have a real CLV example yet"). Don't let the edit imply we beat a sharp closing line.
- **A real MiroMind run is slower and messier.** Verified live (KB): one multi-part question ran **9+ minutes**, with **77 web searches** and **~15,600 thinking steps**, and still hadn't finished at a ~560-second cap ("逻辑长征" — the logic long march). A raw trace is a firehose: lots of audit, not much speed or readability.
- **So the open question we test before filming:** can a real MiroMind trace, on a tight single-fact prompt, be cut down to ~5-8 clean steps that read like Section 3 — *or* do we run it async/pre-kickoff and distill the result into this readable explainer? KB design judgment leans toward the latter: use the trace as **source material for a distilled, source-checked explainer** (and keep the raw trace linkable behind it for audit), with a short **pre-recorded** highlight reel as the "watch it think" teaser — never a raw live multi-minute run on stage.
- **Net:** this file is the *target shape* of the on-screen artifact. The next task is to hold a real trace up against it and judge the gap.

> **How to check this whole doc:** open it, click any source, and confirm the score, the odds, and the factor. The only un-sourced things are explicitly flagged as illustrative (the exact confidence percentages and the size of the line move).
