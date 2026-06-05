#!/usr/bin/env python3
"""
exp_api_probe.py — get FAMILIAR with the MiroMind API as an OPERATOR, for a
30k-50k-question intel business. One-shot answers are not the point; the point is
the numbers that decide whether a tens-of-thousands-of-questions, live-updating
business is even feasible on this API:

  - latency per call (it's MINUTES — the central constraint)
  - token cost per call (prompt / completion / reasoning) -> $ at 40k scale
  - can we CONTROL the output (a terse, structured, cheap mode) vs full deep research
  - mini vs full model: is the cheap model good enough?
  - how much real web work per call (searches / fetches) -> the decision-node intel

It fires a small matrix concurrently, captures everything, and prints a table plus
a back-of-envelope scale projection. Results -> dataset/runs/probe-*.json.

Usage:
  python3 dataset/exp_api_probe.py
Env: MIRO_TIMEOUT (s/call, default 540), MIRO_WORKERS (default 4)
"""
import concurrent.futures as cf
import json
import os
import socket
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
API_URL = "https://api.miromind.ai/v1/chat/completions"


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        with open(p) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


KEY = load_key()

FULL_SYS = (
    "You are a calibrated sports forecaster. Research current evidence (form, injuries, "
    "lineups, rest, venue), then give calibrated probabilities, 3-5 key factors each with "
    "its source, the market price you anchored to and how far you moved off it, and what "
    "would most change the forecast."
)
TERSE_SYS = (
    "You are a FAST football forecaster for a high-volume intel service. Output ONLY, in "
    "under 120 words: (1) the asked probabilities (must sum ~100%); (2) exactly 3 intel "
    "bullets, each ONE line ending with a source URL; (3) the market/odds line you "
    "anchored to. No preamble, no essay."
)

MINI = "mirothinker-1-7-deepresearch-mini"
FULL = "mirothinker-1-7-deepresearch"

# A matrix that isolates the variables that matter for scale.
MATRIX = [
    {"id": "probe-match-full",  "model": MINI, "sys": FULL_SYS,
     "q": "Forecast win/draw/loss for the opening match of the 2026 FIFA World Cup "
          "(Mexico at Estadio Azteca, 11 Jun 2026). Confirm the opponent first."},
    {"id": "probe-match-terse", "model": MINI, "sys": TERSE_SYS,
     "q": "Win/draw/loss for the 2026 FIFA World Cup opening match (Mexico at Estadio "
          "Azteca, 11 Jun 2026)."},
    {"id": "probe-advance-terse", "model": MINI, "sys": TERSE_SYS,
     "q": "Probability the USA men advance from their group at the 2026 FIFA World Cup?"},
    {"id": "probe-prop-terse", "model": MINI, "sys": TERSE_SYS,
     "q": "Top 5 most likely 2026 FIFA World Cup Golden Boot winners with probabilities."},
    {"id": "probe-match-fullmodel", "model": FULL, "sys": TERSE_SYS,
     "q": "Win/draw/loss for the 2026 FIFA World Cup opening match (Mexico at Estadio "
          "Azteca, 11 Jun 2026)."},
]


def stream_call(q, system, model, timeout):
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": system},
        {"role": "user", "content": q}]}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    steps, sources, content, usage = [], [], "", None
    nsearch = nfetch = 0
    timed_out, err = False, None
    t0 = time.time()
    ttfb = None
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                payload = line[5:].strip()
                if payload == "[DONE]":
                    break
                if ttfb is None:
                    ttfb = round(time.time() - t0, 1)
                try:
                    obj = json.loads(payload)
                except json.JSONDecodeError:
                    continue
                try:
                    delta = obj["choices"][0]["delta"]
                except (KeyError, IndexError):
                    delta = {}
                for s in delta.get("reasoning_steps", []):
                    t = s.get("type")
                    if t == "web_search":
                        nsearch += 1
                        ws = s.get("web_search") or {}
                        for r in ws.get("search_results", []):
                            sources.append(r.get("url"))
                    elif t == "fetch_url_content":
                        nfetch += 1
                        fu = s.get("fetch_url_content") or {}
                        if fu.get("url"):
                            sources.append(fu.get("url"))
                if delta.get("content"):
                    content += delta["content"]
                if obj.get("usage"):
                    usage = obj["usage"]
    except Exception as e:  # noqa: BLE001
        if isinstance(e, (socket.timeout, TimeoutError)) or "timed out" in str(e).lower():
            timed_out = True
        else:
            err = f"{type(e).__name__}: {e}"
    elapsed = round(time.time() - t0, 1)
    return {"content": content, "usage": usage, "nsearch": nsearch, "nfetch": nfetch,
            "nsources": len(set(s for s in sources if s)), "answer_chars": len(content),
            "elapsed_s": elapsed, "ttfb_s": ttfb, "timed_out": timed_out, "error": err}


def run_one(task, timeout):
    r = stream_call(task["q"], task["sys"], task["model"], timeout)
    rec = dict(task)
    rec.update(r)
    os.makedirs(RUNS, exist_ok=True)
    with open(os.path.join(RUNS, task["id"] + ".json"), "w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)
    u = r["usage"] or {}
    print(f"[done] {task['id']:24s} {r['elapsed_s']:>6}s ttfb={r['ttfb_s']}  "
          f"search={r['nsearch']:<2} fetch={r['nfetch']:<2} ans={r['answer_chars']:<5}c  "
          f"tok(p/c/r)={u.get('prompt_tokens','?')}/{u.get('completion_tokens','?')}/"
          f"{u.get('reasoning_tokens','?')}  to={r['timed_out']} err={r['error']}",
          flush=True)
    return rec


def main():
    if not KEY:
        print("NO API KEY. Aborting.", flush=True)
        raise SystemExit(2)
    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    workers = int(os.environ.get("MIRO_WORKERS", "4"))
    print(f"API PROBE | {len(MATRIX)} calls | timeout={timeout}s workers={workers}\n", flush=True)

    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        recs = list(ex.map(lambda t: run_one(t, timeout), MATRIX))

    # ---- scale projection from what we just measured (mini, terse mode) ----
    terse = [r for r in recs if r["model"] == MINI and "terse" in r["id"]
             and not r["timed_out"] and not r["error"] and r["usage"]]
    print("\n==== SCALE READ (mini, terse mode) ====", flush=True)
    if terse:
        avg_s = sum(r["elapsed_s"] for r in terse) / len(terse)
        avg_ct = sum((r["usage"] or {}).get("completion_tokens", 0) for r in terse) / len(terse)
        avg_rt = sum((r["usage"] or {}).get("reasoning_tokens", 0) or 0 for r in terse) / len(terse)
        avg_pt = sum((r["usage"] or {}).get("prompt_tokens", 0) for r in terse) / len(terse)
        print(f"avg latency:        {avg_s:.0f}s/call", flush=True)
        print(f"avg tokens p/c/r:   {avg_pt:.0f}/{avg_ct:.0f}/{avg_rt:.0f}", flush=True)
        for N in (30000, 50000):
            for C in (20, 100):
                hours = N * avg_s / C / 3600
                print(f"  {N:,} questions @ concurrency {C:<3} -> "
                      f"{hours:,.0f} compute-hours (one full refresh)", flush=True)
        print("NOTE: that's ONE refresh. Live 舆情 updating = many refreshes/day on the "
              "high-value subset -> the long tail MUST be cheaper/cached/templated.",
              flush=True)
    else:
        print("no clean terse samples (timeouts/errors) — rerun or raise timeout", flush=True)

    with open(os.path.join(RUNS, "probe-summary.json"), "w") as f:
        json.dump(recs, f, indent=2, ensure_ascii=False)
    print(f"\nsaved -> {os.path.join(RUNS, 'probe-summary.json')}", flush=True)


if __name__ == "__main__":
    main()
