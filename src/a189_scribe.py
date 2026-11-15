# -*- coding: utf-8 -*-
"""
a189 — Assinatura de 'escriba/seção' por folha (#2). Perfil de bigramas de letra por folha;
distância entre folhas consecutivas (achar emendas/mudanças de mão); o livro é um contínuo
ou tem blocos? Independente dos nomes. seed 1583.
"""
import json,re,math,os,random,collections,unicodedata
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w="".join(c for c in unicodedata.normalize("NFD",str(w)) if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z]","",w.lower())
grd=json.load(open(ROOT+r"\engine\data\loagaeth_grades_simples.json",encoding="utf-8"))
def folha_text(f):
    s=[]
    for side in "ab":
        k=f"{f}{side}"
        if k in grd: s+=[norm(x) for x in grd[k]]
    return "#".join(x for x in s if x)
folhas=sorted(set(int(re.match(r"(\d+)",k).group(1)) for k in grd if k and k[0].isdigit()))
def bigram(s):
    c=collections.Counter()
    for i in range(len(s)-1):
        if s[i]!="#" and s[i+1]!="#": c[s[i:i+2]]+=1
    t=sum(c.values()) or 1
    return {k:v/t for k,v in c.items()}
def cos(a,b):
    ks=set(a)|set(b); d=sum(a.get(k,0)*b.get(k,0) for k in ks)
    na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return d/(na*nb) if na and nb else 0
prof={f:bigram(folha_text(f)) for f in folhas}
# distancia entre folhas consecutivas
print("distância entre folhas consecutivas (1-cos); emendas = picos:")
dists=[]
for i in range(len(folhas)-1):
    d=1-cos(prof[folhas[i]],prof[folhas[i+1]]); dists.append((folhas[i],folhas[i+1],d))
mu=sum(d for _,_,d in dists)/len(dists); sd=(sum((d-mu)**2 for _,_,d in dists)/len(dists))**.5
seams=[(a,b,d) for a,b,d in dists if d>mu+1.6*sd]
print(f"  média {mu:.3f} dp {sd:.3f}")
print("  EMENDAS (salto > média+1.6dp):", ", ".join(f"{a}|{b}({d:.2f})" for a,b,d in seams) or "nenhuma")
# contínuo vs blocos: correlação distância-de-perfil x distância-de-folha
import itertools
xs=[];ys=[]
for i,j in itertools.combinations(range(len(folhas)),2):
    xs.append(abs(folhas[i]-folhas[j])); ys.append(1-cos(prof[folhas[i]],prof[folhas[j]]))
n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
r=sum((xs[k]-mx)*(ys[k]-my) for k in range(n))/((sum((x-mx)**2 for x in xs)*sum((y-my)**2 for y in ys))**.5)
print(f"\nCorrelação distância-no-livro × dissimilaridade de perfil: r={r:+.2f}")
print("  (r>0 forte = contínuo/gradiente; r~0 = blocos ou aleatório)")
# null: embaralhar a ordem das folhas e ver se os saltos somem
def seam_count(order):
    ds=[1-cos(prof[order[i]],prof[order[i+1]]) for i in range(len(order)-1)]
    m=sum(ds)/len(ds); s=(sum((x-m)**2 for x in ds)/len(ds))**.5
    return sum(1 for x in ds if x>m+1.6*s)
real_sc=len(seams); nul=[]
for _ in range(2000):
    o=folhas[:]; random.shuffle(o); nul.append(seam_count(o))
mun=sum(nul)/len(nul)
print(f"\nnº de emendas: real {real_sc} | null(ordem embaralhada) {mun:.1f}")
PY=0
