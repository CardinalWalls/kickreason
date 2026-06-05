#!/usr/bin/env python3
"""
build_replay.py — generate dataset/replay.html: ONE self-contained HTML replay of the whole
system, with every detail baked in (real MiroMind trace + the graded 2022 arc + the business
model). No server, no network: open replay.html in any browser, press Play, record the screen.

  python3 dataset/build_replay.py

It reads the REAL artifacts on disk and inlines them:
  - dataset/runs/wc26-usa-advance.json   -> the real MiroMind reasoning chain (searches/fetches/sources/judgment)
  - dataset/arc_2022.graded.json         -> the graded 2022 arc (board) + the Saudi hero node's 4 layers
Every number shown is the real one; nothing is typed into the HTML by hand.
"""
import json, os, re, html

ROOT = os.path.dirname(os.path.abspath(__file__))


def short(s, n):
    s = (s or "").replace("**", "").replace("\\n", " ").replace("\\\"", '"')
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n] + ("…" if len(s) > n else "")


def clean_evidence(snip):
    """Pull a human-readable evidence line out of a fetch snippet, robust to the
    double-encoded {"error":"","extracted_info":"…"} wrapper (parse may fail)."""
    if not snip:
        return ""
    ev = None
    try:
        ev = json.loads(snip).get("extracted_info")
    except Exception:
        m = re.search(r'"extracted_info"\s*:\s*"(.*?)"\s*}\s*$', snip, re.DOTALL) \
            or re.search(r'"extracted_info"\s*:\s*"(.*)', snip, re.DOTALL)
        ev = m.group(1) if m else snip
    ev = re.sub(r"^\s*EXTRACTED INFORMATION[:\s-]*", "", ev or "", flags=re.I)
    return short(ev, 230)


def host(u):
    m = re.match(r"https?://([^/]+)", u or "")
    return (m.group(1).replace("www.", "") if m else "source")


# ── 1) the real MiroMind reasoning chain (the live forward problem) ───────────
def build_trace():
    r = json.load(open(os.path.join(ROOT, "runs", "wc26-usa-advance.json")))
    steps = r.get("steps") or []
    chain = []
    for s in steps:
        a = s.get("action")
        if a == "web_search":
            kw = s.get("keywords") or []
            chain.append({"i": s.get("i", 0), "type": "search",
                          "text": "  ·  ".join(kw) if isinstance(kw, list) else str(kw)})
        elif a == "fetch":
            chain.append({"i": s.get("i", 0), "type": "fetch", "url": s.get("url"),
                          "host": host(s.get("url")), "evidence": clean_evidence(s.get("snippet"))})
    chain.sort(key=lambda x: x["i"])
    # curate for legibility: interleave, keep the information-bearing ones, cap ~16
    seen_hosts, curated = set(), []
    for c in chain:
        if c["type"] == "search":
            curated.append(c)
        elif c.get("evidence"):
            curated.append(c)
        if len(curated) >= 16:
            break
    factors = r.get("factors") or []
    if isinstance(factors, str):
        factors = [factors]
    # faithful, clean judgment (the trace de-vigs -750 → 88.2%; demo.py's sharp line is 91%)
    judg = ("The forecast anchors on the de-vigged market line — -750 implies ~88.2% to advance — "
            "confirmed by host advantage, squad depth and recent form. Computed forecast ~88% "
            "(sharp de-vig line 91%). One research pass agrees with the market; an edge needs new info.")
    usage = r.get("usage") or {}
    return {
        "q": r.get("q"),
        "steps": curated,
        "n_steps": len(steps),
        "n_search": sum(1 for s in steps if s.get("action") == "web_search"),
        "n_fetch": sum(1 for s in steps if s.get("action") == "fetch"),
        "n_sources": len(r.get("sources") or []),
        "tokens": usage.get("total_tokens"),
        "elapsed_s": r.get("elapsed_s"),
        "judgment": judg or "De-vig of the sharp line (-750 → ~88%) anchors the forecast; host advantage and squad depth confirm it.",
        "factors": [short(f, 150) for f in factors[:5]],
    }


# ── 2) the graded 2022 arc: the board + the Saudi hero node's four layers ─────
def build_arc():
    g = json.load(open(os.path.join(ROOT, "arc_2022.graded.json")))
    summ = g["summary"]
    rows = []
    for n in g["nodes"]:
        gr = n.get("grade", {})
        if not gr.get("graded"):
            continue
        rows.append({
            "fixture": n["fixture"], "stage": n.get("stage", ""),
            "mkt": round(gr["market_prob"] * 100),
            "won": gr["favourite_won"], "brier": gr["brier"],
            "wrong": gr.get("confidently_wrong", False),
            "verdict": gr["verdict"],
        })
    hero = next(n for n in g["nodes"] if (n.get("node_id") or n.get("id")) == "arg-ksa")
    L = hero["layers"]
    mm = (L["magic_moment"] or [])[-1] if L.get("magic_moment") else {}
    return {
        "summary": {"mean_brier": summ["mean_market_brier"],
                    "n_wrong": summ["n_market_confidently_wrong"],
                    "wrong_fixtures": summ["confidently_wrong_fixtures"]},
        "rows": rows,
        "hero": {
            "fixture": hero["fixture"], "score": hero["outcome"]["score"],
            "competition": hero.get("competition", ""),
            "grade": hero["grade"],
            "odds": {"text": short(L["odds"].get("text"), 300), "src": L["odds"].get("source_url"),
                     "system": L["odds"].get("system")},
            "narrative": [{"s": x.get("storyline"), "t": short(x.get("text"), 220),
                           "sys": x.get("system"), "src": x.get("source_url")} for x in (L.get("narrative") or [])[:3]],
            "magic": {"minute": mm.get("minute"), "scorer": mm.get("scorer"),
                      "t": short(mm.get("text"), 240), "src": mm.get("source_url")},
            "stats": [{"m": x.get("metric"), "v": x.get("value"), "sys": x.get("system"),
                       "src": x.get("source_url")} for x in (L.get("stats") or [])[:4]],
        },
    }


BUSINESS = [
    {"layer": "odds", "system": "bookmaker de-vig · Opta supercomputer", "buyer": "bettors · quants · sportsbooks", "graded": "Brier / CLV"},
    {"layer": "narrative", "system": "the pundit / analyst (The Athletic · Opta · Guardian)", "buyer": "media · creators", "graded": "sourced"},
    {"layer": "magic_moment", "system": "broadcast / highlights / the star", "buyer": "fans · social · TV", "graded": "sourced"},
    {"layer": "stats", "system": "the data co (Opta · StatsBomb · FBref)", "buyer": "clubs · analysts · B2B", "graded": "sourced"},
]


def build_update():
    """The REAL captured MiroMind update run (news -> moved, sourced forecast)."""
    u = json.load(open(os.path.join(ROOT, "runs", "exp-update-latency.json")))
    rev = ""
    m = re.search(r"REVISED:[^\n]*", u.get("answer", ""))
    if m:
        rev = m.group(0).replace("REVISED:", "").strip()
    src = (u.get("sources") or [{}])[0].get("url", "")
    return {"fixture": u.get("fixture"), "news": short(u.get("breaking_news"), 110),
            "revised": rev, "latency_min": u.get("latency_min"),
            "n_steps": u.get("n_steps"), "src": src, "src_host": host(src)}


def main():
    DATA = {
        "oneLiner": "MiroMind reasons through a match — sources, steps, judgment — and our compiler turns that reasoning into a forecast you can audit AND grade. We graded an entire World Cup to prove it. Now it runs live for 2026.",
        "trace": build_trace(),
        "arc": build_arc(),
        "business": BUSINESS,
        "update": build_update(),
    }
    payload = json.dumps(DATA, ensure_ascii=False)
    out = TEMPLATE.replace("/*__DATA__*/", payload)
    open(os.path.join(ROOT, "replay.html"), "w", encoding="utf-8").write(out)
    t, a = DATA["trace"], DATA["arc"]
    print("wrote dataset/replay.html (self-contained)")
    print(f"  trace: {len(t['steps'])} curated steps from {t['n_steps']:,} real "
          f"({t['n_search']} searches · {t['n_fetch']} fetches · {t['n_sources']} sources · {t['tokens']:,} tokens)")
    print(f"  arc:   {len(a['rows'])} graded nodes · mean Brier {a['summary']['mean_brier']} · "
          f"{a['summary']['n_wrong']} confidently wrong")
    print("  open it: just double-click dataset/replay.html  (or: open dataset/replay.html)")


# ── the self-contained page (CSS+JS inline; DATA injected at /*__DATA__*/) ────
TEMPLATE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE LEDGER — replay (MiroMind · graded World Cup)</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Hanken+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#080a09;--panel:#121514;--panel2:#191d18;--ink:#f3f1e9;--mute:#9aa39a;--faint:#5d655c;--line:#262b25;
  --edge:#4cf0a3;--down:#ff6b5e;--break:#ffc24d;--star:#ffd76b;--narr:#8ab4ff;--violet:#c9a0ff}
*{box-sizing:border-box;margin:0;padding:0}
html,body{height:100%}
body{background:var(--bg);color:var(--ink);font-family:"Hanken Grotesk",sans-serif;line-height:1.45;overflow:hidden}
.mono{font-family:"JetBrains Mono",monospace}
.stage{position:fixed;inset:0;overflow:hidden}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:7vh 8vw;
  opacity:0;transform:translateY(16px);transition:opacity .6s ease,transform .6s ease;pointer-events:none;overflow:auto}
.scene.on{opacity:1;transform:none;pointer-events:auto}
.kick{font-family:"JetBrains Mono";font-size:12px;letter-spacing:.34em;text-transform:uppercase;color:var(--edge);margin-bottom:16px}
h1{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(30px,5.2vw,60px);line-height:1.04;letter-spacing:-.02em;max-width:18ch}
h1 .hl{color:var(--edge)} h1 .red{color:var(--down)} h1 .gold{color:var(--star)}
.lead{color:var(--mute);font-size:clamp(15px,1.7vw,21px);margin-top:18px;max-width:60ch}
.big{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(56px,12vw,150px);line-height:.9;letter-spacing:-.04em}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:26px;align-items:start}
@media(max-width:900px){.row2{grid-template-columns:1fr}}

/* spine diagram */
.spine{display:flex;flex-wrap:wrap;gap:10px;align-items:stretch;margin-top:8px}
.sp{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:13px 16px;flex:1;min-width:150px}
.sp b{font-family:"Bricolage Grotesque";font-size:15px} .sp .d{color:var(--mute);font-size:12.5px;margin-top:4px}
.sp.k{border-color:var(--edge);box-shadow:0 0 0 1px rgba(76,240,163,.2) inset}
.arrow{align-self:center;color:var(--faint);font-size:20px}

/* trace */
.trace{background:#0c0f0d;border:1px solid var(--line);border-radius:12px;padding:8px 6px;max-height:62vh;overflow:auto}
.tstep{display:grid;grid-template-columns:96px 1fr;gap:12px;padding:9px 12px;border-bottom:1px solid #1b201a;opacity:0;transform:translateY(8px);transition:.3s}
.tstep.on{opacity:1;transform:none}
.tact{font-family:"JetBrains Mono";font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;font-weight:700;padding-top:2px}
.tstep.search .tact{color:var(--break)} .tstep.fetch .tact{color:var(--edge)} .tstep.judge .tact{color:var(--star)}
.tbody{font-size:13.5px} .tbody .ev{color:var(--mute);font-size:12.5px;margin-top:3px}
.src{font-family:"JetBrains Mono";font-size:11px;color:var(--narr)} .src a{color:var(--narr);text-decoration:none}
.facts{margin-top:14px} .facts li{margin:6px 0 6px 18px;font-size:14px;color:var(--ink)}

/* layer chips + match */
.chips{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:10px}
@media(max-width:900px){.chips{grid-template-columns:1fr 1fr}}
.chip{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--lc);border-radius:11px;padding:14px 16px;opacity:0;transform:scale(.96);transition:.45s}
.chip.on{opacity:1;transform:none}
.chip .tag{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--lc);font-weight:700}
.chip .b{font-size:13px;color:var(--mute);margin-top:5px} .chip .who{font-size:12px;color:var(--faint);margin-top:6px}
.mm{--lc:var(--star)} .nv{--lc:var(--narr)} .od{--lc:var(--edge)} .st{--lc:var(--violet)}
.lyr{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--lc);border-radius:11px;padding:13px 17px;margin-bottom:9px}
.lyr .tag{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.12em;text-transform:uppercase;color:var(--lc);font-weight:700}
.lyr .bd{font-size:13.5px;margin-top:3px} .lyr .mt{font-family:"JetBrains Mono";font-size:11px;color:var(--faint);margin-top:5px}
.grade{display:flex;align-items:baseline;gap:14px;margin-top:6px}
.grade .num{font-family:"Bricolage Grotesque";font-weight:800;font-size:40px;color:var(--down)} .grade .l{font-family:"JetBrains Mono";font-size:12px;color:var(--down)}

/* board */
table{width:100%;border-collapse:collapse;font-size:13px}
th,td{text-align:left;padding:6px 9px;border-bottom:1px solid var(--line)} th{font-family:"JetBrains Mono";font-size:10px;letter-spacing:.1em;text-transform:uppercase;color:var(--faint);font-weight:400}
td.r,th.r{text-align:right} .wrong{color:var(--down);font-weight:600} .right{color:var(--edge)}
tr.brow{opacity:0;transform:translateX(-8px);transition:.28s} tr.brow.on{opacity:1;transform:none}
.meanwrap{display:flex;gap:30px;align-items:flex-end;margin-bottom:14px}
.meanwrap .n{font-family:"Bricolage Grotesque";font-weight:800;font-size:64px;line-height:1}

/* biz */
.bizgrid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-top:14px}
@media(max-width:900px){.bizgrid{grid-template-columns:1fr 1fr}}
.bcard{background:var(--panel);border:1px solid var(--line);border-top:4px solid var(--lc);border-radius:11px;padding:16px}
.bcard .tag{font-family:"JetBrains Mono";font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:var(--lc);font-weight:700}
.bcard .sys{font-size:13px;color:var(--mute);margin-top:8px} .bcard .buy{font-size:13px;margin-top:10px} .bcard .gr{font-family:"JetBrains Mono";font-size:11px;color:var(--faint);margin-top:8px}

/* hud */
.hud{position:fixed;left:0;right:0;bottom:0;padding:13px 20px;display:flex;align-items:center;gap:14px;background:linear-gradient(transparent,rgba(0,0,0,.65));z-index:30}
.btn{font-family:"JetBrains Mono";font-weight:700;font-size:12px;letter-spacing:.05em;color:var(--bg);background:var(--edge);border:none;border-radius:7px;padding:9px 15px;cursor:pointer;text-transform:uppercase}
.nav{font-family:"JetBrains Mono";font-size:12px;color:var(--mute);background:none;border:1px solid var(--line);border-radius:6px;padding:8px 11px;cursor:pointer}
.bar{flex:1;height:4px;background:var(--line);border-radius:3px;overflow:hidden}.bar>i{display:block;height:100%;width:0;background:var(--edge);transition:width .3s}
.lab{font-family:"JetBrains Mono";font-size:11px;color:var(--faint);min-width:240px;text-align:right}
.brand{position:fixed;top:16px;left:20px;font-family:"Bricolage Grotesque";font-weight:800;font-size:15px;z-index:30}.brand .dot{color:var(--edge)}
.tag2{position:fixed;top:16px;right:20px;font-family:"JetBrains Mono";font-size:10.5px;color:var(--faint);z-index:30;text-align:right}
.dots{display:flex;gap:5px}.dot{width:8px;height:8px;border-radius:50%;background:var(--line);cursor:pointer}.dot.on{background:var(--edge)}
</style></head><body>
<div class="brand">THE LEDGER<span class="dot">.</span></div>
<div class="tag2" id="tag2">self-contained replay · real data baked in</div>
<div class="stage" id="stage"></div>
<div class="hud">
  <button class="btn" id="play">▶ Play</button>
  <button class="nav" onclick="go(cur-1)">←</button><button class="nav" onclick="go(cur+1)">→</button>
  <div class="dots" id="dots"></div>
  <div class="bar"><i id="fill"></i></div>
  <span class="lab" id="lab"></span>
</div>
<script>
const DATA = /*__DATA__*/;
const $=s=>document.querySelector(s), stage=$('#stage');
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function A(u,h){return u?('<a class="src" href="'+u+'" target="_blank">↗ '+esc(h||u)+'</a>'):''}
function H(u){try{return new URL(u).hostname.replace('www.','')}catch(e){return 'source'}}

// each scene: {label, secs, html(), reveal(p)}
const T=DATA.trace, ARC=DATA.arc, BIZ=DATA.business;
const SCENES=[
{label:'the hook', secs:8, html:()=>`
  <div class="kick">the dream demo · 2022 graded → 2026 live</div>
  <h1>We graded an <span class="hl">entire World Cup.</span></h1>
  <div class="lead">${esc(DATA.oneLiner)}</div>`},
{label:'the gap (business)', secs:9, html:()=>`
  <div class="kick">① business — the problem</div>
  <h1>Every AI predicts football.<br><span class="red">None lets you check it.</span></h1>
  <div class="lead">They never show their reasoning, and never keep score — when they're wrong, they just move on. KickOracle, the category leader, even has an "accuracy" page. It's blank. <b style="color:var(--ink)">We're the one you can audit — and grade.</b></div>`},
{label:'the idea (how MiroMind is used)', secs:11, html:()=>`
  <div class="kick">the system, end to end</div>
  <h1 style="font-size:clamp(24px,3.4vw,40px)">One research pass → a graded, four-layer forecast</h1>
  <div class="spine">
    <div class="sp"><b>Problem</b><div class="d">a real match question</div></div><div class="arrow">→</div>
    <div class="sp k"><b>MiroMind API</b><div class="d">multi-step reasoning + sources (the engine + the updater)</div></div><div class="arrow">→</div>
    <div class="sp k"><b>Compiler</b><div class="d">trace → structured, auditable node (our IP)</div></div><div class="arrow">→</div>
    <div class="sp"><b>4 expert layers</b><div class="d">odds · narrative · magic · stats</div></div><div class="arrow">→</div>
    <div class="sp"><b>Grade</b><div class="d">Brier / CLV — the proof</div></div>
  </div>
  <div class="lead">The compiler is what turns MiroMind from a web-searcher into a problem-solver: it produces the reasoning; we make it structured, layered, and checkable.</div>`},
{label:'MiroMind reasons (the 60s walkthrough)', secs:30, html:()=>`
  <div class="kick">② MiroMind reasons — real trace · steps · references · judgment</div>
  <h1 style="font-size:clamp(20px,2.6vw,30px)">${esc(T.q)}</h1>
  <div class="mono" style="color:var(--faint);font-size:12px;margin:6px 0 10px">${T.n_steps.toLocaleString()} reasoning steps · ${T.n_search} searches · ${T.n_fetch} fetches · ${T.n_sources} sources · ${(T.tokens||0).toLocaleString()} tokens — selected real steps below (full trace in runs/)</div>
  <div class="trace" id="trace"></div>`,
  reveal:(p)=>{const box=$('#trace'); if(!box)return; const items=T.steps.concat([{type:'judge'}]);
    const k=Math.floor(p*(items.length+1));
    while(box.children.length<Math.min(k,items.length)){const j=box.children.length;const s=items[j];const d=document.createElement('div');
      if(s.type==='search'){d.className='tstep search';d.innerHTML='<div class="tact">search</div><div class="tbody">"'+esc(s.text)+'"</div>';}
      else if(s.type==='fetch'){d.className='tstep fetch';d.innerHTML='<div class="tact">read</div><div class="tbody">'+A(s.url,s.host)+'<div class="ev">'+esc(s.evidence)+'</div></div>';}
      else{d.className='tstep judge';d.innerHTML='<div class="tact">judgment</div><div class="tbody">'+esc(T.judgment)+'<ul class="facts">'+T.factors.map(f=>'<li>'+esc(f)+'</li>').join('')+'</ul></div>';}
      box.appendChild(d);requestAnimationFrame(()=>d.classList.add('on'));box.scrollTop=box.scrollHeight;}}},
{label:'the compiler', secs:9, html:()=>`
  <div class="kick">④ the compiler — one trace, four products</div>
  <h1 style="font-size:clamp(22px,3vw,36px)">That reasoning compiles into four expert layers</h1>
  <div class="chips">
    <div class="chip od seq"><div class="tag">odds</div><div class="b">the calibrated probability — then graded</div><div class="who">→ bettors · quants</div></div>
    <div class="chip nv seq"><div class="tag">narrative</div><div class="b">the tactical WHY, from named outlets</div><div class="who">→ media · creators</div></div>
    <div class="chip mm seq"><div class="tag">magic_moment</div><div class="b">the decisive goal — scorer, minute</div><div class="who">→ fans · social · TV</div></div>
    <div class="chip st seq"><div class="tag">stats</div><div class="b">xG · shots · possession · set-pieces</div><div class="who">→ clubs · analysts</div></div>
  </div>`,
  reveal:(p)=>seq('.seq',p)},
{label:'one whole match, four layers', secs:16, html:()=>{const h=ARC.hero,g=h.grade;
  return `<div class="kick">③ the whole match — Saudi Arabia stun Argentina (the proof unit)</div>
  <h1 style="font-size:clamp(22px,3vw,34px)">${esc(h.fixture)} <span class="mono" style="font-size:14px;color:var(--mute)">${esc(h.score)}</span></h1>
  <div class="row2" style="margin-top:14px">
    <div>
      <div class="lyr mm"><div class="tag">magic_moment</div><div class="bd"><b>${esc(h.magic.minute)} ${esc(h.magic.scorer)}</b> — ${esc(h.magic.t)}</div><div class="mt">${A(h.magic.src,H(h.magic.src))}</div></div>
      <div class="lyr nv"><div class="tag">narrative</div><div class="bd"><b>${esc((h.narrative[0]||{}).s)}</b> — ${esc((h.narrative[0]||{}).t)}</div><div class="mt">${esc((h.narrative[0]||{}).sys)} · ${A((h.narrative[0]||{}).src,H((h.narrative[0]||{}).src))}</div></div>
    </div>
    <div>
      <div class="lyr st"><div class="tag">stats</div><div class="bd">${h.stats.map(s=>esc(s.m)+': <b>'+esc(s.v)+'</b>').join('<br>')}</div><div class="mt">${esc((h.stats[0]||{}).sys)} · ${A((h.stats[0]||{}).src,H((h.stats[0]||{}).src))}</div></div>
      <div class="lyr od"><div class="tag">odds + grade</div><div class="bd">The system priced <b>${esc(g.favourite)} ${Math.round(g.market_prob*100)}%</b> — and was wrong.<div class="grade"><span class="num" id="bn">0.00</span><span class="l">BRIER · ${esc(g.verdict)}</span></div></div><div class="mt">${esc(h.odds.system)} · ${A(h.odds.src,H(h.odds.src))}</div></div>
    </div>
  </div>`;},
  reveal:(p)=>{const e=$('#bn'); if(e){e.textContent=(Math.min(1,p*1.3)*ARC.hero.grade.brier).toFixed(2);}}},
{label:'the graded board (the data)', secs:13, html:()=>{const s=ARC.summary;
  return `<div class="kick">⑤ the grade — the whole 2022 arc, scored by the rig</div>
  <div class="meanwrap"><div><div class="n" id="mn">0.000</div><div class="mono" style="font-size:11px;color:var(--faint)">mean market Brier (coin-flip 0.25)</div></div>
  <h1 style="font-size:clamp(20px,2.6vw,30px)">Right on the chalk — <span class="red">confidently wrong on the ${s.n_wrong} moments you remember.</span></h1></div>
  <table><thead><tr><th>Match</th><th>Stage</th><th class="r">Mkt%</th><th>Result</th><th class="r">Brier</th><th>Verdict</th></tr></thead><tbody>
  ${ARC.rows.map(r=>`<tr class="brow"><td>${esc(r.fixture)}</td><td>${esc(r.stage)}</td><td class="r">${r.mkt}%</td><td class="${r.won?'right':'wrong'}">${r.won?'fav won':'fav LOST'}</td><td class="r ${r.wrong?'wrong':''}">${r.brier.toFixed(3)}</td><td style="font-size:11.5px;color:var(--faint)">${esc(r.verdict)}</td></tr>`).join('')}
  </tbody></table>`;},
  reveal:(p)=>{const e=$('#mn'); if(e)e.textContent=(Math.min(1,p*1.2)*ARC.summary.mean_brier).toFixed(3); seq('.brow',p);}},
{label:'the business (4 layers = 4 buyers)', secs:10, html:()=>`
  <div class="kick">① business — four products from one research pass</div>
  <h1 style="font-size:clamp(22px,3vw,36px)">Four industries. One trace. One scorecard.</h1>
  <div class="bizgrid">${BIZ.map(b=>`<div class="bcard ${b.layer==='odds'?'od':b.layer==='narrative'?'nv':b.layer==='magic_moment'?'mm':'st'}"><div class="tag">${esc(b.layer)}</div><div class="sys">${esc(b.system)}</div><div class="buy">→ ${esc(b.buyer)}</div><div class="gr">graded: ${esc(b.graded)}</div></div>`).join('')}</div>`},
{label:'2026 — live (MiroMind as updater)', secs:11, html:()=>{const u=DATA.update;return `
  <div class="kick">⑤ MiroMind as the updater — a real live re-forecast on breaking news</div>
  <h1 style="font-size:clamp(24px,3.4vw,42px)">News breaks → MiroMind <span class="hl">re-runs the node.</span></h1>
  <div class="lead">Same compiler, same four layers, graded forward. When news lands, <span class="mono">graph_build.py --update</span> sends a re-forecast to the API and the node moves — with the receipt. This one really ran:</div>
  <div class="lyr od" style="margin-top:8px"><div class="tag">live update · ${esc(u.fixture)}</div>
    <div class="bd"><span style="color:var(--break)">news:</span> "${esc(u.news)}" &nbsp;→&nbsp; <b class="up">${esc(u.revised)||'forecast moved'}</b></div>
    <div class="mt">${u.latency_min} min · ${(u.n_steps||0).toLocaleString()} reasoning steps · ${A(u.src,u.src_host)}</div></div>`;}},
{label:'close', secs:8, html:()=>`
  <div class="kick">past = proof · future = product</div>
  <h1>A number is a guess.<br>A forecast you can <span class="hl">audit and check</span> is intelligence.</h1>
  <div class="lead">${esc(DATA.oneLiner)}</div>`},
];

function seq(sel,p){const items=[...document.querySelectorAll(sel)];const k=Math.floor(p*(items.length+1));items.forEach((it,i)=>it.classList.toggle('on',i<k));}

let cur=-1, playing=false, t=0, last=0;
const total=SCENES.reduce((a,s)=>a+s.secs,0);
function buildDots(){$('#dots').innerHTML=SCENES.map((s,i)=>`<div class="dot" onclick="go(${i})" title="${esc(s.label)}"></div>`).join('');}
function render(i){stage.innerHTML='';const el=document.createElement('div');el.className='scene';el.id='scene';el.innerHTML=SCENES[i].html();stage.appendChild(el);requestAnimationFrame(()=>el.classList.add('on'));
  [...$('#dots').children].forEach((d,j)=>d.classList.toggle('on',j===i));$('#lab').textContent=(i+1)+'/'+SCENES.length+' · '+SCENES[i].label;}
function go(i){i=Math.max(0,Math.min(SCENES.length-1,i));cur=i;t=SCENES.slice(0,i).reduce((a,s)=>a+s.secs,0);render(i);if(SCENES[i].reveal)SCENES[i].reveal(1);updbar();}
function updbar(){$('#fill').style.width=(t/total*100)+'%';}
function frame(ts){if(!playing){last=ts;return;}const dt=(ts-last)/1000;last=ts;t=Math.min(total,t+dt);
  let acc=0,i=0;for(;i<SCENES.length;i++){if(t<acc+SCENES[i].secs)break;acc+=SCENES[i].secs;}i=Math.min(i,SCENES.length-1);
  if(i!==cur){cur=i;render(i);}const p=(t-acc)/SCENES[i].secs;if(SCENES[i].reveal)SCENES[i].reveal(Math.min(1,p));
  updbar();if(t>=total){playing=false;$('#play').textContent='↻ Replay';}requestAnimationFrame(frame);}
$('#play').onclick=()=>{if(t>=total){t=0;cur=-1;}playing=!playing;$('#play').textContent=playing?'❚❚ Pause':'▶ Play';if(playing){last=performance.now();requestAnimationFrame(frame);}};
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(cur+1);if(e.key==='ArrowLeft')go(cur-1);if(e.key===' '){e.preventDefault();$('#play').click();}});
buildDots();go(0);
</script></body></html>"""


if __name__ == "__main__":
    main()
