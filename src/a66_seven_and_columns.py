"""
66 - The 7x7 obsession, and a column template.

The book is built on 49 = 7 x 7. Does a 7-fold substructure show in the text, or is 49 only the
frame? And does position in the row predict the letter - a vertical template over the grid?

  A) Seven. Do word boundaries fall on multiples of 7? Do names start at a preferred position mod 7?
     Is there a period-7 rhythm in the vowel pattern (autocorrelation at lag 7)?
  B) Columns. For each column 0-48, the share of rows with a vowel there. Is it flat (no template),
     or does position predict vowel/consonant beyond the row's own composition (shuffle control)?
"""
import json
import os
import random
import re
import statistics
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum
import a51_word_points as wp

VOW = set("AEIOUVY")


def run():
    rng = random.Random(66)
    book = base_book()
    rows = [r for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if len(r) == 49]

    # A seven
    G = wp.parse()
    cutpos = Counter(c for k in G for i in G[k] for c in G[k][i]["cuts"] if 0 < c < 49)
    tot = sum(cutpos.values())
    at7 = sum(cutpos[c] for c in (7, 14, 21, 28, 35, 42))

    def vpat(r):
        return [1 if c in VOW else 0 for c in r]

    def autocorr(lag):
        s = n = 0
        for r in rows:
            v = vpat(r)
            for i in range(len(v) - lag):
                s += v[i] == v[i + lag]
                n += 1
        return s / n
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    names = [x["name"] for x in d] + ["CHASTOR", "NOCHA", "GETH", "ACLAX", "OXAD", "NACHO"]
    mod7 = Counter()
    for r in rows:
        for nm in names:
            i = r.find(nm)
            while i >= 0:
                mod7[i % 7] += 1
                i = r.find(nm, i + 1)
    A = {"word_points_at_multiples_of_7_percent": round(100 * at7 / tot, 1), "chance_percent": round(100 * 6 / 48, 1),
         "vowel_autocorrelation_by_lag": {L: round(autocorr(L), 3) for L in (1, 2, 3, 4, 5, 6, 7, 14)},
         "name_start_positions_mod_7": dict(sorted(mod7.items())),
         "conclusion": "No 7-fold substructure. Word boundaries fall on multiples of 7 slightly BELOW chance (11.6 vs "
                       "12.5%%); names start evenly across positions mod 7; the vowel autocorrelation peaks at lag 3, not "
                       "lag 7. The 49 = 7x7 is the frame of the grid, not a rhythm in the text (the lag-3 peak is the "
                       "3-syllable stress foot of a63)."}

    # B columns
    colv = [sum(1 for r in rows if r[c] in VOW) / len(rows) for c in range(49)]
    nul = []
    for _ in range(80):
        sh = ["".join(rng.sample(r, 49)) for r in rows]
        nul.append(statistics.pstdev([sum(1 for r in sh if r[c] in VOW) / len(sh) for c in range(49)]))
    sd_front = statistics.pstdev(colv[:5])
    sd_rest = statistics.pstdev(colv[5:])
    B = {"vowel_share_per_column_first_6": [round(x, 2) for x in colv[:6]], "min": round(min(colv), 2), "max": round(max(colv), 2),
         "sd_all_columns": round(statistics.pstdev(colv), 3), "sd_shuffled": round(statistics.mean(nul), 3),
         "z": round((statistics.pstdev(colv) - statistics.mean(nul)) / statistics.pstdev(nul), 1),
         "sd_first_5_columns": round(sd_front, 3), "sd_columns_5_to_48": round(sd_rest, 3),
         "conclusion": "There is a column effect (z ~25), but it is a line-ONSET signature, not a deep vertical template: "
                       "the vowel share swings in the first five columns (col 1 vowel-heavy 0.57, col 2 consonant-heavy "
                       "0.25) and is flat from column five on (~0.39-0.42). Rows begin with a characteristic shape, then "
                       "position stops predicting the letter. Consistent with the rows as a stream (a49) with a preferred "
                       "opening, not a columnar architecture."}

    res = {"A_seven": A, "B_columns": B}
    load.save_result("66_seven_and_columns", res)
    return res


if __name__ == "__main__":
    r = run()
    print("SEVEN:", r["A_seven"]["word_points_at_multiples_of_7_percent"], "% at mult-7 (chance", r["A_seven"]["chance_percent"], "%)")
    print("  vowel autocorr:", r["A_seven"]["vowel_autocorrelation_by_lag"])
    print("  ", r["A_seven"]["conclusion"])
    print("COLUMNS: sd all", r["B_columns"]["sd_all_columns"], "vs shuffled", r["B_columns"]["sd_shuffled"], "z", r["B_columns"]["z"])
    print("  first 6 cols vowel-share:", r["B_columns"]["vowel_share_per_column_first_6"], "| sd first5", r["B_columns"]["sd_first_5_columns"], "sd rest", r["B_columns"]["sd_columns_5_to_48"])
    print("  ", r["B_columns"]["conclusion"])
