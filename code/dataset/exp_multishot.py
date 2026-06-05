#!/usr/bin/env python3
"""
exp_multishot.py — THE experiment the whole thesis rests on.

Question under test: does a SECOND, adversarial pass move MiroMind's forecast OFF
the public consensus *with cited evidence* — or does it just repeat the consensus /
hand-wave? One-shot calls so far look like a de-vig of the public market (no edge).
If multi-shot can't produce sourced, defensible movement, then there is no verifiable
"edge" to build ANY prediction product on. NOTE: buyer and product are still UNDECIDED
(not a betting desk, not anything yet) — this probe commits to nothing. It only asks
what the agent CAN do. Capability probe, not a track-record entry.

What it does, on ONE real upcoming fixture:
  Shot 1 (baseline)   : ask for a calibrated forecast (expected: market de-vig).
  Shot 2 (challenger) : SAME conversation, append the baseline answer + a hard
                        adversarial turn that demands sourced movement OR an
                        explicit "market is efficient here" verdict.
Then it saves both turns (full trace + sources + timing) and prints a compact
read so we can judge: did it move? were moves backed by NEW web_search/fetch?

Usage:
  python3 dataset/exp_multishot.py            # run it (SLOW: two sequential calls)
  MIRO_MODEL=mirothinker-1-7-deepresearch python3 dataset/exp_multishot.py   # big model
Env: MIRO_MODEL, MIRO_TIMEOUT (s, per call), FIXTURE (override the match string)
"""
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

SYSTEM = (
    "You are a calibrated sports forecaster in the tradition of professional "
    "forecasters and quant bettors. Forecasting is estimating a probability, not "
    "picking a winner. Research CURRENT evidence (recent form, injuries, squad/lineup "
    "news, schedule/rest, venue), then answer with — (1) calibrated win/draw/loss "
    "probabilities that sum to ~100%; (2) 3-5 key factors, EACH with its source; "
    "(3) the market price you started from and how far you moved off it; (4) what new "
    "information would most change the forecast. Reason only from information available "
    "now; never assume a result."
)

# The adversarial second turn. This is the heart of the experiment.
CHALLENGE = (
    "Your forecast above mostly reflects the betting-market consensus. Now switch role: "
    "you are a sharp, skeptical bettor whose ONLY job is to BEAT THE CLOSING LINE on this "
    "exact match. Go find specific, recent, SOURCED evidence the market may be slow to "
    "price: confirmed/likely starting XI, injuries, suspensions, fatigue/travel/rest, "
    "motivation (dead rubber, rotation, must-win), tactical matchup, weather, venue, "
    "referee. Then deliver:\n"
    "(a) your FINAL win/draw/loss probabilities;\n"
    "(b) the market probabilities you started from;\n"
    "(c) for EACH outcome, the exact percentage-point move and the SPECIFIC cited reason "
    "for it;\n"
    "(d) if, after researching, you find no genuine edge, say plainly 'the market is "
    "efficient here' and DO NOT move the numbers.\n"
    "Hard rule: do not move any probability without a cited, match-specific reason. "
    "Vague narrative is not a reason."
)

# A real, soon-gradable fixture: the 2026 World Cup opener. Override with FIXTURE env.
FIXTURE = os.environ.get(
    "FIXTURE",
    "the opening match of the 2026 FIFA World Cup (Mexico's group-stage opener at "
    "Estadio Azteca, Mexico City, on 11 June 2026). First confirm the actual opponent "
    "and kickoff, then forecast win/draw/loss for Mexico in that match",
)
BASE_Q = f"Forecast {FIXTURE}."


def stream_messages(messages, model, timeout):
    body = json.dumps({"model": model, "messages": messages}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    steps, sources, content, usage = [], [], "", None
    sid = 0
    timed_out, err = False, None
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
    except Exception as e:  # noqa: BLE001
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


def counts(turn):
    ws = sum(1 for s in turn["steps"] if s["action"] == "web_search")
    fe = sum(1 for s in turn["steps"] if s["action"] == "fetch")
    return ws, fe


def main():
    if not KEY:
        print("NO API KEY. Aborting.", flush=True)
        raise SystemExit(2)
    model = os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini")
    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    print(f"EXP multishot | model={model} timeout={timeout}s/call", flush=True)
    print(f"FIXTURE: {FIXTURE}", flush=True)

    # --- Shot 1: baseline ---
    print("\n[1/2] baseline forecast ...", flush=True)
    base_msgs = [{"role": "system", "content": SYSTEM},
                 {"role": "user", "content": BASE_Q}]
    base = stream_messages(base_msgs, model, timeout)
    bws, bfe = counts(base)
    print(f"[1/2] done {base['elapsed_s']}s  search={bws} fetch={bfe} "
          f"src={len(base['sources'])} timeout={base['timed_out']} err={base['error']} "
          f"ans={len(base['content'])}chars", flush=True)

    # --- Shot 2: adversarial challenger, SAME conversation ---
    print("\n[2/2] adversarial challenger (multi-turn) ...", flush=True)
    chal_msgs = base_msgs + [
        {"role": "assistant", "content": base["content"] or "(no answer returned)"},
        {"role": "user", "content": CHALLENGE},
    ]
    chal = stream_messages(chal_msgs, model, timeout)
    cws, cfe = counts(chal)
    print(f"[2/2] done {chal['elapsed_s']}s  search={cws} fetch={cfe} "
          f"src={len(chal['sources'])} timeout={chal['timed_out']} err={chal['error']} "
          f"ans={len(chal['content'])}chars", flush=True)

    base_urls = {s["url"] for s in base["sources"]}
    new_urls = [s for s in chal["sources"] if s["url"] not in base_urls]

    rec = {
        "id": "exp-multishot-wc26-opener",
        "kind": "capability-probe",
        "fixture": FIXTURE,
        "model": model,
        "question": BASE_Q,
        "challenge": CHALLENGE,
        "baseline": base,
        "challenger": chal,
        "summary": {
            "baseline_searches": bws, "baseline_fetches": bfe,
            "challenger_searches": cws, "challenger_fetches": cfe,
            "challenger_new_sources": len(new_urls),
            "multiturn_worked": bool(chal["content"]) and not chal["error"],
        },
    }
    os.makedirs(RUNS, exist_ok=True)
    out = os.path.join(RUNS, rec["id"] + ".json")
    with open(out, "w") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)

    print("\n==== READ ====", flush=True)
    print(f"multi-turn worked: {rec['summary']['multiturn_worked']}", flush=True)
    print(f"challenger did NEW web research: {len(new_urls)} new sources "
          f"({cws} searches, {cfe} fetches)", flush=True)
    print(f"saved -> {out}", flush=True)
    print("Next: read the two .content blocks and judge — did the number MOVE, "
          "and was the move tied to cited, match-specific evidence?", flush=True)


if __name__ == "__main__":
    main()
