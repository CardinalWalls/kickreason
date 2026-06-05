#!/usr/bin/env python3
"""
build_odds_baseline.py — the ODDS layer for lib2022, as a TRANSPARENT Elo baseline.

StatsBomb has no odds, and no clean free all-64 market-odds file exists. So we fill
the ODDS layer the way TASKS.md Lane 2 specifies: a real, reproducible model — World
Football Elo win-expectancy — clearly LABELLED as a model baseline, not the live market.
Real market odds (seed-resolved.json, 10 cases) can be layered on top for CLV later.

Model (canonical Elo expectancy, citeable):
    E_home = 1 / (1 + 10 ** (-(elo_home + home_adv - elo_away) / 400))
World Cup venues are neutral → home_adv = 0, EXCEPT host Qatar's group matches (+100).
E_home is the two-way win-expectancy (who-goes-through probability); a full 1X2 split
needs a draw model or real market prices — flagged, not faked.

Inputs : dataset/lib2022/index.json (matches), dataset/lib2022/elo_ratings.json (pre-WC Elo)
Output : dataset/lib2022/odds_baseline.json  + a printed Brier self-grade vs real results.
"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "lib2022")
sys.path.insert(0, HERE)
try:
    from baseline import brier            # the self-tested scoring fn
except Exception:
    def brier(p, o): return (p - o) ** 2

QATAR_HOME_ADV = 100   # host advantage applied only to Qatar's group matches

def expectancy(elo_a, elo_b, home_adv=0):
    return 1.0 / (1.0 + 10 ** (-((elo_a + home_adv) - elo_b) / 400.0))

def main():
    idx = json.load(open(f"{LIB}/index.json"))
    elo = json.load(open(f"{LIB}/elo_ratings.json"))
    teams_used = {m["home_team"] for m in idx} | {m["away_team"] for m in idx}
    missing = sorted(teams_used - set(elo))
    if missing:
        print("ERROR: missing Elo for:", missing); sys.exit(1)

    rows, briers = [], []
    upsets = 0
    for m in idx:
        h, a = m["home_team"], m["away_team"]
        ha = QATAR_HOME_ADV if (h == "Qatar" and m["stage"] == "Group Stage") else 0
        # (Qatar only played group stage, but the guard is explicit anyway)
        p_h = round(expectancy(elo[h], elo[a], ha), 4)
        p_a = round(1 - p_h, 4)
        fav = h if p_h >= p_a else a
        p_fav = max(p_h, p_a)
        hs, as_ = m["home_score"], m["away_score"]
        winner = h if hs > as_ else a if as_ > hs else "Draw"
        fav_won = None if winner == "Draw" else (winner == fav)
        # grade the favourite's win-probability against the realised two-way outcome
        # (draw counts as the favourite NOT winning — same convention as GOLDEN.md)
        outcome = 1 if fav_won else 0
        b = round(brier(p_fav, outcome), 4)
        briers.append(b)
        if fav_won is False:
            upsets += 1
        rows.append({
            "match_id": m["match_id"], "date": m["date"], "stage": m["stage"],
            "home_team": h, "away_team": a, "elo_home": elo[h], "elo_away": elo[a],
            "p_home_2way": p_h, "p_away_2way": p_a,
            "favourite": fav, "p_favourite": p_fav,
            "actual_winner": winner, "favourite_won": fav_won,
            "brier_favourite": b,
            "model": "World Football Elo win-expectancy (neutral venue; Qatar +100 host adv, group only)",
        })
    out = {
        "model": "Elo win-expectancy baseline",
        "source": "eloratings.net pre-tournament ratings (~2022-11-19); see elo_ratings.json",
        "note": "LABELLED MODEL BASELINE, not live market odds. Two-way (win/not-win); full 1X2 needs a draw model or real prices.",
        "mean_brier_favourite": round(sum(briers) / len(briers), 4),
        "n_matches": len(rows), "n_upsets_favourite_lost": upsets,
        "matches": rows,
    }
    json.dump(out, open(f"{LIB}/odds_baseline.json", "w"), indent=1, ensure_ascii=False)

    # cross-check vs the real market on the hero case
    hero = next((r for r in rows if r["match_id"] == 3857300), None)
    print(f"odds_baseline: {len(rows)} matches | mean favourite Brier = {out['mean_brier_favourite']} "
          f"| {upsets} upsets (favourite lost)")
    if hero:
        print(f"  HERO check Argentina-Saudi: Elo favourite={hero['favourite']} "
              f"p={hero['p_favourite']} (real market said Argentina ~0.871) -> "
              f"favourite_won={hero['favourite_won']} Brier={hero['brier_favourite']}")
    print(f"wrote -> {LIB}/odds_baseline.json")

if __name__ == "__main__":
    main()
