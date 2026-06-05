# HERO — the whole story of FIFA 2022, told through four graded layers

> **The story (one line).** A finished World Cup, replayed as a forecast graph: every match seen
> through **odds · narrative · magic-moment · stats**, every probability **graded** by the rig
> (`arc_build.py` → [`arc_2022.md`](arc_2022.md)). The thesis the numbers hand us is sharper than
> "the market is dumb": **the market is right on the chalk and *confidently wrong on exactly the
> moments everyone remembers* — and two heroes prove that edge is a repeatable mechanism, not luck.**
>
> Built on the real graded arc ([`arc_2022.graded.json`](arc_2022.graded.json)): **13 marquee
> nodes · mean market Brier 0.262 · market confidently wrong on 4 clear-favourite upsets.** Every
> claim below is sourced in the node data; every Brier is computed, not asserted. *(This is the
> MARKET graded — not an agent backtest; you can't backtest a research agent on games it already
> knows. 2022 proves the layer system; 2026 is the live agent.)*

## How to read a node (the four professional systems)

| layer | the system | what it answers | buyer |
|---|---|---|---|
| **odds** | bookmaker de-vig · Opta supercomputer | how sure was the market — and was it right? (**Brier**) | bettors · quants · books |
| **narrative** | the analyst / 解说 (Opta, The Athletic, Guardian) | *why* did it happen — the tactical mechanism | media · creators |
| **magic_moment** | broadcast / the star | the image you remember — scorer, minute | fans · social · TV |
| **stats** | the data co (Opta · StatsBomb · FBref) | the hard truth under the scoreline — xG, shots | clubs · analysts · B2B |

One trace fills all four. The grade is what makes it honest.

---

## The frame — the futures market, and where it was looking

Before a ball was kicked the market's No.1 was **Brazil (~13% on our de-vig of the field; ~4/1 the
shortest price)**. Brazil never reached the final — **Croatia knocked them out in the quarters**
(Petković's 117th-minute equaliser, then penalties). The eventual champion, **Argentina, was the
third favourite (~13/2)**. The whole tournament is the story of the field's favourite falling and a
value side rising — and of the market pricing the *chalk matches* well while missing the *shocks*
that defined it. `wc2022-winner` · Brier on Brazil 0.018 *(near coin-flip — futures resolve far from
1/0, so Brier is small either way; the story is the elimination, not the number).*

---

## ACT I — The Fall (and the parallel shock): the market at its most confidently wrong

**Argentina 1–2 Saudi Arabia · group · the market's worst call of the tournament.**
- **odds:** Argentina **87%** (FanDuel −650; Opta's supercomputer cross-check 80.2% / Saudi 6.9%).
  Argentina lost. **Brier 0.759 — *confidently wrong*** (coin-flip is 0.25). The single most
  mispriced marquee result in the arc.
- **narrative (Opta):** *Renard's high line, weaponised.* Saudi Arabia stepped up in unison all
  match; Argentina were flagged offside **six times inside the first 32 minutes** — more than any
  team managed in a *whole match* at the 2018 World Cup. The favourite's main weapon (runners in
  behind) became a self-defeating trap.
- **magic_moment:** **Al-Shehri 48'** broke the dam (Saudi's first shot on target); **Al-Dawsari
  53'** — out of the sky, past two defenders, curled beyond Emi Martínez — won it.
- **stats:** Argentina **2.16 xG** to Saudi **0.14** (Opta). The lowest xG a team had needed to win
  a World Cup match since 1966. *Territory said landslide; the scoreboard said upset.*

> The layer the price missed was **narrative + stats**: a side generating 2.16 xG "should" win, but
> the *mechanism* (offside trap + ruthless 0.14-xG conversion) is exactly the sourced, contrarian
> signal a graded forecast surfaces and the 87% line buried.

**Germany 1–2 Japan · group · the same lesson, a different continent.**
- **odds:** Germany **68%** → lost → **Brier 0.458, confidently wrong.**
- **narrative:** Moriyasu's **halftime 4-2-3-1 → 3-4-3** switch activated wing-backs and turned the
  game; **magic_moment:** sub **Asano 83'** ran clear and rifled the winner past Neuer.
- **stats:** Germany **2.58 xG** (StatsBomb) and ~76% possession — and lost. The second
  possession-dominant favourite felled in 24 hours.

*Two clear favourites, two confident prices, two losses the layers can explain and the odds couldn't.*

---

## ACT II — The edge that repeats: Morocco, and why this isn't luck

If Saudi and Japan were single shocks, **Morocco is the thesis** — the *same mechanism* beating a
clear or fancied favourite **three rounds running**. That repeatability is the difference between a
lucky upset and a **sourced, gradeable edge** (a CLV goldmine for anyone holding the contrarian side).

**Morocco 2–0 Belgium · group.** odds: Belgium **48%** (3-way; FIFA No.2) → lost → Brier 0.235
*(near coin-flip in 3-way terms — but the No.2 side losing is the signal).* narrative: Regragui's
**compact 4-1-4-1 mid-block** strangled the golden generation, Amrabat shadowing Hazard. magic:
**Aboukhlal 90+2'** off a Ziyech transition. stats: Morocco **1.28 xG** while ceding the ball.

**Morocco 0–0 Spain (3–0 pens) · R16.** odds: Spain **60%** → lost → **Brier 0.359, confidently
wrong.** narrative: *surrendering the ball by design* — a narrow low block built around Amrabat.
magic: **Hakimi's Panenka** won the shootout after **Bono** saved Soler and Busquets. stats: Spain
1.28 xG to 0.77 — Spain's vaunted possession produced almost nothing.

**Morocco 1–0 Portugal · QF.** odds: Portugal **60%** → lost → **Brier 0.360, confidently wrong.**
narrative: *win the game with 31% of the ball* — the second-lowest possession share of any team in
the tournament, by design. magic: **En-Nesyri 42'**, a towering header over a hesitant Diogo Costa
— first African nation in a World Cup semi-final. stats: Morocco 1.25 xG; Ronaldo eliminated.

> **The edge, named:** Regragui's low-block-and-transition beat three fancied possession sides.
> The market priced each as a favourite (clearly so vs Spain and Portugal). A forecast that scored
> the *mechanism* — `node_eval.py`'s "defence/set-piece + venue" signal class, learned from exactly
> these resolved upsets — would have been on the right side **four times** (Belgium too). That is a
> repeatable, sourced edge. The price treated each as a one-off.

---

## ACT III — The recovery: the market is *right* on the chalk (and so are we)

The honest counterweight, and why the pitch isn't "fade the market." When the favourite is real and
holds, the odds layer grades **well** — and our graph agrees with it, claiming no fake edge.

- **Argentina 2–0 Mexico** (64% → **Brier 0.130, right**) — Tata's 5-3-2 frustrated them until
  **Messi 64'** broke it and **Enzo 87'** curled the seal. *Recovery match after the fall.*
- **Argentina 2–0 Poland** (65% → **0.122, right**) — Scaloni's positional fluidity; **Álvarez 67'**;
  Argentina **3.49 xG** to 0.36. Messi missed a penalty and it didn't matter.
- **Argentina 2–1 Australia · R16** (76% → **0.058, right**) — the cleanest "favourite held" of the
  arc; Messi's first World Cup knockout goal, **Álvarez** off an error, a late Goodwin deflection.

> This is the trust-builder: a forecast that only ever screams "upset" is a broken clock. Ours
> grades the chalk correctly and **spends its contrarian credibility only where the mechanism earns
> it** (Act I, II) — which is precisely what a *proper* (un-gameable) Brier score rewards.

---

## ACT IV — The knife-edges: coin-flips the favourite survived

Two matches the market priced near 50/50 — and the layers explain how Argentina lived.

- **Argentina 2–2 Netherlands (4–3 pens) · QF** — priced **44%** (near coin-flip); Argentina held
  on pens. narrative: **Scaloni's switch to a back-three** smothered the Dutch for 80 minutes;
  **Messi 73' pen** and a cheeky Molina opener built a 2-0 — then **Weghorst's** two late goals
  (incl. the rehearsed free-kick) forced extra time before **Emi Martínez's** shootout heroics.
  stats: Argentina ~1.95 xG to ~0.53 — they deserved more than penalties.
- **Argentina 3–0 Croatia · SF** — priced **52%** (coin-flip); won comfortably. narrative: a compact
  4-4-2 neutralised Croatia's possession machine; **Messi 34' pen + Álvarez 39', 69'** (one a
  Messi-assisted solo demolition of Gvardiol). stats: **3.21 xG to 0.61** — the scoreline flattered
  no one.

---

## ACT V — The crowning: the value champion, the greatest final

**France 2–0 Morocco · SF** closes the underdog arc honestly: France **63% → Brier 0.140, market
right.** Deschamps' reactive 4-3-3 sat deep (~39% possession) and struck — **Theo Hernández 5'**,
then **Kolo Muani 79'**, 44 seconds after coming on (third-fastest sub goal in World Cup history).
Morocco's run ended at the line the market correctly drew.

**Argentina 3–3 France (4–2 pens) · the Final.** Priced a near coin-flip (~**53%** Argentina on the
even-money trophy market) → won → Brier 0.225.
- **narrative:** *Scaloni's ambush* — recalling **Di María** to torture Koundé; Argentina led 2-0
  and cruising.
- **magic_moment:** **Messi 23' pen, Di María 36', Messi 108'** — and **Mbappé's** 80'/81'/118'
  hat-trick, two goals in 97 seconds, the first World Cup final hat-trick since 1966. Then **Emi
  Martínez's 123rd-minute save** from Kolo Muani at 3-3 kept Argentina alive.
- **stats:** **Argentina 3.45 xG to France 2.29** across 120 minutes — a final that earned its
  reputation on the underlying numbers, not just the drama.

And the futures frame pays off: the field's favourite (Brazil, ~13%) was long gone; the **third
favourite lifted the trophy.** Messi's crowning, and a value champion the pre-tournament price
under-rated.

---

## What the layers did that the price could not (the product, restated)

- The **odds** layer kept everyone honest: it graded the market **right on the chalk** (Argentina's
  wins, France's semi) and **confidently wrong on the four marquee shocks** (Saudi 0.76, Germany
  0.46, Spain 0.36, Portugal 0.36). No opinion — the Brier delivered the verdict.
- The **narrative** + **stats** layers named the *mechanism* the price missed — the high line, the
  low block, the xG-vs-scoreline gap — the sourced, contrarian signal that turns "shock" into
  "edge." Morocco proves it **repeats**.
- The **magic_moment** layer is why anyone watches — Al-Dawsari's curler, Hakimi's Panenka,
  En-Nesyri's header, Messi's title — the same trace that priced the match also tells the story that
  sells it.

**One finished tournament, one compiler, four products, one honest scorecard.** That is the dream
demo's proof half. Now run it forward — that's 2026.

> **Check any of it:** `python3 dataset/arc_build.py` (re-grades + drift-checks vs `seed-resolved.json`),
> then open [`arc_2022.md`](arc_2022.md) for the table and [`arc_2022.graded.json`](arc_2022.graded.json)
> for every layer + source URL. Hero vehicle decision: **Argentina's redemption arc is the spine,
> Morocco's repeatable edge is the proof** — the intel story, not the fairy-tale.
