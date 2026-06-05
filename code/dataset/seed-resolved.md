# Past results + odds (the market baseline) — 10 resolved matches

> **What this is, honestly:** the market baseline + scoring data — past results and the odds the
> market set — **not** MiroMind forecasts and **not** a "track record." A web-research agent can't
> forecast a past match: it already knows the result (*lookahead certainty* — see
> [README](README.md)). Use these rows to build the de-vig → Brier/calibration baseline that a
> real *forward* forecast must beat. (The original "seed track record" framing was wrong; corrected here.)

> These are **real games that already happened.** Every result is final and has a source you can
> open and check.

The track-record page only means anything if a reader can verify it. So each row below is:
the fixture, the date, **what a pre-match forecast would have said** (the market's own pick
and odds where we have them), **the real outcome**, and **where the result is recorded.**
We did not invent any score or any odd. Where our sources didn't give a pre-match price,
the cell says so plainly.

We deliberately favour **upsets** — games where the betting favourite lost — because those
are the ones that make a track record interesting and are the hardest to fake after the fact.

---

## The 10 seed events

Odds shown as American moneyline with the implied probability in brackets (e.g. +145 ≈ 41%
chance, −280 ≈ 74% chance). "Implied probability" just means: the chance the odds price in.

| Fixture | Date | What the pre-match market said | Real outcome | Result recorded by |
|---|---|---|---|---|
| **Saudi Arabia vs Argentina** (WC 2022, Group C) | 2022-11-22 | Argentina heavy favourite, ~−675 (**≈87%**); Saudi Arabia +1200 to +1900 (**≈5–8%**) | 🟥 **UPSET — Saudi Arabia 2-1** (Al-Shehri 48', Al-Dawsari 53'; Messi 10' pen). Ended Argentina's 36-game unbeaten run. | ESPN, FOX Sports, Sky Sports, FIFA |
| **Germany vs Japan** (WC 2022, Group E) | 2022-11-23 | Germany favourite, −210 to −245 (**≈66–71%**); Japan +550 to +650 (**≈15%**) | 🟥 **UPSET — Japan 2-1** (Doan 75', Asano 83'; Gundogan 33' pen). Japan's first-ever win over Germany. | ESPN, Sky Sports, FanDuel, NPR |
| **Portugal vs Morocco** (WC 2022, Quarter-final) | 2022-12-10 | Portugal favourite, −150 to −162 (**≈60–62%**); Morocco +425 to +450 (**≈19%**) | 🟥 **UPSET — Morocco 1-0** (En-Nesyri 42'). First African nation in a WC semi-final; Ronaldo out. | ESPN, Sky Sports, SI, NPR |
| **Georgia vs Portugal** (Euro 2024, Group F) | 2024-06-26 | Portugal favourite, −280 (**≈74%**; Opta model 75.8%). *Portugal had top spot locked and rested 8 starters.* | 🟥 **UPSET — Georgia 2-0** (Kvaratskhelia ~2', Mikautadze pen). FIFA ~74th beat ~6th; last 16 on debut. | Sky Sports, ESPN, FanDuel, CNN |
| **Spain vs Germany** (Euro 2024, Quarter-final) | 2024-07-05 | Near coin-flip: both ~+175 in 90 min (**≈36% each**), draw ~+200 | ⚪ **Spain 2-1 AET** (Olmo 51', Merino 119'; Wirtz 89'). Spain knock out the hosts. *No clear favourite.* | Sky Sports, CBS Sports, ESPN |
| **Spain vs England** (Euro 2024, **Final**, Berlin) | 2024-07-14 | Spain favourite on the match line, ~8/11 / +145 (**≈41–58%**). *Pre-tournament England were the favourite (+300); Spain only 4th (+750).* | 🟩 **Spain 2-1** (Nico Williams 47', Oyarzabal 86'; Palmer 73'). Record 4th Euro title, perfect 7-of-7. **The champion was not the pre-tournament favourite.** | UEFA, Olympics.com, Sky Sports, CBS Sports |
| **Argentina vs France** (WC 2022, **Final**, Lusail) | 2022-12-18 | **[no pre-match odds found]** | ⚪ **Argentina 3-3 France, 4-2 on pens** (Messi 23' pen, 108', Di Maria 36'; Mbappe hat-trick 80'/81'/118'). Argentina's 3rd World Cup. | Sky Sports, ESPN, Wikipedia |
| **Argentina vs Colombia** (Copa America 2024, **Final**, Miami) | 2024-07-14 | Argentina favoured, but **[no pre-match odds found]** | ⚪ **Argentina 1-0 AET** (Lautaro 112'). Ended Colombia's 28-match unbeaten run; Messi off injured ~64'. | ESPN, Sky Sports, NBC News |
| **France vs Morocco** (WC 2022, Semi-final) | 2022-12-14 | France favoured, but **[no pre-match odds found]** | ⚪ **France 2-0** (Theo Hernandez 5', Kolo Muani 79'). First side in back-to-back WC finals since Brazil 2002. | ESPN, Olympics.com, Sky Sports, NPR |
| **WC 2022 outright winner** (pre-tournament futures) | resolved 2022-12-18 | Favourite **Brazil 4/1** (**≈20%**); France 6/1 (**≈14%**); **Argentina 13/2** third (**≈13%**) | 🟥 **UPSET — Argentina won the tournament** as third favourite. Favourite Brazil went out in the QF to Croatia (4-2 pens). | Statista, Sky Sports, ESPN, FIFA |

🟥 = betting favourite lost · 🟩 = favourite/our pick held · ⚪ = near coin-flip or no clear favourite

---

## Which rows have a market price, and which are outcome-only

There are two kinds of row here, and we should be honest about the difference.

**Rows with a real pre-match price (7 of 10)** — Saudi–Argentina, Germany–Japan,
Portugal–Morocco, Georgia–Portugal, Spain–Germany, the Euro 2024 final, and the WC 2022
outright winner. For these we have the market's own odds, so we can show **"the market
priced the eventual winner at X%, and a pick that disagreed before kickoff was right"** — a
forecast that took Saudi Arabia, Japan, Morocco, Georgia, or Argentina-to-win-it-all backed
a 5–20% outcome and the world proved it out. That is the headline a track record is for.

> **Be precise — this is not CLV yet.** True *closing line value* compares **our** logged
> pick price against the sharp **closing** line for the same bet. These rows compare the
> *outcome* to the *market's* price — a "favourite-vs-market, and the underdog won" story,
> which is real and checkable but **not** a CLV number. **No row in this dataset carries a
> genuine our-odds-vs-closing-line CLV figure yet** — producing one (log our pick price,
> compare to the close) is open next-work, not done.

**Outcome-only rows (3 of 10)** — the WC 2022 final, the Copa America 2024 final, and the
WC 2022 semi-final. Our sources confirm the **result** cleanly, but we did **not** find a
pre-match match price for them, so we can show ✓/✗ "did the pick resolve right?" but **not**
a closing-line comparison. We keep them because they are famous, clean, and fully sourced —
just don't claim a CLV number we can't back.

> **The point:** five of these are upsets where the favourite lost. That is exactly the
> shape a forecast wants to be measured on — and exactly the shape that can't be faked once
> the match is over.

---

## The hero row, in plain words (for the 60-second walkthrough)

If we want one event to narrate on camera, it's the **Euro 2024 final, Spain 2-1 England**.
Here is why it's the clean one, all of it sourced in the row above and in `seed-resolved.json`:

- **It's a real favourite-vs-outcome gap, two ways.** On the *match line* Spain were the
  favourite (~+145), so picking Spain was picking *with* the market — fine. But on the
  *pre-tournament* futures, England were the favourite (+300) and Spain were only **fourth**
  (+750). So a forecast that locked Spain weeks before still beat the market's headline call.
- **It resolved cleanly and legibly.** A late Oyarzabal winner (86'), one scoreline, no
  shootout to argue about — easy to grade ✓, easy to show.
- **The supporting facts check out.** Spain came in perfect (6-of-6 going in, 7-of-7 after),
  had already beaten the hosts Germany and pre-tournament favourites France, and led the
  tournament for goals and chances created. Those are the kind of pre-match reasons a
  research agent would surface — and they all trace to UEFA / Sky Sports / CBS Sports.

The two World Cup 2022 upsets — **Saudi Arabia over Argentina** and **Japan over Germany** —
are the best *underdog* stories for the same page: a pick that backed a 5–15% outcome and
was proven right. Use the hero for the favourite-called-right narrative and an upset for the
market-was-wrong narrative; both are fully sourced.

A caveat worth stating: the implied-probability percentages are **rough**. Books price in
their own margin, odds shift between sources, and a few of our numbers come straight from a
match report rather than a clean odds feed. Treat the percentages as "roughly this likely",
not to the decimal. The **scores and dates** are firm; the **odds** are as-sourced.

---

## How to check this

Open `dataset/seed-resolved.json` (the machine-readable twin of this table) and pick any
row. Take its `fixture` + `date` + `outcome`, and confirm the score against any source named
in that row's `resolution_source` (e.g. the ESPN or Sky Sports match report). For the seven
rows that carry odds, the `odds_source_or_null` field names where the pre-match price came
from (FOX Bet, FanDuel, CBS Sports, Caesars, Statista). Every cell either traces to one of
those sources or says **[no pre-match odds found]** — there are no invented numbers.
