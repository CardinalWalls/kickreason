#!/usr/bin/env python3
"""
narrative.py — get the NARRATIVE GRAIN the dream demo needs.

The dream: "not only the scoreline, but the KEY NARRATIVE", replayed against a game's
MAGIC MOMENT. Our current nodes are mostly odds-echoes (L0 grain) — they give a
probability, not a story. This run asks the MiroMind API for the L1 NARRATIVE grain:
the tactical/human storylines that decide a match, NOT the odds. It also breaks the
evidence monoculture for the live fixture.

Two real calls -> dataset/runs/narrative-*.json (full trace + sources):
  1. a resolved MAGIC-MOMENT game (Saudi 2-1 Argentina, WC2022) — the narrative the
     market missed, so we can pair it with the real moment (Al-Dawsari 53') + the grade.
  2. the forward fixture (USMNT advance) — narrative storylines, NOT odds (anti-monoculture).

Run:  python3 dataset/narrative.py
Env:  MIRO_MODEL, MIRO_TIMEOUT (s), MIRO_WORKERS
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

SYSTEM = (
    "You are a football analyst extracting the KEY NARRATIVE of a match — the tactical "
    "and human storylines that decide it, NOT the betting odds and NOT a bare scoreline. "
    "Research, then give 3-5 DISTINCT narrative factors. For EACH: (1) a one-sentence "
    "storyline; (2) why it mattered / will matter; (3) the source URL. Hard rule: do not "
    "restate betting odds or implied probabilities — those are not narrative. Each factor "
    "must be a different story (tactics, key player, motivation, game-state turning point), "
    "not the same point reworded."
)

QUESTIONS = [
    {"id": "narrative-sau-arg-2022", "kind": "resolved-magic-moment",
     "q": "Analyze Saudi Arabia's 2-1 upset of Argentina at the 2022 FIFA World Cup "
          "(group stage). What were the KEY NARRATIVE factors and tactical storylines that "
          "decided it — e.g. Saudi Arabia's aggressive high defensive/offside line, "
          "Argentina's blanked second-half attack, the Saudi surge right after halftime, "
          "the goalkeeping? Give the distinct storylines, each with a source. Identify the "
          "decisive 'magic moment' (the goal that turned it) and who scored it."},
    {"id": "narrative-usa-advance", "kind": "forward",
     "q": "For the 2026 FIFA World Cup, what are the KEY NARRATIVES and storylines (NOT "
          "odds) that will decide whether the USA advance from Group D — tactical setup, "
          "key players, motivation/host pressure, the specific threat each of Paraguay, "
          "Australia and Türkiye poses? Give the distinct storylines, each with a source."},
]


def stream_call(prompt, model, timeout):
    body = json.dumps({"model": model, "messages": [
        {"role": "system", "content": SYSTEM},
        {"role": "user", "content": prompt}]}).encode()
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
    seen, uniq = set(), []
    for s in sources:
        u = s.get("url")
        if u and u not in seen:
            seen.add(u)
            uniq.append(s)
    return {"content": content, "steps": steps, "sources": uniq, "usage": usage,
            "elapsed_s": round(time.time() - t0, 1), "timed_out": timed_out, "error": err}


def run_one(item, model, timeout):
    res = stream_call(item["q"], model, timeout)
    if not res["content"] and not res["error"] and not res["timed_out"]:
        res = stream_call(item["q"], model, timeout)        # retry the ~1-in-6 empty
    rec = dict(item)
    rec.update({"model": model})
    rec.update(res)
    os.makedirs(RUNS, exist_ok=True)
    with open(os.path.join(RUNS, item["id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(rec, f, indent=2, ensure_ascii=False)
    nsearch = sum(1 for s in res["steps"] if s["action"] == "web_search")
    print(f"[done] {item['id']:28s} {res['elapsed_s']:>6}s  search={nsearch} "
          f"src={len(res['sources'])} ans={len(res['content'])}c "
          f"timeout={res['timed_out']} err={res['error']}", flush=True)
    return item["id"]


def main():
    if not KEY:
        print("NO API KEY. Aborting.", flush=True)
        raise SystemExit(2)
    model = os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini")
    timeout = int(os.environ.get("MIRO_TIMEOUT", "480"))
    workers = int(os.environ.get("MIRO_WORKERS", "2"))      # 2 < 5 QPS, safe
    print(f"NARRATIVE GRAIN | {len(QUESTIONS)} calls | model={model} timeout={timeout}s", flush=True)
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(lambda it: run_one(it, model, timeout), QUESTIONS))
    print("DONE -> dataset/runs/narrative-*.json  (next: extract L1 narrative-grain nodes)", flush=True)


if __name__ == "__main__":
    main()
