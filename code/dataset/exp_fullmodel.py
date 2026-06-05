#!/usr/bin/env python3
"""
exp_fullmodel.py — FULL-MODEL ECONOMICS experiment.

Kill-switch under test: is the FULL model (mirothinker-1-7-deepresearch) affordable
for a Tier-A catalog, or must the catalog run on the mini? We only ever had ONE
full-model data point (probe-match-fullmodel.json: 228s / 184k tokens on the opening
match). This runs 3 distinct FORWARD forecast questions on the full model and captures,
per call: elapsed, ttfb, usage (prompt/completion/total + reasoning tokens),
#search, #fetch, #sources. Then it computes the full-vs-mini multiplier.

Design notes (matches the GROUND-TRUTH constraints):
  - FULL model only, timeout 540s, retry-once when content comes back EMPTY
    (~1 in 6 calls returns empty; one retry is the documented mitigation).
  - 3 DISTINCT question kinds: a MATCH (w/d/l), a TEAM-ADVANCE, a PLAYER-PROP.
    These are the three shapes a real catalog runs, so latency/cost generalise.
  - Same TERSE "FAST forecaster" system prompt the full-model probe used, so the
    full-vs-mini comparison is apples-to-apples (same workload, only model differs).
  - Saves each call to runs/exp-fullmodel-<id>.json and a roll-up
    runs/exp-fullmodel-summary.json with the verdict inputs.

Bounded cost: exactly 3 questions x (1 + up-to-1 retry) = at most 6 full-model calls.

Usage:
  python3 dataset/exp_fullmodel.py
Env: MIRO_TIMEOUT (default 540), MIRO_WORKERS (default 3; lower if throttled).
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
FULL_MODEL = "mirothinker-1-7-deepresearch"
MINI_MODEL = "mirothinker-1-7-deepresearch-mini"


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        with open(p) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


KEY = load_key()

# The terse, high-volume catalog system prompt — identical in spirit to the one
# the existing probe-match-fullmodel.json used, so the comparison is fair.
SYSTEM = (
    "You are a FAST football forecaster for a high-volume intel service. Output "
    "ONLY, in under 120 words: (1) the asked probabilities (must sum ~100%); "
    "(2) exactly 3 intel bullets, each ONE line ending with a source URL; "
    "(3) the market/odds line you anchored to. No preamble, no essay. Reason only "
    "from information available as of the question's date; never assume a result "
    "you were not given."
)

# 3 distinct forward question SHAPES — match / team-advance / player-prop.
QUESTIONS = [
    {"id": "match", "kind": "match",
     "q": "Win/draw/loss probabilities for the 2026 FIFA World Cup group match "
          "Argentina vs Mexico. Give the three probabilities (sum ~100%)."},
    {"id": "advance", "kind": "team-advance",
     "q": "Probability that Brazil advances from its group at the 2026 FIFA World "
          "Cup. Give a single probability and the anchor odds."},
    {"id": "prop", "kind": "player-prop",
     "q": "Probability that Kylian Mbappe scores 3 or more goals across the 2026 "
          "FIFA World Cup group stage. Give a single probability and the anchor."},
]

# Known mini baselines (measured, prior session) for the multiplier.
# Same-Q full-vs-mini reference: the opening-match probe was 52s/88k on mini.
MINI_SAME_Q = {"elapsed_s": 52.0, "total_tokens": 88000}
# Forward-batch mini median latency (the catalog-relevant number).
MINI_FORWARD_MEDIAN_S = 240.0


def stream_call(prompt, model, timeout):
    body = json.dumps({
        "model": model,
        "messages": [{"role": "system", "content": SYSTEM},
                     {"role": "user", "content": prompt}],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})

    content, usage = "", None
    nsearch = nfetch = 0
    sources = []
    ttfb = None
    timed_out = False
    err = None
    t0 = time.time()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            for raw in resp:
                line = raw.decode("utf-8", "replace").strip()
                if not line.startswith("data:"):
                    continue
                if ttfb is None:
                    ttfb = round(time.time() - t0, 1)
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
                    if t == "web_search":
                        nsearch += 1
                        ws = s.get("web_search") or {}
                        for r in ws.get("search_results", []):
                            if r.get("url"):
                                sources.append(r["url"])
                    elif t == "fetch_url_content":
                        nfetch += 1
                        fu = s.get("fetch_url_content") or {}
                        if fu.get("url"):
                            sources.append(fu["url"])
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
    return {
        "content": content,
        "usage": usage,
        "nsearch": nsearch,
        "nfetch": nfetch,
        "nsources": len(set(sources)),
        "answer_chars": len(content),
        "elapsed_s": elapsed,
        "ttfb_s": ttfb,
        "timed_out": timed_out,
        "error": err,
    }


def run_one(item, timeout):
    res = stream_call(item["q"], FULL_MODEL, timeout)
    retried = False
    # ~1 in 6 calls returns EMPTY content -> retry once.
    if not res["content"].strip() and not res["timed_out"]:
        retried = True
        print(f"[retry] {item['id']}: empty content, retrying once", flush=True)
        res = stream_call(item["q"], FULL_MODEL, timeout)
    rec = dict(item)
    rec["model"] = FULL_MODEL
    rec["sys"] = SYSTEM
    rec["retried_empty"] = retried
    rec.update(res)
    os.makedirs(RUNS, exist_ok=True)
    path = os.path.join(RUNS, f"exp-fullmodel-{item['id']}.json")
    with open(path, "w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)
    u = res["usage"] or {}
    print(f"[done] {item['id']:14s} {res['elapsed_s']:>7}s  ttfb={res['ttfb_s']}  "
          f"tot_tok={u.get('total_tokens')}  search={res['nsearch']} fetch={res['nfetch']} "
          f"src={res['nsources']}  retry={retried}  timeout={res['timed_out']} "
          f"err={res['error']}  ans={res['answer_chars']}chars", flush=True)
    return rec


def median(xs):
    xs = sorted(xs)
    n = len(xs)
    if not n:
        return None
    m = n // 2
    return xs[m] if n % 2 else (xs[m - 1] + xs[m]) / 2.0


def main():
    if not KEY:
        print("NO API KEY found (.miroapi or MIROMIND_API_KEY). Aborting.", flush=True)
        sys.exit(2)
    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    workers = int(os.environ.get("MIRO_WORKERS", "3"))
    print(f"FULL-MODEL ECONOMICS: {len(QUESTIONS)} forward Qs on {FULL_MODEL} | "
          f"timeout={timeout}s workers={workers} | retry-once-on-empty", flush=True)

    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        recs = list(ex.map(lambda it: run_one(it, timeout), QUESTIONS))
    wall = round(time.time() - t0, 1)

    ok = [r for r in recs if r["content"].strip() and not r["timed_out"]]
    lat = [r["elapsed_s"] for r in ok]
    toks = [(r["usage"] or {}).get("total_tokens") for r in ok]
    toks = [t for t in toks if t is not None]
    ptoks = [(r["usage"] or {}).get("prompt_tokens") for r in ok]
    ptoks = [t for t in ptoks if t is not None]
    ctoks = [(r["usage"] or {}).get("completion_tokens") for r in ok]
    ctoks = [t for t in ctoks if t is not None]

    med_lat = median(lat)
    med_tok = median(toks)

    # Multipliers vs the known mini profiles.
    lat_mult_same_q = round(med_lat / MINI_SAME_Q["elapsed_s"], 1) if med_lat else None
    tok_mult_same_q = round(med_tok / MINI_SAME_Q["total_tokens"], 1) if med_tok else None
    lat_mult_forward = round(med_lat / MINI_FORWARD_MEDIAN_S, 1) if med_lat else None

    summary = {
        "experiment": "full-model-economics",
        "model": FULL_MODEL,
        "n_questions": len(QUESTIONS),
        "n_ok": len(ok),
        "n_timed_out": sum(1 for r in recs if r["timed_out"]),
        "n_retried_empty": sum(1 for r in recs if r.get("retried_empty")),
        "wall_clock_s": wall,
        "workers": workers,
        "per_call": [
            {"id": r["id"], "kind": r["kind"], "elapsed_s": r["elapsed_s"],
             "ttfb_s": r["ttfb_s"], "usage": r["usage"], "nsearch": r["nsearch"],
             "nfetch": r["nfetch"], "nsources": r["nsources"],
             "answer_chars": r["answer_chars"], "retried_empty": r.get("retried_empty"),
             "timed_out": r["timed_out"], "error": r["error"]}
            for r in recs
        ],
        "full_model_profile": {
            "latency_s": {"values": lat, "median": med_lat,
                          "min": min(lat) if lat else None,
                          "max": max(lat) if lat else None},
            "prompt_tokens": {"values": ptoks, "median": median(ptoks)},
            "completion_tokens": {"values": ctoks, "median": median(ctoks)},
            "total_tokens": {"values": toks, "median": med_tok,
                             "min": min(toks) if toks else None,
                             "max": max(toks) if toks else None},
        },
        "mini_baseline": {
            "same_q": MINI_SAME_Q,
            "forward_median_s": MINI_FORWARD_MEDIAN_S,
            "prior_full_model_point": {"elapsed_s": 228.3, "total_tokens": 184315,
                                       "note": "probe-match-fullmodel.json"},
        },
        "full_vs_mini": {
            "latency_multiplier_same_q_basis": lat_mult_same_q,
            "token_multiplier_same_q_basis": tok_mult_same_q,
            "latency_multiplier_vs_forward_median": lat_mult_forward,
        },
    }
    with open(os.path.join(RUNS, "exp-fullmodel-summary.json"), "w") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n==== FULL-MODEL ECONOMICS SUMMARY ====", flush=True)
    print(json.dumps(summary["full_model_profile"], indent=2), flush=True)
    print(json.dumps(summary["full_vs_mini"], indent=2), flush=True)
    print(f"ok={len(ok)}/{len(QUESTIONS)} timeouts={summary['n_timed_out']} "
          f"retries={summary['n_retried_empty']} wall={wall}s", flush=True)
    print("Saved: runs/exp-fullmodel-*.json + runs/exp-fullmodel-summary.json", flush=True)


if __name__ == "__main__":
    main()
