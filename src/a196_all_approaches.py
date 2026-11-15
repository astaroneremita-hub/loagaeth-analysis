# -*- coding: utf-8 -*-
"""a196 - "Did you try EVERYTHING?" Kings, Seniors, God names under every search rule.

For the canonical names (12 god + 4 kings + 24 seniors = 40), count how many appear at
least once ANYWHERE in the book under each rule, observed vs a within-folha shuffle null:

  straight8  : straight line, 8 directions (forward AND backward)
  knight     : straight line of knight moves (8 knight vectors) - "pulando" em L
  skip1      : straight line skipping one cell each step (step = 2*unit), 8 dirs
  boggle     : connected path, 8-neighbour, can turn, no cell reuse ("traçado livre")

If kings/seniors only show up under the loosest rules at the SAME rate as the null, the
"names" are search-space artifacts, not writing. Honest answer to "tentou de trás,
pulando, etc?" -> yes, here are the numbers.

Writes results/196_all_approaches.json. stdlib only. Seed 1583.
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import enoch
from a190_tower_traces import side_grids

SEED = 1583
TRIALS = 30
DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
KNIGHT = [(1, 2), (2, 1), (-1, 2), (-2, 1), (1, -2), (2, -1), (-1, -2), (-2, -1)]
NB = DIRS8


def straight(word, g, dirs, step=1):
    W = word.upper()
    L = len(W)
    H = len(g); Wd = len(g[0])
    for r in range(H):
        for c in range(Wd):
            if g[r][c] != W[0]:
                continue
            for dr, dc in dirs:
                er, ec = r + dr * step * (L - 1), c + dc * step * (L - 1)
                if not (0 <= er < H and 0 <= ec < Wd):
                    continue
                if all(g[r + dr * step * i][c + dc * step * i] == W[i] for i in range(L)):
                    return True
    return False


def boggle(word, g):
    W = word.upper()
    L = len(W)
    H = len(g); Wd = len(g[0])

    def dfs(r, c, i, seen):
        if i == L:
            return True
        for dr, dc in NB:
            rr, cc = r + dr, c + dc
            if 0 <= rr < H and 0 <= cc < Wd and (rr, cc) not in seen and g[rr][cc] == W[i]:
                seen.add((rr, cc))
                if dfs(rr, cc, i + 1, seen):
                    return True
                seen.discard((rr, cc))
        return False

    for r in range(H):
        for c in range(Wd):
            if g[r][c] == W[0] and dfs(r, c, 1, {(r, c)}):
                return True
    return False


METHODS = {
    "straight8": lambda w, g: straight(w, g, DIRS8, 1),
    "knight": lambda w, g: straight(w, g, KNIGHT, 1),
    "skip1": lambda w, g: straight(w, g, DIRS8, 2),
    "boggle": lambda w, g: boggle(w, g),
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = list(side_grids().values())
    nm = enoch.derive_names()

    def grp(k):
        return "senior" if k.startswith("senior") else k
    cats = {"god name": [], "king": [], "senior": []}
    for n in nm:
        g = grp(n["kind"])
        if g in cats and n["name"] not in cats[g]:
            cats[g].append(n["name"])
    allnames = [w for v in cats.values() for w in v]
    print("canonical:", {k: len(v) for k, v in cats.items()}, "total", len(allnames), flush=True)

    def found_any(word, method):
        f = METHODS[method]
        return any(f(word, g) for g in grids)

    def count(method, words, gs):
        f = METHODS[method]
        return sum(1 for w in words if any(f(w, g) for g in gs))

    rng = random.Random(SEED)

    def shuffled(grid):
        flat = [ch for row in grid for ch in row]
        rng.shuffle(flat)
        Wd = len(grid[0])
        return ["".join(flat[i:i + Wd]) for i in range(0, len(flat), Wd)]

    report = {}
    for method in METHODS:
        row = {}
        for cat, words in cats.items():
            obs = count(method, words, grids)
            sims = []
            for _ in range(TRIALS):
                sg = [shuffled(g) for g in grids]
                sims.append(count(method, words, sg))
            m = sum(sims) / len(sims)
            sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
            z = (obs - m) / sd if sd else 0.0
            row[cat] = {"n": len(words), "found": obs, "null_mean": round(m, 2),
                        "null_sd": round(sd, 2), "z": round(z, 2)}
            print(f"{method:10s} {cat:9s} found {obs:2d}/{len(words):2d}  null {m:5.1f}+-{sd:4.1f}  z={z:+.2f}", flush=True)
        report[method] = row

    out = {"test": "Kings/Seniors/God-names under every search rule vs null",
           "seed": SEED, "trials": TRIALS, "methods": list(METHODS), "report": report}
    rdir = os.path.join(os.path.dirname(HERE), "results")
    os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "196_all_approaches.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
