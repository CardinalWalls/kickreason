#!/usr/bin/env python3
"""
exp_update_latency.py — POST-NEWS UPDATE LATENCY kill-switch test.

The edge of the whole business is the window AFTER team-news breaks and BEFORE the
market corrects. This measures the ONE number that decides whether that edge is real
for us: end-to-end latency from "a breaking-news line lands" to "a moved forecast is
in hand" — using a single mini deep-research call.

Bound: at most 2 API calls (1 + retry-once on EMPTY/timeout). Mini model only.

Scenario (simulated, so no result leakage):
  Base question:  pre-match win/draw/loss probability for a fixture.
  Breaking news:  "BREAKING: [team]'s key striker ruled out 1h before kickoff."
  Ask for:        the REVISED probability + a one-line reason + a source.

We measure wall-clock from the instant we "receive" the news (t_news) to the instant
the moved forecast is fully streamed back (t_answer). That gap is what has to fit
inside the post-news correction window.

Usage:
  python3 dataset/exp_update_latency.py
Env: MIRO_TIMEOUT (default 300)

Reuses the stream_call SSE pattern from dataset/run_forecasts.py and compiler/miro.py.
"""
import json
import os
import socket
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
OUT = os.path.join(RUNS, "exp-update-latency.json")
API_URL = "https://api.miromind.ai/v1/chat/completions"
MODEL = "mirothinker-1-7-deepresearch-mini"


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        with open(p) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


KEY = load_key()

# Concrete, plausible fixture + a simulated breaking-news line. Simulated on purpose:
# we are timing the UPDATE round-trip, not forecasting a real game, and we must not
# leak a result. The model is told to treat the news as just-confirmed and revise.
TEAM = "Brazil"
FIXTURE = "Brazil vs Croatia (2026 FIFA World Cup group stage)"
NEWS = f"BREAKING: {TEAM}'s key striker is ruled out, confirmed 1 hour before kickoff."

PROMPT = (
    f"Treat this as a live in-running forecast update for the fixture: {FIXTURE}.\n\n"
    f"News just confirmed (treat as true, ~1 hour before kickoff): {NEWS}\n\n"
    "You are updating a pre-existing win/draw/loss forecast in light of this single "
    "piece of team news. Be fast and decisive. Answer in EXACTLY this shape and "
    "nothing else:\n"
    f"REVISED: {TEAM} win XX% / draw XX% / opponent win XX% (must sum to ~100)\n"
    "REASON: <one line on how the striker being out moved the number>\n"
    "SOURCE: <one URL or named source backing the striker's absence or its impact>\n"
)


def stream_call(prompt, model, timeout):
    """One streaming MiroMind call. Captures partial output on any failure."""
    body = json.dumps({
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})

    steps, sources, content, usage = [], [], "", None
    sid = 0
    timed_out = False
    err = None
    t0 = time.time()
    t_first = None  # time-to-first-byte: when the model first emits anything
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                try:
                    delta = obj["choices"][0]["delta"]
                except (KeyError, IndexError):
                    delta = {}
                for s in delta.get("reasoning_steps", []):
                    if t_first is None:
                        t_first = time.time()
                    t = s.get("type")
                    if t == "thinking":
                        sid += 1
                        steps.append({"i": sid, "action": "thinking",
                                      "text": str(s.get("thought", ""))[:400]})
                    elif t == "web_search":
                        ws = s.get("web_search") or {}
                        sid += 1
                        steps.append({"i": sid, "action": "web_search",
                                      "keywords": ws.get("search_keywords", [])})
                        for r in ws.get("search_results", []):
                            sources.append({"url": r.get("url"), "title": r.get("title")})
                    elif t == "fetch_url_content":
                        fu = s.get("fetch_url_content") or {}
                        sid += 1
                        steps.append({"i": sid, "action": "fetch", "url": fu.get("url"),
                                      "snippet": str(fu.get("snippet", ""))[:240]})
                        if fu.get("url"):
                            sources.append({"url": fu.get("url"), "title": "(fetched)"})
                if delta.get("content"):
                    if t_first is None:
                        t_first = time.time()
                    content += delta["content"]
                if obj.get("usage"):
                    usage = obj["usage"]
    except Exception as e:  # noqa: BLE001 — capture partial on any failure
        if isinstance(e, (socket.timeout, TimeoutError)) or "timed out" in str(e).lower():
            timed_out = True
        else:
            err = f"{type(e).__name__}: {e}"
    elapsed = round(time.time() - t0, 1)
    ttfb = round(t_first - t0, 1) if t_first else None

    seen, uniq = set(), []
    for s in sources:
        u = s.get("url")
        if u and u not in seen:
            seen.add(u)
            uniq.append(s)
    return {"content": content, "steps": steps, "sources": uniq, "usage": usage,
            "elapsed_s": elapsed, "ttfb_s": ttfb, "timed_out": timed_out, "error": err}


def is_empty(res):
    """The known ~1-in-6 EMPTY-content failure mode, or a timeout/error."""
    return (not res["content"].strip()) or res["timed_out"] or res["error"]


def main():
    if not KEY:
        print("NO API KEY found (.miroapi or MIROMIND_API_KEY). Aborting.", flush=True)
        return 2
    timeout = int(os.environ.get("MIRO_TIMEOUT", "300"))
    os.makedirs(RUNS, exist_ok=True)

    print(f"EXPERIMENT post-news update latency | {MODEL} | timeout={timeout}s", flush=True)
    print(f"  fixture: {FIXTURE}", flush=True)
    print(f"  news:    {NEWS}", flush=True)

    # t_news = the moment the breaking line lands and we kick off the update call.
    attempts = []
    t_news = time.time()

    res = stream_call(PROMPT, MODEL, timeout)
    attempts.append({"attempt": 1, **{k: res[k] for k in
                     ("elapsed_s", "ttfb_s", "timed_out", "error")},
                     "answer_chars": len(res["content"])})
    print(f"[attempt 1] elapsed={res['elapsed_s']}s ttfb={res['ttfb_s']}s "
          f"timeout={res['timed_out']} err={res['error']} ans={len(res['content'])}chars",
          flush=True)

    if is_empty(res):
        print("[retry] attempt 1 EMPTY/timeout/err -> retrying once", flush=True)
        res = stream_call(PROMPT, MODEL, timeout)
        attempts.append({"attempt": 2, **{k: res[k] for k in
                         ("elapsed_s", "ttfb_s", "timed_out", "error")},
                         "answer_chars": len(res["content"])})
        print(f"[attempt 2] elapsed={res['elapsed_s']}s ttfb={res['ttfb_s']}s "
              f"timeout={res['timed_out']} err={res['error']} ans={len(res['content'])}chars",
              flush=True)

    # End-to-end latency: from news landing to a moved forecast in hand. Includes the
    # retry if one happened — that is the HONEST cost of the ~1-in-6 EMPTY failure.
    latency_s = round(time.time() - t_news, 1)
    moved_forecast_in_hand = (not is_empty(res))

    # Verdict bands (typical post-news correction windows):
    #   late lineup (~1h pre-kickoff): minutes to ~1h before odds fully settle
    #   in-running / injury mid-game: seconds to a few minutes
    mins = latency_s / 60.0
    if not moved_forecast_in_hand:
        verdict = "FAIL — no moved forecast returned (empty/timeout even after retry)"
    elif latency_s <= 120:
        verdict = ("PASS — fits even the tighter late-lineup window; comfortably "
                   "inside the typical hours-long pre-kickoff correction window")
    elif latency_s <= 600:
        verdict = ("CONDITIONAL PASS — fits the common pre-kickoff window (news often "
                   "breaks ~1h out, odds take many minutes to fully move); TOO SLOW for "
                   "fast in-running/seconds-scale corrections")
    else:
        verdict = ("MARGINAL — slower than typical late-lineup reaction; only usable "
                   "when the correction window is the slow hours-long kind")

    record = {
        "experiment": "post-news update latency",
        "model": MODEL,
        "timeout_s": timeout,
        "fixture": FIXTURE,
        "breaking_news": NEWS,
        "prompt": PROMPT,
        "attempts": attempts,
        "n_calls": len(attempts),
        "latency_news_to_moved_forecast_s": latency_s,
        "latency_min": round(mins, 2),
        "ttfb_s": res["ttfb_s"],
        "moved_forecast_in_hand": moved_forecast_in_hand,
        "verdict": verdict,
        "answer": res["content"],
        "sources": res["sources"],
        "n_steps": len(res["steps"]),
        "usage": res["usage"],
    }
    with open(OUT, "w") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print("\n=== RESULT ===", flush=True)
    print(f"latency (news -> moved forecast in hand): {latency_s}s ({mins:.2f} min) "
          f"over {len(attempts)} call(s)", flush=True)
    print(f"moved forecast in hand: {moved_forecast_in_hand}", flush=True)
    print(f"VERDICT: {verdict}", flush=True)
    print(f"\nanswer:\n{res['content'][:600]}", flush=True)
    print(f"\nsaved -> {OUT}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
