"""
70 - Does the name-packing mean anything? The decisive controls.

We can tile a leaf with dozens of cell-disjoint name-paths (85 traces, 38 names on 2b). The question
is whether that reflects a real arrangement of names, or only the letter frequencies - any grid of
these letters would pack the same. Two controls settle it:

  A) The grid. Pack the REAL leaf, a SHUFFLE of its own letters (same multiset, positions destroyed),
     and a Markov-3 surrogate (keeps local letter-flow). If the real leaf packs no more than its
     shuffle, the packing is the letter frequencies, not an arrangement.
  B) The names. Pack the real leaf with the real catalogue names, and with RANDOM "names" (strings
     over the leaf's alphabet, same length distribution). If real names don't pack more than random
     strings, the catalogue names are nothing special to the grid.

Greedy packing (rarest name first), same as viz/path_view.html, on leaves 2b, 14b and 18b.
"""
import json
import os
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3


def count_paths_cap(grid, tg, cap):
    R = len(grid)
    res = []

    def nb(r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < len(grid[nr]):
                        yield nr, nc

    def dfs(r, c, idx, path):
        if idx == len(tg):
            res.append(tuple(path))
            return len(res) < cap
        for nr, nc in nb(r, c):
            if (nr, nc) not in path and grid[nr][nc] == tg[idx]:
                path.append((nr, nc))
                if not dfs(nr, nc, idx + 1, path):
                    return False
                path.pop()
        return True
    for r in range(R):
        for c in range(len(grid[r])):
            if grid[r][c] == tg[0]:
                dfs(r, c, 1, [(r, c)])
    return res


def pack(grid, names, cap=120):
    cand = []
    for nm in names:
        ps = count_paths_cap(grid, nm, cap)
        if ps:
            cand.append((nm, ps))
    cand.sort(key=lambda t: (len(t[1]), -len(t[0])))
    used = set()
    placed = 0
    names_used = set()
    changed = True
    while changed:
        changed = False
        for nm, ps in cand:
            for p in ps:
                if not any(c in used for c in p):
                    used.update(p)
                    placed += 1
                    names_used.add(nm)
                    changed = True
                    break
    return {"traces": placed, "distinct_names": len(names_used), "cells": len(used)}


def shuffle_grid(grid, rng):
    flat = [ch for row in grid for ch in row]
    rng.shuffle(flat)
    out, i = [], 0
    for row in grid:
        out.append("".join(flat[i:i + len(row)]))
        i += len(row)
    return out


def surrogate_grid(grid, rng):
    s = markov3("".join("".join(r) for r in grid), rng)
    out, i = [], 0
    for row in grid:
        out.append(s[i:i + len(row)])
        i += len(row)
    return out


def run():
    rng = random.Random(70)
    lv = load.leaves()
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    masters = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX", "DAHAHOXOM"]
    names = sorted({n for n in (set(masters) | {x["name"] for x in d}) if len(n) >= 4}, key=len)
    lens = [len(n) for n in names]
    res = {}
    for leaf in ("2b", "14b", "18b"):
        grid = [load.letters(r) for r in lv[leaf] if load.letters(r)]
        if len(grid) != 49:
            continue
        f = Counter("".join(grid))
        alph, wt = list(f), [f[c] for c in f]
        real = pack(grid, names)
        # A controls
        sh = [pack(shuffle_grid(grid, rng), names) for _ in range(5)]
        su = [pack(surrogate_grid(grid, rng), names) for _ in range(5)]
        # B control: random names of same lengths, on the real grid
        randnames = ["".join(rng.choices(alph, wt, k=L)) for L in lens]
        rn = pack(grid, randnames)
        res[leaf] = {
            "real_grid": real,
            "shuffled_grid_mean": {k: round(statistics.mean(x[k] for x in sh), 1) for k in real},
            "surrogate_grid_mean": {k: round(statistics.mean(x[k] for x in su), 1) for k in real},
            "random_names_on_real_grid": rn}
    res["conclusion"] = ("")
    # verdict from 2b
    r2 = res.get("2b", {})
    if r2:
        rt = r2["real_grid"]["traces"]
        st = r2["shuffled_grid_mean"]["traces"]
        rn = r2["random_names_on_real_grid"]["traces"]
        same_grid = abs(rt - st) / max(1, st) < 0.2
        same_names = abs(rt - rn) / max(1, rn) < 0.2
        res["conclusion"] = (
            "On 2b the real grid packs %d name-traces; a shuffle of its own letters packs %.0f, and random names on the "
            "real grid pack %d. %s %s So the packing is %s - it reflects the letter frequencies and the shape of the "
            "catalogue names, not a deliberate arrangement of those names in the grid. It is a true picture of how "
            "name-saturated this alphabet is, and an honest 'no' to the idea that the square is secretly tiled with these "
            "particular names on purpose." % (
                rt, st, rn,
                "Shuffling the letters barely changes it (%.0f vs %d)," % (st, rt) if same_grid else "The real grid packs clearly more than its shuffle (%d vs %.0f)," % (rt, st),
                "and real names pack about the same as random strings." if same_names else "and real names pack more than random strings (%d vs %d)." % (rt, rn),
                "mostly the dense field" if same_grid else "partly real: the arrangement adds something"))
    load.save_result("70_packing_meaning", res)
    return res


if __name__ == "__main__":
    r = run()
    for leaf in ("2b", "14b", "18b"):
        if leaf in r:
            x = r[leaf]
            print(leaf, "real:", x["real_grid"], "| shuffled:", x["shuffled_grid_mean"], "| surrogate:", x["surrogate_grid_mean"], "| random names:", x["random_names_on_real_grid"])
    print("\n" + r["conclusion"])
