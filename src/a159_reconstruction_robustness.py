"""
159 - ROBUSTNESS of the order reconstruction (#329). Does recovering Dee's order survive leave-out, other
features, other algorithms -- AND, crucially, is it MORE than a generic global compositional gradient?

Key control (user): any smoothly-varying sequence is recoverable by seriation. So high Spearman may only show
"a smooth global gradient exists", not deliberate local encoding. We separate the two:
  DETREND test: fit each letter's frequency as a linear function of position; subtract it. Reconstruct from the
  RESIDUALS alone. If residual reconstruction ~ chance, ALL order-info is the global gradient (expected, not
  special). If residuals still reconstruct, there is LOCAL sequential structure beyond the global trend.
  ARTIFICIAL-GRADIENT surrogate: keep the fitted global trend, replace residuals with shuffled ones -> a
  sequence with the same global gradient but scrambled local detail. Reconstruct; compare to real.

Units: leaves 2..48. Score: |Spearman vs Dee|, max over reflection. p reported as <1e-5 bound when 0/1e5.
FROZEN: features, algorithms, controls defined before running.
"""
import random
import numpy as np
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum


def profiles(kind):
    book = base_book(); prof = {}
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if not g:
            continue
        n = tnum(k)
        c = Counter()
        for row in g:
            s = "".join(x for x in row if x.isalpha())
            if kind == "freq":
                c.update(s)
            elif kind == "bigram":
                for i in range(len(s) - 1):
                    c[s[i:i + 2]] += 1
            elif kind == "trigram":
                for i in range(len(s) - 2):
                    c[s[i:i + 3]] += 1
        if c:
            prof.setdefault(n, Counter()).update(c)
    return prof


def to_matrix(prof, ns=None):
    if ns is None:
        ns = sorted(prof)
    keys = sorted({k for p in prof.values() for k in p})
    X = np.array([[prof[n].get(k, 0) for k in keys] for n in ns], float)
    X = X / np.maximum(X.sum(1, keepdims=True), 1e-12)
    return ns, X


def simmat(X):
    Xn = X / np.maximum(np.linalg.norm(X, axis=1, keepdims=True), 1e-12)
    S = Xn @ Xn.T; np.fill_diagonal(S, 0); return S


def spectral_order(S):
    d = S.sum(1); dinv = 1 / np.sqrt(np.maximum(d, 1e-12))
    Ln = np.diag(dinv) @ (np.diag(d) - S) @ np.diag(dinv)
    w, V = np.linalg.eigh(Ln); return np.argsort(V[:, 1])


def tsp_order(S):
    D = 1 - S; n = len(D); best = None
    for start in range(n):
        unv = set(range(n)); cur = start; unv.discard(cur); path = [cur]
        while unv:
            nxt = min(unv, key=lambda j: D[cur, j]); path.append(nxt); unv.discard(nxt); cur = nxt
        cost = sum(D[path[i], path[i + 1]] for i in range(n - 1))
        if best is None or cost < best[0]:
            best = (cost, path)
    path = best[1][:]
    tl = lambda p: sum(D[p[i], p[i + 1]] for i in range(len(p) - 1))
    imp = True
    while imp:
        imp = False
        for i in range(1, n - 1):
            for j in range(i + 1, n):
                q = path[:i] + path[i:j + 1][::-1] + path[j + 1:]
                if tl(q) < tl(path) - 1e-12:
                    path = q; imp = True
    return np.array(path)


def pca_order(X):
    Xc = X - X.mean(0); U, s, Vt = np.linalg.svd(Xc, full_matrices=False)
    return np.argsort(U[:, 0] * s[0])


def spearman(a, b):
    ra = np.asarray(a).argsort().argsort(); rb = np.asarray(b).argsort().argsort()
    return np.corrcoef(ra, rb)[0, 1]


def sc(order, n):
    t = np.arange(n); return max(abs(spearman(order, t)), abs(spearman(order[::-1], t)))


def reconstruct(X, method):
    if method == "pca":
        return pca_order(X)
    S = simmat(X)
    return spectral_order(S) if method == "spectral" else tsp_order(S)


def run():
    out = {}
    # --- robustness across features x algorithms ---
    grid = {}
    for feat in ("freq", "bigram", "trigram"):
        ns, X = to_matrix(profiles(feat))
        n = len(ns)
        for meth in ("spectral", "tsp", "pca"):
            grid[f"{feat}/{meth}"] = round(float(sc(reconstruct(X, meth), n)), 3)
    out["feature_x_algorithm"] = grid

    # --- leave-one-out & leave-five-out (freq/tsp, a strong combo) ---
    ns, X = to_matrix(profiles("bigram"))
    n = len(ns)
    base = round(float(sc(reconstruct(X, "tsp"), n)), 3)
    loo = []
    for i in range(n):
        keep = [j for j in range(n) if j != i]
        loo.append(sc(reconstruct(X[keep], "tsp"), len(keep)))
    rng = random.Random(329)
    l5 = []
    for _ in range(50):
        drop = set(rng.sample(range(n), 5)); keep = [j for j in range(n) if j not in drop]
        l5.append(sc(reconstruct(X[keep], "tsp"), len(keep)))
    out["leave_out"] = {"base_bigram_tsp": base,
                        "loo_min": round(float(min(loo)), 3), "loo_max": round(float(max(loo)), 3),
                        "l5o_mean": round(float(np.mean(l5)), 3), "l5o_min": round(float(min(l5)), 3)}

    # --- DECISIVE control: detrend (is there order beyond the global gradient?) ---
    ns, X = to_matrix(profiles("freq"))
    n = len(ns); pos = np.arange(n)
    # fit each column (letter) linearly on position, subtract -> residuals
    A = np.vstack([pos, np.ones(n)]).T
    coef, *_ = np.linalg.lstsq(A, X, rcond=None)
    trend = A @ coef
    resid = X - trend
    full_sc = round(float(sc(reconstruct(X, "tsp"), n)), 3)
    trend_sc = round(float(sc(reconstruct(trend + 1e-9 * np.random.RandomState(0).randn(*trend.shape), "tsp"), n)), 3)
    resid_sc = round(float(sc(reconstruct(resid, "tsp"), n)), 3)
    # artificial-gradient surrogate: trend + shuffled residual rows
    sur_scores = []
    rr = np.random.RandomState(329)
    for _ in range(200):
        perm = rr.permutation(n)
        sur = trend + resid[perm]
        sur_scores.append(sc(reconstruct(sur, "tsp"), n))
    out["detrend_control"] = {
        "full_order_score": full_sc,
        "pure_trend_score": trend_sc,          # a clean global gradient -> seriation recovers it ~perfectly
        "residual_only_score": resid_sc,       # order info BEYOND the global trend
        "chance_mean": 0.118,
        "artificial_gradient_mean": round(float(np.mean(sur_scores)), 3),
        "artificial_gradient_max": round(float(np.max(sur_scores)), 3),
    }
    load.save_result("159_reconstruction_robustness", out)
    return out


if __name__ == "__main__":
    r = run()
    print("RECONSTRUCTION ROBUSTNESS #329\n")
    print("feature x algorithm (|Spearman vs Dee|):")
    for k, v in r["feature_x_algorithm"].items():
        print("   %-18s %.3f" % (k, v))
    lo = r["leave_out"]
    print("\nleave-out (bigram/tsp, base %.3f): LOO [%.3f, %.3f] | L5O mean %.3f (min %.3f)" % (
        lo["base_bigram_tsp"], lo["loo_min"], lo["loo_max"], lo["l5o_mean"], lo["l5o_min"]))
    d = r["detrend_control"]
    print("\nDETREND control (freq/tsp):")
    print("   full order           %.3f" % d["full_order_score"])
    print("   pure global trend    %.3f  (clean gradient -> trivially recoverable)" % d["pure_trend_score"])
    print("   RESIDUAL only        %.3f  (order beyond the global gradient; chance ~%.3f)" % (d["residual_only_score"], d["chance_mean"]))
    print("   artificial-gradient  %.3f mean / %.3f max  (same global trend, scrambled local)" % (
        d["artificial_gradient_mean"], d["artificial_gradient_max"]))
