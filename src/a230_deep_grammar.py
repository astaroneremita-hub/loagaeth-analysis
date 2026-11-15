# -*- coding: utf-8 -*-
"""a230 - deeper structured deep hypotheses (29, 33, 37, 39).

#37 DIAGONAL MI: mutual information between cells at the descending-diagonal offset (the
   name-reading line #341) vs horizontal/vertical. Does the diagonal carry grammar?
#29 LOCAL GRAMMAR DRIFT: train an order-3 model on region A, test perplexity on region B.
   Does the predictive grammar drift across the book (grammar-level dialect)?
#39 FINE LEAF JUNCTION: does the last row of leaf N predict the first row of leaf N+1 at the
   same column (vertical flow across the page break)?
#33 VOWEL/CONSONANT RUN periodicity: is the V/C pattern periodic (syllable rhythm)?
seed 1583, stdlib only.
"""
import os
import sys
import json
import math
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
from a190_tower_traces import side_grids

rng = random.Random(1583)
VOW = set("AEIOU")


def mi(pairs):
    n=len(pairs); pa=Counter(a for a,b in pairs); pb=Counter(b for a,b in pairs); pab=Counter(pairs); m=0
    for (a,b),c in pab.items():
        px=pa[a]/n; py=pb[b]/n; pxy=c/n
        if pxy>0: m+=pxy*math.log2(pxy/(px*py))
    return m


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = list(side_grids().values())

    # ---------- #37 diagonal vs horizontal vs vertical MI ----------
    print("[#37] MI por direção (célula x célula adjacente):", flush=True)
    def dir_pairs(dr, dc):
        pp=[]
        for g in grids:
            H=len(g); W=len(g[0])
            for r in range(H):
                for c in range(W):
                    rr,cc=r+dr,c+dc
                    if 0<=rr<H and 0<=cc<W and g[r][c]!="?" and g[rr][cc]!="?":
                        pp.append((g[r][c],g[rr][cc]))
        return pp
    for name,(dr,dc) in [("horizontal",(0,1)),("vertical",(1,0)),("diagonal ↘",(1,1)),("anti ↙",(1,-1))]:
        print(f"   {name:12s} MI={mi(dir_pairs(dr,dc)):.4f}", flush=True)

    # ---------- #29 local grammar drift ----------
    print("[#29] DERIVA DE GRAMÁTICA (perplexidade cruzada por região):", flush=True)
    nums=load.table_numbers()
    regions={"corpo(11-22)":range(11,23),"costura(26-28)":range(26,29),"profundo(41-48)":range(41,49)}
    def train(rng_):
        ctx=defaultdict(Counter)
        for n in rng_:
            s=load.table_text(n)
            for i in range(len(s)-3): ctx[s[i:i+3]][s[i+3]]+=1
        return ctx
    def perp(ctx,rng_):
        bits=0;cnt=0;V=24
        for n in rng_:
            s=load.table_text(n)
            for i in range(len(s)-3):
                c=ctx.get(s[i:i+3]);
                if c:
                    tot=sum(c.values()); p=(c.get(s[i+3],0)+0.5)/(tot+0.5*V)
                else: p=1/V
                bits+=-math.log2(p); cnt+=1
        return bits/cnt
    models={k:train(v) for k,v in regions.items()}
    for ka in regions:
        line=[]
        for kb in regions:
            line.append(f"{kb.split('(')[0]}={perp(models[ka],regions[kb]):.2f}")
        print(f"   treino {ka.split('(')[0]:9s}: {line}", flush=True)

    # ---------- #39 fine leaf junction ----------
    print("[#39] JUNÇÃO FINA entre folhas (última linha N prediz 1ª linha N+1, mesma coluna):", flush=True)
    lv=load.leaves()
    sides=[k for k in lv if k[-1] in "ab" and len([1 for r in lv[k] if len(load.letters(r))==49])==49]
    def rows(k): return [load.letters(r) for r in lv[k]]
    pp=[]
    order=sorted([k for k in lv if k[-1] in "ab"], key=lambda k:(int("".join(c for c in k if c.isdigit())),k))
    for a,b in zip(order,order[1:]):
        ra=rows(a); rb=rows(b)
        if len(ra)==49 and len(rb)==49 and len(ra[-1])==49 and len(rb[0])==49:
            for c in range(49):
                if ra[-1][c]!="?" and rb[0][c]!="?":
                    pp.append((ra[-1][c], rb[0][c]))
    obs=mi(pp) if pp else 0
    sims=[]
    for _ in range(200):
        bs=[b for _,b in pp]; rng.shuffle(bs); sims.append(mi(list(zip([a for a,_ in pp],bs))))
    m=sum(sims)/len(sims); sd=(sum((x-m)**2 for x in sims)/len(sims))**0.5
    print(f"   MI(última linha N, 1ª linha N+1) = {obs:.4f} vs null {m:.4f}±{sd:.4f} z={(obs-m)/sd if sd else 0:+.2f}", flush=True)

    # ---------- #33 V/C run periodicity ----------
    print("[#33] RUNS vogal/consoante (ritmo silábico):", flush=True)
    S=load.dense_stream()
    vc="".join("V" if ch in VOW else "C" for ch in S)
    runs=[]; cur=1
    for i in range(1,len(vc)):
        if vc[i]==vc[i-1]: cur+=1
        else: runs.append((vc[i-1],cur)); cur=1
    cr=Counter(l for t,l in runs if t=="C"); vr=Counter(l for t,l in runs if t=="V")
    print(f"   runs de consoante (tamanho:qtd): {dict(sorted(cr.items())[:5])}", flush=True)
    print(f"   runs de vogal: {dict(sorted(vr.items())[:5])}", flush=True)
    meanC=sum(l*q for l,q in cr.items())/sum(cr.values()); meanV=sum(l*q for l,q in vr.items())/sum(vr.values())
    print(f"   run médio: consoante {meanC:.2f}, vogal {meanV:.2f} (ritmo CV)", flush=True)

    rdir=os.path.join(HERE,"..","results"); os.makedirs(rdir,exist_ok=True)
    with open(os.path.join(rdir,"230_deep_grammar.json"),"w",encoding="utf-8") as f:
        json.dump({"note":"ver stdout"},f)
    print("done", flush=True)


if __name__ == "__main__":
    main()
