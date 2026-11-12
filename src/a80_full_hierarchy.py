"""
80 - The complete hierarchy map: every square's king and its court, ranked by repetition.

Murilo's model, straight from the Watchtowers: the name that repeats most on a square is its KING; the
next names down are its court (god-name, spirit, archangel, senior...); the names that appear once are
the lesser spirits under them. More repetition = more power. We build that map for every square.

To keep it meaningful (and not rank by bigram-noise like OXAD), the inventory is the validated name
catalogue: the discovered names (a23) plus the master family names, length >= 5, so a count reflects a
real recurring name, not a common letter-pair. Count = occurrences of the name as a substring on the leaf,
forward and reversed (a name may be written either way). Per leaf: rank -> tiers. Across the book: the
supreme ranking.
"""
import json
from collections import Counter

import load

TIERS = ["Rei", "Nome de Deus", "Nome do Espirito", "Arcanjo", "Senior", "Anjo", "Anjo menor"]


def count_on(text, name):
    return text.count(name) + text.count(name[::-1])


def run():
    lv = load.leaves()
    grids = {}
    for leaf, rows in lv.items():
        g = "".join("".join(load.letters(r)) for r in rows if load.letters(r))
        if len(g) >= 2000:
            grids[leaf] = g
    order = sorted(grids, key=lambda k: (int(k[:-1]), k[-1]))

    d = json.load(open(load.RESULTS + "/23_name_discovery.json", encoding="utf-8"))["A_candidates"]["top"]
    masters = ["CHASTOR", "NOCHA", "ADNOCHA", "NOCHAP", "GETH", "ALGETH", "CHADAX", "ACHADAX",
               "DAHAHOXOM", "ANZACH", "ACLAX", "GRADAX", "ANTANTOX", "NACHO", "DABAHOXIM"]
    names = sorted({n for n in (set(masters) | {x["name"] for x in d}) if len(n) >= 5}, key=lambda s: -len(s))
    # drop names that are substrings of a longer kept name counted at the same spot? keep all; he wants all.

    global_count = Counter()
    per_leaf = {}
    for leaf in order:
        t = grids[leaf]
        cnt = Counter({nm: count_on(t, nm) for nm in names})
        cnt = Counter({k: v for k, v in cnt.items() if v > 0})
        global_count.update(cnt)
        ranked = cnt.most_common()
        king = ranked[0] if ranked else None
        # independent ruler = top name that is NOT a substring of a longer present name (strips nesting)
        present = [nm for nm, _ in ranked]
        indep = None
        for nm, c in ranked:
            if not any(nm != o and nm in o for o in present):
                indep = {"name": nm, "count": c}
                break
        hierarchy = []
        for i, (nm, c) in enumerate(ranked):
            tier = TIERS[i] if i < len(TIERS) - 1 else ("Anjo menor" if c == 1 else "Anjo")
            hierarchy.append({"name": nm, "count": c, "tier": tier})
        per_leaf[leaf] = {
            "king": {"name": king[0], "count": king[1]} if king else None,
            "independent_ruler": indep,
            "distinct_names": len(ranked),
            "lesser_spirits_count": sum(1 for _, c in ranked if c == 1),
            "hierarchy": hierarchy,
        }

    supreme = global_count.most_common()
    global_hier = []
    for i, (nm, c) in enumerate(supreme):
        tier = TIERS[i] if i < len(TIERS) - 1 else ("Anjo menor" if c <= 2 else "Anjo")
        global_hier.append({"name": nm, "total": c, "tier": tier,
                            "rules_leaves": sum(1 for lf in per_leaf if per_leaf[lf]["king"] and per_leaf[lf]["king"]["name"] == nm),
                            "rules_leaves_independent": sum(1 for lf in per_leaf if per_leaf[lf]["independent_ruler"] and per_leaf[lf]["independent_ruler"]["name"] == nm)})

    res = {
        "names_in_inventory": len(names),
        "leaves": len(order),
        "order": order,
        "supreme_king": {"name": supreme[0][0], "total": supreme[0][1]} if supreme else None,
        "global_hierarchy": global_hier,
        "per_leaf": per_leaf,
        "note": "King = most-repeated validated name on the square; court = next ranks; lesser spirits = "
                "names appearing once. Counts are forward+reversed substring occurrences of catalogue names "
                "(length >= 5, so a count is a real recurring name, not a common letter-pair).",
    }
    load.save_result("80_full_hierarchy", res)
    return res


if __name__ == "__main__":
    r = run()
    print("inventory %d names | supreme king: %s (%d total)\n" % (
        r["names_in_inventory"], r["supreme_king"]["name"], r["supreme_king"]["total"]))
    print("GLOBAL HIERARCHY (top 12):")
    for h in r["global_hierarchy"][:12]:
        print("  %-14s %-16s total %4d  rules %2d squares" % (h["name"], h["tier"], h["total"], h["rules_leaves"]))
    print("\nKING OF EACH SQUARE (raw repeat | independent ruler strips nesting):")
    for lf in r["order"]:
        p = r["per_leaf"][lf]
        k = p["king"]
        ind = p["independent_ruler"]
        if not k:
            print("  %-4s (no catalogue name)" % lf)
            continue
        print("  %-4s king %-11s x%-3d | indep %-11s x%-3d  (%d names, %d lesser)" % (
            lf, k["name"], k["count"], ind["name"] if ind else "-", ind["count"] if ind else 0,
            p["distinct_names"], p["lesser_spirits_count"]))
