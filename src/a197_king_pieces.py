# -*- coding: utf-8 -*-
"""a197 - Do the KINGS appear as PIECES? Split each 8-letter king into halves
(BATAIVAH -> BATA + IVAH) and test:

  1) does each half appear at all (straight, 8 dirs)? how many times / how many folhas?
  2) do the two halves appear JOINED - the full name as two straight strokes meeting at
     a turn (H1 ends, H2 starts on a neighbouring cell)? observed vs null.

Honest: 4-letter halves are common, so they appear a lot by chance (like lesser angels).
The real test is the JOINT - the pieces landing together to spell the king. Null =
within-folha shuffle (50 trials). stdlib only. Seed 1583.
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
TRIALS = 50
DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def occ_straight(word, g):
    """all straight-8 occurrences: list of (r,c,dr,dc,end_r,end_c)."""
    W = word.upper(); L = len(W); H = len(g); Wd = len(g[0]); out = []
    for r in range(H):
        for c in range(Wd):
            if g[r][c] != W[0]:
                continue
            for dr, dc in DIRS8:
                er, ec = r + dr * (L - 1), c + dc * (L - 1)
                if 0 <= er < H and 0 <= ec < Wd and all(g[r + dr * i][c + dc * i] == W[i] for i in range(L)):
                    out.append((r, c, dr, dc, er, ec))
    return out


def joint_count(h1, h2, g):
    """full name as two straight strokes: H1 ends at e, H2 starts at an 8-neighbour of e."""
    e1 = occ_straight(h1, g)
    if not e1:
        return 0
    s2 = {}
    for (r, c, dr, dc, er, ec) in occ_straight(h2, g):
        s2.setdefault((r, c), []).append(1)  # start cells of H2
    cnt = 0
    for (r, c, dr, dc, er, ec) in e1:
        for ddr, ddc in DIRS8:
            if (er + ddr, ec + ddc) in s2:
                cnt += 1
                break
    return cnt


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = list(side_grids().values())
    kings = [enoch.king(el) for el in enoch.TOWERS]

    def total_occ(word):
        return sum(len(occ_straight(word, g)) for g in grids)

    def total_joint(h1, h2):
        return sum(joint_count(h1, h2, g) for g in grids)

    rng = random.Random(SEED)
    def shuffled(grid):
        flat = [ch for row in grid for ch in row]; rng.shuffle(flat); Wd = len(grid[0])
        return ["".join(flat[i:i + Wd]) for i in range(0, len(flat), Wd)]

    rows = []
    for k in kings:
        h1, h2 = k[:4], k[4:]
        o1, o2 = total_occ(h1), total_occ(h2)
        oj = total_joint(h1, h2)
        # null for joint
        sims = []
        for _ in range(TRIALS):
            sg = [shuffled(g) for g in grids]
            sims.append(sum(joint_count(h1, h2, g) for g in sg))
        m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
        z = (oj - m) / sd if sd else 0.0
        rows.append({"king": k, "h1": h1, "h2": h2, "occ_h1": o1, "occ_h2": o2,
                     "joint": oj, "joint_null_mean": round(m, 2), "joint_null_sd": round(sd, 2),
                     "joint_z": round(z, 2)})
        print(f"{k}  {h1}={o1:4d}  {h2}={o2:4d}  JUNTA obs={oj:3d} null={m:5.1f}+-{sd:4.1f} z={z:+.2f}", flush=True)

    out = {"test": "Kings as two joined 4-letter pieces", "seed": SEED, "trials": TRIALS, "kings": rows}
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "197_king_pieces.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
