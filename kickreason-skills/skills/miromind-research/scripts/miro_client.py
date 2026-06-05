"""
miro.py — the ONE LLM plug-in point: the MiroMind hosted deep-research API.

In TOWOW terms this is the Agent-内部循环 (third loop): a semantic task is 降维'd into
低维执行 and returns typed slices. The compiler's job is NOT this call — it is the
升维存储 around it. So the whole pipeline makes exactly ONE MiroMind call (enrichment);
everything else is deterministic (extract.py / wow.py / trust.py).

Verified API shape (live, 2026-06-04):
  POST https://api.miromind.ai/v1/chat/completions  (OpenAI-compatible, SSE)
  models: mirothinker-1-7-deepresearch-mini | mirothinker-1-7-deepresearch
  each SSE chunk: choices[0].delta.reasoning_steps[] of typed steps:
    {type:"thinking", thought}
    {type:"web_search", web_search:{search_keywords[], search_results:[{title,snippet,url}]}}
    {type:"fetch_url_content", fetch_url_content:{url, snippet}}
  final answer in delta.content; last chunk has usage incl reasoning_tokens.

NOTE: it is SLOW (a multi-part query ran 9+ min and did not finish at a 560s cap).
So this client is OPTIONAL in the bootstrap: the deterministic artifact stands without
it; when it returns it enriches `steps[]` + the intent ledger.
"""
import json
import os
import urllib.request

API_URL = "https://api.miromind.ai/v1/chat/completions"

def _load_key(key_path):
    if os.path.exists(key_path):
        with open(key_path) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")

def call(prompt, model="mirothinker-1-7-deepresearch-mini",
         key_path=None, timeout=540, system=None):
    """One streaming MiroMind call. Returns {content, steps, sources, raw_steps, usage}."""
    key = _load_key(key_path or os.path.expanduser(
        os.path.join(os.path.dirname(__file__), "..", ".miroapi")))
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": prompt})
    body = json.dumps({"model": model, "messages": msgs}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})

    steps, sources, content, usage = [], [], "", None
    step_id = 0
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
            delta = obj["choices"][0]["delta"]
            for s in delta.get("reasoning_steps", []):
                t = s.get("type")
                if t == "thinking":
                    # decision-node intel lives here; previously DROPPED.
                    # keep as a step so downstream node-extraction sees it.
                    thought = str(s.get("thought", "")).strip()
                    if not thought:
                        continue
                    step_id += 1
                    steps.append({"step_id": step_id, "action": "thinking",
                                  "thought": thought, "observation": ""})
                elif t == "web_search":
                    ws = s.get("web_search") or {}
                    step_id += 1
                    steps.append({"step_id": step_id, "action": "web_search",
                                  "thought": "", "observation": "",
                                  "search_keywords": ws.get("search_keywords", [])})
                    for r in ws.get("search_results", []):
                        sources.append({"url": r.get("url"), "title": r.get("title")})
                elif t == "fetch_url_content":
                    fu = s.get("fetch_url_content") or {}
                    step_id += 1
                    steps.append({"step_id": step_id, "action": "fetch_url_content",
                                  "thought": "", "observation": str(fu.get("snippet", ""))[:240],
                                  "url": fu.get("url")})
                    if fu.get("url"):
                        sources.append({"url": fu.get("url"), "title": "(fetched)"})
            if delta.get("content"):
                content += delta["content"]
            if "usage" in obj:
                usage = obj["usage"]
    # dedup sources
    seen, uniq = set(), []
    for s in sources:
        if s["url"] and s["url"] not in seen:
            seen.add(s["url"]); uniq.append(s)
    return {"content": content, "steps": steps, "sources": uniq, "usage": usage}
