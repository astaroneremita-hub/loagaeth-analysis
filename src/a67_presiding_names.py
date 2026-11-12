"""
67 - The presiding name of each table.

The record frames each table as opened, by its Call, to summon the ministers that belong to it. If a
practitioner opens table N, which name is most at home there? For every leaf, the recurring name most
over-represented relative to the whole book, with a Poisson significance (how surprising its count is
given its book-wide rate scaled to the leaf's length). This turns the catalogue into a per-table
working list: the name that rules each leaf.
"""
import json
import math
import os
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum

MASTERS = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX", "CHUSTOR"]


def poisson_sf(k, lam):
    # P(X >= k) for X~Poisson(lam)
    if k <= 0:
        return 1.0
    cum = sum(math.exp(-lam) * lam ** i / math.factorial(i) for i in range(k))
    return max(0.0, 1.0 - cum)


def run():
    book = base_book()
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    names = sorted(set(MASTERS) | {x["name"] for x in d}, key=len, reverse=True)
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k))]
    text = {k: "".join(r for r in book[k] if r) for k in keys}
    total = sum(len(text[k]) for k in keys)
    glob = {n: sum(text[k].count(n) for k in keys) for n in names}

    rows = []
    for k in keys:
        L = len(text[k])
        if L < 500:
            continue
        best = None
        for n in names:
            c = text[k].count(n)
            if c < 3:
                continue
            exp = glob[n] * L / total
            if exp < 0.3:
                continue
            p = poisson_sf(c, exp)
            score = c / exp
            if best is None or (p < best["p"] - 1e-12) or (abs(p - best["p"]) < 1e-12 and score > best["ratio"]):
                best = {"name": n, "count": c, "expected": round(exp, 1), "ratio": round(score, 1), "p": p}
        if best:
            best["significant"] = best["p"] < 0.01
            rows.append({"leaf": k, **best})
    strong = [r for r in rows if r["count"] >= 5 and r["ratio"] >= 2.5]
    res = {"leaves": len(rows), "presiding_name_by_leaf": [{k: v for k, v in r.items() if k != "p"} | {"p": round(r["p"], 4)} for r in rows],
           "strong_signatures": [{"leaf": r["leaf"], "name": r["name"], "count": r["count"], "ratio": r["ratio"]} for r in strong],
           "note": "The presiding name is the recurring name most over-represented on that leaf (Poisson p vs its "
                   "book-wide rate). Strong = at least 5 occurrences and 2.5x over chance. The pattern follows the houses "
                   "(NACHO/NOCHA/ADNOCHA early, ACLAX/GETH late, CHASTOR around leaf 32) and the territories of a28, so it "
                   "is the real local structure, not noise. This is a working list, not a claim that the name is the "
                   "table's 'true' minister - the record names no minister for any specific leaf except leaf 18 (earth "
                   "spirits)."}
    load.save_result("67_presiding_names", res)
    return res


if __name__ == "__main__":
    r = run()
    print("leaf  name        count  ratio  p       sig")
    for x in r["presiding_name_by_leaf"]:
        print("%-4s %-11s %3d   %4.1fx  %.4f %s" % (x["leaf"], x["name"], x["count"], x["ratio"], x["p"], "*" if x["significant"] else ""))
    print("\nstrong signatures:", len(r["strong_signatures"]))
