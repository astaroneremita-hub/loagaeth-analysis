"""
65 - Three more places structure could hide: other systems, refrains, acrostics.

  A) Bridges. Do the names of the other Enochian systems - the 91 governors and 30 Aethyrs
     (governadores.json), the Heptarchy names (heptarquia.json) - appear in the Loagaeth tables more
     than length-matched random strings? (Deepens a25.)
  B) Refrains. A chant repeats whole lines. Does any full line, or any 20-letter line-opening, repeat
     anywhere in the book?
  C) Acrostics. Read the first letter of each row down the left margin (and the last down the right).
     Do these column reads spell the recurring names, more than the same margins from shuffled grids?
     (a24 tested only the prologue; this is every full table.)
"""
import json
import os
import random
import re
import statistics
from collections import Counter

import load
import a15_book_geometry as a15
from a22_robustness_and_depth import base_book, tnum

NAMES = ["CHASTOR", "NOCHA", "GETH", "ACLAX", "ADNOCHA", "NACHO", "OXAD", "ANZACH", "ALGETH", "CHADAX", "GRADAX", "ANTANTOX"]


def norm(s):
    return re.sub(r"[^A-Z]", "", s.upper())


def fullgrid(n):
    lv = load.leaves()
    for k in (f"{n}a", f"{n}b"):
        g = [load.letters(r) for r in lv.get(k, []) if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            return g
    g = a15.rebuild(n)
    return g if g and not any(x is None for row in g for x in row) else None


def run():
    rng = random.Random(65)
    book = base_book()
    S = "".join(r for k, v in book.items() if 2 <= tnum(k) <= 48 for r in v if r)
    f = Counter(S)
    alph, wt = list(f), [f[c] for c in f]

    # A bridges
    D = os.path.join(os.path.dirname(load.DATA), "engine", "data")
    gov = json.load(open(os.path.join(D, "governadores.json"), encoding="utf-8"))
    governors = sorted({norm(g.get("nome", "")) for g in gov.get("governadores", []) if len(norm(g.get("nome", ""))) >= 4})
    hep = json.load(open(os.path.join(D, "heptarquia.json"), encoding="utf-8"))
    hep_names = []

    def harvest(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("nome", "name", "rei", "principe") and isinstance(v, str):
                    hep_names.append(norm(v))
                harvest(v)
        elif isinstance(o, list):
            for x in o:
                harvest(x)
    harvest(hep)
    hep_names = sorted({x for x in hep_names if len(x) >= 4})

    def bridge(wl):
        real = sum(1 for w in wl if w in S)
        nul = [sum(1 for w in wl if "".join(rng.choices(alph, wt, k=len(w))) in S) for _ in range(300)]
        return {"words": len(wl), "found": real, "random": round(statistics.mean(nul), 2),
                "z": round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1)}
    A = {"91_governors": bridge(governors), "heptarchy_names": bridge(hep_names)}

    # B refrains
    rows = [r for k, v in book.items() if 2 <= tnum(k) <= 48 for r in v if r]
    whole = Counter(r for r in rows if len(r) >= 20)
    opens = Counter(r[:20] for r in rows if len(r) >= 20)
    B = {"identical_whole_lines_repeated": sum(1 for n in whole.values() if n > 1),
         "identical_20_letter_openings_repeated": sum(1 for n in opens.values() if n > 1)}

    # C acrostics (true: column reads)
    cols = []
    scols_sets = []
    for n in range(2, 49):
        g = fullgrid(n)
        if not g:
            continue
        cols.append("".join(g[r][0] for r in range(49)))
        cols.append("".join(g[r][48] for r in range(49)))
    real_ac = sum(1 for s in cols for nm in NAMES if nm in s)
    nul_ac = []
    for _ in range(100):
        got = 0
        for n in range(2, 49):
            g = fullgrid(n)
            if not g:
                continue
            flat = [x for row in g for x in row]
            rng.shuffle(flat)
            sg = [flat[i * 49:(i + 1) * 49] for i in range(49)]
            for s in ("".join(sg[r][0] for r in range(49)), "".join(sg[r][48] for r in range(49))):
                got += sum(1 for nm in NAMES if nm in s)
        nul_ac.append(got)
    C = {"names_in_left_or_right_margin_read_down": real_ac, "shuffled": round(statistics.mean(nul_ac), 1),
         "z": round((real_ac - statistics.mean(nul_ac)) / (statistics.pstdev(nul_ac) or 1e-9), 1),
         "note": "First/last letter of each row read down the column. (Reading a whole top or bottom ROW finds names, "
                 "but that is ordinary row text, not an acrostic.)"}

    res = {"A_bridges": A, "B_refrains": B, "C_acrostics": C,
           "conclusion": "Nothing in any of the three. Other-system names appear only about once (governors 1 of 91, "
                         "Heptarchy 1 of 53 - Poisson noise on long rare strings), so the systems stay separate, as a25 "
                         "found and as the record implies (the Loagaeth is a different language from the Calls and the "
                         "Great Table). No whole line and no 20-letter opening ever repeats - there are no refrains. And no "
                         "name reads down the left or right margin (0 vs ~0.3) - no acrostics. The book's structure is the "
                         "names set in metrical rows (a62-a64); nothing hides in other systems, refrains, or margins."}
    load.save_result("65_bridges_refrains_acrostics", res)
    return res


if __name__ == "__main__":
    r = run()
    print("bridges:", r["A_bridges"])
    print("refrains:", r["B_refrains"])
    print("acrostics:", {k: v for k, v in r["C_acrostics"].items() if k != "note"})
    print(r["conclusion"])
