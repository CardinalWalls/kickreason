#!/usr/bin/env python3
"""
build_match_page.py — a REAL per-match page IN the app (KickReason design).

The 60s replay zooms from the macro champion-rooted DAG down into ONE real match node;
this is where that hand-off lands: a real, openable product page for that exact node,
rendered from the GRADED source of truth (arc_2022.graded.json) — every number computed,
every layer sourced, the grade real. Deploy target: site/match.html
(https://CardinalWalls.github.io/kickreason/match.html).

  python3 dataset/build_match_page.py            # -> site/match.html (node arg-ksa)
  python3 dataset/build_match_page.py morocco-portugal   # any graded node id, if present
"""
import html
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARC = os.path.join(HERE, "arc_2022.graded.json")
OUT = os.path.normpath(os.path.join(HERE, "..", "site", "match.html"))
APP_URL = "https://CardinalWalls.github.io/kickreason/"

E = lambda s: html.escape(str(s or ""))
def first(x): return (x[0] if x else {}) if isinstance(x, list) else (x or {})
def aslist(x): return x if isinstance(x, list) else ([x] if x else [])


def src_link(url, label=None):
    if not url:
        return ""
    short = label or url.replace("https://", "").replace("http://", "").replace("www.", "")
    return f'<a class="src" href="{E(url)}" target="_blank" rel="noopener">&#8599; {E(short[:54])}</a>'


def load_node(node_id):
    arc = json.load(open(ARC, encoding="utf-8"))
    for n in arc["nodes"]:
        if (n.get("node_id") or n.get("id")) == node_id:
            return n, arc
    raise SystemExit(f"node '{node_id}' not in {ARC}")


def render(node, arc):
    L = node["layers"]
    g = node["grade"]
    mkt = round(g["market_prob"] * 100)
    fav = g["favourite"]
    brier = g["brier"]
    fixture = node["fixture"]
    comp = node.get("competition", "")
    date = node.get("date", "")
    score = node.get("outcome", {}).get("score", "")
    winner = node.get("outcome", {}).get("winner", "")
    arc_brier = arc["summary"].get("mean_market_brier")

    od = first(L.get("odds"))
    # odds card
    odds_html = (
        f'<div class="lv">{E(od.get("text"))}</div>'
        f'<div class="lsys">{E(od.get("system"))}</div>'
        f'<div class="lsrc">{src_link(od.get("source_url"))}</div>'
    )
    # narrative card (list)
    nv_html = "".join(
        f'<div class="item"><div class="ihead">{E(n.get("storyline"))}</div>'
        f'<div class="itext">{E(n.get("text"))}</div>'
        f'<div class="lsrc"><span class="sys">{E(n.get("system"))}</span> {src_link(n.get("source_url"))}</div></div>'
        for n in aslist(L.get("narrative"))
    )
    # magic-moment card (list)
    mm_html = "".join(
        f'<div class="item"><div class="ihead"><span class="min">{E(m.get("minute"))}</span> {E(m.get("scorer"))}</div>'
        f'<div class="itext">{E(m.get("text"))}</div>'
        f'<div class="lsrc"><span class="sys">{E(m.get("system"))}</span> {src_link(m.get("source_url"))}</div></div>'
        for m in aslist(L.get("magic_moment"))
    )
    # stats card (list)
    st_html = "".join(
        f'<div class="item"><div class="ihead">{E(s.get("metric"))}: <b>{E(s.get("value"))}</b></div>'
        f'<div class="lsrc"><span class="sys">{E(s.get("system"))}</span> {src_link(s.get("source_url"))}</div></div>'
        for s in aslist(L.get("stats"))
    )

    return TEMPLATE.format(
        fixture=E(fixture), comp=E(comp), date=E(date), score=E(score), winner=E(winner),
        fav=E(fav), mkt=mkt, brier=brier, verdict=E(g["verdict"]), arc_brier=arc_brier,
        odds=odds_html, narrative=nv_html, magic=mm_html, stats=st_html, app=APP_URL,
        n_layers=sum(len(aslist(L.get(k))) for k in ("odds", "narrative", "magic_moment", "stats")),
    )


TEMPLATE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{fixture} — KickReason</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Hanken+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#080a09;--panel:#121514;--panel2:#191d18;--ink:#f3f1e9;--mute:#9aa39a;--faint:#5d655c;--line:#262b25;
  --edge:#4cf0a3;--down:#ff6b5e;--break:#ffc24d;--star:#ffd76b;--narr:#8ab4ff;--violet:#c9a0ff}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Hanken Grotesk",sans-serif;line-height:1.5;
  padding:0 0 80px;-webkit-font-smoothing:antialiased}}
a{{color:inherit}}
.wrap{{max-width:980px;margin:0 auto;padding:0 22px}}
.top{{position:sticky;top:0;z-index:10;background:rgba(8,10,9,.92);backdrop-filter:blur(8px);
  border-bottom:1px solid var(--line)}}
.topin{{max-width:980px;margin:0 auto;padding:14px 22px;display:flex;align-items:center;gap:16px}}
.brand{{font-family:"Bricolage Grotesque";font-weight:800;font-size:16px}}.brand .dot{{color:var(--edge)}}
.back{{font-family:"JetBrains Mono";font-size:11px;color:var(--mute);text-decoration:none;letter-spacing:.04em}}
.back:hover{{color:var(--edge)}}
.path{{font-family:"JetBrains Mono";font-size:11px;color:var(--faint);letter-spacing:.03em;margin-left:auto}}
.path b{{color:var(--edge)}}
.hero{{padding:34px 0 8px}}
.kick{{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.28em;text-transform:uppercase;color:var(--edge);margin-bottom:12px}}
h1{{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(28px,5vw,46px);line-height:1.05}}
.sub{{color:var(--mute);font-size:14px;margin-top:8px;font-family:"JetBrains Mono"}}
.grade{{margin:20px 0 6px;border:1px solid var(--down);background:rgba(255,107,94,.08);border-radius:12px;
  padding:16px 18px;display:flex;flex-wrap:wrap;gap:6px 26px;align-items:baseline}}
.grade .big{{font-family:"Bricolage Grotesque";font-weight:800;font-size:30px;color:var(--down)}}
.grade .lab{{font-family:"JetBrains Mono";font-size:11px;color:var(--mute);text-transform:uppercase;letter-spacing:.1em}}
.grade .vd{{flex-basis:100%;color:var(--ink);font-size:14px;margin-top:4px}}
.grade .arc{{flex-basis:100%;color:var(--faint);font-size:12px;font-family:"JetBrains Mono"}}
.lhead{{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:var(--faint);
  margin:30px 0 12px}}
.layers{{display:grid;grid-template-columns:1fr 1fr;gap:14px}}
@media(max-width:760px){{.layers{{grid-template-columns:1fr}}}}
.card{{border:1px solid var(--line);border-left:3px solid var(--lc);background:var(--panel);border-radius:12px;padding:15px 16px}}
.card.od{{--lc:var(--edge)}}.card.nv{{--lc:var(--narr)}}.card.mm{{--lc:var(--star)}}.card.st{{--lc:var(--violet)}}
.ctag{{font-family:"JetBrains Mono";font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:var(--lc);margin-bottom:10px}}
.lv{{font-size:14.5px;color:var(--ink)}}
.lsys{{font-family:"JetBrains Mono";font-size:11px;color:var(--mute);margin-top:8px}}
.item{{padding:9px 0;border-top:1px solid var(--line)}}.item:first-of-type{{border-top:none;padding-top:0}}
.ihead{{font-weight:700;font-size:14px;color:var(--ink)}}.ihead .min{{color:var(--star);font-family:"JetBrains Mono"}}
.ihead b{{color:var(--ink)}}
.itext{{font-size:13px;color:var(--mute);margin-top:3px}}
.lsrc{{margin-top:7px;font-size:11px}}.lsrc .sys{{font-family:"JetBrains Mono";color:var(--faint);margin-right:8px}}
.src{{font-family:"JetBrains Mono";font-size:11px;color:var(--narr);text-decoration:none}}.src:hover{{text-decoration:underline}}
.foot{{margin-top:34px;border-top:1px solid var(--line);padding-top:18px;color:var(--faint);font-size:12px;
  font-family:"JetBrains Mono";display:flex;flex-wrap:wrap;gap:6px 18px;align-items:center}}
.foot a{{color:var(--edge);text-decoration:none}}
.foot .grade-by{{color:var(--mute)}}
</style></head><body>
<div class="top"><div class="topin">
  <span class="brand">KickReason<span class="dot">.</span></span>
  <a class="back" href="./index.html">&larr; the app</a>
  <span class="path">champion &rsaquo; group stage &rsaquo; group C &rsaquo; <b>this match</b> &rsaquo; node</span>
</div></div>
<div class="wrap">
  <div class="hero">
    <div class="kick">one node &middot; 4 sourced layers &middot; graded</div>
    <h1>{fixture}</h1>
    <div class="sub">{comp} &middot; {date} &middot; final {score} &middot; {winner} won</div>
    <div class="grade">
      <div><div class="lab">market priced {fav}</div><div class="big">{mkt}%</div></div>
      <div><div class="lab">result</div><div class="big" style="color:var(--down)">LOST</div></div>
      <div><div class="lab">Brier (lower=better)</div><div class="big">{brier}</div></div>
      <div class="vd">{verdict}</div>
      <div class="arc">graded against the closing market &middot; arc mean Brier across 13 nodes = {arc_brier}</div>
    </div>
    <div class="lhead">the four expert layers &mdash; each concrete, each sourced (click to verify)</div>
    <div class="layers">
      <div class="card od"><div class="ctag">odds &middot; the calibrated price</div>{odds}</div>
      <div class="card nv"><div class="ctag">narrative &middot; the why</div>{narrative}</div>
      <div class="card mm"><div class="ctag">magic moment &middot; the star</div>{magic}</div>
      <div class="card st"><div class="ctag">stats &middot; the hard data</div>{stats}</div>
    </div>
    <div class="foot">
      <span class="grade-by">{n_layers} sourced claims &middot; graded by the compiler (Brier / CLV)</span>
      <span>this is 1 of 8,367 nodes in the champion-rooted DAG</span>
      <a href="./index.html">&#8599; open KickReason</a>
    </div>
  </div>
</div>
</body></html>"""


def main():
    node_id = sys.argv[1] if len(sys.argv) > 1 else "arg-ksa"
    node, arc = load_node(node_id)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    open(OUT, "w", encoding="utf-8").write(render(node, arc))
    L = node["layers"]
    nlayers = sum(len(aslist(L.get(k))) for k in ("odds", "narrative", "magic_moment", "stats"))
    print(f"wrote {os.path.relpath(OUT, HERE)} · {node['fixture']} · "
          f"market {round(node['grade']['market_prob']*100)}% -> Brier {node['grade']['brier']} · "
          f"{nlayers} sourced claims across 4 layers")
    print(f"  deploy URL: {APP_URL}match.html")


if __name__ == "__main__":
    main()
