# -*- coding: utf-8 -*-
"""a192 - full roster of every Great-Table being, found or not, for the explorer screen.

Every hierarchy name (god names, kings, seniors, kerubic archangels, kerubs,
calvary flames/commands, lesser angels) of the 4 Towers, with tower + sub-angle +
kind, and whether it appears as a straight-line trace in the Loagaeth grids.

Key point (honest): long canonical names (kings 8, seniors 7) basically never trace;
short ones (lesser angels 4, god names 3) appear a lot - because short strings hit by
chance in a 49x49 grid. The screen shows that contrast by letting you select a kind.

Writes viz/all_beings.json. Python stdlib only.
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
import enoch
from a190_tower_traces import side_grids, search_all

TOWER_PT = {"ar": "Ar", "agua": "Agua", "terra": "Terra", "fogo": "Fogo"}

# normalize kind -> display group
def group_of(kind):
    if kind.startswith("senior"):
        return "senior"
    return kind

GROUP_PT = {
    "god name": "Nome de Deus",
    "king": "Rei",
    "senior": "Senior (Ancião)",
    "calvary-flame": "Cruz do Calvário (chama)",
    "calvary-command": "Cruz do Calvário (comando)",
    "kerub": "Querubim",
    "kerubic archangel": "Arcanjo querúbico",
    "lesser angel": "Anjo menor (serviente)",
}
# the 3 holy/great names of each tower are the three god names of the spirit line;
# also expose the Tower-of-Union name as the "sacred name" tag per tower.


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = side_grids()
    names = enoch.derive_names()

    # dedup by exact string, remember every (tower, sub, kind) tag it carries
    seen = {}
    for n in names:
        seen.setdefault(n["name"], []).append(n)

    beings = []
    for name, metas in seen.items():
        hit = search_all(name, grids)
        found = hit is not None
        if found:
            side, r, c, dr, dc = hit
            path = [[r + dr * i, c + dc * i] for i in range(len(name))]
        else:
            side, path = None, None
        # one row per distinct (tower, sub, group) so selecting a kind/tower works
        tags = {}
        for m in metas:
            tags[(m["tower"], m.get("sub"), group_of(m["kind"]))] = True
        for (tower, sub, grp) in tags:
            beings.append({
                "name": name, "tower": tower, "sub": sub,
                "group": grp, "len": len(name),
                "found": found, "side": side, "path": path,
            })

    # stats per group: found distinct / total distinct
    from collections import defaultdict
    tot = defaultdict(set)
    fnd = defaultdict(set)
    for b in beings:
        tot[b["group"]].add(b["name"])
        if b["found"]:
            fnd[b["group"]].add(b["name"])
    stats = {g: {"total": len(tot[g]), "found": len(fnd[g]),
                 "pct": round(100 * len(fnd[g]) / len(tot[g]))} for g in tot}

    viz = {
        "grids": grids,
        "beings": beings,
        "towers": TOWER_PT,
        "group_pt": GROUP_PT,
        "stats": stats,
        "union_names": enoch.TOWER_UNION,  # the 4 sacred Table-of-Union names
    }
    vpath = os.path.join(os.path.dirname(HERE), "viz", "all_beings.json")
    with open(vpath, "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    print("beings rows", len(beings), "wrote viz/all_beings.json")
    for g in sorted(stats, key=lambda k: -stats[k]["total"]):
        s = stats[g]
        print(f"  {g:22s} achados {s['found']:3d}/{s['total']:3d}  ({s['pct']:3d}%)")


if __name__ == "__main__":
    main()
