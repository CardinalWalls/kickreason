#!/usr/bin/env python3
"""
baseline.py — track 1: the scoring rig + the market baseline (NO agent involved).

Plain version of what this does:
  1. Turn betting odds into the market's own probability.
  2. Strip the bookmaker's margin ("de-vig") so the probabilities are fair.
  3. Score probabilities against what actually happened — two standard numbers:
       • Brier score  = average of (probability - outcome)^2.  Lower is better.
                        0 = perfect, 0.25 = a coin-flip guess, 1 = confidently wrong.
       • Log loss     = punishes confident wrong calls harder.  Lower is better.
  4. Calibration = when you say 60%, does it happen ~60% of the time?

WHY it matters: this is the number a real MiroMind forecast would have to BEAT.
You build it on PAST data with no agent, so there's no lookahead problem.

Run it:   python3 dataset/baseline.py
It self-tests the math first (prints PASS/FAIL), then runs on dataset/seed-resolved.json
and writes a plain dataset/baseline.md.  It is honest that our seed sample is too small
and deliberately upset-biased to be a REAL baseline — that's the point it proves.
"""
import json, math, os

ROOT = os.path.dirname(os.path.abspath(__file__))


# ── the math (each tiny, each testable) ──────────────────────────────────────
def implied_prob_american(odds):
    """American moneyline -> implied probability. +150 -> 0.40, -200 -> 0.667."""
    odds = float(odds)
    if odds > 0:
        return 100.0 / (odds + 100.0)
    return (-odds) / ((-odds) + 100.0)


def devig(probs):
    """Remove the bookmaker margin by normalising raw implied probs to sum to 1.
    (Simple normalisation de-vig; other methods exist — Shin, power — noted in the md.)"""
    total = sum(probs)
    if total <= 0:
        raise ValueError("probs must sum to > 0")
    return [p / total for p in probs]


def brier(prob, outcome):
    """Single-event Brier: (prob - outcome)^2, outcome is 1 if it happened else 0."""
    return (prob - outcome) ** 2


def log_loss(prob, outcome, eps=1e-15):
    p = min(max(prob, eps), 1 - eps)
    return -(outcome * math.log(p) + (1 - outcome) * math.log(1 - p))


def score_set(pairs):
    """pairs = list of (prob, outcome). Returns mean Brier, mean log loss, n."""
    if not pairs:
        return {"n": 0, "brier": None, "log_loss": None}
    n = len(pairs)
    return {
        "n": n,
        "brier": sum(brier(p, o) for p, o in pairs) / n,
        "log_loss": sum(log_loss(p, o) for p, o in pairs) / n,
    }


# ── self-test: prove the math on textbook values before trusting it ──────────
def self_test():
    checks = [
        ("implied +100 = 0.5", abs(implied_prob_american(100) - 0.5) < 1e-9),
        ("implied -200 = 0.667", abs(implied_prob_american(-200) - 2/3) < 1e-9),
        ("devig [.55,.55] sums to 1", abs(sum(devig([0.55, 0.55])) - 1.0) < 1e-9),
        ("devig [.55,.55] -> .5 each", abs(devig([0.55, 0.55])[0] - 0.5) < 1e-9),
        ("brier perfect = 0", brier(1.0, 1) == 0.0),
        ("brier coin-flip = 0.25", brier(0.5, 1) == 0.25),
        ("brier confident-wrong = 1", brier(0.0, 1) == 1.0),
        ("log_loss 0.5 = ln2", abs(log_loss(0.5, 1) - math.log(2)) < 1e-9),
        ("score_set mean", abs(score_set([(0.5, 1), (0.5, 0)])["brier"] - 0.25) < 1e-9),
    ]
    ok = all(p for _, p in checks)
    print("self-test:", "PASS" if ok else "FAIL")
    for name, p in checks:
        print(f"  {'✓' if p else '✗'} {name}")
    return ok


# ── run the rig on the seed data, and be honest about what it can't say ──────
def run_on_seed():
    path = os.path.join(ROOT, "seed-resolved.json")
    rows = json.load(open(path))
    usable, skipped = [], []
    for r in rows:
        pm = r.get("pre_match", {})
        prob = pm.get("market_prob_or_null")
        fav = pm.get("favourite")
        # only rows with a real favourite + a market price + a clear win/loss
        if prob is None or not fav or "even" in str(fav).lower() or "outright" in r["id"]:
            skipped.append((r["fixture"], "no clean favourite price" if prob is None else "coin-flip / futures"))
            continue
        favourite_won = 0 if r.get("upset") else 1   # upset = the favourite lost
        usable.append({"fixture": r["fixture"], "p": prob, "won": favourite_won})

    s = score_set([(u["p"], u["won"]) for u in usable])
    return usable, skipped, s


def write_md(usable, skipped, s):
    L = []
    L.append("# Market baseline (track 1) — the rig works; the sample doesn't (yet)")
    L.append("")
    L.append("> Auto-written by `python3 dataset/baseline.py`. The scoring math is **self-tested and")
    L.append("> correct** (run it — it prints PASS). But the number below is **not a real baseline**,")
    L.append("> and the script is honest about why. No agent is involved here — this is pure past data.")
    L.append("")
    L.append("## What the rig computed on our seed rows")
    L.append("")
    L.append("| Fixture | Market said favourite wins | Favourite actually won? |")
    L.append("|---|---|---|")
    for u in usable:
        L.append(f"| {u['fixture']} | {u['p']*100:.0f}% | {'yes' if u['won'] else 'NO (upset)'} |")
    L.append("")
    if s["n"]:
        L.append(f"**Market Brier on these {s['n']} rows: {s['brier']:.3f}**  ·  log loss: {s['log_loss']:.3f}")
        L.append("(Brier: 0 = perfect, 0.25 = coin-flip, 1 = confidently wrong.)")
    L.append("")
    L.append("## Why this is NOT a real baseline (the honest part)")
    L.append("")
    L.append("- **The sample is upset-biased on purpose.** `seed-resolved.json` was hand-picked to")
    L.append("  feature famous upsets. So the market 'looks bad' here (it backed favourites who lost)")
    L.append("  ONLY because we cherry-picked the games it got wrong. On a full, unbiased schedule the")
    L.append("  market scores far better. This number would defame the market — don't quote it.")
    L.append(f"- **N is tiny ({s['n']}).** You can't calibrate anything on a handful of games.")
    L.append("- **These are favourite-only prices, not full 1X2.** A proper de-vig needs all three")
    L.append("  match prices (home / draw / away) at the close; the seed has rough, single-side numbers.")
    if skipped:
        L.append("- **Rows skipped** (no clean favourite price, or coin-flip/futures): "
                 + "; ".join(f"{fx} ({why})" for fx, why in skipped) + ".")
    L.append("")
    L.append("## What a real baseline needs (the dataset to plug in here)")
    L.append("")
    L.append("- Full **closing 1X2 odds** for many matches (so we can de-vig properly), paired with results.")
    L.append("- A complete competition or season, **not** a highlight reel — so it's unbiased.")
    L.append("- Candidate sources (being located by the parallel research pass): football-data.co.uk")
    L.append("  closing columns, FiveThirtyEight's published World Cup forecast CSVs (a beatable baseline),")
    L.append("  and historical odds feeds. Swap that file in where `run_on_seed()` reads, and this same,")
    L.append("  already-validated rig produces the real number a MiroMind forecast must beat.")
    L.append("")
    L.append("## How to check this")
    L.append("")
    L.append("- `python3 dataset/baseline.py` — re-runs the self-test (math correctness) and rewrites this file.")
    L.append("- The Brier/log-loss definitions and the de-vig are in the script, each with a unit test.")
    L.append("")
    open(os.path.join(ROOT, "baseline.md"), "w").write("\n".join(L))


if __name__ == "__main__":
    passed = self_test()
    if not passed:
        raise SystemExit("self-test failed — not writing baseline.md")
    usable, skipped, s = run_on_seed()
    write_md(usable, skipped, s)
    n = s["n"]
    b = f"{s['brier']:.3f}" if s["brier"] is not None else "n/a"
    print(f"\nran rig on seed: {n} usable rows, market Brier {b} (illustrative only — see baseline.md)")
    print("wrote dataset/baseline.md")
