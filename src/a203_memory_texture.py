# -*- coding: utf-8 -*-
"""a203 - memory & texture of the field (new technical lenses).

A) MARKOV ORDER: conditional entropy H(X | previous k letters), k=0..4, on the stream.
   How much memory the generator has. Compare to shuffled (order 0).
B) ANISOTROPY: conditional entropy of HORIZONTAL bigrams vs VERTICAL bigrams. If vertical
   is more predictable (lower H), the weave is real by an information measure.
C) VERTICAL RUNS: run-lengths of equal letters down columns vs null (the warp).
D) BORDER PALETTE: which letters make the frame (col0, col48) vs interior - concrete.
E) FOLHA DIALECTS: cluster the 48 folhas by bigram profile; are there distinct zones?

Writes results/203_memory_texture.json + viz/dialects.json. Seed 1583. stdlib only.
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


def H(counter):
    n = sum(counter.values())
    if n == 0:
        return 0.0
    return -sum((v / n) * math.log2(v / n) for v in counter.values() if v)


def cond_entropy(seq, k):
    """H(X_i | X_{i-k..i-1}) over sequence seq (string)."""
    if k == 0:
        return H(Counter(seq))
    ctx = defaultdict(Counter)
    for i in range(k, len(seq)):
        ctx[seq[i - k:i]][seq[i]] += 1
    tot = sum(sum(c.values()) for c in ctx.values())
    return sum((sum(c.values()) / tot) * H(c) for c in ctx.values())


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    sides = side_grids()
    grids = list(sides.values())
    S = load.dense_stream()
    result = {"seed": 1583}

    # ---------- A: Markov order ----------
    markov = {str(k): round(cond_entropy(S, k), 4) for k in range(5)}
    sh = list(S); rng.shuffle(sh); sh = "".join(sh)
    markov_sh = {str(k): round(cond_entropy(sh, k), 4) for k in range(3)}
    result["markov"] = {"cond_entropy": markov, "shuffled": markov_sh}
    print("[A] H(X|k):", markov, "| embaralhado:", markov_sh, flush=True)

    # ---------- B: anisotropy ----------
    hb = defaultdict(Counter)  # horizontal: prev -> next
    vb = defaultdict(Counter)  # vertical
    for g in grids:
        Hh = len(g); W = len(g[0])
        for r in range(Hh):
            for c in range(W - 1):
                hb[g[r][c]][g[r][c + 1]] += 1
        for r in range(Hh - 1):
            for c in range(W):
                vb[g[r][c]][g[r + 1][c]] += 1
    def cond_from(bmap):
        tot = sum(sum(c.values()) for c in bmap.values())
        return sum((sum(c.values()) / tot) * H(c) for c in bmap.values())
    Hh = cond_from(hb); Hv = cond_from(vb)
    result["anisotropy"] = {"H_horizontal": round(Hh, 4), "H_vertical": round(Hv, 4),
                            "diff": round(Hh - Hv, 4)}
    print(f"[B] H(next|prev) horizontal={Hh:.4f}  vertical={Hv:.4f}  (menor = mais previsível)", flush=True)

    # ---------- C: vertical runs ----------
    def run_stats(gs):
        runs = []
        for g in gs:
            Hh = len(g); W = len(g[0])
            for c in range(W):
                cur = 1
                for r in range(1, Hh):
                    if g[r][c] == g[r - 1][c] and g[r][c] != "?":
                        cur += 1
                    else:
                        if cur > 1:
                            runs.append(cur)
                        cur = 1
                if cur > 1:
                    runs.append(cur)
        return runs
    obs_runs = run_stats(grids)
    obs_n = len(obs_runs); obs_max = max(obs_runs) if obs_runs else 0
    sims_n, sims_max = [], []
    for _ in range(20):
        sg = []
        for g in grids:
            flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
            sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
        rr = run_stats(sg); sims_n.append(len(rr)); sims_max.append(max(rr) if rr else 0)
    mn = sum(sims_n) / len(sims_n); sdn = (sum((x - mn) ** 2 for x in sims_n) / len(sims_n)) ** 0.5
    zc = (obs_n - mn) / sdn if sdn else 0
    result["vertical_runs"] = {"n_runs_ge2": obs_n, "max_run": obs_max,
                               "null_n_mean": round(mn, 1), "null_n_sd": round(sdn, 1), "z_n": round(zc, 2),
                               "null_max_mean": round(sum(sims_max) / len(sims_max), 1)}
    print(f"[C] corridas verticais >=2: obs {obs_n} (max {obs_max}) vs null {mn:.0f}±{sdn:.0f}  z={zc:+.2f}", flush=True)

    # ---------- D: border palette ----------
    def col_letters(ci):
        c = Counter()
        for g in grids:
            for r in range(len(g)):
                if g[r][ci] != "?":
                    c[g[r][ci]] += 1
        return c
    glob = Counter(ch for g in grids for row in g for ch in row if ch != "?")
    gtot = sum(glob.values())
    def enrich(c):
        n = sum(c.values())
        return sorted(((l, round((c[l] / n) / (glob[l] / gtot), 2), c[l]) for l in c),
                      key=lambda x: -x[1])[:8]
    result["border_palette"] = {
        "col0_top_enriched": enrich(col_letters(0)),
        "col48_top_enriched": enrich(col_letters(48)),
        "global_top": [l for l, _ in glob.most_common(8)],
    }
    print("[D] borda col0 letras enriquecidas:", result["border_palette"]["col0_top_enriched"][:5], flush=True)

    # ---------- E: folha dialects ----------
    # per-folha bigram profile (horizontal+vertical), cosine distance
    def profile(g):
        c = Counter()
        Hh = len(g); W = len(g[0])
        for r in range(Hh):
            for cc in range(W - 1):
                c[g[r][cc] + g[r][cc + 1]] += 1
        return c
    folhas = sorted(sides.keys(), key=lambda s: (int("".join(ch for ch in s if ch.isdigit())), s))
    profs = {s: profile(sides[s]) for s in folhas}
    keys = sorted(set(k for p in profs.values() for k in p))
    import math as _m
    def vec(p):
        n = sum(p.values()) or 1
        return {k: p[k] / n for k in p}
    vecs = {s: vec(profs[s]) for s in folhas}
    def cos(a, b):
        dot = sum(a[k] * b.get(k, 0) for k in a)
        na = _m.sqrt(sum(v * v for v in a.values())); nb = _m.sqrt(sum(v * v for v in b.values()))
        return dot / (na * nb) if na and nb else 0
    # distance of each folha to the book mean
    mean = defaultdict(float)
    for s in folhas:
        for k, v in vecs[s].items():
            mean[k] += v / len(folhas)
    outliers = sorted(((s, round(1 - cos(vecs[s], mean), 4)) for s in folhas), key=lambda x: -x[1])
    result["dialects"] = {"most_distinct_folhas": outliers[:8], "most_typical": outliers[-5:]}
    print("[E] folhas mais distintas (dialeto):", outliers[:6], flush=True)

    # viz payload: distance-to-mean per folha (ordered)
    viz = {"folhas": [s for s in folhas], "distance": [round(1 - cos(vecs[s], mean), 4) for s in folhas]}
    with open(os.path.join(os.path.dirname(HERE), "viz", "dialects.json"), "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)

    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "203_memory_texture.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
