"""
157 - ROBUSTNESS AUDIT of the Loagaeth sequential gradient (#317), user protocol #327. FROZEN.

Independent of the name-grammar question. Statistic: Mantel correlation between leaf index-distance |i-j|
and letter-profile cosine-DISTANCE (1-cos), over all leaf pairs, in Dee's order. Real #317 ~ +0.5
(far leaves are more dissimilar). Higher = stronger sequential organization.

PRE-REGISTERED (frozen before running; groups chosen by principle, NOT from results):
  T1 Permutation : 100,000 random relabelings of the leaf->index assignment (Mantel null).
  T2 Leave-one-out : drop each leaf once; report min/max Mantel r -> does one leaf dominate?
  T3 Pre-defined partitions (fixed in advance):
       P1 vowels-only profiles  {A,E,I,O,U}
       P2 consonants-only profiles
       P3 first half of the book only (leaves <= median index)
       P4 second half only (leaves > median index)
     -> gradient must survive on BOTH letter classes and BOTH halves to be structural, not localized.
  T4 Autocorrelation / distance decay : mean similarity by index-distance bin -> monotonic across ALL
     distances (global), not only distance-1 (local continuity)?
  Multiple-comparison: Bonferroni over the T3 partition tests (4) + the lag test.
Statistical trend only; cosmological reading (seed/body/dissolution) is NOT tested here.
"""
import hashlib
import json
import math
import random
import statistics
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum

V = set("AEIOU")


def leaf_profiles(letter_filter=None):
    book = base_book()
    prof = {}
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if not g:
            continue
        n = tnum(k)
        ch = [c for row in g for c in row if c.isalpha() and (letter_filter is None or c in letter_filter)]
        if ch:
            prof.setdefault(n, Counter()).update(ch)
    return prof


def cos(a, b):
    ks = set(a) | set(b)
    d = sum(a.get(k, 0) * b.get(k, 0) for k in ks)
    na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return d / (na * nb) if na and nb else 0.0


def pearson(xs, ys):
    mx = statistics.mean(xs); my = statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    sx = math.sqrt(sum((x - mx) ** 2 for x in xs)); sy = math.sqrt(sum((y - my) ** 2 for y in ys))
    return cov / (sx * sy) if sx and sy else 0.0


def mantel_pairs(ns, prof):
    """return (index_dist list, profile_dist list) over all pairs, in given order ns."""
    idx = {n: i for i, n in enumerate(ns)}
    D = {}
    for a in range(len(ns)):
        for b in range(a + 1, len(ns)):
            D[(a, b)] = 1 - cos(prof[ns[a]], prof[ns[b]])
    I = [abs(a - b) for a in range(len(ns)) for b in range(a + 1, len(ns))]
    Dl = [D[(a, b)] for a in range(len(ns)) for b in range(a + 1, len(ns))]
    return I, Dl, D


def mantel_r(ns, prof):
    I, Dl, _ = mantel_pairs(ns, prof)
    return pearson(I, Dl)


def run(perm_n=100000):
    prof = leaf_profiles()
    ns = sorted(prof)
    frozen = {"n_leaves": len(ns), "hash": hashlib.sha256(json.dumps(ns).encode()).hexdigest()[:12],
              "statistic": "Mantel r(|i-j|, 1-cos profile)", "perm_n": perm_n}
    realr = mantel_r(ns, prof)

    # T1 permutation (Mantel): fix profile-distance matrix, permute index assignment
    # precompute profile-distance by leaf-pair
    pdist = {}
    for a in range(len(ns)):
        for b in range(a + 1, len(ns)):
            pdist[(ns[a], ns[b])] = 1 - cos(prof[ns[a]], prof[ns[b]])
            pdist[(ns[b], ns[a])] = pdist[(ns[a], ns[b])]
    base_I = [abs(a - b) for a in range(len(ns)) for b in range(a + 1, len(ns))]
    mI = statistics.mean(base_I); sI = math.sqrt(sum((x - mI) ** 2 for x in base_I))
    rng = random.Random(327)
    ge = 0
    for _ in range(perm_n):
        perm = ns[:]; rng.shuffle(perm)
        Dl = []
        for a in range(len(perm)):
            pa = perm[a]
            for b in range(a + 1, len(perm)):
                Dl.append(pdist[(pa, perm[b])])
        mD = statistics.mean(Dl)
        cov = sum((base_I[i] - mI) * (Dl[i] - mD) for i in range(len(Dl)))
        sD = math.sqrt(sum((d - mD) ** 2 for d in Dl))
        r = cov / (sI * sD) if sI and sD else 0
        if r >= realr:
            ge += 1
    p_perm = (ge + 1) / (perm_n + 1)

    # T2 leave-one-out
    loo = []
    for drop in ns:
        sub = [n for n in ns if n != drop]
        loo.append(mantel_r(sub, prof))
    loo_min, loo_max = min(loo), max(loo)

    # T3 pre-defined partitions
    pv = leaf_profiles(V); pc = leaf_profiles(set("BCDFGHKLMNPQRSTXYZ"))
    nv = sorted(pv); nc = sorted(pc)
    med = ns[len(ns) // 2]
    first = [n for n in ns if n <= med]; second = [n for n in ns if n > med]
    partitions = {
        "vowels_only": mantel_r(nv, pv) if len(nv) > 5 else None,
        "consonants_only": mantel_r(nc, pc) if len(nc) > 5 else None,
        "first_half": mantel_r(first, prof) if len(first) > 5 else None,
        "second_half": mantel_r(second, prof) if len(second) > 5 else None,
    }

    # T4 distance-decay bins
    I, Dl, _ = mantel_pairs(ns, prof)
    bins = {}
    for d, dd in zip(I, Dl):
        bins.setdefault(min(d // 8, 5), []).append(1 - dd)  # similarity
    decay = {f"{b*8}-{b*8+7}": round(statistics.mean(v), 4) for b, v in sorted(bins.items())}

    res = {"frozen": frozen, "real_mantel_r": round(realr, 4), "perm_p": round(p_perm, 6),
           "leave_one_out": {"min_r": round(loo_min, 4), "max_r": round(loo_max, 4), "n": len(loo)},
           "partitions": {k: (round(v, 4) if v is not None else None) for k, v in partitions.items()},
           "distance_decay_similarity": decay,
           "bonferroni_alpha": round(0.05 / 5, 4)}
    load.save_result("157_gradient_audit", res)
    return res


if __name__ == "__main__":
    import sys
    pn = int(sys.argv[1]) if len(sys.argv) > 1 else 100000
    r = run(pn)
    print("GRADIENT ROBUSTNESS AUDIT #327 (FROZEN)\n")
    print("hash", r["frozen"]["hash"], "| leaves", r["frozen"]["n_leaves"])
    print("real Mantel r(dist, dissimilarity) = %.4f" % r["real_mantel_r"])
    print("T1 permutation (%d shuffles): p = %.2g" % (r["frozen"]["perm_n"], r["perm_p"]))
    print("T2 leave-one-out: r ranges [%.4f, %.4f] over %d drops" % (
        r["leave_one_out"]["min_r"], r["leave_one_out"]["max_r"], r["leave_one_out"]["n"]))
    print("T3 pre-defined partitions (Bonferroni alpha %.4f):" % r["bonferroni_alpha"])
    for k, v in r["partitions"].items():
        print("     %-16s r = %s" % (k, v))
    print("T4 distance-decay (similarity by |i-j| bin):", r["distance_decay_similarity"])
