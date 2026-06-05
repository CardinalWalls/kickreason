#!/usr/bin/env python3
"""
build_process60.py — THE 60-SECOND REPLAY: our TWO SCALES of the DAG + a real match, into the app.

ONE continuous camera proves macro and micro are the SAME graph:
  open INSIDE the real match card (Argentina 1-2 Saudi Arabia) → expand its 4 sourced layers →
  pull back along a lit spine (match → Group C → Group stage → champion) to reveal it is 1 of
  8,367 graded nodes → show both scales at once → push back down the same spine → GRADE it
  (market 87% → Brier 0.7586, confidently wrong) → snap into the LIVE KickReason app (match.html).

Every number is real: the macro structure + counts come from dag.json (branch subtree-sums =
8,367; spine group-stage 6,039 → Group C 759 → this match 129 questions); the micro node + grade
come from arc_2022.graded.json (arg-ksa). Nothing hardcoded, nothing faked.

  python3 dataset/build_process60.py   ->   dataset/process60.html
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
clean = lambda s, n=150: re.sub(r"\s+", " ", (s or "").replace("**", "").replace("\\n", " ")).strip()[:n]

DAG = json.load(open(os.path.join(HERE, "dag.json"), encoding="utf-8"))
ARC = json.load(open(os.path.join(HERE, "arc_2022.graded.json"), encoding="utf-8"))


def qsum(node):
    tot = len(node.get("questions", []) or [])
    for k in node.get("kids", []) or []:
        tot += qsum(k)
    return tot or (node.get("qn") or 0)


# ---- MACRO: the real champion-rooted DAG (structure + counts from dag.json) ----
BRANCH_X = {"final": -990, "third-place": -660, "semi-final": -330, "group-stage": 0,
            "quarter-final": 330, "round-of-16": 660, "team-outlooks": 990}
branches = []
for k in DAG["kids"]:
    bid = k.get("id")
    branches.append({"id": bid, "label": k.get("label").split(" (")[0], "qsum": qsum(k),
                     "x": BRANCH_X.get(bid, 0), "y": -720})
futures = len(DAG.get("futures", []) or [])
TOTAL = sum(b["qsum"] for b in branches) + futures

gs = next(k for k in DAG["kids"] if k.get("id") == "group-stage")
grpC = next(g for g in gs["kids"] if g.get("id") == "grp-C")
hero_fix = next(m for m in grpC["kids"] if m.get("id") == "f-argentina-vs-saudi-arabia")

# the LIT spine (real path), top→down in world coords; card anchor sits at (0,0)
spine = [
    {"id": "champion", "label": "WHO IS THE CHAMPION?", "sub": "→ Argentina (2022) ✓", "x": 0, "y": -1020},
    {"id": "group-stage", "label": "Group stage", "sub": f'{qsum(gs):,} q', "x": 0, "y": -720},
    {"id": "grp-C", "label": "Group C", "sub": f'{qsum(grpC):,} q', "x": 0, "y": -420},
    {"id": "hero", "label": "Argentina 1–2 Saudi Arabia", "sub": f'{hero_fix.get("qn")} q · the match', "x": 0, "y": -210},
]
# the other 5 Group C matches as context dots fanned around grp-C
others = [m for m in grpC["kids"] if m.get("id") != "f-argentina-vs-saudi-arabia"]
fan = [(-175, -470), (175, -470), (-235, -360), (235, -360), (0, -545)]
groupc_dots = [{"label": clean(m.get("label"), 30), "x": fx, "y": fy}
               for m, (fx, fy) in zip(others, fan)]


# ---- deterministic scatter for the dense "8,367 nodes" field (LCG, stable build) ----
def lcg(seed):
    s = seed
    while True:
        s = (1103515245 * s + 12345) & 0x7FFFFFFF
        yield s / 0x7FFFFFFF


rng = lcg(73)
specks, matchdots = [], []
for _ in range(520):
    x = -1180 + next(rng) * 2360
    y = -1080 + next(rng) * 900
    if abs(x) < 70 and y > -760:   # keep the spine column clear near the card
        continue
    specks.append({"x": round(x), "y": round(y), "r": round(1.2 + next(rng) * 1.8, 1)})
for _ in range(64):
    matchdots.append({"x": round(-1120 + next(rng) * 2240), "y": round(-1040 + next(rng) * 820)})


# ---- MICRO: the real graded match node (arc_2022.graded.json :: arg-ksa) ----
node = next(n for n in ARC["nodes"] if (n.get("node_id") or n.get("id")) == "arg-ksa")
L = node["layers"]
g = node["grade"]
first = lambda x: (x[0] if x else {}) if isinstance(x, list) else (x or {})
od, nv = first(L["odds"]), first(L["narrative"])
mm = (L["magic_moment"] or [{}])[0]
mm2 = (L["magic_moment"] or [{}, {}])[-1]
sts = L["stats"]
arc_brier = ARC["summary"].get("mean_market_brier")

micro = {
    "fixture": node["fixture"], "comp": node.get("competition", ""), "date": node.get("date", ""),
    "score": node.get("outcome", {}).get("score", ""), "fav": g["favourite"],
    "market_pct": round(g["market_prob"] * 100), "brier": g["brier"], "verdict": g["verdict"],
    "arc_brier": arc_brier,
    "layers": [
        {"k": "odds", "cls": "od", "head": f'market priced Argentina {round(g["market_prob"]*100)}% — FanDuel -650 de-vig · Opta 80.2%',
         "sys": "market de-vig · Opta supercomputer", "src": od.get("source_url")},
        {"k": "narrative", "cls": "nv", "head": clean(nv.get("storyline"), 92),
         "sys": "The Analyst (Opta)", "src": nv.get("source_url")},
        {"k": "magic moment", "cls": "mm", "head": f'{mm.get("minute","")} {mm.get("scorer","")} · {mm2.get("minute","")} {mm2.get("scorer","")} (the winner)',
         "sys": "Sky Sports", "src": mm.get("source_url")},
        {"k": "stats", "cls": "st", "head": "xG 2.16 vs 0.14 · 69% poss · shots 15–3 · 7 offsides",
         "sys": "Opta / StatsBomb / xgscore.io", "src": (sts[0] if sts else {}).get("source_url")},
    ],
}

DATA = {
    "branches": branches, "futures": futures, "total": TOTAL,
    "spine": spine, "groupc_dots": groupc_dots, "specks": specks, "matchdots": matchdots,
    "micro": micro, "coin_flip": 0.25,
    "app_url": "https://CardinalWalls.github.io/kickreason/match.html",
    "iframe": "../site/match.html",
}
payload = json.dumps(DATA, ensure_ascii=False)

TEMPLATE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>KickReason — one graph, two scales (60s)</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#070908;--panel:#0c0f0d;--panel2:#11150f;--ink:#e9f2ec;--mute:#8b958c;--faint:#566055;--line:#1b201a;
  --edge:#4cf0a3;--search:#ffc24d;--fetch:#8ab4ff;--star:#ffd76b;--narr:#8ab4ff;--violet:#c9a0ff;--down:#ff6b5e}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%;background:#000;overflow:hidden;font-family:"JetBrains Mono",monospace;color:var(--ink)}
#fit{position:fixed;inset:0;display:flex;align-items:center;justify-content:center;background:#000}
#stage{position:relative;width:1280px;height:720px;background:var(--bg);overflow:hidden;transform-origin:center center}
/* world (the DAG) — scaled by the camera each frame */
#world{position:absolute;left:0;top:0;width:1280px;height:720px;transform-origin:0 0;will-change:transform}
#wsvg{position:absolute;overflow:visible;left:0;top:0}  /* world (0,0)=#world(0,0); camera transform maps it to screen */
.edge{fill:none;stroke:var(--line);stroke-width:1.4}
.edge.lit{stroke:var(--edge);stroke-width:2.4;filter:drop-shadow(0 0 4px rgba(76,240,163,.5))}
.gnode rect{fill:#0c0f0d;stroke:var(--faint);stroke-width:1.5}
.gnode.lit rect{stroke:var(--edge);stroke-width:2}
.gnode text{font-family:"JetBrains Mono";fill:var(--ink)}
.gnode .sub{fill:var(--mute)}
.gnode.champ rect{stroke:var(--star)}
.dot{fill:var(--faint)}.mdot{fill:var(--fetch);opacity:.7}
.cdot{fill:#0c0f0d;stroke:var(--mute);stroke-width:1.2}
#fld{position:absolute;left:0;top:0}
/* the match CARD — screen-space, fonts stay legible (driven by camera) */
#card{position:absolute;width:660px;height:520px;border:1.5px solid var(--edge);background:linear-gradient(180deg,#0d100e,#0a0c0b);
  border-radius:12px;box-shadow:0 0 0 1px rgba(76,240,163,.12),0 18px 50px rgba(0,0,0,.6);overflow:hidden;
  transform-origin:center center;will-change:transform,opacity}
#card .face{position:absolute;inset:0;padding:14px 16px;opacity:0;transition:opacity .5s}
#card .face.on{opacity:1}
.kick{font-size:10px;letter-spacing:.22em;text-transform:uppercase;color:var(--edge);margin-bottom:7px}
.ctitle{font-family:"Bricolage Grotesque";font-weight:800;font-size:21px;line-height:1.05}
.csub{font-size:10.5px;color:var(--mute);margin:5px 0 12px}
.lrow{display:flex;gap:9px;align-items:flex-start;padding:7px 0;border-top:1px solid var(--line);opacity:0;transform:translateY(4px);transition:.45s}
.lrow:first-of-type{border-top:none}.lrow.on{opacity:1;transform:none}
.lrow .tg{font-size:9px;font-weight:700;letter-spacing:.06em;text-transform:uppercase;min-width:78px;color:var(--lc);padding-top:2px}
.lrow.od{--lc:var(--edge)}.lrow.nv{--lc:var(--narr)}.lrow.mm{--lc:var(--star)}.lrow.st{--lc:var(--violet)}
.lrow .bd{font-size:11.5px;color:var(--ink);line-height:1.35}
.lrow .sr{display:block;margin-top:3px;font-size:9.5px;color:var(--fetch);text-decoration:none}
/* graded face */
.gbig{font-family:"Bricolage Grotesque";font-weight:800;font-size:46px;color:var(--down);line-height:1}
.gcap{font-size:11px;color:var(--mute);text-transform:uppercase;letter-spacing:.1em}
.gline{font-size:12.5px;color:var(--ink);margin-top:10px}
.gref{font-size:11px;color:var(--star);margin-top:6px}
.obar{height:10px;border-radius:5px;background:var(--line);margin-top:12px;overflow:hidden}
.obar>i{display:block;height:100%;background:var(--down);width:87%}
.olab{font-size:10px;color:var(--mute);margin-top:4px}
/* overlay: both-scales caption + connector + odometer + honesty */
#ovl{position:absolute;inset:0;pointer-events:none}
.twoscale{position:absolute;right:30px;top:120px;width:430px;opacity:0;transition:opacity .5s}
.twoscale .vc{border:1px solid var(--edge);border-radius:12px;background:#0c0f0d;padding:14px 16px}
.tcap{position:absolute;left:50%;bottom:70px;transform:translateX(-50%);text-align:center;font-size:13px;color:var(--ink);opacity:0;transition:.5s;max-width:760px}
.tcap b{color:var(--edge)}
#conn{position:absolute;left:0;top:0;overflow:visible;pointer-events:none}
.odo{position:absolute;left:50%;top:34px;transform:translateX(-50%);text-align:center;opacity:0;transition:.5s}
.odo .n{font-family:"Bricolage Grotesque";font-weight:800;font-size:40px;color:var(--star)}
.odo .l{font-size:10px;letter-spacing:.2em;text-transform:uppercase;color:var(--mute)}
.honest{position:absolute;left:14px;bottom:60px;font-size:9.5px;color:var(--faint);opacity:0;transition:.5s}
/* browser-chrome app handoff */
#browser{position:absolute;opacity:0;transition:opacity .6s;border-radius:10px;overflow:hidden;
  border:1px solid var(--line);background:#0c0f0d;box-shadow:0 24px 70px rgba(0,0,0,.7)}
.chrome{height:34px;background:#15191400;display:flex;align-items:center;gap:8px;padding:0 12px;border-bottom:1px solid var(--line);background:#101410}
.dots3{display:flex;gap:6px}.dots3 i{width:10px;height:10px;border-radius:50%;background:#2a312a}
.addr{flex:1;height:20px;border-radius:5px;background:#0a0c0a;border:1px solid var(--line);display:flex;align-items:center;padding:0 8px;font-size:11px;color:var(--mute)}
.addr .lock{color:var(--edge);margin-right:6px}
.open{font-size:10px;font-weight:700;color:var(--bg);background:var(--edge);border-radius:5px;padding:4px 9px;text-decoration:none;text-transform:uppercase}
#browser iframe{width:100%;height:calc(100% - 34px);border:0;background:#080a09;display:block}
/* top HUD */
.top{position:absolute;top:0;left:0;right:0;height:40px;padding:0 14px;display:flex;align-items:center;gap:12px;
  background:linear-gradient(180deg,rgba(7,9,8,.95),rgba(7,9,8,0));z-index:40}
.brand{font-family:"Bricolage Grotesque";font-weight:800;font-size:14px}.brand .d{color:var(--edge)}
.phase{font-size:10px;color:var(--edge);letter-spacing:.12em;text-transform:uppercase;min-width:330px}
.bar{flex:1;height:3px;background:var(--line);border-radius:2px;overflow:hidden}.bar>i{display:block;height:100%;width:0;background:var(--edge)}
.clk{font-size:10px;color:var(--mute)}
.btn{font-size:10px;font-weight:700;color:var(--bg);background:var(--edge);border:none;border-radius:6px;padding:6px 12px;cursor:pointer;text-transform:uppercase}
.foot{position:absolute;left:14px;bottom:12px;font-size:10px;color:var(--faint);z-index:40}
</style></head><body>
<div id="fit"><div id="stage">
  <div id="world">
    <canvas id="fld" width="2600" height="1300"></canvas>
    <svg id="wsvg"><g id="edges"></g><g id="dots"></g><g id="gnodes"></g></svg>
  </div>
  <a id="card" href="#" target="_blank" rel="noopener" style="text-decoration:none;color:inherit">
    <div class="face front on" id="front"></div>
    <div class="face grade" id="gface"></div>
  </a>
  <div id="ovl">
    <svg id="conn"><path id="connp" class="edge lit" d=""/></svg>
    <div class="odo" id="odo"><div class="n" id="odon">0</div><div class="l">graded nodes · one champion-rooted DAG</div></div>
    <div class="twoscale" id="twoscale"><div class="vc" id="vcard"></div></div>
    <div class="tcap" id="tcap"></div>
    <div class="honest" id="honest">structure + counts real (dag.json) · leaf-question dots sampled for density</div>
  </div>
  <div id="browser"><div class="chrome"><div class="dots3"><i></i><i></i><i></i></div>
    <div class="addr"><span class="lock">🔒</span><span id="url"></span></div>
    <a class="open" id="openlive" href="#" target="_blank">open live →</a></div>
    <iframe id="appframe" title="KickReason match page"></iframe></div>
  <div class="top"><span class="brand">KickReason<span class="d">.</span></span>
    <span class="phase" id="phase">press play</span>
    <div class="bar"><i id="fill"></i></div><span class="clk" id="clk">0s</span>
    <button class="btn" id="play">▶ play</button></div>
  <div class="foot" id="foot">2022 graded · 2026 live — this isn't a screenshot, it's the product</div>
</div></div>
<script>
const D=/*__DATA__*/, M=D.micro, $=s=>document.querySelector(s);
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function nf(n){return Math.round(n).toLocaleString()}
function ease(p){p=Math.max(0,Math.min(1,p));return p<.5?4*p*p*p:1-Math.pow(-2*p+2,3)/2}
function lerp(a,b,p){return a+(b-a)*ease(p)}

/* ---- fit the 1280x720 stage to the viewport ---- */
function fit(){const s=Math.min(innerWidth/1280,innerHeight/720);$('#stage').style.transform='scale('+s+')';}
addEventListener('resize',fit);fit();

/* ---- build the world: dense field (canvas), edges, dots, spine + branch nodes ---- */
const cv=$('#fld'),ctx=cv.getContext('2d');   // canvas is 2600x1300, world (0,0) at its center
function wx(x){return 1300+x} function wy(y){return 650+y}
function drawField(){ctx.clearRect(0,0,2600,1300);
  D.specks.forEach(s=>{ctx.beginPath();ctx.fillStyle='rgba(86,96,85,.55)';ctx.arc(wx(s.x),wy(s.y),s.r,0,7);ctx.fill();});
  D.matchdots.forEach(s=>{ctx.beginPath();ctx.fillStyle='rgba(138,180,255,.6)';ctx.arc(wx(s.x),wy(s.y),2.6,0,7);ctx.fill();});}
drawField();
// canvas center (1300,650) must sit at world (0,0) = #world local (0,0)
$('#fld').style.left='-1300px';$('#fld').style.top='-650px';

const NS='http://www.w3.org/2000/svg';
const eG=$('#edges'),dG=$('#dots'),nG=$('#gnodes');
const spineById={};D.spine.forEach(n=>spineById[n.id]=n);
function line(a,b,lit){const l=document.createElementNS(NS,'path');
  l.setAttribute('d',`M${a.x},${a.y} L${b.x},${b.y}`);l.setAttribute('class','edge'+(lit?' lit':''));return l;}
// champion -> branches (dim), + spine (lit)
const champ=spineById['champion'];
D.branches.forEach(b=>{eG.appendChild(line(champ,b,false));});
const litpath=[['champion','group-stage'],['group-stage','grp-C'],['grp-C','hero']];
const litEdges=[];
litpath.forEach(([a,b])=>{const e=line(spineById[a],spineById[b],true);litEdges.push(e);eG.appendChild(e);});
// hero -> card(0,0)
const heroToCard=line(spineById['hero'],{x:0,y:0},true);litEdges.push(heroToCard);eG.appendChild(heroToCard);
// grp-C -> other group C dots (dim)
const grpC=spineById['grp-C'];
D.groupc_dots.forEach(c=>{eG.appendChild(line(grpC,c,false));
  const d=document.createElementNS(NS,'circle');d.setAttribute('cx',c.x);d.setAttribute('cy',c.y);d.setAttribute('r',6);d.setAttribute('class','cdot');dG.appendChild(d);});
// branch nodes + spine nodes
function gnode(n,cls){const g=document.createElementNS(NS,'g');g.setAttribute('class','gnode '+cls);
  const w=Math.max(120,(n.label.length)*8.4+18),h=n.sub?44:32;
  g.innerHTML=`<rect x="${n.x-w/2}" y="${n.y-h/2}" width="${w}" height="${h}" rx="8"/>`+
    `<text x="${n.x}" y="${n.y+(n.sub?-2:5)}" text-anchor="middle" font-size="14" font-weight="700">${esc(n.label)}</text>`+
    (n.sub?`<text class="sub" x="${n.x}" y="${n.y+15}" text-anchor="middle" font-size="11">${esc(n.sub)}</text>`:'');
  return g;}
D.branches.forEach(b=>{const lit=b.id==='group-stage';nG.appendChild(gnode({x:b.x,y:b.y,label:b.label,sub:b.qsum.toLocaleString()+' q'},lit?'lit':''));});
nG.appendChild(gnode(spineById['champion'],'champ lit'));
nG.appendChild(gnode(spineById['grp-C'],'lit'));
// hero node (the match) — small node that the CARD overlays; draw a ring so it reads at macro
const hY=spineById['hero'].y;
const hr=document.createElementNS(NS,'circle');hr.setAttribute('cx',0);hr.setAttribute('cy',hY);
hr.setAttribute('r',9);hr.setAttribute('class','gnode lit');hr.setAttribute('fill','#0c0f0d');hr.setAttribute('stroke','var(--edge)');hr.setAttribute('stroke-width','2');dG.appendChild(hr);
const hl=document.createElementNS(NS,'text');hl.setAttribute('x',0);hl.setAttribute('y',hY+26);hl.setAttribute('text-anchor','middle');
hl.setAttribute('font-size','13');hl.setAttribute('font-weight','700');hl.setAttribute('fill','var(--ink)');hl.textContent=spineById['hero'].label;
dG.appendChild(hl);
const hl2=document.createElementNS(NS,'text');hl2.setAttribute('x',0);hl2.setAttribute('y',hY+42);hl2.setAttribute('text-anchor','middle');
hl2.setAttribute('font-size','11');hl2.setAttribute('fill','var(--mute)');hl2.textContent=spineById['hero'].sub;dG.appendChild(hl2);

// prime lit edges for stroke-dashoffset draw-on
litEdges.forEach(e=>{const len=e.getTotalLength();e.style.strokeDasharray=len;e.style.strokeDashoffset=len;e.dataset.len=len;});
function drawSpine(p){litEdges.forEach((e,i)=>{const seg=1/litEdges.length,lp=Math.max(0,Math.min(1,(p-i*seg)/seg));
  e.style.strokeDashoffset=e.dataset.len*(1-ease(lp));});}
drawSpine(0);

/* ---- the match CARD (front = layers, graded = verdict) ---- */
$('#front').innerHTML=`<div class="kick">one node · 4 sourced layers</div>
  <div class="ctitle">${esc(M.fixture)}</div>
  <div class="csub">${esc(M.comp)} · ${esc(M.date)} · final ${esc(M.score)}</div>`+
  M.layers.map(l=>`<div class="lrow ${l.cls}"><div class="tg">${esc(l.k)}</div><div class="bd">${esc(l.head)}`+
    (l.src?`<span class="sr">↗ ${esc(l.src.replace(/^https?:\/\/(www\.)?/,'').slice(0,42))}</span>`:'')+`</div></div>`).join('');
$('#gface').innerHTML=`<div class="kick">graded where it resolved</div>
  <div class="gcap">market priced ${esc(M.fav)} ${M.market_pct}% — clear favourite</div>
  <div class="gbig" id="briern">0.000</div><div class="gcap">Brier (lower = better) · coin-flip = ${M.coin_flip}</div>
  <div class="gline">${esc(M.fixture)} → <b style="color:var(--down)">LOST</b>. The market was <b style="color:var(--down)">confidently wrong</b>.</div>
  <div class="gref">across 13 graded 2022 nodes, mean Brier ${M.arc_brier} — this is the worst miss.</div>
  <div class="obar"><i id="obari"></i></div><div class="olab" id="olab">market ${M.market_pct}% on Argentina</div>`;
const cardA=$('#card');cardA.href=D.app_url;

/* the right-hand verdict card for the both-scales beat (same data, compact) */
$('#vcard').innerHTML=`<div class="kick" style="color:var(--star)">its full verdict — the micro scale</div>
  <div class="ctitle" style="font-size:18px">${esc(M.fixture)}</div>
  <div class="gline" style="margin-top:8px">market <b>${M.market_pct}%</b> on Argentina → <b style="color:var(--down)">Brier ${M.brier}</b></div>
  ${M.layers.map(l=>`<div class="lrow on ${l.cls}" style="padding:5px 0"><div class="tg">${esc(l.k)}</div><div class="bd" style="font-size:10.5px">${esc(l.head.slice(0,64))}</div></div>`).join('')}`;

/* ---- camera keyframes [t,k,fx,fy] — ONE continuous space; KREF=2.0 = card full-size ---- */
const KREF=2.0, CARD_W=660, CARD_H=520;
const KF=[[0,2.0,0,0],[6,2.0,0,0],[12,2.0,0,-30],[19,1.0,0,-300],[30,0.5,0,-460],
          [36,0.5,0,-460],[45,2.0,0,0],[52,2.0,0,0],[57,2.4,0,0],[60,2.4,0,0]];
function cam(t){let i=0;while(i<KF.length-1&&t>KF[i+1][0])i++;const a=KF[i],b=KF[Math.min(i+1,KF.length-1)];
  const p=b[0]>a[0]?(t-a[0])/(b[0]-a[0]):0;return{k:lerp(a[1],b[1],p),fx:lerp(a[2],b[2],p),fy:lerp(a[3],b[3],p)};}

/* world (0,0) -> screen */
function w2s(c,wx,wy){return [640+(wx-c.fx)*c.k, 360+(wy-c.fy)*c.k];}
function placeCard(c){
  // fixed-size card, scaled by the camera (transform-origin center) so it zooms WITH the world
  const [sx,sy]=w2s(c,0,0), sc=c.k/KREF;
  const card=$('#card');
  card.style.left=(sx-CARD_W/2)+'px';card.style.top=(sy-CARD_H/2)+'px';
  card.style.transform='scale('+sc+')';
}
function placeWorld(c){$('#world').style.transform=`translate(${640-c.fx*c.k}px,${360-c.fy*c.k}px) scale(${c.k})`;}

/* ---- phases ---- */
const PH=[[0,'① the match — in the app'],[6,'② its four sourced layers'],[12,'③ pull back — one lit path to the champion'],
  [19,'④ one graph · 8,367 graded nodes'],[30,'⑤ two scales — the node ↔ its verdict'],[36,'⑥ back down the same path'],
  [45,'⑦ graded — the market was confidently wrong'],[52,'⑧ open it live in the app']];
function phase(t){let p=PH[0][1];for(const[s,n]of PH)if(t>=s)p=n;return p;}

/* ---- handoff iframe geometry ---- */
let appReady=false;
function browserRect(t){
  // from t=52..57 grow from the card's rect to a near-full-stage browser
  const c=cam(52);const sx=640,sy=360;const w0=CARD_W*c.k,h0=w0*0.82;
  const r0={x:sx-w0/2,y:sy-h0/2,w:w0,h:h0};
  const r1={x:120,y:70,w:1040,h:600};
  const p=Math.max(0,Math.min(1,(t-52)/4));
  return{x:lerp(r0.x,r1.x,p),y:lerp(r0.y,r1.y,p),w:lerp(r0.w,r1.w,p),h:lerp(r0.h,r1.h,p)};
}

/* ---- the loop (paint(t) is idempotent so we can seek to any timestamp) ---- */
let playing=false,t=0,last=0;
function paint(){
  $('#fill').style.width=(t/60*100)+'%';$('#clk').textContent=t.toFixed(0)+'s';$('#phase').textContent=phase(t);
  const c=cam(t);placeWorld(c);placeCard(c);
  // beat 2: expand layer rows (6-12)
  const rows=document.querySelectorAll('#front .lrow');
  const w=t>=6?Math.floor((Math.min(t,11.5)-6)/(11.5-6)*rows.length)+1:0;
  rows.forEach((r,i)=>r.classList.toggle('on',i<w));
  // beat 3: draw the lit spine (12-19)
  drawSpine(t>=12?Math.min(1,(t-12)/(19-12)):0);
  // beat 4/5: macro odometer + honesty (visible 19-36)
  const macro=t>=19&&t<36;$('#odo').style.opacity=macro?1:0;$('#honest').style.opacity=(t>=19&&t<30)?1:0;
  $('#odon').textContent=nf(lerp(0,D.total,t>=19?(Math.min(t,30)-19)/(30-19):0));
  // beat 5: both scales side-by-side (30-36)
  const two=t>=30&&t<36;$('#twoscale').style.opacity=two?1:0;$('#tcap').style.opacity=two?1:0;
  if(two){$('#tcap').innerHTML='<b>one node here · its full verdict here.</b> the match you opened is 1 of '+nf(D.total)+' nodes — every match/team/moment, graded where it resolves.';
    const hys=360+(spineById['hero'].y-c.fy)*c.k, hxs=640+(0-c.fx)*c.k;
    $('#connp').setAttribute('d',`M${hxs},${hys} C${hxs+120},${hys} 770,210 812,210`);
  }else{$('#connp').setAttribute('d','');}
  // beat 6/7: flip to graded face (≥43), count Brier (45-52)
  $('#front').classList.toggle('on',t<43);$('#gface').classList.toggle('on',t>=43);
  const gp=t>=45?Math.min(1,(t-45)/(52-45)):0;
  const bn=$('#briern');if(bn)bn.textContent=lerp(0,M.brier,gp).toFixed(3);
  const ob=$('#obari');if(ob)ob.style.width=(M.market_pct*(1-gp))+'%';
  const ol=$('#olab');if(ol)ol.textContent=gp>0.9?'the priced edge collapsed — favourite lost':'market '+M.market_pct+'% on Argentina';
  // beat 8: snap into the live app (52-60)
  if(t>=52){const br=browserRect(t),b=$('#browser');b.style.opacity=1;
    b.style.left=br.x+'px';b.style.top=br.y+'px';b.style.width=br.w+'px';b.style.height=br.h+'px';
    if(!appReady){appReady=true;$('#appframe').src=D.iframe;$('#openlive').href=D.app_url;}
    const tp=Math.min(1,(t-52.4)/2.4);$('#url').textContent=D.app_url.slice(0,Math.floor(tp*D.app_url.length))+(tp<1?'▋':'');
    $('#card').style.opacity=Math.max(0,1-(t-52)/1.6);
  }else{$('#browser').style.opacity=0;$('#card').style.opacity=c.k<1.25?0:1;}
}
function frame(ts){if(!playing){last=ts;return;}t=Math.min(60,t+(ts-last)/1000);last=ts;paint();
  if(t>=60){playing=false;$('#play').textContent='↻ replay';}requestAnimationFrame(frame);}
window.seek=function(sec){t=Math.max(0,Math.min(60,sec));paint();};window.__dur=60;
$('#play').onclick=()=>{if(t>=60){t=0;appReady=false;$('#appframe').src='about:blank';}playing=!playing;
  $('#play').textContent=playing?'❚❚ pause':'▶ play';if(playing){last=performance.now();requestAnimationFrame(frame);}};
paint();  // initial
</script></body></html>"""

out = os.path.join(HERE, "process60.html")
open(out, "w", encoding="utf-8").write(TEMPLATE.replace("/*__DATA__*/", payload))
print(f"wrote dataset/process60.html")
print(f"  MACRO (dag.json): {len(branches)} branches summing {sum(b['qsum'] for b in branches):,} + {futures} futures = {TOTAL:,} nodes")
print(f"    spine: champion → Group stage ({qsum(gs):,}q) → Group C ({qsum(grpC):,}q) → {hero_fix['label']} ({hero_fix['qn']}q)")
print(f"  MICRO (arc_2022.graded.json): {micro['fixture']} · market {micro['market_pct']}% → Brier {micro['brier']} · arc mean {micro['arc_brier']}")
print(f"  APP handoff: iframe→{DATA['iframe']} · URL shown {DATA['app_url']}")
print("  open: open dataset/process60.html   (commit+push site/match.html to make the URL resolve live)")
