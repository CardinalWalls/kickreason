#!/usr/bin/env python3
"""
eval_traces.py — score the REAL traces captured by run_forecasts.py.

This is the "metric to evaluate the USE of the API" — it grades the TRACE (process),
not the forecast result. All mechanical, all checkable, none of it requires the
forecast to be "right". Writes dataset/eval-results.json + dataset/EVAL.md.

Trace-quality dimensions (per brainstorm/kickoracle/05 + the trace-eval reframe):
  finished        — did the call complete (not timeout/error)?
  grounded        — did it actually search + fetch real sources?
  reputable       — share of sources from recognizable outlets
  has_probability — does the answer commit to a number (a forecast, not prose)?
  coverage        — of the question's "factors", how many did the trace touch?

For PAST events (leakage probe) two SEPARATE signals — because they mean different
things and conflating them is how my first pass lied to me:
  answer_leak          — does the model's ANSWER betray the real result? (the real risk)
  post_result_sources  — how many retrieved SOURCES already contain the result?
                         (expected for a past event; a risk indicator, not a leak itself)
"""
import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")

REPUTABLE = ("fifa.com", "uefa.com", "espn", "bbc.", "skysports", "theathletic",
             "reuters", "apnews", "ap.org", "opta", "statsperform", "fbref",
             "transfermarkt", "goal.com", "nytimes", "theguardian", "cbssports",
             "foxsports", "wikipedia", "sofascore", "whoscored", "oddschecker",
             "pinnacle", "flashscore", "365scores", "radiotimes", "yahoo")

# Result-specific tells for the Euro-2024 final leak probe (Spain 2-1 England,
# Oyarzabal 86'). Word-boundaried so a date like "12-14" does NOT match "2-1".
RESULT_TELLS = [
    r"(?<!\d)2\s?[-‒-―]\s?1(?!\d)",          # the 2-1 scoreline, not a date span
    r"oyarz[aá]bal",                              # the winning scorer
    r"spain\s+(?:won|beat|defeated|lifted|were\s+crowned|claimed\s+the)",
    r"england\s+(?:lost|were\s+beaten|fell\s+short)",
    r"champions?\s+of\s+europe",
]


def find_tells(text):
    hits = []
    for pat in RESULT_TELLS:
        m = re.search(pat, text, re.I)
        if m:
            hits.append(m.group(0).strip())
    return hits


def has_prob(text):
    return bool(re.search(r"\b\d{1,3}\s?%", text)) or bool(re.search(r"\b0?\.\d{2}\b", text))


def coverage(rec):
    hay = (rec.get("content", "") + " " + json.dumps(rec.get("steps", []))).lower()
    hits = []
    for f in rec.get("factors", []):
        words = [w for w in f.lower().split() if len(w) > 2]
        if words and any(w in hay for w in words):
            hits.append(f)
    return hits


def reputable_share(sources):
    if not sources:
        return 0.0, 0
    c = sum(1 for s in sources if any(d in (s.get("url") or "").lower() for d in REPUTABLE))
    return round(c / len(sources), 2), c


def answer_leak(rec):
    """Result tells in the model's OWN answer (the real leak). None if not a past event."""
    if rec.get("kind") != "past":
        return None
    return find_tells(rec.get("content", ""))


def post_result_sources(rec):
    """How many retrieved sources' url/title already contain the result. Risk, not leak."""
    if rec.get("kind") != "past":
        return None
    n = 0
    for s in rec.get("sources", []):
        if find_tells((s.get("url") or "") + " " + (s.get("title") or "")):
            n += 1
    return n


def score(row):
    """Transparent 0-1 composite of trace quality (process, not result)."""
    s = 0.0
    s += 0.25 if row["finished"] else 0.0
    s += 0.20 if row["web_search"] > 0 else 0.0
    s += 0.15 if row["fetch"] > 0 else 0.0
    s += 0.15 if row["has_probability"] else 0.0
    cov_n, cov_d = (row["coverage"].split("/") + ["0", "1"])[:2]
    s += 0.15 * (int(cov_n) / max(1, int(cov_d)))
    s += 0.10 * row["reputable_share"]
    return round(s, 2)


def main():
    paths = sorted(glob.glob(os.path.join(RUNS, "*.json")))
    if not paths:
        print("No runs found in dataset/runs/. Run run_forecasts.py first.")
        return
    rows = []
    for p in paths:
        rec = json.load(open(p))
        steps = rec.get("steps", [])
        ws = sum(1 for s in steps if s.get("action") == "web_search")
        fetch = sum(1 for s in steps if s.get("action") == "fetch")
        cov = coverage(rec)
        rep_share, rep_n = reputable_share(rec.get("sources", []))
        row = {
            "id": rec["id"], "kind": rec.get("kind"),
            "finished": not rec.get("timed_out") and not rec.get("error"),
            "elapsed_s": rec.get("elapsed_s"), "timed_out": rec.get("timed_out"),
            "error": rec.get("error"),
            "steps": len(steps), "web_search": ws, "fetch": fetch,
            "sources": len(rec.get("sources", [])),
            "reputable_sources": rep_n, "reputable_share": rep_share,
            "answer_chars": len(rec.get("content", "")),
            "has_probability": has_prob(rec.get("content", "")),
            "coverage": f"{len(cov)}/{len(rec.get('factors', []))}",
            "coverage_hits": cov,
            "reasoning_tokens": (rec.get("usage") or {}).get("reasoning_tokens"),
            "answer_leak": answer_leak(rec),
            "post_result_sources": post_result_sources(rec),
        }
        row["trace_score"] = score(row)
        rows.append(row)

    json.dump(rows, open(os.path.join(HERE, "eval-results.json"), "w"),
              indent=2, ensure_ascii=False)

    # ---- markdown report ----
    lines = ["# Trace eval — real MiroMind API runs", "",
             "Scores the **trace** (use of the API), not the forecast result. "
             "`trace_score` is a transparent 0-1 composite (finished .25 / searched .20 / "
             "fetched .15 / committed-a-probability .15 / factor-coverage .15 / "
             "reputable-source-share .10).", "",
             "| id | kind | done | elapsed | steps | search | fetch | sources (rep) | prob? | coverage | answer-leak | score |",
             "|---|---|---|--:|--:|--:|--:|--:|:--:|:--:|---|--:|"]
    for r in rows:
        if r["answer_leak"] is None:
            leak = "—"
        elif r["answer_leak"]:
            leak = "LEAK: " + ",".join(r["answer_leak"])
        else:
            leak = f"clean ({r['post_result_sources']} src w/ result)"
        fin = "✓" if r["finished"] else ("timeout" if r["timed_out"] else "err")
        lines.append(
            f"| {r['id']} | {r['kind']} | {fin} | {r['elapsed_s']}s | {r['steps']} | "
            f"{r['web_search']} | {r['fetch']} | {r['sources']} ({r['reputable_sources']}) | "
            f"{'✓' if r['has_probability'] else '·'} | {r['coverage']} | {leak} | "
            f"**{r['trace_score']}** |")
    fin_n = sum(1 for r in rows if r["finished"])
    avg = round(sum(r["trace_score"] for r in rows) / len(rows), 2)
    lines += ["",
              f"**{len(rows)} runs · {fin_n} finished · mean trace_score {avg}**", "",
              "## What the leak probe actually showed", "",
              "- The past Euro-2024 question did **not** leak the result *in the answer* "
              "(`answer-leak: clean`) — the model gave a disciplined pre-kickoff forecast "
              "off pre-match odds. But its **source pool did** contain post-result and even "
              "wrong-event (Euro 2025 Women's final) material — `post_result_sources` counts it.",
              "- So leakage on a past event lives in the *retrieved sources and the model's "
              "latent knowledge*, not necessarily the prose. You cannot rely on it staying "
              "out of the answer at scale -> result-accuracy is still graded FORWARD only.",
              "- This grades process quality on data we already have; it does NOT claim the "
              "forecasts are calibrated (that needs forward grading on live fixtures)."]
    open(os.path.join(HERE, "EVAL.md"), "w").write("\n".join(lines) + "\n")
    print("\n".join(lines))
    print("\nWrote dataset/eval-results.json and dataset/EVAL.md")


if __name__ == "__main__":
    main()
