#!/usr/bin/env python3
"""
serve_demo.py — THE REAL DEMO (not a slideshow).

A local web app that, on every request, RUNS THE REAL PIPELINE — it actually executes
the compiler (node_extract -> node_eval -> forecast -> doctor) on a real captured
MiroMind trace and serves whatever the engine just computed. Nothing on the page is
typed in; press "Run again" and the numbers re-compute. It also reads the real
narrative grain (2022 + 2026) and the real API-usage ledger from disk.

Run:
    python3 dataset/serve_demo.py
    # then open http://localhost:8000  (auto-runs the pipeline on load)

Stdlib only. No network needed (the trace is replayed); the numbers are real.
"""
import http.server
import io
import json
import os
import re
import time
import importlib.util
from collections import Counter
from contextlib import redirect_stdout

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(os.environ.get("PORT", "8000"))


def _load(name):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, name + ".py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


# import the REAL pipeline (demo.py wires the real compiler modules together)
demo = _load("demo")
views = demo.views


def _read_json(fname):
    p = os.path.join(HERE, fname)
    if os.path.exists(p):
        try:
            return json.load(open(p, encoding="utf-8"))
        except Exception:  # noqa: BLE001
            return None
    return None


def run_pipeline():
    """Execute the REAL loop and capture what it actually computed."""
    t0 = time.time()
    buf = io.StringIO()
    with redirect_stdout(buf):                       # swallow the pipeline's prints
        run = demo.step1_trace()
        nodes = demo.step2_extract(run)
        weights = demo.step3_eval(nodes)             # sorts nodes by value
        graph, anchor, line, cap = demo.step4_attach(nodes)
        forecast_before = next(n for n in graph["nodes"] if n["id"] == demo.PARENT_ID)["prob"]
        seed = views.load_seed()
        edge = views.attach_value(nodes, seed)
        fan = views.view_fan(graph, nodes)
        analyst = views.view_analyst(graph, nodes)
        moving = views.view_moving(graph, nodes, edge)
        record = demo.step6_doctor(graph, nodes, anchor, line, cap, weights)
    elapsed_ms = round((time.time() - t0) * 1000)

    steps = run.get("steps", [])
    acts = dict(Counter(s.get("action") for s in steps))
    sample_steps = []
    for s in steps:
        if s.get("action") == "thinking" and len(sample_steps) < 3:
            sample_steps.append(["thinking", (s.get("text") or "")[:40]])
    for s in steps:
        if s.get("action") == "web_search":
            sample_steps.append(["web_search", str(s.get("keywords"))[:60]]); break
    for s in steps:
        if s.get("action") == "fetch":
            sample_steps.append(["fetch", s.get("url")]); break

    top = sorted(nodes, key=lambda n: -(n.get("value_score") or 0))[:10]
    odds_nodes = [{"id": n["node_id"], "judgment": (n.get("judgment") or "")[:150],
                   "dir": n.get("prob_direction"), "value": round(n.get("value_score") or 0, 3),
                   "source": (n.get("sources") or ["—"])[0],
                   "tier": n.get("source_tier")} for n in top]

    # the REAL narrative grain (from the API runs, verified+sourced on disk)
    nar2026 = _read_json("narrative_nodes_2026.json") or {}
    nar2022 = _read_json("narrative_nodes.json") or {}

    return {
        "ran_at_ms": elapsed_ms,
        "trace": {"id": run.get("id"), "q": run.get("q"), "n_steps": len(steps),
                  "acts": acts, "sample": sample_steps,
                  "n_sources": len(run.get("sources") or [])},
        "odds_nodes": odds_nodes,
        "narrative_nodes": (nar2026.get("nodes") or []),
        "narrative_sources": (nar2026.get("sources") or {}),
        "weights": weights,
        "forecast_before": forecast_before,
        "anchor_pct": int(round(anchor * 100)), "line": line,
        "doctor": record,
        "views": {"fan": fan, "analyst": "\n".join(analyst.splitlines()[:22]),
                  "moving": "\n".join(moving.splitlines()[:16])},
        "magic_moment": (nar2022.get("layers", {}).get("magic_moment") or []),
        "grade": ((nar2022.get("layers", {}).get("odds") or [{}])[0].get("grade") or {}),
    }


def load_arc():
    """The graded FIFA-2022 arc (arc_build.py output) + the REAL MiroMind trace steps for the
    'raw trace' view (the distilled layers are the nodes themselves — both surfaced, per the
    raw+distilled decision)."""
    arc = _read_json("arc_2022.graded.json")
    if not arc:
        return {"status": "pending", "hint": "run: python3 dataset/arc_build.py"}
    run = _read_json(os.path.join("runs", "narrative-sau-arg-2022.json")) or {}
    trace = []
    for s in (run.get("steps") or []):
        a = s.get("action")
        if a == "thinking":
            t, act = (s.get("text") or ""), "think"
        elif a == "web_search":
            t, act = "search: " + ", ".join(s.get("keywords") or []), "search"
        elif a == "fetch":
            t, act = "fetch " + (s.get("url") or ""), "fetch"
        else:
            t, act = str(s)[:160], "think"
        if t.strip():
            trace.append({"action": act, "t": t[:170]})
    arc = dict(arc)
    arc["trace"] = trace[:48]
    arc["trace_meta"] = {"run": run.get("id"), "n_steps": len(run.get("steps") or []),
                         "n_sources": len(run.get("sources") or [])}
    return arc


def proof_totals():
    md = os.path.join(HERE, "API_USAGE.md")
    if not os.path.exists(md):
        return "run api_usage.py for the ledger"
    txt = open(md, encoding="utf-8").read()
    lines = [l.strip("- ").strip() for l in txt.splitlines() if l.strip().startswith("- **")]
    return " · ".join(re.sub(r"[*`]", "", l) for l in lines[:4])


PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>THE LEDGER · the REAL demo (runs live)</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Hanken+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0c0b;--panel:#141714;--panel2:#191d18;--ink:#f3f1e9;--mute:#9aa39a;--faint:#5d655c;--line:#262b25;--edge:#4cf0a3;--down:#ff6b5e;--break:#ffc24d;--star:#ffd76b}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--ink);font-family:"Hanken Grotesk",sans-serif;line-height:1.5}
.mono{font-family:"JetBrains Mono",monospace}.up{color:var(--edge)}.dn{color:var(--down)}
.wrap{max-width:1100px;margin:0 auto;padding:28px}
header{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:24px}
.brand{font-family:"Bricolage Grotesque";font-weight:800;font-size:22px}.brand .dot{color:var(--edge)}
.live{font-family:"JetBrains Mono";font-size:11px;color:var(--edge);border:1px solid var(--edge);border-radius:5px;padding:5px 10px}
.live::before{content:"● ";}
.runbtn{font-family:"JetBrains Mono";font-weight:700;font-size:13px;letter-spacing:.06em;color:var(--bg);background:var(--edge);border:none;border-radius:8px;padding:12px 22px;cursor:pointer;text-transform:uppercase}
.runbtn:hover{filter:brightness(1.08)}.runbtn:disabled{opacity:.5;cursor:wait}
.ran{font-family:"JetBrains Mono";font-size:12px;color:var(--mute);margin-left:14px}
h2{font-family:"Bricolage Grotesque";font-weight:700;font-size:22px;margin:34px 0 12px}
.step{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.18em;text-transform:uppercase;color:var(--faint);margin-bottom:8px}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px 20px;margin-bottom:10px}
pre{font-family:"JetBrains Mono";font-size:12px;color:var(--mute);white-space:pre-wrap;line-height:1.5}
.node{display:grid;grid-template-columns:26px 1fr auto;gap:12px;align-items:center;background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:11px 14px;margin-bottom:7px;border-left:3px solid var(--lc,var(--line))}
.node.nv{--lc:var(--break)}.node.od{--lc:var(--edge)}
.d{width:26px;height:26px;border-radius:6px;display:grid;place-items:center;font-family:"JetBrains Mono";font-weight:700;font-size:13px}
.d.u{color:var(--edge);background:rgba(76,240,163,.08)}.d.d{color:var(--down);background:rgba(255,107,94,.08)}.d.n{color:var(--mute);background:var(--panel2)}
.j{font-size:13.5px}.meta{font-family:"JetBrains Mono";font-size:10.5px;color:var(--faint);margin-top:4px}
.meta a{color:var(--mute)}
.val{font-family:"JetBrains Mono";font-size:12px;color:var(--mute)}
.big{font-family:"Bricolage Grotesque";font-weight:800;font-size:88px;line-height:1;letter-spacing:-.04em}
.move{display:flex;align-items:baseline;gap:16px}.from{font-family:"JetBrains Mono";font-size:20px;color:var(--faint);text-decoration:line-through}
.grade{font-family:"JetBrains Mono";font-size:14px;color:var(--down)}
.mm{border-left:3px solid var(--star);background:rgba(255,215,107,.05)}
.note{font-size:12px;color:var(--faint);margin-top:8px}
.proof{font-family:"JetBrains Mono";font-size:12px;color:var(--edge);background:rgba(76,240,163,.05);border:1px solid var(--edge-dim,#1d6b4c);border-radius:8px;padding:12px 16px}
.err{color:var(--down);font-family:"JetBrains Mono"}
</style></head><body><div class="wrap">
<header>
  <div class="brand">THE LEDGER<span class="dot">.</span> <span class="mono" style="font-size:11px;color:var(--faint);margin-left:8px">the REAL demo — the compiler runs live on every click</span></div>
  <div><button class="runbtn" id="run" onclick="runIt()">▶ Run the real pipeline</button><span class="ran" id="ran"></span></div>
</header>
<div id="out"><p class="note">Press <b>Run the real pipeline</b> — the server will execute the compiler on the real MiroMind trace and fill this page with whatever it just computed.</p></div>
</div>
<script>
async function runIt(){
  const b=document.getElementById('run'); b.disabled=true; b.textContent='running the compiler…';
  document.getElementById('ran').textContent='';
  try{
    const r=await fetch('/run'); const d=await r.json();
    if(d.error){document.getElementById('out').innerHTML='<p class="err">pipeline error: '+d.error+'</p>';return;}
    render(d);
    document.getElementById('ran').textContent='✓ executed live in '+d.ran_at_ms+' ms · '+new Date().toLocaleTimeString();
  }catch(e){document.getElementById('out').innerHTML='<p class="err">'+e+'</p>';}
  finally{b.disabled=false;b.textContent='▶ Run again';}
}
function dirCls(x){return x==='up'?'u':x==='down'?'d':'n'} function dirSym(x){return x==='up'?'▲':x==='down'?'▼':'—'}
function render(d){
  const t=d.trace, doc=d.doctor, g=d.grade||{};
  let h='';
  h+='<div class="proof">PROVEN LIVE: '+(d.proof||'')+'</div>';
  // step1
  h+='<h2>1 · the real MiroMind trace</h2><div class="step">replayed · '+t.n_steps.toLocaleString()+' steps · '+t.n_sources+' sources</div><div class="panel"><div class="mono" style="font-size:12px;color:var(--mute)">'+t.q+'</div><pre>'+JSON.stringify(t.acts)+'\\n'+t.sample.map(s=>'['+s[0]+'] '+s[1]).join('\\n')+'</pre></div>';
  // step2/3 nodes — ODDS layer (live extracted)
  h+='<h2>2–3 · compiled into nodes, value-scored <span class="mono" style="font-size:12px;color:var(--faint)">(odds layer — extracted live)</span></h2>';
  h+=d.odds_nodes.map(n=>'<div class="node od"><div class="d '+dirCls(n.dir)+'">'+dirSym(n.dir)+'</div><div><div class="j">'+esc(n.judgment)+'</div><div class="meta">'+ (n.source||'') +'</div></div><div class="val">'+n.value+'</div></div>').join('');
  // narrative layer (real grain)
  if(d.narrative_nodes && d.narrative_nodes.length){
    h+='<h2>the narrative layer <span class="mono" style="font-size:12px;color:var(--faint)">(the 解说 / reporter — real grain, sourced)</span></h2>';
    h+=d.narrative_nodes.map(n=>{const src=(d.narrative_sources||{})[(n.sources||[])[0]]||'';return '<div class="node nv"><div class="d '+dirCls(n.prob_direction)+'">'+dirSym(n.prob_direction)+'</div><div><div class="j"><b>'+esc(n.storyline||'')+'</b> — '+esc(n.text||'')+'</div><div class="meta">'+(n.grain||'')+' · <a href="'+src+'" target="_blank">'+host(src)+' ↗</a></div></div><div class="val"></div></div>'}).join('');
  }
  // forecast + doctor
  h+='<h2>4 · forecast = the sharp market, then the doctor update</h2><div class="panel"><div class="move"><span class="from">'+d.forecast_before+'%</span><span class="big dn">'+doc.parent_prob_after+'%</span></div><div class="note">computed: anchor '+d.anchor_pct+'% (line '+d.line+') · injury (unpriced) → '+doc.parent_prob_after+'% · market still '+doc.market_anchor_pct+'% → <b class="up">'+(doc.market_anchor_pct-doc.parent_prob_after)+' pts below the stale line</b>. '+esc(doc.news||'')+'</div></div>';
  // magic moment + grade (2022 video layer, real)
  if(d.magic_moment && d.magic_moment.length){
    const mm=d.magic_moment[d.magic_moment.length-1];
    h+='<h2>the magic-moment + grade layer <span class="mono" style="font-size:12px;color:var(--faint)">(2022 proof)</span></h2><div class="panel mm"><div class="j"><b class="st">'+esc(mm.minute||'')+' '+esc(mm.scorer||'')+'</b> — '+esc(mm.text||'')+'</div><div class="grade">odds layer graded: '+esc(g.verdict||'')+'</div></div>';
  }
  // views
  h+='<h2>5 · three products from the one trace</h2><div class="panel"><pre>'+esc(d.views.fan)+'</pre></div>';
  document.getElementById('out').innerHTML=h;
}
function esc(s){return (s||'').replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]))}
function host(u){try{return new URL(u).hostname.replace('www.','')}catch(e){return 'source'}}
window.addEventListener('load',runIt);
</script></body></html>"""


class H(http.server.BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/" or self.path.startswith("/index"):
            self._send(200, PAGE.encode("utf-8"), "text/html; charset=utf-8")
        elif self.path.startswith("/replay"):         # the self-contained replay (the demo-video deck)
            p = os.path.join(HERE, "replay.html")
            self._send(200, open(p, "rb").read(), "text/html; charset=utf-8")
        elif self.path.startswith("/arc60"):          # the 60s reasoning+compiling web animation
            p = os.path.join(HERE, "arc60.html")
            self._send(200, open(p, "rb").read(), "text/html; charset=utf-8")
        elif self.path.startswith("/arc"):            # the graded FIFA-2022 arc data (+ real trace)
            self._send(200, json.dumps(load_arc()).encode("utf-8"), "application/json")
        elif self.path.startswith("/run"):
            try:
                result = run_pipeline()
                result["proof"] = proof_totals()
            except Exception as e:  # noqa: BLE001
                import traceback
                result = {"error": f"{type(e).__name__}: {e}", "tb": traceback.format_exc()[-800:]}
            self._send(200, json.dumps(result).encode("utf-8"), "application/json")
        else:
            self._send(404, b"not found", "text/plain")


def main():
    print(f"THE REAL DEMO running at  http://localhost:{PORT}")
    print("Open it; every click executes the compiler on the real trace. Ctrl-C to stop.")
    http.server.HTTPServer(("127.0.0.1", PORT), H).serve_forever()


if __name__ == "__main__":
    main()
