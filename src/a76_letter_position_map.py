"""
76 - Where does each letter sit? A per-letter column map, and can it predict the next lines?

The stratification (a75) says every row carries a balanced share of each letter. This asks the finer
question Murilo wants: WITHIN a row, which columns does each letter favour, and is that stable enough
that you could predict where the letter lands in the next lines?

Per leaf:
  A) column profile of each letter = how its occurrences spread over the 49 columns. Concentration =
     1 - normalised entropy (0 = flat/no preference, 1 = always the same column).
  B) PREDICTABILITY: build each letter's column profile from the ODD rows, and from the EVEN rows.
     If the letter sits in consistent columns, the two halves agree. Score = cosine similarity of the
     two half-profiles, real vs a leaf whose cells are shuffled (same letters, positions destroyed).
     Real >> shuffle means the column a letter prefers in some rows predicts where it sits in others.
Book-wide column profile per letter is saved so a map can be drawn and used to guess the next line.
"""
import json
import math
import random
import statistics
from collections import defaultdict

import load

COLS = 49


def col_profile(rowlist, ch):
    p = [0] * COLS
    for row in rowlist:
        for c, x in enumerate(row):
            if x == ch:
                p[c] += 1
    return p


def norm_entropy(p):
    s = sum(p)
    if s == 0:
        return None
    ps = [x / s for x in p if x]
    h = -sum(x * math.log(x) for x in ps)
    return h / math.log(COLS)  # 0..1


def cosine(a, b):
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na == 0 or nb == 0:
        return None
    return sum(x * y for x, y in zip(a, b)) / (na * nb)


def shuffle_leaf(rows, rng):
    flat = [ch for row in rows for ch in row]
    rng.shuffle(flat)
    out, i = [], 0
    for row in rows:
        out.append("".join(flat[i:i + len(row)]))
        i += len(row)
    return out


def run():
    rng = random.Random(76)
    lv = load.leaves()
    grids = {}
    for leaf, rows in lv.items():
        g = ["".join(load.letters(r)) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            grids[leaf] = g

    alph = sorted(set("".join("".join(g) for g in grids.values())))
    book_profile = {ch: [0] * COLS for ch in alph}

    concentration, pred_real, pred_shuf = [], [], []
    per_leaf = {}
    for leaf, rows in grids.items():
        odd, even = rows[0::2], rows[1::2]
        srows = shuffle_leaf(rows, rng)
        sodd, seven = srows[0::2], srows[1::2]
        letters = [ch for ch in alph if sum(row.count(ch) for row in rows) >= 49]
        concs, prs, pss = [], [], []
        for ch in letters:
            full = col_profile(rows, ch)
            for c in range(COLS):
                book_profile[ch][c] += full[c]
            ne = norm_entropy(full)
            if ne is not None:
                concs.append(1 - ne)
            cr = cosine(col_profile(odd, ch), col_profile(even, ch))
            cs = cosine(col_profile(sodd, ch), col_profile(seven, ch))
            if cr is not None and cs is not None:
                prs.append(cr)
                pss.append(cs)
        per_leaf[leaf] = {"mean_concentration": round(statistics.mean(concs), 3),
                          "halves_cosine_real": round(statistics.mean(prs), 3),
                          "halves_cosine_shuffle": round(statistics.mean(pss), 3)}
        concentration.append(statistics.mean(concs))
        pred_real.append(statistics.mean(prs))
        pred_shuf.append(statistics.mean(pss))

    # which letters are most positionally pinned, book-wide (peak column share)
    pinned = []
    for ch in alph:
        p = book_profile[ch]
        s = sum(p)
        if s >= 200:
            peak = max(range(COLS), key=lambda c: p[c])
            pinned.append({"letter": ch, "peak_col": peak,
                           "peak_share_pct": round(100 * p[peak] / s, 1),
                           "concentration": round(1 - (norm_entropy(p) or 1), 3)})
    pinned.sort(key=lambda d: -d["concentration"])

    mr, ms = statistics.mean(pred_real), statistics.mean(pred_shuf)
    res = {
        "leaves": len(grids),
        "mean_concentration": round(statistics.mean(concentration), 3),
        "predictability_halves_cosine_real": round(mr, 3),
        "predictability_halves_cosine_shuffle": round(ms, 3),
        "predictability_gain": round(mr - ms, 3),
        "note": "concentration 0 = letter has no column preference, 1 = always same column. halves-cosine: "
                "agreement between a letter's column profile on odd vs even rows; real>>shuffle means its "
                "column habit in some lines predicts where it sits in others.",
        "most_pinned_letters": pinned[:12],
        "book_column_profile": {ch: book_profile[ch] for ch in alph},
        "per_leaf": per_leaf,
        "conclusion": "",
    }
    verdict = ("letters DO carry a stable column habit you can predict from other lines"
               if mr > ms + 0.05 else
               "column position is barely more predictable than chance - each letter roams the row")
    res["conclusion"] = (
        "Across %d leaves, mean column-concentration %.2f (0=no preference, 1=fixed column). Odd vs even "
        "rows agree at cosine %.2f real vs %.2f shuffled (gain %.3f): %s." % (
            len(grids), res["mean_concentration"], mr, ms, mr - ms, verdict))
    load.save_result("76_letter_position_map", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["conclusion"])
    print("\nmost positionally pinned letters (book-wide):")
    for d in r["most_pinned_letters"]:
        print("  %s  peak col %2d  (%4.1f%% of its hits there)  concentration %.3f" % (
            d["letter"], d["peak_col"], d["peak_share_pct"], d["concentration"]))
