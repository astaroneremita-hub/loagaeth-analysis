"""
74 - Kabbalistic lens: is there ARITHMETIC in the arrangement? (line/column gematria balance)

A cabalistic / magic-square reading predicts the letters are placed so that lines carry balanced
numeric value - rows (or columns) summing to equal-ish gematria, or exact sums recurring far more than
chance. If Dee only wrote names with no arithmetic intent, the row-sums are whatever the letter multiset
and its arrangement happen to give, and SHUFFLING the leaf's own letters (same multiset, arrangement
destroyed) leaves the spread of row-sums unchanged.

Two tests per full 49x49 leaf, under the isopsefia values (F07), repeated for a second value system:
  A) BALANCE: coefficient of variation (sd/mean) of the 49 row-sums, real vs 200 within-leaf shuffles.
     Real CV well BELOW shuffle = rows deliberately evened out (magic-square-like). z over shuffles.
  B) EXACT REPEATS: the most-repeated exact row-sum value, real vs shuffle. More exact repeats than
     chance = quantised to special totals. Same for columns.
A real arithmetic design shows up as balance and/or repeats beyond the shuffle on many leaves; letter-flow
alone shows real ~ shuffle.
"""
import json
import os
import random
import statistics
from collections import Counter

import load

# isopsefia latino-grega (F07) and digital reduction (F07) - both full 21-letter
ISO = {"A": 1, "B": 2, "C": 20, "D": 4, "E": 5, "F": 6, "G": 3, "H": 8, "I": 10, "L": 30,
       "M": 40, "N": 50, "O": 70, "P": 80, "Q": 90, "R": 100, "S": 200, "T": 300, "U": 400,
       "X": 60, "Z": 7}
DEE_ORDINAL = {c: i + 1 for i, c in enumerate("BCDFGHLMNPQRSTUXZAEIO")}  # consonants then vowels order proxy


def val(row, table):
    return sum(table.get(ch, 0) for ch in row)


def cv(xs):
    m = statistics.mean(xs)
    return (statistics.pstdev(xs) / m) if m else 0.0


def top_repeat(xs):
    return max(Counter(xs).values())


def shuffle_leaf(grid, rng):
    flat = [ch for row in grid for ch in row]
    rng.shuffle(flat)
    out, i = [], 0
    for row in grid:
        out.append(flat[i:i + len(row)])
        i += len(row)
    return ["".join(r) for r in out]


def analyse(grid, table, rng, nshuf=200):
    rows = ["".join(r) for r in grid]
    cols = ["".join(grid[r][c] for r in range(49)) for c in range(49)]
    r_cv, c_cv = cv([val(x, table) for x in rows]), cv([val(x, table) for x in cols])
    r_rep = top_repeat([val(x, table) for x in rows])
    sh_rcv, sh_ccv, sh_rep = [], [], []
    for _ in range(nshuf):
        sg = shuffle_leaf(grid, rng)
        srows = sg
        scols = ["".join(sg[r][c] for r in range(49)) for c in range(49)]
        sh_rcv.append(cv([val(x, table) for x in srows]))
        sh_ccv.append(cv([val(x, table) for x in scols]))
        sh_rep.append(top_repeat([val(x, table) for x in srows]))

    def z(real, nul, lower_is_signal):
        mu, sd = statistics.mean(nul), (statistics.pstdev(nul) or 1e-9)
        zz = (real - mu) / sd
        return round(zz, 2)
    return {
        "row_cv": round(r_cv, 4), "shuffle_row_cv_mean": round(statistics.mean(sh_rcv), 4),
        "row_cv_z": z(r_cv, sh_rcv, True),
        "col_cv": round(c_cv, 4), "shuffle_col_cv_mean": round(statistics.mean(sh_ccv), 4),
        "col_cv_z": z(c_cv, sh_ccv, True),
        "row_top_repeat": r_rep, "shuffle_row_repeat_mean": round(statistics.mean(sh_rep), 2),
        "row_repeat_z": z(r_rep, sh_rep, False),
    }


def run():
    rng = random.Random(74)
    lv = load.leaves()
    grids = {}
    for leaf, rows in lv.items():
        g = [load.letters(r) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            grids[leaf] = g

    per = {}
    for leaf, g in grids.items():
        per[leaf] = {"ISO": analyse(g, ISO, rng), "DEE_ORD": analyse(g, DEE_ORDINAL, rng)}

    # aggregate z across leaves (negative row_cv_z = rows more balanced than shuffle)
    def agg(sys, field):
        xs = [per[k][sys][field] for k in per]
        return round(statistics.mean(xs), 2)

    summary = {}
    for sys in ("ISO", "DEE_ORD"):
        summary[sys] = {
            "mean_row_cv_z": agg(sys, "row_cv_z"),
            "mean_col_cv_z": agg(sys, "col_cv_z"),
            "mean_row_repeat_z": agg(sys, "row_repeat_z"),
            "leaves_rows_balanced_z_lt_-2": sum(1 for k in per if per[k][sys]["row_cv_z"] < -2),
            "leaves_repeat_excess_z_gt_2": sum(1 for k in per if per[k][sys]["row_repeat_z"] > 2),
        }

    iso = summary["ISO"]
    strong = (iso["mean_row_cv_z"] < -2 or iso["mean_col_cv_z"] < -2 or iso["mean_row_repeat_z"] > 2)
    verdict = ("CONFIRMADO NOVO: the leaves carry deliberate line arithmetic - sums balanced/quantised "
               "beyond the letter multiset." if strong else
               "DESCRIPTIVE: line gematria is whatever the letters give; no arithmetic balancing beyond "
               "the multiset (real ~ shuffle). No magic-square design.")
    res = {
        "leaves": len(grids),
        "shuffles_per_leaf": 200,
        "note": "row_cv_z < 0 = rows more balanced (equal-value) than a shuffle of the same letters; "
                "row_repeat_z > 0 = an exact row-sum repeats more than a shuffle. Both are signatures of "
                "intentional arithmetic. ~0 = none.",
        "summary": summary,
        "conclusion": "%s ISO mean row-cv z %.2f, col-cv z %.2f, repeat z %.2f over %d leaves." % (
            verdict, iso["mean_row_cv_z"], iso["mean_col_cv_z"], iso["mean_row_repeat_z"], len(grids)),
        "per_leaf": per,
    }
    load.save_result("74_gematria_lines", res)
    return res


if __name__ == "__main__":
    r = run()
    for sys in ("ISO", "DEE_ORD"):
        s = r["summary"][sys]
        print("%-8s row-cv z %6.2f | col-cv z %6.2f | repeat z %6.2f | balanced leaves %d | repeat leaves %d"
              % (sys, s["mean_row_cv_z"], s["mean_col_cv_z"], s["mean_row_repeat_z"],
                 s["leaves_rows_balanced_z_lt_-2"], s["leaves_repeat_excess_z_gt_2"]))
    print("\n" + r["conclusion"])
