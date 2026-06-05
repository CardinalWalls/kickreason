#!/usr/bin/env python3
"""
build_compiler_demo.py — the VIDEO demo of the compiler process.

Shows the whole north-star loop on a real node, scene by scene (auto-plays, recordable):
  1. THE QUESTION        — one valued node in the champion-rooted graph
  2. MIROMIND REASONS     — the real trace: searches, fetches, sources (transparent reasoning)
  3. THE COMPILER         — prose answer  ->  a structured debatable node  (the centerpiece)
  4. THE DEBATABLE NODE   — position · sourced why · counterpoint · argue with it · graded
  5. CHAMPION-ROOTED GRAPH— every valued node ladders to the final one: WHO IS THE CHAMPION

Reads a compiled node (dataset/nodes/*.json) + its run (dataset/runs/*.json) and inlines them.
  python3 dataset/build_compiler_demo.py [nodes/<slug>.json] [runs/<run>.json]
Self-contained -> dataset/compiler_demo.html (open via file://, no server).
"""
import json, os, re, sys, glob

HERE = os.path.dirname(os.path.abspath(__file__))


def clean(s, n=600):
    s = (s or "").replace("**", "").replace("\\n", " ").replace("•", "·")
    s = re.sub(r"\s+", " ", s).strip()
    return s[:n] + ("…" if len(s) > n else "")


def host(u):
    m = re.match(r"https?://([^/]+)", u or "")
    return (m.group(1).replace("www.", "") if m else "source")


def pick_node():
    if len(sys.argv) > 1:
        return json.load(open(os.path.join(HERE, sys.argv[1])))
    files = sorted(glob.glob(os.path.join(HERE, "nodes", "*.json")), key=os.path.getmtime)
    return json.load(open(files[-1])) if files else None


def pick_run(node):
    if len(sys.argv) > 2:
        return json.load(open(os.path.join(HERE, sys.argv[2])))
    # match a run whose question ~ the node's, else newest ask-*
    for p in sorted(glob.glob(os.path.join(HERE, "runs", "*.json")), key=os.path.getmtime, reverse=True):
        try:
            r = json.load(open(p))
        except Exception:
            continue
        q = r.get("q") or r.get("question") or ""
        if q and node and q[:30].lower() in (node.get("question", "").lower()):
            return r
    cands = sorted(glob.glob(os.path.join(HERE, "runs", "ask-*.json")), key=os.path.getmtime)
    return json.load(open(cands[-1])) if cands else {}


def main():
    node = pick_node()
    if not node:
        raise SystemExit("no compiled node in dataset/nodes/ — run compile_question.py first")
    run = pick_run(node)
    steps = run.get("steps") or []
    searches = [", ".join(s.get("keywords") or []) if isinstance(s.get("keywords"), list) else str(s.get("keywords"))
                for s in steps if s.get("action") == "web_search"][:8]
    fetches = [s.get("url") for s in steps if s.get("action") == "fetch"][:5]
    raw = clean(run.get("answer") or run.get("content") or "", 520)

    DATA = {
        "question": node.get("question", ""),
        "trace": {
            "searches": searches, "fetches": fetches,
            "n_sources": len(run.get("sources") or node.get("sources") or []),
            "tokens": (run.get("usage") or {}).get("total_tokens") or (node.get("_meta") or {}).get("tokens"),
            "elapsed": run.get("elapsed_s") or (node.get("_meta") or {}).get("elapsed_s"),
            "raw": raw,
        },
        "node": {
            "position": clean(node.get("position"), 240),
            "arguments": [{"claim": clean(a.get("claim"), 130), "host": host(a.get("source")), "source": a.get("source")}
                          for a in (node.get("arguments") or [])[:5]],
            "counterpoint": clean(node.get("counterpoint"), 260),
            "what_would_change": clean(node.get("what_would_change"), 200),
            "confidence": node.get("confidence", "medium"),
            "resolvable": node.get("resolvable"),
        },
    }
    payload = json.dumps(DATA, ensure_ascii=False)
    out = TEMPLATE.replace("/*__DATA__*/", payload)
    open(os.path.join(HERE, "compiler_demo.html"), "w", encoding="utf-8").write(out)
    print("wrote dataset/compiler_demo.html (self-contained)")
    print(f"  node: \"{DATA['question'][:60]}\"  · {len(DATA['node']['arguments'])} sourced arguments")
    print(f"  trace: {len(searches)} searches · {DATA['trace']['n_sources']} sources · {DATA['trace']['tokens']} tokens")
    print("  open: open dataset/compiler_demo.html")


TEMPLATE = r"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>the compiler — reasoning → debatable node</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Hanken+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#080a09;--panel:#121514;--p2:#0c0f0d;--ink:#f3f1e9;--mute:#9aa39a;--faint:#5d655c;--line:#262b25;
  --edge:#4cf0a3;--down:#ff6b5e;--break:#ffc24d;--star:#ffd76b;--narr:#8ab4ff;--violet:#c9a0ff}
*{box-sizing:border-box;margin:0;padding:0}html,body{height:100%}
body{background:var(--bg);color:var(--ink);font-family:"Hanken Grotesk",sans-serif;line-height:1.45;overflow:hidden}
.mono{font-family:"JetBrains Mono",monospace}
.stage{position:fixed;inset:0;overflow:hidden}
.scene{position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;padding:7vh 8vw;opacity:0;transform:translateY(16px);transition:.55s;overflow:auto}
.scene.on{opacity:1;transform:none}
.kick{font-family:"JetBrains Mono";font-size:12px;letter-spacing:.32em;text-transform:uppercase;color:var(--edge);margin-bottom:16px}
h1{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(26px,4.4vw,52px);line-height:1.05;letter-spacing:-.02em;max-width:20ch}
.lead{color:var(--mute);font-size:clamp(15px,1.7vw,20px);margin-top:16px;max-width:60ch}
.two{display:grid;grid-template-columns:1fr 64px 1fr;gap:18px;align-items:center;margin-top:8px}
@media(max-width:900px){.two{grid-template-columns:1fr;gap:12px}.two .ar{display:none}}
.box{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px 18px;max-height:64vh;overflow:auto}
.box.raw{border-left:3px solid var(--break)} .box.node{border-left:3px solid var(--edge)}
.boxlab{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--faint);margin-bottom:10px}
.rawtext{font-size:13px;color:var(--mute);line-height:1.6}
.ar{font-family:"Bricolage Grotesque";font-weight:800;font-size:40px;color:var(--edge);text-align:center}
.fld{opacity:0;transform:translateX(8px);transition:.4s;margin-bottom:11px;padding-bottom:10px;border-bottom:1px solid #1b201a}
.fld.on{opacity:1;transform:none}
.fld .k{font-family:"JetBrains Mono";font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;color:var(--violet);font-weight:700}
.fld .v{font-size:14px;margin-top:3px} .fld .v.pos{font-weight:600} .fld .v.cp{color:var(--down)}
.fld .src{font-family:"JetBrains Mono";font-size:11px;color:var(--narr)}
.arg{margin:5px 0} .arg .b{font-size:13.5px} .arg .src{font-size:11px}
.trace{background:var(--p2);border:1px solid var(--line);border-radius:12px;padding:10px 14px;max-height:56vh;overflow:auto;margin-top:8px}
.tl{font-family:"JetBrains Mono";font-size:13px;color:var(--mute);margin:7px 0;opacity:0;transform:translateY(6px);transition:.3s}
.tl.on{opacity:1;transform:none}.tl .a{color:var(--break)}.tl.f .a{color:var(--edge)}
.stat{display:flex;gap:10px;flex-wrap:wrap;margin-top:12px}.stat div{background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:10px 14px}
.stat b{font-family:"Bricolage Grotesque";font-size:22px;display:block}.stat span{font-family:"JetBrains Mono";font-size:10px;color:var(--faint)}
/* graph */
.graph{display:flex;flex-direction:column;align-items:center;gap:0;margin-top:10px}
.champ{background:var(--star);color:#1a1407;font-family:"Bricolage Grotesque";font-weight:800;padding:12px 22px;border-radius:10px;font-size:18px}
.edge{width:2px;height:26px;background:var(--line)}
.tier{display:flex;gap:10px;flex-wrap:wrap;justify-content:center}
.qn{background:var(--panel);border:1px solid var(--line);border-radius:8px;padding:8px 12px;font-size:12.5px;opacity:0;transform:scale(.95);transition:.4s}
.qn.on{opacity:1;transform:none}.qn.hot{border-color:var(--edge);color:var(--edge)}
.debate{background:var(--panel);border:1px solid var(--line);border-radius:11px;padding:14px 16px;margin-top:12px}
.debate .u{color:var(--narr)} .debate .a{color:var(--edge)}
.hud{position:fixed;left:0;right:0;bottom:0;padding:13px 20px;display:flex;align-items:center;gap:14px;background:linear-gradient(transparent,rgba(0,0,0,.65));z-index:30}
.btn{font-family:"JetBrains Mono";font-weight:700;font-size:12px;color:var(--bg);background:var(--edge);border:none;border-radius:7px;padding:9px 15px;cursor:pointer;text-transform:uppercase}
.nav{font-family:"JetBrains Mono";font-size:12px;color:var(--mute);background:none;border:1px solid var(--line);border-radius:6px;padding:8px 11px;cursor:pointer}
.bar{flex:1;height:4px;background:var(--line);border-radius:3px;overflow:hidden}.bar>i{display:block;height:100%;width:0;background:var(--edge);transition:width .3s}
.lab{font-family:"JetBrains Mono";font-size:11px;color:var(--faint);min-width:230px;text-align:right}
.dots{display:flex;gap:5px}.dot{width:8px;height:8px;border-radius:50%;background:var(--line);cursor:pointer}.dot.on{background:var(--edge)}
.brand{position:fixed;top:16px;left:20px;font-family:"Bricolage Grotesque";font-weight:800;font-size:15px;z-index:30}.brand .d{color:var(--edge)}
</style></head><body>
<div class="brand">THE COMPILER<span class="d">.</span></div>
<div class="stage" id="stage"></div>
<div class="hud">
  <button class="btn" id="play">▶ Play</button>
  <button class="nav" onclick="go(cur-1)">←</button><button class="nav" onclick="go(cur+1)">→</button>
  <div class="dots" id="dots"></div><div class="bar"><i id="fill"></i></div><span class="lab" id="lab"></span>
</div>
<script>
const DATA=/*__DATA__*/;const $=s=>document.querySelector(s),stage=$('#stage');
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function seq(sel,p){const it=[...document.querySelectorAll(sel)];const k=Math.floor(p*(it.length+1));it.forEach((e,i)=>e.classList.toggle('on',i<k));}
const N=DATA.node,T=DATA.trace;
const SCENES=[
{label:'the question (a valued node)',secs:8,html:()=>`
  <div class="kick">★ every question is a valued node · rooted at the champion</div>
  <h1>${esc(DATA.question)}</h1>
  <div class="lead">Not "who wins" handed down as a number — a question worth asking, that ladders toward the one that matters. Watch it become a debatable, sourced node.</div>`},
{label:'MiroMind reasons (the engine)',secs:12,html:()=>`
  <div class="kick">① the engine — MiroMind researches & reasons, transparently</div>
  <h1 style="font-size:clamp(20px,2.6vw,30px)">It researches the question — live, sourced, step by step.</h1>
  <div class="trace" id="trace"></div>
  <div class="stat">
    <div><b>${T.n_sources}</b><span>sources cited</span></div>
    <div><b>${(T.tokens||0).toLocaleString()}</b><span>tokens of reasoning</span></div>
    <div><b>${T.elapsed||'~'}s</b><span>one live call</span></div>
  </div>`,
  reveal:(p)=>{const box=$('#trace');if(!box)return;const items=T.searches.map(s=>['search',s]).concat(T.fetches.map(f=>['read',f]));
    const k=Math.floor(Math.min(1,p*1.3)*(items.length+1));while(box.children.length<Math.min(k,items.length)){const j=box.children.length;const [a,t]=items[j];
    const d=document.createElement('div');d.className='tl '+(a==='read'?'f':'');d.innerHTML='<span class="a">'+a+'</span> '+esc(t);box.appendChild(d);requestAnimationFrame(()=>d.classList.add('on'));box.scrollTop=box.scrollHeight;}}},
{label:'THE COMPILER (prose → node)',secs:16,html:()=>`
  <div class="kick">② the compiler — raw reasoning → a structured debatable node</div>
  <div class="two">
    <div class="box raw"><div class="boxlab">raw: MiroMind's answer (prose)</div><div class="rawtext">${esc(T.raw)}</div></div>
    <div class="ar">→</div>
    <div class="box node"><div class="boxlab">compiled: the debatable node</div>
      <div class="fld seq"><div class="k">position</div><div class="v pos">${esc(N.position)}</div></div>
      <div class="fld seq"><div class="k">arguments (each sourced)</div><div class="v">${N.arguments.map(a=>`<div class="arg"><span class="b">· ${esc(a.claim)}</span> <a class="src" href="${esc(a.source)}" target="_blank">↗ ${esc(a.host)}</a></div>`).join('')}</div></div>
      <div class="fld seq"><div class="k">counterpoint</div><div class="v cp">${esc(N.counterpoint||'—')}</div></div>
      <div class="fld seq"><div class="k">confidence · graded</div><div class="v">${esc(N.confidence)} · ${N.resolvable?'locked before kickoff → graded after':'analytical'}</div></div>
    </div>
  </div>`,
  reveal:(p)=>seq('.fld',Math.max(0,(p-0.2)/0.8))},
{label:'the debatable node',secs:11,html:()=>`
  <div class="kick">③ you don't read it — you argue with it</div>
  <h1 style="font-size:clamp(20px,2.6vw,30px)">Challenge it. It answers with sources.</h1>
  <div class="debate">
    <div><span class="u">you:</span> "${esc((N.counterpoint||'that ignores the toughest opponent').split('.')[0])}?"</div>
    <div style="margin-top:8px"><span class="a">node:</span> here's the sourced counter-case — and ${N.arguments.length} cited arguments behind the position. Disagree? <b style="color:var(--ink)">Lock your own take — the scoreboard settles it.</b></div>
  </div>
  <div class="lead">KickOracle gives a number you argue about with your mates. This argues back, with receipts.</div>`},
{label:'champion-rooted graph (the SSOT)',secs:9,html:()=>`
  <div class="kick">★ the law — every valued node ladders to the final one</div>
  <div class="graph">
    <div class="champ">WHO IS THE CHAMPION?</div><div class="edge"></div>
    <div class="tier">
      <div class="qn seq">contenders & threats</div><div class="qn seq hot">this node</div><div class="qn seq">exploitable weakness</div><div class="qn seq">path through the draw</div>
    </div><div class="edge"></div>
    <div class="tier"><div class="qn seq">match nodes</div><div class="qn seq">player nodes</div><div class="qn seq">moment nodes</div><div class="qn seq">… thousands, grounded in real 2022 data</div></div>
  </div>
  <div class="lead">One reasoned, sourced, debatable node — multiplied across every question that bears on the trophy. That's the graph.</div>`,
  reveal:(p)=>seq('.qn',p)},
];
let cur=-1,playing=false,t=0,last=0;const total=SCENES.reduce((a,s)=>a+s.secs,0);
$('#dots').innerHTML=SCENES.map((s,i)=>`<div class="dot" onclick="go(${i})"></div>`).join('');
function render(i){stage.innerHTML='';const el=document.createElement('div');el.className='scene';el.id='scene';el.innerHTML=SCENES[i].html();stage.appendChild(el);requestAnimationFrame(()=>el.classList.add('on'));[...$('#dots').children].forEach((d,j)=>d.classList.toggle('on',j===i));$('#lab').textContent=(i+1)+'/'+SCENES.length+' · '+SCENES[i].label;}
function go(i){i=Math.max(0,Math.min(SCENES.length-1,i));cur=i;t=SCENES.slice(0,i).reduce((a,s)=>a+s.secs,0);render(i);if(SCENES[i].reveal)SCENES[i].reveal(1);$('#fill').style.width=(t/total*100)+'%';}
function frame(ts){if(!playing){last=ts;return;}t=Math.min(total,t+(ts-last)/1000);last=ts;let acc=0,i=0;for(;i<SCENES.length;i++){if(t<acc+SCENES[i].secs)break;acc+=SCENES[i].secs;}i=Math.min(i,SCENES.length-1);if(i!==cur){cur=i;render(i);}if(SCENES[i].reveal)SCENES[i].reveal(Math.min(1,(t-acc)/SCENES[i].secs));$('#fill').style.width=(t/total*100)+'%';if(t>=total){playing=false;$('#play').textContent='↻ Replay';}requestAnimationFrame(frame);}
$('#play').onclick=()=>{if(t>=total){t=0;cur=-1;}playing=!playing;$('#play').textContent=playing?'❚❚ Pause':'▶ Play';if(playing){last=performance.now();requestAnimationFrame(frame);}};
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(cur+1);if(e.key==='ArrowLeft')go(cur-1);if(e.key===' '){e.preventDefault();$('#play').click();}});
go(0);
</script></body></html>"""

if __name__ == "__main__":
    main()
