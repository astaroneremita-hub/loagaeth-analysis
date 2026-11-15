# -*- coding: utf-8 -*-
"""
a188 — Novas leituras das grades (#21-26): espiral, bustrófedon, sub-blocos 7×7, acróstico
(coluna 0), telestich (coluna 48). Conta recorrência dos 90 nomes por leitura vs null. seed 1583.
"""
import json,re,os,random,unicodedata
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w="".join(c for c in unicodedata.normalize("NFD",str(w)) if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z]","",w.lower())
fg=json.load(open(ROOT+r"\viz\forge_grammar.json",encoding="utf-8"))
NAMES=sorted(set(norm(n) for n in fg["real_names"]),key=len,reverse=True)
grd=json.load(open(ROOT+r"\engine\data\loagaeth_grades_simples.json",encoding="utf-8"))
faces=[]
for k in grd:
    if k and k[0].isdigit() and k not in ("1a","1b"):
        rows=[norm(r) for r in grd[k]]
        if len(rows)==49 and all(len(r)==49 for r in rows): faces.append(rows)
N=49
def spiral(g):
    t,b,l,r=0,N-1,0,N-1; out=[]
    while t<=b and l<=r:
        for c in range(l,r+1): out.append(g[t][c])
        t+=1
        for rr in range(t,b+1): out.append(g[rr][r])
        r-=1
        if t<=b:
            for c in range(r,l-1,-1): out.append(g[b][c]);
            b-=1
        if l<=r:
            for rr in range(b,t-1,-1): out.append(g[rr][l])
            l+=1
    return "".join(out)
def boustro(g):
    out=[]
    for i,row in enumerate(g): out.append(row if i%2==0 else row[::-1])
    return "".join(out)
def blocks7(g):
    s=[]
    for bi in range(7):
        for bj in range(7):
            s.append("".join(g[bi*7+r][bj*7+c] for r in range(7) for c in range(7)))
    return s
def col(g,c): return "".join(g[r][c] for r in range(N))

def texts(g,kind):
    if kind=="SPIRAL": return [spiral(g)]
    if kind=="BOUSTRO": return [boustro(g)]
    if kind=="BLOCOS7": return blocks7(g)
    if kind=="ACROSTICO": return [col(g,0)]
    if kind=="TELESTICH": return [col(g,N-1)]
    return []
KINDS=["SPIRAL","BOUSTRO","BLOCOS7","ACROSTICO","TELESTICH"]
BIG={k:[] for k in KINDS}
for g in faces:
    for k in KINDS:
        BIG[k].append("#".join(texts(g,k)+[t[::-1] for t in texts(g,k)]))
def recur(name,k): return sum(1 for txt in BIG[k] if name in txt)
letpool="".join(r for g in faces for r in g)
def rnd(n): return "".join(random.choice(letpool) for _ in n)
print(f"faces {len(faces)}\n{'leitura':<11}{'total':>7}{'/nome':>7}{'null':>7}{'z':>7}")
for k in KINDS:
    real=sum(recur(n,k) for n in NAMES)
    nul=[sum(recur(rnd(n),k) for n in NAMES) for _ in range(200)]
    mu=sum(nul)/len(nul); sd=(sum((x-mu)**2 for x in nul)/len(nul))**.5 or 1
    print(f"{k:<11}{real:>7}{real/len(NAMES):>7.1f}{mu:>7.1f}{(real-mu)/sd:>+7.1f}")
