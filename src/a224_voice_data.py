# -*- coding: utf-8 -*-
"""a224 - assemble the phonetic profile for the 'Voice of the Loagaeth' chant guide.
Consolidates #386-392 into usable data: vowel melodies, consonant inventory, and a set of
names syllabified with penultimate stress + sustained open ending, ready to recite.
stdlib only.
"""
import os
import sys
import json
import re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

VOW = set("AEIOU")


def syllabify(w):
    """crude max-onset syllabification into CV(C) units for recitation display."""
    vpos = [i for i, c in enumerate(w) if c in VOW]
    if not vpos:
        return [w]
    cuts = [0]
    for k in range(len(vpos) - 1):
        gap = w[vpos[k] + 1:vpos[k + 1]]
        # leave one consonant as onset of next syllable; cut after first gap consonant
        if len(gap) == 0:
            cut = vpos[k] + 1
        else:
            cut = vpos[k] + 1 + max(0, len(gap) - 1)
        cuts.append(cut)
    cuts.append(len(w))
    return [w[cuts[i]:cuts[i + 1]] for i in range(len(cuts) - 1)]


def stress_syllable(sylls):
    """penultimate stress (Latin default, #388); if 1 syllable, that one."""
    n = len(sylls)
    return max(0, n - 2) if n >= 2 else 0


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    full = load.dense_stream()
    c6 = Counter(full[i:i+6] for i in range(len(full)-5))
    cand = sorted([g for g, v in c6.items() if v >= 15], key=lambda g: -c6[g])
    def g4(s): return set(s[i:i+4] for i in range(len(s)-3))
    NAMES = []
    for v in cand:
        if all(not (g4(v) & g4(u)) for u in NAMES):
            NAMES.append(v)
        if len(NAMES) >= 30:
            break

    # vowel melodies
    melo = Counter("".join(c for c in w if c in VOW) for w in NAMES).most_common(8)
    # consonant inventory (the articulators)
    cons = Counter(c for w in NAMES for c in w if c not in VOW).most_common(10)
    # vowel inventory
    vowc = Counter(c for w in NAMES for c in w if c in VOW).most_common()

    recite = []
    for w in NAMES[:16]:
        s = syllabify(w)
        si = stress_syllable(s)
        recite.append({"name": w, "syllables": s, "stress_index": si,
                       "open_ending": w[-1] in VOW, "melody": "".join(c for c in w if c in VOW)})

    out = {
        "vowel_melodies": melo,
        "consonants": cons,
        "vowels": vowc,
        "recite": recite,
        "rules": {
            "tone_vowel": "A",
            "stress": "penúltima (latina)",
            "ending": "vogal aberta, sustentada",
            "chaining": "vizinhos assonam (vogais partilhadas)",
        },
    }
    with open(os.path.join(os.path.dirname(HERE), "viz", "voice.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print("melodias:", melo[:5], flush=True)
    print("consoantes:", cons[:6], flush=True)
    print("vogais:", vowc, flush=True)
    print("exemplo recite:", recite[0], flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
