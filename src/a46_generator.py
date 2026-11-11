"""
46 - Analysis by synthesis: write a false book from the rules we measured, and see what it lacks.

Three machines write the row-written tables (2-24) again, side by side, line lengths kept:

  G3   one letter model, three letters of context, for the whole book
  G5   one letter model, five letters of context, for the whole book
  G5L  five letters of context, a model per side trained on that side and its three neighbours on
       each hand (the "vocabulary of the leaf" found in a42-a43)

Each false book goes through the measurements made on the real one. What a machine reproduces is
explained by its rule; what none reproduces is the residue - the place to look next.
"""
import json
import random
import statistics

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a39_long_repeats import repeats
from a40_formulas import variants14
from a43_recency import echo

MASTERS = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"]


def measures(sides, rng):
    lines = [r for ls in sides for r in ls]
    S = "|".join(lines)

    def echo_ratio():
        def stat(fs):
            a = b = 0
            for ls in fs:
                for x, y in echo(ls, 4, 5):
                    a += x
                    b += y
            return a / max(1, b)
        real = stat(sides)
        nul = []
        for _ in range(20):
            sh = []
            for ls in sides:
                t = ls[:]
                rng.shuffle(t)
                sh.append(t)
            nul.append(stat(sh))
        return real / statistics.mean(nul)
    sets = [{r[i:i + 8] for r in ls for i in range(len(r) - 7)} for ls in sides]

    def share(d):
        return 1000 * statistics.mean(len(sets[i] & sets[i + d]) / max(1, min(len(sets[i]), len(sets[i + d]))) for i in range(len(sets) - d))
    return {"repeated strings of 12": len(repeats(lines, 12)), "repeated strings of 14": len(repeats(lines, 14)),
            "one-letter variants of 14": len(variants14(lines)),
            "the 12 master names": sum(S.count(n) for n in MASTERS), "CHASTOR": S.count("CHASTOR"), "GETHACLAX": S.count("GETHACLAX"),
            "doubled letters": sum(a == b for r in lines for a, b in zip(r, r[1:])),
            "distinct strings of 6": len({r[i:i + 6] for r in lines for i in range(len(r) - 5)}),
            "echo 1-4 lines / shuffled": round(echo_ratio(), 3),
            "shared with next side (per 1000)": round(share(1), 1), "shared 20 sides away (per 1000)": round(share(20), 1)}


def write(models, sides, rng):
    return [[models(i).sample(len(r), rng) for r in ls] for i, ls in enumerate(sides)]


def run():
    rng = random.Random(46)
    book = base_book()
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 2 <= tnum(k) <= 24]
    sides = [[r for r in book[k] if r] for k in keys]
    flat = [r for ls in sides for r in ls]
    g3 = CharLM(3, alpha=0.01).fit(flat)
    g5 = CharLM(5, alpha=0.001).fit(flat)
    local = [CharLM(5, alpha=0.001).fit([r for ls in sides[max(0, i - 3):i + 4] for r in ls]) for i in range(len(sides))]
    res = {"book": measures(sides, rng)}
    for name, f in (("G3", lambda i: g3), ("G5", lambda i: g5), ("G5L", lambda i: local[i])):
        runs = [measures(write(f, sides, rng), rng) for _ in range(3)]
        res[name] = {k: round(statistics.mean(r[k] for r in runs), 2) for k in runs[0]}
    load.save_result("46_generator", res)
    return res


if __name__ == "__main__":
    r = run()
    for k in r["book"]:
        print(f"{k:36s}", *(f"{n}: {r[n][k]:>9}" for n in ("book", "G3", "G5", "G5L")))
