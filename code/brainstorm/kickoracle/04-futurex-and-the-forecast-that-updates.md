# 04 — FutureX, and the forecast that updates (the layer above the compiler)

> [03](03-miromind-fit-and-60s-demo.md) is the demo. This doc explains the two ideas
> *underneath* it, in plain words: **why** a research agent can forecast at all (FutureX),
> and the one feature that makes it feel alive (**forecasts that update**). The **compiler**
> (separate, in `/compiler`) is the later milestone that turns these into a track record.
>
> Every section: *what it is · why it works · how to check it.*

---

## A. FutureX — why MiroMind can forecast matches at all

- **What it is:** FutureX is a public test made of **real questions about the future**
  ("who will win X?", "up or down by date Y?"). The important part: each question is
  **graded automatically *after* the event actually happens** — the world supplies the
  answer, nobody can fake it. MiroMind's agent (MiroFlow) was **ranked #1** on it.
- **Why it works for us:** a football match is the same shape — a real event, in the
  future, that resolves to a clear result. So forecasting a match isn't a gimmick; it's
  literally the thing MiroMind is already best-in-class at. And because the match really
  happens, our accuracy number is **honest by construction** — it can't be massaged.
- **How to check:** open the FutureX paper (arXiv 2508.11987) and MiroMind's blog post
  about topping it. The one property to confirm with your own eyes: *questions are scored
  after the event, not before.* That's what makes it real.

---

## B. The forecast that updates (the "interaction" idea)

- **What it is:** a forecast is **not a one-shot guess**. Between now and kickoff the world
  changes — an injury, a confirmed starting XI, weather, a suspension. Each new fact should
  **move the forecast, and the system should say what moved it**: "Brazil 62% → 55% because
  Neymar was ruled out (source)."
- **Why it works:** three reasons. (1) It's **more honest** — a number that never moves is
  pretending the world stood still. (2) It's **more engaging** — a moving line is a *story
  to follow*, which keeps the audience coming back (the audience is the business's real
  asset). (3) It's **what MiroMind is built to do** — it re-researches and re-reasons when
  new information arrives, instead of being a formula frozen weeks ago (which is exactly
  KickOracle's weakness from [01](01-business-teardown.md)).
- **How to check:** take one forecast, hand the system one new fact, and watch. Pass = the
  number changes **and a reason + source is shown**. Fail = it changes silently, or doesn't
  change. (This is a design rule, not a research claim — you test it live.)

---

## C. Where the compiler comes in (the later milestone — separate, in `/compiler`)

- **The problem it solves:** [03](03-miromind-fit-and-60s-demo.md) says the *wedge* is a
  **track-record page** — every forecast, locked before kickoff, then marked ✓/✗ after the
  match, with a running accuracy score. That page only means something if the record behind
  it is **kept honestly and can be checked**. Seeding a few JSON rows is fine for the demo;
  the compiler is what makes it *trustworthy at scale*.
- **What the compiler does (plain):** it reads the history of a forecast — the question, the
  reasoning steps with their sources, the updates (and why), and the final result — and
  writes **one markdown file you can open and read**, plus a small **checker script** that
  re-reads that file and confirms **every claim has a source and a date**. Nothing magic:
  text in, a readable record out, and an automatic "does every claim check out?" pass/fail.
- **Why it works for FIFA:** it produces exactly the thing KickOracle fakes — an **auditable,
  checkable track record** — as a side effect of doing the forecasts properly. The forecast
  and its own grade become a permanent, inspectable record instead of a number on a page.
- **Why it's *later*, not day-one:** the 60s demo ([03](03-miromind-fit-and-60s-demo.md))
  doesn't need it — a handful of seeded rows look alive. The compiler earns its place once
  there are many forecasts to keep honest. It's a **milestone after the demo works**, not a
  prerequisite.
- **How to test it today:** it already runs on a conversation (the only "forecast history"
  we have right now is this project's own conversation):
  ```bash
  python3 compiler/compile.py     # reads a transcript → writes one readable markdown record
  bash    compiler/verify.sh      # re-checks it → "pass" only if every claim has a source
  ```
  Open `compiler/out/trajectory-bootstrap.md` and read it. For FIFA, the input changes from
  "a conversation" to "a match forecast + its result"; the machinery is the same. Full plain
  explanation of what it learned and why it works: [`compiler/README.md`](../../compiler/README.md).

---

## The whole thing in one line

**MiroMind forecasts the match and shows its sources → the line moves as news arrives, with
reasons → the match happens → ✓ or ✗ → the compiler files it into a track record you can
actually check.** That chain is the product, and the last link is the one KickOracle can't show.
