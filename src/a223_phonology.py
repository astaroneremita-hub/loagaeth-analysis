# -*- coding: utf-8 -*-
"""a223 - deeper phonology of the names (the fertile sound axis).

A) VOWEL MELODY: is the vowel-skeleton (vowels only, in order) concentrated on a few
   signature patterns (a canonical chant-melody) more than chance?
B) ONSET WELL-FORMEDNESS: do name-initial consonant clusters RISE in sonority toward the
   vowel (the Sonority Sequencing Principle)? vs null.
C) OPEN-SYLLABLE RATE: syllabify by max-onset; is the language dominated by open (CV)
   syllables (like Polynesian/liturgical chant) more than chance?
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
SON = {}
for g, v in [("AEIOU", 4), ("LR", 3), ("MN", 2), ("SZXFHV", 1), ("BCDGPTQK", 0)]:
    for ch in g:
        SON[ch] = v


def vskel(w):
    return "".join(c for c in w if c in VOW)


def onsets(w):
    """leading consonant cluster + each consonant cluster before a vowel."""
    out = []
    cur = ""
    for c in w:
        if c in VOW:
            if cur:
                out.append(cur); cur = ""
        else:
            cur += c
    return [o for o in out if len(o) >= 2]


def open_syllable_rate(w):
    """max-onset syllabification: count syllables; a syllable is 'open' if it ends in a vowel."""
    # simple: split into V-nuclei; a coda exists if consonants sit between this vowel and the
    # next onset. Approx: count VC...CV -> if >=2 consonants between vowels, 1 is coda (closed).
    syl_closed = 0; syl_tot = 0; i = 0
    vpos = [j for j, c in enumerate(w) if c in VOW]
    for k in range(len(vpos)):
        syl_tot += 1
        if k < len(vpos) - 1:
            gap = vpos[k + 1] - vpos[k] - 1  # consonants between
            if gap >= 2:
                syl_closed += 1  # one consonant becomes a coda
        else:
            # final: closed if a consonant follows
            if vpos[k] < len(w) - 1:
                syl_closed += 1
    return 1 - syl_closed / syl_tot if syl_tot else 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    full = load.dense_stream()
    c6 = Counter(full[i:i+6] for i in range(len(full)-5))
    cand = sorted([g for g, v in c6.items() if v >= 15], key=lambda g: -c6[g])
    def g4(s): return set(s[i:i+4] for i in range(len(s)-3))
    NAMES = []
    for v in cand:
        if all(not (g4(v) & g4(u)) for u in NAMES):
            NAMES.append(v)
        if len(NAMES) >= 40:
            break
    freq = Counter(full); letters = list(freq); weights = [freq[c] for c in letters]
    lens = [len(n) for n in NAMES]
    result = {"n_names": len(NAMES)}

    def rand_set():
        return ["".join(rng.choices(letters, weights, k=L)) for L in lens]

    # ---- A vowel melody concentration ----
    def top_share(words, k=5):
        c = Counter(vskel(w) for w in words)
        return sum(v for _, v in c.most_common(k)) / sum(c.values()), c.most_common(6)
    obsA, melo = top_share(NAMES)
    simA = [top_share(rand_set())[0] for _ in range(500)]
    mA = sum(simA)/len(simA); sA = (sum((x-mA)**2 for x in simA)/len(simA))**0.5
    zA = (obsA-mA)/sA if sA else 0
    result["vowel_melody"] = {"top5_share": round(obsA,3), "null": round(mA,3), "sd": round(sA,3), "z": round(zA,2), "top": melo}
    print(f"[A melodia] top-5 esqueletos vocálicos cobrem {obsA:.2f} vs null {mA:.2f}±{sA:.2f} z={zA:+.2f}", flush=True)
    print(f"    melodias dominantes: {melo}", flush=True)

    # ---- B onset sonority rise ----
    def onset_wf(words):
        good = tot = 0
        for w in words:
            for o in onsets(w):
                tot += 1
                sons = [SON.get(ch, 0) for ch in o]
                if all(sons[i] <= sons[i+1] for i in range(len(sons)-1)):
                    good += 1
        return good / tot if tot else None, tot
    obsB, nB = onset_wf(NAMES)
    simB = [onset_wf(rand_set())[0] for _ in range(500)]
    simB = [x for x in simB if x is not None]
    mB = sum(simB)/len(simB); sB = (sum((x-mB)**2 for x in simB)/len(simB))**0.5
    zB = (obsB-mB)/sB if sB else 0
    result["onset_sonority"] = {"obs": round(obsB,3), "n_clusters": nB, "null": round(mB,3), "sd": round(sB,3), "z": round(zB,2)}
    print(f"[B onset] clusters iniciais que SOBEM em sonoridade: obs {obsB:.2f} ({nB} clusters) vs null {mB:.2f}±{sB:.2f} z={zB:+.2f}", flush=True)

    # ---- C open-syllable rate ----
    def osr(words):
        return sum(open_syllable_rate(w) for w in words) / len(words)
    obsC = osr(NAMES)
    simC = [osr(rand_set()) for _ in range(500)]
    mC = sum(simC)/len(simC); sC = (sum((x-mC)**2 for x in simC)/len(simC))**0.5
    zC = (obsC-mC)/sC if sC else 0
    result["open_syllable"] = {"obs": round(obsC,3), "null": round(mC,3), "sd": round(sC,3), "z": round(zC,2)}
    print(f"[C abertura] taxa de sílaba aberta (CV): obs {obsC:.2f} vs null {mC:.2f}±{sC:.2f} z={zC:+.2f}", flush=True)

    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "223_phonology.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
