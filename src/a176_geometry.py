# -*- coding: utf-8 -*-
"""
a176 — Qual GEOMETRIA concentra a recorrencia dos nomes? (#337 achou: seleciona por
recorrencia; aqui: em QUE direcao de leitura). Le cada face quadrada 49x49 em
ROW / COL / DIAG-descendente / DIAG-ascendente / BORDA (ida+volta) e conta em quantas
faces cada um dos 90 nomes aparece, por direcao, vs null pareado. seed 1583.
"""
import json, re, os, random
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=str(w).lower()
    for a,b in [("áàäâ","a"),("éèê","e"),("íìî","i"),("óòô","o"),("úùû","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=[norm(n) for n in fg["real_names"]]
grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))

# faces quadradas 49x49 (grades 2-48); cada celula = 1 letra
faces=[]
for k in grd:
    if k and k[0].isdigit() and k not in ("1a","1b"):
        rows=[norm(r) for r in grd[k]]
        if len(rows)==49 and all(len(r)==49 for r in rows):
            faces.append((k,rows))
print(f"faces quadradas 49x49: {len(faces)}")

def directions(rows):
    N=len(rows)
    row=rows[:]
    col=["".join(rows[r][c] for r in range(N)) for c in range(N)]
    dr=[]  # diagonais r-c const (descendente)
    for d in range(-N+1,N):
        s="".join(rows[r][r-d] for r in range(N) if 0<=r-d<N)
        if len(s)>=2: dr.append(s)
    dl=[]  # antidiagonais r+c const (ascendente)
    for d in range(2*N-1):
        s="".join(rows[r][d-r] for r in range(N) if 0<=d-r<N)
        if len(s)>=2: dl.append(s)
    top=rows[0]; bot=rows[N-1][::-1]
    right="".join(rows[r][N-1] for r in range(N))
    left="".join(rows[r][0] for r in range(N))[::-1]
    border=[top+right+bot+left]
    return {"ROW":row,"COL":col,"DIAG_desc":dr,"DIAG_asc":dl,"BORDA":border}

# pre-computa texto juntado (fwd+rev) por face/direcao
BIG={d:[] for d in ("ROW","COL","DIAG_desc","DIAG_asc","BORDA")}
for k,rows in faces:
    dd=directions(rows)
    for d,strs in dd.items():
        f="#".join(strs); r="#".join(s[::-1] for s in strs)
        BIG[d].append(f+"@"+r)
def recur(name,d):  # em quantas faces aparece nessa direcao (ida ou volta)
    return sum(1 for txt in BIG[d] if name in txt)

letpool="".join(r for _,rows in faces for r in rows)
def randname(n): return "".join(random.choice(letpool) for _ in n)

print("\nRecorrencia dos 90 nomes por direcao (soma de faces-hit) vs null:\n")
import statistics
res={}
for d in ("ROW","COL","DIAG_desc","DIAG_asc","BORDA"):
    real=sum(recur(n,d) for n in NAMES)
    nul=[]
    for _ in range(300):
        nul.append(sum(recur(randname(n),d) for n in NAMES))
    mu=sum(nul)/len(nul); sd=(sum((x-mu)**2 for x in nul)/len(nul))**.5
    z=(real-mu)/sd if sd else 0
    per=real/len(NAMES)
    print(f"  {d:<10} total={real:>5}  (~{per:.1f} faces/nome)  null={mu:6.1f}  z={z:+.1f}")
    res[d]={"total":real,"por_nome":round(per,1),"null":round(mu,1),"z":round(z,1)}
json.dump(res,open(os.path.join(ROOT,"results","176_geometry.json"),"w"),ensure_ascii=False,indent=1)
best=max(res,key=lambda d:res[d]["z"])
print(f"\ngeometria dominante: {best} (z={res[best]['z']:+.1f})")
print("saved results/176_geometry.json")
