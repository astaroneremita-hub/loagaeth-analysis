# -*- coding: utf-8 -*-
"""
a181 — Dados do Atlas dos Nomes. Para cada nome real: onde aparece no livro (folhas,
pico, recorrencia) por linha+diagonal, elemento dominante, esqueleto. Tambem embute o
mapa de letras (elemento) e o gradiente por folha. Gera results/181_atlas.json.
"""
import json, re, os, collections
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=str(w).lower()
    for a,b in [("áàäâ","a"),("éèê","e"),("íìî","i"),("óòô","o"),("úùû","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=sorted(set(norm(n) for n in fg["real_names"]))
LET=fg["letters"]; ELEM=["Fogo","Terra","Ar","Agua"]
grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))

def face(key):
    if key not in grd: return None
    rows=[norm(r) for r in grd[key]]
    if len(rows)==49 and all(len(r)==49 for r in rows): return rows
    return None
def diag_texts(rows):
    N=len(rows); out=[]
    for d in range(-N+1,N):
        s="".join(rows[r][r-d] for r in range(N) if 0<=r-d<N)
        if len(s)>=2: out.append(s)
    return out

# por folha: textos de linha (todas) + diagonais (so 26-28, que sao diagonais)
folha_lines={}; folha_diag={}
for f in range(1,49):
    L=[]; D=[]
    for side in "ab":
        k=f"{f}{side}"
        if k in grd:
            L+=[norm(x) for x in grd[k]]
            rows=face(k)
            if rows and f in (26,27,28): D+=diag_texts(rows)
    folha_lines[f]=[s for s in L if s]; folha_diag[f]=D

def elem_dom(n):
    c=collections.Counter()
    for ch in n.upper():
        if ch in LET and LET[ch]["e"] in ELEM: c[LET[ch]["e"]]+=1
    return c.most_common(1)[0][0] if c else "?"

names_out=[]
for n in NAMES:
    per={}
    for f in range(1,49):
        cnt=sum(s.count(n) for s in folha_lines[f])+sum(s.count(n) for s in folha_diag[f])
        if cnt: per[f]=cnt
    occ=sum(per.values()); peak=max(per,key=per.get) if per else 0
    names_out.append({"n":n,"occ":occ,"peak":peak,"folhas":sorted(per),
                      "elem":elem_dom(n)})

# gradiente por folha (de 177)
sweep=json.load(open(os.path.join(ROOT,"results","177_sweep.json"),encoding="utf-8"))
grad=[{"f":r["folha"],"elem":r["elem"],"occ":r["occ"]} for r in sweep]

out={"letters":{k:LET[k]["e"] for k in LET},
     "elems":ELEM,
     "names":names_out,
     "gradient":grad,
     "roots":[r.lower() for r in fg["roots"]],
     "prefixes":[p.lower() for p in fg["prefixes"]],
     "suffixes":[s.lower() for s in fg["suffixes"]]}
json.dump(out,open(os.path.join(ROOT,"results","181_atlas.json"),"w"),ensure_ascii=False,separators=(",",":"))
tot=sum(x["occ"] for x in names_out); haspos=sum(1 for x in names_out if x["peak"])
print(f"{len(names_out)} nomes enriquecidos, {haspos} com posicao no livro, occ total {tot}")
print("ex:", json.dumps(names_out[0],ensure_ascii=False))
print("saved results/181_atlas.json")
