# bootstrap-compiler

Eats one human↔AI **conversation transcript** and compiles it into a structured,
audited, MiroVerse-aligned **interaction trajectory** — the data class MiroVerse's
static QA corpus structurally lacks (no human-in-the-loop, no time-decay, no audit).

The control case is **this conversation**. Run it on yourself:

```bash
python3 compiler/compile.py              # deterministic only (fast, zero-LLM)
python3 compiler/compile.py --miro       # + ONE MiroMind deep-research call (slow)
bash    compiler/verify.sh               # external verdict owner → contract-result.json
```

Output → `compiler/out/`: `gate_pack.json` (written first), `trajectory-bootstrap.index.json`,
`trajectory-bootstrap.md`, `contract-result.json`.

## In plain words (what / why / how to test)

- **What it does:** it reads a record of an interaction and writes **one markdown file you
  can open and read** — what was decided, what was ruled out (and why), what's still open,
  the facts (each with a source and date), and a simple map of how the ideas connect — plus
  a **checker script** that re-reads that file and confirms **every claim has a source**.
- **Why it works:** there's no magic. It's text in, a readable record out, and an automatic
  pass/fail check. Most of it is plain pattern-matching (no AI); exactly **one** step calls
  the MiroMind API. Because the rest is deterministic, you can re-run it and get the same
  file every time — so it's checkable, not a black box.
- **How to test:** run the two commands above and open `compiler/out/trajectory-bootstrap.md`.
  See if it matches what really happened. Run `verify.sh` — it prints `pass` only if every
  claim is backed by a source.

## Where this fits the FIFA demo (a later milestone)

The World Cup demo's wedge is a **track-record page** — every forecast locked before kickoff,
then marked ✓/✗ after the match, with an honest accuracy score (the page KickOracle fakes).
This compiler is the engine that keeps that record **honest and checkable**: feed it a match
forecast (the reasoning + sources + the final result) instead of a conversation, and it writes
the same kind of readable, source-checked record. Day-one the demo can seed a few rows by hand;
this is the milestone that makes the track record trustworthy once there are many forecasts.
See [`brainstorm/kickoracle/04-futurex-and-the-forecast-that-updates.md`](../brainstorm/kickoracle/04-futurex-and-the-forecast-that-updates.md).

## What it is (the deeper frame — TOWOW)

The compiler is the **升维存储 + 意图萃取** layer around short-lived agent "lives".
A conversation throws off 三种证据 (原话/判断/事件); this turns them into 两种承载
(状态/快照) that the next life can inherit — with the **human as 上升端**.

```
transcript ─▶ segment ─▶ [DET] extract ─▶ [DET] classify ─▶ [LLM×1] MiroMind ─▶ [DET] freeze ─▶ artifact
                          gbrain graph     wow-harness        enrichment        plan-lock
                          + facts          gate_pack          (optional)        vN-final
```

**Exactly one LLM call** (the MiroMind API, the Agent-内部 execution unit). Everything
else is zero-LLM and rebuildable byte-for-byte.

## The four output layers (one schema)

| layer | borrowed from | what it carries |
|---|---|---|
| **intent ledger** | intent-ledger + wow-harness | stable_intent / **rejected_directions** (the negative-space memory) / open_questions / operator_entries / gate_pack |
| **knowledge graph** | gbrain `link-extraction.ts` + `facts-fence.ts` | concept pages + typed edges (zero-LLM verb inference) + `## Facts` temporal fence + trajectory regressions/drift |
| **MiroVerse trajectory** | MiroMind ReAct + contract-loop | thought/action/observation steps + sources + verdicts |
| **did the human stay in charge?** | A2UI + HCI (jargon dropped) | a plain count per decision: did the human override the AI when it was **wrong**, and rely on it when it was **right**? |

## Files

- `extract.py` — DET. Ported from gbrain: link regexes, `inferLinkType` verb precedence
  (domain-adapted: supersedes/rejects/lacks/produces/uses/grounds/maps_to), the
  `<!--- gbrain:facts:begin -->` fence parser, timeline parser, + a domain concept lexicon.
- `wow.py` — DET. From wow-harness: Change Classification, plan-lock hedge scanner +
  `vN-final` freeze, the `gate_pack` state-pack (escalation requires `message_for_user`).
- `trust.py` — DET. Plain counts per decision: did the human change position after seeing
  the AI, agree, look at the reasoning, override the AI when it was wrong, rely when right.
  "No confirmed answer yet" is allowed — we never pretend to know the right answer.
- `miro.py` — the ONE LLM call. MiroMind SSE client (`api.miromind.ai`), parses the typed
  `reasoning_steps` trace into ReAct steps. Slow by design; optional.
- `compile.py` — orchestrator + renderer.
- `verify.sh` — external contract verifier (controller owns the verdict, not the worker).
- `input/this-conversation.transcript.md` — the bootstrap input (this conversation).

## Honest gaps (flagged, not hidden)

1. Zero-LLM edge typing is a regex heuristic (~70–94% in gbrain's own benchmark); a few
   edges are noise. The MiroMind call can re-type them, but the graph is the load-bearing
   wall on its own.
2. "How far did the human move toward the AI?" only works when positions are numbers;
   in a text conversation we fall back to the simple yes/no "did they switch / agree?".
3. To say whether an override was *justified*, you need to know the real answer. When the
   conversation has no confirmed answer yet, we say exactly that instead of scoring it.
4. The MiroMind deep-research call is slow (a multi-part query ran 9+ min, timed out at
   560s). The deterministic artifact stands without it; enrichment is additive.

## Maps to the hackathon

For FIFA, the compiler is the **track-record engine** (see the FIFA section above): it turns
each forecast — its sourced reasoning, its updates, and its after-the-match ✓/✗ — into one
readable, source-checked record. That running record of "what we predicted and whether we
were right" is the page KickOracle never publishes, and it's the thing this tool produces
as a by-product of doing the forecasts honestly.
