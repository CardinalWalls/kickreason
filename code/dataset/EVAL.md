# Trace eval — real MiroMind API runs

Scores the **trace** (use of the API), not the forecast result. `trace_score` is a transparent 0-1 composite (finished .25 / searched .20 / fetched .15 / committed-a-probability .15 / factor-coverage .15 / reputable-source-share .10).

| id | kind | done | elapsed | steps | search | fetch | sources (rep) | prob? | coverage | answer-leak | score |
|---|---|---|--:|--:|--:|--:|--:|:--:|:--:|---|--:|
| euro24-final-leakprobe | past | ✓ | 435.1s | 32470 | 57 | 28 | 287 (102) | ✓ | 2/5 | clean (8 src w/ result) | **0.85** |
| wc26-golden-boot | forward | ✓ | 259.7s | 2695 | 3 | 5 | 20 (7) | ✓ | 4/5 | — | **0.91** |
| wc26-spain-final | forward | ✓ | 73.2s | 1186 | 3 | 1 | 9 (2) | ✓ | 3/4 | — | **0.88** |
| wc26-usa-advance | forward | ✓ | 733.8s | 22054 | 14 | 32 | 100 (37) | ✓ | 5/5 | — | **0.94** |
| wc26-winner | forward | ✓ | 221.9s | 5612 | 4 | 7 | 36 (18) | ✓ | 4/5 | — | **0.92** |

**5 runs · 5 finished · mean trace_score 0.9**

## What the leak probe actually showed

- The past Euro-2024 question did **not** leak the result *in the answer* (`answer-leak: clean`) — the model gave a disciplined pre-kickoff forecast off pre-match odds. But its **source pool did** contain post-result and even wrong-event (Euro 2025 Women's final) material — `post_result_sources` counts it.
- So leakage on a past event lives in the *retrieved sources and the model's latent knowledge*, not necessarily the prose. You cannot rely on it staying out of the answer at scale -> result-accuracy is still graded FORWARD only.
- This grades process quality on data we already have; it does NOT claim the forecasts are calibrated (that needs forward grading on live fixtures).
