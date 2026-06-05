# TRAFFIC layer — fan-engagement (domain 4), 2022 World Cup

> Built by `python3 dataset/build_traffic_layer.py` (+ `build_trends.py`). This is the **5th layer**
> our model was missing — graded on **engagement, not correctness** — and it shares its trigger with
> MAGIC-MOMENT (a goal fires both). It proves *"one moment, re-read into a different domain's metric."*

## Why 2022 (not 2026)
X/Twitter and Reddit **live** APIs are paid now, so historical dumps are the only realistic access — and
2022 has them. This is exactly why the past tournament is the right slice to prototype the traffic layer.

## Sources (Kaggle, free — sampled #WorldCup2022 scrapes)
| Set | Rows | Span | Role |
|---|---|---|---|
| `konradb/qatar-world-cup-2022-tweets` | 124,679 | Nov 20 → Jan 18, hourly, +follower counts | **PRIMARY** (covers every hero) |
| `deepeshnigamdata/tweets-on-football-world-cup-2022` | 100,000 | Dec 5 → Dec 24 | knockouts + final |
| `tirendazacademy/fifa-world-cup-2022-tweets` | 22,524 | opening day, **human-labelled sentiment** | VADER validation only |

Sentiment = **VADER** (lexicon, social-tuned), compound ∈ [-1,1]. **It's noisy**: 0.584 three-class
agreement vs the human labels (`vader_validation.json`) — so we **lead with volume/mention-share**, not sentiment.

## The hero proof — the moment IS the engagement spike
**Saudi Arabia 2–1 Argentina (Nov 22).** Al-Dawsari's winner (StatsBomb: 52', xG **0.033**) lands ~11:00 UTC:

| Hour (UTC) | Tweets | Argentina mentions | Saudi mentions |
|---|---|---|---|
| 10:00 (kickoff) | 257 | 158 | 149 |
| **11:00 (winner)** | **2,540** (91% of the day) | 1,975 | **2,155 ← underdog overtakes** |

The conversation **10×'d in one hour** and **flipped to Saudi-dominant** — the magic-moment node and the
traffic node, same trigger, different metric. (`hero_saudi_arg.json`; final in `hero_final.json`.)

## Day-level engagement (real, sourced)
`engagement_by_day.json` — per tournament day: volume, mean sentiment, **reach (Σ followers)**, top teams.
Biggest days: **Final Dec 18** (34,408 tw / 165M reach) · QF Dec 9 (19,146 / 126M) · **semi Dec 14
France–Morocco (236M reach)** — Morocco's run drove the tournament's biggest reach spike.

## Honest limits
- **Sampled, not a firehose** → the *shape* of a spike is the signal; absolute counts aren't comparable across days.
- **VADER is weak** (0.58) → volume + mention-share are the trustworthy metrics; sentiment is directional only.
- **tirendaz** covers only opening day; **Google Trends** automated pull is **blocked** by Google
  (`google_trends.json` records it) — manual CSV export from trends.google.com is the fallback.

## Files
`engagement_by_day.json` · `hero_saudi_arg.json` · `hero_final.json` · `vader_validation.json` · `google_trends.json`
