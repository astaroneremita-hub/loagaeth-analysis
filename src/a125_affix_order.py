"""
Passo 9 (a125) - Affix order: is the morphology positional? Does each affix sit on a FIXED side of the root?

A real derivational grammar fixes morpheme position: a prefix is always a prefix, a suffix always a suffix. We take
every attested house name built on a root, split it into prefix + root + suffix, and collect the affix morphemes on
each side. Test: does each affix occur on only ONE side across the lexicon (positionally fixed) far more than if
affixes attached to either side at random? If yes, the name-language has a fixed prefix·root·suffix template - a real
morphological grammar, not free letter-gluing.
"""
import json
import random
from collections import Counter, defaultdict

import load

ROOTS = ["ANTANTOX", "CHASTOR", "GRADAX", "CHADAX", "ANZACH", "NOCHA", "NACHO", "ACLAX", "PHANGE", "GETH"]


def split(name):
    """find the longest root inside; return (prefix, root, suffix) or None."""
    best = None
    for r in ROOTS:
        i = name.find(r)
        if i >= 0 and (best is None or len(r) > len(best[1])):
            best = (name[:i], r, name[i + len(r):])
    return best


def run():
    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))
    pre_side = defaultdict(Counter)   # affix -> {'pre':n,'suf':n}
    prefixes, suffixes = Counter(), Counter()
    templates = Counter()
    decomp = []
    for nm in names:
        sp = split(nm)
        if not sp:
            continue
        pre, root, suf = sp
        decomp.append((pre, root, suf, nm))
        if pre:
            prefixes[pre] += 1
            pre_side[pre]["pre"] += 1
        if suf:
            suffixes[suf] += 1
            pre_side[suf]["suf"] += 1
        templates[(bool(pre), root, bool(suf))] += 1

    # positional fixity: fraction of affix TYPES that occur on only one side
    affixes = set(prefixes) | set(suffixes)
    fixed = sum(1 for a in affixes if not (a in prefixes and a in suffixes))
    real_fix = fixed / len(affixes) if affixes else 0

    # null: reassign each affix token to a random side, recompute fixity
    tokens = [("pre", a) for a in prefixes.elements()] + [("suf", a) for a in suffixes.elements()]
    rng = random.Random(125)
    nulls = []
    for _ in range(500):
        sides = defaultdict(set)
        for _, a in tokens:
            sides[a].add(rng.choice(("pre", "suf")))
        nf = sum(1 for a in sides if len(sides[a]) == 1) / len(sides)
        nulls.append(nf)
    nmean = sum(nulls) / len(nulls)
    ge = sum(1 for x in nulls if x >= real_fix)
    p = (ge + 1) / (len(nulls) + 1)

    res = {
        "names_decomposed": len(decomp),
        "top_prefixes": prefixes.most_common(10),
        "top_suffixes": suffixes.most_common(10),
        "affix_types": len(affixes), "positional_fixity_real": round(real_fix, 3),
        "positional_fixity_null": round(nmean, 3), "p": round(p, 4),
        "example_decomp": [("%s-%s-%s" % (p or "0", r, s or "0"), nm) for p, r, s, nm in decomp[:14]],
        "finding": (
            "Dos %d nomes decompostos, %.0f%% dos tipos de afixo ocorrem num LADO SÓ (prefixo xor sufixo) vs %.0f%% "
            "no acaso (p=%.3f). %s Prefixos: %s. Sufixos: %s." % (
                len(decomp), real_fix * 100, nmean * 100, p,
                ("CONFIRMADO: a morfologia é posicional - template fixo prefixo·raiz·sufixo."
                 if p < 0.05 and real_fix > nmean else
                 "afixos não têm lado fixo claro acima do acaso."),
                ", ".join(a for a, _ in prefixes.most_common(5)),
                ", ".join(a for a, _ in suffixes.most_common(5)))),
    }
    load.save_result("125_affix_order", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("fixidez posicional: real %.0f%% vs null %.0f%% (p=%.3f)" % (
        r["positional_fixity_real"] * 100, r["positional_fixity_null"] * 100, r["p"]))
    print("\nexemplos de decomposição (prefixo-raiz-sufixo):")
    for d, nm in r["example_decomp"]:
        print("  %-22s  (%s)" % (d, nm))
