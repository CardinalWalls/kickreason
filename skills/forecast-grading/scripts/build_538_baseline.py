#!/usr/bin/env python3
"""
build_538_baseline.py — add FiveThirtyEight's published 2022 World Cup forecast to the
ODDS/CALIBRATION layer as a second, recognized MODEL baseline.

Source: FiveThirtyEight 2022 World Cup predictions (SPI model), mirrored on Kaggle
(kutlukatalay/2022-fifa-world-cup-predictions) from
projects.fivethirtyeight.com/soccer-api/international/2022/wc_matches.csv.
Stored under lib2022/sources/fivethirtyeight/ for provenance.

Why it matters: it's a REAL, citeable published forecast with full pre-match 1X2
probabilities (prob1/probtie/prob2) for all 64 matches — better than our two-way Elo
because it models the draw. GOLDEN.md already names 538 as the calibration benchmark.
NOTE: it is a MODEL forecast, NOT market closing odds. No clean free WC2022 market-odds
dataset exists (verified on Kaggle); the 10 hand-sourced market cases in
seed-resolved.json remain the only real-market anchor.

Output: lib2022/forecast_538.json (per-match 1X2 + SPI + 538 xG, mapped to match_id,
self-graded by Brier) + a printed head-to-head vs the Elo baseline.
"""
import csv, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "lib2022")
sys.path.insert(0, HERE)
try:
    from baseline import brier
except Exception:
    def brier(p, o): return (p - o) ** 2

NAME = {"USA": "United States"}     # only diff vs StatsBomb names
def norm(t): return NAME.get(t, t)

def main():
    idx = json.load(open(f"{LIB}/index.json"))
    # lookup: frozenset(pair) -> list of index entries (handles a pair meeting twice)
    by_pair = {}
    for m in idx:
        by_pair.setdefault(frozenset((m["home_team"], m["away_team"])), []).append(m)

    fte = list(csv.DictReader(open(f"{LIB}/sources/fivethirtyeight/wc_matches.csv", encoding="utf-8-sig")))
    rows, b_fav, b_1x2, unmatched = [], [], [], []
    for r in fte:
        t1, t2 = norm(r["team1"]), norm(r["team2"])
        cands = by_pair.get(frozenset((t1, t2)), [])
        if not cands:
            unmatched.append((t1, t2, r["date"])); continue
        m = min(cands, key=lambda x: abs((x["date"] > r["date"]) - (x["date"] < r["date"]))) \
            if len(cands) > 1 else cands[0]
        if len(cands) > 1:   # disambiguate a repeated pair by closest date
            m = min(cands, key=lambda x: abs(_d(x["date"]) - _d(r["date"])))
        p1, ptie, p2 = float(r["prob1"]), float(r["probtie"]), float(r["prob2"])
        hs, as_ = m["home_score"], m["away_score"]
        winner = m["home_team"] if hs > as_ else m["away_team"] if as_ > hs else "Draw"
        # favourite (same convention as the Elo baseline + GOLDEN: draw = favourite not-won)
        fav, p_fav = (t1, p1) if p1 >= p2 else (t2, p2)
        fav_won = None if winner == "Draw" else (winner == fav)
        bf = round(brier(p_fav, 1 if fav_won else 0), 4)
        # full proper 3-class Brier on (team1 win, draw, team2 win)
        o1, otie, o2 = (1, 0, 0) if winner == t1 else (0, 0, 1) if winner == t2 else (0, 1, 0)
        b3 = round((p1 - o1) ** 2 + (ptie - otie) ** 2 + (p2 - o2) ** 2, 4)
        b_fav.append(bf); b_1x2.append(b3)
        rows.append({
            "match_id": m["match_id"], "date": m["date"], "stage": m["stage"],
            "team1": t1, "team2": t2,
            "p_team1_win": round(p1, 4), "p_draw": round(ptie, 4), "p_team2_win": round(p2, 4),
            "spi1": float(r["spi1"]), "spi2": float(r["spi2"]),
            "fte_xg1": float(r["xg1"]) if r.get("xg1") else None,
            "fte_xg2": float(r["xg2"]) if r.get("xg2") else None,
            "favourite": fav, "p_favourite": round(p_fav, 4),
            "actual_winner": winner, "favourite_won": fav_won,
            "brier_favourite": bf, "brier_1x2": b3,
            "model": "FiveThirtyEight SPI pre-match forecast",
        })
    out = {
        "model": "FiveThirtyEight SPI (2022 World Cup)",
        "source": "projects.fivethirtyeight.com/soccer-api/international/2022/wc_matches.csv "
                  "(via Kaggle kutlukatalay/2022-fifa-world-cup-predictions); see sources/fivethirtyeight/",
        "note": "Recognized MODEL forecast with full 1X2 incl. draw — NOT market odds.",
        "n_matches": len(rows),
        "mean_brier_favourite": round(sum(b_fav) / len(b_fav), 4),
        "mean_brier_1x2": round(sum(b_1x2) / len(b_1x2), 4),
        "unmatched": unmatched,
        "matches": rows,
    }
    json.dump(out, open(f"{LIB}/forecast_538.json", "w"), indent=1, ensure_ascii=False)

    # head-to-head vs Elo baseline
    elo = json.load(open(f"{LIB}/odds_baseline.json"))
    hero = next((r for r in rows if r["match_id"] == 3857300), None)
    print(f"538 forecast merged: {len(rows)}/64 matches | unmatched: {unmatched}")
    print(f"  mean favourite Brier : 538 = {out['mean_brier_favourite']}  vs  Elo = {elo['mean_brier_favourite']}")
    print(f"  mean 1X2 Brier (538, proper 3-class, lower=better): {out['mean_brier_1x2']}")
    if hero:
        print(f"  HERO Argentina-Saudi: 538 said Argentina win p1={hero['p_team1_win'] if hero['team1']=='Argentina' else hero['p_team2_win']} "
              f"draw={hero['p_draw']} -> favourite={hero['favourite']} p={hero['p_favourite']} "
              f"won={hero['favourite_won']} Brier_fav={hero['brier_favourite']}")
    print(f"wrote -> {LIB}/forecast_538.json")

def _d(s):
    y, m, d = s.split("-"); return int(y) * 372 + int(m) * 31 + int(d)

if __name__ == "__main__":
    main()
