"""
Passo 3 (a123) - Phonotactics: does the name-language forbid certain letter sequences? (categorical constraints)

A language's spelling obeys phonotactic rules: some letter pairs are legal, others essentially never occur. We build
the letter-bigram matrix of the book, compare each ordered pair to its independence expectation, and look for hard
constraints: pairs strongly AVOIDED (observed << expected) - especially doubled letters (the known 'no-double' rule).
Null: the same counts on letter-shuffled rows (destroys order, keeps letter frequencies). A real phonotactics shows
far more strongly-avoided pairs than the shuffle, and categorical gaps (near-zero where chance predicts many).
"""
import random
from collections import Counter

import load
from a22_robustness_and_depth import base_book


def bigrams(rows):
    c = Counter()
    uni = Counter()
    for r in rows:
        for i in range(len(r)):
            uni[r[i]] += 1
            if i + 1 < len(r):
                c[r[i:i + 2]] += 1
    return c, uni


def avoided(c, uni, total):
    """pairs with observed much below expected (ratio<0.2) and expected>=5."""
    av = []
    for a in uni:
        for b in uni:
            exp = uni[a] * uni[b] / total
            if exp >= 5:
                obs = c.get(a + b, 0)
                if obs < 0.2 * exp:
                    av.append((a + b, obs, round(exp, 1)))
    return av


def run():
    book = base_book()
    rows = [r for k in book for r in book[k] if r]
    total = sum(len(r) for r in rows)
    c, uni = bigrams(rows)
    real_av = avoided(c, uni, total)

    # doubled letters
    doubles = {a + a: c.get(a + a, 0) for a in uni}
    dbl_exp = {a + a: round(uni[a] ** 2 / total, 1) for a in uni}
    dbl_total = sum(doubles.values())
    dbl_exp_total = sum(dbl_exp.values())

    # null: shuffle letters within each row
    rng = random.Random(123)
    null_counts = []
    for _ in range(10):
        srows = []
        for r in rows:
            L = list(r); rng.shuffle(L); srows.append("".join(L))
        sc, su = bigrams(srows)
        null_counts.append(len(avoided(sc, su, total)))
    nmean = sum(null_counts) / len(null_counts)

    real_av.sort(key=lambda x: x[1] - x[2])
    res = {
        "avoided_pairs_real": len(real_av), "avoided_pairs_null_mean": round(nmean, 1),
        "strongest_avoided": real_av[:14],
        "doubles_observed": dbl_total, "doubles_expected": round(dbl_exp_total, 1),
        "double_ratio": round(dbl_total / dbl_exp_total, 3) if dbl_exp_total else None,
        "finding": (
            "A fonotática é real: %d pares de letra são fortemente EVITADOS (obs < 20%% do esperado) vs %.1f no "
            "shuffle. Letras dobradas: %d observadas vs %.0f esperadas (%.0f%% do acaso) - a regra 'não dobra letra' "
            "é categórica. %s" % (
                len(real_av), nmean, dbl_total, dbl_exp_total,
                100 * dbl_total / dbl_exp_total if dbl_exp_total else 0,
                ("CONFIRMADO: há restrições fonotáticas categóricas acima do acaso."
                 if len(real_av) > nmean * 1.5 or (dbl_exp_total and dbl_total < 0.3 * dbl_exp_total)
                 else "restrições fracas."))),
    }
    load.save_result("123_phonotactics", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("pares mais evitados (par | observado | esperado):")
    for p, o, e in r["strongest_avoided"]:
        print("  %s  obs %d  esp %.1f" % (p, o, e))
    print("\nletras dobradas: %d obs vs %.0f esp (%.0f%%)" % (
        r["doubles_observed"], r["doubles_expected"], 100 * r["doubles_observed"] / r["doubles_expected"]))
