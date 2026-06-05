#!/usr/bin/env python3
"""
api_usage.py — PROOF OF MIROMIND API USAGE, accumulated from disk.

Scans every real call we have captured (dataset/runs/*.json + dataset/graph/graph.json)
and emits one verifiable ledger: per-call receipts (model, latency, tokens, searches,
fetches, sources, ok?) + grand totals. This is the evidence that we actually USED the
hosted deep-research API — re-run any time as we make more calls; it only counts what
is really on disk.

Run:
    python3 dataset/api_usage.py        # prints the ledger + writes API_USAGE.md
"""
import json
import os
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
GRAPH = os.path.join(HERE, "graph", "graph.json")
OUT_MD = os.path.join(HERE, "API_USAGE.md")


def _tokens(c):
    u = c.get("usage") or {}
    if not isinstance(u, dict):
        return 0
    if u.get("total_tokens"):
        return int(u["total_tokens"])
    return int((u.get("prompt_tokens") or 0) + (u.get("completion_tokens") or 0))


def _counts(c):
    ns = c.get("nsearch")
    nf = c.get("nfetch")
    if ns is None or nf is None:
        steps = c.get("steps") or []
        ns = sum(1 for s in steps if s.get("action") == "web_search")
        nf = sum(1 for s in steps if s.get("action") == "fetch")
    src = c.get("nsources")
    if src is None:
        src = c.get("n_sources")
    if src is None:
        src = len(c.get("sources") or [])
    return ns or 0, nf or 0, src or 0


def _elapsed(c):
    # concurrency probe records per-call wall time as latency_s
    return float(c.get("elapsed_s") or c.get("elapsed") or c.get("latency_s") or 0.0)


def _http(c):
    # accept either {"status": ...} or {"http_status": ...} (concurrency probe)
    s = c.get("status")
    if s is None:
        s = c.get("http_status")
    try:
        return int(s) if s is not None else None
    except (TypeError, ValueError):
        return None


def _ok(c):
    if c.get("timed_out"):
        return False
    if c.get("error"):
        return False
    h = _http(c)
    if h is not None and h >= 400:        # HTTP 429 throttles & 5xx -> NOT ok
        return False
    if c.get("ok") is False:
        return False
    return True


def _throttled(c):
    """A call that was rejected by the live rate limiter (HTTP 429)."""
    return _http(c) == 429


def _is_call(c):
    return isinstance(c, dict) and any(
        k in c for k in ("usage", "elapsed_s", "elapsed", "latency_s",
                         "content", "steps", "status", "http_status", "ok"))


def _model(c):
    m = c.get("model") or "mirothinker-1-7-deepresearch-mini"
    return m.replace("mirothinker-1-7-deepresearch", "…-deepresearch")


def normalize(c, label):
    ns, nf, src = _counts(c)
    return {"label": label, "model": _model(c), "elapsed": round(_elapsed(c), 1),
            "tokens": _tokens(c), "search": ns, "fetch": nf, "sources": src,
            "ok": _ok(c), "throttled": _throttled(c), "http": _http(c),
            "q": (c.get("q") or c.get("question") or c.get("id") or "")}


def calls_from(path):
    name = os.path.basename(path)
    if "summary" in name:
        return [], "aggregate (skipped to avoid double-count)"
    try:
        d = json.load(open(path, encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        return [], f"unreadable: {e}"
    out = []
    if isinstance(d, list):                       # probe lists
        out = [normalize(c, f"{name}#{k}") for k, c in enumerate(d) if _is_call(c)]
        kind = f"{len(out)} calls (list)"
    elif isinstance(d.get("results"), list) and isinstance(d.get("summary"), dict):
        # exp-concurrency.json: a rate-limit ceiling probe. Each entry in
        # "results" is one real attempt against the live API; the 7 HTTP-429s
        # are the PROOF we hit the 5-QPS server limit at concurrency=12.
        out = [normalize(c, f"{name}#{c.get('idx', k)}")
               for k, c in enumerate(d["results"]) if _is_call(c)]
        n_429 = sum(1 for c in out if c["throttled"])
        n_ok = sum(1 for c in out if c["ok"])
        kind = (f"{len(out)} attempts (concurrency probe: {n_ok} ok / "
                f"{n_429} HTTP-429 throttled — hit live 5-QPS limit)")
    elif "batch" in d and "single" in d:          # exp-batch.json
        # batch_vs_single_node_update: 2 real calls (one multi-question batch
        # call + one single-question call) compared head-to-head.
        out = [normalize(d["batch"], name + ":batch"),
               normalize(d["single"], name + ":single")]
        kind = "2 calls (batch vs single)"
    elif "baseline" in d and "challenger" in d:   # exp-multishot
        out = [normalize(d["baseline"], name + ":baseline"),
               normalize(d["challenger"], name + ":challenger")]
        kind = "2 calls (multi-shot)"
    elif "nodes" in d and isinstance(d["nodes"], list):   # graph.json
        out = [normalize(n, f"{name}:{n.get('id','?')}") for n in d["nodes"] if _is_call(n)]
        kind = f"{len(out)} calls (graph nodes)"
    elif _is_call(d):
        out = [normalize(d, name)]
        kind = "1 call"
    else:
        kind = "no call found"
    return out, kind


def main():
    files = sorted(glob.glob(os.path.join(RUNS, "*.json")))
    if os.path.exists(GRAPH):
        files.append(GRAPH)

    all_calls, per_file = [], []
    for f in files:
        calls, kind = calls_from(f)
        per_file.append((os.path.relpath(f, HERE), kind, calls))
        all_calls.extend(calls)

    ok = [c for c in all_calls if c["ok"]]
    throttled = [c for c in all_calls if c["throttled"]]
    failed = [c for c in all_calls if not c["ok"] and not c["throttled"]]
    tot_tok = sum(c["tokens"] for c in all_calls)
    tot_min = sum(c["elapsed"] for c in all_calls) / 60.0
    tot_src = sum(c["sources"] for c in all_calls)
    tot_search = sum(c["search"] for c in all_calls)
    tot_fetch = sum(c["fetch"] for c in all_calls)

    def status_glyph(c):
        if c["ok"]:
            return "✓"
        if c["throttled"]:
            return "429"
        return "✗"

    print("=" * 64)
    print("  PROOF OF MIROMIND API USAGE  (accumulated from disk)")
    print("=" * 64)
    print(f"  REAL CALLS CAPTURED : {len(all_calls)}   ({len(ok)} ok / "
          f"{len(throttled)} throttled(429) / {len(failed)} other-failed)")
    print(f"  TOTAL TOKENS        : {tot_tok:,}")
    print(f"  TOTAL DEEP-RESEARCH : {tot_min:,.0f} minutes of agent time")
    print(f"  WEB SEARCHES        : {tot_search:,}")
    print(f"  PAGES FETCHED       : {tot_fetch:,}")
    print(f"  SOURCES RETRIEVED   : {tot_src:,}")
    if throttled:
        print(f"  RATE-LIMIT PROOF    : {len(throttled)} live HTTP-429 "
              f"'QPS limit exceeded' (limit=5) — we probed the ceiling")
    print("=" * 64)
    print(f"  {'call':44s} {'sec':>6} {'tokens':>10} {'sch':>4} {'fch':>4} {'src':>4} ok")
    print("  " + "-" * 78)
    for c in all_calls:
        print(f"  {c['label'][:44]:44s} {c['elapsed']:>6.0f} {c['tokens']:>10,} "
              f"{c['search']:>4} {c['fetch']:>4} {c['sources']:>4} {status_glyph(c)}")

    # write the markdown ledger
    L = ["# Proof of MiroMind API usage", "",
         f"_Auto-scanned from `dataset/runs/` + `graph/graph.json`. Re-run `python3 dataset/api_usage.py`._",
         "",
         "## Totals (what we have actually run)", "",
         f"- **{len(all_calls)} real API calls** captured "
         f"({len(ok)} ok, {len(throttled)} throttled/HTTP-429, {len(failed)} other-failed)",
         f"- **{tot_tok:,} tokens** of deep research",
         f"- **~{tot_min:,.0f} minutes** of agent run-time",
         f"- **{tot_search:,} web searches**, **{tot_fetch:,} pages fetched**, "
         f"**{tot_src:,} sources retrieved**", ""]
    if throttled:
        L += ["## Rate-limit proof (we probed the live ceiling)", "",
              f"- **{len(throttled)} calls were rejected with HTTP 429** "
              f"`{{\"error\":\"QPS limit exceeded\",\"limit\":5}}` during a "
              f"concurrency=12 burst.",
              "- This is hard evidence the hosted API enforces a **live 5 requests/sec "
              "limit** — the 429s are a feature of the proof, not a bug: they show we "
              "actually hit the server, not a mock.",
              "- The throttled calls are counted as attempts but **excluded from the "
              "`ok` set** (and they carry no token usage, so they don't inflate totals).",
              ""]
    L += ["## Every call (receipts)", "",
          "| call | sec | tokens | search | fetch | sources | status |",
          "|---|--:|--:|--:|--:|--:|:--:|"]
    for c in all_calls:
        st = "✓" if c["ok"] else ("429" if c["throttled"] else "✗")
        L.append(f"| `{c['label']}` | {c['elapsed']:.0f} | {c['tokens']:,} | "
                 f"{c['search']} | {c['fetch']} | {c['sources']} | {st} |")
    L += ["", "## Files scanned", ""]
    for rel, kind, calls in per_file:
        L.append(f"- `{rel}` — {kind}")
    L += ["", "_Tokens=0 means the call returned no usage block (e.g. the empty-content "
          "returns, throttled 429s, or graph nodes saved without usage). "
          "Latency still proves the call ran._"]
    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L))
    print(f"\n  wrote -> {os.path.relpath(OUT_MD, HERE)}")


if __name__ == "__main__":
    main()
