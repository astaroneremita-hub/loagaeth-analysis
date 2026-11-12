"""
119 - Do the core names have a fixed SEAT across the 36 sheets, or do they wander? (positional paradigm)

a118 showed NOCHA/GETH/ANZACH recur in nearly every table. Now: when a name recurs across sheets, does it sit in the
SAME positional zone (a registered template - each power has its seat) or scatter uniformly? For each core name we
collect the (row, col) start of every straight row/column occurrence across all 36 square tables and measure how
concentrated those positions are (mean pairwise Chebyshev distance), comparing to the same number of uniformly
random positions. A name far more concentrated than random has a seat; if names scatter like random, the sheets are
not aligned and the book is 36 independent draws from one lexicon.
"""
import json
import random
import statistics

import load
from a22_robustness_and_depth import base_book


def square_grids(book):
    out = []
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            out.append(g)
    return out


def positions(grids, w):
    """start (row,col) of straight row & column occurrences of w across all grids."""
    pos = []
    R = 49
    for g in grids:
        for r in range(R):
            row = g[r]
            s = 0
            while True:
                i = row.find(w, s)
                if i < 0:
                    break
                pos.append((r, i))
                s = i + 1
        for c in range(R):
            col = "".join(g[r][c] for r in range(R))
            s = 0
            while True:
                i = col.find(w, s)
                if i < 0:
                    break
                pos.append((i, c))
                s = i + 1
    return pos


def mean_pair_dist(pts):
    if len(pts) < 2:
        return None
    ds = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            ds.append(max(abs(pts[i][0] - pts[j][0]), abs(pts[i][1] - pts[j][1])))
    return statistics.mean(ds)


def run():
    book = base_book()
    grids = square_grids(book)
    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))
    rng = random.Random(119)

    results = []
    for w in names:
        pts = positions(grids, w)
        if len(pts) < 8:
            continue
        real = mean_pair_dist(pts)
        nulls = []
        for _ in range(200):
            rp = [(rng.randrange(49), rng.randrange(49)) for _ in pts]
            nulls.append(mean_pair_dist(rp))
        nm = statistics.mean(nulls)
        le = sum(1 for x in nulls if x <= real)
        p = (le + 1) / (len(nulls) + 1)
        results.append({"name": w, "occ": len(pts), "real_spread": round(real, 1),
                        "null_spread": round(nm, 1), "p": round(p, 4),
                        "seated": real < nm and p < 0.05})
    results.sort(key=lambda x: x["p"])
    seated = [r for r in results if r["seated"]]
    res = {
        "names_tested": len(results), "seated_count": len(seated),
        "seated_sample": [(r["name"], r["occ"], r["real_spread"], r["null_spread"], r["p"]) for r in seated[:15]],
        "finding": (
            "%d de %d nomes-núcleo têm ASSENTO posicional (ocorrem concentrados numa zona através das folhas, não "
            "espalhados; p<0.05). %s. Se a maioria tem assento, as 49 folhas são um template registrado - cada nome "
            "num lugar seu. Se poucos, as folhas são sorteios independentes do mesmo léxico." % (
                len(seated), len(results),
                "Exemplos: " + ", ".join(r["name"] for r in seated[:6]) if seated else "Nenhum caso forte")),
    }
    load.save_result("119_name_seats", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("nome | ocorrências | espalhamento real vs null | p (menor = mais assentado)")
    for nm, occ, rs, ns, p in r["seated_sample"]:
        print("  %-12s %3d  real %.1f vs null %.1f  p=%.4f" % (nm, occ, rs, ns, p))
