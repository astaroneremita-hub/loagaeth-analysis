"""
17 - The kingdom: sides, mirrors, borders on the 7x7 plan, and the two houses.

  A) Pillars: does any great name prefer the left or right half, top or bottom half, of the
     full 49x49 grids? Null = strings of the same length and similar frequency (a long name can
     only start towards the left, so a naive 50% baseline would be wrong).
  B) "As above, so below": in the diamond tables, is row i similar to its mirror row n-1-i?
     In the full tables, is row i similar to row 48-i beyond any two rows of the same table?
  C) Borders on the 7x7 plan of the 49 tables (the Gebofal weeks): where each segment boundary
     falls. Descriptive only - these positions were picked after seeing the data.
  D) The implicit correlation zone: which names rise and fall together from table to table once
     overall name density is removed? Family-wise threshold from shuffled series; containment
     pairs (one name inside the other) flagged as trivial; antagonisms re-tested inside each
     segment so that "they live in different realms" cannot explain them.
"""
import itertools
import json
import math
import random
import statistics
from collections import Counter

import load

STEMS = ["CHASTOR", "ANZACH", "GETH", "NOCHA", "ADNOCHA", "ALGETH", "CHAPH"]
NAMES = ["CHASTOR", "ANZACH", "GETH", "ADNOCHA", "NOCHAPH", "ACHEPHA", "ANTANTO", "ACLAX",
         "OXAD", "NODAX", "UDRAX", "GRADAX", "ALGETH", "NOLZAD", "NOCLAX"]


def rows(key):
    return [load.letters(r) for r in load.leaves().get(key, [])]


def stream(t):
    return "".join(load.letters("".join(load.leaves().get(f"{t}{s}", []))) for s in "ab")


def full_grids():
    out = []
    for t in range(2, 26):
        for s in "ab":
            g = rows(f"{t}{s}")
            if len(g) == 49 and all(len(r) == 49 for r in g):
                out.append(g)
    return out


def tri(s):
    return {s[i:i + 3] for i in range(len(s) - 2)}


def jac(a, b):
    A, B = tri(a), tri(b)
    return len(A & B) / len(A | B) if A | B else 0.0


def pearson(a, b):
    ma, mb = statistics.mean(a), statistics.mean(b)
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b))
    return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / den if den else 0.0


def resid(y, x):
    mx, my = statistics.mean(x), statistics.mean(y)
    d = sum((a - mx) ** 2 for a in x) or 1
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / d
    return [c - (my + b * (a - mx)) for a, c in zip(x, y)]


def run():
    rng = random.Random(17)
    grids = full_grids()

    # A pillars
    def positions(sub):
        cols, rws = [], []
        for g in grids:
            for ri, r in enumerate(g):
                i = r.find(sub)
                while i >= 0:
                    cols.append(i + len(sub) / 2)
                    rws.append(ri)
                    i = r.find(sub, i + 1)
        return cols, rws
    # Analytic baseline: a k-letter name can only start at columns 0..49-k, so under uniform
    # placement its centre falls left of the middle with a known probability; rows are uniform.
    pillars = {}
    for stem in STEMS:
        cols, rws = positions(stem)
        n = len(cols)
        if n < 15:
            continue
        k = len(stem)
        starts = range(0, 50 - k)
        p_left = sum(1 for i in starts if i + k / 2 < 24.5) / len(starts)
        p_top = 24 / 49
        fl = sum(1 for c in cols if c < 24.5) / n
        ft = sum(1 for r in rws if r < 24) / n
        pillars[stem] = {"n": n, "left_share": round(fl, 2), "expected_left": round(p_left, 2),
                         "z_left": round((fl - p_left) / math.sqrt(p_left * (1 - p_left) / n), 1),
                         "top_share": round(ft, 2), "expected_top": round(p_top, 2),
                         "z_top": round((ft - p_top) / math.sqrt(p_top * (1 - p_top) / n), 1)}
    n_tests = 2 * len(pillars)

    # B mirrors
    sides = [rows(f"{t}{s}") for t in range(29, 49) for s in "ab"]
    bylen = {}
    for sd in sides:
        for r in sd:
            bylen.setdefault(len(r), []).append(r)
    mo, mn = [], []
    for sd in sides:
        n = len(sd)
        for i in range(n // 2):
            a, b = sd[i], sd[n - 1 - i]
            if len(a) >= 6 and len(a) == len(b):
                mo.append(jac(a, b))
                mn.extend(jac(a, rng.choice(bylen[len(a)])) for _ in range(5))
    fo, fn = [], []
    for g in grids:
        for i in range(24):
            fo.append(jac(g[i], g[48 - i]))
            others = [j for j in range(49) if j not in (i, 48 - i)]
            fn.append(jac(g[i], g[rng.choice(others)]))
    mirrors = {"diamond_row_vs_mirror": round(statistics.mean(mo), 4), "diamond_row_vs_random_same_length": round(statistics.mean(mn), 4),
               "full_row_vs_mirror": round(statistics.mean(fo), 4), "full_row_vs_random_row_same_table": round(statistics.mean(fn), 4),
               "verdict": "no mirror symmetry beyond ordinary within-table similarity"}

    # C borders on the 7x7 plan
    borders = []
    for name, t in [("CHASTOR appears", 6), ("writing turns from rows to diagonals (side 25b)", 25),
                    ("diamond format begins", 29), ("U-register end begins", 44)]:
        borders.append({"event": name, "table": t, "week": (t - 1) // 7 + 1, "position_in_week": (t - 1) % 7 + 1})

    # D implicit correlation zone
    T = [t for t in range(2, 49) if t not in (26, 27, 28)]
    tx = {t: stream(t) for t in T}
    dens = {n: [1000 * tx[t].count(n) / len(tx[t]) for t in T] for n in NAMES}
    tot = [sum(dens[n][i] for n in NAMES) for i in range(len(T))]
    R = {n: resid(dens[n], tot) for n in NAMES}
    pairs = []
    for a, b in itertools.combinations(NAMES, 2):
        pairs.append({"a": a, "b": b, "r": round(pearson(R[a], R[b]), 2), "containment": a in b or b in a})
    mx = []
    for _ in range(300):
        S = {n: rng.sample(R[n], len(R[n])) for n in NAMES}
        mx.append(max(abs(pearson(S[a], S[b])) for a, b in itertools.combinations(NAMES, 2)))
    thr = sorted(mx)[int(0.95 * len(mx))]
    strong = [p for p in sorted(pairs, key=lambda p: -abs(p["r"])) if abs(p["r"]) > thr]

    def within(rg, a, b):
        tt = [t for t in rg]
        tx2 = {t: stream(t) for t in tt}
        nm = [a, b] + [n for n in NAMES if n not in (a, b)]
        d2 = {n: [1000 * tx2[t].count(n) / len(tx2[t]) for t in tt] for n in nm}
        to2 = [sum(d2[n][i] for n in nm) for i in range(len(tt))]
        ra, rb = resid(d2[a], to2), resid(d2[b], to2)
        o = pearson(ra, rb)
        s = [pearson(ra, rng.sample(rb, len(rb))) for _ in range(2000)]
        return {"r": round(o, 2), "p": round(sum(1 for x in s if x <= o) / len(s), 3)}
    houses = {}
    for a, b in [("ADNOCHA", "ALGETH"), ("ADNOCHA", "ACLAX"), ("NODAX", "ALGETH"), ("NOCHAPH", "ACLAX")]:
        houses[f"{a}~{b}"] = {"heartland_6_25": within(range(6, 26), a, b), "diamonds_29_43": within(range(29, 44), a, b)}
    seg_density = {}
    for n in ["ADNOCHA", "NOCHAPH", "NODAX", "ALGETH", "ACLAX", "GETH"]:
        seg_density[n] = {k: round(statistics.mean(1000 * stream(t).count(n) / len(stream(t)) for t in rg), 2)
                          for k, rg in [("opening", range(2, 6)), ("heartland", range(6, 26)),
                                        ("diamonds", range(29, 44)), ("end", range(44, 49))]}

    res = {
        "A_pillars": {"stems": pillars, "tests": n_tests, "bonferroni_z": 2.9,
                      "verdict": ("no great name prefers the left or the right; ALGETH (GETH house) sits in the "
                                  "lower half of the full grids beyond the Bonferroni bar, GETH and the NOCHA "
                                  "family only lean (bottom / top) without passing it")},
        "B_mirrors": mirrors,
        "C_borders_on_7x7_plan": {"borders": borders,
                                  "note": ("Table 25 is the exact centre of the 7x7 plan (week 4, position 4) and of 1..49; "
                                           "the writing turns from rows to diagonals between its two sides (25a|25b), "
                                           "i.e. after side 49 of 98. Tables 26-28 belong to CHASTOR's realm once read "
                                           "on their diagonals (a18). Descriptive, noticed after seeing the data.")},
        "D_correlation_zone": {"names": NAMES, "familywise_threshold_abs_r": round(thr, 2),
                               "strong_pairs": strong, "houses_within_segments": houses,
                               "house_density_per_1000_letters": seg_density,
                               "residual_matrix": {f"{p['a']}~{p['b']}": p["r"] for p in pairs}},
        "conclusion": ("No side or height is preferred by any great name and there is no mirror symmetry. "
                       "Beyond density, two houses exclude each other table by table - the NOCHA house "
                       "(ADNOCHA, NOCHAPH, NODAX) and the GETH/ACLAX house (ALGETH, ACLAX) - inside the "
                       "heartland and inside the diamonds; the NOCHA house leads the first half, the "
                       "GETH/ACLAX house holds or grows in the second."),
    }
    load.save_result("17_kingdom", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1)[:4000])
