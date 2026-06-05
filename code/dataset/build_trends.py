#!/usr/bin/env python3
"""Google Trends corroboration for the TRAFFIC layer (free, no key). Saves whatever returns;
Google frequently rate-limits automated pulls — failure is recorded honestly, not faked."""
import json, os
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "lib2022", "traffic")
try:
    from pytrends.request import TrendReq
    pt = TrendReq(hl="en-US", tz=0, retries=2, backoff_factor=0.5)
    kw = ["Saudi Arabia", "Argentina", "Morocco", "Mbappe"]
    pt.build_payload(kw, timeframe="2022-11-15 2022-12-20", geo="")
    df = pt.interest_over_time()
    rec = [{"date": str(i.date()), **{k: int(row[k]) for k in kw}} for i, row in df.iterrows()]
    json.dump({"source": "Google Trends (interest over time, worldwide)", "keywords": kw, "series": rec},
              open(f"{OUT}/google_trends.json", "w"), indent=1)
    peak = max(rec, key=lambda r: r["Saudi Arabia"])
    print(f"Google Trends OK: {len(rec)} days. Saudi Arabia interest peaked {peak['date']} (={peak['Saudi Arabia']}/100)")
except Exception as e:
    json.dump({"status": "blocked", "error": f"{type(e).__name__}: {e}",
               "note": "Google rate-limited the automated pull; manual CSV export from trends.google.com works."},
              open(f"{OUT}/google_trends.json", "w"), indent=1)
    print(f"Google Trends BLOCKED ({type(e).__name__}) — recorded honestly; manual export is the fallback.")
