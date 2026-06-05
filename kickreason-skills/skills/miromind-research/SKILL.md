---
name: miromind-research
description: >-
  Run a MiroMind deep-research API call and capture the FULL reasoning trace + sources. Use
  whenever a task needs a sourced, multi-step researched answer with an auditable trace —
  forecasts, "find out X and cite it", live news on a fixture, narrative grain — especially
  forecasting questions. Handles the hard 5-requests/sec limit, slow (minutes) calls, the
  ~1-in-6 empty return (retry once), and the fact that the model returns PROSE, not JSON.
---

# miromind-research — the deep-research engine

Calls `api.miromind.ai/v1/chat/completions` (OpenAI-style, streaming) and captures the typed trace
(thinking · web_search · fetch_url_content) plus the final answer and every source. This is the base
capability the rest of the pipeline builds on.

## Procedure
1. Load the key from `.miroapi` (first line) or `MIROMIND_API_KEY`.
2. POST the question; stream the SSE `reasoning_steps`. Capture: thinking spans (the trace is ~99.8%
   thinking — the intel lives there), searches + their results, fetched URLs + snippets, final `content`,
   `usage`.
3. **Throttle to ≤5 requests/sec** (token bucket). Retry once on HTTP 429 or an empty return (~1 in 6).
4. Return `{content, steps, sources, usage, elapsed_s}` — **prose**. Do not demand JSON from the model;
   structure it downstream with `forecast-compiler`.

## Run
```bash
python3 scripts/narrative.py        # example: capture narrative-grain traces for fixtures
# or import miro_client.stream_call(prompt, model, timeout) in your own script
```

## Output
A captured trace: the written judgement + the full step-by-step reasoning + a de-duplicated source list.
Slow (~240s median; range 73–734s) — produce ahead of kickoff, not live in-running.

## References
`references/api-reality.md` — verified behavior (slow, 5 QPS, prose-not-JSON; conditions on node status
passed in; one call ≈ de-vigged market = consensus, not edge).
