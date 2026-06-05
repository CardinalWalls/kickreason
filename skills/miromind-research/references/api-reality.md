# MiroMind API — verified reality

Ground truth for the engine. Do not overclaim beyond this.

## What one call is
A single call to `api.miromind.ai/v1/chat/completions` (OpenAI-style, SSE) is an **autonomous deep-research
agent**: it web-searches, fetches pages, and reasons, then returns a final written judgement + the full
reasoning trace + sources + usage. Model used: `mirothinker-1-7-deepresearch-mini`.

## Behaviour (measured)
- **The trace is ~99.8% thinking** (e.g. 22,008 thinking vs 14 search vs 32 fetch in one heavy run). The
  intel ("striker ruled out, market hasn't moved") lives in the thinking span next to a fetch.
- **Slow:** ~240s median/call (range 73–734s). Prompt-tokens dominate (it re-feeds fetched pages).
- **Hard throttle: 5 requests/sec** (HTTP 429 beyond; no queue). Use a 5-QPS token bucket + 429 retry.
- **~1 in 6 returns empty** → retry once.
- **Returns PROSE, not JSON.** Asking for a JSON fence yields `prob=None`. Structure post-hoc
  (`forecast-compiler`). It DOES condition on node status passed into the prompt.
- **Post-news update latency ~6 min** → fits the pre-kickoff / late-lineup window, NOT seconds-scale in-running.

## Economics / honesty
- One call ≈ **de-vigs the market = CONSENSUS, not edge**. The only real edge is live decision-node intel in
  the post-news / pre-correction window, measured by CLV — never asserted.
- Self-grading lineage (MiroThinker): a local verifier audits each step + a global verifier audits the whole
  chain ("think → verify locally → verify globally → answer").

## Auth
Key in `.miroapi` (first line) or `MIROMIND_API_KEY`. Never commit the key.
