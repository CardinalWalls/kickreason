#!/usr/bin/env python3
"""
graph_build.py — USE the MiroMind API to SOLVE the real problem: build a slice of the
FIFA-2026 forecast GRAPH. Not 40k independent calls (the probe proved that's impossible:
one open question = 1.78M tokens / 323s). Instead a DAG rooted at "who wins the World Cup",
where each node is populated by ONE deep-research call that returns a probability + the
decision-node INTEL (the signals that move it) + sources. The trace at each node = business
value; the maintained, graded graph = flywheel data.

Each call uses a reliable (non-terse) forecaster system prompt — the probe showed terse
prompts can return EMPTY — and asks the model to END with a small ```json fence we parse:
  {"prob": <number 0-100 or {"label":pct,...}>, "intel": ["signal — http(s)://source", ...],
   "depends_on": ["child sub-question", ...]}

Build the slice:
  python3 dataset/graph_build.py
Update one node on breaking news (propagates 'stale' to ancestors):
  python3 dataset/graph_build.py --update france_final --news "Mbappe ruled out with injury"
Env: MIRO_TIMEOUT (s/call, 540), MIRO_WORKERS (3)
"""
import concurrent.futures as cf
import json
import os
import re
import socket
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "graph")
API_URL = "https://api.miromind.ai/v1/chat/completions"
MODEL = os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini")


def load_key():
    p = os.path.join(HERE, "..", ".miroapi")
    if os.path.exists(p):
        with open(p) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


KEY = load_key()

SYSTEM = (
    "You are a calibrated football forecaster building one node of a World Cup forecast "
    "graph. Research current evidence (form, injuries, lineups, rest, draw/path, market "
    "odds), reason in steps, and give a calibrated probability anchored to (and de-vigged "
    "from) the betting market. Be concrete and cite sources. "
    "IMPORTANT: after your analysis, end your message with a fenced json block exactly like:\n"
    "```json\n"
    '{"prob": <single number 0-100, OR an object of outcome:percent>, '
    '"intel": ["one-line decision-node signal — https://source", "...3 to 6 of these"], '
    '"depends_on": ["child sub-question this forecast depends on", "...2 to 5"]}\n'
    "```\n"
    "The 'intel' bullets are the product: each must be a specific signal that MOVES the "
    "forecast, with its source URL. 'depends_on' are the graph children."
)

# The graph skeleton: id -> (parent_id|None, type, question). MiroMind fills each node.
NODES = [
    ("champion", None, "root",
     "Who will win the 2026 FIFA World Cup? Give title probabilities for the top 6-8 "
     "contenders and the single key factor for each."),
    ("france_final", "champion", "team-path",
     "What is the probability that France reaches the final of the 2026 FIFA World Cup, "
     "and what is their path/key factors?"),
    ("france_match", "france_final", "match",
     "Forecast France's toughest 2026 FIFA World Cup group-stage match (win/draw/loss). "
     "Identify the opponent first."),
    ("spain_final", "champion", "team-path",
     "What is the probability that Spain reaches the final of the 2026 FIFA World Cup, "
     "and what is their path/key factors?"),
    ("spain_match", "spain_final", "match",
     "Forecast Spain's toughest 2026 FIFA World Cup group-stage match (win/draw/loss). "
     "Identify the opponent first."),
    ("star_fitness", "champion", "intel-leaf",
     "Latest fitness / injury / availability news for the key attackers of France and "
     "Spain ahead of the 2026 FIFA World Cup."),
]


def stream_call(messages, timeout):
    body = json.dumps({"model": MODEL, "messages": messages}).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    sources, content, usage = [], "", None
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
                try:
                    delta = obj["choices"][0]["delta"]
                except (KeyError, IndexError):
                    delta = {}
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


def parse_fence(content):
    """Pull the trailing ```json fence. Robust fallbacks if absent."""
    blocks = re.findall(r"```json\s*(.*?)```", content, re.DOTALL)
    if not blocks:
        blocks = re.findall(r"```\s*(\{.*?\})\s*```", content, re.DOTALL)
    for b in reversed(blocks):
        try:
            d = json.loads(b.strip())
            return {"prob": d.get("prob"), "intel": d.get("intel") or [],
                    "depends_on": d.get("depends_on") or []}
        except json.JSONDecodeError:
            continue
    return {"prob": None, "intel": [], "depends_on": [], "_parse": "failed"}


def expand(node, timeout, extra_user=None):
    nid, parent, ntype, q = node
    msgs = [{"role": "system", "content": SYSTEM},
            {"role": "user", "content": q}]
    if extra_user:
        msgs.append({"role": "user", "content": extra_user})
    res = stream_call(msgs, timeout)
    if not res["content"] and not res["error"] and not res["timed_out"]:
        # probe showed occasional empty returns — retry once
        res = stream_call(msgs, timeout)
    parsed = parse_fence(res["content"])
    rec = {"id": nid, "parent": parent, "type": ntype, "question": q,
           "prob": parsed["prob"], "intel": parsed["intel"],
           "depends_on": parsed["depends_on"], "sources": res["sources"],
           "n_sources": len(res["sources"]), "nsearch": res["nsearch"],
           "nfetch": res["nfetch"], "elapsed_s": res["elapsed_s"],
           "usage": res["usage"], "stale": False, "raw": res["content"]}
    u = res["usage"] or {}
    print(f"[node] {nid:14s} {res['elapsed_s']:>6}s  search={res['nsearch']:<2} "
          f"prob={str(parsed['prob'])[:34]:34s} intel={len(parsed['intel'])} "
          f"src={len(res['sources'])} tok={u.get('total_tokens','?')}", flush=True)
    return rec


def render_md(graph):
    by_id = {n["id"]: n for n in graph["nodes"]}
    children = {}
    for n in graph["nodes"]:
        children.setdefault(n["parent"], []).append(n["id"])

    lines = ["# FIFA 2026 forecast graph (slice) — built live by MiroMind",
             "",
             f"_Nodes: {len(graph['nodes'])} · root: who wins the World Cup · each node = one "
             "deep-research call → probability + decision-node intel + sources._", ""]

    def walk(nid, depth):
        n = by_id[nid]
        pad = "  " * depth
        flag = " ⚠️STALE" if n["stale"] else ""
        lines.append(f"{pad}- **{n['id']}** ({n['type']}) — `prob={n['prob']}`"
                     f"  · {n['n_sources']} sources{flag}")
        for it in n["intel"][:6]:
            lines.append(f"{pad}  - intel: {it}")
        for c in children.get(nid, []):
            walk(c, depth + 1)

    for root in children.get(None, []):
        walk(root, 0)
    lines += ["", "---",
              "**Business value** = the intel bullets at each node (live, sourced).  ",
              "**Flywheel** = this whole audited, graded graph is the human-stakes "
              "trajectory data MiroVerse lacks.  ",
              "**Scale** = one node-call feeds many child markets; news re-runs only "
              "affected nodes, never all 30k-50k."]
    return "\n".join(lines)


def save(graph):
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "graph.json"), "w") as f:
        json.dump(graph, f, indent=2, ensure_ascii=False)
    with open(os.path.join(OUT, "graph.md"), "w") as f:
        f.write(render_md(graph))
    print(f"\nsaved -> {os.path.join(OUT, 'graph.json')} + graph.md", flush=True)


def ancestors(nodes_by_id, nid):
    out, cur = [], nodes_by_id[nid]["parent"]
    while cur:
        out.append(cur)
        cur = nodes_by_id[cur]["parent"]
    return out


def cmd_update(node_id, news, timeout):
    path = os.path.join(OUT, "graph.json")
    if not os.path.exists(path):
        print("no graph yet — run build first", flush=True)
        raise SystemExit(2)
    graph = json.load(open(path))
    by_id = {n["id"]: n for n in graph["nodes"]}
    if node_id not in by_id:
        print(f"unknown node {node_id}", flush=True)
        raise SystemExit(2)
    n = by_id[node_id]
    print(f"[update] {node_id} on news: {news!r}", flush=True)
    skeleton = (n["id"], n["parent"], n["type"], n["question"])
    fresh = expand(skeleton, timeout,
                   extra_user=f"BREAKING UPDATE since your last forecast: {news}. "
                              "Re-forecast this node, state how the probability moved and "
                              "why, and whether the market has adjusted yet.")
    old = n["prob"]
    n.update(fresh)
    n["stale"] = False
    affected = ancestors(by_id, node_id)
    for a in affected:
        by_id[a]["stale"] = True  # parents now need re-aggregation
    print(f"[update] {node_id} prob {old} -> {n['prob']}; marked stale (need re-run): "
          f"{affected}", flush=True)
    save(graph)


def main():
    if not KEY:
        print("NO API KEY. Aborting.", flush=True)
        raise SystemExit(2)
    timeout = int(os.environ.get("MIRO_TIMEOUT", "540"))
    workers = int(os.environ.get("MIRO_WORKERS", "3"))

    if "--update" in sys.argv:
        i = sys.argv.index("--update")
        node_id = sys.argv[i + 1]
        news = sys.argv[sys.argv.index("--news") + 1] if "--news" in sys.argv else "(unspecified)"
        cmd_update(node_id, news, timeout)
        return

    print(f"GRAPH BUILD | {len(NODES)} nodes | model={MODEL} timeout={timeout}s "
          f"workers={workers}\n", flush=True)
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        nodes = list(ex.map(lambda n: expand(n, timeout), NODES))
    graph = {"built_s": round(time.time() - t0, 1), "model": MODEL, "nodes": nodes}
    tot = sum((n["usage"] or {}).get("total_tokens", 0) or 0 for n in nodes)
    print(f"\nbuilt {len(nodes)} nodes in {graph['built_s']}s · total tokens {tot:,}", flush=True)
    save(graph)
    print("\nNext: python3 dataset/graph_build.py --update france_final "
          "--news \"<breaking news>\"   (shows live propagation)", flush=True)


if __name__ == "__main__":
    main()
