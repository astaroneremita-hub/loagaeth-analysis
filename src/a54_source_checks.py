"""
54 - Tests that come from reading the diaries (Sloane 3188, A True and Faithful Relation).

Until this module the study tested ideas of its own. These come from what the record says.

  A) Leaf 1 is a table of WORDS. The diary: every leaf has 49 x 49 squares; on the first leaf a
     square holds a word (1 to 12 letters), on the others a single letter ("every side conteyneth
     2400 and one od letter"). Check: does side 1 of leaf 1, as transcribed, have 49 words a row?
  B) Is leaf 1 a key to the others, square for square? ("The first leaf is the last of the Book";
     "every Element hath 49 manner of understandings".) For every side with a full 49 x 49 grid:
     does the letter in cell (row, column) agree with the word in the same square of leaf 1 - its
     first letter, its last letter, a letter it contains - or does the length of the word tell the
     letter? Squares are counted both as transcribed and from the right hand (the diary numbers the
     squares 7 6 5 4 3 2 1 from right to left). Null: rows of leaf 1 in random order.
  C) The nine rows of single letters that end side 2 of leaf 1: the first table-like text of the
     book. Are they written like the tables (bits per letter under the tables' letter model)? Do
     they hold the tables' names?
  D) The eighteenth leaf "was of the spirites of the earth" (15 April 1583) - the only leaf whose
     content the record states. Is table 18 set apart from its neighbours in letters or names?
"""
import json
import math
import os
import random
import statistics
from collections import Counter

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum

FOLD = {"V": "U", "J": "I", "Y": "I", "K": "C", "W": "U"}


def fold(s):
    return "".join(FOLD.get(c, c) for c in s)


def run():
    rng = random.Random(54)
    lv = load.leaves()
    one = [[fold(load.letters(w)) for w in r.split() if load.letters(w)] for r in lv["1a"]]
    A = {"rows": len(one), "words_per_row": [len(r) for r in one], "rows_with_exactly_49_words": sum(len(r) == 49 for r in one),
         "words": sum(len(r) for r in one), "longest_word": max(len(w) for r in one for w in r),
         "word_lengths": dict(sorted(Counter(min(len(w), 12) for r in one for w in r).items()))}

    # B
    rows49 = [i for i, r in enumerate(one) if len(r) == 49]
    grids = {}
    for k, v in lv.items():
        if k in ("1a", "1b"):
            continue
        g = [fold(load.letters(r)) for r in v if load.letters(r)]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            grids[k] = g

    def nmi(pairs):
        n = len(pairs)
        ab, a, b = Counter(pairs), Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
        return sum(v * math.log2(v * n / (a[x] * b[y])) for (x, y), v in ab.items()) / n

    def stats(g, order, mirror):
        ini = fin = has = 0
        pl = []
        for i, j in zip(rows49, order):
            for c in range(49):
                w = one[j][48 - c if mirror else c]
                ch = g[i][c]
                ini += w[0] == ch
                fin += w[-1] == ch
                has += ch in w
                pl.append((min(len(w), 10), ch))
        n = len(rows49) * 49
        return [ini / n, fin / n, has / n, nmi(pl)]
    labels = ["first letter of the word", "last letter of the word", "a letter of the word", "length of the word (bits)"]
    tests = []
    for k, g in sorted(grids.items(), key=lambda x: (tnum(x[0]), x[0])):
        for mirror in (False, True):
            real = stats(g, rows49, mirror)
            nul = []
            for _ in range(60):
                sh = rows49[:]
                rng.shuffle(sh)
                nul.append(stats(g, sh, mirror))
            for q, lab in enumerate(labels):
                xs = [n[q] for n in nul]
                tests.append({"side": k, "squares_counted": "from the right" if mirror else "as transcribed", "what": lab,
                              "book": round(real[q], 4), "rows_shuffled": round(statistics.mean(xs), 4),
                              "z": round((real[q] - statistics.mean(xs)) / (statistics.pstdev(xs) or 1e-9), 1)})
    zs = [t["z"] for t in tests]
    B = {"sides_with_a_full_grid": len(grids), "rows_of_leaf_1_used": len(rows49), "tests": len(tests),
         "mean_z": round(statistics.mean(zs), 2), "tests_with_z_above_3": sum(z > 3 for z in zs),
         "expected_above_3_by_chance": round(len(tests) * 0.00135, 1),
         "strongest": sorted(tests, key=lambda t: -t["z"])[:6],
         "by_measure": {lab: {"mean_z": round(statistics.mean(t["z"] for t in tests if t["what"] == lab), 2),
                              "max_z": max(t["z"] for t in tests if t["what"] == lab)} for lab in labels}}

    # C
    book = base_book()
    tables = [r for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if r]
    m = CharLM(3, alpha=0.1).fit(tables)
    nine = [load.letters(r) for r in lv["1b"] if len(r.split()) == 1 and len(load.letters(r)) >= 40]
    words1 = ["".join(load.letters(w) for w in r.split()) for r in lv["1a"]]
    d23 = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    names = sorted({x["name"] for x in d23} | {"CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"})
    t2 = [r for r in book.get("2a", []) if r]
    C = {"rows": len(nine), "letters": sum(map(len, nine)),
         "bits_per_letter_under_the_tables_model": {"the nine rows": round(m.bits(nine), 3), "table 2a": round(m.bits(t2), 3),
                                                    "leaf 1 word rows (spaces removed)": round(m.bits(words1), 3),
                                                    "letters of the nine rows shuffled": round(m.bits(["".join(rng.sample(r, len(r))) for r in nine]), 3)},
         "catalogue_names_found": sorted({n for n in names if any(n in r for r in nine)}),
         "the_rows": nine}

    # D
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 13 <= tnum(k) <= 24]
    prof = {}
    for k in keys:
        c = Counter("".join(book[k]))
        n = sum(c.values())
        prof[k] = {x: c[x] / n for x in "ABCDEFGHILMNOPQRSTUVXZ"}
    cen = {x: statistics.mean(p[x] for p in prof.values()) for x in "ABCDEFGHILMNOPQRSTUVXZ"}
    dist = {k: math.sqrt(sum((p[x] - cen[x]) ** 2 for x in cen)) for k, p in prof.items()}
    rank = sorted(dist, key=lambda k: -dist[k])
    S = {k: "|".join(book[k]) for k in keys}
    enr = []
    for n in names:
        tot = sum(S[k].count(n) for k in keys)
        if tot >= 15:
            here = S["18a"].count(n) + S["18b"].count(n)
            exp = tot * 2 / len(keys)
            enr.append({"name": n, "on_leaf_18": here, "expected": round(exp, 1), "ratio": round(here / exp, 2)})
    enr.sort(key=lambda x: -x["ratio"])
    lm = {k: CharLM(3, alpha=0.1).fit([r for j in keys if j != k for r in book[j] if r]).bits([r for r in book[k] if r]) for k in keys}
    D = {"sides_compared": len(keys), "distance_from_the_average_letter_profile": {k: round(dist[k], 4) for k in ("18a", "18b")},
         "rank_among_the_sides": {k: rank.index(k) + 1 for k in ("18a", "18b")},
         "bits_per_letter_read_by_the_other_sides": {k: round(lm[k], 3) for k in ("18a", "18b")},
         "rank_of_those_bits": {k: sorted(lm, key=lambda j: -lm[j]).index(k) + 1 for k in ("18a", "18b")},
         "names_most_and_least_at_home_on_leaf_18": enr[:5] + enr[-5:]}
    res = {"A_leaf_1_is_a_table_of_words": A, "B_leaf_1_as_a_key_square_for_square": B, "C_nine_rows_of_letters": C, "D_the_eighteenth_leaf": D}
    load.save_result("54_source_checks", res)
    return res


if __name__ == "__main__":
    r = run()
    for k, v in r.items():
        print(k)
        for a, b in v.items():
            print("  ", a, b)
