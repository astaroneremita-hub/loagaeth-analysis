# -*- coding: utf-8 -*-
"""a229 - remaining fine deep hypotheses (HIPOTESES_PROFUNDAS.md 31,32,36,40).

#40 ISLANDS OF ORDER: which folhas compress best (= most ordered)? outliers vs the book,
   and vs null (shuffled). Where does order concentrate in the chaos?
#36 COLUMN TWINS: are any two columns near-duplicates (shared structure) beyond chance?
#31 ROW first-letter predicts last-letter? (MI)
#32 ROW letter-value (gematria) sum forms a sequence with trend/periodicity?
seed 1583, stdlib only.
"""
import os
import sys
import json
import zlib
import math
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
from a190_tower_traces import side_grids

rng = random.Random(1583)
GEM = {"A":1,"B":2,"C":20,"D":4,"E":5,"F":6,"G":3,"H":8,"I":10,"L":30,"M":40,"N":50,"O":70,
       "P":80,"Q":90,"R":100,"S":200,"T":300,"U":400,"X":60,"Z":7,"V":400}


def comp_ratio(s):
    b = s.encode()
    return len(zlib.compress(b, 9)) / len(b) if b else 1.0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nums = load.table_numbers()
    ftext = {n: load.table_text(n) for n in nums}

    # ---------- #40 islands of order ----------
    print("[#40] ILHAS DE ORDEM (compressão por folha; menor = mais ordenada):", flush=True)
    cr = {n: comp_ratio(ftext[n]) for n in nums}
    vals = sorted(cr.items(), key=lambda x: x[1])
    book = comp_ratio("".join(ftext[n] for n in nums))
    # null: shuffle each folha
    def shuf(s):
        l = list(s); rng.shuffle(l); return "".join(l)
    null_cr = {n: [comp_ratio(shuf(ftext[n])) for _ in range(20)] for n in nums}
    # z per folha: how much MORE ordered than its own shuffle
    zrows = []
    for n in nums:
        m = sum(null_cr[n])/len(null_cr[n]); sd = (sum((x-m)**2 for x in null_cr[n])/len(null_cr[n]))**0.5
        z = (cr[n]-m)/sd if sd else 0
        zrows.append((n, round(cr[n],3), round(z,2)))
    zrows.sort(key=lambda x: x[2])
    print(f"   livro inteiro ratio={book:.3f}", flush=True)
    print(f"   mais ordenadas (ratio e z vs próprio shuffle): {zrows[:6]}", flush=True)
    print(f"   menos ordenadas: {zrows[-4:]}", flush=True)

    # ---------- #36 column twins ----------
    print("[#36] COLUNAS-GÊMEAS:", flush=True)
    grids = list(side_grids().values())
    # average column profile across grids (letter freq per column index)
    colprof = [Counter() for _ in range(49)]
    for g in grids:
        for c in range(49):
            for r in range(49):
                if g[r][c] != "?": colprof[c][g[r][c]] += 1
    def cos(a, b):
        ks = set(a)|set(b); dot=sum(a[k]*b[k] for k in ks)
        na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
        return dot/(na*nb) if na and nb else 0
    best = (0, None)
    for i in range(49):
        for j in range(i+1, 49):
            s = cos(colprof[i], colprof[j])
            if s > best[0]: best = (s, (i, j))
    print(f"   par de colunas mais parecido: {best[1]} cos={best[0]:.3f} (borda tende a casar com borda)", flush=True)

    # ---------- #31 row first->last ----------
    print("[#31] PRIMEIRA letra da linha prediz a ÚLTIMA?:", flush=True)
    pairs = []
    for g in grids:
        for r in range(49):
            row = g[r]
            if row[0] != "?" and row[-1] != "?":
                pairs.append((row[0], row[-1]))
    def mi(pp):
        n=len(pp); pa=Counter(a for a,b in pp); pb=Counter(b for a,b in pp); pab=Counter(pp); m=0
        for (a,b),c in pab.items():
            px=pa[a]/n; py=pb[b]/n; pxy=c/n
            if pxy>0: m+=pxy*math.log2(pxy/(px*py))
        return m
    obs = mi(pairs)
    sims = []
    for _ in range(200):
        bs = [b for _,b in pairs]; rng.shuffle(bs)
        sims.append(mi(list(zip([a for a,_ in pairs], bs))))
    m=sum(sims)/len(sims); sd=(sum((x-m)**2 for x in sims)/len(sims))**0.5
    print(f"   MI(1ª,última) = {obs:.4f} vs null {m:.4f}±{sd:.4f}  z={(obs-m)/sd if sd else 0:+.2f}", flush=True)

    # ---------- #32 row value sum sequence ----------
    print("[#32] SOMA de valor por linha — sequência com estrutura?:", flush=True)
    sums = []
    for g in grids[:1]:  # one representative grid
        for r in range(49):
            sums.append(sum(GEM.get(ch,0) for ch in g[r]))
    # autocorr lag1 of the sum sequence vs shuffled
    def ac1(x):
        n=len(x)-1; mx=sum(x)/len(x)
        num=sum((x[i]-mx)*(x[i+1]-mx) for i in range(n)); den=sum((v-mx)**2 for v in x)
        return num/den if den else 0
    obs=ac1(sums); sims=[]
    for _ in range(200):
        s=sums[:]; rng.shuffle(s); sims.append(ac1(s))
    m=sum(sims)/len(sims); sd=(sum((x-m)**2 for x in sims)/len(sims))**0.5
    print(f"   autocorr lag1 da soma por linha = {obs:+.3f} vs null {m:+.3f}±{sd:.3f} z={(obs-m)/sd if sd else 0:+.2f}", flush=True)

    result = {"islands_most_ordered": zrows[:8], "islands_least": zrows[-4:], "book_ratio": round(book,3),
              "column_twin": {"pair": best[1], "cos": round(best[0],3)}}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "229_order_islands.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
