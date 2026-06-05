#!/usr/bin/env python3
"""
gen_questions_2022.py — the REAL question universe for the 2022 FIFA World Cup, at scale.

Deterministically enumerates the actual 2022 tournament (8 groups, 32 real teams, 64 real
matches) into the full prediction-question universe — futures, group standings, per-team
progression, per-match markets, and per-match player props — and flags the VALUABLE subset
(the few thousand that carry SEO/market value) vs the long tail. Because 2022 is resolved,
the marquee questions also carry their real ANSWER (gradable).

NO fabricated player names: real stars are named; squad depth is honest numbered slots.

Run:  python3 dataset/gen_questions_2022.py
Out:  dataset/questions_2022.json (full universe) + dataset/questions_2022.counts.json
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

# ---- the REAL 2022 World Cup structure ----
GROUPS = {
    "A": ["Qatar", "Ecuador", "Senegal", "Netherlands"],
    "B": ["England", "Iran", "USA", "Wales"],
    "C": ["Argentina", "Saudi Arabia", "Mexico", "Poland"],
    "D": ["France", "Australia", "Denmark", "Tunisia"],
    "E": ["Spain", "Costa Rica", "Germany", "Japan"],
    "F": ["Belgium", "Canada", "Morocco", "Croatia"],
    "G": ["Brazil", "Serbia", "Switzerland", "Cameroon"],
    "H": ["Portugal", "Ghana", "Uruguay", "South Korea"],
}
TEAMS = [t for g in GROUPS.values() for t in g]   # 32

# Real notable players (verifiable) — used for the VALUABLE player props.
STARS = {
    "Argentina": ["Lionel Messi", "Julian Alvarez", "Lautaro Martinez", "Angel Di Maria"],
    "France": ["Kylian Mbappe", "Olivier Giroud", "Antoine Griezmann", "Ousmane Dembele"],
    "Brazil": ["Neymar", "Vinicius Junior", "Richarlison", "Raphinha"],
    "England": ["Harry Kane", "Bukayo Saka", "Marcus Rashford", "Raheem Sterling"],
    "Portugal": ["Cristiano Ronaldo", "Bruno Fernandes", "Joao Felix", "Goncalo Ramos"],
    "Netherlands": ["Memphis Depay", "Cody Gakpo", "Davy Klaassen"],
    "Spain": ["Alvaro Morata", "Ferran Torres", "Dani Olmo"],
    "Morocco": ["Hakim Ziyech", "Youssef En-Nesyri", "Sofiane Boufal"],
    "Croatia": ["Luka Modric", "Andrej Kramaric", "Ivan Perisic"],
    "Poland": ["Robert Lewandowski"],
    "Saudi Arabia": ["Salem Al-Dawsari", "Saleh Al-Shehri"],
    "Japan": ["Ritsu Doan", "Takuma Asano"],
    "Germany": ["Kai Havertz", "Serge Gnabry", "Jamal Musiala"],
    "Senegal": ["Sadio Mane"],
    "Uruguay": ["Darwin Nunez", "Luis Suarez"],
    "USA": ["Christian Pulisic", "Tim Weah"],
}

# Real resolved answers for the marquee questions (from seed-resolved + history).
RESOLVED = {
    "winner": "Argentina", "runner_up": "France", "golden_boot": "Kylian Mbappe (8)",
    "final": "Argentina (won on penalties vs France)",
}
RESOLVED_MATCH = {  # famous upsets we have graded
    "Saudi Arabia vs Argentina": "Saudi Arabia won 2-1 (upset; market ~87% Argentina)",
    "Germany vs Japan": "Japan won 2-1 (upset; market ~68% Germany)",
    "Portugal vs Morocco": "Morocco won 1-0 (upset; market ~60% Portugal)",
    "Argentina vs France": "Argentina won (final, on penalties)",
    "France vs Morocco": "France won 2-0 (semi-final)",
}

# per-match core (non-player) markets — real bookmaker market types
CORE_MARKETS = (
    ["match result (1X2)", "double chance", "draw no bet", "both teams to score"]
    + [f"over/under {x} goals" for x in (0.5, 1.5, 2.5, 3.5, 4.5)]
    + [f"home team over/under {x}" for x in (0.5, 1.5, 2.5)]
    + [f"away team over/under {x}" for x in (0.5, 1.5, 2.5)]
    + [f"correct score {h}-{a}" for h in range(4) for a in range(4)]   # 16
    + ["HT/FT result", "half-time result", "total goals odd/even",
       "home win to nil", "away win to nil", "home clean sheet", "away clean sheet",
       "over/under 9.5 corners", "over/under 3.5 cards", "first team to score"]
)
PLAYER_PROPS = ["anytime goalscorer", "first goalscorer", "to score 2+",
                "shots over/under", "shots on target o/u", "to be carded", "anytime assist"]


def matches():
    """The real 64: 48 group + 16 knockout (slots for KO, real fixtures for groups)."""
    out = []
    for g, teams in GROUPS.items():
        for i in range(len(teams)):
            for j in range(i + 1, len(teams)):
                out.append({"stage": f"Group {g}", "home": teams[i], "away": teams[j]})
    ko = [("Round of 16", 8), ("Quarter-final", 4), ("Semi-final", 2),
          ("Third place", 1), ("Final", 1)]
    for stage, n in ko:
        for k in range(n):
            out.append({"stage": stage, "home": f"{stage} winner slot {2*k+1}",
                        "away": f"{stage} slot {2*k+2}"})
    return out


def gen():
    Q = []
    def add(cat, layer, subject, market, valuable, resolved=None, **extra):
        rec = {"id": f"q{len(Q)+1:05d}", "category": cat, "layer": layer,
               "subject": subject, "market": market, "valuable": valuable,
               "resolved": resolved}
        rec.update(extra)
        Q.append(rec)

    # 1. FUTURES (valuable; resolved)
    for m, r in [("Tournament winner", RESOLVED["winner"]),
                 ("Top scorer / Golden Boot", RESOLVED["golden_boot"]),
                 ("Reach the final", None), ("Reach the semi-final", None),
                 ("Golden Glove", None), ("Best young player", None),
                 ("Dark horse", None), ("Group of death", None)]:
        add("futures", "odds", "World Cup 2022", m, True, r)
    for t in TEAMS:                                   # per-team outright
        add("futures", "odds", t, "to win the World Cup", True,
            "won" if t == RESOLVED["winner"] else "no")

    # 2. GROUP STANDINGS (mostly valuable)
    for g, teams in GROUPS.items():
        for t in teams:
            for pos in ["win the group", "to qualify (top 2)", "to finish bottom"]:
                add("group", "odds", t, f"Group {g}: {pos}", True)
        for h in teams:                               # exact-order is long tail
            add("group", "odds", f"Group {g}", f"exact standings incl {h} 1st", False)

    # 3. PER-TEAM PROGRESSION (valuable)
    for t in TEAMS:
        for stage in ["advance from group", "reach R16", "reach QF", "reach SF",
                      "reach final", "win it"]:
            add("progression", "odds", t, stage, True)

    # 4. PER-MATCH markets + player props
    for mt in matches():
        fixture = f"{mt['home']} vs {mt['away']}"
        is_real = not mt["home"].endswith("slot 1") and "slot" not in mt["home"]
        res = RESOLVED_MATCH.get(fixture)
        # core markets: 1X2 + a few are valuable, rest long-tail
        for mk in CORE_MARKETS:
            val = mk in ("match result (1X2)", "both teams to score",
                         "over/under 2.5 goals", "first team to score")
            add("match_core", "odds", fixture, mk, val and is_real,
                res if mk == "match result (1X2)" else None,
                stage=mt["stage"], magic_layer=("magic_moment" if res else None))
        # player props: real STARS = valuable; squad depth = honest slots, long tail
        for side in (mt["home"], mt["away"]):
            named = STARS.get(side, [])
            for p in named:
                for prop in PLAYER_PROPS[:3]:        # scorer props for stars = valuable
                    add("player_prop", "narrative" if prop == "anytime goalscorer" else "stats",
                        side, f"{p} — {prop}", True, stage=mt["stage"], player=p, fixture=fixture)
                add("player_prop", "stats", side, f"{p} — shots on target o/u", True,
                    player=p, fixture=fixture)
            # squad-depth slots to realistic scorer-runner count (~18/side) — long tail
            for s in range(len(named) + 1, 18):
                add("player_prop", "stats", side, f"squad player #{s} — anytime goalscorer",
                    False, fixture=fixture, slot=True)
            for s in range(len(named) + 1, 13):       # deep props for ~12 players/side
                for prop in ("shots o/u", "to be carded"):
                    add("player_prop", "stats", side, f"squad player #{s} — {prop}",
                        False, fixture=fixture, slot=True)

    return Q


def main():
    Q = gen()
    from collections import Counter
    cats = Counter(q["category"] for q in Q)
    layers = Counter(q["layer"] for q in Q)
    valuable = sum(1 for q in Q if q["valuable"])
    resolved = sum(1 for q in Q if q["resolved"])
    named = sum(1 for q in Q if q.get("player") and not q.get("slot"))
    slots = sum(1 for q in Q if q.get("slot"))

    counts = {"total": len(Q), "valuable": valuable, "resolved_marquee": resolved,
              "by_category": dict(cats), "by_layer": dict(layers),
              "named_player_props": named, "squad_slot_props (honest long tail)": slots,
              "matches": len(matches()), "teams": len(TEAMS), "groups": len(GROUPS)}

    json.dump(Q, open(os.path.join(HERE, "questions_2022.json"), "w"), indent=0)
    json.dump(counts, open(os.path.join(HERE, "questions_2022.counts.json"), "w"), indent=2)

    print("=" * 60)
    print("  REAL 2022 WORLD CUP QUESTION UNIVERSE")
    print("=" * 60)
    print(f"  TOTAL QUESTIONS : {len(Q):,}")
    print(f"  VALUABLE subset : {valuable:,}  (SEO/market value — all real, named)")
    print(f"  long tail       : {len(Q)-valuable:,}  (squad-slot depth, honest)")
    print(f"  resolved marquee: {resolved} (carry the real 2022 answer → gradable)")
    print(f"  named-player props: {named:,}   squad-slot props: {slots:,}")
    print("  by category:")
    for c, n in cats.most_common():
        print(f"    {c:16s} {n:>7,}")
    print("  by layer:", dict(layers))
    print(f"\n  wrote -> questions_2022.json ({len(Q):,} q) + questions_2022.counts.json")


if __name__ == "__main__":
    main()
