# THE INTEL DESK — how we think, and the standard we hold

*Our operating standard. Plain English. The point: we forecast the way professional intelligence analysts forecast — a calibrated number, named sources, the other side argued, and a score we publish afterward. This is the discipline behind our one-line wedge: **we publish our accuracy where the industry hides it.***

---

## 1. What separates a pro from an amateur

An amateur gives a hot take: "Brazil are looking unstoppable, they'll win it." It sounds confident, it cites nothing, it never gets checked, and next month nobody remembers it. A pro does four things instead. They **put a number on it** ("Brazil to win the group: likely, ~72%"), so the claim is precise enough to be right or wrong. They **name where the number came from** (official injury feed, the sharpest betting market, a named beat reporter), so a reader can audit it. They **argue the opposite on purpose** ("what would make this wrong?") before committing, so they don't just collect facts that flatter their first guess. And they **keep score out loud** — when the match resolves, they check the call against what actually happened and publish the result, win or lose. The number, the sources, the counter-case, and the scorecard are the whole difference. Everything below is just how to do those four things consistently.

---

## 2. The operating standard — 8 plain rules

These translate the formal intelligence rulebooks (ICD 203, Heuer's ACH, Kent, Tetlock, the NATO Admiralty source code) into plain desk rules. Each: **the rule** · why it matters · how MiroMind does it.

| # | Rule | Why it matters | How MiroMind does it |
|---|------|----------------|----------------------|
| 1 | **Put a number on it, not a word.** | "Good chance" means 75% to one reader and 30% to another. A real study (Kent, 1964) found professionals reading the *same word* anywhere from 20% to 80%. A number can't drift. | Every MiroMind call ends in a final judgement; we convert that into a percentage and a fixed band (see Section 3) instead of leaving it as prose. |
| 2 | **Keep "how likely" and "how sure" apart.** | "Likely" (the event) is not the same as "confident" (your evidence). A 70% call on a confirmed lineup is not a 70% call on one rumor. The intelligence rule (ICD 203) literally forbids putting both in the same sentence. | We print two separate fields: **likelihood** (the % the event happens) and **confidence** (high / moderate / low, driven by how good the sources were). Never blended. |
| 3 | **Rate every source.** | A trusted source can still pass along a shaky claim. You must rate *the source* and *the specific claim* separately, or a trusted name launders a weak fact. | Each page the call fetched gets a source tier (Section 4) and a corroboration check. A lone unconfirmed item is capped as provisional until a second *independent* source agrees. |
| 4 | **"Confirmed" means independent, not louder.** | Ten websites copying one wire story is **one** source, not ten. Echo is not corroboration (NATO Admiralty rule: confirmed = backed by *independent* sources). | The trace re-feeds the pages it read; we de-duplicate by origin before we ever say "multiple sources confirm." |
| 5 | **Argue the other side.** | The biggest trap is seeing only what fits your first guess (confirmation bias / mind-set). The cure (Heuer's ACH) is to list *every* plausible outcome first, then ask of each fact: which outcomes does this rule OUT? | We can prompt the call to lay out the full outcome set (home / draw / away, or "striker plays / rested / hidden injury") and rank by *least contradicted*, not most cheered-for. The call's own self-checking step is a built-in "what would make this wrong?" |
| 6 | **Use all the feeds, and name the gap.** | Pros use every relevant input and then say plainly what they *couldn't* see. Hiding the gap is how you get blindsided. | The trace shows exactly which pages were fetched and which weren't; when key info is missing (no confirmed lineup yet), we say so on the face of the forecast. |
| 7 | **Lead with the answer, then show the chain.** | A reader is short on time. Give the bottom line first, then the reasoning that supports it — and flag the contrary evidence too, don't bury it. | The call returns a final answer up front plus the full reasoning trace behind it; we surface the load-bearing facts, including the ones that cut against the call. |
| 8 | **Score yourself out loud, and say what moved the number.** | Vague forecasters hide so they're never provably wrong. Pros keep a time-stamped track record (Tetlock's Good Judgment Project proved scored, calibrated forecasters beat vague experts) and, when the number changes, they say exactly what changed it. | We grade past calls with a proper score (Brier) and Closing Line Value on a leakage-free 2022 backtest, and publish the calibration curve. When team news moves a number, the difference between the old trace and the new one *is* the "what changed" statement. |

**One rule we hold against ourselves:** don't hedge to stay safe. A cowardly 50/50 to avoid being wrong is its own failure (ICD 203 Standard 8: "should not avoid difficult judgments in order to minimize the risk of being wrong"). Commit to the hard call, and let the scorecard judge it.

---

## 3. How we express a forecast (the house style)

Every published forecast carries five parts, in this order:

1. **A number** (e.g. 72%)
2. **A band word** from one fixed scale (e.g. "likely")
3. **A give-or-take range** (e.g. 60–80%) — no false precision
4. **A confidence level** — separate sentence (high / moderate / low)
5. **The sources** and **what would change our mind**

We use one fixed word-to-number scale (the ICD 203 lexicon) so a word never drifts:

| Plain word | Means (probability) |
|---|---|
| almost no chance / remote | 1–5% |
| very unlikely | 5–20% |
| unlikely | 20–45% |
| roughly even chance | 45–55% |
| likely / probable | 55–80% |
| very likely | 80–95% |
| almost certain | 95–99% |

**Concrete World Cup example (the house style in one line):**

> **Argentina to beat Mexico in the group stage: likely, ~70% (range 60–80%). Confidence: moderate.**
> Why: Argentina rated clearly stronger on our 2022 Elo/SPI baseline; market agrees. *Moderate*, not high, because the starting XI isn't confirmed yet.
> Sources: official squad feed [tier 1]; sharpest market de-vigged close [tier 2]; named beat reporter on rotation rumor [tier 3, single-source, provisional].
> **What would change our mind:** Messi confirmed rested (would cut this toward roughly even); a back-line injury confirmed by a second independent source.

Notice: the number and the confidence are in **different sentences**, the range admits error, and the last line says exactly what we're watching.

---

## 4. How we rate a source

Two dials, rated **separately** (this is the NATO Admiralty method, plain): one for *how trustworthy the source is* over its track record, one for *how well this specific claim holds up*. A trustworthy source relaying a shaky claim still gets flagged — the good name does not auto-promote the weak fact.

**Source tier (trustworthiness):**

| Tier | Source | Example |
|---|---|---|
| 1 — Official feed | The original record / primary observer | Club or federation injury statement; the published team sheet |
| 2 — Sharp market | The crowd-corrected consensus price | Sharpest book's closing line, with the bookmaker margin stripped out |
| 3 — Named analyst | A reporter/analyst with a track record | A named beat reporter at the training ground |
| 4 — Pundit | Opinion, no special access | A TV panel "they look tired" take |
| 5 — Rumor | Anonymous / unconfirmed | A single anonymous social post |

**Claim credibility (this specific item):** confirmed by independent sources → probably true → possibly true → doubtful. A lone tier-3 rumor can only ever be "possibly true (provisional)" until a *second, independent* source agrees — then it becomes "confirmed."

**The plain idea behind the two dials:** *reliability* = "do I trust this source in general?"; *credibility* = "does this particular claim check out?" Keep them apart. And know your relayer: an official feed (primary) outranks a pundit *summarizing* that feed (secondary), even when both are "right."

One honest note about the market (tier 2): one good research pass usually just reproduces the de-vigged market price. That makes the market a **baseline to beat**, not proof we're right. Agreeing with the market is consensus, not edge.

---

## 5. The desk loop

Six steps, the same every time. Each maps to something the MiroMind trace already produces.

| Step | Plain meaning | What the MiroMind trace already gives us |
|---|---|---|
| 1. **Collect** | Pull every relevant feed; note what's missing. | One call autonomously web-searches and fetches pages; the trace lists exactly what it read (and, by absence, what it didn't). |
| 2. **Reason** | Work out what it means; separate fact from inference. | ~99.8% of the trace is *thinking* sitting next to a few fetches — the reasoning is right there to read, and we can tag each step as observed-fact vs. assumption vs. judgement. |
| 3. **Argue the other side** | List rival outcomes; find the fact that rules each out. | We prompt for the full outcome set and a consistent/inconsistent grid; the call's own step-by-step self-check is a built-in devil's advocate. |
| 4. **Put a number on it** | Convert the judgement to %, band, range, confidence. | We post-process the final answer into the fixed lexicon (Section 3), splitting likelihood from confidence. |
| 5. **Publish with sources** | Ship the call with a numbered, retrievable source list. | The call returns its sources; we render them as a tiered, de-duplicated list with a one-line "source summary." |
| 6. **Grade, then update** | Score the call after it resolves; say what moved the number when it moves. | We score on a leakage-free 2022 backtest (Brier + Closing Line Value) and publish the calibration curve; the ~6-minute post-news update lets us re-run on real team news and the trace-diff *is* the "what changed." |

**The honest boundary of the whole standard.** This discipline makes our forecasts *auditable and calibrated* — that is real and it is the thing competitors don't do. But it does **not** by itself make us beat the market. One call equals consensus; any edge claim has to be *measured* (Closing Line Value and Brier on a point-in-time backtest), never asserted — and it only lives in the narrow window after real news breaks and before the market corrects, never seconds-scale in-running. We hold ourselves to measuring it, not claiming it.
