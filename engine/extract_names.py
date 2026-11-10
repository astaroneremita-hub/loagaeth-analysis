# -*- coding: utf-8 -*-
"""Exploratory: can a Watchtower-style GEOMETRY extract a name-system from the 49x49
Loagaeth tables, the way the Great Cross extracts kings/seniors/angels from the Towers?

This is a HYPOTHESIS tool, not a revealed system. It applies tower-style extraction
(cross arms + a king-like spiral) from the centre of each 49x49 grid, produces candidate
names, and tests them against a NULL: the same extraction from RANDOM positions. If the
centre beats the null (recurrence / lexicon-match / positional-grammar fit), the grid
hides a name-structure. If not, the geometry is arbitrary and the "names" are grid
fragments.

Result (bundled data): NEGATIVE. The centre does not beat the null (recurrence z~1.7,
lexicon z~0, grammar z~0.5). The Loagaeth 49x49 grid is NOT built like the Great Table -
there is no Great-Cross / spiral-king geometry. The real names live in the CONTIGUOUS
linear reading (the recurring-substring network of modules a02/a03), not in geometry.

Run: python extract_names.py
"""
import json
import os
import random
import re
import statistics

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")


def letters(s):
    return re.sub("[^A-Z]", "", s.upper())


def load_grids():
    T = json.load(open(os.path.join(DATA, "loagaeth_tables.json"), encoding="utf-8"))["leaves"]
    grids = {}
    for k, v in T.items():
        m = re.match(r"(\d+)a$", k)
        if not m:
            continue
        rows = [letters(r) for r in v if letters(r)]
        rows = [r for r in rows if len(r) >= 40][:49]
        if len(rows) >= 40:
            grids[int(m.group(1))] = rows
    return grids


def extract(g, cr, cc, L=7):
    def at(r, c):
        return g[r][c] if 0 <= r < len(g) and 0 <= c < len(g[r]) else ""
    up = "".join(at(cr - i, cc) for i in range(L))
    dn = "".join(at(cr + i, cc) for i in range(L))
    lf = "".join(at(cr, cc - i) for i in range(L))
    rt = "".join(at(cr, cc + i) for i in range(L))
    spiral = "".join([at(cr, cc), at(cr - 1, cc), at(cr - 1, cc + 1), at(cr, cc + 1),
                      at(cr + 1, cc + 1), at(cr + 1, cc), at(cr + 1, cc - 1), at(cr, cc - 1)])
    return [w for w in (up, dn, lf, rt, spiral) if len(w) >= 6]


def run():
    rng = random.Random(49)
    grids = load_grids()
    corpus = "".join("".join(g) for g in grids.values())
    LEX = set(json.load(open(os.path.join(DATA, "call_lexicon.json"), encoding="utf-8"))["attested_wordforms"])

    def score(cands):
        rec = sum(corpus.count(w) for w in cands)
        lx = sum(1 for w in cands if w[:5] in LEX or w in LEX)
        gram = sum(1 for w in cands if w and (w[0] in "GV" or w[-1] == "H"))
        return rec, lx, gram

    cen = [0, 0, 0]
    samples = []
    for n, g in grids.items():
        cr, cc = len(g) // 2, len(g[len(g) // 2]) // 2
        c = extract(g, cr, cc)
        r, l, gr = score(c)
        cen[0] += r
        cen[1] += l
        cen[2] += gr
        if len(samples) < 6:
            samples.append({"table": n, "center_names": c[:3]})

    def null_once():
        tot = [0, 0, 0]
        for n, g in grids.items():
            cr = rng.randint(6, len(g) - 7)
            w = len(g[cr])
            cc = rng.randint(6, w - 7) if w > 13 else w // 2
            r, l, gr = score(extract(g, cr, cc))
            tot[0] += r
            tot[1] += l
            tot[2] += gr
        return tot
    nulls = [null_once() for _ in range(200)]

    def zof(obs, arr):
        mu = statistics.mean(arr)
        sd = statistics.pstdev(arr) or 1
        return round((obs - mu) / sd, 1), round(mu, 1)

    labels = ["recurrence", "lexicon_hits", "grammar_fit"]
    stats = {}
    for i, lab in enumerate(labels):
        z, mu = zof(cen[i], [x[i] for x in nulls])
        stats[lab] = {"center": cen[i], "null_mean": mu, "z": z,
                      "verdict": "ABOVE chance" if z > 3 else "chance"}

    res = {
        "n_grids": len(grids),
        "sample_center_names": samples,
        "stats": stats,
        "conclusion": "NEGATIVE: Watchtower-style geometry does not extract a name-system "
                      "from the 49x49 Loagaeth. The names are in the contiguous linear reading "
                      "(see modules a02/a03), not in grid geometry.",
    }
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "results", "extract_names.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(run(), ensure_ascii=False, indent=1))
