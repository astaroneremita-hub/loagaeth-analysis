# -*- coding: utf-8 -*-
"""a234 - NAME x POSITION patterns.

Does each name have a preferred position (a lattice/template that recurs across folhas), or
does it spread? For the top names: (A) the distribution of START positions (r,c) - concentrated
on few cells (template) or uniform? (B) row-band and column-band preference. (C) do name-starts
prefer certain residue positions (r%7, c%7)? Null: uniform / shuffled grids.
stdlib only. seed 1583.
"""
import os
import sys
import json
import math
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
from a190_tower_traces import side_grids

rng = random.Random(1583)
DIRS8 = [(0,1),(1,0),(0,-1),(-1,0),(1,1),(-1,-1),(1,-1),(-1,1)]
NAMES = ["NOCHA","CHASTOR","ANZACH","ALGETH","NACHO","DAXVAR","VOXAR","GETH","ACLAX","GRAPHA"]


def all_starts(word, grids):
    W = word.upper(); L = len(W); out = []
    for g in grids:
        H=len(g); Wd=len(g[0])
        for r in range(H):
            for c in range(Wd):
                if g[r][c]!=W[0]: continue
                for dr,dc in DIRS8:
                    er,ec=r+dr*(L-1),c+dc*(L-1)
                    if 0<=er<H and 0<=ec<Wd and all(g[r+dr*i][c+dc*i]==W[i] for i in range(L)):
                        out.append((r,c)); break
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = list(side_grids().values())
    ncells = 49*49
    print("nome       | ocorr | células distintas | top-célula | conc(top10/total) | banda linha | mod r%7,c%7", flush=True)
    rows = []
    for nm in NAMES:
        starts = all_starts(nm, grids)
        if not starts: continue
        cellc = Counter(starts)
        conc = sum(c for _, c in cellc.most_common(10))/len(starts)
        # expected concentration if uniform over used positions
        band = Counter("topo" if r<16 else("meio" if r<33 else "fundo") for r,c in starts)
        modr = Counter(r%7 for r,c in starts); modc = Counter(c%7 for r,c in starts)
        rows.append({"nome":nm,"ocorr":len(starts),"distintas":len(cellc),
                     "top_cell":list(cellc.most_common(1)[0][0]),"top_count":cellc.most_common(1)[0][1],
                     "conc_top10":round(conc,3),
                     "banda":dict(band),"modr_top":modr.most_common(2),"modc_top":modc.most_common(2)})
        print(f"{nm:10s} | {len(starts):5d} | {len(cellc):5d} | {cellc.most_common(1)[0]} | {conc:.2f} | {dict(band)} | r{modr.most_common(1)[0]} c{modc.most_common(1)[0]}", flush=True)

    # test: is NOCHA's start-position concentration above a uniform null?
    nm = "NOCHA"; starts = all_starts(nm, grids); cellc = Counter(starts)
    obs_top = cellc.most_common(1)[0][1]
    nstart = len(starts)
    # null: nstart points thrown uniformly over the ncells positions -> max cell count
    sims = []
    for _ in range(300):
        c = Counter(rng.randrange(ncells) for _ in range(nstart))
        sims.append(c.most_common(1)[0][1])
    m = sum(sims)/len(sims); sd = (sum((x-m)**2 for x in sims)/len(sims))**0.5
    print(f"\n[NOCHA template] célula mais usada {obs_top}× vs null uniforme {m:.1f}±{sd:.1f} z={(obs_top-m)/sd if sd else 0:+.2f}", flush=True)

    out = {"names": rows}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "234_name_position.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
