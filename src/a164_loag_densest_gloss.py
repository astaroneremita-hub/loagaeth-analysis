# -*- coding: utf-8 -*-
"""
a164 — Qual trecho da FOLHA 1 do Loag tem mais palavras-com-traducao juntas?
Nao prova sintaxe (#332 = ordem nao carrega info). So localiza o span mais 'legivel'
lendo as glosas das Chamadas onde existirem. Rotulo honesto: leitura literal, nao gramatica.
"""
import json, re, os
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

d=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
gloss={}
for c in d["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        gl=(p.get("ingles_sl3191") or "").strip()
        # descarta glosas que sao so numero/pontuacao
        if len(k)>=2 and gl and not re.fullmatch(r"[\d:.\- ]+", gl):
            gloss.setdefault(k, gl)

g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
lines=[]
for key in ("1a","1b"):
    for ln in g[key]:
        raw=ln.split()
        lines.append([(w, norm(w)) for w in raw if len(norm(w))>=1])

# densidade por linha: fracao de tokens com gloss
best=[]
for li,ln in enumerate(lines):
    hits=[(w,gloss.get(n)) for (w,n) in ln if gloss.get(n)]
    tot=len([1 for (w,n) in ln if len(n)>=2])
    if tot>=4:
        best.append((len(hits)/tot, len(hits), li, ln))
best.sort(reverse=True)

print("TOP 5 linhas mais densas em palavras-com-traducao:\n")
for frac,nh,li,ln in best[:5]:
    key = "1a" if li<49 else "1b"; row = li if li<49 else li-49
    print(f"--- {key} linha {row}  ({nh} glosadas / {len([1 for w,n in ln if len(n)>=2])} palavras = {frac*100:.0f}%) ---")
    print("  cru: "+" ".join(w for w,n in ln))
    out=[]
    for w,n in ln:
        g2=gloss.get(n)
        out.append(f"[{w}={g2}]" if g2 else w)
    print("  lido:"+" ".join(out)); print()

# melhor JANELA contigua (>=3 glosadas dentro de 6 palavras)
print("MELHOR JANELA contigua de glosadas:")
bestwin=None
for li,ln in enumerate(lines):
    toks=[(w,gloss.get(n)) for (w,n) in ln]
    for i in range(len(toks)):
        for L in (3,4,5,6):
            win=toks[i:i+L]
            if len(win)<3: continue
            ng=sum(1 for w,g2 in win if g2)
            dens=ng/len(win)
            if ng>=3 and (bestwin is None or (ng,dens)>(bestwin[0],bestwin[1])):
                bestwin=(ng,dens,li,i,win)
if bestwin:
    ng,dens,li,i,win=bestwin
    key="1a" if li<49 else "1b"; row=li if li<49 else li-49
    print(f"  {key} linha {row} ({ng} glosadas em {len(win)} palavras)")
    print("  cru: "+" ".join(w for w,g2 in win))
    print("  lido:"+" ".join(f"[{w}={g2}]" if g2 else w for w,g2 in win))
