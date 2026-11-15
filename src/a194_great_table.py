# -*- coding: utf-8 -*-
"""a194 - export the four Watchtower letter grids (Great Table) + each name's cells,
so the viewer can SHOW the letters in the squares and light up where every angel sits.

Writes viz/great_table.json. stdlib only.
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import enoch

TOWER_PT = {"ar": "Ar", "agua": "Água", "terra": "Terra", "fogo": "Fogo"}
SUBANGLES = enoch.SUBANGLES  # [((r0,c0), sub), ...] 4 corners


def three_name_cells(el):
    out = []
    spans = [(0, 3), (3, 7), (7, 12)]
    for a, b in spans:
        out.append([[6, c] for c in range(a, b)])
    return out  # 3 god names, row 6


def king_cells():
    return [[6, 4], [5, 5], [5, 6], [6, 7], [7, 6], [7, 5], [6, 5], [6, 6]]


def senior_cells():
    up_l = [[r, 5] for r in range(6, -1, -1)]
    up_r = [[r, 6] for r in range(6, -1, -1)]
    dn_l = [[r, 5] for r in range(6, 13)]
    dn_r = [[r, 6] for r in range(6, 13)]
    left = [[6, c] for c in range(6, -1, -1)]
    right = [[6, c] for c in range(5, 12)]
    return {"up_l": up_l, "up_r": up_r, "dn_l": dn_l, "dn_r": dn_r, "left": left, "right": right}


def sub_cells(k):
    (r0, c0), sub = SUBANGLES[k]
    # map local (r,c) in 6x5 to absolute
    def ab(r, c):
        return [r0 + r, c0 + c]
    calvary_flame = [ab(r, 2) for r in range(6)]
    calvary_command = [ab(1, c) for c in range(5)]
    kerub = [ab(0, 0), ab(0, 1), ab(0, 3), ab(0, 4)]
    servients = []
    for r in range(2, 6):
        servients.append([ab(r, 0), ab(r, 1), ab(r, 3), ab(r, 4)])
    return sub, calvary_flame, calvary_command, kerub, servients


def main():
    grids = {el: enoch.GRID[el] for el in enoch.TOWERS}
    names = []
    for el in enoch.TOWERS:
        tn = enoch.three_names(el)
        for s, cells in zip(tn, three_name_cells(el)):
            names.append({"name": s, "kind": "god name", "tower": el, "cells": cells})
        names.append({"name": enoch.king(el), "kind": "king", "tower": el, "cells": king_cells()})
        sv = enoch.seniors(el)
        for arm, cells in senior_cells().items():
            names.append({"name": sv[arm], "kind": "senior", "tower": el, "cells": cells})
        for k in range(4):
            sub, flame, command, kerub, servients = sub_cells(k)
            call, cmd = enoch.calvary(el, k)
            names.append({"name": call, "kind": "calvary-flame", "tower": el, "sub": sub, "cells": flame})
            names.append({"name": cmd, "kind": "calvary-command", "tower": el, "sub": sub, "cells": command})
            base = enoch.kerubic(el, k)[0]
            names.append({"name": base, "kind": "kerub", "tower": el, "sub": sub, "cells": kerub})
            for sline in servients:
                s = "".join(enoch.GRID[el][r][c] for r, c in sline)
                names.append({"name": s, "kind": "lesser angel", "tower": el, "sub": sub, "cells": sline})

    viz = {
        "grids": grids,
        "names": names,
        "towers": TOWER_PT,
        "union": enoch.TOWER_UNION,
        "subangles": [{"corner": c, "sub": s} for (c, s) in SUBANGLES],
    }
    vpath = os.path.join(os.path.dirname(HERE), "viz", "great_table.json")
    with open(vpath, "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    print("towers", len(grids), "names", len(names), "wrote viz/great_table.json")


if __name__ == "__main__":
    main()
