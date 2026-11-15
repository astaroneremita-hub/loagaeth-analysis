# -*- coding: utf-8 -*-
"""a205 - what REPEATS, and quadrant structure.

REPEATS - repeated n-grams (n=5..10) in the book stream: how many distinct strings recur,
          the most-repeated long chunks (the real recurring 'phrases'), vs null.
QUAD    - split each 49x49 into four ~24x24 quadrants; compare letter profiles across them
          (echo of the Tower's 4 sub-angles?) via chi-square, vs null.
DUP     - exact duplicate rows and columns across the whole book, vs null.

Writes results/205_repeats_quadrants.json + viz/repeats.json. Seed 1583. stdlib only.
"""
import os
import sys
import json
import math
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
from a190_tower_traces import side_grids


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    sides = side_grids()
    grids = list(sides.values())
    S = load.dense_stream()
    N = len(S)
    result = {"seed": 1583}

    # ---------- repeated n-grams ----------
    def repeats(stream, n):
        c = Counter(stream[i:i + n] for i in range(len(stream) - n + 1))
        rep = {g: v for g, v in c.items() if v >= 2}
        return rep
    rep_report = {}
    viz_rep = {}
    sh = list(S); rng.shuffle(sh); sh = "".join(sh)
    for n in (5, 6, 7, 8, 10):
        r = repeats(S, n)
        rn = repeats(sh, n)
        distinct = len(r); distinct_null = len(rn)
        top = sorted(r.items(), key=lambda x: -x[1])[:12]
        rep_report[str(n)] = {"distinct_repeated": distinct, "null_distinct": distinct_null,
                              "max_mult": max(r.values()) if r else 0,
                              "top": top[:6]}
        viz_rep[str(n)] = [[g, v] for g, v in top]
        print(f"[REP] n={n:2d} distintos repetidos {distinct:5d} (null {distinct_null:5d})  max {max(r.values()) if r else 0}  top {top[:3]}", flush=True)

    # ---------- quadrants ----------
    glob = Counter(ch for g in grids for row in g for ch in row if ch != "?")
    alpha = sorted(glob); gtot = sum(glob.values())
    def quad_counts(gs):
        # quadrants split at row/col 24 (center excluded)
        Q = {"NO": Counter(), "NE": Counter(), "SO": Counter(), "SE": Counter()}
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W):
                    ch = g[r][c]
                    if ch == "?" or r == 24 or c == 24:
                        continue
                    k = ("N" if r < 24 else "S") + ("O" if c < 24 else "E")
                    Q[k][ch] += 1
        return Q
    Q = quad_counts(grids)
    # chi-square between quadrants: compare each quadrant to the pooled
    pooled = Counter()
    for q in Q.values():
        pooled.update(q)
    ptot = sum(pooled.values())
    chis = {}
    for k, cnt in Q.items():
        n = sum(cnt.values()); x2 = 0.0
        for a in alpha:
            exp = n * pooled.get(a, 0) / ptot
            if exp > 0:
                x2 += (cnt.get(a, 0) - exp) ** 2 / exp
        chis[k] = round(x2, 1)
    obs_quad = sum(chis.values())
    sims = []
    for _ in range(15):
        sg = []
        for g in grids:
            flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
            sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
        Qs = quad_counts(sg); ps = Counter()
        for q in Qs.values():
            ps.update(q)
        pt = sum(ps.values()); tot = 0.0
        for k, cnt in Qs.items():
            n = sum(cnt.values())
            for a in alpha:
                exp = n * ps.get(a, 0) / pt
                if exp > 0:
                    tot += (cnt.get(a, 0) - exp) ** 2 / exp
        sims.append(tot)
    m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
    z = (obs_quad - m) / sd if sd else 0
    result["quadrants"] = {"chi_per_quad": chis, "total_chi": round(obs_quad, 1),
                           "null_mean": round(m, 1), "null_sd": round(sd, 1), "z": round(z, 2)}
    print(f"[QUAD] chi2 por quadrante {chis} total {obs_quad:.0f} vs null {m:.0f}±{sd:.0f} z={z:+.2f}", flush=True)

    # ---------- duplicate rows / columns ----------
    all_rows = [row for g in grids for row in g]
    all_cols = ["".join(g[r][c] for r in range(len(g))) for g in grids for c in range(len(g[0]))]
    def dup_count(strings):
        c = Counter(strings)
        return sum(v for v in c.values() if v >= 2) - sum(1 for v in c.values() if v >= 2), c.most_common(3)
    dr, top_r = dup_count(all_rows)
    dc, top_c = dup_count(all_cols)
    # null
    def dup_null(axis, trials=10):
        out = []
        for _ in range(trials):
            sg = []
            for g in grids:
                flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
                sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
            if axis == "row":
                strs = [row for g in sg for row in g]
            else:
                strs = ["".join(g[r][c] for r in range(len(g))) for g in sg for c in range(len(g[0]))]
            c = Counter(strs); out.append(sum(v for v in c.values() if v >= 2) - sum(1 for v in c.values() if v >= 2))
        return sum(out) / len(out)
    result["duplicates"] = {"dup_rows_extra": dr, "dup_rows_null": round(dup_null("row"), 2),
                            "dup_cols_extra": dc, "dup_cols_null": round(dup_null("col"), 2),
                            "top_rows": top_r, "top_cols": top_c}
    print(f"[DUP] linhas duplicadas extra {dr} (null {result['duplicates']['dup_rows_null']}); colunas {dc} (null {result['duplicates']['dup_cols_null']})", flush=True)

    with open(os.path.join(os.path.dirname(HERE), "viz", "repeats.json"), "w", encoding="utf-8") as f:
        json.dump({"repeats": viz_rep, "quadrants": result["quadrants"]}, f, ensure_ascii=False)
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "205_repeats_quadrants.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
