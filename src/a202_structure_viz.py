# -*- coding: utf-8 -*-
"""a202 - deterministic structure curves for the viz (significance already from a201).

Full 1D autocorrelation curve (lags 1..120), per-column and per-row chi-square of the
letter distribution, and a 2D autocorrelation grid of small offsets. No nulls (fast).

Writes viz/structure.json. stdlib only.
"""
import os
import sys
import json
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
from a190_tower_traces import side_grids


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sides = side_grids()
    grids = list(sides.values())
    S = load.dense_stream()
    N = len(S)
    alpha = sorted(set(S))
    f = Counter(S)
    base = sum(f[a] ** 2 for a in alpha) / (N * N)

    # 1D autocorrelation curve
    def ac(lag):
        n = N - lag
        return sum(1 for i in range(n) if S[i] == S[i + lag]) / n
    lags = list(range(1, 121))
    curve = [round(ac(l), 5) for l in lags]

    # per-column / per-row chi-square
    glob = Counter(S); gtot = sum(glob.values())
    def chi_axis(axis):
        per = defaultdict(Counter)
        for g in grids:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W):
                    ch = g[r][c]
                    if ch == "?":
                        continue
                    per[c if axis == "col" else r][ch] += 1
        arr = []
        for idx in range(49):
            cnt = per.get(idx, Counter()); n = sum(cnt.values()); x2 = 0.0
            for a in alpha:
                exp = n * glob.get(a, 0) / gtot
                if exp > 0:
                    x2 += (cnt.get(a, 0) - exp) ** 2 / exp
            arr.append(round(x2, 1))
        return arr
    col_chi = chi_axis("col")
    row_chi = chi_axis("row")

    # 2D autocorrelation grid (offsets dr,dc in -4..4)
    def m2(dr, dc):
        hit = tot = 0
        for g in grids:
            H = len(g); W = len(g[0])
            for r in range(H):
                rr = r + dr
                if not (0 <= rr < H):
                    continue
                row = g[r]; row2 = g[rr]
                for c in range(W):
                    cc = c + dc
                    if 0 <= cc < W:
                        tot += 1
                        if row[c] == row2[cc]:
                            hit += 1
        return hit / tot if tot else 0
    R = 4
    grid2d = [[round(m2(dr, dc), 4) for dc in range(-R, R + 1)] for dr in range(-R, R + 1)]

    out = {"base": round(base, 5), "lags": lags, "ac_curve": curve,
           "col_chi": col_chi, "row_chi": row_chi,
           "ac2_grid": grid2d, "ac2_radius": R,
           "notable_lags": {"1": curve[0], "7": curve[6], "49": round(ac(49), 5),
                            "98": round(ac(98), 5), "2401": round(ac(2401), 5)}}
    with open(os.path.join(os.path.dirname(HERE), "viz", "structure.json"), "w", encoding="utf-8") as fp:
        json.dump(out, fp, ensure_ascii=False)
    print("col0 chi2", col_chi[0], "| ac lag1", curve[0], "lag49", out["notable_lags"]["49"],
          "| 2D(0,1)", grid2d[R][R + 1], "(1,0)", grid2d[R + 1][R], flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
