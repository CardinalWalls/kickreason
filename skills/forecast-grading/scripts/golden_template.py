#!/usr/bin/env python3
"""
golden_template.py — THE STANDARD, proven on real resolved cases.

Plain version of what this does:
  We are NOT inventing a way to score forecasts. We are adopting the recognized
  one and showing it works on games whose outcomes are already known.

  The recognized FORMAT is FutureX (arXiv:2508.11987 — the benchmark MiroMind
  topped): a *verifiable future event*, *predicted before it happens*, then
  *auto-graded after* it resolves. No opinion, no hindsight.

  The recognized SCORING is the Brier score:
        Brier = (probability_you_gave - what_actually_happened)^2
        0.00 = perfect      0.25 = a coin-flip guess      1.00 = confidently wrong
  Lower is better. It is a proper scoring rule: you can only lower your score by
  reporting your true belief, so it can't be gamed.

  Here we point that exact formula at the *market itself* on resolved games:
  take the closing price the market gave the favourite, take whether the
  favourite actually won (1) or lost (0), and compute the market's own Brier.
  The famous upsets show the formula proving — not asserting — that the market
  was confidently wrong. Saudi Arabia vs Argentina: market 0.871 on Argentina,
  Argentina LOST, so Brier = (0.871 - 0)^2 ≈ 0.759, far worse than a 0.25 coin
  flip. That is the whole point: the number, not us, calls it.

Run it:   python3 dataset/golden_template.py
It imports brier + implied_prob_american from baseline.py (the self-tested rig),
re-checks the two textbook anchors, prints the graded golden table, and writes
GOLDEN.md. Every number is computed; nothing is typed in.
"""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))

# Import the recognized, self-tested scoring rig. If baseline.py can't be
# imported for any reason, replicate the two functions exactly (same formulas)
# so this file still stands alone — but we prefer the shared, unit-tested ones.
try:
    from baseline import brier, implied_prob_american
    RIG_SOURCE = "imported from baseline.py (self-tested)"
except Exception:  # pragma: no cover - fallback only
    def implied_prob_american(odds):
        odds = float(odds)
        if odds > 0:
            return 100.0 / (odds + 100.0)
        return (-odds) / ((-odds) + 100.0)

    def brier(prob, outcome):
        return (prob - outcome) ** 2
    RIG_SOURCE = "replicated inline (baseline.py import unavailable)"

COIN_FLIP = 0.25   # Brier of a 50/50 guess on a binary event — the reference line
PERFECT = 0.0      # Brier of a forecast that was 100% right

# The single-line FutureX template every call on our page obeys.
FUTUREX_TEMPLATE = (
    "FutureX template: a verifiable future event + a probability committed "
    "BEFORE kickoff + automatic Brier grading AFTER it resolves."
)


def grade_resolved_cases():
    """For every resolved seed case that has a market price on a real favourite
    and a clear win/loss, grade the MARKET with its own Brier score.

    Returns a list of dict rows, each fully computed:
      fixture, favourite, market_prob (on favourite), favourite_won (1/0),
      result_text, brier, verdict-vs-coin-flip.
    """
    rows = json.load(open(os.path.join(ROOT, "seed-resolved.json")))
    graded = []
    for r in rows:
        pm = r.get("pre_match", {})
        prob = pm.get("market_prob_or_null")
        fav = pm.get("favourite")
        # need: a real favourite, a market price, and a binary win/loss.
        # skip coin-flips ("even") and pre-tournament futures (outright).
        if prob is None or not fav:
            continue
        if "even" in str(fav).lower() or "outright" in r["id"]:
            continue
        favourite_won = 0 if r.get("upset") else 1   # upset == favourite lost
        b = brier(prob, favourite_won)
        graded.append({
            "fixture": r["fixture"],
            "favourite": fav,
            "market_prob": prob,
            "favourite_won": favourite_won,
            "result": r.get("outcome", "").split(".")[0],
            "brier": b,
            "beats_coin_flip": b < COIN_FLIP,   # True = market scored better than 0.25
        })
    return graded


def recheck_anchors():
    """Re-prove the two textbook Brier anchors we cite, before trusting any row."""
    checks = [
        ("brier(perfect 1.0, happened) == 0.00", brier(1.0, 1) == PERFECT),
        ("brier(coin-flip 0.5, happened) == 0.25", brier(0.5, 1) == COIN_FLIP),
        ("brier(confident 0.0, happened) == 1.00", brier(0.0, 1) == 1.0),
        ("implied_prob_american(-675) ≈ 0.871", abs(implied_prob_american(-675) - 0.871) < 0.005),
    ]
    ok = all(p for _, p in checks)
    print(f"anchor re-check ({RIG_SOURCE}):", "PASS" if ok else "FAIL")
    for name, p in checks:
        print(f"  {'OK ' if p else 'XX '} {name}")
    return ok


def print_table(graded):
    print("\nTHE STANDARD — market graded by its own Brier on resolved cases")
    print("(FutureX format · Brier scoring · reference: coin-flip = 0.25, perfect = 0.00)\n")
    hdr = f"{'Fixture':32} {'Fav':10} {'Mkt%':>5} {'Result':14} {'Brier':>6}  vs 0.25"
    print(hdr)
    print("-" * len(hdr))
    for g in graded:
        res = "WON" if g["favourite_won"] else "LOST (upset)"
        verdict = "better" if g["beats_coin_flip"] else "WORSE than coin-flip"
        print(f"{g['fixture'][:32]:32} {g['favourite'][:10]:10} "
              f"{g['market_prob']*100:4.0f}% {res:14} {g['brier']:6.3f}  {verdict}")
    n = len(graded)
    mean_b = sum(g["brier"] for g in graded) / n if n else float("nan")
    worse = sum(1 for g in graded if not g["beats_coin_flip"])
    print("-" * len(hdr))
    print(f"n={n}  mean market Brier={mean_b:.3f}  "
          f"({worse}/{n} of these famous picks scored WORSE than a 0.25 coin-flip)")
    print("NOTE: this seed is an upset highlight-reel by design — it shows the "
          "FORMULA works, it is not the market's true season Brier.")
    return mean_b


def write_md(graded, mean_b):
    sa = next((g for g in graded if "Saudi" in g["fixture"]), None)
    L = []
    L.append("# THE STANDARD — the recognized way to grade a forecast, proven on real resolved cases")
    L.append("")
    L.append("> Auto-written by `python3 dataset/golden_template.py`. Every number below is")
    L.append("> **computed**, not typed: the script imports the self-tested `brier` from")
    L.append("> `baseline.py`, points it at games whose outcomes are already known, and lets")
    L.append("> the formula deliver the verdict. We did not invent a scoring method — we adopted")
    L.append("> the recognized one and showed it holds.")
    L.append("")
    L.append("## The format: FutureX")
    L.append("")
    L.append("**" + FUTUREX_TEMPLATE + "**")
    L.append("")
    L.append("FutureX (arXiv:2508.11987) is the recognized benchmark for forecasting agents —")
    L.append("the one MiroMind's agent topped. Its rule is simple and ungameable: the event must")
    L.append("be *verifiable*, the probability must be committed *before* the event, and grading")
    L.append("is *automatic* once it resolves. No hindsight, no opinion.")
    L.append("")
    L.append("## The scoring: Brier")
    L.append("")
    L.append("```")
    L.append("Brier = (probability_you_gave - what_actually_happened)^2")
    L.append("  0.00 = perfect      0.25 = coin-flip guess      1.00 = confidently wrong")
    L.append("```")
    L.append("")
    L.append("The Brier score (Brier, 1950) is a *proper* scoring rule: your expected score is")
    L.append("only minimised by reporting your honest probability, so you cannot game it by")
    L.append("over- or under-stating confidence. Lower is better. We pair it with calibration")
    L.append("(when you say 60%, it should happen ~60% of the time) and CLV (closing-line value:")
    L.append("did you have the price before the market moved?).")
    L.append("")
    L.append("## Proof — the market graded by its OWN Brier on resolved games")
    L.append("")
    L.append("Closing price on the favourite vs. what actually happened. The formula, not us,")
    L.append("decides who was right.")
    L.append("")
    L.append("| Fixture | Favourite | Market said | Result | Brier (computed) | vs 0.25 coin-flip |")
    L.append("|---|---|---|---:|---:|---|")
    for g in graded:
        res = "favourite WON" if g["favourite_won"] else "**favourite LOST (upset)**"
        verdict = "better" if g["beats_coin_flip"] else "**WORSE**"
        L.append(f"| {g['fixture']} | {g['favourite']} | {g['market_prob']*100:.0f}% "
                 f"| {res} | {g['brier']:.3f} | {verdict} |")
    L.append("")
    n = len(graded)
    worse = sum(1 for g in graded if not g["beats_coin_flip"])
    L.append(f"**Mean market Brier on these {n} cases: {mean_b:.3f}.** "
             f"{worse} of {n} scored worse than a 0.25 coin-flip.")
    L.append("")
    if sa:
        L.append("### The clearest case: Saudi Arabia vs Argentina")
        L.append("")
        L.append(f"- The market priced Argentina at **{sa['market_prob']*100:.1f}%** "
                 f"(≈ −675 American, `implied_prob_american(-675)`).")
        L.append("- Argentina **LOST** 2–1. Actual outcome for the favourite = 0.")
        L.append(f"- `brier({sa['market_prob']}, 0)` = **{sa['brier']:.3f}** — versus 0.25 for a")
        L.append("  coin-flip and 0.00 for a perfect call.")
        L.append("- The formula proves the market was *confidently wrong*. That is a fact the")
        L.append("  arithmetic produced, not an opinion we asserted.")
        L.append("")
    L.append("## Honest scope")
    L.append("")
    L.append("- This seed (`seed-resolved.json`) is an **upset highlight-reel on purpose**. It")
    L.append("  proves the *formula* discriminates right from wrong calls; it is NOT the market's")
    L.append("  true long-run Brier (on a full unbiased schedule the market scores far better).")
    L.append("- We grade favourite-side prices only; a full 1X2 de-vig needs all three closing")
    L.append("  prices. The `baseline.py` rig already does the de-vig and is unit-tested.")
    L.append("")
    L.append("## Our forward call uses this exact template")
    L.append("")
    L.append("Our live USMNT call — *will the USMNT advance from Group D?* — is committed at a")
    L.append("probability **before** the group stage and will be graded by the **same Brier**")
    L.append("after it resolves: identical FutureX format, identical formula, no special pleading.")
    L.append("That is the standard. Everything we ship is gradable by it.")
    L.append("")
    L.append("## How to check this")
    L.append("")
    L.append("- `python3 dataset/golden_template.py` — re-proves the textbook Brier anchors,")
    L.append("  recomputes every row above from `seed-resolved.json`, rewrites this file.")
    L.append("- `python3 dataset/baseline.py` — the self-tested source of `brier` (prints PASS).")
    L.append("- Sources: FutureX arXiv:2508.11987 · Brier (1950), *Monthly Weather Review* 78(1).")
    L.append("  Per-case resolution sources are listed in `seed-resolved.json`.")
    L.append("")
    open(os.path.join(ROOT, "GOLDEN.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    if not recheck_anchors():
        raise SystemExit("anchor re-check failed — refusing to write GOLDEN.md")
    graded = grade_resolved_cases()
    mean_b = print_table(graded)
    write_md(graded, mean_b)
    print("\nwrote dataset/GOLDEN.md")
