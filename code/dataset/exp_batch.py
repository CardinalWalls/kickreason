#!/usr/bin/env python3
"""
exp_batch.py — EMPIRICAL TEST: can ONE MiroMind call update MANY nodes (batch),
or is it strictly one-question-per-call?

Two REAL calls, apples-to-apples:
  (A) BATCH  — one prompt listing 4 distinct forecast sub-questions, asking for a
               COMPACT per-question answer (prob + 1 reason + 1 source URL, one line each).
  (B) SINGLE — exactly ONE of those 4 sub-questions alone (the per-node baseline).

We measure for each: elapsed wall time, total/prompt/completion/reasoning tokens,
answer length, #searches/#fetches, and — for the batch — whether ALL 4 questions
came back. Then we PRINT a verdict table and compute batch-cost vs 4x-single cost.

The point: which call shape is the right manipulation mechanism for updating nodes
in the forecast graph — one batch call, or N per-node calls?

stdlib only. Key from ../.miroapi. model = mini. timeout 300. retry-once on EMPTY.
Calls are SLOW (minutes each); that is expected.

Run:  python3 exp_batch.py
Raw:  ./runs/exp-batch.json
"""
import json
import os
import re
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(HERE, "..", ".miroapi")
RUNS_DIR = os.path.join(HERE, "runs")
OUT_PATH = os.path.join(RUNS_DIR, "exp-batch.json")

API_URL = "https://api.miromind.ai/v1/chat/completions"
MODEL = "mirothinker-1-7-deepresearch-mini"
TIMEOUT = 300

# The 4 distinct forecast sub-questions (the kind of nodes the graph holds).
SUBQS = [
    ("usa_opener",   "Do the USA men win their opening match at the 2026 FIFA World Cup?"),
    ("mexico_group", "Does Mexico finish top of their group at the 2026 FIFA World Cup?"),
    ("spain_final",  "Does Spain reach the 2026 FIFA World Cup final?"),
    ("mbappe_score", "Does Kylian Mbappe score in France's first match at the 2026 FIFA World Cup?"),
]

# Compact, identical output contract for BOTH call shapes so lengths are comparable.
SYS_BATCH = (
    "You are a FAST football forecaster for a high-volume intel service. "
    "You will be given several numbered sub-questions. Answer EVERY one. "
    "For EACH question output EXACTLY one line in this format:\n"
    "Qn: <probability %> | <one-sentence reason> | <one source URL>\n"
    "Nothing else. No preamble, no essay, no shared section. One line per question, in order."
)
SYS_SINGLE = (
    "You are a FAST football forecaster for a high-volume intel service. "
    "Answer the single question in EXACTLY one line in this format:\n"
    "<probability %> | <one-sentence reason> | <one source URL>\n"
    "Nothing else. No preamble, no essay."
)


def _load_key():
    if os.path.exists(KEY_PATH):
        with open(KEY_PATH) as f:
            return f.readline().strip()
    return os.environ.get("MIROMIND_API_KEY", "")


def _stream_call(system, user, key):
    """One streaming call. Returns dict with content/usage/counts/timing."""
    body = json.dumps({
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }).encode()
    req = urllib.request.Request(API_URL, data=body, headers={
        "Authorization": f"Bearer {key}", "Content-Type": "application/json"})

    content, usage = "", None
    nsearch = nfetch = 0
    sources = []
    t0 = time.time()
    ttfb = None
    timed_out = False
    err = None
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as resp:
            for raw in resp:
                if ttfb is None:
                    ttfb = round(time.time() - t0, 1)
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
                if "usage" in obj:
                    usage = obj["usage"]
    except Exception as e:  # noqa: BLE001 — timeout/socket/http all collapse to a recorded error
        err = f"{type(e).__name__}: {e}"
        timed_out = "timed out" in str(e).lower() or "timeout" in type(e).__name__.lower()
    elapsed = round(time.time() - t0, 1)
    nsources = len(set(sources))
    return {
        "content": content,
        "usage": usage,
        "nsearch": nsearch,
        "nfetch": nfetch,
        "nsources": nsources,
        "answer_chars": len(content),
        "elapsed_s": elapsed,
        "ttfb_s": ttfb,
        "timed_out": timed_out,
        "error": err,
    }


def call_retry_once(system, user, key, label):
    """Make the call; if content is EMPTY (the ~1-in-6 dud), retry exactly once."""
    print(f"[{label}] calling MiroMind (slow, up to {TIMEOUT}s)...", flush=True)
    r = _stream_call(system, user, key)
    attempts = 1
    if not r["content"].strip():
        print(f"[{label}] EMPTY content (chars=0) -> retry once...", flush=True)
        r2 = _stream_call(system, user, key)
        attempts = 2
        # keep whichever actually produced content; else keep first
        if r2["content"].strip():
            r = r2
        else:
            r = r2  # both empty: report the second (most recent) attempt
    r["attempts"] = attempts
    print(f"[{label}] done: chars={r['answer_chars']} elapsed={r['elapsed_s']}s "
          f"searches={r['nsearch']} fetches={r['nfetch']} attempts={attempts}", flush=True)
    return r


def detect_questions_covered(batch_content):
    """How many of the 4 sub-questions are answered in the batch output.

    Robust to format drift: a question counts as 'covered' if we can find its
    Q-line (Q1:/Q2:...) OR a topical keyword cluster near a probability token.
    """
    text = batch_content or ""
    low = text.lower()
    # 1) explicit Qn lines (the requested contract)
    qline_hits = set(int(m.group(1)) for m in re.finditer(r"\bq\s*([1-4])\s*[:.\)]", low))
    # 2) topical fallback per question (keyword + a % somewhere in the same line)
    topic_keys = {
        1: ["usa", "united states", "opener", "opening"],
        2: ["mexico", "top of", "win their group", "finish top", "group winner"],
        3: ["spain", "final"],
        4: ["mbapp", "mbappe", "france"],
    }
    pct_line = re.compile(r".*\d{1,3}\s*%.*")
    topic_hits = set()
    for ln in text.splitlines():
        if not pct_line.match(ln):
            continue
        lnl = ln.lower()
        for qn, keys in topic_keys.items():
            if any(k in lnl for k in keys):
                topic_hits.add(qn)
    covered = sorted(qline_hits | topic_hits)
    return {
        "n_covered": len(covered),
        "covered_qnums": covered,
        "all_four": len(covered) == 4,
        "qline_hits": sorted(qline_hits),
        "topic_hits": sorted(topic_hits),
    }


def usage_num(usage, k, default=0):
    if not usage:
        return default
    return usage.get(k, default) or default


def main():
    key = _load_key()
    if not key:
        raise SystemExit("No API key at " + KEY_PATH)
    os.makedirs(RUNS_DIR, exist_ok=True)

    t_start = time.time()

    # (A) BATCH: all 4 sub-questions in one prompt.
    batch_user = "Sub-questions:\n" + "\n".join(
        f"Q{i+1}: {q}" for i, (_, q) in enumerate(SUBQS)
    )
    A = call_retry_once(SYS_BATCH, batch_user, key, "BATCH")

    # (B) SINGLE: one sub-question alone (use Q1 — the USA opener — as the per-node baseline).
    single_id, single_q = SUBQS[0]
    B = call_retry_once(SYS_SINGLE, single_q, key, "SINGLE")

    coverage = detect_questions_covered(A["content"])

    # ---- cost math ----
    A_tot = usage_num(A["usage"], "total_tokens")
    B_tot = usage_num(B["usage"], "total_tokens")
    four_single_tot = B_tot * 4  # extrapolated cost of doing 4 per-node calls
    tok_ratio = (A_tot / four_single_tot) if four_single_tot else None

    A_time = A["elapsed_s"]
    B_time = B["elapsed_s"]
    four_single_time = B_time * 4  # 4 sequential per-node calls
    time_ratio = (A_time / four_single_time) if four_single_time else None

    out = {
        "experiment": "batch_vs_single_node_update",
        "model": MODEL,
        "timeout_s": TIMEOUT,
        "subquestions": [{"id": i, "q": q} for i, q in SUBQS],
        "batch": {
            "sys": SYS_BATCH,
            "user": batch_user,
            **A,
            "coverage": coverage,
        },
        "single": {
            "sys": SYS_SINGLE,
            "id": single_id,
            "q": single_q,
            **B,
        },
        "compare": {
            "batch_total_tokens": A_tot,
            "single_total_tokens": B_tot,
            "four_single_total_tokens": four_single_tot,
            "batch_vs_4x_token_ratio": round(tok_ratio, 3) if tok_ratio else None,
            "batch_elapsed_s": A_time,
            "single_elapsed_s": B_time,
            "four_single_elapsed_s": round(four_single_time, 1),
            "batch_vs_4x_time_ratio": round(time_ratio, 3) if time_ratio else None,
            "batch_completion_tokens": usage_num(A["usage"], "completion_tokens"),
            "single_completion_tokens": usage_num(B["usage"], "completion_tokens"),
            "batch_searches": A["nsearch"],
            "single_searches": B["nsearch"],
        },
        "wall_clock_s": round(time.time() - t_start, 1),
    }

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2)

    _print_verdict(out)
    return out


def _cell(v, w):
    return str(v).ljust(w)


def _print_verdict(out):
    c = out["compare"]
    A = out["batch"]
    B = out["single"]
    cov = A["coverage"]

    print("\n" + "=" * 72)
    print("VERDICT TABLE — batch (4 sub-Qs in one call) vs single (1 sub-Q)")
    print("=" * 72)
    cols = ["metric", "BATCH (4 Qs)", "SINGLE (1 Q)", "4x SINGLE (extrap)"]
    w = [26, 16, 16, 18]
    print("".join(_cell(cols[i], w[i]) for i in range(4)))
    print("-" * 72)

    def row(name, a, b, four=""):
        print(_cell(name, w[0]) + _cell(a, w[1]) + _cell(b, w[2]) + _cell(four, w[3]))

    row("elapsed (s)", A["elapsed_s"], B["elapsed_s"], c["four_single_elapsed_s"])
    row("total tokens", c["batch_total_tokens"], c["single_total_tokens"],
        c["four_single_total_tokens"])
    row("completion tokens", c["batch_completion_tokens"], c["single_completion_tokens"], "")
    row("web searches", A["nsearch"], B["nsearch"], "")
    row("answer chars", A["answer_chars"], B["answer_chars"], "")
    row("attempts (retry?)", A["attempts"], B["attempts"], "")
    row("empty/dud?", "yes" if not A["content"].strip() else "no",
        "yes" if not B["content"].strip() else "no", "")
    print("-" * 72)
    print(f"BATCH coverage: {cov['n_covered']}/4 sub-questions answered  "
          f"(all_four={cov['all_four']}; qnums={cov['covered_qnums']})")
    print(f"  explicit Qn-lines found: {cov['qline_hits']}   topical+% hits: {cov['topic_hits']}")
    print("-" * 72)
    print(f"COST  batch_total / (4 x single_total) = {c['batch_vs_4x_token_ratio']}  "
          "(<1 means batch is cheaper than 4 per-node calls)")
    print(f"TIME  batch_elapsed / (4 x single_elapsed) = {c['batch_vs_4x_time_ratio']}  "
          "(<1 means batch is faster than 4 sequential calls)")
    print("-" * 72)

    # ---- crisp verdict ----
    works = cov["all_four"] and bool(A["content"].strip())
    partial = cov["n_covered"] >= 2 and not works
    cheaper = (c["batch_vs_4x_token_ratio"] is not None and c["batch_vs_4x_token_ratio"] < 1)
    faster = (c["batch_vs_4x_time_ratio"] is not None and c["batch_vs_4x_time_ratio"] < 1)
    # quality preserved heuristic: each batch sub-answer should have meaningful length
    per_q_chars = (A["answer_chars"] / max(cov["n_covered"], 1)) if cov["n_covered"] else 0
    quality_ok = per_q_chars >= 60 and B["answer_chars"] > 0

    print("VERDICT:")
    if works:
        print(f"  * BATCH WORKS: one call returned all 4 sub-questions.")
    elif partial:
        print(f"  * BATCH PARTIAL: only {cov['n_covered']}/4 came back -> NOT reliable for node updates.")
    else:
        print(f"  * BATCH FAILED: {cov['n_covered']}/4 (empty={not A['content'].strip()}).")
    print(f"  * Per-node quality: ~{int(per_q_chars)} chars/sub-answer in batch vs "
          f"{B['answer_chars']} chars for the dedicated single call "
          f"-> {'preserved' if quality_ok else 'DEGRADED (batch answers thinner)'}.")
    print(f"  * Cost: batch is {'CHEAPER' if cheaper else 'NOT cheaper'} than 4 single calls "
          f"(token ratio {c['batch_vs_4x_token_ratio']}).")
    print(f"  * Time: batch is {'FASTER' if faster else 'NOT faster'} than 4 sequential calls "
          f"(time ratio {c['batch_vs_4x_time_ratio']}).")
    print("  * MECHANISM: " + (
        "BATCH is the right node-update mechanism (1 call updates many nodes, "
        "cheaper+faster, quality holds)."
        if (works and (cheaper or faster) and quality_ok)
        else "PER-NODE (one-question-per-call) is the safer mechanism; "
             "batch is unreliable/degraded here."))
    print("=" * 72)
    print(f"\nRaw saved -> {OUT_PATH}")


if __name__ == "__main__":
    main()
