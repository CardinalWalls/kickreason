#!/usr/bin/env python3
"""
build_traffic_layer.py — the TRAFFIC / GROWTH / FAN-ENGAGEMENT layer (domain 4) for 2022.

This is the layer our 4-layer model was missing. It is graded NOT on correctness but on
ENGAGEMENT (volume, sentiment, reach, virality), and it is triggered by the same events as
MAGIC-MOMENT (a goal fires both) — so it proves "one moment, re-read into a different domain's
metric." 2022 is the right slice to prototype it: X/Reddit LIVE APIs are paid now, so historical
dumps are the only realistic access — and 2022 has them.

Sources (Kaggle, free; sampled #WorldCup2022 scrapes — so the SHAPE of a spike is the signal,
absolute counts are not a firehose):
  - konradb/qatar-world-cup-2022-tweets  (124,679 tweets, 2022-11-20 -> 2023-01-18, hourly, +followers) = PRIMARY
  - deepeshnigamdata/tweets-on-football-world-cup-2022 (100,000, knockouts, huge on the final)
  - tirendazacademy/fifa-world-cup-2022-tweets (opening day only, but pre-LABELLED sentiment = VADER validation)
Sentiment: VADER (lexicon, social-media tuned) — compound in [-1,1]. NOT a trained classifier; labelled honestly.

Outputs (dataset/lib2022/traffic/):
  engagement_by_day.json  — per tournament day: volume, mean sentiment, reach, top team mentions
  hero_saudi_arg.json     — hourly volume + sentiment on 2022-11-22, annotated with kickoff + goals (the spike)
  hero_final.json         — hourly volume + sentiment on 2022-12-18
  vader_validation.json   — VADER vs the human labels on the opening-day set (honesty check)
"""
import csv, json, os, collections
from datetime import datetime
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "lib2022")
OUT = os.path.join(LIB, "traffic")
KAG = "/tmp/kag"
VADER = SentimentIntensityAnalyzer()

TEAMS = {  # name -> aliases to scan for in tweet text (lowercased)
    "Argentina": ["argentina", "messi", "albiceleste", "scaloni"],
    "Saudi Arabia": ["saudi", "ksa", "green falcons", "dawsari"],
    "France": ["france", "mbappe", "mbappé", "les bleus", "griezmann"],
    "Morocco": ["morocco", "maroc", "atlas lions", "hakimi", "regragui"],
    "Croatia": ["croatia", "modric"],
    "Brazil": ["brazil", "neymar"],
    "Portugal": ["portugal", "ronaldo"],
    "England": ["england", "kane"],
}

def parse(s):
    s = (s or "").strip().split("+")[0].strip()
    for f in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try: return datetime.strptime(s, f)
        except Exception: pass
    return None

def senti(text):
    return VADER.polarity_scores(text or "")["compound"]

def mentions(text):
    t = (text or "").lower()
    return [team for team, al in TEAMS.items() if any(a in t for a in al)]

def load(path, dcol, tcol, fcol=None):
    out = []
    if not os.path.exists(path): return out
    for r in csv.DictReader(open(path, encoding="utf-8", errors="replace")):
        dt = parse(r.get(dcol, ""))
        if not dt: continue
        txt = r.get(tcol, "")
        foll = 0
        if fcol and r.get(fcol):
            try: foll = int(float(r[fcol]))
            except Exception: foll = 0
        out.append({"dt": dt, "text": txt, "foll": foll})
    return out

def main():
    os.makedirs(OUT, exist_ok=True)
    konr = load(f"{KAG}/tw_qatar-world-cup-2022-tweets/tweets.csv", "date", "text", "user_followers")
    deep = load(f"{KAG}/tw_tweets-on-football-world-cup-2022/tweets_football.csv", "Date", "Tweet")
    tweets = konr + deep
    print(f"loaded {len(konr)} konradb + {len(deep)} deepesh = {len(tweets)} tweets")
    # score once
    for t in tweets:
        t["s"] = senti(t["text"])
        t["m"] = mentions(t["text"])

    # ---- per-day engagement across the tournament ----
    by_day = collections.defaultdict(lambda: {"n": 0, "s_sum": 0.0, "reach": 0, "teams": collections.Counter()})
    for t in tweets:
        d = t["dt"].strftime("%Y-%m-%d")
        rec = by_day[d]
        rec["n"] += 1; rec["s_sum"] += t["s"]; rec["reach"] += t["foll"]
        for tm in t["m"]: rec["teams"][tm] += 1
    days = []
    for d in sorted(by_day):
        r = by_day[d]
        days.append({"date": d, "tweets": r["n"], "mean_sentiment": round(r["s_sum"] / r["n"], 4),
                     "reach_followers": r["reach"], "top_teams": r["teams"].most_common(4)})
    json.dump(days, open(f"{OUT}/engagement_by_day.json", "w"), indent=1, ensure_ascii=False)

    # ---- hero time-series (hourly UTC) ----
    def hero(day, focus_a, focus_b, kickoff_utc, goals_note, fname):
        rows = [t for t in tweets if t["dt"].strftime("%Y-%m-%d") == day]
        hourly = collections.defaultdict(lambda: {"n": 0, "s_sum": 0.0, "a": 0, "b": 0})
        for t in rows:
            h = hourly[t["dt"].hour]
            h["n"] += 1; h["s_sum"] += t["s"]
            if focus_a in t["m"]: h["a"] += 1
            if focus_b in t["m"]: h["b"] += 1
        series = [{"hour_utc": hh, "tweets": hourly[hh]["n"],
                   "mean_sentiment": round(hourly[hh]["s_sum"] / hourly[hh]["n"], 4) if hourly[hh]["n"] else None,
                   f"mentions_{focus_a}": hourly[hh]["a"], f"mentions_{focus_b}": hourly[hh]["b"]}
                  for hh in range(24) if hourly[hh]["n"]]
        # team-vs-team mention share + sentiment on the day (robust; the sample concentrates on the match window)
        a_s = [t["s"] for t in rows if focus_a in t["m"]]
        b_s = [t["s"] for t in rows if focus_b in t["m"]]
        peak = max(series, key=lambda x: x["tweets"]) if series else {}
        out = {"day": day, "focus": [focus_a, focus_b], "kickoff_utc": f"{kickoff_utc:02d}:00",
               "goals": goals_note, "total_tweets": len(rows),
               "peak_hour_utc": peak.get("hour_utc"), "peak_hour_tweets": peak.get("tweets"),
               f"{focus_a}_mentions": len(a_s), f"{focus_b}_mentions": len(b_s),
               f"{focus_a}_mention_sentiment": round(sum(a_s) / len(a_s), 4) if a_s else None,
               f"{focus_b}_mention_sentiment": round(sum(b_s) / len(b_s), 4) if b_s else None,
               "hourly": series,
               "note": "Sampled hashtag scrape — the SHAPE (volume spike + mention-share flip at the moment) is the "
                       "signal, not absolute volume. VADER sentiment is noisy (see vader_validation.json); lead with volume."}
        json.dump(out, open(f"{OUT}/{fname}", "w"), indent=1, ensure_ascii=False)
        print(f"  {day} ({focus_a} v {focus_b}): {len(rows)} tw | peak {peak.get('hour_utc')}:00 UTC "
              f"({peak.get('tweets')} tw, {round(100*peak.get('tweets',0)/max(len(rows),1))}% of day) | "
              f"mentions {focus_a}={len(a_s)} vs {focus_b}={len(b_s)}")
        return out

    print("HERO time-series:")
    hero("2022-11-22", "Argentina", "Saudi Arabia", 10, "Messi pen 9'; Al-Shehri 47'; Al-Dawsari 52' (winner ~11:00 UTC)", "hero_saudi_arg.json")
    hero("2022-12-18", "Argentina", "France", 15, "Messi 22',108'; Di Maria 35'; Mbappe 80',81'(pen),118'; Argentina win pens", "hero_final.json")

    # ---- VADER validation vs human labels (opening-day set) ----
    val = []
    tir = f"{KAG}/tw_fifa-world-cup-2022-tweets/fifa_world_cup_2022_tweets.csv"
    if os.path.exists(tir):
        agree = tot = 0
        for r in csv.DictReader(open(tir, encoding="utf-8", errors="replace")):
            lab = (r.get("Sentiment") or "").lower()
            if lab not in ("positive", "negative", "neutral"): continue
            c = senti(r.get("Tweet", ""))
            pred = "positive" if c >= 0.05 else "negative" if c <= -0.05 else "neutral"
            tot += 1; agree += (pred == lab)
        val = {"n": tot, "vader_vs_human_agreement": round(agree / tot, 3) if tot else None,
               "note": "3-class agreement of VADER vs the dataset's human labels on the opening-day set."}
        json.dump(val, open(f"{OUT}/vader_validation.json", "w"), indent=1, ensure_ascii=False)
        print(f"VADER vs human labels: {val['vader_vs_human_agreement']} agreement on {tot} opening-day tweets")

    print(f"\nwrote -> {OUT}/  (engagement_by_day.json, hero_saudi_arg.json, hero_final.json, vader_validation.json)")

if __name__ == "__main__":
    main()
