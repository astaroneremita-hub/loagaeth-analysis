"""
35 - Nalvage's coordinates (13-14 April 1584): are the letters of the first Call located in the
     tables of the Loagaeth?

When the first Call was dictated (backwards, words 86 -> 68), each letter came with a reference such
as "In the thirteenth Table, 7003, is I" or "The 30th Table, 13025, from the low angle on the left
side ... ascending" (A True & Faithful Relation, pp. 78-83). Laycock called the numbers inexplicable
(many exceed 2,401 = 49 x 49); no fit has been published. TUPLES below are the references that give a
letter, a table and a number.

Test, fixed in advance: for every tuple look up the cell of the stated table at the stated count
under a family of 48 plain indexings - row-major / column-major, from the top or bottom, from the
left or right, the count taken modulo the table size; "ascending"/"descending" either ignored or
used to choose bottom-up / top-down; side a, side b, or a then b; tables in Dee's order or counted
from the end ("the first leaf is the last"). Hit = the cell holds the stated letter (U = V, I = J = Y).
Null: the same tuples with their letters permuted (2,000 times), taking the BEST of the 48 schemes
each time - a family-wise p-value.

Also: do the numbers simply rise with the table number? (Spearman.)
"""
import json
import random
import statistics

import load
from a15_book_geometry import rebuild

T = [  # (letter, table, number, 'a'scending / 'd'escending / None), in the order dictated
    ("I", 13, 7003, None), ("A", 21, 11406, "d"),
    ("A", 13, 740, "a"), ("M", 30, 13025, "a"),
    ("O", 7, 99, "a"), ("C", 19, 409, "d"), ("N", 31, 5009, "d"),
    ("O", 39, 9073, "d"), ("D", 41, 27004, "a"), ("R", 43, 34006, None), ("I", 4, 72000, "a"),
    ("P", 6, 109, "a"), ("A", 9, 405, "a"), ("L", 11, 603, "d"),
    ("E", 6, 700, None), ("G", 13, 2000, "d"), ("R", 17, 11004, "d"), ("O", 32, 32000, "d"), ("Z", 47, 194000, "d"),
    ("A", 19, 17200, "d"), ("A", 24, 25000, "a"), ("Q", 24, 33000, "a"),
    ("E", 2, 112, "a"), ("C", 19, 1013, "d"), ("I", 13, 2005, "d"), ("C", 14, 2907, "d"),
    ("O", 4, 309, "a"), ("D", 5, 812, "d"), ("O", 5, 902, "d"),
    ("N", 9, 804, "d"), ("A", 11, 2005, "d"), ("R", 14, 5006, "d"), ("M", 16, 12004, "d"), ("A", 20, 17006, "d"), ("Z", 32, 40006, "d"),
    ("T", 4, 212, "d"), ("O", 6, 1907, "a"),
    ("A", 9, 500, "a"), ("C", 10, 602, "d"),
    ("R", 16, 22006, "a"), ("A", 19, 23012, "d"), ("C", 30, 30006, "a"), ("A", 39, 42012, "d"), ("Z", 46, 312004, "a"),
    ("N", 6, 309, "d"), ("A", 7, 360, "a"), ("O", 9, 1000, "a"), ("O", 13, 1050, "a"), ("U", 17, 2004, "a"),
    ("D", 5, 4, "a"), ("O", 39, 7806, "a"),
    ("L", 17, 419, "a"), ("O", 18, 2017, "a"), ("M", 24, 5069, "a"), ("A", 30, 9012, "d"), ("I", 35, 15079, "a"), ("P", 43, 159068, "d"),
    ("P", 4, 97, "a"), ("A", 6, 112, "a"), ("I", 8, 207, "a"), ("P", 9, 307, "a"),
]
EQ = {"V": "U", "J": "I", "Y": "I", "K": "C"}


def fold(c):
    return EQ.get(c, c)


def grids():
    """Each side as a list of rows (as laid out on the page)."""
    lv = load.leaves()
    G = {}
    for t in range(2, 49):
        sq = rebuild(t) if t >= 29 else None
        for s in "ab":
            rows = [load.letters(r) for r in lv.get(f"{t}{s}", []) if load.letters(r)]
            if rows:
                G[(t, s)] = rows
        if sq and all(c for row in sq for c in row):
            G[(t, "sq")] = ["".join(row) for row in sq]
    return G


def seq(rows, major, vflip, hflip):
    R = rows[::-1] if vflip else rows
    R = [r[::-1] for r in R] if hflip else R
    if major == "row":
        return "".join(R)
    w = max(len(r) for r in R)
    return "".join(r[c] for c in range(w) for r in R if c < len(r))


def schemes():
    out = []
    for order in ("dee", "from_end"):
        for side in ("a", "b", "ab"):
            for major in ("row", "col"):
                for hflip in (False, True):
                    for use_dir in (False, True):
                        out.append((order, side, major, hflip, use_dir))
    return out


def lookup(G, cache, sch, t, n, d):
    order, side, major, hflip, use_dir = sch
    tt = t if order == "dee" else 50 - t
    vflip = use_dir and d == "a"
    key = (tt, side, major, hflip, vflip)
    if key not in cache:
        parts = []
        for s in (("a", "b") if side == "ab" else (side,)):
            rows = G.get((tt, s))
            if rows:
                parts.append(seq(rows, major, vflip, hflip))
        cache[key] = "".join(parts)
    s = cache[key]
    return fold(s[(n - 1) % len(s)]) if s else None


def run():
    rng = random.Random(35)
    G = grids()
    S = schemes()
    cache = {}
    cells = [[lookup(G, cache, sch, t, n, d) for (_, t, n, d) in T] for sch in S]
    letters = [fold(L) for L, *_ in T]

    def hits(perm):
        return [sum(1 for c, L in zip(row, perm) if c == L) for row in cells]
    obs = hits(letters)
    best = max(obs)
    nul_best, nul_all = [], []
    for _ in range(2000):
        p = letters[:]
        rng.shuffle(p)
        h = hits(p)
        nul_best.append(max(h))
        nul_all.append(statistics.mean(h))
    top = sorted(zip(obs, S), key=lambda x: -x[0])[:5]
    # do numbers rise with the table?
    xs, ys = [t for _, t, n, _ in T], [n for _, t, n, _ in T]

    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for i, k in enumerate(o):
            r[k] = i
        return r
    ra, rb = rank(xs), rank(ys)
    n = len(T)
    rho = 1 - 6 * sum((a - b) ** 2 for a, b in zip(ra, rb)) / (n * (n * n - 1))
    ends = sum(1 for _, _, v, _ in T if v >= 1000 and (v % 1000) < 100)
    big = sum(1 for _, _, v, _ in T if v >= 1000)
    res = {"tuples": n, "schemes_tried": len(S),
           "hits_best_scheme": best, "hits_mean_over_schemes": round(statistics.mean(obs), 2),
           "null_best_of_schemes_mean": round(statistics.mean(nul_best), 2),
           "null_best_95th": sorted(nul_best)[1899],
           "family_wise_p": round((sum(v >= best for v in nul_best) + 1) / 2001, 4),
           "null_mean_hits_per_scheme": round(statistics.mean(nul_all), 2),
           "top_schemes": [{"hits": h, "order": s[0], "side": s[1], "major": s[2], "right_to_left": s[3], "uses_direction": s[4]} for h, s in top],
           "number_rises_with_table_spearman": round(rho, 2),
           "numbers_over_1000_with_small_tail": f"{ends} of {big} (tail < 100 after the thousands)",
           "exceed_one_table_2401": sum(1 for _, _, v, _ in T if v > 2401),
           "exceed_whole_book_235298": sum(1 for _, _, v, _ in T if v > 98 * 2401)}
    load.save_result("35_nalvage_coordinates", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
