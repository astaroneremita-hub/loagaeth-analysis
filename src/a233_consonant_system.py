# -*- coding: utf-8 -*-
"""a233 - is the consonant inventory a coherent phonological SYSTEM?

Identity is consonantal (#402). So: classify the consonants by PLACE and MANNER; is the
inventory balanced (a designed phonology) or skewed? Which natural classes dominate? And do
the names contrast by a single consonant from the same class (consonant minimal pairs,
mirroring the vowel ones #358)?
stdlib only.
"""
import os
import sys
import json
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

VOW = set("AEIOU")
# place / manner for the Enochian (Latin-transliterated) consonants
PLACE = {"B":"labial","P":"labial","M":"labial","F":"labial","V":"labial",
         "D":"coronal","T":"coronal","N":"coronal","S":"coronal","Z":"coronal","L":"coronal","R":"coronal",
         "C":"velar","G":"velar","Q":"velar","X":"velar","H":"glotal"}
MANNER = {"B":"oclusiva","P":"oclusiva","D":"oclusiva","T":"oclusiva","C":"oclusiva","G":"oclusiva","Q":"oclusiva",
          "M":"nasal","N":"nasal","L":"liquida","R":"liquida",
          "F":"fricativa","V":"fricativa","S":"fricativa","Z":"fricativa","X":"fricativa","H":"fricativa"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    full = load.dense_stream()
    c6 = Counter(full[i:i+6] for i in range(len(full)-5))
    cand = sorted([g for g, v in c6.items() if v >= 15], key=lambda g: -c6[g])
    def g4(s): return set(s[i:i+4] for i in range(len(s)-3))
    names = []
    for v in cand:
        if all(not (g4(v) & g4(u)) for u in names): names.append(v)
        if len(names) >= 60: break

    cc = Counter(ch for g in [full] for ch in g if ch not in VOW)
    tot = sum(cc.values())
    place = Counter(); manner = Counter()
    for ch, n in cc.items():
        if ch in PLACE: place[PLACE[ch]] += n
        if ch in MANNER: manner[MANNER[ch]] += n
    print("[PONTO de articulação] share:", {k: round(100*v/tot) for k, v in place.most_common()}, flush=True)
    print("[MODO de articulação] share:", {k: round(100*v/tot) for k, v in manner.most_common()}, flush=True)

    # consonant minimal pairs: names equal except ONE consonant, which is same manner/place
    def cskel(w): return [c for c in w if c not in VOW]
    pairs_same_class = 0; pairs_total = 0; examples = []
    for i in range(len(names)):
        for j in range(i+1, len(names)):
            a, b = names[i], names[j]
            if len(a) != len(b): continue
            diff = [(x, y) for x, y in zip(a, b) if x != y]
            if len(diff) == 1:
                x, y = diff[0]
                if x not in VOW and y not in VOW:
                    pairs_total += 1
                    if MANNER.get(x) == MANNER.get(y) or PLACE.get(x) == PLACE.get(y):
                        pairs_same_class += 1
                        if len(examples) < 8: examples.append((a, b, f"{x}/{y}"))
    print(f"[contraste] pares de nome que diferem por 1 consoante: {pairs_total}; mesma classe: {pairs_same_class}", flush=True)
    print(f"    exemplos: {examples}", flush=True)

    # balance: is the manner distribution close to uniform (4 manners) or skewed?
    import math
    def H(c):
        n = sum(c.values()); return -sum((v/n)*math.log2(v/n) for v in c.values() if v)
    print(f"[balanço] entropia modo = {H(manner):.2f} de {math.log2(len(manner)):.2f} máx; ponto = {H(place):.2f} de {math.log2(len(place)):.2f}", flush=True)

    out = {"place": dict(place), "manner": dict(manner), "cons_minpairs": pairs_total,
           "same_class": pairs_same_class, "examples": examples}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "233_consonant_system.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
