# -*- coding: utf-8 -*-
"""
a173 — CAMADA DE SELECAO: o gerador (#335) produz ~1100 nomes possiveis, so ~90 sao
reais. O que filtra? Separa os REAIS dos gerados-mas-nao-reais e procura o discriminador:
fonotatica, tamanho, ou recorrencia na grade. Se nenhuma regra separa, a selecao e
geometrica (posicao na tabela), nao linguistica. seed 1583.
"""
import json, re, os, random, collections, itertools
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=str(w).lower()
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
REAL=set(norm(n) for n in fg["real_names"])
PREF=[p.lower() for p in fg["prefixes"]]
RTS =[r.lower() for r in fg["roots"]]
SUF =[s.lower() for s in fg["suffixes"]]
VOW=set("aeiou")

# candidatos: PREFIXO? RAIZ SUFIXO{0,1}
cand=set()
for p in [""]+PREF:
    for r in RTS:
        for s in [""]+SUF:
            cand.add(p+r+s)
realcand = cand & REAL
noncand  = cand - REAL
print(f"candidatos gerados={len(cand)}  reais entre eles={len(realcand)}  nao-reais={len(noncand)}")
print(f"(reais totais={len(REAL)}; {len(REAL-cand)} reais NAO sao gerados por PREF?+RAIZ+SUF<=1)\n")

# livro inteiro (row letras)
grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
faces=[k for k in grd if k and k[0].isdigit()]
lines=[norm(ln) for k in faces for ln in grd[k] if norm(ln)]
def subcount(w):  # em quantas linhas aparece
    return sum(1 for s in lines if w in s)

# poder: reais sao row-substring?
real_hit=sum(1 for n in REAL if subcount(n)>0)
print(f"PODER: {real_hit}/{len(REAL)} nomes reais aparecem como substring de linha no livro")

# metricas fonotaticas
def maxrun(w,s):  # maior sequencia de chars em s
    best=cur=0
    for ch in w:
        if ch in s: cur+=1; best=max(best,cur)
        else: cur=0
    return best
def feats(w):
    return {"len":len(w),"vmax":maxrun(w,VOW),
            "cmax":maxrun(w,set("bcdfghlmnpqrstxz")),
            "viol": (1 if maxrun(w,VOW)>2 else 0)+(1 if maxrun(w,set("bcdfghlmnpqrstxz"))>3 else 0)}

def meanf(S,key):
    v=[feats(w)[key] for w in S]; return sum(v)/len(v) if v else 0

print("\nDiscriminador real vs nao-real (media):")
rows=[]
for key in ("len","vmax","cmax","viol"):
    mr=meanf(realcand,key); mn=meanf(noncand,key)
    # permutacao: embaralha rotulos
    pool=list(realcand)+list(noncand); nr=len(realcand)
    diffs=[]
    for _ in range(2000):
        random.shuffle(pool)
        a=pool[:nr]; b=pool[nr:]
        diffs.append(meanf(a,key)-meanf(b,key))
    mu=sum(diffs)/len(diffs); sd=(sum((x-mu)**2 for x in diffs)/len(diffs))**.5
    z=((mr-mn)-mu)/sd if sd else 0
    print(f"  {key:<5} real={mr:.2f}  nao-real={mn:.2f}  z={z:+.1f}")
    rows.append((key,round(mr,2),round(mn,2),round(z,1)))

# recorrencia na grade: real vs nao-real (so candidatos >=5 letras p/ reduzir acaso)
rr=[subcount(w) for w in realcand if len(w)>=5]
nn=[subcount(w) for w in noncand if len(w)>=5]
mr=sum(rr)/len(rr) if rr else 0; mn=sum(nn)/len(nn) if nn else 0
pool=[(w,1) for w in realcand if len(w)>=5]+[(w,0) for w in noncand if len(w)>=5]
sc={w:subcount(w) for w,_ in pool}; nr=sum(1 for _,l in pool if l)
diffs=[]
for _ in range(2000):
    random.shuffle(pool)
    a=[sc[w] for w,_ in pool[:nr]]; b=[sc[w] for w,_ in pool[nr:]]
    diffs.append(sum(a)/len(a)-sum(b)/len(b))
mu=sum(diffs)/len(diffs); sd=(sum((x-mu)**2 for x in diffs)/len(diffs))**.5
zr=((mr-mn)-mu)/sd if sd else 0
print(f"\nRecorrencia(linhas) >=5letras: real={mr:.2f}  nao-real={mn:.2f}  z={zr:+.1f}")

res={"cand":len(cand),"real_in_cand":len(realcand),"real_rowhit":real_hit,"real_total":len(REAL),
     "feat_z":rows,"recur_real":round(mr,2),"recur_nonreal":round(mn,2),"recur_z":round(zr,1)}
json.dump(res,open(os.path.join(ROOT,"results","173_selection.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/173_selection.json")
