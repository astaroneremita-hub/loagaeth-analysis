# -*- coding: utf-8 -*-
"""Core data and rules of the Great Table (Golden Dawn version).

Data source: data/quadrados.json (624 squares + the 20 of the Table of Union, with
faces, zones, attributions and letters, extracted from Golden Dawn line works).
Usage: import enoch; enoch.GRID['ar'][r][c] (0-based), enoch.derive_names(), enoch.search(...)

Tower ids are the Portuguese element names kept as stable keys:
  ar = Air, agua = Water, terra = Earth, fogo = Fire.
"""
import itertools
import json
import os
import random

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
SQ = json.load(open(os.path.join(DATA, "quadrados.json"), encoding="utf-8"))
TOWERS = ["ar", "agua", "terra", "fogo"]
NAME = {"ar": "Air", "agua": "Water", "terra": "Earth", "fogo": "Fire"}
UNION = ["EXARP", "HCOMA", "NANTA", "BITOM"]
TOWER_UNION = {"ar": "EXARP", "agua": "HCOMA", "terra": "NANTA", "fogo": "BITOM"}
# order of sub-angles within each Tower: (row0, col0) of the corner and its element
SUBANGLES = [((0, 0), "ar"), ((0, 7), "agua"), ((7, 0), "terra"), ((7, 7), "fogo")]


def _grid(el):
    g = [["?"] * 12 for _ in range(13)]
    for s in SQ[el]:
        g[s["row"] - 1][s["col"] - 1] = s["letter"].upper()
    return g


GRID = {el: _grid(el) for el in TOWERS}


def row(el, r):
    return "".join(GRID[el][r])


def col(el, c):
    return "".join(GRID[el][r][c] for r in range(13))


# ------------------------------------------------------------------ names by the GD rule

def three_names(el):
    """Spirit line (row 7): the three God-names of 3, 4 and 5 letters."""
    s = row(el, 6)
    return [s[0:3], s[3:7], s[7:12]]


def king(el):
    """King: spiral from the centre of the Great Cross (cols 6-7, rows 6-8)."""
    g = GRID[el]
    # GD order checked against BATAIVAH (Air): B(6,4) A(5,5) T(5,6) A(6,7) I(7,6) V(7,5) A(6,5) H(6,6)
    order = [(6, 4), (5, 5), (5, 6), (6, 7), (7, 6), (7, 5), (6, 5), (6, 6)]
    return "".join(g[r][c] for r, c in order)


def seniors(el):
    """Six Seniors: arms of the Great Cross from the centre (7 letters each, sharing the centre)."""
    g = GRID[el]
    up_l = "".join(g[r][5] for r in range(6, -1, -1))     # column 6 going up
    up_r = "".join(g[r][6] for r in range(6, -1, -1))     # column 7 going up
    dn_l = "".join(g[r][5] for r in range(6, 13))         # column 6 going down
    dn_r = "".join(g[r][6] for r in range(6, 13))         # column 7 going down
    left = "".join(g[6][c] for c in range(6, -1, -1))     # row 7, from col 7 leftward (HABIORO)
    right = "".join(g[6][c] for c in range(5, 12))        # row 7, from col 6 rightward (AHAOZPI)
    return {"up_l": up_l, "up_r": up_r, "dn_l": dn_l, "dn_r": dn_r, "left": left, "right": right}


def subangle(el, k):
    (r0, c0), sub = SUBANGLES[k]
    return [[GRID[el][r0 + r][c0 + c] for c in range(5)] for r in range(6)], sub


def calvary(el, k):
    """Calvary Cross of a sub-angle: central column (6 letters, the 'flame') and row 2 (5 letters)."""
    m, _ = subangle(el, k)
    call = "".join(m[r][2] for r in range(6))
    command = "".join(m[1])
    return call, command


def kerubic(el, k):
    """Kerubic line (row 1 of the sub-angle without the central column): 4 letters and 3 rotations."""
    m, _ = subangle(el, k)
    base = m[0][0] + m[0][1] + m[0][3] + m[0][4]
    return [base[i:] + base[:i] for i in range(4)]


def servient(el, k):
    """Four servient lines (3-6), without the central column: four 4-letter names."""
    m, _ = subangle(el, k)
    return [m[r][0] + m[r][1] + m[r][3] + m[r][4] for r in range(2, 6)]


def derive_names():
    """All hierarchy names derived by the GD rule (for checking and search)."""
    out = []
    for el in TOWERS:
        for n in three_names(el):
            out.append({"name": n, "kind": "god name", "tower": el})
        out.append({"name": king(el), "kind": "king", "tower": el})
        for k, v in seniors(el).items():
            out.append({"name": v, "kind": f"senior ({k})", "tower": el})
        for k in range(4):
            sub = SUBANGLES[k][1]
            call, command = calvary(el, k)
            out.append({"name": call, "kind": "calvary-flame", "tower": el, "sub": sub})
            out.append({"name": command, "kind": "calvary-command", "tower": el, "sub": sub})
            spirit = TOWER_UNION[el][0]  # archangel prefix comes from the Tower (16/16 in GD data), not the sub-angle
            for i, kn in enumerate(kerubic(el, k)):
                out.append({"name": kn, "kind": "kerub", "tower": el, "sub": sub})
                out.append({"name": spirit + kn, "kind": "kerubic archangel", "tower": el, "sub": sub})
            for sv in servient(el, k):
                for i in range(4):
                    out.append({"name": sv[i:] + sv[:i], "kind": "lesser angel", "tower": el, "sub": sub})
    return out


# ------------------------------------------------------------------ search and baseline

DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def search(grid, word, dirs=DIRS, knight=False):
    """Occurrences of `word` in the grid as a straight line (8 directions). Returns [(r, c, dr, dc)]."""
    word = word.upper()
    H, W = len(grid), len(grid[0])
    hits = []
    for r in range(H):
        for c in range(W):
            if grid[r][c] != word[0]:
                continue
            for dr, dc in dirs:
                ok = True
                for i, ch in enumerate(word):
                    rr, cc = r + dr * i, c + dc * i
                    if not (0 <= rr < H and 0 <= cc < W) or grid[rr][cc] != ch:
                        ok = False
                        break
                if ok:
                    hits.append((r, c, dr, dc))
    return hits


def shuffled(grid, rng):
    flat = [x for rw in grid for x in rw]
    rng.shuffle(flat)
    W = len(grid[0])
    return [flat[i:i + W] for i in range(0, len(flat), W)]


def baseline(words, grids, trials=2000, seed=777):
    """How many words of the list appear by chance in grids with the same letters shuffled.
    Returns (observed, mean, sd, empirical p-value)."""
    def count(gs):
        return sum(1 for w in words if any(search(g, w) for g in gs))
    obs = count(grids)
    rng = random.Random(seed)
    sims = [count([shuffled(g, rng) for g in grids]) for _ in range(trials)]
    mean = sum(sims) / len(sims)
    sd = (sum((x - mean) ** 2 for x in sims) / len(sims)) ** 0.5
    p = (1 + sum(1 for x in sims if x >= obs)) / (1 + trials)
    return obs, mean, sd, p


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    for el in TOWERS:
        print(NAME[el], three_names(el), king(el), list(seniors(el).values()))
    print(len(derive_names()), "derived names")
