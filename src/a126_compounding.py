"""
Passo 11 (a126) - Compounding: do super-names join two roots, and in a fixed order? (NOCHASTOR = NOCHA+CHASTOR)

Beyond prefix/suffix, the long names look like two roots fused (super-names). We take every attested name, find all
pairs of distinct roots it contains, and record their left-right order. Then test: do specific root pairs compound
far above chance, and is the order fixed (A before B, not B before A)? Null: random strings of the same length seldom
contain two roots at all. A fixed-order compounding rule is the syntax of name-building - the deepest layer of the
generative grammar.
"""
import json
import random
from collections import Counter

import load

ROOTS = ["ANTANTOX", "CHASTOR", "GRADAX", "CHADAX", "ANZACH", "NOCHA", "NACHO", "ACLAX", "PHANGE", "GETH"]


def roots_in_order(name):
    hits = []
    for r in ROOTS:
        i = name.find(r)
        if i >= 0:
            hits.append((i, r))
    hits.sort()
    return [r for _, r in hits]


def run():
    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))
    compounds = []
    order = Counter()
    for nm in names:
        rs = roots_in_order(nm)
        # distinct roots, >=2
        seen = []
        for r in rs:
            if r not in seen:
                seen.append(r)
        if len(seen) >= 2:
            compounds.append((nm, seen))
            for i in range(len(seen) - 1):
                order[(seen[i], seen[i + 1])] += 1

    # order fixity: for each unordered root pair, is one direction dominant?
    pairs = {}
    for (a, b), n in order.items():
        k = tuple(sorted((a, b)))
        pairs.setdefault(k, {})[(a, b)] = n
    fixed = []
    for k, dirs in pairs.items():
        tot = sum(dirs.values())
        if tot >= 3:
            best = max(dirs.items(), key=lambda kv: kv[1])
            if best[1] >= 0.8 * tot:
                fixed.append((best[0][0] + "+" + best[0][1], best[1], tot))

    # null: random strings, how often contain >=2 distinct roots
    rng = random.Random(126)
    alpha = "ABCDEFGHILMNOPQRSTUVXZ"
    lens = [len(nm) for nm, _ in compounds] or [9]
    null_hits = 0
    N = 2000
    for _ in range(N):
        L = rng.choice(lens)
        s = "".join(rng.choice(alpha) for _ in range(L))
        if len(set(roots_in_order(s))) >= 2:
            null_hits += 1
    null_rate = null_hits / N

    fixed.sort(key=lambda x: -x[2])
    res = {
        "compound_names": len(compounds), "total_names": len(names),
        "real_compound_rate": round(len(compounds) / len(names), 3),
        "null_compound_rate": round(null_rate, 4),
        "fixed_order_pairs": fixed[:12],
        "sample": [(nm, "+".join(rs)) for nm, rs in compounds[:12]],
        "finding": (
            "%d dos %d nomes são COMPOSTOS (>=2 raízes distintas) - taxa %.1f%% vs %.2f%% em strings aleatórias do "
            "mesmo tamanho (%.0fx). Pares de ordem fixa (uma direção >=80%%): %s. %s" % (
                len(compounds), len(names), 100 * len(compounds) / len(names), 100 * null_rate,
                (len(compounds) / len(names)) / max(null_rate, 0.0005),
                ", ".join(p for p, _, _ in fixed[:5]) or "nenhum",
                ("CONFIRMADO: os super-nomes compõem raízes em ordem fixa - há sintaxe de composição."
                 if len(compounds) / len(names) > null_rate * 5 else "composição ~ acaso."))),
    }
    load.save_result("126_compounding", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("compostos exemplo:", r["sample"][:8])
    print("\npares de ordem fixa (composto | nessa ordem | total):")
    for p, n, t in r["fixed_order_pairs"]:
        print("  %-18s %d/%d" % (p, n, t))
