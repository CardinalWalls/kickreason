#!/usr/bin/env python3
"""
build_mass.py — render the REAL mass: every one of the 8,367 question-nodes from
questions_2022.json, rooted at the champion, with the REAL MiroMind-reasoned nodes
featured at the top. No placeholders, no JS — static HTML, ~50 pages of real data.

  python3 dataset/build_mass.py   ->   dataset/mass.html  (open via file://)
"""
import json, os, re, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))


def clean(s, n=260):
    s = (s or "").replace("**", "").replace("\\n", " ")
    s = re.sub(r"\s+", " ", s).strip().lstrip(":").strip()
    return s[:n] + ("…" if len(s) > n else "")


def hesc(s):
    return html.escape(str(s if s is not None else ""))


def host(u):
    m = re.match(r"https?://([^/]+)", u or "")
    return (m.group(1).replace("www.", "") if m else "src")


QS = json.load(open(os.path.join(HERE, "questions_2022.json")))
COUNTS = json.load(open(os.path.join(HERE, "questions_2022.counts.json")))
NODES = [json.load(open(f)) for f in sorted(glob.glob(os.path.join(HERE, "nodes", "*.json")))]
PLAYERS = json.load(open(os.path.join(HERE, "lib2022", "players.json")))
nplayers = len(PLAYERS if isinstance(PLAYERS, list) else PLAYERS.get("players", PLAYERS))

CHAMPION = next((q.get("resolved") for q in QS if q.get("market", "").startswith("Tournament winner")), "Argentina")

CAT_ORDER = [("futures", "Futures — the title race"), ("group", "Group outcomes"),
             ("progression", "Progression — how far each side goes"),
             ("match_core", "Match nodes — result · stats · moment (all 64)"),
             ("player_prop", "Player nodes — props across 681 players")]
bycat = {}
for q in QS:
    bycat.setdefault(q["category"], []).append(q)


def node_card(n):
    args = "".join(
        f'<div class="arg">· {hesc(clean(a.get("claim"), 120))} '
        f'<a href="{hesc(a.get("source"))}" target="_blank">↗ {hesc(host(a.get("source")))}</a></div>'
        for a in (n.get("arguments") or [])[:5])
    m = n.get("_meta", {})
    return f"""<div class="mnode">
      <div class="mq">{hesc(clean(n.get("question"), 160))}</div>
      <div class="mp"><b>position:</b> {hesc(clean(n.get("position"), 220))}</div>
      <div class="margs">{args}</div>
      <div class="mcp"><b>counterpoint:</b> {hesc(clean(n.get("counterpoint"), 220)) or "—"}</div>
      <div class="mmeta">reasoned live by MiroMind · {m.get("n_sources","?")} sources · {(m.get("tokens") or 0):,} tokens · compiled → debatable node</div>
    </div>"""


def q_row(q):
    subj = q.get("subject", "")
    mk = q.get("market") or q.get("prop") or q.get("metric") or ""
    res = q.get("resolved")
    badge = f'<span class="res">→ {hesc(res)}</span>' if res else ""
    val = ' val' if q.get("valuable") else ''
    return (f'<div class="qr{val}"><span class="ql {hesc(q.get("layer",""))}">{hesc(q.get("layer",""))}</span>'
            f'<span class="qid">{hesc(q.get("id",""))}</span>'
            f'<span class="qt">{hesc(subj)} · {hesc(mk)}</span>{badge}</div>')


sections = []
for cat, title in CAT_ORDER:
    rows = bycat.get(cat, [])
    if not rows:
        continue
    body = "".join(q_row(q) for q in rows)
    sections.append(f'<section><h2>{hesc(title)} <span class="cn">{len(rows):,} nodes</span></h2>'
                    f'<div class="qgrid">{body}</div></section>')

HTMLDOC = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>the mass — {len(QS):,} real question-nodes, rooted at the champion</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Hanken+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#080a09;--panel:#121514;--p2:#0c0f0d;--ink:#f3f1e9;--mute:#9aa39a;--faint:#5d655c;--line:#20251f;
  --edge:#4cf0a3;--down:#ff6b5e;--break:#ffc24d;--star:#ffd76b;--narr:#8ab4ff;--violet:#c9a0ff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Hanken Grotesk",sans-serif;line-height:1.4}}
.wrap{{max-width:1180px;margin:0 auto;padding:30px 24px 80px}}
.hero{{text-align:center;padding:40px 0 26px;border-bottom:1px solid var(--line)}}
.kick{{font-family:"JetBrains Mono";font-size:12px;letter-spacing:.3em;text-transform:uppercase;color:var(--edge)}}
.champ{{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(30px,5vw,58px);letter-spacing:-.02em;margin:12px 0 6px}}
.champ .a{{color:var(--star)}}
.scale{{font-family:"JetBrains Mono";font-size:13px;color:var(--mute);margin-top:10px}}
.scale b{{color:var(--ink)}}
.note{{color:var(--faint);font-size:12.5px;margin-top:8px}}
.feat{{margin:26px 0 10px}}.feat .h{{font-family:"JetBrains Mono";font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--violet);margin-bottom:12px}}
.fgrid{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}@media(max-width:860px){{.fgrid{{grid-template-columns:1fr}}}}
.mnode{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--edge);border-radius:12px;padding:16px 18px}}
.mq{{font-family:"Bricolage Grotesque";font-weight:700;font-size:16px}}
.mp{{font-size:13.5px;margin-top:8px}}.mp b{{color:var(--edge);font-family:"JetBrains Mono";font-size:11px;text-transform:uppercase;letter-spacing:.08em}}
.margs{{margin:8px 0}}.arg{{font-size:12.5px;color:var(--mute);margin:3px 0}}.arg a{{color:var(--narr);font-family:"JetBrains Mono";font-size:11px;text-decoration:none}}
.mcp{{font-size:12.5px;color:var(--down);margin-top:4px}}.mcp b{{font-family:"JetBrains Mono";font-size:11px;text-transform:uppercase;letter-spacing:.08em}}
.mmeta{{font-family:"JetBrains Mono";font-size:10.5px;color:var(--faint);margin-top:9px;border-top:1px solid var(--line);padding-top:7px}}
section{{margin-top:30px}}
h2{{font-family:"Bricolage Grotesque";font-weight:800;font-size:21px;margin-bottom:10px;position:sticky;top:0;background:var(--bg);padding:8px 0;border-bottom:1px solid var(--line);z-index:2}}
h2 .cn{{font-family:"JetBrains Mono";font-size:12px;color:var(--edge);font-weight:400;margin-left:8px}}
.qgrid{{display:grid;grid-template-columns:1fr 1fr;gap:0 22px}}@media(max-width:860px){{.qgrid{{grid-template-columns:1fr}}}}
.qr{{display:flex;align-items:baseline;gap:8px;padding:4px 0;border-bottom:1px solid #14180f;font-size:12.5px}}
.qr.val{{background:rgba(76,240,163,.03)}}
.ql{{font-family:"JetBrains Mono";font-size:9px;text-transform:uppercase;letter-spacing:.05em;padding:1px 5px;border-radius:4px;color:var(--faint);border:1px solid var(--line);min-width:46px;text-align:center}}
.ql.odds{{color:var(--edge);border-color:#1d5b40}}.ql.stats{{color:var(--violet);border-color:#4a3a6b}}.ql.narrative{{color:var(--break);border-color:#6b5520}}
.qid{{font-family:"JetBrains Mono";font-size:10px;color:var(--faint)}}
.qt{{color:var(--mute);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}
.res{{font-family:"JetBrains Mono";font-size:11px;color:var(--edge)}}
.foot{{margin-top:40px;text-align:center;font-family:"JetBrains Mono";font-size:11.5px;color:var(--faint)}}
</style></head><body><div class="wrap">
<div class="hero">
  <div class="kick">★ the law — every valued node ladders to the final one</div>
  <div class="champ">WHO IS THE CHAMPION? <span class="a">→ {hesc(CHAMPION)} ✓</span></div>
  <div class="scale"><b>{len(QS):,}</b> real question-nodes · <b>{COUNTS.get('matches')}</b> matches · <b>{COUNTS.get('teams')}</b> teams · <b>{nplayers}</b> players · <b>{COUNTS.get('valuable'):,}</b> flagged valuable</div>
  <div class="note">Grounded in the StatsBomb 2022 library (dataset/lib2022) — real results, xG, events, odds. Not a number we invented: every node below is real.</div>
</div>

<div class="feat"><div class="h">2 of these {len(QS):,} nodes, reasoned live by MiroMind & compiled to debatable nodes (the kernel — the rest is the universe they live in):</div>
  <div class="fgrid">{''.join(node_card(n) for n in NODES)}</div>
</div>

{''.join(sections)}

<div class="foot">{len(QS):,} nodes rendered from questions_2022.json · prove the kernel for real (MiroMind above), ground the scale in real 2022 data (the universe below) · rooted at the champion.</div>
</div></body></html>"""

open(os.path.join(HERE, "mass.html"), "w", encoding="utf-8").write(HTMLDOC)
kb = len(HTMLDOC) // 1024
print(f"wrote dataset/mass.html ({kb:,} KB · {len(QS):,} real nodes rendered · {len(NODES)} MiroMind nodes featured)")
print(f"  champion: {CHAMPION} · categories: " + ", ".join(f"{c}={len(bycat.get(c,[]))}" for c, _ in CAT_ORDER))
print("  open: open dataset/mass.html")
