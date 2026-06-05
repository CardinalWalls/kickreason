#!/usr/bin/env python3
"""
prove_kernel.py — THE kernel proof: can the MiroMind API return a REASONABLE DAG NODE
with the BUSINESS VIEW baked in — by prompting the grain (the four layers) INTO the call?

A reasonable node is NOT a probability. It is one fact seen four ways — the business grain:
  odds (the calibrated number + basis) · narrative (the WHY, commentator grain) ·
  magic_moment (the star/decisive moment) · stats (a hard data point) — each SOURCED.

We prompt that grain directly into the API and demand JSON. If it returns clean, layered,
sourced nodes that respect the status we passed in, the kernel is proven and the rest can
be mocked. If not, we've found the real blocker.

Run:  python3 dataset/prove_kernel.py   (one real API call, minutes; retries one empty)
Out:  dataset/runs/prove-kernel.json + a printed VERDICT
"""
import json
import os
import re
import socket
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
API_URL = "https://api.miromind.ai/v1/chat/completions"
LAYERS = ["odds", "narrative", "magic_moment", "stats"]


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        with open(p) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


KEY = load_key()

SYSTEM = (
    "You are a NODE-UPDATER for a World Cup forecast graph. A node is ONE fact seen four "
    "ways — the BUSINESS LAYERS. You are given nodes with a question + current_status. "
    "Research current real evidence (form, injuries, lineups, market odds, match reports), "
    "then return each node with ALL FOUR layers filled, each tied to a real source.\n"
    "Output ONLY a JSON array — no prose, no markdown fences. Each element EXACTLY:\n"
    "{\n"
    '  "node_id": <echo the id>,\n'
    '  "probability": <0-100 number>,\n'
    '  "direction": "up|down|neutral",\n'
    '  "moved_from": <the current_status.probability you were given>,\n'
    '  "layers": {\n'
    '    "odds":         {"text": "<calibrated probability + its basis: market de-vig / Elo>", "source_url": "<real URL>"},\n'
    '    "narrative":    {"text": "<the key storyline / WHY, one sentence>", "source_url": "<real URL>"},\n'
    '    "magic_moment": {"text": "<for a PAST game: the decisive goal + scorer + minute; for a FUTURE game: the star / moment to watch>", "source_url": "<real URL>"},\n'
    '    "stats":        {"text": "<one hard underlying data point or pattern>", "source_url": "<real URL>"}\n'
    "  },\n"
    '  "confidence": "low|medium|high",\n'
    '  "what_would_change_it": "<one sentence>"\n'
    "}\n"
    "Start with [ and end with ]. Output nothing but the JSON array."
)

NODES = [
    {"node_id": "usa_advance",
     "question": "Will the USA advance from Group D at the 2026 FIFA World Cup?",
     "current_status": {"probability": 88, "basis": "de-vigged market line ~ -750",
                        "note": "host nation; a key forward reportedly doubtful"}},
    {"node_id": "sau_arg_2022",
     "question": "Saudi Arabia vs Argentina, 2022 FIFA World Cup group stage (a RESOLVED game) "
                 "— fill the layers of this node; probability is the pre-match chance Saudi win.",
     "current_status": {"probability": 13, "basis": "pre-match market had Argentina ~87%",
                        "result": "Saudi Arabia won 2-1"}},
]


def stream_call(messages, timeout):
    body = json.dumps({"model": os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini"),
                       "messages": messages}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    content, sources, usage = "", [], None
    nsearch = nfetch = 0
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
                delta = (obj.get("choices") or [{}])[0].get("delta", {})
                for s in delta.get("reasoning_steps", []):
                    t = s.get("type")
                    if t == "web_search":
                        nsearch += 1
                        for r in (s.get("web_search") or {}).get("search_results", []):
                            if r.get("url"):
                                sources.append(r["url"])
                    elif t == "fetch_url_content":
                        nfetch += 1
                        u = (s.get("fetch_url_content") or {}).get("url")
                        if u:
                            sources.append(u)
                if delta.get("content"):
                    content += delta["content"]
                if obj.get("usage"):
                    usage = obj["usage"]
    except Exception as e:  # noqa: BLE001
        if isinstance(e, (socket.timeout, TimeoutError)) or "timed out" in str(e).lower():
            timed_out = True
        else:
            err = f"{type(e).__name__}: {e}"
    return {"content": content, "sources": sorted(set(sources)), "usage": usage,
            "nsearch": nsearch, "nfetch": nfetch, "elapsed_s": round(time.time() - t0, 1),
            "timed_out": timed_out, "error": err}


def parse_json_array(text):
    m = re.search(r"```json\s*(.*?)```", text, re.DOTALL) or re.search(r"```\s*(.*?)```", text, re.DOTALL)
    cand = m.group(1) if m else text
    s, e = cand.find("["), cand.rfind("]")
    if s != -1 and e != -1 and e > s:
        try:
            d = json.loads(cand[s:e + 1])
            return d if isinstance(d, list) else None
        except json.JSONDecodeError:
            return None
    return None


def main():
    if not KEY:
        print("NO API KEY. Aborting.", flush=True); raise SystemExit(2)
    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    print("KERNEL PROOF — prompt the 4 business layers INTO the API; demand layered nodes back\n", flush=True)
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": "NODES:\n" + json.dumps(NODES, indent=2)}]
    res = stream_call(msgs, timeout)
    if not res["content"] and not res["error"] and not res["timed_out"]:
        print("  (empty return — retrying once)", flush=True)
        res = stream_call(msgs, timeout)

    print(f"  elapsed {res['elapsed_s']}s · searches {res['nsearch']} · fetches {res['nfetch']} "
          f"· sources {len(res['sources'])} · answer {len(res['content'])} chars "
          f"· timeout={res['timed_out']} err={res['error']}\n", flush=True)

    parsed = parse_json_array(res["content"])
    given = {n["node_id"]: n["current_status"]["probability"] for n in NODES}

    checks = {"parsed": False, "all_four_layers": False, "layers_sourced": False,
              "has_probability": False, "conditioned": False}
    rows = []
    if parsed:
        checks["parsed"] = True
        full_layer = src_layer = has_prob = cond = 0
        valid = [n for n in parsed if isinstance(n, dict)]
        for nd in valid:
            ly = nd.get("layers") or {}
            have = [k for k in LAYERS if isinstance(ly.get(k), dict) and (ly[k].get("text") or "").strip()]
            sourced = [k for k in have if str(ly[k].get("source_url") or "").startswith("http")]
            if len(have) == 4:
                full_layer += 1
            if len(sourced) == 4:
                src_layer += 1
            if isinstance(nd.get("probability"), (int, float)):
                has_prob += 1
            if nd.get("moved_from") == given.get(nd.get("node_id")):
                cond += 1
            rows.append({"node_id": nd.get("node_id"), "prob": nd.get("probability"),
                         "moved_from": nd.get("moved_from"), "layers_present": have,
                         "layers_sourced": sourced,
                         "sample": {k: (ly.get(k, {}).get("text") or "")[:80] for k in LAYERS}})
        n = len(valid) or 1
        checks["all_four_layers"] = full_layer == len(valid) and full_layer > 0
        checks["layers_sourced"] = src_layer > 0
        checks["has_probability"] = has_prob == len(valid) and has_prob > 0
        checks["conditioned"] = cond > 0

    json.dump({"id": "prove-kernel", "nodes_sent": NODES, "result": res,
               "parsed_nodes": parsed, "checks": checks, "rows": rows},
              open(os.path.join(RUNS, "prove-kernel.json"), "w"), indent=2, ensure_ascii=False)

    print("  PER-NODE (the layered DAG node, as returned):", flush=True)
    for r in rows:
        print(f"    ● {r['node_id']}  p={r['prob']} moved_from={r['moved_from']}  "
              f"layers={r['layers_present']}  sourced={len(r['layers_sourced'])}/4", flush=True)
        for k in LAYERS:
            print(f"        {k:13s}: {r['sample'].get(k,'')}", flush=True)
    pa = checks["parsed"] and checks["all_four_layers"] and checks["layers_sourced"]
    print("\n  ==== VERDICT ====", flush=True)
    for k, v in checks.items():
        print(f"    {k:18s}: {v}", flush=True)
    print(f"\n  KERNEL {'PROVEN ✓ — the API returns reasonable LAYERED DAG nodes when the grain is prompted in. Mock the rest.' if pa else 'NOT proven ✗ — see runs/prove-kernel.json; layered structured output is the blocker (try fewer nodes / full model / firmer schema).'}", flush=True)
    print("  saved -> dataset/runs/prove-kernel.json", flush=True)


if __name__ == "__main__":
    main()
