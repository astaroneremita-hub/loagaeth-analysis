"""
56 - "They are but one Name": how few roots generate the recurring names?

The diary (Il, 29 April 1583): "every letter here bringeth furth the Names of God: But ... they are
but one Name." A direct, testable reading: under the transformations this study already measured -
prefixes (AD-, NO-, NE-, NI-, ZI-, I-, A-, AX-, AL-), suffixes (-A, -AL, -AD, -H, -HA, -R, -TO,
-TOR, -P), and one interior vowel swap (A/O/E) - how few roots does it take to generate the whole set
of recurring names? And is that fewer than the same rules reach on a surrogate set of names of the
same lengths?

Not a claim that the names mean one thing; a measure of how far the family rules compress the set.
"""
import json
import os
import random
import statistics

import load

PREF = ["AD", "NO", "NE", "NI", "ZI", "AX", "AL", "A", "I", "O", "Z", "H"]
SUF = ["TOR", "TO", "HA", "AL", "AD", "AN", "A", "H", "R", "P", "X"]
VSET = "AOE"


def strip_affixes(w):
    """Return the set of forms reachable by removing any one prefix and/or any one suffix (>=3 left)."""
    out = {w}
    for p in PREF:
        if w.startswith(p) and len(w) - len(p) >= 3:
            out.add(w[len(p):])
    for s in SUF:
        if w.endswith(s) and len(w) - len(s) >= 3:
            out.add(w[:-len(s)])
    for p in PREF:
        for s in SUF:
            if w.startswith(p) and w.endswith(s) and len(w) - len(p) - len(s) >= 3:
                out.add(w[len(p):-len(s)])
    return out


def canon(w):
    """Canonical root: strip affixes to the shortest reachable form, then fold interior A/O/E to A."""
    core = min(strip_affixes(w), key=len)
    return core[0] + "".join("A" if c in VSET else c for c in core[1:-1]) + core[-1] if len(core) >= 2 else core


def roots_of(names):
    groups = {}
    for n in names:
        groups.setdefault(canon(n), []).append(n)
    return groups


def run():
    rng = random.Random(56)
    d23 = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    masters = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"]
    names = sorted(set(masters) | {x["name"] for x in d23})
    groups = roots_of(names)

    # surrogate name-sets: Markov-3 strings of the same lengths, trained on the tables
    from a19_machine import CharLM
    from a22_robustness_and_depth import base_book, tnum
    book = base_book()
    m = CharLM(3, alpha=0.1).fit([r for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if r])
    lens = [len(n) for n in names]
    nul = []
    for _ in range(500):
        fake = []
        for L in lens:
            fake.append(m.sample(L, rng))
        nul.append(len(roots_of(sorted(set(fake)))))
    big = sorted(groups.items(), key=lambda kv: -len(kv[1]))
    res = {"names": len(names), "roots": len(groups),
           "roots_in_surrogate_name_sets": {"mean": round(statistics.mean(nul), 1), "min": min(nul),
                                            "p_real_fewer": round((sum(x <= len(groups) for x in nul) + 1) / 501, 4)},
           "largest_roots": [{"root": r, "count": len(ns), "names": sorted(ns, key=len)} for r, ns in big[:10]],
           "singletons": sum(1 for ns in groups.values() if len(ns) == 1),
           "share_in_the_5_biggest_roots": round(sum(len(ns) for _, ns in big[:5]) / len(names), 3),
           "note": "Roots are the canonical forms reached by removing one measured prefix/suffix and folding interior A/O/E. "
                   "'One Name' is read as 'few roots', not as a single one; the test is whether the family rules compress the "
                   "recurring names more than they compress random strings of the same lengths."}
    load.save_result("56_one_name", res)
    return res


if __name__ == "__main__":
    r = run()
    print("names %d -> roots %d (surrogate %s, p %.3f)" % (r["names"], r["roots"], r["roots_in_surrogate_name_sets"]["mean"], r["roots_in_surrogate_name_sets"]["p_real_fewer"]))
    print("share in 5 biggest roots:", r["share_in_the_5_biggest_roots"])
    for g in r["largest_roots"]:
        print("  %-8s %d  %s" % (g["root"], g["count"], " ".join(g["names"])))
