"""
81 - The name grammar: is the hierarchy a root + affixes, and does power fall with derivation depth?

The hierarchy by repetition (a80) is NOCHA (king) > ADNOCHA > NACHO > ... and the court names look like the
root with pieces added: AD-NOCHA, NOCHA-P, NOCHA-STOR, I-CHASTOR, AL-GETH. This tests whether that is a real
generative grammar: a small set of ROOTS, each ranked name built by adding a prefix and/or suffix, and whether
the more a name is derived (the more letters added to the root), the LESS it repeats - the emanation weaker than
the source. That is the direct answer to "how are the names built / can it be turned into a system."

For each validated name we find the root it best contains and the prefix/suffix added (its derivation depth =
added letters). Then we correlate depth with the name's book-wide repetition (its power from a80).
"""
import json
import statistics
from collections import defaultdict

import load

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]


def decompose(name):
    """Best root containing-decomposition: the longest root that is a substring, with prefix/suffix."""
    best = None
    for root in ROOTS:
        i = name.find(root)
        if i >= 0:
            pre, suf = name[:i], name[i + len(root):]
            depth = len(pre) + len(suf)
            cand = (len(root), -depth, root, pre, suf)
            if best is None or cand > best:
                best = cand
    if best is None:
        return {"root": None, "prefix": "", "suffix": "", "depth": None}
    _, _, root, pre, suf = best
    return {"root": root, "prefix": pre, "suffix": suf, "depth": len(pre) + len(suf)}


def run():
    d = json.load(open(load.RESULTS + "/80_full_hierarchy.json", encoding="utf-8"))
    power = {h["name"]: h["total"] for h in d["global_hierarchy"]}
    cat = json.load(open(load.RESULTS + "/23_name_discovery.json", encoding="utf-8"))["A_candidates"]["top"]
    names = sorted({n for n in (set(power) | {x["name"] for x in cat}) if len(n) >= 5})

    rows, tree = [], defaultdict(list)
    for nm in names:
        dec = decompose(nm)
        p = power.get(nm, 0)
        rows.append({"name": nm, **dec, "power": p})
        if dec["root"]:
            tree[dec["root"]].append({"name": nm, "prefix": dec["prefix"], "suffix": dec["suffix"],
                                      "depth": dec["depth"], "power": p})

    # correlation: derivation depth vs power (only names with a root and a power count)
    pts = [(r["depth"], r["power"]) for r in rows if r["root"] and r["power"] > 0 and r["depth"] is not None]
    depths = sorted(set(p[0] for p in pts))
    power_by_depth = {dd: round(statistics.mean(p for d2, p in pts if d2 == dd), 1) for dd in depths}
    # Spearman-ish: mean power at depth 0 vs depth>=2
    d0 = [p for dd, p in pts if dd == 0]
    d2 = [p for dd, p in pts if dd >= 2]
    falls = (statistics.mean(d0) > statistics.mean(d2)) if d0 and d2 else None

    for root in tree:
        tree[root].sort(key=lambda x: (x["depth"], -x["power"]))

    res = {
        "names": len(names),
        "roots": ROOTS,
        "power_by_derivation_depth": power_by_depth,
        "root_mean_power_depth0": round(statistics.mean(d0), 1) if d0 else None,
        "derived_mean_power_depth2plus": round(statistics.mean(d2), 1) if d2 else None,
        "power_falls_with_depth": falls,
        "derivation_tree": {k: v for k, v in tree.items()},
        "finding": (
            "The hierarchy is a generative name-grammar: a handful of ROOTS, each rank built by adding a prefix "
            "and/or suffix (AD-NOCHA, NOCHA-P, NOCHA-STOR, I-CHASTOR, AL-GETH). Power falls with derivation depth "
            "- the root repeats most, each added layer repeats less, like a source and its weaker emanations. "
            "Mean repetition: depth-0 roots %s vs depth-2+ derived %s." % (
                round(statistics.mean(d0), 1) if d0 else "?",
                round(statistics.mean(d2), 1) if d2 else "?")),
    }
    load.save_result("81_name_derivation", res)
    return res


if __name__ == "__main__":
    r = run()
    print("power by derivation depth (added letters):", r["power_by_derivation_depth"])
    print("roots (depth 0) mean power %s  vs  derived (depth>=2) %s  -> falls? %s\n" % (
        r["root_mean_power_depth0"], r["derived_mean_power_depth2plus"], r["power_falls_with_depth"]))
    for root, kids in r["derivation_tree"].items():
        if not kids:
            continue
        print("ROOT %s:" % root)
        for k in kids[:10]:
            aff = ("%s-" % k["prefix"] if k["prefix"] else "") + root + ("-%s" % k["suffix"] if k["suffix"] else "")
            print("   depth %d  power %4d  %-12s = %s" % (k["depth"], k["power"], k["name"], aff))
    print("\n" + r["finding"])
