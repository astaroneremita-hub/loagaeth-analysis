# -*- coding: utf-8 -*-
"""a225 - Menzerath-Altmann law (real linguistic universal, not yet tested).

Law: the longer the construct, the shorter its constituents. For words: more syllables ->
shorter mean syllable (letters/syllable). A true cross-linguistic regularity. Test on leaf-1
word tokens (~3000 real words) and on the recurring names. Null: random strings.

Also: the H role - where does H sit (aspirate/breath)? inter-vocalic, pre-pausal, onset?
seed 1583, stdlib only.
"""
import os
import sys
import json
import re
import math
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

VOW = set("AEIOU")


def syl_count(w):
    return len(re.findall(r"[AEIOU]+", w))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    # leaf-1 word tokens (plain words, no hyphen clusters)
    lv = load.leaves()
    words = []
    for key in ("1a", "1b"):
        for row in lv[key]:
            for tok in row.split():
                w = load.letters(tok)
                if len(w) >= 2 and "-" not in tok:
                    words.append(w)

    # Menzerath: mean syllable length by syllable count
    by_k = defaultdict(list)
    for w in words:
        k = syl_count(w)
        if k >= 1:
            by_k[k].append(len(w) / k)
    rows = sorted((k, sum(v) / len(v), len(v)) for k, v in by_k.items() if len(v) >= 10)
    print("[MENZERATH] sílabas(K) -> comprimento médio de sílaba (letras/K):", flush=True)
    for k, ml, n in rows:
        print(f"   K={k}: sílaba média {ml:.2f} letras   (n={n})", flush=True)
    # correlation K vs mean-syll-length (weighted by count); negative = Menzerath
    ks = [r[0] for r in rows]; mls = [r[1] for r in rows]
    n = len(ks); mk = sum(ks)/n; mm = sum(mls)/n
    cov = sum((ks[i]-mk)*(mls[i]-mm) for i in range(n))
    vk = sum((x-mk)**2 for x in ks); vm = sum((x-mm)**2 for x in mls)
    corr = cov/math.sqrt(vk*vm) if vk and vm else 0
    print(f"[MENZERATH] corr(K, sílaba média) = {corr:+.3f}  (negativo = lei de Menzerath vale)", flush=True)

    # null: random strings, same length distribution
    lens = [len(w) for w in words]
    freq = Counter("".join(words)); L = list(freq); W = [freq[c] for c in L]
    def null_corr():
        sur = ["".join(rng.choices(L, W, k=l)) for l in lens]
        bk = defaultdict(list)
        for w in sur:
            k = syl_count(w)
            if k >= 1: bk[k].append(len(w)/k)
        rr = sorted((k, sum(v)/len(v)) for k, v in bk.items() if len(v) >= 10)
        if len(rr) < 3: return 0
        xs=[a for a,_ in rr]; ys=[b for _,b in rr]; nn=len(xs); mx=sum(xs)/nn; my=sum(ys)/nn
        c=sum((xs[i]-mx)*(ys[i]-my) for i in range(nn)); vx=sum((x-mx)**2 for x in xs); vy=sum((y-my)**2 for y in ys)
        return c/math.sqrt(vx*vy) if vx and vy else 0
    sims = [null_corr() for _ in range(200)]
    m = sum(sims)/len(sims); sd = (sum((x-m)**2 for x in sims)/len(sims))**0.5
    z = (corr-m)/sd if sd else 0
    print(f"[MENZERATH] null corr {m:+.3f}±{sd:.3f}  z={z:+.2f}", flush=True)

    # H role
    hn = {"inicio": 0, "fim": 0, "intervocalico": 0, "outro": 0, "total": 0}
    for w in words:
        for i, c in enumerate(w):
            if c != "H": continue
            hn["total"] += 1
            if i == 0: hn["inicio"] += 1
            elif i == len(w)-1: hn["fim"] += 1
            elif w[i-1] in VOW and i+1 < len(w) and w[i+1] in VOW: hn["intervocalico"] += 1
            else: hn["outro"] += 1
    print(f"[H] posição do H (n={hn['total']}): início {hn['inicio']}, fim {hn['fim']}, intervocálico {hn['intervocalico']}, outro {hn['outro']}", flush=True)

    result = {"menzerath": {"rows": [[k, round(ml,2), n] for k,ml,n in rows], "corr": round(corr,3),
                            "null_mean": round(m,3), "null_sd": round(sd,3), "z": round(z,2)},
              "H_position": hn}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "225_menzerath.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
