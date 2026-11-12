"""
49 - The other dimension: the leaf as an object, and how lines join.

Along its rows the book carries no memory beyond five letters (a47, a48). Two questions that do not
run along a row:

  A) The two sides of a leaf. Is side b related to side a cell by cell - the same letter in the same
     place, or in the place that shows through the paper (mirrored left-right), or turned upside
     down, half-turned, or transposed? Share of equal letters for the true pairs (table t, a and b)
     against side a paired with side b of other tables. Row-written tables 2-24, full 49 x 49 grids.

  B) Junctions. Does the text run on from one line to the next? A letter model (three letters of
     context) reads the first three letters of a line given the last three of another:
        the row below            (ordinary reading)
        the row above            (bottom to top)
        the row below, reversed  (boustrophedon: back along the next row)
        the same row on side b   (across the leaf)
     against rows paired at random inside the same side. For scale: the same three letters read
     in the middle of a row, where the text certainly runs on.
"""
import json
import math
import random
import statistics

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum

TRANSFORMS = {
    "same cell": lambda r, c: (r, c),
    "mirrored left-right (shows through the paper)": lambda r, c: (r, 48 - c),
    "upside down": lambda r, c: (48 - r, c),
    "half turn": lambda r, c: (48 - r, 48 - c),
    "transposed": lambda r, c: (c, r),
}


def grid(rows):
    g = [r for r in rows if r]
    return g if len(g) == 49 and all(len(r) == 49 for r in g) else None


def A_leaf(book, rng):
    pairs = {}
    for t in range(2, 25):
        a, b = grid(book.get(f"{t}a", [])), grid(book.get(f"{t}b", []))
        if a and b:
            pairs[t] = (a, b)
    ts = sorted(pairs)

    def ident(a, b, f):
        return sum(a[r][c] == b[f(r, c)[0]][f(r, c)[1]] for r in range(49) for c in range(49)) / 2401
    out = {"leaves_with_two_full_sides": len(ts)}
    for name, f in TRANSFORMS.items():
        M = {(i, j): ident(pairs[i][0], pairs[j][1], f) for i in ts for j in ts}
        true = statistics.mean(M[(t, t)] for t in ts)
        other = [M[(i, j)] for i in ts for j in ts if i != j]
        nul = []
        for _ in range(2000):
            sh = ts[:]
            rng.shuffle(sh)
            nul.append(statistics.mean(M[(i, j)] for i, j in zip(ts, sh)))
        out[name] = {"true_pairs": round(true, 4), "other_pairs": round(statistics.mean(other), 4),
                     "z": round((true - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
                     "p": round((sum(v >= true for v in nul) + 1) / 2001, 4)}
    return out


def B_junctions(book, rng):
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 2 <= tnum(k) <= 24]
    sides = {k: [r for r in book[k] if len(r) >= 8] for k in keys}
    m = CharLM(3, alpha=0.1).fit([r for v in sides.values() for r in v])

    def cost(ctx, nxt):
        b = 0.0
        for ch in nxt:
            b -= math.log2(m.prob(ctx, ch))
            ctx = ctx[1:] + ch
        return b
    kinds = {
        "the row below": lambda v, i: (v[i][-3:], v[i + 1][:3]) if i + 1 < len(v) else None,
        "the row above": lambda v, i: (v[i][-3:], v[i - 1][:3]) if i >= 1 else None,
        "the row below, reversed": lambda v, i: (v[i][-3:], v[i + 1][::-1][:3]) if i + 1 < len(v) else None,
    }
    out = {}
    inside = [cost(r[j - 3:j], r[j:j + 3]) for v in sides.values() for r in v for j in (20, 30)]
    out["inside a row (for scale)"] = {"bits_for_three_letters": round(statistics.mean(inside), 3)}
    for name, f in kinds.items():
        real = [cost(*f(v, i)) for v in sides.values() for i in range(len(v)) if f(v, i)]
        nul = []
        for _ in range(200):
            x = []
            for v in sides.values():
                sh = v[:]
                rng.shuffle(sh)
                x += [cost(*f(sh, i)) for i in range(len(sh)) if f(sh, i)]
            nul.append(statistics.mean(x))
        obs = statistics.mean(real)
        out[name] = {"junctions": len(real), "bits_for_three_letters": round(obs, 3), "random_rows": round(statistics.mean(nul), 3),
                     "z": round((statistics.mean(nul) - obs) / (statistics.pstdev(nul) or 1e-9), 1),
                     "p": round((sum(v <= obs for v in nul) + 1) / 201, 4)}
    # across the leaf: row i of side a -> row i of side b
    real, nul = [], [[] for _ in range(200)]
    for t in range(2, 25):
        a, b = sides.get(f"{t}a"), sides.get(f"{t}b")
        if not a or not b:
            continue
        n = min(len(a), len(b))
        real += [cost(a[i][-3:], b[i][:3]) for i in range(n)]
        for x in nul:
            sh = b[:n]
            rng.shuffle(sh)
            x += [cost(a[i][-3:], sh[i][:3]) for i in range(n)]
    obs, ns = statistics.mean(real), [statistics.mean(x) for x in nul]
    out["the same row on side b"] = {"junctions": len(real), "bits_for_three_letters": round(obs, 3), "random_rows": round(statistics.mean(ns), 3),
                                     "z": round((statistics.mean(ns) - obs) / (statistics.pstdev(ns) or 1e-9), 1),
                                     "p": round((sum(v <= obs for v in ns) + 1) / 201, 4)}
    return out


def C_line_break(book, rng):
    """What the junction is made of: the rule against doubled letters across the break, names that
    straddle it, and whether a side runs on into the next side."""
    import os
    from collections import Counter
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 2 <= tnum(k) <= 24]
    sides = {k: [r for r in book[k] if len(r) >= 8] for k in keys}
    ends = Counter(r[-1] for v in sides.values() for r in v)
    starts = Counter(r[0] for v in sides.values() for r in v)
    n = sum(len(v) - 1 for v in sides.values())
    same = sum(v[i][-1] == v[i + 1][0] for v in sides.values() for i in range(len(v) - 1))
    nul = []
    for _ in range(1000):
        t = 0
        for v in sides.values():
            sh = v[:]
            rng.shuffle(sh)
            t += sum(sh[i][-1] == sh[i + 1][0] for i in range(len(sh) - 1))
        nul.append(t)
    inside = sum(a == b for v in sides.values() for r in v for a, b in zip(r, r[1:]))
    letters = sum(len(r) - 1 for v in sides.values() for r in v)
    f = Counter(c for v in sides.values() for r in v for c in r)
    N = sum(f.values())
    d23 = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    names = sorted({x["name"] for x in d23} | {"CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"})

    def straddle(v, keep=None):
        k = 0
        for i in range(len(v) - 1):
            for nm in names:
                L = len(nm)
                a = v[i][-(L - 1):]
                j = a + v[i + 1][:L - 1]
                p = j.find(nm)
                while p >= 0:
                    if p < len(a) < p + L:
                        k += 1
                        if keep is not None:
                            keep.append((i + 1, v[i][-8:] + "/" + v[i + 1][:8], nm))
                    p = j.find(nm, p + 1)
        return k
    ex = []
    real = 0
    for k, v in sides.items():
        got = []
        real += straddle(v, got)
        ex += [(k,) + g for g in got]
    ns = []
    for _ in range(200):
        t = 0
        for v in sides.values():
            sh = v[:]
            rng.shuffle(sh)
            t += straddle(sh)
        ns.append(t)
    return {"same_letter_across_the_break": {"book": same, "rows_in_random_order": round(statistics.mean(nul), 1), "junctions": n,
                                             "z": round((same - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
                                             "p": round((sum(x <= same for x in nul) + 1) / 1001, 4)},
            "doubled_letters_inside_rows": {"book": inside, "by_letter_frequency": round(letters * sum((v / N) ** 2 for v in f.values()), 0)},
            "names_across_the_break": {"book": real, "rows_in_random_order": round(statistics.mean(ns), 1),
                                       "z": round((real - statistics.mean(ns)) / (statistics.pstdev(ns) or 1e-9), 1),
                                       "p": round((sum(x >= real for x in ns) + 1) / 201, 4),
                                       "examples": [{"side": a, "after_row": b, "break": c, "name": d} for a, b, c, d in ex[:14]]},
            "commonest_row_ends": ends.most_common(6), "commonest_row_starts": starts.most_common(6)}


def D_other_formats(book, rng):
    """The same junction test on the other formats, lines in the order they are stored (a15, a37):
    does line i run on into line i+1 ("next"), or line i+1 into line i ("previous")?"""
    groups = [("tables 2-24 (rows)", lambda k: 2 <= tnum(k) <= 24),
              ("leaves 25b-28b (chessboard diagonals)", lambda k: (tnum(k) == 25 and k.endswith("b")) or 26 <= tnum(k) <= 28),
              ("diamonds 29-40", lambda k: 29 <= tnum(k) <= 40),
              ("diamonds 41-48", lambda k: 41 <= tnum(k) <= 48)]
    out = {}
    for name, sel in groups:
        sides = [[r for r in book[k] if len(r) >= 6] for k in sorted(book, key=lambda k: (tnum(k), k)) if sel(k)]
        m = CharLM(3, alpha=0.1).fit([r for v in sides for r in v])

        def cost(ctx, nxt):
            b = 0.0
            for ch in nxt:
                b -= math.log2(m.prob(ctx, ch))
                ctx = ctx[1:] + ch
            return b
        row = {"junctions": sum(len(v) - 1 for v in sides)}
        for lab, f in (("next", lambda v, i: (v[i][-3:], v[i + 1][:3])), ("previous", lambda v, i: (v[i + 1][-3:], v[i][:3]))):
            real = statistics.mean(cost(*f(v, i)) for v in sides for i in range(len(v) - 1))
            nul = []
            for _ in range(150):
                x = []
                for v in sides:
                    sh = v[:]
                    rng.shuffle(sh)
                    x += [cost(*f(sh, i)) for i in range(len(sh) - 1)]
                nul.append(statistics.mean(x))
            row[lab] = {"bits": round(real, 2), "random_order": round(statistics.mean(nul), 2),
                        "z": round((statistics.mean(nul) - real) / (statistics.pstdev(nul) or 1e-9), 1)}
        out[name] = row
    return out


def run():
    rng = random.Random(49)
    book = base_book()
    res = {"A_two_sides_of_a_leaf": A_leaf(book, rng), "B_junctions_between_lines": B_junctions(book, rng),
           "C_what_the_line_break_is": C_line_break(book, rng), "D_junctions_in_other_formats": D_other_formats(book, rng)}
    load.save_result("49_leaf_and_junctions", res)
    return res


if __name__ == "__main__":
    for k, v in run().items():
        print(k)
        for a, b in v.items():
            print("  ", a, b)
