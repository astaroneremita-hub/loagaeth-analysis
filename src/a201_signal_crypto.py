# -*- coding: utf-8 -*-
"""a201 - signal / cryptanalysis battery. New technical lenses, hunting STRUCTURE
(not names): a hidden period, a cipher key length, a positional template, a 2D tiling.

Modules:
  IC   - Index of Coincidence (whole book + per folha) vs random & vs a language band.
  KAS  - Kasiski: repeated trigrams, GCD of their gaps -> candidate cipher period.
  AC1  - 1D autocorrelation of the stream at lags 1..120 (watch 7, 49, 98) vs null band.
  POS  - positional bias: per column index and per row index, chi-square of the letter
         distribution vs the global one -> is any column/row a template/grille?
  AC2  - 2D autocorrelation: for offsets (dr,dc), P(cell == cell+offset) vs null.

Anything with z>3 over its null is flagged CONFIRMADO NOVO. Seed 1583. stdlib only.
"""
import os
import sys
import json
import random
import math
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
from a190_tower_traces import side_grids

SEED = 1583


def ic(s):
    n = len(s)
    if n < 2:
        return 0.0
    f = Counter(s)
    return sum(v * (v - 1) for v in f.values()) / (n * (n - 1))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(SEED)
    sides = side_grids()
    grids = list(sides.values())
    S = load.dense_stream()
    N = len(S)
    alpha = sorted(set(S))
    K = len(alpha)
    result = {"seed": SEED, "N": N, "alpha": K, "flags": []}

    def flag(name, z, detail):
        if abs(z) >= 3:
            result["flags"].append({"name": name, "z": round(z, 2), "detail": detail})
            print(f"  *** CONFIRMADO NOVO? {name}  z={z:+.2f}  {detail}", flush=True)

    # ---------- IC ----------
    obs_ic = ic(S)
    rand_ic = 1.0 / K
    # null: shuffle
    sims = [ic("".join(rng.sample(S, min(len(S), 20000)))) for _ in range(20)]
    # IC is scale-free-ish; compare obs on a sample for fairness
    samp = S[:20000]
    obs_ic_s = ic(samp)
    m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
    z = (obs_ic_s - m) / sd if sd else 0.0
    result["IC"] = {"obs": round(obs_ic, 5), "random_1_over_K": round(rand_ic, 5),
                    "obs_sample": round(obs_ic_s, 5), "null_mean": round(m, 5), "null_sd": round(sd, 5), "z": round(z, 2)}
    print(f"[IC] obs={obs_ic:.5f}  aleatorio(1/{K})={rand_ic:.5f}  null={m:.5f}±{sd:.5f}  z={z:+.2f}", flush=True)
    flag("IC acima do aleatorio", z, f"IC={obs_ic:.4f}")

    # ---------- Kasiski ----------
    tri = defaultdict(list)
    for i in range(N - 3):
        tri[S[i:i + 3]].append(i)
    gaps = Counter()
    for g, pos in tri.items():
        if len(pos) < 2:
            continue
        for a, b in zip(pos, pos[1:]):
            d = b - a
            if 2 <= d <= 400:
                gaps[d] += 1
    # factor histogram
    fac = Counter()
    for d, cnt in gaps.items():
        for p in range(2, 50):
            if d % p == 0:
                fac[p] += cnt
    top_fac = fac.most_common(10)
    result["Kasiski"] = {"top_factors": top_fac, "n_repeated_trigrams": sum(1 for p in tri.values() if len(p) > 1)}
    print(f"[KAS] fatores de gap mais comuns: {top_fac[:6]}", flush=True)

    # ---------- 1D autocorrelation ----------
    def autocorr(stream, lag):
        n = len(stream) - lag
        return sum(1 for i in range(n) if stream[i] == stream[i + lag]) / n
    base = sum(Counter(S)[a] ** 2 for a in alpha) / (N * N)  # expected match prob
    acs = {}
    peaks = []
    for lag in list(range(1, 121)) + [196, 245, 2401, 49 * 49]:
        if lag < N:
            acs[lag] = autocorr(S, lag)
    # null band from base
    sd_est = math.sqrt(base * (1 - base) / (N))  # rough
    for lag, v in acs.items():
        z = (v - base) / sd_est if sd_est else 0
        if abs(z) >= 5 and lag in (7, 49, 98, 2401):
            flag(f"autocorr lag {lag}", z, f"match={v:.4f} vs base {base:.4f}")
    result["AC1"] = {"base": round(base, 5),
                     "notable": {str(l): round(acs[l], 5) for l in (1, 7, 48, 49, 50, 98, 2401) if l in acs},
                     "max_lag": max(acs, key=acs.get), "max_val": round(max(acs.values()), 5)}
    print(f"[AC1] base={base:.4f}  lag1={acs.get(1):.4f} lag7={acs.get(7):.4f} lag49={acs.get(49):.4f}  pico lag={max(acs,key=acs.get)}({max(acs.values()):.4f})", flush=True)

    # ---------- positional bias (template) ----------
    glob = Counter(S)
    gtot = sum(glob.values())
    def chi2_positions(axis):
        # axis 'col' or 'row'; aggregate per index 0..48 across all grids
        per = defaultdict(Counter)
        for g in grids:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W):
                    ch = g[r][c]
                    if ch == "?":
                        continue
                    idx = c if axis == "col" else r
                    per[idx][ch] += 1
        chis = {}
        for idx, cnt in per.items():
            n = sum(cnt.values())
            x2 = 0.0
            for a in alpha:
                exp = n * glob.get(a, 0) / gtot
                if exp > 0:
                    x2 += (cnt.get(a, 0) - exp) ** 2 / exp
            chis[idx] = x2
        return chis
    col_chi = chi2_positions("col")
    row_chi = chi2_positions("row")
    df = K - 1
    # null: shuffle each grid, recompute max chi2
    def maxchi_null(axis, trials=15):
        out = []
        for _ in range(trials):
            sg = []
            for g in grids:
                flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
                sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
            per = defaultdict(Counter)
            for g in sg:
                H = len(g); W = len(g[0])
                for r in range(H):
                    for c in range(W):
                        ch = g[r][c]
                        if ch == "?":
                            continue
                        idx = c if axis == "col" else r
                        per[idx][ch] += 1
            mx = 0
            for idx, cnt in per.items():
                n = sum(cnt.values()); x2 = 0.0
                for a in alpha:
                    exp = n * glob.get(a, 0) / gtot
                    if exp > 0:
                        x2 += (cnt.get(a, 0) - exp) ** 2 / exp
                mx = max(mx, x2)
            out.append(mx)
        return out
    obs_col_max = max(col_chi.values()); obs_row_max = max(row_chi.values())
    nc = maxchi_null("col"); nr = maxchi_null("row")
    mc = sum(nc) / len(nc); sdc = (sum((x - mc) ** 2 for x in nc) / len(nc)) ** 0.5
    mr = sum(nr) / len(nr); sdr = (sum((x - mr) ** 2 for x in nr) / len(nr)) ** 0.5
    zc = (obs_col_max - mc) / sdc if sdc else 0; zr = (obs_row_max - mr) / sdr if sdr else 0
    result["POS"] = {"df": df,
                     "col_max_chi2": round(obs_col_max, 1), "col_null_mean": round(mc, 1), "col_null_sd": round(sdc, 1), "col_z": round(zc, 2),
                     "col_worst_index": max(col_chi, key=col_chi.get),
                     "row_max_chi2": round(obs_row_max, 1), "row_null_mean": round(mr, 1), "row_null_sd": round(sdr, 1), "row_z": round(zr, 2),
                     "row_worst_index": max(row_chi, key=row_chi.get)}
    print(f"[POS] coluna max chi2={obs_col_max:.0f} (col {max(col_chi,key=col_chi.get)}) null {mc:.0f}±{sdc:.0f} z={zc:+.2f}", flush=True)
    print(f"[POS] linha  max chi2={obs_row_max:.0f} (lin {max(row_chi,key=row_chi.get)}) null {mr:.0f}±{sdr:.0f} z={zr:+.2f}", flush=True)
    flag("viés posicional de coluna", zc, f"col {max(col_chi,key=col_chi.get)} chi2={obs_col_max:.0f}")
    flag("viés posicional de linha", zr, f"lin {max(row_chi,key=row_chi.get)} chi2={obs_row_max:.0f}")

    # ---------- 2D autocorrelation ----------
    offsets = [(0, 1), (1, 0), (1, 1), (1, -1), (0, 7), (7, 0), (7, 7), (0, 48), (48, 0), (24, 24)]
    def match2d(gs, dr, dc):
        hit = tot = 0
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W):
                    rr, cc = r + dr, c + dc
                    if 0 <= rr < H and 0 <= cc < W:
                        tot += 1
                        if g[r][c] == g[rr][cc]:
                            hit += 1
        return hit / tot if tot else 0
    ac2 = {}
    for (dr, dc) in offsets:
        obs = match2d(grids, dr, dc)
        sims = []
        for _ in range(12):
            sg = []
            for g in grids:
                flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
                sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
            sims.append(match2d(sg, dr, dc))
        m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
        z = (obs - m) / sd if sd else 0
        ac2[f"{dr},{dc}"] = {"obs": round(obs, 4), "null_mean": round(m, 4), "null_sd": round(sd, 4), "z": round(z, 2)}
        print(f"[AC2] offset ({dr:3d},{dc:3d}) match={obs:.4f} null={m:.4f}±{sd:.4f} z={z:+.2f}", flush=True)
        flag(f"autocorr 2D offset ({dr},{dc})", z, f"match={obs:.4f}")
    result["AC2"] = ac2

    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "201_signal_crypto.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("FLAGS:", result["flags"] if result["flags"] else "nenhum z>=3 novo", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
