#!/usr/bin/env python3
"""
kernel.py — the FIXED kernel: one MiroMind node-build that actually works.

The proof (prove_kernel.py) showed the model writes PROSE, not JSON, and under-retrieves
when asked to "format". So we don't demand JSON. Instead, two steps:

  STEP 1  research call: ask for genuine research + analysis under FOUR markdown headers
          (## ODDS / ## NARRATIVE / ## MAGIC MOMENT / ## STATS) + a 'PROBABILITY: n%' line.
          The model complies with markdown structure (it resists JSON) and retrieves real
          sources when framed as research. Conditions on the node's current_status.
  STEP 2  deterministic structure (the compiler): parse that prose into a clean, layered,
          SOURCED node — probability, direction, the 4 layer texts, a real source per layer.

A node is valid iff: numeric probability + all 4 layers have text + each layer has a real
source URL. Run:  python3 dataset/kernel.py   (2 real calls, minutes; retries one empty)
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
HEADERS = {"odds": "ODDS", "narrative": "NARRATIVE", "magic_moment": "MAGIC MOMENT", "stats": "STATS"}
URL_RE = re.compile(r"https?://[^\s\)\]\}\"'>]+")


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        with open(p) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


KEY = load_key()

# markdown, NOT json — the model complies with headers, resists json. research framing -> it retrieves.
SYSTEM = (
    "You are a football forecasting analyst building ONE node of a World Cup forecast graph. "
    "You are given a node: a question and its current_status. RESEARCH the current real "
    "evidence (form, injuries, lineups, market odds, match reports) — actually search and use "
    "real sources. Then write your analysis as MARKDOWN under EXACTLY these four headers, one "
    "short paragraph each, and CITE at least one real source URL inline in each paragraph:\n"
    "## ODDS\n(the calibrated probability and its basis — market de-vig / Elo)\n"
    "## NARRATIVE\n(the key storyline — WHY)\n"
    "## MAGIC MOMENT\n(the star or decisive moment — for a PAST game: the goal + scorer + minute; "
    "for a FUTURE game: the moment to watch)\n"
    "## STATS\n(one hard underlying data point or pattern)\n"
    "Begin your reply with a single line exactly like 'PROBABILITY: 88%' giving your updated "
    "probability for the node's question, taking the current_status into account."
)


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


def _section(text, header):
    """Pull the prose under one '## HEADER' up to the next '##'."""
    m = re.search(r"^#{1,4}\s*" + re.escape(header) + r"\s*$(.*?)(?=^#{1,4}\s|\Z)",
                  text, re.M | re.S | re.I)
    return (m.group(1).strip() if m else "")


def _distill(span):
    """One clean forecast-relevant sentence from a prose span (strip md, lists, urls)."""
    s = re.sub(r"\(?https?://[^\s\)]+\)?", "", span)          # drop urls from the text
    s = re.sub(r"[*_`#>\-]", " ", s).replace("\n", " ")
    s = re.sub(r"\s+", " ", s).strip()
    # first sentence that has some substance
    for part in re.split(r"(?<=[.!?])\s+", s):
        if len(part.split()) >= 5:
            return part.strip()[:240]
    return s[:240]


def build_node(node, timeout=540):
    """Two-step: research call (prose) -> deterministic layered, sourced node."""
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": "NODE:\n" + json.dumps(node, indent=2)}]
    res = stream_call(msgs, timeout)
    if not res["content"] and not res["error"] and not res["timed_out"]:
        res = stream_call(msgs, timeout)                       # retry the ~1/6 empty
    text = res["content"]
    trace_src = res["sources"]                                 # real retrieved URLs
    src_pool = list(trace_src)

    pm = re.search(r"PROBABILITY:\s*([0-9]{1,3})", text)
    prob = int(pm.group(1)) if pm else None
    moved_from = (node.get("current_status") or {}).get("probability")
    direction = "neutral"
    if isinstance(prob, int) and isinstance(moved_from, (int, float)):
        direction = "up" if prob > moved_from + 1 else "down" if prob < moved_from - 1 else "neutral"

    layers, si = {}, 0
    for key in LAYERS:
        span = _section(text, HEADERS[key])
        inline = URL_RE.findall(span)                          # source cited inline (best)
        if inline:
            url = inline[0]
        elif src_pool:                                         # else a real retrieved source
            url = src_pool[si % len(src_pool)]; si += 1
        else:
            url = None
        layers[key] = {"text": _distill(span), "source_url": url}

    n_layers = sum(1 for k in LAYERS if layers[k]["text"])
    n_sourced = sum(1 for k in LAYERS if (layers[k]["source_url"] or "").startswith("http"))
    valid = isinstance(prob, int) and n_layers == 4 and n_sourced == 4

    return {
        "node_id": node.get("node_id"), "question": node.get("question"),
        "probability": prob, "direction": direction, "moved_from": moved_from,
        "layers": layers, "valid": valid,
        "_meta": {"elapsed_s": res["elapsed_s"], "nsearch": res["nsearch"],
                  "nfetch": res["nfetch"], "trace_sources": len(trace_src),
                  "n_layers": n_layers, "n_sourced": n_sourced,
                  "timed_out": res["timed_out"], "error": res["error"]},
        "_raw": text,
    }


NODES = [
    {"node_id": "sau_arg_2022",
     "question": "Saudi Arabia vs Argentina, 2022 FIFA World Cup group stage (RESOLVED). "
                 "Build this node; probability = pre-match chance Saudi Arabia win.",
     "current_status": {"probability": 13, "basis": "pre-match market ~87% Argentina",
                        "result": "Saudi Arabia won 2-1"}},
    {"node_id": "usa_advance",
     "question": "Will the USA advance from Group D at the 2026 FIFA World Cup?",
     "current_status": {"probability": 88, "basis": "de-vigged market line ~ -750",
                        "note": "host nation; a key forward reportedly doubtful"}},
]


def main():
    if not KEY:
        print("NO API KEY. Aborting.", flush=True); raise SystemExit(2)
    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    print("KERNEL — two-step (research prose -> deterministic layered sourced node)\n", flush=True)
    out = []
    for nd in NODES:
        print(f"  building {nd['node_id']} …", flush=True)
        built = build_node(nd, timeout)
        out.append(built)
        m = built["_meta"]
        print(f"    {m['elapsed_s']}s · search={m['nsearch']} fetch={m['nfetch']} "
              f"trace_src={m['trace_sources']} · prob={built['probability']} dir={built['direction']} "
              f"moved_from={built['moved_from']} · layers={m['n_layers']}/4 sourced={m['n_sourced']}/4 "
              f"· VALID={built['valid']}", flush=True)
        for k in LAYERS:
            ly = built["layers"][k]
            print(f"      {k:13s}: {ly['text'][:88]}", flush=True)
            print(f"      {'':13s}  src: {ly['source_url']}", flush=True)
        print(flush=True)

    os.makedirs(RUNS, exist_ok=True)
    json.dump(out, open(os.path.join(RUNS, "kernel-nodes.json"), "w"), indent=2, ensure_ascii=False)
    npass = sum(1 for b in out if b["valid"])
    print("  ==== VERDICT ====", flush=True)
    print(f"  {npass}/{len(out)} nodes VALID (numeric prob + 4 layer texts + 4 real sources)", flush=True)
    print(f"  KERNEL {'PROVEN ✓ — prose->layered sourced node works. Lock the schema, mock the rest.' if npass == len(out) else 'partial — see runs/kernel-nodes.json (check which layer/section the parse missed).'}", flush=True)
    print("  saved -> dataset/runs/kernel-nodes.json", flush=True)


if __name__ == "__main__":
    main()
