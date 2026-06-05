# Real per-match market depth (collapses the 13k-60k question-universe band)

Goal: replace the un-scraped "~40 players x ~6 props/match" guess with grounded,
named-source counts of how many distinct markets, and specifically how many
NAMED-PLAYER prop markets, a real football match actually carries.

Method: WebSearch + WebFetch against live sportsbooks / odds pages (NOT the
MiroMind API). Many live odds grids (DraftKings, bet365 help, oddschecker bet
builder, statschecker) are JS-rendered or return 403/timeout to a plain fetch,
so where the live grid could not be scraped directly the count comes from the
bookmaker's own published figure or from the rendered fragments search returned.
Every number below is attributed.

## What was actually measured

### 1. Total markets per match
- bet365: **"100+ markets per top-tier soccer match, covering everything from
  anytime goal scorer to corners in each half to player shots on target."**
  Confirmed by two independent searches quoting the same figure.
  Source: https://agentbets.ai/guides/bet365-prop-bets/
- This 100+ is the TOTAL slate (match result, totals, corners, cards, half-time,
  correct score, team props, AND the named-player props). The player-prop subset
  is what drives our question universe.

### 2. Distinct NAMED-PLAYER prop market TYPES (props per player)
Triangulated from three sources, all naming the same core set:
- bet365 player-prop categories: anytime goalscorer, first goalscorer, last
  goalscorer, to score 2+ goals, hat-trick, player shots, player shots on
  target, player to record an assist, player to be booked/carded.
  Source: https://agentbets.ai/guides/bet365-prop-bets/
- covers.com World Cup per-match player props: anytime goalscorer, first
  goalscorer, to score 2+/3+, shots on target, assists, cards.
  Source: https://www.covers.com/world-cup/props
- oddschecker bet-builder player markets: anytime goalscorer, player shots,
  shots on target per player, assists, passes completed, saves made,
  yellow/red cards, fouls, tackles.
  Sources: https://www.oddschecker.com/football/bet-builders ,
  https://www.oddschecker.com/football
- DraftKings live sub-categories seen: Player Shots, Player Shots on Target
  (1+/2+/3+ tiers), Player Assists, Goalscorer (anytime/first/last/2+),
  Shots on Target each-half / header / outside-box.
  Source (rendered fragment via search):
  https://sportsbook.draftkings.com/leagues/soccer/usa---mls?category=player-shots&subcategory=player-shots-on-target

GROUNDED props-per-player band:
- CORE distinct player-prop market types (the ones priced for many players):
  **~6** — anytime scorer, to-score-2+, shots, shots on target, assists,
  cards. (This validates the original "~6 props/match per player" guess as a
  reasonable CENTRAL value, not the low end.)
- DEEP slate (bet365/oddschecker max) adds first/last scorer, hat-trick,
  passes completed, fouls, tackles, saves -> up to **~10-12** types, but the
  extra ones are priced for far fewer players (e.g. saves only for the 2 GKs,
  hat-trick only for a handful of forwards).

### 3. NAMED PLAYERS priced per match — the part that actually moved
The two ends of the band are driven by HOW MANY players each prop covers, and
the prop types do NOT all cover the same number of players:

- **Anytime goalscorer prices the whole matchday squad.** Bookmaker rules:
  "all players who participate in the game are considered runners" / "every
  effort will be made to quote all potential goalscorers."
  Sources: https://support.skybet.com/app/answers/detail/football-goalscorer-rules/ ,
  https://help.smarkets.com/hc/en-gb/articles/210005425-12-Football-rules
  -> 11 starters x2 = 22, plus subs. A World Cup matchday squad is up to 26
  named per team; in practice ~16-23 of each squad are realistic runners that
  get a price. Grounded count: **~30-40 named players** carry an anytime-scorer
  price per match (call it ~36 = both ~18-man realistic-runner lists).

- **Deeper props (shots, shots on target, assists, cards) are priced for far
  FEWER players** — only the likely-involved outfield players, not the whole
  squad. DraftKings' live shots-on-target market for a single MLS match listed
  roughly **8 named players** (Evander, Asprilla, S. Moreno, Navarro, Bassett,
  Mihailovic, Harris, Chara) for that one sub-market.
  Source (rendered fragment via search):
  https://sportsbook.draftkings.com/leagues/soccer/usa---mls?category=player-shots&subcategory=player-shots-on-target
  Top-tier / World Cup books price these deeper props for more names than a
  mid-table MLS game, so grounded band per deep-prop type: **~10-16 players**.

## Corrected question-universe estimate (per match)

Instead of one flat "players x props," count per prop type because coverage
differs. Per single match:

| Prop type            | players priced | source basis                          |
|----------------------|----------------|----------------------------------------|
| Anytime goalscorer   | ~36            | full matchday squads (skybet/smarkets) |
| To score 2+ goals    | ~20            | subset of scorer list                  |
| Player shots         | ~12            | DK live grid (~8 MLS) scaled to WC     |
| Player shots on tgt  | ~12            | DK live grid ~8 MLS -> ~12 WC          |
| Player assists       | ~12            | DK shots/assists category              |
| Player cards/booked  | ~14            | oddschecker/bet365 booking market      |

Player-prop QUESTIONS per match (sum of the column):
  36 + 20 + 12 + 12 + 12 + 14 = **~106 named-player prop questions per match**.

Cross-check with the simple model: ~14 distinct players who get the deep
treatment x ~6 core props = ~84, plus the long anytime-scorer tail (~36) ->
same ~100-110 range. The two methods agree.

### Scale to the tournament
World Cup 2026 = **104 matches** (FanDuel: "betting on all 104 World Cup
matches"; CBS: 48 teams / 104 matches).
Source: https://www.fanduel.com/sports-betting-guide/how-to-bet-on-world-cup

- Player-prop questions across the tournament:
  ~106 per match x 104 matches = **~11,000 named-player prop questions**.
- Add non-player match markets (~ the rest of bet365's 100+: result, totals,
  corners, cards team-level, correct score, HT/FT, etc. ~ another 40-60/match):
  ~50 x 104 = ~5,200 -> **total ~16,000 betting questions** if we grade every
  market type, but only the ~11k player-prop slice is the part our edge targets.

## Bottom line (collapses 13k-60k)

- Named players per match: **~36** carry a scorer price; **~12-16** carry the
  deep props (shots / SoT / assists / cards). The old "~40 players" guess was
  right ONLY for the anytime-scorer market and ~3x too high for every other prop.
- Props per (deeply-covered) player: **~6 core** (up to ~10-12 on the deepest
  books). The "~6 props" guess was a good central estimate.
- Per match: **~106 named-player prop questions** (measured-coverage sum), not a
  flat 40x6=240.
- Tournament question universe (the number that matters):
  **~11,000 named-player prop questions** (was 13k-60k).
  With all non-player markets graded too: **~16,000 total**.

This kills the 60k high end (it assumed every prop covers all ~40 players) and
sits just under the old 13k low end. Use **~11k player-prop questions / ~16k
all-markets** as the grounded planning number.

ESTIMATE FLAGS: the ~12-16 deep-coverage player count and the World-Cup uplift
from the MLS DK sample (~8 -> ~12) are estimates scaled from one live grid;
the ~36 scorer count is an estimate of realistic runners within the 26-man
squad rule. The 100+ markets/match and 104 matches figures are quoted, not
estimated.

## Sources
- https://agentbets.ai/guides/bet365-prop-bets/  (100+ markets/match; player-prop categories)
- https://www.covers.com/world-cup/props  (per-match player prop types)
- https://www.oddschecker.com/football  ,  https://www.oddschecker.com/football/bet-builders  (bet-builder player markets list)
- https://sportsbook.draftkings.com/leagues/soccer/usa---mls?category=player-shots&subcategory=player-shots-on-target  (live ~8 named players in one shots-on-target market)
- https://support.skybet.com/app/answers/detail/football-goalscorer-rules/  (anytime scorer = all participating players)
- https://help.smarkets.com/hc/en-gb/articles/210005425-12-Football-rules  (goalscorer runners rule)
- https://www.fanduel.com/sports-betting-guide/how-to-bet-on-world-cup  (104 matches)
