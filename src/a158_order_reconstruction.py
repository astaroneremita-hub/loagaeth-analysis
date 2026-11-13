"""
158 - DECISIVE TEST (#328): recover Dee's leaf order from CONTENT ALONE, blind to position.

The gradient (#317/#327) is confirmatory on an exploratory finding. This is the clean out-of-sample test:
strip the leaf numbers, build a distance matrix from each leaf's statistical features, and let an ordering
algorithm (spectral seriation + nearest-neighbour TSP) propose a sequence. If the recovered order matches
Dee's historical sequence far above random orders, the content itself encodes the sequence.

Units: leaves 2..48 (47 consecutive clean square grids; leaf 1 is segmented, leaf 49 absent).
Features: letter-frequency profile (primary); bigram profile (secondary check).
Methods: spectral seriation (Fiedler vector of the similarity-graph Laplacian) + greedy NN-TSP + 2-opt.
Score: |Spearman(recovered, true)|, taking the max over the sequence and its reverse (reflection symmetry).
Null: 100,000 random orders -> distribution of |Spearman vs true|. FROZEN: features, methods, score defined
before running; no tuning to fit Dee's order.
"""
import json
import random
import numpy as np
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum

V = set("AEIOU")


def profiles(bigram=False):
    book = base_book()
    prof = {}
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if not g:
            continue
        n = tnum(k)
        if bigram:
            c = Counter()
            for row in g:
                s = "".join(x for x in row if x.isalpha())
                for i in range(len(s) - 1):
                    c[s[i:i + 2]] += 1
        else:
            c = Counter(x for row in g for x in row if x.isalpha())
        if c:
            prof.setdefault(n, Counter()).update(c)
    return prof


def matrix(prof):
    ns = sorted(prof)
    keys = sorted({k for p in prof.values() for k in p})
    X = np.array([[prof[n].get(k, 0) for k in keys] for n in ns], float)
    X = X / X.sum(1, keepdims=True)                      # row-normalise to fractions
    # cosine similarity
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    S = Xn @ Xn.T
    np.fill_diagonal(S, 0)
    return ns, S


def spectral_order(S):
    d = S.sum(1)
    L = np.diag(d) - S
    # normalised Laplacian for seriation
    dinv = 1 / np.sqrt(np.maximum(d, 1e-12))
    Ln = np.diag(dinv) @ L @ np.diag(dinv)
    w, V = np.linalg.eigh(Ln)
    fiedler = V[:, 1]                                    # 2nd smallest eigenvector
    return np.argsort(fiedler)


def nn_tsp(S):
    D = 1 - S
    n = len(D)
    best = None
    for start in range(n):
        unv = set(range(n)); cur = start; unv.discard(cur); path = [cur]
        while unv:
            nxt = min(unv, key=lambda j: D[cur, j]); path.append(nxt); unv.discard(nxt); cur = nxt
        cost = sum(D[path[i], path[i + 1]] for i in range(n - 1))
        if best is None or cost < best[0]:
            best = (cost, path)
    # 2-opt
    path = best[1][:]

    def tl(p):
        return sum(D[p[i], p[i + 1]] for i in range(len(p) - 1))
    improved = True
    while improved:
        improved = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                np_ = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
                if tl(np_) < tl(path) - 1e-12:
                    path = np_; improved = True
    return np.array(path)


def spearman(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    ra = a.argsort().argsort(); rb = b.argsort().argsort()
    return np.corrcoef(ra, rb)[0, 1]


def score(order, true_idx):
    rho = spearman(order, true_idx)
    return max(abs(rho), abs(spearman(order[::-1], true_idx)))


def run(perm_n=100000):
    out = {}
    for tag, big in [("letter_freq", False), ("bigram", True)]:
        prof = profiles(big)
        ns, S = matrix(prof)
        true_idx = np.arange(len(ns))                   # Dee order = sorted leaf numbers
        sp = spectral_order(S)
        ts = nn_tsp(S)
        sp_sc = score(sp, true_idx); ts_sc = score(ts, true_idx)
        rng = random.Random(328)
        perm = []
        base = list(range(len(ns)))
        for _ in range(perm_n):
            r = base[:]; rng.shuffle(r)
            perm.append(score(np.array(r), true_idx))
        perm = np.array(perm)
        out[tag] = {
            "n_leaves": len(ns), "leaves": [int(x) for x in ns],
            "spectral_score": round(float(sp_sc), 4), "tsp_score": round(float(ts_sc), 4),
            "random_mean": round(float(perm.mean()), 4), "random_sd": round(float(perm.std()), 4),
            "p_spectral": round(float((perm >= sp_sc).mean()), 6),
            "p_tsp": round(float((perm >= ts_sc).mean()), 6),
            "spectral_order_leaves": [int(ns[i]) for i in sp],
        }
    load.save_result("158_order_reconstruction", out)
    return out


if __name__ == "__main__":
    r = run()
    print("ORDER RECONSTRUCTION #328 (blind to position)\n")
    for tag in ("letter_freq", "bigram"):
        d = r[tag]
        print("features = %s  (%d leaves 2..48)" % (tag, d["n_leaves"]))
        print("  spectral seriation: |Spearman vs Dee| = %.3f   (random %.3f +- %.3f)  p=%.2g" % (
            d["spectral_score"], d["random_mean"], d["random_sd"], d["p_spectral"]))
        print("  NN-TSP + 2opt:      |Spearman vs Dee| = %.3f   p=%.2g" % (d["tsp_score"], d["p_tsp"]))
    print("\nspectral order (letter_freq):", r["letter_freq"]["spectral_order_leaves"])
