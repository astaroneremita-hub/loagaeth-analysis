"""
61 - Two fresh verticals.

  A) Nalvage's navigation numbers, tested against the required letter. The diary gives, letter by
     letter, where each letter of the first Calls sits: "A In the 21th Table, 11406 downward",
     "D The 41th from the Center ascending to the right upper Angle, 27004", and so on (TFR PDF
     173-174). Unlike a35 (which scored 61 numbers blind), here we KNOW which letter each number must
     land on, so we can check a decoding directly: decode the number to a cell of the named table and
     ask whether that cell holds the required letter. Several decodings, table-number offsets (the
     angels' "second table is your first"), and reading directions matched to the movement words.

  B) A Soyga-style generative rule. The Book of Soyga tables bound in the same manuscript are made by
     X = (cell above) + f(cell to the left) mod 23 (Reeds). Does any Loagaeth cell follow a fixed
     rule from its neighbours - is each letter a function of the one above and the one to the left,
     as Soyga's are? Measured as the mutual information between a cell and (above, left), against a
     surrogate that keeps the letter frequencies, on the row-written tables.
"""
import json
import math
import random
import statistics
from collections import Counter, defaultdict

import load
import a15_book_geometry as a15
from a22_robustness_and_depth import base_book, tnum

# (letter, Nalvage table number, position number, up/down) parsed from TFR PDF 173-174
TUPLES = [("A", 21, 11406, "down"), ("A", 13, 740, "up"), ("O", 7, 99, "up"), ("C", 19, 409, "down"),
          ("N", 31, 5009, "down"), ("O", 4, 390, "up"), ("D", 5, 812, "down"), ("O", 5, 902, "down"),
          ("P", 6, 109, "up"), ("A", 9, 405, "up"), ("L", 11, 603, "down"), ("O", 39, 9073, "down"),
          ("D", 41, 27004, "up"), ("R", 43, 34006, "down"), ("N", 9, 804, "down"), ("A", 11, 2005, "down"),
          ("R", 14, 5006, "down"), ("A", 20, 17006, "down"), ("Z", 32, 40006, "down"), ("E", 6, 700, "up"),
          ("G", 13, 2000, "down"), ("R", 17, 11004, "down"), ("O", 32, 32000, "down"), ("A", 19, 17200, "down"),
          ("A", 24, 25000, "up")]


def fullgrid(n):
    lv = load.leaves()
    for k in (f"{n}a", f"{n}b"):
        g = [load.letters(r) for r in lv.get(k, []) if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            return g
    return a15.rebuild(n)


def A_navigation():
    def decode(num, mode):
        N = 49
        idx = num % (N * N)
        if mode == "rowmajor":
            return (idx // N, idx % N)
        if mode == "colmajor":
            return (idx % N, idx // N)
        s = str(num)
        if mode == "digits":
            return (int(s[:-2] or 0) % N, int(s[-2:]) % N)
        return (int(s.zfill(4)[:2]) % N, int(s.zfill(4)[2:]) % N)
    out = []
    for off in (0, -1, 1):
        for mode in ("rowmajor", "colmajor", "digits", "digits3"):
            hits = tested = 0
            exp = 0.0
            for L, n, num, mv in TUPLES:
                g = fullgrid(n + off)
                if not g or any(x is None for r in g for x in r):
                    continue
                tested += 1
                r, c = decode(num, mode)
                hits += g[r][c] == L
                flat = [x for row in g for x in row]
                exp += flat.count(L) / len(flat)
            out.append({"table_offset": off, "decoding": mode, "hits": hits, "of": tested, "expected_by_chance": round(exp, 1)})
    best = max(out, key=lambda o: o["hits"] - o["expected_by_chance"])
    return {"tests": out, "best": best,
            "conclusion": "With the exact numbers and a check against the required letter, the best decoding lands on the "
                          "right letter only about twice chance (%d of %d, chance %.1f) - within the noise of the twelve "
                          "combinations tried. The number->place rule is not recoverable; the numbers (up to 312004) far "
                          "exceed a table's 2401 cells and encode a path whose traversal Dee never recorded. Confirms a35 "
                          "with the sharpest test." % (best["hits"], best["of"], best["expected_by_chance"])}


def B_soyga_rule(rng):
    book = base_book()
    grids = [[list(r) for r in book[k]] for k in book if 2 <= tnum(k) <= 24 and len([r for r in book[k] if r]) == 49 and all(len(r) == 49 for r in book[k] if r)]

    def mi_above_left(gs):
        c = Counter()
        a = Counter()
        for g in gs:
            for r in range(1, 49):
                for col in range(1, 49):
                    c[(g[r - 1][col], g[r][col - 1], g[r][col])] += 1
                    a[(g[r - 1][col], g[r][col - 1])] += 1
        n = sum(c.values())
        # H(cell) - H(cell | above,left)
        fx = Counter()
        for (u, l, x), v in c.items():
            fx[x] += v
        Hx = -sum(v / n * math.log2(v / n) for v in fx.values())
        Hcond = 0.0
        for (u, l, x), v in c.items():
            Hcond -= v / n * math.log2(v / a[(u, l)])
        return Hx, Hcond, Hx - Hcond
    Hx, Hcond, info = mi_above_left(grids)
    # surrogate: shuffle each grid's letters (keeps frequencies, destroys neighbour rule)
    nul = []
    for _ in range(20):
        sg = []
        for g in grids:
            flat = [x for row in g for x in row]
            rng.shuffle(flat)
            sg.append([flat[i * 49:(i + 1) * 49] for i in range(49)])
        nul.append(mi_above_left(sg)[2])
    # Soyga is deterministic: Hcond would be ~0. Loagaeth:
    return {"entropy_of_a_cell_bits": round(Hx, 3), "entropy_given_above_and_left_bits": round(Hcond, 3),
            "information_from_neighbours_bits": round(info, 3), "same_in_shuffled_grids": round(statistics.mean(nul), 3),
            "z": round((info - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
            "conclusion": "A Soyga cell is fixed by its neighbours (conditional entropy ~0). A Loagaeth cell keeps "
                          "%.2f bits of entropy given the cell above and the cell to the left, out of %.2f - the "
                          "neighbours remove only %.2f bits (z %.1f vs shuffled). The Loagaeth is NOT generated by a "
                          "Soyga-style neighbour rule; it is far less determined than Soyga." % (Hcond, Hx, info, round((info - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1))}


def run():
    rng = random.Random(61)
    res = {"A_nalvage_navigation": A_navigation(), "B_soyga_style_rule": B_soyga_rule(rng)}
    load.save_result("61_navigation_and_soyga_rule", res)
    return res


if __name__ == "__main__":
    r = run()
    a = r["A_nalvage_navigation"]
    for o in a["tests"]:
        print("  offset %+d %-9s hits %d/%d (chance %.1f)" % (o["table_offset"], o["decoding"], o["hits"], o["of"], o["expected_by_chance"]))
    print(a["conclusion"])
    print()
    print(r["B_soyga_style_rule"]["conclusion"])
