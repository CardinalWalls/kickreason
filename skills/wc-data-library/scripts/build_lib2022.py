#!/usr/bin/env python3
"""
build_lib2022.py — assemble a REAL, complete 2022 FIFA World Cup data library.

Source: StatsBomb Open Data (CC-BY-NC 4.0), the full 2022 World Cup
(competition_id=43, season_id=106) — all 64 matches, every on-ball event with
StatsBomb xG, lineups, and 360 freeze-frame availability.

This is the NO-FAKING spine: every number below is fetched + derived, never typed.
It fully powers the STATS and MAGIC-MOMENT layers and the ground-truth RESULTS
needed for grading. It does NOT contain ODDS (StatsBomb has none) or NARRATIVE —
those are the two gaps the library README marks honestly for separate sourcing.

Output tree (dataset/lib2022/):
  index.json            — all 64 matches (id, date, stage, teams, score, stadium, ref)
  results.json          — compact ground truth per match (for grading)
  matches/{id}.json     — RICH derived record (xG, shots, goals w/ xG+minute, cards, possession proxy)
  events/{id}.json       — raw StatsBomb events (the full library, all 64)
  lineups/{id}.json      — raw lineups (XI + subs + positions)

Run:  python3 dataset/build_lib2022.py
"""
import json, os, sys, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor, as_completed

RAW = "https://raw.githubusercontent.com/statsbomb/open-data/master/data"
COMP, SEASON = 43, 106
HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "lib2022")

def fetch(url, tries=3):
    last = None
    for _ in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=40) as r:
                return json.load(r)
        except Exception as e:           # noqa
            last = e
    raise last

def ensure(*paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def derive(match_meta, events):
    """Turn raw events into a compact, rich, gradable per-match record."""
    home = match_meta["home_team"]["home_team_name"]
    away = match_meta["away_team"]["away_team_name"]
    teams = [home, away]
    xg = {t: 0.0 for t in teams}
    shots = {t: 0 for t in teams}
    sot = {t: 0 for t in teams}
    passes = {t: 0 for t in teams}
    goals, cards, shootout = [], [], []
    for ev in events:
        et = ev["type"]["name"]
        team = ev.get("team", {}).get("name")
        # period 5 = penalty shootout — NOT in-play; keep separate so it never inflates xG/goals
        if ev.get("period") == 5:
            if et == "Shot":
                sh = ev["shot"]
                shootout.append({"player": ev.get("player", {}).get("name"), "team": team,
                                 "outcome": sh.get("outcome", {}).get("name")})
            continue
        if et == "Pass" and team in passes:
            passes[team] += 1
        elif et == "Shot":
            sh = ev["shot"]
            if team in xg:
                xg[team] += sh.get("statsbomb_xg", 0.0)
                shots[team] += 1
                oc = sh.get("outcome", {}).get("name")
                if oc in ("Goal", "Saved", "Saved To Post"):
                    sot[team] += 1
                if oc == "Goal":
                    goals.append({
                        "minute": ev.get("minute"), "second": ev.get("second"),
                        "player": ev.get("player", {}).get("name"),
                        "team": team,
                        "xg": round(sh.get("statsbomb_xg", 0.0), 3),
                        "type": sh.get("type", {}).get("name"),          # Open Play / Penalty / Free Kick
                        "body_part": sh.get("body_part", {}).get("name"),
                    })
        elif et == "Own Goal Against":
            # own goal credited to the OTHER team's score
            scorer_team = team
            benef = away if scorer_team == home else home
            goals.append({"minute": ev.get("minute"), "second": ev.get("second"),
                          "player": ev.get("player", {}).get("name"),
                          "team": benef, "xg": None, "type": "Own Goal", "body_part": None})
        # cards
        card = None
        if "foul_committed" in ev and ev["foul_committed"].get("card"):
            card = ev["foul_committed"]["card"]["name"]
        elif "bad_behaviour" in ev and ev["bad_behaviour"].get("card"):
            card = ev["bad_behaviour"]["card"]["name"]
        if card:
            cards.append({"minute": ev.get("minute"), "player": ev.get("player", {}).get("name"),
                          "team": team, "card": card})
    goals.sort(key=lambda g: (g["minute"] or 0, g["second"] or 0))
    total_pass = sum(passes.values()) or 1
    return {
        "match_id": match_meta["match_id"],
        "date": match_meta["match_date"],
        "stage": match_meta["competition_stage"]["name"],
        "home_team": home, "away_team": away,
        "score": {"home": match_meta["home_score"], "away": match_meta["away_score"]},
        "winner": (home if match_meta["home_score"] > match_meta["away_score"]
                   else away if match_meta["away_score"] > match_meta["home_score"] else "Draw"),
        "team_xg": {t: round(v, 3) for t, v in xg.items()},
        "shots": shots, "shots_on_target": sot,
        "possession_proxy_pass_share": {t: round(passes[t] / total_pass, 3) for t in teams},
        "goals": goals,
        "shootout": shootout,
        "cards": cards,
        "n_events": len(events),
        "source": "StatsBomb Open Data CC-BY-NC 4.0 (competition 43 / season 106)",
    }

def one(meta):
    mid = meta["match_id"]
    events = fetch(f"{RAW}/events/{mid}.json")
    try:
        lineups = fetch(f"{RAW}/lineups/{mid}.json")
    except Exception:
        lineups = None
    json.dump(events, open(f"{LIB}/events/{mid}.json", "w"))
    if lineups is not None:
        json.dump(lineups, open(f"{LIB}/lineups/{mid}.json", "w"))
    rich = derive(meta, events)
    json.dump(rich, open(f"{LIB}/matches/{mid}.json", "w"), indent=1, ensure_ascii=False)
    return rich

def main():
    ensure(LIB, f"{LIB}/matches", f"{LIB}/events", f"{LIB}/lineups")
    print("Fetching 2022 World Cup match index ...")
    matches = fetch(f"{RAW}/matches/{COMP}/{SEASON}.json")
    matches.sort(key=lambda m: (m["match_date"], m["kick_off"] or ""))
    index = [{
        "match_id": m["match_id"], "date": m["match_date"], "kick_off": m.get("kick_off"),
        "stage": m["competition_stage"]["name"], "match_week": m.get("match_week"),
        "home_team": m["home_team"]["home_team_name"], "away_team": m["away_team"]["away_team_name"],
        "home_score": m["home_score"], "away_score": m["away_score"],
        "stadium": (m.get("stadium") or {}).get("name"),
        "referee": (m.get("referee") or {}).get("name"),
        "has_360": m.get("match_status_360") == "available",
    } for m in matches]
    json.dump(index, open(f"{LIB}/index.json", "w"), indent=1, ensure_ascii=False)
    print(f"  {len(index)} matches indexed -> lib2022/index.json")

    print(f"Fetching events + lineups for {len(matches)} matches (parallel) ...")
    rich_all, done, errs = [], 0, []
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(one, m): m for m in matches}
        for f in as_completed(futs):
            m = futs[f]
            try:
                rich_all.append(f.result()); done += 1
                if done % 8 == 0 or done == len(matches):
                    print(f"  {done}/{len(matches)} ...")
            except Exception as e:
                errs.append((m["match_id"], str(e)))
    rich_all.sort(key=lambda r: r["date"])

    results = [{
        "match_id": r["match_id"], "date": r["date"], "stage": r["stage"],
        "home_team": r["home_team"], "away_team": r["away_team"],
        "home_score": r["score"]["home"], "away_score": r["score"]["away"],
        "winner": r["winner"], "team_xg": r["team_xg"],
        "scorers": [f"{g['minute']}' {g['player']} ({g['team']}) xG={g['xg']}" for g in r["goals"]],
    } for r in rich_all]
    json.dump(results, open(f"{LIB}/results.json", "w"), indent=1, ensure_ascii=False)

    # coverage summary
    total_goals = sum(len(r["goals"]) for r in rich_all)
    total_events = sum(r["n_events"] for r in rich_all)
    n360 = sum(1 for m in index if m["has_360"])
    print("\n=== LIBRARY BUILT ===")
    print(f"matches:        {len(rich_all)}/64")
    print(f"raw events:     {total_events:,} on-ball events across the tournament")
    print(f"goals captured: {total_goals}")
    print(f"360 available:  {n360}/64 matches")
    print(f"errors:         {len(errs)}", errs[:5] if errs else "")
    print(f"\nwrote -> {LIB}/  (index.json, results.json, matches/, events/, lineups/)")

if __name__ == "__main__":
    main()
