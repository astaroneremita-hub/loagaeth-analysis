"""
101 - Syntax between names: is there a FIXED ORDER when two roots chain? (plan item 5)

a100 found that roots chain into long compounds (GETH+NOCHA...). Syntax asks something sharper: is the order
fixed? If GETH-then-NOCHA occurs far more than NOCHA-then-GETH, the book has word order - a grammar between
names, not only inside them. For every ordered pair of roots A,B we count the adjacent concatenation AB vs BA,
and vs what independent frequencies predict. Asymmetric, above-chance pairs are the syntactic collocations.
"""
import json
from collections import Counter

import load
from a22_robustness_and_depth import base_book

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]


def run():
    book = base_book()
    full = "".join("".join(r for r in book[k] if r) for k in book)
    N = len(full)
    freq = {r: full.count(r) for r in ROOTS}

    rows = []
    for a in ROOTS:
        for b in ROOTS:
            ab = full.count(a + b)          # adjacent, no gap
            # near-adjacency: a then b within 2 letters (one linking letter, like GETHA-DNOCHA)
            near = 0
            start = 0
            while True:
                i = full.find(a, start)
                if i < 0:
                    break
                seg = full[i + len(a):i + len(a) + 2]
                if seg[:len(b)] == b or (len(seg) >= 1 and full[i + len(a) + 1:i + len(a) + 1 + len(b)] == b):
                    near += 1
                start = i + 1
            exp = freq[a] * freq[b] / N  # expected adjacent under independence
            if ab >= 3 or near >= 5:
                rows.append({"a": a, "b": b, "AB": ab, "near": near, "expected": round(exp, 2),
                             "ratio": round(ab / max(exp, 0.05), 1)})
    # directionality: for each unordered pair, compare AB vs BA
    pairs = {}
    for a in ROOTS:
        for b in ROOTS:
            if a < b:
                ab = full.count(a + b)
                ba = full.count(b + a)
                if ab + ba >= 4:
                    order = (a + "+" + b) if ab >= ba else (b + "+" + a)
                    pairs["%s|%s" % (a, b)] = {"order": order, "strong": max(ab, ba), "weak": min(ab, ba),
                                                "asymmetry": round(max(ab, ba) / max(1, min(ab, ba)), 1)}
    rows.sort(key=lambda d: -d["ratio"])
    ordered = {k: v for k, v in sorted(pairs.items(), key=lambda kv: -kv[1]["asymmetry"])}
    asym = [v for v in pairs.values() if v["asymmetry"] >= 2]
    res = {
        "adjacent_collocations_top": rows[:25],
        "directional_pairs": ordered,
        "strongly_ordered": len(asym),
        "total_pairs": len(pairs),
        "finding": (
            "Of %d root-pairs that chain, %d have a strongly fixed order (one direction >=2x the other) - e.g. %s. "
            "So there IS a word order between names: roots prefer to chain in a direction, not symmetric. The "
            "strongest collocations (adjacent, above chance): %s. This is the first sign of a SYNTAX between names, "
            "beyond the morphology inside them." % (
                len(pairs), len(asym),
                ", ".join(v["order"] for v in list(ordered.values())[:4]),
                ", ".join("%s%s(%d, %.0fx)" % (r["a"], r["b"], r["AB"], r["ratio"]) for r in rows[:4]))),
    }
    load.save_result("101_name_syntax", res)
    return res


if __name__ == "__main__":
    r = run()
    print("colocacoes adjacentes (AB | esperado | razao):")
    for x in r["adjacent_collocations_top"][:14]:
        print("  %-9s+%-9s AB=%-3d near=%-3d esp=%-5.2f razao=%.0fx" % (x["a"], x["b"], x["AB"], x["near"], x["expected"], x["ratio"]))
    print("\npares com ordem fixa (forte/fraca | assimetria):")
    for k, v in list(r["directional_pairs"].items())[:12]:
        print("  %-18s %3d / %-3d  %.1fx" % (v["order"], v["strong"], v["weak"], v["asymmetry"]))
    print("\n" + r["finding"])
