# -*- coding: utf-8 -*-
"""a209 - WHERE on the 49x49 page do the names sit? (new spatial lens)

For the master + zonal names, collect every straight-8 occurrence's start cell; aggregate
row band (top/mid/bottom), border-ring vs interior, and quadrant. Compare the border-ring
fraction to the null (shuffled grids). Does the name field prefer the frame, the centre,
or the top of each page?

stdlib only. seed 1583.
"""
import os
import sys
import json
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
from a190_tower_traces import side_grids

DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
NAMES = ["NOCHA", "CHASTOR", "ANZACH", "ALGETH", "DNOCHA", "ADNOCHA", "GRAPHA", "ACHEPH"]


def occ_cells(word, g):
    W = word.upper(); L = len(W); H = len(g); Wd = len(g[0]); out = []
    for r in range(H):
        for c in range(Wd):
            if g[r][c] != W[0]:
                continue
            for dr, dc in DIRS8:
                er, ec = r + dr * (L - 1), c + dc * (L - 1)
                if 0 <= er < H and 0 <= ec < Wd and all(g[r + dr * i][c + dc * i] == W[i] for i in range(L)):
                    # record all cells of the occurrence
                    for i in range(L):
                        out.append((r + dr * i, c + dc * i))
    return out


def classify(cells):
    band = Counter(); ring = Counter(); quad = Counter()
    for (r, c) in cells:
        band["topo" if r < 16 else ("meio" if r < 33 else "fundo")] += 1
        ring["borda" if (r < 3 or r > 45 or c < 3 or c > 45) else "miolo"] += 1
        if r != 24 and c != 24:
            quad[("N" if r < 24 else "S") + ("O" if c < 24 else "E")] += 1
    return band, ring, quad


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    grids = list(side_grids().values())

    allcells = []
    for g in grids:
        for nm in NAMES:
            allcells += occ_cells(nm, g)
    band, ring, quad = classify(allcells)
    tot = sum(ring.values())
    obs_border = ring["borda"] / tot if tot else 0

    # null: same names in shuffled grids
    sims = []
    for _ in range(12):
        sg = []
        for g in grids:
            flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
            sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
        cells = []
        for g in sg:
            for nm in NAMES:
                cells += occ_cells(nm, g)
        _, rg, _ = classify(cells)
        t = sum(rg.values())
        sims.append(rg["borda"] / t if t else 0)
    m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
    z = (obs_border - m) / sd if sd else 0

    result = {"seed": 1583, "n_cells": tot,
              "band": dict(band), "ring": dict(ring), "quad": dict(quad),
              "border_frac_obs": round(obs_border, 4), "border_null_mean": round(m, 4),
              "border_null_sd": round(sd, 4), "border_z": round(z, 2),
              "border_area_frac": round((49 * 49 - 43 * 43) / (49 * 49), 3)}
    print(f"[POS] banda {dict(band)}", flush=True)
    print(f"[POS] borda {ring['borda']}/{tot} = {obs_border:.3f} vs null {m:.3f}±{sd:.3f} z={z:+.2f} (área borda={result['border_area_frac']})", flush=True)
    print(f"[POS] quadrante {dict(quad)}", flush=True)
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "209_name_position.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
