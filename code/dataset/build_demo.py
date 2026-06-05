#!/usr/bin/env python3
"""
build_demo.py — the MASTER demo (the 7-point spec). Scrollable, video-recordable, self-contained.
Real data where we have it (champion node, arc layers, 8,367-node DAG, the final's bettor sub-Qs);
faithful labeled [MOCK] for the interactive/report sections. Prove-the-kernel → mock-the-scale.

  §1 how MiroMind predicts, champion → details
  §2 the prompted LAYERED reasoning (factors per node)
  §3 the extracted DAG (manipulable)
  §4 every node is debatable → interactions = the flywheel
  §5 eyeball content (auto-generated)
  §6 expert reports: intel · bet · business · tools
  §7 the complexity: a bettor needs the SCORELINE — not one "who wins" node

  python3 dataset/build_demo.py  ->  dataset/demo.html  (open via file://)
"""
import json, os, re, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))
hesc = lambda s: html.escape(str(s if s is not None else ""))
clean = lambda s, n=300: re.sub(r"\s+", " ", (s or "").replace("**", "")).strip()[:n]
host = lambda u: (re.match(r"https?://([^/]+)", u or "") or [None, "source"])[1].replace("www.", "") if u else "source"

# ── real assets ──
QS = json.load(open(os.path.join(HERE, "questions_2022.json")))
COUNTS = json.load(open(os.path.join(HERE, "questions_2022.counts.json")))
ARC = json.load(open(os.path.join(HERE, "arc_2022.graded.json")))
champ_f = sorted(glob.glob(os.path.join(HERE, "nodes", "who-will-win*.json")), key=os.path.getmtime)
CHAMP = json.load(open(champ_f[-1])) if champ_f else {}
saudi = next(n for n in ARC["nodes"] if (n.get("node_id") or n.get("id")) == "arg-ksa")
SL = saudi["layers"]

# champion position: the live node's is heuristic-garbled; take a clean sentence from its narrative
cpos = clean(CHAMP.get("position"), 120)
if not re.search(r"[A-Z][a-z]+", cpos) or cpos.startswith(("1%", "(see")):
    sents = re.split(r"(?<=[.!?])\s+", CHAMP.get("narrative", ""))
    cpos = clean(next((s for s in sents if re.search(r"Spain|Argentina|France|Brazil|favou?rite|win", s)), sents[0] if sents else ""), 200)
cmeta = CHAMP.get("_meta", {})

# the final's real bettor sub-questions (point 7) — by real stage (subject is a pre-draw slot)
final_qs = [q for q in QS if q["category"] == "match_core" and q.get("stage") == "Final"]
final_show = [q for q in final_qs if any(k in (q.get("market", "").lower()) for k in
              ["result", "correct", "both teams", "2.5", "double chance", "draw no bet", "1.5 goals", "first half"])][:9] or final_qs[:9]


def src(u):
    return f'<a class="src" href="{hesc(u)}" target="_blank">↗ {hesc(host(u))}</a>' if u else ""


# §2 the 6 layers (4 real from the arc, 2 framed for the demo)
mm = (SL.get("magic_moment") or [{}])[-1]
nv = (SL.get("narrative") or [{}])[0]
st = (SL.get("stats") or [{}])[0]
od = SL.get("odds") or {}
LAYERS = [
    ("odds", "the calibrated price (bettors, books)", clean(od.get("text"), 150), od.get("source_url"), "real · graded Brier 0.76"),
    ("stats", "xG / shots / the data (clubs, analysts)", f"{st.get('metric','')}: {st.get('value','')}", st.get("source_url"), "real · sourced"),
    ("narrative", "the WHY / storyline (media, fans)", f"{nv.get('storyline','')} — {clean(nv.get('text'),110)}", nv.get("source_url"), "real · sourced"),
    ("magic_moment", "the star / drama (broadcast, social)", f"{mm.get('minute','')} {mm.get('scorer','')} — {clean(mm.get('text'),100)}", mm.get("source_url"), "real · sourced"),
    ("actionable", "the one move before the deadline (DFS/props)", "Fade Argentina -650; the de-vig leaves Saudi +EV vs the 0.14-xG trap read", None, "[MOCK — the pick layer]"),
    ("calibration", "how it's graded after it resolves (the track record)", "Locked pre-match at 87% → graded Brier 0.76 (confidently wrong) → into the public record", None, "real grade · [MOCK framing]"),
]

LAYER_HTML = "".join(
    f'<div class="lyr l-{k}"><div class="lh"><span class="lk">{hesc(k)}</span><span class="lt">{hesc(who)}</span></div>'
    f'<div class="lv">{hesc(txt)}</div><div class="lm">{src(u)} <span class="flag">{hesc(flag)}</span></div></div>'
    for k, who, txt, u, flag in LAYERS)

ARG_HTML = "".join(
    f'<div class="q"><span class="ql {hesc(q.get("layer",""))}">{hesc((q.get("layer") or "")[:4])}</span>'
    f'<span class="qt">{hesc(q.get("market"))}</span>'
    + (f'<span class="res">→ {hesc(q.get("resolved"))}</span>' if q.get("resolved") else "") + "</div>"
    for q in final_show)

REPORTS = [
    ("intel", "Analyst brief", "The title turns on Spain's midfield control + Yamal's fitness; the contender quietly exposed is the side with the thinnest knockout-tested spine.", "narrative + stats"),
    ("bet", "Bettor edge", "Don't take 'who wins' — the value is the de-vigged scoreline & props: correct-score longshots and BTTS where the market lags the xG.", "odds + actionable"),
    ("business", "Rights/sponsor", "Which storylines + magic-moments will spike attention (the clippable swings) — sponsor exposure mapped to forecast volatility.", "magic_moment + narrative"),
    ("tools", "Fan/FPL", "Captaincy + bracket picks seeded by the same trace; argue with each, lock it, see it graded.", "actionable + calibration"),
]
REPORT_HTML = "".join(
    f'<div class="rep"><div class="rk">{hesc(k)}</div><div class="rn">{hesc(name)}</div>'
    f'<div class="rt">{hesc(txt)}</div><div class="rf">from layers: {hesc(fr)} · [MOCK report — real layers underneath]</div></div>'
    for k, name, txt, fr in REPORTS)

TOTAL = COUNTS["total"]
DOC = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>the system — 7 ways · champion-rooted, MiroMind-reasoned, debatable</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Hanken+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#080a09;--panel:#121514;--p2:#0c0f0d;--ink:#f3f1e9;--mute:#9aa39a;--faint:#5d655c;--line:#20251f;--edge:#4cf0a3;--down:#ff6b5e;--break:#ffc24d;--narr:#8ab4ff;--violet:#c9a0ff;--star:#ffd76b}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Hanken Grotesk",sans-serif;line-height:1.45}}
.wrap{{max-width:1060px;margin:0 auto;padding:30px 22px 90px}}
.hero{{text-align:center;padding:30px 0 22px;border-bottom:1px solid var(--line)}}
.nm{{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(30px,5vw,56px);letter-spacing:-.02em}}.nm .d{{color:var(--edge)}}
.tag{{color:var(--mute);font-size:clamp(15px,1.8vw,20px);margin-top:8px}}
.sub{{font-family:"JetBrains Mono";font-size:12px;color:var(--faint);margin-top:10px}}
section{{margin-top:40px}}
.sh{{font-family:"JetBrains Mono";font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--edge);margin-bottom:6px}}
h2{{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(20px,2.8vw,30px);margin-bottom:12px;letter-spacing:-.01em}}
.lead{{color:var(--mute);font-size:15px;margin-bottom:14px;max-width:72ch}}
.panel{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px}}
.chain{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:8px 0}}
.cn{{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:9px 13px;font-size:13px}}
.cn.hot{{border-color:var(--edge)}}.cn b{{font-family:"Bricolage Grotesque"}}.ar{{color:var(--faint)}}
.mmn{{border-left:3px solid var(--edge)}}.mmn .pos{{font-size:15px;margin:6px 0}}.mmn .meta{{font-family:"JetBrains Mono";font-size:11px;color:var(--faint)}}
.lyr{{border:1px solid var(--line);border-left:3px solid var(--lc,var(--line));border-radius:10px;padding:11px 14px;margin-bottom:8px}}
.l-odds{{--lc:var(--edge)}}.l-stats{{--lc:var(--violet)}}.l-narrative{{--lc:var(--narr)}}.l-magic_moment{{--lc:var(--star)}}.l-actionable{{--lc:var(--break)}}.l-calibration{{--lc:#67e8f9}}
.lh{{display:flex;gap:10px;align-items:baseline}}.lk{{font-family:"JetBrains Mono";font-size:11px;text-transform:uppercase;letter-spacing:.08em;color:var(--lc);font-weight:700}}.lt{{font-size:11.5px;color:var(--faint)}}
.lv{{font-size:13.5px;margin-top:4px}}.lm{{font-size:11px;color:var(--faint);margin-top:5px}}.src{{color:var(--narr);text-decoration:none;font-family:"JetBrains Mono"}}.flag{{margin-left:6px}}
details.dag summary{{cursor:pointer;font-size:14px;padding:6px 0;list-style:none}}details.dag summary::before{{content:"▸ ";color:var(--faint)}}details.dag[open]>summary::before{{content:"▾ "}}
.dag .bd{{border-left:1px solid var(--line);margin-left:8px;padding-left:12px}}
.cnt{{font-family:"JetBrains Mono";font-size:10.5px;color:var(--edge);border:1px solid var(--line);border-radius:5px;padding:1px 6px;margin-left:6px}}
.q{{display:flex;gap:8px;align-items:baseline;padding:4px 0;border-bottom:1px solid #14180f;font-size:12.5px}}
.ql{{font-family:"JetBrains Mono";font-size:9px;text-transform:uppercase;border:1px solid var(--line);border-radius:3px;padding:1px 4px;color:var(--faint);min-width:34px;text-align:center}}.ql.odds{{color:var(--edge)}}.ql.stats{{color:var(--violet)}}
.qt{{color:var(--mute);flex:1}}.res{{font-family:"JetBrains Mono";font-size:11px;color:var(--edge)}}
.debate .u{{color:var(--narr)}}.debate .a{{color:var(--edge)}}.debate div{{margin:6px 0;font-size:14px}}
.fly{{font-family:"JetBrains Mono";font-size:11.5px;color:var(--break);margin-top:8px}}
.eye{{border-left:3px solid var(--star)}}.eye .big{{font-family:"Bricolage Grotesque";font-weight:800;font-size:22px}}
.reps{{display:grid;grid-template-columns:1fr 1fr;gap:12px}}@media(max-width:820px){{.reps{{grid-template-columns:1fr}}}}
.rep{{background:var(--panel);border:1px solid var(--line);border-top:3px solid var(--break);border-radius:11px;padding:14px}}
.rk{{font-family:"JetBrains Mono";font-size:11px;text-transform:uppercase;letter-spacing:.1em;color:var(--break)}}.rn{{font-family:"Bricolage Grotesque";font-weight:700;font-size:16px;margin:3px 0}}.rt{{font-size:13.5px;color:var(--ink)}}.rf{{font-family:"JetBrains Mono";font-size:10.5px;color:var(--faint);margin-top:8px}}
.mock{{font-family:"JetBrains Mono";font-size:10px;color:var(--break);border:1px solid var(--break);border-radius:4px;padding:1px 5px;margin-left:8px}}
.foot{{margin-top:46px;border-top:1px solid var(--line);padding-top:14px;font-family:"JetBrains Mono";font-size:11px;color:var(--faint);line-height:1.7}}
.ok{{color:var(--edge)}}.mk{{color:var(--break)}}
</style></head><body><div class="wrap">
<div class="hero">
  <div class="nm">KickReason<span class="d">.</span></div>
  <div class="tag">Argue with every pick — all the way to the champion.</div>
  <div class="sub">the system, 7 ways · champion-rooted · MiroMind-reasoned · debatable · {TOTAL:,} real nodes on 2022</div>
</div>

<section><div class="sh">① how MiroMind predicts — champion → details</div>
  <h2>Top-down: the champion question spawns the details</h2>
  <div class="lead">One MiroMind call reasons the apex; the answer decomposes into the sub-questions it depends on — drill down to any detail. (Sampling the top node live; deeper nodes mocked faithfully.)</div>
  <div class="panel mmn"><div class="meta">CHAMPION · reasoned live by MiroMind · {cmeta.get('elapsed_s','?')}s · {cmeta.get('n_sources','?')} sources · {(cmeta.get('tokens') or 0):,} tokens</div>
    <div class="pos">{hesc(cpos)}</div></div>
  <div class="chain">
    <div class="cn hot"><b>Who is champion?</b></div><span class="ar">→ depends on →</span>
    <div class="cn">Who reaches the final?</div><span class="ar">→</span>
    <div class="cn">Argentina vs France — who wins?</div><span class="ar">→</span>
    <div class="cn">…the correct score <span class="mock">deeper = mock</span></div>
  </div></section>

<section><div class="sh">② the prompted reasoning — layers of factors</div>
  <h2>Each node, seen through 6 professional layers</h2>
  <div class="lead">We prompt MiroMind with our deep-researched layer taxonomy, so each node carries reasonable, sourced factors for every buyer. Example node: <b>Saudi Arabia 1–2 Argentina</b>.</div>
  {LAYER_HTML}</section>

<section><div class="sh">③ the extracted DAG — manipulable</div>
  <h2>The compiler turns reasoning into a graph you can walk</h2>
  <div class="lead">{TOTAL:,} real nodes, champion-rooted, edges = the real 2022 tournament. Expand a branch (full graph in <b>dag.html</b>). Manipulate = re-run / edit / add a node <span class="mock">interaction = mock</span>.</div>
  <div class="panel">
    <details class="dag" open><summary>WHO IS THE CHAMPION? → Argentina ✓ <span class="cnt">{TOTAL:,}</span></summary><div class="bd">
      <details class="dag"><summary>Final <span class="cnt">{len(final_qs)}</span></summary><div class="bd">
        <details class="dag"><summary>Argentina vs France 3-3 (4-2 pens) <span class="cnt">{len(final_qs)}</span></summary><div class="bd">{ARG_HTML}</div></details>
      </div></details>
      <details class="dag"><summary>Semi-finals · Quarter-finals · Round of 16 · Group stage (A–H) <span class="cnt">→ dag.html</span></summary><div class="bd"><div class="q"><span class="qt">8 groups · 64 fixtures · match + player nodes — 8,367 in total</span></div></div></details>
    </div></details>
  </div></section>

<section><div class="sh">④ every node is debatable — interactions feed the flywheel</div>
  <h2>You don't read it. You argue with it.</h2>
  <div class="panel debate">
    <div><span class="u">you:</span> "Argentina 87% — that ignores Saudi's offside trap." <span class="mock">mock interaction</span></div>
    <div><span class="a">node:</span> here's the sourced counter-case (6 first-half offsides, 0.14 xG, the trap) {src(nv.get('source_url'))} — and the grade says the 87% was confidently wrong (Brier 0.76). Lock your take; the scoreboard settles it.</div>
    <div class="fly">→ every challenge, counter-take and re-run relabels the node — the human-stakes trajectory data MiroVerse lacks. Interaction IS the flywheel.</div>
  </div></section>

<section><div class="sh">⑤ content that catches the eyeball</div>
  <h2>The same trace, rendered for attention</h2>
  <div class="panel eye"><div class="big">{hesc(mm.get('minute',''))} {hesc(mm.get('scorer',''))} — the goal that broke the champions</div>
    <div class="lead" style="margin:8px 0 4px">{hesc(clean(mm.get('text'),200))}</div>
    <div class="meta" style="font-family:'JetBrains Mono';font-size:11px;color:var(--faint)">auto-generated shareable: clip caption · the 87%→WRONG hook · {src(mm.get('source_url'))} <span class="mock">render = mock; moment is real</span></div></div></section>

<section><div class="sh">⑥ expert reports — one trace, four buyers</div>
  <h2>Intel · Bet · Business · Tools</h2>
  <div class="lead">The same reasoned node, re-rendered for each buyer. <span class="mock">report copy = mock; the layers underneath are real + sourced</span></div>
  <div class="reps">{REPORT_HTML}</div></section>

<section><div class="sh">⑦ why it's complex — a bettor needs the SCORELINE</div>
  <h2>"Who wins" is one of <b>{len(final_qs)}</b> nodes for the final alone</h2>
  <div class="lead">A single question can't serve a bettor. The real match decomposes into result, scoreline, BTTS, totals, props — each its own valued, debatable, gradable node. Real nodes for <b>Argentina vs France (final)</b>:</div>
  <div class="panel">{ARG_HTML}</div></section>

<div class="foot">
  <b>What's real vs mock (no faking):</b><br>
  <span class="ok">REAL</span>: the champion node (live MiroMind, {cmeta.get('elapsed_s','?')}s/{cmeta.get('n_sources','?')} sources) · the 4 arc layers (odds/stats/narrative/magic, sourced + graded Brier 0.76) · the {TOTAL:,}-node DAG on real 2022 data (lib2022/StatsBomb) · the final's {len(final_qs)} real bettor sub-questions.<br>
  <span class="mk">MOCK (labeled)</span>: the actionable/calibration layer copy · the debate interaction · the eyeball render · the 4 expert-report write-ups — faithful shapes of the proven kernel, not yet generated live.<br>
  Prove the kernel for real → mock the scale faithfully.
</div>
</div></body></html>"""

open(os.path.join(HERE, "demo.html"), "w", encoding="utf-8").write(DOC)
print(f"wrote dataset/demo.html · 7 sections · {TOTAL:,} nodes · final sub-Qs={len(final_qs)} · champion={cmeta.get('n_sources','?')} sources")
print("  open: open dataset/demo.html")
