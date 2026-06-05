#!/usr/bin/env python3
"""
narrative_heroes.py — build the remaining HERO narrative traces for the 2022 library.

We already have narrative-sau-arg-2022 (the #1 hero). The user asked for hero-match
narratives only, so this adds the other two iconic 2022 storylines via the real
MiroMind API, reusing narrative.py's streaming machinery (same SYSTEM prompt, same
trace+source capture). Output: dataset/runs/narrative-*.json (full trace + sources).

Run:  python3 dataset/narrative_heroes.py     (slow — minutes per call; 2 workers < 5 QPS)
"""
import concurrent.futures as cf
import os
from narrative import run_one, KEY          # reuse stream_call/run_one + key loader

HEROES = [
    {"id": "narrative-mar-run-2022", "kind": "resolved-magic-moment",
     "q": "Analyze Morocco's run to the semi-finals at the 2022 FIFA World Cup — topping a "
          "group with Belgium and Croatia, then knocking out Spain (round of 16) and Portugal "
          "(quarter-final). What were the KEY NARRATIVE and tactical storylines that decided "
          "it and that the consensus/market kept underrating round after round (the repeatable "
          "edge) — defensive organization, Regragui's setup, set-pieces, the goalkeeping vs "
          "Spain, key players (Hakimi, En-Nesyri, Bounou)? Give 3-5 distinct storylines, each "
          "with a source URL, and identify the decisive magic moments (e.g. Bounou's shootout "
          "saves vs Spain; En-Nesyri's header vs Portugal)."},
    {"id": "narrative-arg-fra-final-2022", "kind": "resolved-magic-moment",
     "q": "Analyze the 2022 FIFA World Cup final, Argentina vs France (3-3, Argentina won 4-2 "
          "on penalties). What were the KEY NARRATIVE and tactical storylines — Argentina's "
          "first-half control, Messi's tournament-crowning performance, France's blank first "
          "hour then Mbappe's ~97-second two-goal swing, the extra-time blows, the shootout? "
          "Give 3-5 distinct storylines, each with a source URL, and identify the decisive "
          "magic moments (Mbappe's brace to force extra time; Messi's extra-time goal; "
          "Montiel's winning penalty)."},
]


def main():
    if not KEY:
        print("NO API KEY. Aborting.", flush=True)
        raise SystemExit(2)
    model = os.environ.get("MIRO_MODEL", "mirothinker-1-7-deepresearch-mini")
    timeout = int(os.environ.get("MIRO_TIMEOUT", "480"))
    print(f"HERO NARRATIVES | {len(HEROES)} calls | model={model} timeout={timeout}s", flush=True)
    with cf.ThreadPoolExecutor(max_workers=2) as ex:
        list(ex.map(lambda it: run_one(it, model, timeout), HEROES))
    print("DONE -> dataset/runs/narrative-mar-run-2022.json, narrative-arg-fra-final-2022.json", flush=True)


if __name__ == "__main__":
    main()
