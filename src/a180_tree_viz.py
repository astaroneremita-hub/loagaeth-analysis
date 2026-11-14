# -*- coding: utf-8 -*-
"""
a180 — Gera viz/dinastias.html: arvore/grafo genealogico dos 90 nomes.
Casas em clusters, arestas edicao-1, casamento NOCHA x CHASTOR destacado. Layout estatico.
"""
import json, re, os, math, itertools, collections
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w): return re.sub(r"[^a-z]","",str(w).lower())
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=sorted(set(norm(n) for n in fg["real_names"]))
ROOTS=[r.lower() for r in fg["roots"]]
def roots_of(n): return [r for r in ROOTS if r in n]

# casa primaria: se 2 raizes e {nocha,chastor} -> ponte; senao raiz mais longa; senao avulso
def house(n):
    rs=roots_of(n)
    if set(["nocha","chastor"]).issubset(set(rs)): return "PONTE"
    if rs: return max(rs,key=len).upper()
    return "AVULSO"
H=collections.defaultdict(list)
for n in NAMES: H[house(n)].append(n)

def ed1(a,b):
    if a==b: return False
    la,lb=len(a),len(b)
    if abs(la-lb)>1: return False
    if la==lb: return sum(x!=y for x,y in zip(a,b))==1
    if la>lb: a,b=b,a;la,lb=lb,la
    i=j=d=0
    while i<la and j<lb:
        if a[i]==b[j]: i+=1;j+=1
        else: d+=1;j+=1
        if d>1: return False
    return True
edges=[(a,b) for a,b in itertools.combinations(NAMES,2) if ed1(a,b)]

# layout: cada casa num retangulo; membros em aneis; raiz (nome=raiz) no centro
W,Hc=1040,860
cells={
 "NOCHA":(250,250,175),"CHASTOR":(790,250,175),"PONTE":(520,250,120),
 "NACHO":(140,560,110),"CHADAX":(340,560,95),"GETH":(520,560,95),
 "ACLAX":(690,560,85),"GRADAX":(835,560,70),"ANTANTOX":(940,560,70),
 "ANZACH":(940,700,55),"PHANGE":(140,700,55),"AVULSO":(520,770,250),
}
pos={}
for hk,members in H.items():
    if hk not in cells: continue
    cx,cy,R=cells[hk]
    root=hk.lower()
    center=[m for m in members if m==root]
    ring=[m for m in members if m!=root]
    if center: pos[center[0]]=(cx,cy)
    k=len(ring)
    if hk=="AVULSO":  # nuvem em grade
        cols=6
        for i,m in enumerate(ring+center):
            r=i//cols; c=i%cols
            pos[m]=(cx-220+c*90, cy-20+r*34)
    else:
        for i,m in enumerate(ring):
            ang=2*math.pi*i/max(k,1)-math.pi/2
            rr=R*(0.62 if k>8 and i%2 else 0.95)
            pos[m]=(cx+rr*math.cos(ang), cy+rr*math.sin(ang))
# qualquer nome sem pos (ex PONTE root inexistente) ja coberto

COL={"NOCHA":"#5bb3e0","CHASTOR":"#9b6be0","PONTE":"#e0573b","NACHO":"#3d6bd6",
 "CHADAX":"#49b67b","GETH":"#c9a24b","ACLAX":"#d06ba0","GRADAX":"#b5651d",
 "ANTANTOX":"#7a8696","ANZACH":"#e0a13b","PHANGE":"#6bd0c0","AVULSO":"#5b6672"}
hof={m:hk for hk,ms in H.items() for m in ms}

svg=[f'<svg id="dsvg" viewBox="0 0 {W} {Hc}" xmlns="http://www.w3.org/2000/svg"><g id="vp">']
# halos das casas
for hk,(cx,cy,R) in cells.items():
    if hk in ("AVULSO",): continue
    svg.append(f'<circle cx="{cx}" cy="{cy}" r="{R+18}" fill="{COL[hk]}" opacity="0.07"/>')
    svg.append(f'<text x="{cx}" y="{cy-R-6}" text-anchor="middle" fill="{COL[hk]}" font-size="13" font-weight="700">{hk} ({len(H[hk])})</text>')
svg.append(f'<text x="520" y="640" text-anchor="middle" fill="{COL["AVULSO"]}" font-size="13" font-weight="700">AVULSOS / sem raiz ({len(H["AVULSO"])})</text>')
# arestas
for a,b in edges:
    if a in pos and b in pos:
        bridge = hof.get(a)=="PONTE" or hof.get(b)=="PONTE"
        (x1,y1),(x2,y2)=pos[a],pos[b]
        svg.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{"#e0573b" if bridge else "#3a424e"}" stroke-width="{1.4 if bridge else 0.8}" opacity="{0.9 if bridge else 0.6}"/>')
# linhas de casamento: PONTE -> raiz NOCHA e CHASTOR
for p in H["PONTE"]:
    for r in ("nocha","chastor"):
        if p in pos and r in pos:
            (x1,y1),(x2,y2)=pos[p],pos[r]
            svg.append(f'<line x1="{x1:.0f}" y1="{y1:.0f}" x2="{x2:.0f}" y2="{y2:.0f}" stroke="#e0573b" stroke-width="1" stroke-dasharray="3 3" opacity="0.7"/>')
# nos
for m,(x,y) in pos.items():
    c=COL[hof.get(m,"AVULSO")]
    isroot = m==hof.get(m,"").lower()
    svg.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{4.5 if isroot else 3}" fill="{c}" stroke="#0e1116" stroke-width="0.6"/>')
    svg.append(f'<text x="{x:.0f}" y="{y-6:.0f}" text-anchor="middle" fill="#c7d0da" font-size="8">{m}</text>')
svg.append('</g></svg>')

html=f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Dinastias do Loagaeth</title>
<style>:root{{--bg:#0e1116;--ink:#e6edf3;--mut:#8b97a7;--line:#2a313c}}
body{{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 system-ui,Segoe UI,Roboto,Arial;padding:16px}}
h1{{font-size:20px;margin:0 0 2px}} .sub{{color:var(--mut);font-size:13px;margin:0 0 12px}}
.wrap{{background:#121820;border:1px solid var(--line);border-radius:12px;padding:8px}}
svg{{width:100%;height:80vh;display:block;cursor:grab;touch-action:none}} svg:active{{cursor:grabbing}} text{{font-family:ui-monospace,Menlo,Consolas,monospace}}
.ctrls{{margin:8px 0 0}} .ctrls button{{background:#1b2634;border:1px solid #2c3a4e;color:var(--ink);border-radius:6px;padding:3px 10px;font-size:12px;cursor:pointer}}
.note{{color:var(--mut);font-size:12px;border-left:3px solid var(--line);padding-left:10px;margin-top:12px}}</style></head>
<body><h1>Dinastias do Loagaeth · genealogia dos 90 nomes</h1>
<p class="sub">Casas por raiz · arestas = edição-1 · vermelho = casamento NOCHA×CHASTOR → NOCHASTOR. · <b>roda = zoom · arraste = mover · 2 cliques = reset</b></p>
<div class="ctrls"><button id="zin">+</button> <button id="zout">−</button> <button id="zreset">reset</button></div>
<div class="wrap">{''.join(svg)}</div>
<p class="note">Famílias reais (z=+229.6, #344). Contagem = casa <b>primária</b>; os compostos NOCHA+CHASTOR saem para a PONTE, então por raiz NOCHA=19 e CHASTOR=18 (#344). Ponto maior = a raiz-nome da casa. AVULSOS = 24 nomes sem raiz das 10 casas.</p>
<script>
(function(){{var svg=document.getElementById('dsvg'),vp=document.getElementById('vp');
var s=1,tx=0,ty=0,drag=false,lx=0,ly=0;
function apply(){{vp.setAttribute('transform','translate('+tx+' '+ty+') scale('+s+')');}}
function zoomAt(cx,cy,f){{var ns=Math.min(12,Math.max(0.3,s*f));var r=svg.getBoundingClientRect();
 var vb=svg.viewBox.baseVal;var px=(cx-r.left)/r.width*vb.width,py=(cy-r.top)/r.height*vb.height;
 tx=px-(px-tx)*(ns/s);ty=py-(py-ty)*(ns/s);s=ns;apply();}}
svg.addEventListener('wheel',function(e){{e.preventDefault();zoomAt(e.clientX,e.clientY,e.deltaY<0?1.15:1/1.15);}},{{passive:false}});
svg.addEventListener('mousedown',function(e){{drag=true;lx=e.clientX;ly=e.clientY;}});
window.addEventListener('mousemove',function(e){{if(!drag)return;var r=svg.getBoundingClientRect();var vb=svg.viewBox.baseVal;
 tx+=(e.clientX-lx)/r.width*vb.width;ty+=(e.clientY-ly)/r.height*vb.height;lx=e.clientX;ly=e.clientY;apply();}});
window.addEventListener('mouseup',function(){{drag=false;}});
svg.addEventListener('dblclick',function(){{s=1;tx=0;ty=0;apply();}});
document.getElementById('zin').onclick=function(){{var r=svg.getBoundingClientRect();zoomAt(r.left+r.width/2,r.top+r.height/2,1.25);}};
document.getElementById('zout').onclick=function(){{var r=svg.getBoundingClientRect();zoomAt(r.left+r.width/2,r.top+r.height/2,1/1.25);}};
document.getElementById('zreset').onclick=function(){{s=1;tx=0;ty=0;apply();}};
}})();
</script>
</body></html>"""
open(os.path.join(ROOT,"viz","dinastias.html"),"w",encoding="utf-8").write(html)
print("escrito viz/dinastias.html |", len(pos),"nos,",len(edges),"arestas")
