# -*- coding: utf-8 -*-
"""
a171 — O gerador de nomes como GRAMATICA explicita: PREFIXO? RAIZ SUFIXO*.
Parseia os 90 nomes nos slots; mede se poucas regras explicam todos (vs null),
e se ha RESTRICAO de combinacao raiz x afixo (morfologia real tem selecao). seed 1583.
"""
import json, re, os, random, collections, math, itertools
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower()
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=[norm(n) for n in fg["real_names"]]
PREF=sorted((p.lower() for p in fg["prefixes"]),key=len,reverse=True)
SUFF=sorted((s.lower() for s in fg["suffixes"]),key=len,reverse=True)
RTS =sorted((r.lower() for r in fg["roots"]),key=len,reverse=True)

def parse(n):
    """PREFIXO? RAIZ SUFIXO* ; retorna (pref,root,[suf],leftover_letters)."""
    best=None
    for p in [""]+PREF:
        if not n.startswith(p): continue
        i=len(p)
        for r in RTS:
            if n[i:].startswith(r):
                j=i+len(r); sufs=[]
                while j<len(n):
                    hit=None
                    for s in SUFF:
                        if n[j:].startswith(s): hit=s; break
                    if hit: sufs.append(hit); j+=len(hit)
                    else: break
                leftover=len(n)-j
                cand=(p,r,sufs,leftover)
                # prefere menor leftover, depois menos sufixos
                if best is None or (leftover,len(sufs))<(best[3],len(best[2])):
                    best=cand
    return best

parses=[(n,parse(n)) for n in NAMES]
full=[(n,pr) for n,pr in parses if pr and pr[3]==0]
print(f"{len(full)}/{len(NAMES)} nomes parseiam 100% em PREFIXO? RAIZ SUFIXO*")

usedP=collections.Counter(); usedR=collections.Counter(); usedS=collections.Counter()
pairs=collections.Counter()  # (root, suffix1)
for n,pr in full:
    p,r,sufs,_=pr
    usedP[p]+=1; usedR[r]+=1
    for s in sufs: usedS[s]+=1
    pairs[(r, sufs[0] if sufs else "∅")]+=1

print(f"\nSlots realizados: prefixos={len([k for k in usedP if k])}  raizes={len(usedR)}  sufixos={len(usedS)}")
print("raizes:", dict(usedR.most_common()))
print("prefixos:", {k:v for k,v in usedP.most_common() if k})
print("sufixos:", dict(usedS.most_common()))

# MDL / compressao: letras cruas vs tamanho do inventario
raw=sum(len(n) for n in NAMES)
inv=sum(len(x) for x in set(usedP)|set(usedR)|set(usedS) if x)
inv=sum(len(x) for x in (set(usedP)|set(usedR)|set(usedS)) if x)
print(f"MDL: {raw} letras cruas  |  inventario de pecas = {inv} letras  (razao {raw/inv:.1f}x)")

# ---- NULL: nomes aleatorios mesma distribuicao tamanho/letras ----
letpool="".join(NAMES); sizes=[len(n) for n in NAMES]
NT=2000; nullfull=[]
for _ in range(NT):
    rn=["".join(random.choice(letpool) for _ in range(s)) for s in sizes]
    c=sum(1 for n in rn if (pr:=parse(n)) and pr[3]==0)
    nullfull.append(c)
mu=sum(nullfull)/NT; sd=(sum((x-mu)**2 for x in nullfull)/NT)**.5
z=(len(full)-mu)/sd if sd else 0
print(f"\nNULL parse-100%: {mu:.1f}/{len(NAMES)}  (real {len(full)})  z={z:+.1f}")

# ---- RESTRICAO raiz x sufixo: H(suf|root) vs shuffle dos rotulos de raiz ----
def cond_entropy(pr_list):
    byroot=collections.defaultdict(collections.Counter)
    for _,pr in pr_list:
        r=pr[1]; s=pr[2][0] if pr[2] else "∅"; byroot[r][s]+=1
    tot=sum(sum(c.values()) for c in byroot.values()); H=0
    for r,c in byroot.items():
        pr_r=sum(c.values())/tot
        for s,n in c.items():
            p=n/sum(c.values()); H-=pr_r*p*math.log2(p)
    return H
Hreal=cond_entropy(full)
roots=[pr[1] for _,pr in full]; sufs=[(pr[2][0] if pr[2] else "∅") for _,pr in full]
nullH=[]
for _ in range(NT):
    sh=roots[:]; random.shuffle(sh)
    fake=[(None,(None,sh[i],[sufs[i]] if sufs[i]!="∅" else [],0)) for i in range(len(full))]
    nullH.append(cond_entropy(fake))
muH=sum(nullH)/NT; sdH=(sum((x-muH)**2 for x in nullH)/NT)**.5
zH=(Hreal-muH)/sdH if sdH else 0
print(f"H(sufixo|raiz) real={Hreal:.3f} bits  null(shuffle)={muH:.3f}  z={zH:+.1f}  "
      f"({'RESTRICAO' if zH<-2 else 'sem restricao'})")

# matriz raiz x 1o-sufixo
print("\nraiz -> sufixos usados:")
m=collections.defaultdict(collections.Counter)
for _,pr in full: m[pr[1]][pr[2][0] if pr[2] else "∅"]+=1
for r in sorted(m,key=lambda r:-sum(m[r].values())):
    print(f"  {r:<10} {dict(m[r])}")

json.dump({"parse_full":len(full),"n":len(NAMES),"null_mu":round(mu,1),"z_parse":round(z,1),
  "roots_used":dict(usedR),"prefixes_used":{k:v for k,v in usedP.items() if k},
  "suffixes_used":dict(usedS),"mdl_ratio":round(raw/inv,1),
  "H_suf_given_root":round(Hreal,3),"H_null":round(muH,3),"z_H":round(zH,1)},
  open(os.path.join(ROOT,"results","171_name_grammar.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/171_name_grammar.json")
