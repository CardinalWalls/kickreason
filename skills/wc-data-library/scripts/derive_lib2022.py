#!/usr/bin/env python3
"""
derive_lib2022.py — second-pass derivations on the local 2022 WC event library.

Reads dataset/lib2022/events/*.json (already fetched by build_lib2022.py) and
produces the aggregate tables that resolve the PLAYER-PROP and STATS layers with
real, gradable ground truth — no new network calls, nothing typed by hand:

  players.json   — per-player tournament totals (goals, xG, shots, SoT, assists,
                   key passes, minutes, appearances) — the golden-boot race etc.
  teams.json     — per-team tournament totals (xG for/against, goals, shots, result line)
  bracket.json   — the knockout tree (R16 -> Final) with scores + shootouts
  leaders.json   — ready-made leaderboards (top scorers, top xG, most assists, xG over/under-performers)
"""
import json, os, glob, collections

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "lib2022")

def mmss_to_min(v):
    if v is None: return None
    if isinstance(v, (int, float)): return float(v)
    try:
        m, s = str(v).split(":"); return int(m) + int(s) / 60.0
    except Exception:
        return None

def minutes_from_lineup(mid):
    """Best-effort minutes per player from the lineup positions (newer SB format)."""
    p = f"{LIB}/lineups/{mid}.json"
    if not os.path.exists(p): return {}
    out = {}
    for team in json.load(open(p)):
        for pl in team.get("lineup", []):
            name = pl.get("player_name")
            poss = pl.get("positions") or []
            if not poss:
                continue
            froms = [mmss_to_min(x.get("from")) for x in poss if mmss_to_min(x.get("from")) is not None]
            tos = []
            for x in poss:
                t = mmss_to_min(x.get("to"))
                tos.append(t if t is not None else 90.0)  # played to (at least) full time
            if froms:
                out[name] = round(max(tos) - min(froms), 1)
    return out

def main():
    idx = json.load(open(f"{LIB}/index.json"))
    P = collections.defaultdict(lambda: {"team": None, "goals": 0, "xg": 0.0, "shots": 0,
                                          "sot": 0, "assists": 0, "key_passes": 0,
                                          "minutes": 0.0, "apps": 0, "yellow": 0, "red": 0})
    T = collections.defaultdict(lambda: {"goals_for": 0, "goals_against": 0, "xg_for": 0.0,
                                         "xg_against": 0.0, "shots": 0, "matches": 0})

    for meta in idx:
        mid = meta["match_id"]
        events = json.load(open(f"{LIB}/events/{mid}.json"))
        mins = minutes_from_lineup(mid)
        seen = set()
        home, away = meta["home_team"], meta["away_team"]
        T[home]["matches"] += 1; T[away]["matches"] += 1
        for ev in events:
            if ev.get("period") == 5:   # shootout: ignore for in-play aggregates
                continue
            team = ev.get("team", {}).get("name")
            pname = ev.get("player", {}).get("name")
            et = ev["type"]["name"]
            if pname and team:
                rec = P[pname]; rec["team"] = team
                if pname not in seen:
                    seen.add(pname); rec["apps"] += 1
                    if pname in mins: rec["minutes"] += mins[pname]
            if et == "Shot":
                sh = ev["shot"]; xgv = sh.get("statsbomb_xg", 0.0)
                if team in (home, away):
                    T[team]["shots"] += 1; T[team]["xg_for"] += xgv
                    opp = away if team == home else home
                    T[opp]["xg_against"] += xgv
                if pname:
                    P[pname]["shots"] += 1; P[pname]["xg"] += xgv
                    oc = sh.get("outcome", {}).get("name")
                    if oc in ("Goal", "Saved", "Saved To Post"): P[pname]["sot"] += 1
                    if oc == "Goal":
                        P[pname]["goals"] += 1
            elif et == "Pass":
                pa = ev.get("pass", {})
                if pa.get("goal_assist"): P[pname]["assists"] += 1
                if pa.get("shot_assist"): P[pname]["key_passes"] += 1
            card = None
            if "foul_committed" in ev and ev["foul_committed"].get("card"):
                card = ev["foul_committed"]["card"]["name"]
            elif "bad_behaviour" in ev and ev["bad_behaviour"].get("card"):
                card = ev["bad_behaviour"]["card"]["name"]
            if card and pname:
                if "Yellow" in card: P[pname]["yellow"] += 1
                if "Red" in card: P[pname]["red"] += 1
        # team goals from the official score (authoritative; includes set pieces/OGs, excludes shootout)
        T[home]["goals_for"] += meta["home_score"]; T[home]["goals_against"] += meta["away_score"]
        T[away]["goals_for"] += meta["away_score"]; T[away]["goals_against"] += meta["home_score"]

    players = []
    for name, r in P.items():
        r = dict(r); r["player"] = name
        r["xg"] = round(r["xg"], 3); r["minutes"] = round(r["minutes"], 1)
        r["xg_overperformance"] = round(r["goals"] - r["xg"], 3)
        players.append(r)
    players.sort(key=lambda r: (-r["goals"], -r["xg"]))
    json.dump(players, open(f"{LIB}/players.json", "w"), indent=1, ensure_ascii=False)

    teams = []
    for name, r in T.items():
        r = dict(r); r["team"] = name
        r["xg_for"] = round(r["xg_for"], 2); r["xg_against"] = round(r["xg_against"], 2)
        teams.append(r)
    teams.sort(key=lambda r: (-r["goals_for"], -r["xg_for"]))
    json.dump(teams, open(f"{LIB}/teams.json", "w"), indent=1, ensure_ascii=False)

    # knockout bracket
    ko_order = ["Round of 16", "Quarter-finals", "Semi-finals", "3rd Place Final", "Final"]
    bracket = {st: [] for st in ko_order}
    for m in idx:
        if m["stage"] in bracket:
            bracket[m["stage"]].append({
                "date": m["date"], "home": m["home_team"], "away": m["away_team"],
                "score": f"{m['home_score']}-{m['away_score']}",
            })
    json.dump(bracket, open(f"{LIB}/bracket.json", "w"), indent=1, ensure_ascii=False)

    leaders = {
        "top_scorers": [(p["player"], p["team"], p["goals"], p["xg"]) for p in players[:12]],
        "top_xg": sorted([(p["player"], p["team"], p["xg"], p["goals"]) for p in players],
                         key=lambda x: -x[2])[:12],
        "most_assists": sorted([(p["player"], p["team"], p["assists"]) for p in players],
                               key=lambda x: -x[2])[:12],
        "biggest_xg_overperformers": sorted(
            [(p["player"], p["team"], p["xg_overperformance"], p["goals"], p["xg"])
             for p in players if p["shots"] >= 3], key=lambda x: -x[2])[:10],
        "best_xg_for_teams": sorted([(t["team"], t["xg_for"], t["goals_for"]) for t in teams],
                                    key=lambda x: -x[1])[:8],
    }
    json.dump(leaders, open(f"{LIB}/leaders.json", "w"), indent=1, ensure_ascii=False)

    print(f"players: {len(players)} | teams: {len(teams)}")
    print("Golden Boot (top 5):", [(p['player'].split()[-1], p['team'], p['goals']) for p in players[:5]])
    print("Top xG (top 5):", [(x[0].split()[-1], round(x[2],1)) for x in leaders['top_xg'][:5]])
    print("wrote players.json, teams.json, bracket.json, leaders.json -> lib2022/")

if __name__ == "__main__":
    main()
