# -*- coding: utf-8 -*-
"""a222 - REAL linguistic universals not yet tested on the Loagaeth names.

A) VOWEL HARMONY: do adjacent vowels agree in class (front E/I, back O/U, central A)?
   A true cross-linguistic feature (Turkish, Finnish). vs null (random strings).
B) REDUPLICATION: do names carry an immediately-repeated unit (ANT-ANT)? vs null.
C) POSITIONAL PHONOTACTICS: are the name-initial and name-final letter inventories
   significantly different from each other and from the body (onset/coda asymmetry)?
seed 1583, stdlib only.
"""
import os
import sys
import json
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

VOW = set("AEIOU")
VCLASS = {"E": "front", "I": "front", "O": "back", "U": "back", "A": "central"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    # build a solid recurring-name list from the book (6-grams >= 15, deduped by 4-gram overlap)
    full = load.dense_stream()
    c6 = Counter(full[i:i+6] for i in range(len(full)-5))
    cand = sorted([g for g, v in c6.items() if v >= 15], key=lambda g: -c6[g])
    def g4(s): return set(s[i:i+4] for i in range(len(s)-3))
    NAMES = []
    for v in cand:
        gv = g4(v)
        if all(not (gv & g4(u)) for u in NAMES):
            NAMES.append(v)
        if len(NAMES) >= 40:
            break
    freq = Counter(full); letters = list(freq); weights = [freq[c] for c in letters]
    lens = [len(n) for n in NAMES]
    result = {"n_names": len(NAMES)}

    def rand_set():
        return ["".join(rng.choices(letters, weights, k=L)) for L in lens]

    # ---- A vowel harmony ----
    def harmony(words):
        same = tot = 0
        for w in words:
            vs = [VCLASS[c] for c in w if c in VOW]
            for a, b in zip(vs, vs[1:]):
                tot += 1
                if a == b:
                    same += 1
        return same / tot if tot else 0
    obsA = harmony(NAMES)
    simA = [harmony(rand_set()) for _ in range(500)]
    mA = sum(simA)/len(simA); sA = (sum((x-mA)**2 for x in simA)/len(simA))**0.5
    zA = (obsA-mA)/sA if sA else 0
    result["vowel_harmony"] = {"obs": round(obsA,3), "null": round(mA,3), "sd": round(sA,3), "z": round(zA,2)}
    print(f"[A harmonia vocálica] vogais adjacentes mesma classe: obs {obsA:.3f} vs null {mA:.3f}±{sA:.3f} z={zA:+.2f}", flush=True)

    # ---- B reduplication ----
    def redup(words):
        k = 0
        for w in words:
            hit = False
            for L in (2, 3):
                for i in range(len(w)-2*L+1):
                    if w[i:i+L] == w[i+L:i+2*L]:
                        hit = True; break
                if hit: break
            if hit: k += 1
        return k / len(words)
    obsB = redup(NAMES)
    simB = [redup(rand_set()) for _ in range(500)]
    mB = sum(simB)/len(simB); sB = (sum((x-mB)**2 for x in simB)/len(simB))**0.5
    zB = (obsB-mB)/sB if sB else 0
    result["reduplication"] = {"obs": round(obsB,3), "null": round(mB,3), "sd": round(sB,3), "z": round(zB,2),
                               "examples": [w for w in NAMES if any(w[i:i+2]==w[i+2:i+4] for i in range(len(w)-3)) or any(w[i:i+3]==w[i+3:i+6] for i in range(len(w)-5))]}
    print(f"[B reduplicação] nomes com unidade repetida: obs {obsB:.3f} vs null {mB:.3f}±{sB:.3f} z={zB:+.2f}", flush=True)
    print(f"    exemplos: {result['reduplication']['examples'][:8]}", flush=True)

    # ---- C positional phonotactics ----
    onset = Counter(w[0] for w in NAMES)
    coda = Counter(w[-1] for w in NAMES)
    body = Counter(c for w in NAMES for c in w[1:-1])
    bt = sum(body.values())
    def enrich(pos):
        n = sum(pos.values())
        return sorted(((l, round((pos[l]/n)/(body.get(l,0.5)/bt), 2)) for l in pos), key=lambda x: -x[1])[:6]
    result["phonotactics"] = {"onset_top": [l for l,_ in onset.most_common(6)],
                              "coda_top": [l for l,_ in coda.most_common(6)],
                              "onset_enriched_vs_body": enrich(onset),
                              "coda_enriched_vs_body": enrich(coda)}
    print(f"[C fonotática] início (onset) top: {onset.most_common(6)}", flush=True)
    print(f"               fim (coda) top: {coda.most_common(6)}", flush=True)
    print(f"               enriquecido no início: {enrich(onset)[:4]}", flush=True)
    print(f"               enriquecido no fim: {enrich(coda)[:4]}", flush=True)

    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "222_linguistic_universals.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
