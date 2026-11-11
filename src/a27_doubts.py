"""
27 - Track A of the roadmap: closing the remaining doubts about the data.

  A3) Where are the segment borders, if we do not assume them? Each side (2a-48b, 25b-28b read on
      their decoded currents) becomes a profile vector (21 letter shares + shares of the 150 most
      common trigrams). The book order is cut into k contiguous blocks by exact dynamic programming
      (least within-block squared distance), k = 2..8. Each k is compared with the same cut of
      shuffled side orders; the number of blocks is chosen where the gain over the null stops.
  A2) The irregular rows. Sides 2a-25a should be 49 rows of 49 letters. For every side that is not,
      list the irregular rows and test the simplest explanation: a letter carried across a row break
      (a 50-letter row next to a 48-letter row, total 98).
  A1) The U/A doubt needs the manuscript images. The transcription page carries photographs of
      some leaf titles only (no table images); recorded here, with what can and cannot be checked.
"""
import json
import math
import random
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum

OURS = {"opening|heartland": "5b|6a", "heartland|26-28": "25b|26a", "26-28|diamonds": "28b|29a",
        "diamonds|end": "43b|44a"}


def profiles(book, keys):
    tri = Counter()
    for k in keys:
        for r in book[k]:
            tri.update(r[i:i + 3] for i in range(len(r) - 2))
    top = [g for g, _ in tri.most_common(150)]
    letters = sorted({c for k in keys for r in book[k] for c in r})
    vec = []
    for k in keys:
        c = Counter(ch for r in book[k] for ch in r)
        t = Counter(g for r in book[k] for g in (r[i:i + 3] for i in range(len(r) - 2)))
        n, m = sum(c.values()), max(1, sum(t.values()))
        vec.append([c[L] / n for L in letters] + [t[g] / m * 3 for g in top])
    return vec


def seg_cost(X):
    n, d = len(X), len(X[0])
    # prefix sums for O(1) block cost
    S = [[0.0] * d for _ in range(n + 1)]
    Q = [0.0] * (n + 1)
    for i in range(n):
        for j in range(d):
            S[i + 1][j] = S[i][j] + X[i][j]
        Q[i + 1] = Q[i] + sum(v * v for v in X[i])

    def cost(a, b):  # block a..b-1
        m = b - a
        return Q[b] - Q[a] - sum((S[b][j] - S[a][j]) ** 2 for j in range(d)) / m
    return cost


def best_partition(X, K):
    n = len(X)
    cost = seg_cost(X)
    C = [[0.0] * (n + 1) for _ in range(n + 1)]
    for a in range(n):
        for b in range(a + 1, n + 1):
            C[a][b] = cost(a, b)
    out = {}
    D = [[math.inf] * (n + 1) for _ in range(K + 1)]
    B = [[0] * (n + 1) for _ in range(K + 1)]
    D[0][0] = 0
    for k in range(1, K + 1):
        for b in range(1, n + 1):
            for a in range(k - 1, b):
                v = D[k - 1][a] + C[a][b]
                if v < D[k][b]:
                    D[k][b], B[k][b] = v, a
        cuts, b = [], n
        for kk in range(k, 0, -1):
            a = B[kk][b]
            if a > 0:
                cuts.append(a)
            b = a
        out[k] = (D[k][n], sorted(cuts))
    return out


def A3_borders(book, rng):
    keys = sorted(book, key=lambda k: (tnum(k), k[-1]))
    X = profiles(book, keys)
    K = 8
    obs = best_partition(X, K)
    total = obs[1][0]
    nul = {k: [] for k in range(2, K + 1)}
    for _ in range(20):
        Y = X[:]
        rng.shuffle(Y)
        p = best_partition(Y, K)
        for k in range(2, K + 1):
            nul[k].append(1 - p[k][0] / p[1][0])
    rows = []
    for k in range(2, K + 1):
        expl = 1 - obs[k][0] / total
        rows.append({"blocks": k, "variance_explained": round(expl, 3),
                     "shuffled_order_mean": round(sum(nul[k]) / len(nul[k]), 3),
                     "borders": [f"{keys[c-1]}|{keys[c]}" for c in obs[k][1]]})
    # marginal gain of each extra block, observed minus null
    for i in range(1, len(rows)):
        rows[i]["extra_gain"] = round((rows[i]["variance_explained"] - rows[i - 1]["variance_explained"])
                                      - (rows[i]["shuffled_order_mean"] - rows[i - 1]["shuffled_order_mean"]), 3)
    return {"sides": len(keys), "by_blocks": rows, "our_borders": OURS}


def A2_irregular(book):
    lv = load.leaves()
    out = []
    for t in range(2, 26):
        for s in "ab":
            k = f"{t}{s}"
            if k == "25b" or k not in lv:
                continue
            rows = [load.letters(r) for r in lv[k] if load.letters(r)]
            L = [len(r) for r in rows]
            if len(rows) == 49 and all(x == 49 for x in L):
                continue
            odd = [(i + 1, x) for i, x in enumerate(L) if x != 49]
            carried = sum(1 for i in range(len(L) - 1) if L[i] + L[i + 1] == 98 and L[i] != 49)
            out.append({"side": k, "rows": len(rows), "letters": sum(L), "irregular_rows": odd[:12],
                        "pairs_50_48": carried,
                        "missing_or_extra_letters": sum(L) - 2401})
    return out


NEW_PARTS = {"I 2a-12b": (("2a", "12b")), "II 13a-25a": ("13a", "25a"), "III 25b-33a": ("25b", "33a"),
             "IV 33b-40b": ("33b", "40b"), "V 41a-48b": ("41a", "48b")}


def A3_stability(book):
    keys = sorted(book, key=lambda k: (tnum(k), k[-1]))
    X = profiles(book, keys)
    out = {}
    for lab, sl in (("letters_only", slice(0, 22)), ("trigrams_only", slice(22, None))):
        p = best_partition([x[sl] for x in X], 5)
        out[lab] = {k: [f"{keys[c-1]}|{keys[c]}" for c in p[k][1]] for k in (3, 4, 5)}
    return out


def A3_retest(book):
    """Re-run two segment-based results on the data-driven parts."""
    from a19_machine import CharLM
    keys = sorted(book, key=lambda k: (tnum(k), k[-1]))
    idx = {k: i for i, k in enumerate(keys)}
    parts = {lab: [k for k in keys if idx[a] <= idx[k] <= idx[b]] for lab, (a, b) in NEW_PARTS.items()}
    rng = random.Random(7)
    tr, te = {}, {}
    for lab, ks in parts.items():
        L = [r for k in ks for r in book[k]]
        rng.shuffle(L)
        tr[lab], te[lab] = L[:len(L) // 2], L[len(L) // 2:]
    M = {}
    for lab in parts:
        m = CharLM(3)
        m.fit(tr[lab])
        M[lab] = {o: round(m.bits(te[o]), 2) for o in parts}

    def grams(ks):
        c = Counter()
        for k in ks:
            for r in book[k]:
                c.update(r[i:i + 5] for i in range(len(r) - 4))
        return c
    end, heart = grams(parts["V 41a-48b"]), grams(parts["II 13a-25a"] + parts["I 2a-12b"])
    rec = [g for g, c in end.items() if c >= 3]
    hs = {g for g, c in heart.items() if c >= 3}
    swaps = {}
    for a, b in (("as_is", None), ("U->A", ("U", "A")), ("U->E", ("U", "E")), ("U->O", ("U", "O")), ("U->I", ("U", "I"))):
        swaps[a] = sum((g if not b else g.replace(*b)) in hs for g in rec)
    return {"parts": {k: len(v) for k, v in parts.items()}, "dialects": M, "u_register_part_V": swaps}


def run():
    rng = random.Random(27)
    book = base_book()
    res = {"A3_segment_borders": A3_borders(book, rng),
           "A3_stability_by_feature": A3_stability(book),
           "A3_retest_on_new_parts": A3_retest(book),
           "A2_irregular_rows": A2_irregular(book),
           "A1_images": "The transcription page shows photographs of 14 leaf titles (e.g. 5b "
                        "ZVCHASTORS) and no table images; the British Library record of Sloane 3189 "
                        "is linked but no digitised table images are available to us. The U/A check "
                        "of tables 43-48 stays open (needs the manuscript)."}
    load.save_result("27_doubts", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
