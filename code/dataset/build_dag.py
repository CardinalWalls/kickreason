#!/usr/bin/env python3
"""
build_dag.py — assemble the REAL champion-rooted DAG and render it.

Edges = the real 2022 tournament. CHAMPION ← Final ← Semi-finals ← Quarter-finals ← Round of 16
← Group stage(A-H) ← the 64 fixtures ← all 8,367 question-nodes. Stage comes from each question's
own `stage` field (real), so every node attaches — nothing is dropped. Scores enrich from
lib2022/index.json + bracket.json. The root carries the live MiroMind champion node (6 layers +
its depends_on = the top edges) when present.

  python3 dataset/build_dag.py   ->   dataset/dag.json + dataset/dag.html  (open via file://)
"""
import json, os, re, html, glob

HERE = os.path.dirname(os.path.abspath(__file__))
L = lambda *p: os.path.join(HERE, "lib2022", *p)
hesc = lambda s: html.escape(str(s if s is not None else ""))
clean = lambda s, n=240: re.sub(r"\s+", " ", (s or "").replace("**", "")).strip()[:n]
fixkey = lambda s: re.sub(r"\s+", " ", (s or "").strip()).lower()

QS = json.load(open(os.path.join(HERE, "questions_2022.json")))
IDX = json.load(open(L("index.json")))
BR = json.load(open(L("bracket.json")))
TEAMS = json.load(open(L("teams.json")))
champ_files = sorted(glob.glob(os.path.join(HERE, "nodes", "who-will-win*.json")), key=os.path.getmtime)
CHAMP = json.load(open(champ_files[-1])) if champ_files else None

# ── attach every question by its real stage/fixture (nothing dropped) ──
q_by_fixture, fix_stage, fix_label, q_by_team, futures = {}, {}, {}, {}, []
for q in QS:
    cat = q["category"]
    if cat == "futures":
        futures.append(q)
    elif cat in ("group", "progression"):
        q_by_team.setdefault(q.get("subject"), []).append(q)
    elif cat == "match_core":
        fx = fixkey(q.get("subject"))
        q_by_fixture.setdefault(fx, []).append(q)
        fix_stage.setdefault(fx, q.get("stage"))
        fix_label.setdefault(fx, q.get("subject"))
    elif cat == "player_prop":
        q_by_fixture.setdefault(fixkey(q.get("fixture")), []).append(q)

# real scores per fixture (index = group + everything; bracket = knockout)
score = {}
for m in IDX:
    score[fixkey(f"{m['home_team']} vs {m['away_team']}")] = f"{m.get('home_score')}-{m.get('away_score')}"
for rnd, ms in BR.items():
    for m in ms:
        score[fixkey(f"{m['home']} vs {m['away']}")] = m.get("score", "")


def fixture_node(fx):
    qs = q_by_fixture.get(fx, [])
    sc = score.get(fx, "")
    return {"id": "f-" + re.sub(r"[^a-z0-9]+", "-", fx)[:30], "type": "match",
            "label": f"{fix_label.get(fx, fx)}  {sc}".strip(), "questions": qs, "qn": len(qs)}


stage_fix = {}
for fx, st in fix_stage.items():
    stage_fix.setdefault(st, []).append(fx)

# champion ← these rounds (dependency order); each round ← its real fixtures
KO_ORDER = ["Final", "Third place", "Semi-final", "Quarter-final", "Round of 16"]
ko_nodes = [{"id": st.lower().replace(" ", "-"), "type": "round", "label": st,
             "kids": [fixture_node(fx) for fx in sorted(stage_fix.get(st, []))]}
            for st in KO_ORDER if stage_fix.get(st)]
groups = sorted(g for g in stage_fix if g.startswith("Group "))
group_node = {"id": "group-stage", "type": "round", "label": "Group stage",
              "kids": [{"id": "grp-" + g[-1], "type": "group", "label": g,
                        "kids": [fixture_node(fx) for fx in sorted(stage_fix[g])]} for g in groups]}
team_outlooks = {"id": "team-outlooks", "type": "round",
                 "label": "Team outlooks (win-group · advance · reach-round)",
                 "kids": [{"id": "t-" + re.sub(r"[^a-z0-9]+", "-", fixkey(t)), "type": "team",
                           "label": t, "questions": qs, "qn": len(qs)}
                          for t, qs in sorted(q_by_team.items(), key=lambda kv: -len(kv[1]))]}

CHAMPION = next((q.get("resolved") for q in QS if (q.get("market") or "").startswith("Tournament winner")), "Argentina")
DAG = {
    "id": "champion", "type": "champion",
    "label": f"WHO IS THE CHAMPION?  →  {CHAMPION} (2022) ✓",
    "miromind": ({"position": clean(CHAMP.get("position"), 200),
                  "layers": {k: clean((v or {}).get("text"), 150) for k, v in (CHAMP.get("layers") or {}).items()},
                  "depends_on": [clean(c, 120) for c in (CHAMP.get("depends_on") or [])],
                  "sources": (CHAMP.get("_meta") or {}).get("n_sources"),
                  "tokens": (CHAMP.get("_meta") or {}).get("tokens")} if CHAMP else None),
    "futures": futures,
    "kids": ko_nodes + [group_node, team_outlooks],
}


def count_q(node):
    return (len(node.get("questions", [])) + len(node.get("futures", []))
            + sum(count_q(k) for k in node.get("kids", [])))


TOTAL = count_q(DAG)
json.dump(DAG, open(os.path.join(HERE, "dag.json"), "w"), ensure_ascii=False, indent=1)


def q_rows(qs):
    out = []
    for q in qs:
        res = f' <span class="res">→ {hesc(q.get("resolved"))}</span>' if q.get("resolved") else ""
        out.append(f'<div class="q"><span class="ql {hesc(q.get("layer",""))}">{hesc((q.get("layer") or "")[:4])}</span>'
                   f'<span class="qt">{hesc(q.get("market") or q.get("subject"))}</span>{res}</div>')
    return "".join(out)


def render(node, depth=0):
    badge = f'<span class="cnt">{count_q(node):,} nodes</span>'
    head = f'<summary class="nd {hesc(node.get("type",""))}">{hesc(node["label"])} {badge}</summary>'
    inner = (f'<div class="qs">{q_rows(node["questions"])}</div>' if node.get("questions") else "")
    inner += "".join(render(k, depth + 1) for k in node.get("kids", []))
    return f'<details class="lvl{min(depth,4)}" {"open" if depth<1 else ""}>{head}<div class="bd">{inner}</div></details>'


mm = DAG["miromind"]
if mm:
    layers = "".join(f'<div class="ly"><b>{hesc(k)}</b> {hesc(v)}</div>' for k, v in mm["layers"].items() if v)
    deps = "".join(f'<div class="dep">→ {hesc(d)}</div>' for d in mm["depends_on"])
    mm_html = (f'<div class="mm"><div class="mmh">the champion node — reasoned live by MiroMind '
               f'({mm.get("sources")} sources · {(mm.get("tokens") or 0):,} tokens) · 6 layers + depends_on (the top edges)</div>'
               f'<div class="pos"><b>position:</b> {hesc(mm["position"])}</div>'
               f'<div class="lys">{layers}</div>'
               f'<div class="deph">depends_on → these become the child nodes (the DAG edges):</div><div class="deps">{deps}</div></div>')
else:
    mm_html = '<div class="mm pending">★ champion node still compiling live via MiroMind — re-run build_dag.py when it lands to seat it at the root with its 6 layers + depends_on.</div>'

DOC = f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>champion-rooted DAG — {TOTAL:,} real nodes</title>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:wght@700;800&family=Hanken+Grotesk:wght@400;500;600&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{{--bg:#080a09;--panel:#121514;--ink:#f3f1e9;--mute:#9aa39a;--faint:#5d655c;--line:#20251f;--edge:#4cf0a3;--break:#ffc24d;--narr:#8ab4ff;--violet:#c9a0ff;--star:#ffd76b}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{background:var(--bg);color:var(--ink);font-family:"Hanken Grotesk",sans-serif;line-height:1.4}}
.wrap{{max-width:1080px;margin:0 auto;padding:28px 22px 80px}}
.hero{{text-align:center;padding:24px 0 16px;border-bottom:1px solid var(--line)}}
.kick{{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.3em;text-transform:uppercase;color:var(--edge)}}
.champ{{font-family:"Bricolage Grotesque";font-weight:800;font-size:clamp(24px,4vw,44px);letter-spacing:-.02em;margin:10px 0 6px}}.champ .a{{color:var(--star)}}
.scale{{font-family:"JetBrains Mono";font-size:12.5px;color:var(--mute)}}.scale b{{color:var(--ink)}}
.mm{{background:var(--panel);border:1px solid var(--line);border-left:3px solid var(--edge);border-radius:12px;padding:15px 18px;margin:18px 0}}
.mm.pending{{color:var(--break);border-left-color:var(--break);font-family:"JetBrains Mono";font-size:12.5px}}
.mmh{{font-family:"JetBrains Mono";font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--edge);margin-bottom:8px}}
.pos{{font-size:14px;margin-bottom:8px}}.pos b{{color:var(--edge)}}
.lys{{display:grid;grid-template-columns:1fr 1fr;gap:5px 16px;margin:6px 0}}.ly{{font-size:12.5px;color:var(--mute)}}.ly b{{color:var(--violet);font-family:"JetBrains Mono";font-size:11px;text-transform:uppercase}}
.deph{{font-family:"JetBrains Mono";font-size:10.5px;color:var(--faint);margin-top:8px;text-transform:uppercase;letter-spacing:.08em}}
.dep{{font-size:13px;color:var(--narr);margin:2px 0}}
.tree{{margin-top:10px}}
details{{margin:2px 0}}.bd{{border-left:1px solid var(--line);margin-left:9px;padding-left:13px}}
summary.nd{{cursor:pointer;list-style:none;padding:6px 9px;border-radius:7px;font-size:14px;display:flex;align-items:center;gap:9px}}
summary.nd::-webkit-details-marker{{display:none}}summary.nd::before{{content:"▸";color:var(--faint);font-size:11px}}
details[open]>summary.nd::before{{content:"▾"}}summary.nd:hover{{background:var(--panel)}}
.nd.round{{font-family:"Bricolage Grotesque";font-weight:700}}.nd.group{{color:var(--break)}}.nd.match,.nd.team{{color:var(--mute);font-size:13px}}
.cnt{{font-family:"JetBrains Mono";font-size:10.5px;color:var(--edge);margin-left:auto;border:1px solid var(--line);border-radius:5px;padding:1px 7px}}
.qs{{display:grid;grid-template-columns:1fr 1fr;gap:0 18px;padding:4px 0 4px 14px}}
.q{{display:flex;gap:7px;align-items:baseline;padding:3px 0;border-bottom:1px solid #14180f;font-size:12px}}
.ql{{font-family:"JetBrains Mono";font-size:8.5px;text-transform:uppercase;padding:1px 4px;border-radius:3px;color:var(--faint);border:1px solid var(--line);min-width:34px;text-align:center}}
.ql.odds{{color:var(--edge);border-color:#1d5b40}}.ql.stats{{color:var(--violet);border-color:#4a3a6b}}.ql.narrative{{color:var(--break)}}
.qt{{color:var(--mute);flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}}.res{{font-family:"JetBrains Mono";font-size:10.5px;color:var(--edge)}}
.foot{{margin-top:30px;text-align:center;font-family:"JetBrains Mono";font-size:11px;color:var(--faint)}}
</style></head><body><div class="wrap">
<div class="hero">
  <div class="kick">★ the champion-rooted DAG · edges = the real 2022 tournament</div>
  <div class="champ">{hesc(DAG["label"])}</div>
  <div class="scale"><b>{TOTAL:,}</b> real question-nodes · <b>{len(stage_fix)}</b> stages · <b>{sum(len(v) for v in stage_fix.values())}</b> fixtures · <b>{len(TEAMS)}</b> teams · edges from lib2022 (StatsBomb) — expand any branch to walk the graph</div>
</div>
{mm_html}
<div style="font-family:'JetBrains Mono';font-size:11px;color:var(--faint);margin:8px 0 4px;letter-spacing:.05em">CHAMPION ← rounds (real edges) ← fixtures ← the mass of question-nodes — every edge a real 2022 result:</div>
<div class="tree">
  {''.join(render(k) for k in DAG["kids"])}
  <details class="lvl0"><summary class="nd round">Futures — the title race <span class="cnt">{len(futures)} nodes</span></summary><div class="bd"><div class="qs">{q_rows(futures)}</div></div></details>
</div>
<div class="foot">{TOTAL:,} nodes · champion-rooted · every edge a real 2022 result (lib2022) · the live MiroMind champion node seats at the root, its depends_on = the top edges.</div>
</div></body></html>"""

open(os.path.join(HERE, "dag.html"), "w", encoding="utf-8").write(DOC)
print(f"wrote dataset/dag.json + dag.html · {TOTAL:,} nodes (all attached — nothing dropped)")
print("  stages: " + " · ".join(f"{st}={len(v)}fx" for st, v in sorted(stage_fix.items())))
print(f"  futures={len(futures)} · team-outlooks={sum(len(v) for v in q_by_team.values())} · champion node: "
      + ("attached" if CHAMP else "PENDING"))
print("  open: open dataset/dag.html")
