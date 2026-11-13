"""
a139 - Four remaining minor investigations, each vs a null.
  #3 geometry: do names cluster at the CENTER of each square vs the edges?
  #4 gematria: do consonant-root families share a letter-sum value? (practitioner layer; Dee didn't use it)
  #5 borders/acrostic: do the first/last column and the main diagonal spell names above chance?
  #6 Watchtowers: do the Loagaeth grids share phonology (bigrams) with the 4 Watchtower tables?
"""
import json
import random
import statistics
import unicodedata
from collections import Counter, defaultdict

import load
from a22_robustness_and_depth import base_book

VOWELS = set("AEIOU")
VAL = {'B': 1, 'C': 2, 'G': 3, 'D': 4, 'F': 5, 'A': 6, 'E': 7, 'M': 8, 'I': 9, 'H': 10, 'L': 11,
       'P': 12, 'Q': 13, 'N': 14, 'X': 15, 'O': 16, 'R': 17, 'Z': 18, 'U': 19, 'S': 20, 'T': 21}


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").upper()


def square_grids():
    book = base_book()
    out = []
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            out.append(g)
    return out


def geometry(grids, names):
    """name-start cells: fraction in central 7x7 vs expected (49/2401)."""
    R = 49
    cen = tot = 0
    for g in grids:
        for r in range(R):
            row = g[r]
            for w in names:
                if len(w) < 4:
                    continue
                i = row.find(w)
                while i >= 0:
                    tot += 1
                    if 21 <= r <= 27 and 21 <= i <= 27:
                        cen += 1
                    i = row.find(w, i + 1)
    exp = (7 * 7) / (R * R)
    return {"name_starts": tot, "central_frac": round(cen / tot, 4) if tot else 0,
            "expected_frac": round(exp, 4), "enrichment": round((cen / tot) / exp, 2) if tot else 0}


def gematria(names):
    def val(w):
        return sum(VAL.get(c, 0) for c in w)
    skel = lambda w: "".join(c for c in w if c not in VOWELS)
    fam = defaultdict(list)
    for w in names:
        fam[skel(w)].append(val(w))
    multi = {s: vs for s, vs in fam.items() if len(vs) >= 3}
    real_cv = statistics.mean(statistics.pstdev(vs) / (statistics.mean(vs) or 1) for vs in multi.values()) if multi else 0
    allv = [val(w) for w in names]
    rng = random.Random(1)
    nulls = []
    for _ in range(200):
        shuffled = allv[:]
        rng.shuffle(shuffled)
        it = iter(shuffled)
        g = {s: [next(it) for _ in vs] for s, vs in multi.items()}
        nulls.append(statistics.mean(statistics.pstdev(v) / (statistics.mean(v) or 1) for v in g.values()))
    nmean = statistics.mean(nulls)
    return {"families": len(multi), "within_family_cv_real": round(real_cv, 3),
            "within_family_cv_null": round(nmean, 3),
            "shares_value": real_cv < nmean * 0.8}


def borders(grids, names):
    nset = set(w for w in names if len(w) >= 4)
    R = 49
    hits = 0
    lines = []
    for g in grids:
        lines.append("".join(g[r][0] for r in range(R)))      # first column
        lines.append("".join(g[r][R - 1] for r in range(R)))  # last column
        lines.append("".join(g[r][r] for r in range(R)))      # main diagonal
        lines.append("".join(g[0]))                            # top row
        lines.append("".join(g[R - 1]))                        # bottom row
    for ln in lines:
        for w in nset:
            if w in ln or w in ln[::-1]:
                hits += 1
    # null: random columns
    allletters = "".join("".join(g) for g in grids)
    rng = random.Random(5)
    nulls = []
    for _ in range(100):
        nh = 0
        for _ in range(len(lines)):
            s = "".join(rng.choice(allletters) for _ in range(R))
            for w in nset:
                if w in s or w in s[::-1]:
                    nh += 1
        nulls.append(nh)
    return {"border_name_hits": hits, "null_mean": round(statistics.mean(nulls), 1),
            "null_max": max(nulls), "above": hits > max(nulls)}


def watchtowers(grids):
    def bg(text):
        c = Counter()
        for i in range(len(text) - 1):
            if text[i].isalpha() and text[i + 1].isalpha():
                c[text[i:i + 2]] += 1
        t = sum(c.values()) or 1
        return {k: v / t for k, v in c.items()}

    def cos(a, b):
        ks = set(a) | set(b)
        na = sum(v * v for v in a.values()) ** 0.5
        nb = sum(v * v for v in b.values()) ** 0.5
        return sum(a.get(k, 0) * b.get(k, 0) for k in ks) / (na * nb) if na and nb else 0
    loag = bg("".join("".join(g) for g in grids))
    try:
        tt = json.load(open(load.ROOT + "/engine/data/tabuas_dee1584.json", encoding="utf-8"))["torres"]
        wt_text = ""
        for name, grid in tt.items():
            if isinstance(grid, dict):
                grid = grid.get("grade") or grid.get("linhas") or list(grid.values())
            if isinstance(grid, list):
                wt_text += da("".join(x for x in grid if isinstance(x, str)))
        wt = bg(wt_text)
        sim = round(cos(loag, wt), 3)
    except Exception as e:
        sim = None
    return {"loag_vs_watchtowers_bigram": sim}


def run():
    grids = square_grids()
    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))
    res = {
        "geometry": geometry(grids, names),
        "gematria": gematria(names),
        "borders": borders(grids, names),
        "watchtowers": watchtowers(grids),
    }
    load.save_result("139_minor_four", res)
    return res


if __name__ == "__main__":
    r = run()
    g = r["geometry"]
    print("#3 GEOMETRIA: %.1f%% dos nomes começam no centro 7x7 vs %.1f%% esperado (%.1fx) -> %s" % (
        g["central_frac"] * 100, g["expected_frac"] * 100, g["enrichment"],
        "centro preferido" if g["enrichment"] > 1.3 else "sem preferência de centro"))
    gm = r["gematria"]
    print("#4 GEMATRIA: CV intra-família real %.3f vs null %.3f -> %s" % (
        gm["within_family_cv_real"], gm["within_family_cv_null"],
        "famílias partilham valor" if gm["shares_value"] else "não partilham (gematria não estrutura)"))
    b = r["borders"]
    print("#5 BORDAS: %d nomes nas bordas/diagonal vs null média %.1f (máx %d) -> %s" % (
        b["border_name_hits"], b["null_mean"], b["null_max"],
        "acima do acaso" if b["above"] else "~acaso"))
    w = r["watchtowers"]
    print("#6 TORRES: similaridade de bigrama Loagaeth x Torres = %s" % w["loag_vs_watchtowers_bigram"])
