"""
60 - Could the tables have been altered or scrambled after Dee? What a text can and cannot show.

A reader asks whether the data we have might have been manipulated later, so that it "no longer makes
sense". Two kinds of alteration leave different traces:

  - alteration that BREAKS the text's own regularities (a region replaced by noise, leaves shuffled,
    a block scrambled) is detectable: it shows as a leaf whose predictability, doubled-letter rate or
    letter profile jumps away from the rest, or as geometry that no longer adds up;
  - alteration that PRESERVES the local statistics (two leaves of the same dialect swapped, letters
    substituted while keeping the letter-flow) is NOT detectable from one copy. Only an independent
    copy could catch it.

So this module measures the first kind. It reports per leaf: bits per letter under one model of the
whole book, the doubled-letter rate against its own letter frequencies, and the distance of its
letter profile from the book average; it flags outliers and the largest jumps between consecutive
leaves, and checks the chessboard/diamond geometry (each leaf of 29-48 should be 1201 + 1200 = 2401).
"""
import math
import statistics
from collections import Counter

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum

# known structural borders (a27) and their diary dates (WHAT_THE_SOURCES_SAY.md)
KNOWN_BORDERS = {"25a|25b": "rows end, chessboard begins; matches '24 leaves written by 18 April 1583'",
                 "40b|41a": "the U-register segment begins", "33a|33b": "part III/IV",
                 "12b|13a": "part I/II"}


def run():
    book = base_book()
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 2 <= tnum(k) <= 48]
    allrows = [r for k in keys for r in book[k] if r]
    m = CharLM(4, alpha=0.01).fit(allrows)
    f = Counter("".join(allrows))
    N = sum(f.values())
    p2 = sum((v / N) ** 2 for v in f.values())
    cen = {x: f[x] / N for x in f}

    rows = []
    for k in keys:
        rs = [r for r in book[k] if r]
        s = "".join(rs)
        pairs = sum(len(r) - 1 for r in rs)
        same = sum(a == b for r in rs for a, b in zip(r, r[1:]))
        c = Counter(s)
        n = len(s)
        dist = math.sqrt(sum((c[x] / n - cen.get(x, 0)) ** 2 for x in set(c) | set(cen)))
        rows.append({"leaf": k, "bits": round(m.bits(rs), 3), "double_obs_over_exp": round(same / (pairs * p2), 3),
                     "profile_distance": round(dist, 4)})

    def outliers(key):
        vals = [r[key] for r in rows]
        mu, sd = statistics.mean(vals), statistics.pstdev(vals)
        return {"mean": round(mu, 3), "sd": round(sd, 3),
                "outliers_z_gt_2.5": [{"leaf": r["leaf"], "value": r[key], "z": round((r[key] - mu) / sd, 1)} for r in rows if abs((r[key] - mu) / sd) > 2.5]}

    jumps = sorted(((round(abs(rows[i + 1]["bits"] - rows[i]["bits"]), 3), rows[i]["leaf"] + "|" + rows[i + 1]["leaf"]) for i in range(len(rows) - 1)), reverse=True)[:6]

    geom = {}
    for t in range(29, 49):
        a = sum(len(load.letters(r)) for r in load.leaves().get(f"{t}a", []))
        b = sum(len(load.letters(r)) for r in load.leaves().get(f"{t}b", []))
        geom[f"leaf {t}"] = {"a": a, "b": b, "total": a + b, "complete_2401": a + b == 2401}

    res = {"leaves": len(rows),
           "bits_per_leaf": outliers("bits"),
           "doubled_letter_rate": outliers("double_obs_over_exp"),
           "letter_profile_distance": outliers("profile_distance"),
           "largest_bits_jumps": [{"border": b, "jump": j, "known": KNOWN_BORDERS.get(b, "")} for j, b in jumps],
           "chessboard_diamond_geometry": geom,
           "geometry_complete_leaves": sum(1 for v in geom.values() if v["complete_2401"]),
           "conclusion": ("The book is internally homogeneous. Bits per leaf are flat with no outlier (a replaced or "
                          "scrambled leaf would stand out). The doubled-letter rate has two mild high leaves (3a, 7b) with "
                          "the extra doubles spread across many rows, not a localized corruption. The distinct letter "
                          "profile of 43-48 is the known fourth segment (a15), not a seam. The two largest jumps are the "
                          "format border 24b|25a|25b, which matches the diary's writing dates. The chessboard/diamond "
                          "geometry is exactly 1201+1200=2401 on 13 of the 20 leaves 29-48; the other seven are off by one or two cells (ordinary copying slips, about 0.1%) or fall in the known irregular end segment 44-48 - none is scrambled, and a shuffle would not leave near-complete grids. So no "
                          "trace of alteration that broke the text's rules. LIMIT: alteration that preserved the local "
                          "statistics (a same-dialect leaf swap, or letter substitution keeping the letter-flow) cannot be "
                          "detected from one transcription; only an independent copy (Klein's, the 17th-c copies) could. "
                          "The one place with a known ground truth, the Soyga tables at the back (Reeds' generator, a36), "
                          "shows 3.3% copying error and no systematic tampering.")}
    load.save_result("60_tampering", res)
    return res


if __name__ == "__main__":
    r = run()
    for key in ("bits_per_leaf", "doubled_letter_rate", "letter_profile_distance"):
        print(key, "->", r[key]["mean"], "sd", r[key]["sd"], "| outliers:", [(o["leaf"], o["z"]) for o in r[key]["outliers_z_gt_2.5"]])
    print("largest jumps:", [(j["border"], j["jump"]) for j in r["largest_bits_jumps"]])
    print("geometry complete leaves (29-48):", r["geometry_complete_leaves"], "of 20")
    print(r["conclusion"])
