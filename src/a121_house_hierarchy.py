"""
121 - Internal hierarchy of the dominant house: the generative matrix root and the derivation tree.

a120 found CHASTOR-ACLAX-NOCHA travel together. Here we ask: within this house, is there a single MATRIX root that
seeds the others, and do the longer derived names still beat chance (so the whole family tree is attested, not just
the bare roots)? For every house name we measure table-ubiquity and enrichment over same-length random strings, group
by derivation depth (letters added beyond the matrix root), and find the matrix as the short root contained in the
most house names. If deep derivatives still beat their length-matched null, the house is a real generative hierarchy
(matrix -> affixed children -> compounded grandchildren), each layer a genuine attested name.
"""
import json
import random

import load
from a22_robustness_and_depth import base_book

CORES = ["NOCHA", "CHASTOR", "ACLAX", "GETH", "NACHO", "ANZACH", "CHADAX", "ANTANTOX", "GRADAX", "PHANGE"]


def square_grids(book):
    out = []
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            out.append(g)
    return out


def lines(g):
    R = 49
    out = [g[r] for r in range(R)]
    out += ["".join(g[r][c] for r in range(R)) for c in range(R)]
    for s in range(R):
        out.append("".join(g[s + k][k] for k in range(R - s)))
        if s:
            out.append("".join(g[k][s + k] for k in range(R - s)))
    return out


def run():
    book = base_book()
    grids = square_grids(book)
    T = len(grids)
    texts = ["\n".join(lines(g)) for g in grids]
    rtexts = ["\n".join(l[::-1] for l in lines(g)) for g in grids]

    def tcount(w):
        return sum(1 for i in range(T) if w in texts[i] or w in rtexts[i])

    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))
    house = [w for w in names if any(cr in w for cr in CORES)]

    # matrix = core root contained in the most house names
    seed_counts = {cr: sum(1 for w in house if cr in w) for cr in CORES}
    matrix = max(seed_counts, key=seed_counts.get)

    rng = random.Random(121)
    alpha = "ABCDEFGHILMNOPQRSTUVXZ"
    nullL = {}
    for L in range(4, 13):
        nullL[L] = sum(tcount("".join(rng.choice(alpha) for _ in range(L))) for _ in range(15)) / 15

    def depth(w):
        # shortest core contained; depth = extra letters beyond it
        best = min((len(cr) for cr in CORES if cr in w), default=len(w))
        return max(0, len(w) - best)

    rows = []
    for w in house:
        t = tcount(w)
        base = nullL.get(len(w), 0.1)
        rows.append({"name": w, "len": len(w), "depth": depth(w), "tables": t,
                     "null": round(base, 2), "enrich": round(t / max(base, 0.05), 0), "real": t > base * 3})
    rows.sort(key=lambda x: -x["tables"])

    # by depth bucket: fraction still real
    buckets = {}
    for r in rows:
        d = "0 (raiz)" if r["depth"] == 0 else ("1-2" if r["depth"] <= 2 else ("3-4" if r["depth"] <= 4 else "5+"))
        buckets.setdefault(d, []).append(r)
    depth_summary = {}
    for d, rs in buckets.items():
        depth_summary[d] = {"n": len(rs), "real_frac": round(sum(1 for r in rs if r["real"]) / len(rs), 2),
                            "mean_tables": round(sum(r["tables"] for r in rs) / len(rs), 1)}

    res = {
        "matrix_root": matrix, "matrix_seeds": seed_counts[matrix], "house_size": len(house),
        "matrix_tables": tcount(matrix),
        "by_depth": depth_summary,
        "tree_top": [(r["name"], r["depth"], r["tables"], int(r["enrich"])) for r in rows[:18]],
        "finding": (
            "Matriz geradora da casa = %s (semeia %d dos %d nomes, em %d/%d folhas). Por profundidade de derivação, a "
            "fração de nomes que ainda bate o acaso do próprio tamanho: %s. Se as camadas profundas seguem reais, a "
            "casa é uma hierarquia gerativa atestada camada a camada (matriz %s -> filhos afixados -> netos "
            "compostos), não só raízes soltas." % (
                matrix, seed_counts[matrix], len(house), tcount(matrix), T,
                "; ".join("%s: %.0f%% reais, média %.1f folhas" % (d, v["real_frac"] * 100, v["mean_tables"])
                          for d, v in sorted(depth_summary.items())), matrix)),
    }
    load.save_result("121_house_hierarchy", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("ÁRVORE (nome | profundidade | folhas/%d | enriquecimento):" % 36)
    for nm, d, t, e in r["tree_top"]:
        print("  %-13s d%d  %2d  %dx" % (nm, d, t, e))
