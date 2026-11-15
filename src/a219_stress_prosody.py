# -*- coding: utf-8 -*-
"""a219 - sound axis: the stress marks on leaf 1. Does the accent fall in a fixed place?

The diary ordered stress marks for speaking leaf 1 (a54/STATE_AND_NEXT F). The raw text keeps
them (alídes, zálpala, ámphe). If recitation follows a rule, the accent should sit in a fixed
syllable - e.g. always penultimate (Latin) or always final. Extract accented words, find the
stressed vowel-group's position from the START and from the END; is the distribution peaked
(a rule) or flat (free)?

stdlib only.
"""
import os
import sys
import re
import json
import unicodedata
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

VOW = set("AEIOU")
ACUTE = "́"


def is_acc(ch):
    d = unicodedata.normalize("NFD", ch)
    return any(c == ACUTE for c in d)


def base(ch):
    return unicodedata.normalize("NFD", ch)[0].upper()


def vowel_groups_with_stress(word):
    """return (n_groups, stressed_group_index_from_1) or (n,None)."""
    nfd = unicodedata.normalize("NFD", word)
    groups = []  # each: list of (baseletter, is_stressed)
    cur = []
    stressed_idx = None
    letters = []
    # recombine base+accent into (base, acc)
    i = 0
    seq = []
    while i < len(nfd):
        c = nfd[i]
        acc = False
        if i + 1 < len(nfd) and nfd[i+1] == ACUTE:
            acc = True; i += 1
        seq.append((c.upper(), acc))
        i += 1
    gi = 0
    in_v = False
    for (b, acc) in seq:
        if b in VOW:
            if not in_v:
                gi += 1; in_v = True
            if acc:
                stressed_idx = gi
        else:
            in_v = False
    return gi, stressed_idx


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    lv = load.leaves()
    from_start = Counter()
    from_end = Counter()
    nwords = 0
    acc_words = 0
    examples = []
    for key in ("1a", "1b"):
        for row in lv.get(key, []):
            for tok in row.split():
                w = re.sub(r"[^A-Za-zÁÉÍÓÚáéíóú́]", "", tok)
                if len(re.sub(r"[^A-Za-z]", "", unicodedata.normalize("NFD", w))) < 3:
                    continue
                nwords += 1
                n, s = vowel_groups_with_stress(w)
                if s is not None and n >= 2:
                    acc_words += 1
                    from_start[s] += 1
                    from_end[n - s + 1] += 1  # 1 = last syllable (oxytone), 2 = penult...
                    if len(examples) < 12:
                        examples.append((tok, n, s))
    tot = acc_words
    print(f"palavras: {nwords}, com acento marcado (>=2 sílabas): {acc_words}", flush=True)
    print("posição da tônica A PARTIR DO FIM (1=última/oxítona, 2=penúltima/paroxítona, 3=antepenúltima):")
    for k in sorted(from_end):
        print(f"   {k}: {from_end[k]:4d}  ({100*from_end[k]//tot}%)", flush=True)
    print("posição a partir do início:")
    for k in sorted(from_start):
        print(f"   {k}: {from_start[k]:4d}  ({100*from_start[k]//tot}%)", flush=True)
    print("exemplos:", examples[:8], flush=True)
    result = {"n_words": nwords, "accented_words": acc_words,
              "from_end": dict(from_end), "from_start": dict(from_start),
              "examples": examples}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "219_stress_prosody.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
