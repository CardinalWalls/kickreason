#!/usr/bin/env python3
"""
exp_concurrency.py — MEASURE the MiroMind hosted-API CONCURRENCY CEILING.

Why: the whole "overnight live-refresh" plan assumes we can fire ~50 deep-research
calls in parallel. If the hosted API throttles below that (429 / connection refused /
queueing that serializes), the refresh schedule dies. This is a KILL-SWITCH test.

Design (cost-disciplined — we are measuring the throttle, NOT researching):
  - Fire exactly 12 SHORT cheap calls CONCURRENTLY via threads.
  - Prompt: "Reply with only the word: ready"  (mini model, timeout 120s).
  - Per call capture: ok/fail, HTTP status (429=throttle is the signal), error text,
    latency, answer length, usage.
  - Compare total WALL-CLOCK vs SUM-of-latencies: if wall ~= max(latency) the calls
    truly ran in parallel; if wall ~= sum(latency) the server serialized us.

Bounded call count: 12. No retries (a retry would hide a throttle — we WANT the raw
first-attempt outcome). Stdlib only.

Run:  python3 dataset/exp_concurrency.py
Out:  dataset/runs/exp-concurrency.json
"""
import concurrent.futures as cf
import json
import os
import socket
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
API_URL = "https://api.miromind.ai/v1/chat/completions"

N_CALLS = 12
MODEL = "mirothinker-1-7-deepresearch-mini"
TIMEOUT = 120
PROMPT = "Reply with only the word: ready"


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        with open(p) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


KEY = load_key()


def one_call(idx):
    """One streaming call. Returns a result dict; never raises (captures all errors)."""
    body = json.dumps({
        "model": MODEL,
        "messages": [{"role": "user", "content": PROMPT}],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})

    content, usage = "", None
    http_status = None
    err = None
    timed_out = False
    t0 = time.time()
    t_first_byte = None
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            http_status = resp.status
            for raw in resp:
                if t_first_byte is None:
                    t_first_byte = round(time.time() - t0, 2)
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
                if delta.get("content"):
                    content += delta["content"]
                if obj.get("usage"):
                    usage = obj["usage"]
    except urllib.error.HTTPError as e:
        # THIS is the throttle signal: 429 Too Many Requests, 503, etc.
        http_status = e.code
        try:
            err_body = e.read().decode("utf-8", "replace")[:500]
        except Exception:  # noqa: BLE001
            err_body = ""
        err = f"HTTPError {e.code} {e.reason} :: {err_body}"
    except urllib.error.URLError as e:
        reason = getattr(e, "reason", e)
        if isinstance(reason, (socket.timeout, TimeoutError)) or "timed out" in str(reason).lower():
            timed_out = True
            err = f"URLError(timeout): {reason}"
        else:
            err = f"URLError: {reason}"
    except (socket.timeout, TimeoutError) as e:
        timed_out = True
        err = f"timeout: {e}"
    except Exception as e:  # noqa: BLE001
        if "timed out" in str(e).lower():
            timed_out = True
        err = f"{type(e).__name__}: {e}"
    elapsed = round(time.time() - t0, 2)

    ok = err is None and not timed_out and len(content) > 0
    return {
        "idx": idx,
        "ok": ok,
        "http_status": http_status,
        "timed_out": timed_out,
        "error": err,
        "latency_s": elapsed,
        "ttfb_s": t_first_byte,
        "answer_chars": len(content),
        "answer": content.strip()[:120],
        "empty_content": (err is None and not timed_out and len(content) == 0),
        "usage": usage,
    }


def main():
    if not KEY:
        out = {"verdict": "NO API KEY (.miroapi / MIROMIND_API_KEY) — cannot run.",
               "results": []}
        os.makedirs(RUNS, exist_ok=True)
        with open(os.path.join(RUNS, "exp-concurrency.json"), "w") as f:
            json.dump(out, f, indent=2)
        print(json.dumps(out["verdict"]))
        return

    print(f"Firing {N_CALLS} concurrent calls | model={MODEL} timeout={TIMEOUT}s "
          f"prompt={PROMPT!r} key=...{KEY[-6:]}", flush=True)

    wall0 = time.time()
    results = [None] * N_CALLS
    with cf.ThreadPoolExecutor(max_workers=N_CALLS) as ex:
        futs = {ex.submit(one_call, i): i for i in range(N_CALLS)}
        for fut in cf.as_completed(futs):
            r = fut.result()
            results[r["idx"]] = r
            tag = "OK " if r["ok"] else "XX "
            print(f"  [{tag}] call#{r['idx']:<2} {r['latency_s']:>6}s "
                  f"http={r['http_status']} to={r['timed_out']} "
                  f"chars={r['answer_chars']} err={r['error']}", flush=True)
    wall = round(time.time() - wall0, 2)

    lat = [r["latency_s"] for r in results]
    sum_lat = round(sum(lat), 2)
    max_lat = round(max(lat), 2) if lat else 0
    min_lat = round(min(lat), 2) if lat else 0
    n_ok = sum(1 for r in results if r["ok"])
    n_empty = sum(1 for r in results if r["empty_content"])
    n_timeout = sum(1 for r in results if r["timed_out"])
    n_429 = sum(1 for r in results if r["http_status"] == 429)
    n_5xx = sum(1 for r in results if r["http_status"] and 500 <= r["http_status"] < 600)
    n_other_err = sum(1 for r in results
                      if r["error"] and not r["timed_out"]
                      and r["http_status"] != 429
                      and not (r["http_status"] and 500 <= r["http_status"] < 600))

    # Parallelism judgement: if calls were SERIALIZED, wall ~ sum(lat). If TRULY
    # parallel, wall ~ max(lat). speedup = sum/wall ~ effective parallelism achieved.
    speedup = round(sum_lat / wall, 2) if wall > 0 else 0
    if wall <= max_lat * 1.5:
        parallel_judgement = "REAL PARALLELISM (wall ~ slowest call, not the sum)"
    elif wall >= sum_lat * 0.7:
        parallel_judgement = "SERIALIZED (wall ~ sum of latencies — server queued us)"
    else:
        parallel_judgement = "PARTIAL parallelism (between serialized and fully parallel)"

    # Verdict on the throttle ceiling.
    if n_429 > 0:
        ceiling_line = (f"THROTTLED: {n_429}/{N_CALLS} calls got HTTP 429 at "
                        f"concurrency={N_CALLS}. The ~50-parallel assumption FAILS.")
    elif n_5xx > 0 and n_ok < N_CALLS:
        ceiling_line = (f"SERVER ERRORS: {n_5xx}/{N_CALLS} got 5xx at concurrency={N_CALLS} "
                        f"(could be capacity/throttle). The ~50-parallel assumption is AT RISK.")
    elif n_ok == N_CALLS and "REAL" in parallel_judgement:
        ceiling_line = (f"NO THROTTLE at {N_CALLS}-parallel: all {N_CALLS} succeeded AND ran "
                        f"truly in parallel (speedup x{speedup}). Ceiling is ABOVE {N_CALLS}; "
                        f"~50 is plausible but UNPROVEN above {N_CALLS} — would need a bigger burst.")
    elif n_ok == N_CALLS:
        ceiling_line = (f"All {N_CALLS} succeeded but {parallel_judgement.lower()}. "
                        f"No hard error ceiling hit at {N_CALLS}, but throughput may be "
                        f"server-side queued, not free parallelism.")
    else:
        ceiling_line = (f"MIXED: {n_ok}/{N_CALLS} ok, {n_timeout} timeout, {n_empty} empty, "
                        f"{n_other_err} other-error at concurrency={N_CALLS}.")

    summary = {
        "experiment": "api-concurrency-ceiling",
        "n_calls": N_CALLS,
        "model": MODEL,
        "timeout_s": TIMEOUT,
        "prompt": PROMPT,
        "wall_clock_s": wall,
        "sum_latency_s": sum_lat,
        "min_latency_s": min_lat,
        "max_latency_s": max_lat,
        "speedup_vs_serial": speedup,
        "parallel_judgement": parallel_judgement,
        "n_ok": n_ok,
        "n_empty_content": n_empty,
        "n_timeout": n_timeout,
        "n_http_429": n_429,
        "n_http_5xx": n_5xx,
        "n_other_error": n_other_err,
        "ceiling_verdict": ceiling_line,
    }

    out = {"summary": summary, "results": results}
    os.makedirs(RUNS, exist_ok=True)
    with open(os.path.join(RUNS, "exp-concurrency.json"), "w") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)

    print("\n===== SUMMARY =====", flush=True)
    print(json.dumps(summary, indent=2), flush=True)
    print(f"\nSaved -> {os.path.join(RUNS, 'exp-concurrency.json')}", flush=True)


if __name__ == "__main__":
    main()
