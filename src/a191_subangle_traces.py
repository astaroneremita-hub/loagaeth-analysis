# -*- coding: utf-8 -*-
"""a191 - collect Great-Table name traces WITH sub-angle, for the sub-angle screen.

Fast: only the straight-line search (no null). Writes viz/subangle_traces.json with
every trace carrying tower + sub-angle element, so the screen can show "only Air",
"only Water", etc. across all four Towers at once.

Python stdlib only.
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


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = side_grids()
    names = enoch.derive_names()
    # keep sub when present; dedup by (name) but remember all (tower,sub,kind) tags
    seen = {}
    for n in names:
        key = n["name"]
        seen.setdefault(key, []).append(n)
    traces = []
    for name, metas in seen.items():
        hit = search_all(name, grids)
        if not hit:
            continue
        side, r, c, dr, dc = hit
        L = len(name)
        path = [[r + dr * i, c + dc * i] for i in range(L)]
        # one trace per distinct (tower, sub) tag this name carries (sub may be None for cross/king/senior)
        tags = {}
        for m in metas:
            tags[(m["tower"], m.get("sub"), m["kind"])] = True
        for (tower, sub, kind) in tags:
            traces.append({
                "name": name, "tower": tower, "sub": sub, "kind": kind,
                "side": side, "path": path,
            })
    viz = {"grids": grids, "traces": traces, "towers": TOWER_PT}
    vpath = os.path.join(os.path.dirname(HERE), "viz", "subangle_traces.json")
    with open(vpath, "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    from collections import Counter
    print("traces", len(traces), "wrote viz/subangle_traces.json")
    print("by sub", Counter(t["sub"] for t in traces))
    print("sub+kind lesser", Counter(t["sub"] for t in traces if t["kind"] == "lesser angel"))


if __name__ == "__main__":
    main()
