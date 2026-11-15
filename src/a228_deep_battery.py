# -*- coding: utf-8 -*-
"""a228 - deep hidden-pattern battery (HIPOTESES_PROFUNDAS.md). Runs the automatable
families with nulls, flags any z>3 (a real hidden pattern).

Families: A modular lattice (letter x residue r/c/r+c/r-c mod m), B letter periodicity,
D diagonal autocorrelation + 7x7 block position, F null-cell positions + column twins.
Null = within-folha shuffle (preserves letter freq). seed 1583, stdlib only.
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

SEED = 1583
rng = random.Random(SEED)


def shuffle_grid(g):
    flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
    return ["".join(flat[i:i+W]) for i in range(0, len(flat), W)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = list(side_grids().values())
    alpha = sorted(set(ch for g in grids for row in g for ch in row if ch != "?"))
    flags = []

    def flag(name, z, detail=""):
        tag = "  *** z>3 ***" if abs(z) >= 3 else ""
        print(f"  {name:36s} z={z:+6.2f}{tag} {detail}", flush=True)
        if abs(z) >= 3:
            flags.append({"name": name, "z": round(z, 2), "detail": detail})

    # ---------- A modular lattice ----------
    print("[A] LATTICE MODULAR (letra x classe de resíduo):", flush=True)
    def chi2_mod(gs, axis, m):
        # contingency letter x residue
        tab = defaultdict(Counter)
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W):
                    ch = g[r][c]
                    if ch == "?": continue
                    if axis == "r": res = r % m
                    elif axis == "c": res = c % m
                    elif axis == "rc": res = (r+c) % m
                    else: res = (r-c) % m
                    tab[ch][res] += 1
        # chi2 vs independence
        tot = sum(sum(v.values()) for v in tab.values())
        rowt = {l: sum(tab[l].values()) for l in tab}
        colt = Counter()
        for l in tab:
            for res, v in tab[l].items(): colt[res] += v
        x2 = 0.0
        for l in tab:
            for res in range(m):
                exp = rowt[l]*colt[res]/tot
                if exp > 0:
                    x2 += (tab[l].get(res,0)-exp)**2/exp
        return x2
    TRIALS = 25
    for axis in ("r", "c", "rc", "rd"):
        for m in (2, 3, 5, 7):
            obs = chi2_mod(grids, axis, m)
            sims = [chi2_mod([shuffle_grid(g) for g in grids], axis, m) for _ in range(TRIALS)]
            mu = sum(sims)/len(sims); sd = (sum((x-mu)**2 for x in sims)/len(sims))**0.5
            z = (obs-mu)/sd if sd else 0
            flag(f"A: letra x {axis} mod {m}", z, f"chi2={obs:.0f} null~{mu:.0f}")

    # ---------- B letter periodicity ----------
    print("[B] PERIODICIDADE POR LETRA (indicador, autocorr):", flush=True)
    S = load.dense_stream(); N = len(S)
    freq = Counter(S)
    for L in [l for l, _ in freq.most_common(6)] + [l for l, _ in freq.most_common()[-4:]]:
        ind = [1 if ch == L else 0 for ch in S]
        p = sum(ind)/N
        base = p*p
        best = (0, 1)
        for lag in list(range(2, 60)) + [49, 98, 2401]:
            if lag >= N: continue
            n = N-lag
            ac = sum(1 for i in range(n) if ind[i] and ind[i+lag])/n
            z = (ac-base)/math.sqrt(base*(1-base)/n) if base > 0 else 0
            if abs(z) > abs(best[0]): best = (z, lag)
        flag(f"B: letra {L} periodicidade", best[0], f"melhor lag={best[1]}")

    # ---------- D diagonal autocorr + 7x7 block ----------
    print("[D] DIAGONAL + BLOCO 7x7:", flush=True)
    def diag_match(gs, k, anti):
        hit = tot = 0
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W):
                    rr = r+k; cc = c-k if anti else c+k
                    if 0 <= rr < H and 0 <= cc < W:
                        tot += 1
                        if g[r][c] == g[rr][cc]: hit += 1
        return hit/tot if tot else 0
    for k in (2, 3, 4, 5):
        for anti in (False, True):
            obs = diag_match(grids, k, anti)
            sims = [diag_match([shuffle_grid(g) for g in grids], k, anti) for _ in range(15)]
            mu = sum(sims)/len(sims); sd = (sum((x-mu)**2 for x in sims)/len(sims))**0.5
            z = (obs-mu)/sd if sd else 0
            flag(f"D: diag k={k} {'anti' if anti else 'desc'}", z, f"match={obs:.4f}")
    # 7x7 block position
    def block_chi(gs):
        tab = defaultdict(Counter)
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W):
                    ch = g[r][c]
                    if ch == "?": continue
                    tab[ch][(r % 7)*7+(c % 7)] += 1
        tot = sum(sum(v.values()) for v in tab.values())
        rowt = {l: sum(tab[l].values()) for l in tab}; colt = Counter()
        for l in tab:
            for k2, v in tab[l].items(): colt[k2] += v
        x2 = 0
        for l in tab:
            for k2 in range(49):
                exp = rowt[l]*colt[k2]/tot
                if exp > 0: x2 += (tab[l].get(k2, 0)-exp)**2/exp
        return x2
    obs = block_chi(grids)
    sims = [block_chi([shuffle_grid(g) for g in grids]) for _ in range(15)]
    mu = sum(sims)/len(sims); sd = (sum((x-mu)**2 for x in sims)/len(sims))**0.5
    flag("D: posição no bloco 7x7", (obs-mu)/sd if sd else 0, f"chi2={obs:.0f} null~{mu:.0f}")

    # ---------- F null-cell positions ----------
    print("[F] NULOS '?' e COLUNAS GÊMEAS:", flush=True)
    qpos = Counter()
    for g in grids:
        for r in range(len(g)):
            for c in range(len(g[0])):
                if g[r][c] == "?": qpos[(r, c)] += 1
    print(f"  células '?' totais: {sum(qpos.values())}; posições distintas: {len(qpos)}", flush=True)

    result = {"seed": SEED, "flags": flags, "n_flags": len(flags)}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "228_deep_battery.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print(f"\nFLAGS (z>3): {flags if flags else 'NENHUM'}", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
