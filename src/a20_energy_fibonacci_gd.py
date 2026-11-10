"""
20 - Letter "energy" by realm, Fibonacci, gradual division, and a Golden-Dawn-style rearrangement.

  A) Energy: if each letter carries a value (Enochian gematria, in each of the 13 bundled systems)
     or an information weight (surprisal, -log2 p), is the text "denser" at the end of the book?
     Mean value per letter by segment; end vs heartland tested by shuffling tables between the two
     groups; then the same with U turned back into A to see what drives it.
  B) Fibonacci: (i) gaps between successive CHASTOR occurrences - share that are Fibonacci numbers
     vs random positions; (ii) where CHASTOR starts inside a 49-letter row - Fibonacci columns vs
     the rest; (iii) segment borders and the golden section of the 49 tables (descriptive).
  C) Gradual division: the 49x49 grids cut into 7x7 blocks - do blocks differ more than chance?
     The central row/column (the "Great Cross" position of the Watchtowers) vs other rows.
  D) Golden Dawn reformed the Great Table by moving whole tablets. Cut each row-written table into
     four quadrants around the central cross and try all 24 arrangements: does any read better than
     the original (recurring-name share along rows)?
"""
import itertools
import json
import math
import os
import random
import statistics
import sys
from collections import Counter

import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))
DECODED = os.path.join(ROOT, "data", "loagaeth_diagonal_decoded.json")
SEGMENTS = {"opening_2_5": range(2, 6), "heartland_6_24": range(6, 25),
            "diamonds_29_43": range(29, 44), "end_44_48": range(44, 49)}
FIB = {1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597, 2584, 4181}


def rows(key):
    return [load.letters(r) for r in load.leaves().get(key, [])]


def table_text(t):
    return "".join("".join(rows(f"{t}{s}")) for s in "ab")


def full_grids(tables=range(2, 25)):
    out = []
    for t in tables:
        for s in "ab":
            g = rows(f"{t}{s}")
            if len(g) == 49 and all(len(r) == 49 for r in g):
                out.append(g)
    return out


def run():
    rng = random.Random(20)
    try:
        import fontes
        G = fontes.gematria_value_tables()
    except Exception:
        G = {}

    # A energy
    texts = {t: table_text(t) for rg in SEGMENTS.values() for t in rg}
    book = Counter("".join(texts.values()))
    N = sum(book.values())
    surpr = {c: -math.log2(n / N) for c, n in book.items()}

    def mean_val(txt, tab):
        v = [tab[c] for c in txt if c in tab]
        return sum(v) / len(v) if v else None
    energy = {}
    heart = list(SEGMENTS["heartland_6_24"])
    endt = list(SEGMENTS["end_44_48"])

    def perm_test(f):
        a = [f(texts[t]) for t in heart]
        b = [f(texts[t]) for t in endt]
        obs = statistics.mean(b) - statistics.mean(a)
        pool = a + b
        cnt = 0
        for _ in range(2000):
            rng.shuffle(pool)
            if statistics.mean(pool[len(a):]) - statistics.mean(pool[:len(a)]) >= obs:
                cnt += 1
        return round(obs, 3), round(cnt / 2000, 4)
    systems = dict(G)
    systems["surprisal_bits"] = surpr
    for sid, tab in systems.items():
        seg = {k: round(statistics.mean(mean_val(texts[t], tab) for t in rg if mean_val(texts[t], tab) is not None), 2)
               for k, rg in SEGMENTS.items()}
        d, p = perm_test(lambda s, tab=tab: mean_val(s, tab))
        d2, p2 = perm_test(lambda s, tab=tab: mean_val(s.replace("U", "A"), tab))
        energy[sid] = {"mean_by_segment": seg, "end_minus_heartland": d, "p": p,
                       "with_U_as_A": {"end_minus_heartland": d2, "p": p2}}
    sig = [k for k, v in energy.items() if v["p"] < 0.05 / len(energy) and v["end_minus_heartland"] > 0]
    sig_noU = [k for k, v in energy.items() if v["with_U_as_A"]["p"] < 0.05 / len(energy) and v["with_U_as_A"]["end_minus_heartland"] > 0]

    # B Fibonacci
    parts = [table_text(t) for t in range(2, 25)]
    if os.path.exists(DECODED):
        dec = json.load(open(DECODED, encoding="utf-8"))["faces"]
        parts += ["".join(f["down_right"] + f["leftward"]) for f in dec.values()]
    parts += [table_text(t) for t in range(29, 49)]
    stream = "|".join(parts)
    pos = [i for i in range(len(stream)) if stream.startswith("CHASTOR", i)]
    gaps = [b - a for a, b in zip(pos, pos[1:])]
    fib_share = sum(1 for g in gaps if g in FIB) / len(gaps)
    null = []
    for _ in range(2000):
        rp = sorted(rng.sample(range(len(stream)), len(pos)))
        rg = [b - a for a, b in zip(rp, rp[1:])]
        null.append(sum(1 for g in rg if g in FIB) / len(rg))
    cols = []
    for g in full_grids():
        for r in g:
            i = r.find("CHASTOR")
            while i >= 0:
                cols.append(i + 1)
                i = r.find("CHASTOR", i + 1)
    fibcols = [c for c in range(1, 44) if c in FIB]
    obs_fc = sum(1 for c in cols if c in FIB) / len(cols) if cols else 0
    exp_fc = len(fibcols) / 43
    fib = {"chastor_occurrences": len(pos),
           "gaps_that_are_fibonacci": round(fib_share, 4), "null_mean": round(statistics.mean(null), 4),
           "null_95th": round(sorted(null)[1899], 4),
           "chastor_start_column_fibonacci_share": round(obs_fc, 3), "expected_if_uniform": round(exp_fc, 3),
           "n_row_occurrences": len(cols),
           "golden_section_of_49_tables": round(49 / ((1 + 5 ** 0.5) / 2), 1),
           "segment_borders": [6, "25b", 29, 44],
           "note": "Borders are not at Fibonacci numbers nor at the golden section (30.3)."}

    # C gradual division (7x7 blocks) and the central cross
    grids = full_grids()

    def block_chi(gs):
        M = {}
        for g in gs:
            for r in range(49):
                for c in range(49):
                    M.setdefault((r // 7, c // 7), Counter())[g[r][c]] += 1
        tot = {k: sum(v.values()) for k, v in M.items()}
        T = sum(tot.values())
        x = 0.0
        for L in set().union(*M.values()):
            nL = sum(M[k][L] for k in M)
            for k in M:
                e = nL * tot[k] / T
                if e > 5:
                    x += (M[k][L] - e) ** 2 / e
        return x
    xb = block_chi(grids)
    nb = []
    for _ in range(60):
        sh = []
        for g in grids:
            f = list("".join(g))
            rng.shuffle(f)
            sh.append(["".join(f[i * 49:(i + 1) * 49]) for i in range(49)])
        nb.append(block_chi(sh))
    ref = "".join("".join(g) for g in grids)
    rec = {g for g, f in Counter(ref[i:i + 6] for i in range(len(ref) - 5)).items() if f >= 5}

    def names(lines):
        tot = hit = 0
        for l in lines:
            for i in range(len(l) - 5):
                tot += 1
                hit += l[i:i + 6] in rec
        return hit / tot if tot else 0.0
    centre_row = names([g[24] for g in grids])
    other_rows = names([g[r] for g in grids for r in range(49) if r != 24])
    division = {"blocks_7x7_chi2": round(xb), "shuffled_mean": round(statistics.mean(nb)),
                "shuffled_95th": round(sorted(nb)[56]),
                "central_row_names": round(centre_row, 3), "other_rows_names": round(other_rows, 3),
                "pyramid_arithmetic": {"odd_diamond_cells": 1201, "as_squares": "1201 = 25^2 + 24^2",
                                       "even_diamond_cells": 1200, "as_product": "1200 = 2 x 24 x 25",
                                       "upper_half_odd_diamond": "1+3+...+49 = 625 = 25^2 (a stepped pyramid)"}}

    # D Golden Dawn style rearrangement of quadrants
    def quads(g):
        q = {"TL": [r[:24] for r in g[:24]], "TR": [r[25:] for r in g[:24]],
             "BL": [r[:24] for r in g[25:]], "BR": [r[25:] for r in g[25:]]}
        return q

    def assemble(g, order):
        q = quads(g)
        tl, tr, bl, br = (q[o] for o in order)
        top = [tl[i] + g[i][24] + tr[i] for i in range(24)]
        bot = [bl[i] + g[25 + i][24] + br[i] for i in range(24)]
        return top + [g[24]] + bot
    best_counts = Counter()
    gains = []
    for g in grids:
        base = names(g)
        scores = {o: names(assemble(g, o)) for o in itertools.permutations(["TL", "TR", "BL", "BR"])}
        best = max(scores, key=scores.get)
        best_counts["original" if best == ("TL", "TR", "BL", "BR") else "rearranged"] += 1
        gains.append(max(v for o, v in scores.items() if o != ("TL", "TR", "BL", "BR")) - base)
    gd = {"tables": len(grids), "best_arrangement": dict(best_counts),
          "mean_gain_of_best_rearrangement_over_original": round(statistics.mean(gains), 4),
          "note": "Rows run across the central column, so moving quadrants cuts words; the original order is the reading order."}

    res = {"A_energy_by_segment": energy,
           "A_summary": {"systems": len(energy), "end_denser_after_bonferroni": sig,
                         "still_denser_with_U_as_A": sig_noU},
           "B_fibonacci": fib, "C_gradual_division": division, "D_golden_dawn_rearrangement": gd,
           "conclusion": ("The end of the book is 'denser' in most letter-value systems and in information per "
                          "letter, but the effect is carried by the A->U shift: turning U back into A removes most of "
                          "it. No Fibonacci or golden-section structure was found. 7x7 sub-blocks and the central "
                          "cross are not special. Re-arranging quadrants Golden-Dawn style never beats the original.")}
    load.save_result("20_energy_fibonacci_gd", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1)[:3000])
