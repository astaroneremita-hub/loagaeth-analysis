# -*- coding: utf-8 -*-
"""a195 - full occurrence index: EVERY straight-line hit of every Tower name in every
Loagaeth side, with direction (horizontal / vertical / diagonal), for the map screen.

Pick a folha + a type, see ALL occurrences at once, counted by direction.

Directions are canonical (4 forward dirs) so each physical line is counted once:
  0 = horizontal (E)      1 = vertical (S)
  2 = diagonal \\ (SE)     3 = diagonal / (SW, down-left)

Writes viz/occurrence_map.json. stdlib only.
"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import enoch
from a190_tower_traces import side_grids

# 8 directions, forward AND backward. index -> (dr,dc)
# 0 E, 1 S, 2 W(ré), 3 N(ré), 4 SE, 5 NW(ré), 6 SW, 7 NE(ré)
FDIRS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
# category: 0=linha(H) 1=coluna(V) 2=diagonal ; backward flag
DIR_CAT = [0, 1, 0, 1, 2, 2, 2, 2]
DIR_BACK = [0, 0, 1, 1, 0, 1, 0, 1]


def group_of(kind):
    return "senior" if kind.startswith("senior") else kind


def all_occ(word, g):
    W = word.upper()
    L = len(W)
    H = len(g)
    Wd = len(g[0])
    out = []
    for r in range(H):
        for c in range(Wd):
            if g[r][c] != W[0]:
                continue
            for di, (dr, dc) in enumerate(FDIRS):
                er, ec = r + dr * (L - 1), c + dc * (L - 1)
                if not (0 <= er < H and 0 <= ec < Wd):
                    continue
                if all(g[r + dr * i][c + dc * i] == W[i] for i in range(L)):
                    out.append([r, c, di])
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = side_grids()
    names = enoch.derive_names()
    meta = {}
    for n in names:
        m = meta.setdefault(n["name"], {"group": group_of(n["kind"]), "tower": n["tower"],
                                        "sub": n.get("sub"), "len": len(n["name"])})
    uniq = list(meta)

    occ = {}  # side -> name -> [[r,c,dir],...]
    total = 0
    totals = {n: 0 for n in uniq}  # total occurrences across the whole book
    for side, g in grids.items():
        side_map = {}
        for name in uniq:
            hits = all_occ(name, g)
            if hits:
                side_map[name] = hits
                total += len(hits)
                totals[name] += len(hits)
        if side_map:
            occ[side] = side_map

    # full roster per group (every canonical name, found or not)
    roster = {}
    for n, m in meta.items():
        roster.setdefault(m["group"], []).append(n)
    for g in roster:
        roster[g] = sorted(roster[g])

    viz = {
        "grids": grids,
        "occ": occ,
        "meta": meta,
        "group_pt": {
            "god name": "Nome de Deus", "king": "Rei", "senior": "Ancião",
            "kerubic archangel": "Arcanjo querúbico", "kerub": "Querubim",
            "calvary-flame": "Cruz (chama)", "calvary-command": "Cruz (comando)",
            "lesser angel": "Anjo menor",
        },
        "dir_pt": ["E →", "S ↓", "O ← (ré)", "N ↑ (ré)", "SE ↘", "NO ↖ (ré)", "SO ↙", "NE ↗ (ré)"],
        "dir_cat": DIR_CAT,   # 0 linha, 1 coluna, 2 diagonal
        "dir_back": DIR_BACK,  # 1 = lido de trás pra frente
        "roster": roster,
        "totals": totals,
    }
    vpath = os.path.join(os.path.dirname(HERE), "viz", "occurrence_map.json")
    with open(vpath, "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    sz = os.path.getsize(vpath)
    print(f"sides {len(occ)} total occurrences {total} size {sz//1024} KB")
    # quick god-name report on folha 2a
    if "2a" in occ:
        gn = {k: v for k, v in occ["2a"].items() if meta[k]["group"] == "god name"}
        print("folha 2a nomes de Deus:", {k: len(v) for k, v in gn.items()})


if __name__ == "__main__":
    main()
