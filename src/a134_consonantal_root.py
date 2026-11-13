"""
a134 - Typology: is the name-language ROOT-AND-PATTERN (Semitic-type)? Consonantal roots + vocalic melody.

Clue: NOCHA (cons N-CH, vowels O-A) vs NACHO (cons N-CH, vowels A-O) - same consonants, different vowel pattern.
In Semitic morphology the consonants carry the root sense and the vowels inflect it. We strip vowels from every
attested name, group by the consonant skeleton, and count skeletons shared by several names that differ only in
vowels. Null: random strings with the same letter frequencies. If real names cluster by consonant skeleton far
beyond chance, the Loagaeth name-language is root-and-pattern - the vowels are grammatical, the consonants lexical.
"""
import json
import random
import unicodedata
from collections import defaultdict, Counter

import load

VOWELS = set("AEIOUY")


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def skeleton(w):
    return "".join(c for c in w if c not in VOWELS)


def vowels_of(w):
    return "".join(c for c in w if c in VOWELS)


def cluster_stats(names):
    groups = defaultdict(list)
    for w in names:
        s = skeleton(w)
        if len(s) >= 2:
            groups[s].append(w)
    multi = {s: ws for s, ws in groups.items() if len(ws) >= 2}
    shared = sum(len(ws) for ws in multi.values())
    return len(multi), shared, multi


def run():
    names = [da(w) for w in json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))]
    nmulti, nshared, multi = cluster_stats(names)
    frac = nshared / len(names)

    # null: random strings with same letter frequencies and same lengths
    allletters = "".join(names)
    pool = list(allletters)
    lens = [len(w) for w in names]
    rng = random.Random(134)
    nulls = []
    for _ in range(300):
        rng.shuffle(pool)
        rnames, p = [], 0
        for L in lens:
            rnames.append("".join(pool[p:p + L])); p += L
        _, sh, _ = cluster_stats(rnames)
        nulls.append(sh / len(names))
    nmean = sum(nulls) / len(nulls)
    nmax = max(nulls)
    sd = (sum((x - nmean) ** 2 for x in nulls) / len(nulls)) ** 0.5
    z = (frac - nmean) / sd if sd else 0

    # vowel-melody patterns across the biggest families
    big = sorted(multi.items(), key=lambda kv: -len(kv[1]))[:8]
    families = [{"skeleton": s, "names": ws, "vowels": [vowels_of(w) for w in ws]} for s, ws in big]
    # which vowel melodies are most common overall
    melodies = Counter(vowels_of(w) for w in names if len(vowels_of(w)) >= 2).most_common(10)

    res = {
        "names": len(names), "skeletons_shared": nmulti, "names_in_shared": nshared,
        "shared_fraction_real": round(frac, 3), "shared_fraction_null": round(nmean, 3),
        "null_max": round(nmax, 3), "z": round(z, 1),
        "families": families[:8], "top_melodies": melodies,
        "finding": (
            "%d dos %d nomes partilham um ESQUELETO CONSONANTAL com outro nome (vogais diferentes) - %.0f%% vs %.0f%% "
            "no acaso (máx %.0f%%, z=%.1f). %s Melodias vocálicas mais comuns: %s." % (
                nshared, len(names), frac * 100, nmean * 100, nmax * 100, z,
                ("CONFIRMADO: a língua é RAIZ-E-PADRÃO (tipo semítico) - a raiz consonantal carrega o sentido, as "
                 "vogais inflexionam."
                 if frac > nmax and z >= 3 else
                 "agrupamento consonantal ~ acaso: não é claramente raiz-e-padrão."),
                ", ".join("%s(%s)" % (m, n) for m, n in melodies[:5]))),
    }
    load.save_result("134_consonantal_root", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("famílias por esqueleto consonantal (raiz | nomes | vogais):")
    for f in r["families"]:
        print("  %-8s %s" % (f["skeleton"], "  ".join("%s[%s]" % (w, vowels_of(w)) for w in f["names"][:5])))
