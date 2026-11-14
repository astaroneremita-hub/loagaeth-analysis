# -*- coding: utf-8 -*-
"""
a179 — Dinastias dos nomes (genealogia, frente 2). Agrupa os 90 nomes por raiz,
monta grafo edicao-1 (familias), acha PONTES entre dinastias (nomes com 2 raizes =
compostos), e testa a estrutura de familia contra null. seed 1583.
"""
import json, re, os, random, collections, itertools
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    return re.sub(r"[^a-z]","",str(w).lower())
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=sorted(set(norm(n) for n in fg["real_names"]))
ROOTS=[r.lower() for r in fg["roots"]]

# raizes de cada nome (pode ter >1 = ponte)
def roots_of(n):
    return [r for r in ROOTS if r in n]
members=collections.defaultdict(list); bridges=[]
for n in NAMES:
    rs=roots_of(n)
    for r in rs: members[r].append(n)
    if len(rs)>=2: bridges.append((n,rs))
    if len(rs)==0: members["(sem raiz)"].append(n)

print("DINASTIAS (por raiz):")
for r in sorted(members,key=lambda r:-len(members[r])):
    print(f"  {r.upper():<10} {len(members[r]):>2}: {', '.join(members[r])}")

print(f"\nPONTES (nome com 2+ raizes = casamento de dinastias): {len(bridges)}")
for n,rs in bridges:
    print(f"  {n} = {' + '.join(r.upper() for r in rs)}")

# grafo edicao-1 (Levenshtein<=1) entre os 90 nomes
def ed1(a,b):
    if a==b: return False
    la,lb=len(a),len(b)
    if abs(la-lb)>1: return False
    if la==lb: return sum(x!=y for x,y in zip(a,b))==1
    if la>lb: a,b=b,a; la,lb=lb,la
    i=j=0;d=0
    while i<la and j<lb:
        if a[i]==b[j]: i+=1;j+=1
        else:
            d+=1; j+=1
            if d>1: return False
    return True
import sys
adj={n:set() for n in NAMES}
for a,b in itertools.combinations(NAMES,2):
    if ed1(a,b): adj[a].add(b); adj[b].add(a)
# componentes
seen=set();comps=[]
for n in NAMES:
    if n in seen: continue
    st=[n];comp=[]
    while st:
        x=st.pop()
        if x in seen: continue
        seen.add(x);comp.append(x);st+=[y for y in adj[x] if y not in seen]
    comps.append(sorted(comp))
comps.sort(key=len,reverse=True)
edges=sum(len(v) for v in adj.values())//2
print(f"\nGRAFO edicao-1: {edges} arestas, {len(comps)} componentes")
for c in comps[:8]:
    if len(c)>=2: print(f"  familia({len(c)}): {', '.join(c)}")
singles=sum(1 for c in comps if len(c)==1)
print(f"  ... + {singles} isolados")

# null: mesma contagem de arestas em nomes aleatorios (mesmos tamanhos/letras)
letpool="".join(NAMES); sizes=[len(n) for n in NAMES]
NT=1000; nulledges=[]
for _ in range(NT):
    rn=["".join(random.choice(letpool) for _ in range(s)) for s in sizes]
    e=0
    for a,b in itertools.combinations(rn,2):
        if ed1(a,b): e+=1
    nulledges.append(e)
mu=sum(nulledges)/NT; sd=(sum((x-mu)**2 for x in nulledges)/NT)**.5
print(f"\nNULL arestas edicao-1: {mu:.1f} (real {edges}) z={(edges-mu)/sd:+.1f}")

json.dump({"dinastias":{r:members[r] for r in members},
           "pontes":[{"nome":n,"raizes":rs} for n,rs in bridges],
           "edges":edges,"componentes":[c for c in comps if len(c)>=2],
           "null_edges":round(mu,1),"z":round((edges-mu)/sd,1)},
          open(os.path.join(ROOT,"results","179_dynasties.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/179_dynasties.json")
