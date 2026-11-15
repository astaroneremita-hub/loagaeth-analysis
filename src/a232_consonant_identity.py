# -*- coding: utf-8 -*-
"""a232 - is the identity in the CONSONANTS and the chant in the VOWELS?

If the name-register collapses vowels to A (#401), then the names' distinctiveness should
live in the CONSONANTS (high entropy = information) while the VOWELS are low-entropy (A,
redundant = chant overlay). Compare consonant-entropy vs vowel-entropy for the table-names
and for the Call words. A language whose lexical identity is consonantal and whose vowels
carry register/melody.
stdlib only.
"""
import os
import sys
import json
import math
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

DATA = os.path.join(os.path.dirname(HERE), "engine", "data")
VOW = set("AEIOU")


def H(cnt):
    n = sum(cnt.values())
    if not n: return 0
    return -sum((v/n)*math.log2(v/n) for v in cnt.values() if v)


def analyze(words, label):
    vc = Counter(); cc = Counter()
    for w in words:
        for ch in w:
            (vc if ch in VOW else cc)[ch] += 1
    hv = H(vc); hc = H(cc)
    # max possible entropy for each inventory
    hv_max = math.log2(len([x for x in vc])) if vc else 0
    hc_max = math.log2(len([x for x in cc])) if cc else 0
    print(f"{label}:", flush=True)
    print(f"   entropia VOGAIS  = {hv:.3f} bits (de {hv_max:.2f} possíveis; {len(vc)} vogais)  top {vc.most_common(3)}", flush=True)
    print(f"   entropia CONSOANTES = {hc:.3f} bits (de {hc_max:.2f}; {len(cc)} consoantes)  top {cc.most_common(4)}", flush=True)
    print(f"   razão vogal/consoante de entropia = {hv/hc:.2f} (baixo = vogal redundante/melódica)", flush=True)
    return {"H_vowel": round(hv,3), "H_cons": round(hc,3), "H_vowel_max": round(hv_max,2),
            "ratio": round(hv/hc,3) if hc else 0, "n_vowels": len(vc), "n_cons": len(cc)}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    # names
    full = load.dense_stream()
    c6 = Counter(full[i:i+6] for i in range(len(full)-5))
    cand = sorted([g for g, v in c6.items() if v >= 15], key=lambda g: -c6[g])
    def g4(s): return set(s[i:i+4] for i in range(len(s)-3))
    names = []
    for v in cand:
        if all(not (g4(v) & g4(u)) for u in names): names.append(v)
        if len(names) >= 40: break
    # calls
    ch = json.load(open(os.path.join(DATA, "chamadas.json"), encoding="utf-8"))["chamadas"]
    calls = [load.letters(p.get("enoquiano","")) for c in ch for p in (c.get("palavras") or []) if len(load.letters(p.get("enoquiano","")))>=3]

    rn = analyze(names, "NOMES das tabelas (registro invocação)")
    rc = analyze(calls, "CHAMADAS (registro fala)")
    # whole book
    rb = analyze([full], "LIVRO INTEIRO")

    out = {"names": rn, "calls": rc, "book": rb}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "232_consonant_identity.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
