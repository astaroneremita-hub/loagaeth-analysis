"""
a136 - Are the prefixes distinct grammatical OPERATORS? Test by FORCE (not computable from letters -> no circularity).

a125 gave prefixes AD-/NO-/A-/ZI-/AX-; a135 showed vowels carry elemental mode (but partly mechanical). Force comes
from a name's recurrence/attestation, independent of the letter-element arithmetic - so if prefix predicts force (or
ubiquity), the prefix is a real derivational operator with a measurable effect, not just letters. We group names by
prefix and test whether prefix explains force/ubiquity variance beyond a label-shuffle null, and characterize each
prefix's typical effect (its grammatical value: does AD- weaken, does NO- strengthen?).
"""
import json
import random
import statistics
from collections import defaultdict

import load

ROOTS = ["ANTANTOX", "CHASTOR", "GRADAX", "CHADAX", "ANZACH", "NOCHA", "NACHO", "ACLAX", "PHANGE", "GETH"]


def prefix(name):
    for r in ROOTS:
        i = name.find(r)
        if i > 0:
            return name[:i]
    return ""


def between_var(groups, grand):
    return sum(len(v) * (statistics.mean(v) - grand) ** 2 for v in groups.values() if v)


def run():
    tr = json.load(open(load.ROOT + "/viz/name_translation.json", encoding="utf-8"))["names"]
    rows = []
    for x in tr:
        pre = prefix(x["name"])
        rows.append((pre, x.get("force"), x.get("tables")))

    # force by prefix (prefixes with >=2 names)
    by_force = defaultdict(list)
    by_tab = defaultdict(list)
    for pre, fc, tb in rows:
        if pre:
            if fc:
                by_force[pre].append(fc)
            if tb is not None:
                by_tab[pre].append(tb)
    bf = {p: v for p, v in by_force.items() if len(v) >= 2}
    allf = [f for v in bf.values() for f in v]
    grand = statistics.mean(allf) if allf else 0
    real_bv = between_var(bf, grand)

    # null: shuffle force labels across the same prefixed names
    labels = [(p, f) for p, v in bf.items() for f in v]
    prefs = [p for p, _ in labels]
    forces = [f for _, f in labels]
    rng = random.Random(136)
    nulls = []
    for _ in range(1000):
        rng.shuffle(forces)
        g = defaultdict(list)
        for p, f in zip(prefs, forces):
            g[p].append(f)
        nulls.append(between_var(g, grand))
    ge = sum(1 for x in nulls if x >= real_bv)
    pval = (ge + 1) / (len(nulls) + 1)

    pref_stats = {}
    for p in sorted(bf, key=lambda k: -statistics.mean(bf[k])):
        pref_stats[p] = {"n": len(bf[p]), "mean_force": round(statistics.mean(bf[p])),
                         "mean_tables": round(statistics.mean(by_tab.get(p, [0])), 1)}

    res = {
        "prefixes_tested": len(bf), "between_force_var_real": round(real_bv),
        "p": round(pval, 4), "prefix_stats": pref_stats,
        "finding": (
            "Força média por prefixo difere %s do acaso (p=%.3f). %s Valores: %s" % (
                "ACIMA" if pval < 0.05 else "~igual", pval,
                ("CONFIRMADO: os prefixos são operadores derivacionais distintos - cada um modula a força do poder de "
                 "um jeito próprio (não é só letra, pois força independe da aritmética elemental)."
                 if pval < 0.05 else
                 "os prefixos NÃO diferem em força acima do acaso - não são operadores de força distintos; a derivação"
                 " muda forma, não potência medível por prefixo."),
                "; ".join("%s-=força %d (n%d)" % (p, s["mean_force"], s["n"]) for p, s in list(pref_stats.items())[:6]))),
    }
    load.save_result("136_prefix_operators", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("prefixo | n | força média | folhas média:")
    for p, s in r["prefix_stats"].items():
        print("  %-4s n=%d  força %d  folhas %.1f" % (p + "-", s["n"], s["mean_force"], s["mean_tables"]))
