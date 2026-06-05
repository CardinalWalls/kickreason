#!/usr/bin/env python3
"""
ask.py — the demo, stripped to its core: ASK MiroMind one real question, watch it
reason (live, streaming: searches · fetches · thinking), get a sourced answer.

This IS the hackathon demo: a real MiroMind API call, transparent multi-step
reasoning, evidence/sources, an auditable judged answer. Nothing else.

  python3 dataset/ask.py "Will the USA advance from Group D at the 2026 World Cup?"

Streams the reasoning to your terminal as it happens, then saves the full trace +
answer + sources to dataset/runs/ask-<n>.json. Stdlib only.
"""
import json, os, socket, sys, time, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
API_URL = "https://api.miromind.ai/v1/chat/completions"
MODEL = os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini")

DEFAULT_Q = ("Will the United States men's national team advance from their group at the "
             "2026 FIFA World Cup? Give a single probability, the 3 key factors (each with a "
             "source), and your judgment.")


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        return open(p).readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


def ask(question, timeout=540):
    body = json.dumps({"model": MODEL, "messages": [{"role": "user", "content": question}]}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {load_key()}", "Content-Type": "application/json"})
    steps, sources, content, usage = [], [], "", None
    t0 = time.time()
    print(f"\nQ: {question}\n\n— MiroMind is reasoning (live) —\n", flush=True)
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
            delta = (obj.get("choices") or [{}])[0].get("delta", {})
            for s in delta.get("reasoning_steps", []):
                t = s.get("type")
                if t == "web_search":
                    kw = (s.get("web_search") or {}).get("search_keywords", [])
                    print(f"  🔎 search: {', '.join(kw) if isinstance(kw, list) else kw}", flush=True)
                    for r in (s.get("web_search") or {}).get("search_results", []):
                        if r.get("url"):
                            sources.append(r["url"])
                    steps.append({"action": "web_search", "keywords": kw})
                elif t == "fetch_url_content":
                    u = (s.get("fetch_url_content") or {}).get("url")
                    print(f"  📄 read:   {u}", flush=True)
                    if u:
                        sources.append(u)
                    steps.append({"action": "fetch", "url": u})
            if delta.get("content"):
                content += delta["content"]
            if obj.get("usage"):
                usage = obj["usage"]
    return {"q": question, "answer": content, "sources": sorted(set(sources)),
            "steps": steps, "usage": usage, "elapsed_s": round(time.time() - t0, 1),
            "n_search": sum(1 for s in steps if s["action"] == "web_search"),
            "n_fetch": sum(1 for s in steps if s["action"] == "fetch")}


def main():
    q = " ".join(sys.argv[1:]).strip() or DEFAULT_Q
    if not load_key():
        print("NO API KEY (.miroapi). Aborting.", flush=True); raise SystemExit(2)
    res = ask(q)
    if not res["answer"]:                       # ~1/6 empty — retry once
        print("  (empty return — retrying once)", flush=True)
        res = ask(q)
    runs = os.path.join(HERE, "runs"); os.makedirs(runs, exist_ok=True)
    n = 1 + len([f for f in os.listdir(runs) if f.startswith("ask-")])
    path = os.path.join(runs, f"ask-{n}.json")
    json.dump(res, open(path, "w"), indent=2, ensure_ascii=False)
    print(f"\n— ANSWER ({res['elapsed_s']}s · {res['n_search']} searches · {res['n_fetch']} fetches "
          f"· {len(res['sources'])} sources · {(res['usage'] or {}).get('total_tokens','?')} tokens) —\n", flush=True)
    print(res["answer"], flush=True)
    print(f"\nsaved full trace -> {os.path.relpath(path, HERE)}", flush=True)


if __name__ == "__main__":
    main()
