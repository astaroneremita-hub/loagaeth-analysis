# -*- coding: utf-8 -*-
"""a217 - NEW hypothesis on a different axis: the book as SOUND, not text.

The record: Loagaeth = "Speech from God", meant to be SPOKEN (leaf 1 carries stress marks).
Every prior analysis treated it as letters. This tests whether the recurring names are built
for VOCALIZATION - more pronounceable / chantable than chance:
  - vowel ratio (you need vowels to sing),
  - max consonant-cluster length (chantable = short clusters),
  - CV-alternation rate,
  - sonority-sequencing well-formedness (sonority peaks at vowels).
Compare the recurring Loagaeth names to two nulls: (1) random strings, same letter frequency,
same length; (2) Markov-3 surrogate of the book (preserves local letter habits).

If the names are significantly MORE pronounceable than BOTH nulls, the book is phonetically
designed - evidence for "Speech from God", spoken. stdlib only. seed 1583.
"""
import os
import sys
import json
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

VOW = set("AEIOU")
# sonority: vowel 4, liquid 3, nasal 2, fricative 1, stop 0
SON = {}
for g, v in [("AEIOU", 4), ("LR", 3), ("MN", 2), ("SZXFHV", 1), ("BCDGPTQK", 0)]:
    for ch in g:
        SON[ch] = v

NAMES = ['NACHO','NOCHAP','NOCHASTOR','NOCHAPH','ADNOCHAP','ACLAXTO','GRADAX','AXALGRA',
 'NOCHASTORA','ICHASTOR','PHANGE','ANTANTOX','VOXAR','NECHASTOR','ACLAXTOR','ICHASTORA',
 'ZICHASTOR','ANCHANO','NADAB','CHARDAX','AOXARD','ALCHADAX','OXARDRAH','OLCHADNA',
 'NACLANSA','DONCHAL','ACHARDAN','CHIDAXTO','GASTA','NODALGA','UCHER','ALGETH','ANZACH',
 'DAXVAR','NTAGNA','ACHEPH','GRAPHA','NACHOA','NACHOAD','NACHOAL']


def metrics(w):
    n = len(w)
    vr = sum(1 for c in w if c in VOW) / n
    # max consonant run
    mx = cur = 0
    for c in w:
        if c in VOW:
            cur = 0
        else:
            cur += 1; mx = max(mx, cur)
    # CV alternation rate: fraction of adjacent pairs that alternate V/C
    alt = sum(1 for i in range(n - 1) if (w[i] in VOW) != (w[i + 1] in VOW)) / (n - 1) if n > 1 else 0
    # sonority well-formedness: count "bad" adjacencies (two equal-low obstruents, or sonority
    # plateau at 0) as violations; well-formed = low violation rate
    viol = 0
    for i in range(n - 1):
        a, b = SON.get(w[i], 0), SON.get(w[i + 1], 0)
        if a == 0 and b == 0:  # two stops adjacent (hard to pronounce)
            viol += 1
    wf = 1 - viol / (n - 1) if n > 1 else 1
    return vr, mx, alt, wf


def summ(words):
    vs, mxs, alts, wfs = [], [], [], []
    for w in words:
        if len(w) < 3:
            continue
        vr, mx, alt, wf = metrics(w)
        vs.append(vr); mxs.append(mx); alts.append(alt); wfs.append(wf)
    k = len(vs)
    return (sum(vs)/k, sum(mxs)/k, sum(alts)/k, sum(wfs)/k)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    S = load.dense_stream()
    freq = Counter(S); letters = list(freq); weights = [freq[c] for c in letters]
    lens = [len(n) for n in NAMES]

    real = summ(NAMES)

    # null 1: random strings, same letter freq, same lengths
    def rand_names():
        return ["".join(rng.choices(letters, weights, k=L)) for L in lens]
    # null 2: markov-3 surrogate sampled from the book, same lengths
    m3 = defaultdict(list)
    for i in range(len(S) - 3):
        m3[S[i:i+3]].append(S[i+3])
    starts = [S[i:i+3] for i in range(0, len(S)-3, 500)]
    def markov_name(L):
        ctx = rng.choice(starts); out = list(ctx)
        while len(out) < L:
            nxt = m3.get("".join(out[-3:]))
            out.append(rng.choice(nxt) if nxt else rng.choices(letters, weights)[0])
        return "".join(out[:L])
    def markov_names():
        return [markov_name(L) for L in lens]

    def null_dist(gen, trials=300):
        acc = [[], [], [], []]
        for _ in range(trials):
            s = summ(gen())
            for i in range(4):
                acc[i].append(s[i])
        return acc

    n1 = null_dist(rand_names); n2 = null_dist(markov_names)
    labels = ["vowel_ratio", "max_cons_cluster", "cv_alternation", "sonority_wellformed"]
    print(f"{'métrica':20s} {'real':>8s} {'rand':>8s} z1 {'markov3':>9s} z2", flush=True)
    result = {"seed": 1583, "metrics": {}}
    for i, lab in enumerate(labels):
        m1 = sum(n1[i])/len(n1[i]); s1 = (sum((x-m1)**2 for x in n1[i])/len(n1[i]))**0.5
        mm2 = sum(n2[i])/len(n2[i]); s2 = (sum((x-mm2)**2 for x in n2[i])/len(n2[i]))**0.5
        z1 = (real[i]-m1)/s1 if s1 else 0; z2 = (real[i]-mm2)/s2 if s2 else 0
        print(f"{lab:20s} {real[i]:8.3f} {m1:8.3f} {z1:+5.1f} {mm2:9.3f} {z2:+5.1f}", flush=True)
        result["metrics"][lab] = {"real": round(real[i],3), "rand_mean": round(m1,3), "z_vs_rand": round(z1,2),
                                  "markov_mean": round(mm2,3), "z_vs_markov": round(z2,2)}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "217_book_as_sound.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
