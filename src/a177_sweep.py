# -*- coding: utf-8 -*-
"""
a177 — Varredura das grades 2-48 (livro inteiro). Por folha, lido em LINHA (#341):
densidade dos 90 nomes, cobertura pelas pecas do gerador, camada de lexico (Chamadas),
perfil elemental (gradiente) e raizes dominantes. Mapa do Loag inteiro. seed 1583.
"""
import json, re, os, random, collections
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=str(w).lower()
    for a,b in [("áàäâ","a"),("éèê","e"),("íìî","i"),("óòô","o"),("úùû","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=[norm(n) for n in fg["real_names"]]
ROOTS=[r.lower() for r in fg["roots"]]
AFF=[a.lower() for a in fg["prefixes"]+fg["suffixes"]]
LET=fg["letters"]; ELEM=["Fogo","Terra","Ar","Agua"]
CH=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
CALL=set()
for c in CH["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        if len(k)>=4: CALL.add(k)
grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))

# peca-inventario p/ tiling: particulas da folha1 + afixos + raizes
f1=[]
for k in ("1a","1b"):
    for ln in grd[k]: f1+=[norm(w) for w in ln.split()]
F1=collections.Counter(t for t in f1 if len(t)>=2)
glosskeys=set(norm(p.get("chave") or "") for c in CH["chamadas"] for p in c["palavras"])
B=[w for w in F1 if w not in glosskeys and len(w)<=3 and F1[w]>=2]
V=sorted(set(w for w in B+AFF+ROOTS if len(w)>=2),key=len,reverse=True)
maxL=max(len(v) for v in V)
def tilecov(s):
    i=0;cov=0
    while i<len(s):
        m=None
        for L in range(min(maxL,len(s)-i),1,-1):
            if s[i:i+L] in Vset: m=L;break
        if m: cov+=m;i+=m
        else: i+=1
    return cov
Vset=set(V)

def folha_text(f):
    t=[]
    for side in "ab":
        k=f"{f}{side}"
        if k in grd: t+=[norm(ln) for ln in grd[k]]
    return [s for s in t if s]

folhas=sorted(set(int(re.match(r"(\d+)",k).group(1)) for k in grd if k and k[0].isdigit()))
letpool="".join(s for f in folhas for s in folha_text(f))
def randnames(): return ["".join(random.choice(letpool) for _ in n) for n in NAMES]

rows=[]
for f in folhas:
    lines=folha_text(f); txt="#".join(lines); L=len(txt.replace("#",""))
    if L<50:
        rows.append((f,L,0,0,0,0,None)); continue
    namehit=sum(1 for n in NAMES if n in txt)
    nameocc=sum(txt.count(n) for n in NAMES)
    callhit=sum(1 for w in CALL if w in txt)
    cov=sum(tilecov(s) for s in lines)/L
    ec=collections.Counter()
    for s in lines:
        for ch in s.upper():
            if ch in LET and LET[ch]["e"] in ELEM: ec[LET[ch]["e"]]+=1
    tot=sum(ec.values()) or 1
    eprof={e:round(ec[e]/tot,2) for e in ELEM}
    rootc={r:sum(s.count(r) for s in lines) for r in ROOTS}
    toproot=max(rootc,key=rootc.get)
    rows.append((f,L,namehit,nameocc,callhit,round(cov,2),eprof,toproot))

# null densidade de nomes (media por folha)
realavg=sum(r[2] for r in rows if r[6] is not None)/sum(1 for r in rows if r[6] is not None)
nul=[]
for _ in range(200):
    rn=randnames()
    tot=0;cnt=0
    for f in folhas:
        lines=folha_text(f); txt="#".join(lines)
        if len(txt)<50: continue
        tot+=sum(1 for n in rn if n in txt); cnt+=1
    nul.append(tot/cnt)
mu=sum(nul)/len(nul); sd=(sum((x-mu)**2 for x in nul)/len(nul))**.5
print(f"Densidade media de nomes/folha: real={realavg:.1f}  null={mu:.1f}  z={(realavg-mu)/sd:+.1f}\n")

print("folha | let | nomes(hit/occ) | call | cov% | elem(F/T/Ar/Ag) | raiz")
for f,L,nh,no,ch,cov,ep,tr in rows:
    if ep is None: print(f"{f:>5} | {L:>4} | (losango/pequena)"); continue
    print(f"{f:>5} | {L:>4} | {nh:>2}/{no:<3} | {ch:>2} | {int(cov*100):>3} | "
          f"{ep['Fogo']:.2f}/{ep['Terra']:.2f}/{ep['Ar']:.2f}/{ep['Agua']:.2f} | {tr}")

# resumo por terco
def terco(a,b):
    sub=[r for r in rows if a<=r[0]<=b and r[6] is not None]
    nh=sum(r[2] for r in sub)/len(sub); cov=sum(r[5] for r in sub)/len(sub)
    ca=sum(r[4] for r in sub)/len(sub)
    rc=collections.Counter()
    for r in sub: rc[r[7]]+=1
    return nh,cov,ca,rc.most_common(3)
print("\nResumo por terco (nomes/folha, cov, call/folha, raizes top):")
for a,b in ((1,16),(17,32),(33,48)):
    nh,cov,ca,rt=terco(a,b)
    print(f"  folhas {a}-{b}: nomes~{nh:.1f} cov~{cov*100:.0f}% call~{ca:.1f} raizes={rt}")

json.dump([{"folha":r[0],"letras":r[1],"nomes":r[2],"occ":r[3],"call":r[4],"cov":r[5],
            "elem":r[6],"raiz":r[7]} for r in rows],
          open(os.path.join(ROOT,"results","177_sweep.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/177_sweep.json")
