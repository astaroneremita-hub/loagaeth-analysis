# -*- coding: utf-8 -*-
"""a190 - Watchtower angels as straight-line traces inside the Loagaeth grids.

For each hierarchy name of the four Great-Table Towers (by quadrant), look for it
as a straight line (8 directions, word-search style) in every dense 49x49 Loagaeth
side. This is a 2D test, different from the earlier substring-in-row tests (#336/#349).

Null model: shuffle each grid's own letters and repeat. A name system that is really
"written" into the book must be found far above what random placement yields.

Outputs results/190_tower_traces.json (verdict + stats) and
viz/tower_traces.json (grids + found traces, for the visual).

Python stdlib only. Seed 1583.
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
import enoch

SEED = 1583
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
TOWER_PT = {"ar": "Ar", "agua": "Agua", "terra": "Terra", "fogo": "Fogo"}


def side_grids():
    """{sideKey: [49 strings of 49 letters]} for every dense side (skip 1a/1b)."""
    lv = load.leaves()
    out = {}
    for k, rows in lv.items():
        if k[-1] not in "ab":
            continue
        g = [load.letters(r) for r in rows]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            out[k] = g
    return out


def search_all(word, grids):
    """First straight-line hit of word across all grids. Returns (side,r,c,dr,dc) or None."""
    W = word.upper()
    L = len(W)
    for side, g in grids.items():
        H = len(g)
        Wd = len(g[0])
        for r in range(H):
            for c in range(Wd):
                if g[r][c] != W[0]:
                    continue
                for dr, dc in DIRS:
                    er, ec = r + dr * (L - 1), c + dc * (L - 1)
                    if not (0 <= er < H and 0 <= ec < Wd):
                        continue
                    if all(g[r + dr * i][c + dc * i] == W[i] for i in range(L)):
                        return (side, r, c, dr, dc)
    return None


def count_found(words, grids):
    return sum(1 for w in words if search_all(w, grids) is not None)


def shuffled(grid, rng):
    flat = [ch for row in grid for ch in row]
    rng.shuffle(flat)
    W = len(grid[0])
    return ["".join(flat[i:i + W]) for i in range(0, len(flat), W)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = side_grids()
    names = enoch.derive_names()
    # unique (name, tower, kind) but search each unique string once; keep best metadata
    seen = {}
    for n in names:
        seen.setdefault(n["name"], n)
    uniq = list(seen.values())

    # --- collect actual traces FIRST and write the viz payload (fast, unblocks both screens) ---
    traces = []
    for n in uniq:
        hit = search_all(n["name"], grids)
        if hit:
            side, r, c, dr, dc = hit
            L = len(n["name"])
            path = [[r + dr * i, c + dc * i] for i in range(L)]
            traces.append({
                "name": n["name"], "tower": n["tower"], "kind": n["kind"],
                "side": side, "path": path,
            })
    viz0 = {"grids": grids, "traces": traces, "towers": TOWER_PT,
            "z_big": None, "verdict": "calculando"}
    vpath = os.path.join(os.path.dirname(HERE), "viz", "tower_traces.json")
    with open(vpath, "w", encoding="utf-8") as f:
        json.dump(viz0, f, ensure_ascii=False)
    print(f"traces collected: {len(traces)} | wrote viz (pre-null)", flush=True)

    rng = random.Random(SEED)
    # by length tier (4-letter rotations inflate the inventory; test each tier honestly)
    tiers = {}
    for n in uniq:
        tiers.setdefault(len(n["name"]), []).append(n["name"])

    report_tiers = []
    TRIALS = 120
    for L in sorted(tiers):
        words = tiers[L]
        obs = count_found(words, grids)
        sims = []
        for _ in range(TRIALS):
            sg = {k: shuffled(g, rng) for k, g in grids.items()}
            sims.append(count_found(words, sg))
        mean = sum(sims) / len(sims)
        sd = (sum((x - mean) ** 2 for x in sims) / len(sims)) ** 0.5
        z = (obs - mean) / sd if sd > 0 else 0.0
        report_tiers.append({
            "len": L, "n_names": len(words), "found": obs,
            "null_mean": round(mean, 2), "null_sd": round(sd, 2), "z": round(z, 2),
        })
        print(f"len={L:2d}  names={len(words):3d}  found={obs:3d}  null={mean:5.1f}+-{sd:4.1f}  z={z:+.2f}", flush=True)

    # overall for len>=5 (drop the 4-letter rotation soup)
    big = [n["name"] for n in uniq if len(n["name"]) >= 5]
    obs_big = count_found(big, grids)
    sims = []
    for _ in range(TRIALS):
        sg = {k: shuffled(g, rng) for k, g in grids.items()}
        sims.append(count_found(big, sg))
    mean = sum(sims) / len(sims)
    sd = (sum((x - mean) ** 2 for x in sims) / len(sims)) ** 0.5
    z_big = (obs_big - mean) / sd if sd > 0 else 0.0
    print(f"\nlen>=5  names={len(big)}  found={obs_big}  null={mean:.1f}+-{sd:.1f}  z={z_big:+.2f}", flush=True)

    verdict = "REFUTADO" if z_big < 3 else "REAL"
    result = {
        "test": "Watchtower angels as straight-line traces in the Loagaeth grids",
        "seed": SEED, "trials": TRIALS,
        "n_sides": len(grids),
        "tiers": report_tiers,
        "len_ge5": {"n": len(big), "found": obs_big, "null_mean": round(mean, 2),
                    "null_sd": round(sd, 2), "z": round(z_big, 2)},
        "n_traces_total": len(traces),
        "verdict": verdict,
    }
    load.save_result("190_tower_traces", result)

    # viz payload: grids + traces
    # per-tier null map for the lesser-angels screen (len-4 chance expectation)
    tier_null = {t["len"]: {"found": t["found"], "null_mean": t["null_mean"],
                            "null_sd": t["null_sd"], "z": t["z"], "n": t["n_names"]}
                 for t in report_tiers}
    viz = {
        "grids": grids,
        "traces": traces,
        "towers": TOWER_PT,
        "z_big": round(z_big, 2),
        "verdict": verdict,
        "tier_null": tier_null,
    }
    with open(vpath, "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    print("verdict", verdict, "| traces", len(traces), "| wrote viz/tower_traces.json", flush=True)


if __name__ == "__main__":
    main()
