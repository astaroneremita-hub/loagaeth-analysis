"""
73 - Massive sweep: which rotation-families are glued beyond letter-flow, across the WHOLE book?

a72 found one family (CHADAX) glued far tighter than its surrogate. Is that a fluke, or a real
sub-population of deliberately-placed names inside the dense field? Only a massive sweep answers it.

Method:
  - Seeds: every 4- and 5-gram that occurs >= a threshold in the book (hundreds of recurring chunks),
    deduped so each rotation-family is tested once (canonical = lexicographically-smallest rotation).
  - For each family: positions of all its cyclic rotations (both writings) across every full 49x49 leaf;
    take the busiest leaf (need >= MINOCC occurrences); mean nearest-neighbour distance = how glued.
  - Null: 24 Markov-3 surrogates of that leaf (cached per leaf, same local flow), same family, same NN.
    z = (real - surrogate_mean)/surrogate_sd. z < 0 = glued tighter than flow.
  - Count families at z < -2, -2.5, -3 and compare to the false-positive rate a one-tailed normal gives
    (0.023, 0.006, 0.0013 of N). A real sub-population shows a big EXCESS over those counts.
"""
import json
import os
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3

MINOCC = 6
NSURR = 24


def rotations(name):
    rots = {name[i:] + name[:i] for i in range(len(name))}
    rots |= {r[::-1] for r in list(rots)}
    return sorted(rots)


def canon(name):
    return min(name[i:] + name[:i] for i in range(len(name)))


def positions(grid, frags):
    pos = []
    for r, row in enumerate(grid):
        for frag in frags:
            start = 0
            while True:
                i = row.find(frag, start)
                if i < 0:
                    break
                pos.append((r, i + len(frag) / 2.0))
                start = i + 1
    return pos


def mean_nn(pos):
    if len(pos) < 2:
        return None
    tot = 0.0
    for i, a in enumerate(pos):
        best = min(((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) ** 0.5
                   for j, b in enumerate(pos) if j != i)
        tot += best
    return tot / len(pos)


def surrogate(grid, rng):
    s = markov3("".join(grid), rng)
    out, i = [], 0
    for row in grid:
        out.append(s[i:i + len(row)])
        i += len(row)
    return out


def run():
    rng = random.Random(73)
    lv = load.leaves()
    grids = {}
    for leaf, rows in lv.items():
        g = [load.letters(r) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            grids[leaf] = g
    alltext = "".join("".join(g) for g in grids.values())

    # seeds: recurring 4- and 5-grams
    seeds = set()
    for L, thr in ((4, 12), (5, 7)):
        c = Counter(alltext[i:i + L] for i in range(len(alltext) - L + 1))
        for frag, n in c.items():
            if n >= thr and len(set(frag)) >= 2:
                seeds.add(canon(frag))
    seeds = sorted(seeds)

    # cache surrogates per leaf (24 each), built lazily
    surr_cache = {}

    rows_out = []
    for sd in seeds:
        frags = rotations(sd)
        busiest, bg, bpos = None, None, []
        for leaf, g in grids.items():
            p = positions(g, frags)
            if len(p) > len(bpos):
                busiest, bg, bpos = leaf, g, p
        if len(bpos) < MINOCC:
            continue
        real = mean_nn(bpos)
        if busiest not in surr_cache:
            surr_cache[busiest] = [surrogate(bg, rng) for _ in range(NSURR)]
        sur = []
        for sg in surr_cache[busiest]:
            m = mean_nn(positions(sg, frags))
            if m is not None:
                sur.append(m)
        if len(sur) < 5:
            continue
        mu, sd_ = statistics.mean(sur), (statistics.pstdev(sur) or 1e-9)
        z = (real - mu) / sd_
        rows_out.append({"family": sd, "leaf": busiest, "occ": len(bpos),
                         "real_nn": round(real, 2), "surr_nn": round(mu, 2), "z": round(z, 2)})

    N = len(rows_out)
    glued = sorted(rows_out, key=lambda r: r["z"])
    c2 = sum(1 for r in rows_out if r["z"] < -2)
    c25 = sum(1 for r in rows_out if r["z"] < -2.5)
    c3 = sum(1 for r in rows_out if r["z"] < -3)
    exp2, exp25, exp3 = round(0.0228 * N, 1), round(0.0062 * N, 1), round(0.00135 * N, 1)
    res = {
        "families_tested": N,
        "minocc": MINOCC, "surrogates_per_leaf": NSURR,
        "glued_z_lt_-2": {"observed": c2, "expected_by_chance": exp2, "excess": round(c2 - exp2, 1)},
        "glued_z_lt_-2.5": {"observed": c25, "expected_by_chance": exp25, "excess": round(c25 - exp25, 1)},
        "glued_z_lt_-3": {"observed": c3, "expected_by_chance": exp3, "excess": round(c3 - exp3, 1)},
        "scattered_z_gt_+2": sum(1 for r in rows_out if r["z"] > 2),
        "mean_z": round(statistics.mean(r["z"] for r in rows_out), 3),
        "top_glued": glued[:30],
        "conclusion": "",
    }
    excess = c2 - exp2
    if c2 > 2 * exp2 and excess > 8:
        verdict = ("CONFIRMADO NOVO: a real sub-population of rotation-families sits glued far beyond "
                   "letter-flow - %d families at z<-2 against ~%.0f expected by chance. The book places "
                   "SOME name-families deliberately tight while the rest is dense field." % (c2, exp2))
    elif c2 > 1.5 * exp2:
        verdict = ("a mild excess of glued families (%d vs ~%.0f expected) - a lead, not yet decisive; "
                   "re-test the top ones with more surrogates and a second metric." % (c2, exp2))
    else:
        verdict = ("no excess (%d glued vs ~%.0f expected by chance) - CHADAX was a tail event, not a "
                   "sub-population. The gluing is letter-flow across the board." % (c2, exp2))
    res["conclusion"] = ("%d families tested. Mean z %.2f (0 = flat). z<-2: %d obs / %.0f chance. "
                         "z<-3: %d obs / %.1f chance. %s"
                         % (N, res["mean_z"], c2, exp2, c3, exp3, verdict))
    load.save_result("73_family_sweep", res)
    return res


if __name__ == "__main__":
    r = run()
    print("tested %d | mean z %.2f | z<-2 %d (chance %.0f) | z<-2.5 %d (%.0f) | z<-3 %d (%.1f) | scattered %d"
          % (r["families_tested"], r["mean_z"], r["glued_z_lt_-2"]["observed"], r["glued_z_lt_-2"]["expected_by_chance"],
             r["glued_z_lt_-2.5"]["observed"], r["glued_z_lt_-2.5"]["expected_by_chance"],
             r["glued_z_lt_-3"]["observed"], r["glued_z_lt_-3"]["expected_by_chance"], r["scattered_z_gt_+2"]))
    print("\ntop glued families:")
    for x in r["top_glued"]:
        print("  %-8s %-5s occ%3d  real %5.2f  surr %5.2f  z %6.2f" % (
            x["family"], x["leaf"], x["occ"], x["real_nn"], x["surr_nn"], x["z"]))
    print("\n" + r["conclusion"])
