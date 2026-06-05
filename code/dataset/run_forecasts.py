#!/usr/bin/env python3
"""
run_forecasts.py — REAL MiroMind deep-research API calls on forecasting questions.

This is the thing STATUS.md calls next-step #1: stop theorizing, run real questions,
capture what comes back (speed, the trace, the sources, the answer). Each run is saved
to dataset/runs/<id>.json with full trace + timing so eval_traces.py can score it.

Usage:
  python3 dataset/run_forecasts.py --smoke      # quick auth/shape check (~60s cap)
  python3 dataset/run_forecasts.py              # run the full batch (SLOW, minutes each)
Env: MIRO_MODEL, MIRO_TIMEOUT (s), MIRO_WORKERS, MIRO_ONLY=id1,id2
"""
import concurrent.futures as cf
import json
import os
import socket
import sys
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

SYSTEM = (
    "You are a calibrated sports forecaster in the tradition of professional "
    "forecasters and quant bettors. Forecasting is estimating a probability, not "
    "picking a winner. For the question: research the CURRENT evidence (recent form, "
    "injuries, squad/lineup news, schedule/rest, venue), then answer with — "
    "(1) calibrated probabilities that sum to ~100%; "
    "(2) 3 to 5 key factors that drive your estimate, EACH with the source you used; "
    "(3) the base rate or market price you started from and how far you moved off it; "
    "(4) what new information would most change the forecast. "
    "Reason only from information available as of the question's date; never assume a "
    "result you were not given."
)

# A spread across question types from dataset/questions.md: forward (genuinely
# unresolved -> a clean forecast) + one PAST event as a deliberate leakage probe.
QUESTIONS = [
    {"id": "wc26-winner", "kind": "forward",
     "q": "Who will win the 2026 FIFA World Cup? Give calibrated probabilities for the top 6-8 contenders.",
     "factors": ["title odds", "recent form", "squad", "draw path", "manager"]},
    {"id": "wc26-usa-advance", "kind": "forward",
     "q": "Will the United States men's national team advance from their group at the 2026 FIFA World Cup? Give a single probability and the key factors.",
     "factors": ["group draw", "opponents", "recent form", "injuries", "host advantage"]},
    {"id": "wc26-golden-boot", "kind": "forward",
     "q": "Who will win the Golden Boot (top scorer) at the 2026 FIFA World Cup? Give probabilities for the top candidates.",
     "factors": ["scorer odds", "penalties", "run depth", "recent form", "role"]},
    {"id": "wc26-spain-final", "kind": "forward",
     "q": "What is the probability that Spain reaches the final of the 2026 FIFA World Cup? Give the reasoning and key factors.",
     "factors": ["recent form", "squad", "draw path", "ranking"]},
    {"id": "euro24-final-leakprobe", "kind": "past", "kickoff": "2024-07-14",
     "q": "Forecast the result of the UEFA Euro 2024 final between Spain and England, played on 14 July 2024. As if it were before kickoff, give win/draw/loss probabilities using ONLY information available before that match, and cite your sources.",
     "factors": ["recent form", "injuries", "lineups", "suspensions", "route to final"]},
]


def stream_call(prompt, model, timeout):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})

    steps, sources, content, usage = [], [], "", None
    sid = 0
    timed_out = False
    err = None
    t0 = time.time()
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
                    content += delta["content"]
                if obj.get("usage"):
                    usage = obj["usage"]
    except Exception as e:  # noqa: BLE001 — capture partial on any failure
        if isinstance(e, (socket.timeout, TimeoutError)) or "timed out" in str(e).lower():
            timed_out = True
        else:
            err = f"{type(e).__name__}: {e}"
    elapsed = round(time.time() - t0, 1)

    seen, uniq = set(), []
    for s in sources:
        u = s.get("url")
        if u and u not in seen:
            seen.add(u)
            uniq.append(s)
    return {"content": content, "steps": steps, "sources": uniq, "usage": usage,
            "elapsed_s": elapsed, "timed_out": timed_out, "error": err}


def run_one(item, model, timeout):
    res = stream_call(item["q"], model, timeout)
    rec = dict(item)
    rec.update({"model": model})
    rec.update(res)
    os.makedirs(RUNS, exist_ok=True)
    with open(os.path.join(RUNS, item["id"] + ".json"), "w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)
    print(f"[done] {item['id']:24s} {res['elapsed_s']:>7}s  steps={len(res['steps']):<4} "
          f"src={len(res['sources']):<3} timeout={res['timed_out']} "
          f"err={res['error']} ans={len(res['content'])}chars", flush=True)
    return item["id"]


def main():
    if not KEY:
        print("NO API KEY found (.miroapi or MIROMIND_API_KEY). Aborting.", flush=True)
        sys.exit(2)
    model = os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini")

    if "--smoke" in sys.argv:
        print(f"SMOKE: {model}, key=...{KEY[-6:]}", flush=True)
        r = stream_call("Reply with only the word: ready", model, timeout=90)
        print(f"SMOKE result: elapsed={r['elapsed_s']}s timeout={r['timed_out']} "
              f"err={r['error']} steps={len(r['steps'])} ans={r['content'][:120]!r}", flush=True)
        return

    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    workers = int(os.environ.get("MIRO_WORKERS", "3"))
    only = os.environ.get("MIRO_ONLY", "")
    qs = [q for q in QUESTIONS if (not only or q["id"] in only.split(","))]
    print(f"Running {len(qs)} questions on {model} | timeout={timeout}s workers={workers}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(lambda it: run_one(it, model, timeout), qs))
    print("ALL DONE — now run: python3 dataset/eval_traces.py", flush=True)


if __name__ == "__main__":
    main()
