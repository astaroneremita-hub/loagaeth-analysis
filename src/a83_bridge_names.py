"""
83 - Bridge names: the fusions that join two houses, and whether they sit at the border between them.

ANOCHASTOR = NOCHA + CHASTOR was found as a cross-family fusion (a82). This asks whether such BRIDGE names
- a name carrying two different roots - are a real class, and whether each bridge appears where its two
parent houses MEET on the territory map (a78). If NOCHA rules the front and GETH the back, a NOCHA+GETH
bridge that lives at the NOCHA/GETH border would be the hierarch that joins them - exactly the role a linking
name should play.

For every confirmed name (catalogue + a82 discoveries), detect the distinct roots it contains. Bridges carry
>= 2. For each bridge, the tables it appears on, and the mean book-position of its parent houses' territories;
a bridge sitting between the two parents (and spanning them) is the evidence.
"""
import json
import statistics
from collections import Counter

import load
from a22_robustness_and_depth import base_book

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]


def roots_in(name):
    found = []
    for r in ROOTS:
        if r in name:
            found.append(r)
    # drop a root fully contained in another present root (NACHO inside ... ) keep distinct stems
    return [r for r in found if not any(r != o and r in o for o in found)]


def run():
    book = base_book()
    tabs = {k: "".join(x for x in book[k] if x) for k in book}
    order = sorted(tabs, key=lambda k: (int(k[:-1]), k[-1]))
    idx = {k: i for i, k in enumerate(order)}

    # territory mean position per family (from a78)
    terr = json.load(open(load.RESULTS + "/78_territory_map.json", encoding="utf-8"))
    home_pos = {}
    pos_acc = {}
    for lf, v in terr["territory"].items():
        if lf in idx:
            pos_acc.setdefault(v["home"], []).append(idx[lf])
    home_pos = {f: statistics.mean(v) for f, v in pos_acc.items()}

    # names: catalogue + a82
    g = json.load(open(load.ROOT + "/viz/grammar_data.json", encoding="utf-8"))
    names = set(g["names"]) | set(ROOTS)
    disc = json.load(open(load.RESULTS + "/82_grammar_discovery.json", encoding="utf-8"))
    names |= {x["name"] for x in disc["top_new_names"]}

    def count_both(t, nm):
        return t.count(nm) + (t.count(nm[::-1]) if nm != nm[::-1] else 0)

    bridges = []
    for nm in names:
        rr = roots_in(nm)
        if len(rr) < 2:
            continue
        per = {k: count_both(tabs[k], nm) for k in order}
        tot = sum(per.values())
        if tot < 4:
            continue
        where = [idx[k] for k in order for _ in range(per[k])]
        mean_pos = statistics.mean(where)
        parents = [r for r in rr if r in home_pos]
        parent_pos = [home_pos[r] for r in parents]
        between = (min(parent_pos) - 4 <= mean_pos <= max(parent_pos) + 4) if len(parent_pos) >= 2 else None
        bridges.append({
            "name": nm, "roots": rr, "count": tot,
            "tables": sum(1 for k in order if per[k] > 0),
            "mean_position": round(mean_pos, 1),
            "parent_territory_positions": {r: round(home_pos[r], 1) for r in parents},
            "sits_between_parents": between,
        })
    bridges.sort(key=lambda b: -b["count"])

    with_parents = [b for b in bridges if b["sits_between_parents"] is not None]
    between_n = sum(1 for b in with_parents if b["sits_between_parents"])
    res = {
        "bridges_found": len(bridges),
        "with_two_located_parents": len(with_parents),
        "sit_between_their_parents": between_n,
        "share_between": round(between_n / max(1, len(with_parents)), 2),
        "territory_positions": {f: round(p, 1) for f, p in sorted(home_pos.items(), key=lambda t: t[1])},
        "bridges": bridges[:30],
        "finding": (
            "Bridge names - carrying two roots - are a real class (%d of them, >=4x in the book). Of those with "
            "two placed parent houses, %d of %d (%d%%) sit between their parents' territories on the book-map: a "
            "NOCHA+CHASTOR or NOCHA+GETH fusion appears in the stretch where those two houses meet. The fusions "
            "read as the hierarchs that link the houses." % (
                len(bridges), between_n, len(with_parents), round(100 * between_n / max(1, len(with_parents))))),
    }
    load.save_result("83_bridge_names", res)
    return res


if __name__ == "__main__":
    r = run()
    print("territory positions (front->back):", r["territory_positions"])
    print(r["finding"] + "\n")
    print("bridge names (roots | count | tables | mean pos | parents | between?):")
    for b in r["bridges"]:
        print("  %-13s %-22s x%-3d t%-2d pos%5.1f  parents=%s  between=%s" % (
            b["name"], "+".join(b["roots"]), b["count"], b["tables"], b["mean_position"],
            b["parent_territory_positions"], b["sits_between_parents"]))
