# -*- coding: utf-8 -*-
"""a231 - are the Calls and the table-names the SAME language phonetically?

Apply the sound profile (CV-alternation, max consonant cluster, vowel-final rate, vowel
melody, vowel A-dominance) to the Call vocabulary vs the recurring table-names. If they
match, the whole Enochian corpus is one chant-language; if not, they are distinct registers.
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

DATA = os.path.join(os.path.dirname(HERE), "engine", "data")
VOW = set("AEIOU")


def profile(words):
    words = [w for w in words if len(w) >= 3]
    n = len(words)
    cvalt = 0; mxcl = 0; vfin = 0; vowtot = 0; lettot = 0
    vc = Counter(); melo = Counter()
    for w in words:
        for i in range(len(w)-1):
            if (w[i] in VOW) != (w[i+1] in VOW): cvalt += 1
        run = 0
        for c in w:
            if c in VOW: run = 0
            else: run += 1; mxcl += 0
        # max cluster per word
        mc = 0; cur = 0
        for c in w:
            if c in VOW: cur = 0
            else: cur += 1; mc = max(mc, cur)
        mxcl += mc
        if w[-1] in VOW: vfin += 1
        for c in w:
            lettot += 1
            if c in VOW: vowtot += 1; vc[c] += 1
        melo["".join(c for c in w if c in VOW)] += 1
    tot_pairs = sum(len(w)-1 for w in words)
    return {
        "n": n,
        "cv_alt": round(cvalt/tot_pairs, 3) if tot_pairs else 0,
        "max_cluster": round(mxcl/n, 2) if n else 0,
        "vowel_final": round(vfin/n, 3) if n else 0,
        "vowel_ratio": round(vowtot/lettot, 3) if lettot else 0,
        "A_share_of_vowels": round(vc["A"]/sum(vc.values()), 3) if vc else 0,
        "top_melodies": melo.most_common(5),
        "top_vowels": vc.most_common(),
    }


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    # Call words (angelical)
    ch = json.load(open(os.path.join(DATA, "chamadas.json"), encoding="utf-8"))["chamadas"]
    callwords = []
    for c in ch:
        for p in (c.get("palavras") or []):
            w = load.letters(p.get("enoquiano", ""))
            if len(w) >= 3:
                callwords.append(w)
    # table recurring names
    full = load.dense_stream()
    c6 = Counter(full[i:i+6] for i in range(len(full)-5))
    cand = sorted([g for g, v in c6.items() if v >= 15], key=lambda g: -c6[g])
    def g4(s): return set(s[i:i+4] for i in range(len(s)-3))
    names = []
    for v in cand:
        if all(not (g4(v) & g4(u)) for u in names): names.append(v)
        if len(names) >= 40: break

    pc = profile(callwords); pn = profile(names)
    print(f"Chamadas (n={pc['n']}):", flush=True)
    for k in ("cv_alt", "max_cluster", "vowel_final", "vowel_ratio", "A_share_of_vowels"):
        print(f"   {k:20s} Chamadas={pc[k]}   Nomes={pn[k]}", flush=True)
    print(f"   melodias Chamadas: {pc['top_melodies']}", flush=True)
    print(f"   melodias Nomes:    {pn['top_melodies']}", flush=True)
    print(f"   vogais Chamadas: {pc['top_vowels'][:5]}", flush=True)
    print(f"   vogais Nomes:    {pn['top_vowels'][:5]}", flush=True)

    out = {"calls": pc, "names": pn}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "231_call_vs_name_phonetics.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
