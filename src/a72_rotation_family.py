"""
72 - The rotation-family: are a name and its rotations "stuck together" (grudados) beyond letter-flow?

Murilo's reading: in Enochian each rotation / branch of a name is the SAME entity with different
powers. If that is written into the Loagaeth, the rotations of a name (OXAD -> XADO -> ADOX -> DOXA)
should cluster TOGETHER on a leaf - closer than unrelated fragments - not scatter independently.

Statistics cannot touch the metaphysical claim ("same entity"). But it CAN test the physical
consequence he keeps pointing at: the branches sit glued together. The honest null is a Markov-3
surrogate of the SAME leaf (same local letter-flow) carrying the SAME rotation-family: rotations share
letters, so they co-locate somewhat in any such text; if the real leaf glues them TIGHTER than the
surrogate does, that is structure beyond letter-flow - evidence for his reading. If real ~ surrogate,
the gluing is just the shared letters.

Per busy leaf and master name:
  - positions (row, col of each occurrence start) of the name and all its distinct cyclic rotations,
    read in the written rows (both L-R and R-L, since a rotation may be written either way);
  - mean nearest-neighbour distance among those positions (tight = glued);
  - same on 8 Markov-3 surrogates of the leaf. Real NN-distance below surrogate = glued beyond flow.
"""
import json
import os
import random
import statistics

import load
from a19_machine import markov3


def rotations(name):
    rots = {name[i:] + name[:i] for i in range(len(name))}
    rots |= {r[::-1] for r in list(rots)}  # a branch may be written either way
    return sorted(rots)


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
    rng = random.Random(72)
    lv = load.leaves()
    masters = ["OXAD", "CHASTOR", "NOCHA", "GETH", "ACLAX", "ANZACH", "CHADAX", "GRADAX", "NACHO", "ALGETH"]
    grids = {}
    for leaf, rows in lv.items():
        g = [load.letters(r) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            grids[leaf] = g

    rows_out = []
    for nm in masters:
        frags = rotations(nm)
        # pick the leaf where the family is busiest
        busiest, bg, bpos = None, None, None
        for leaf, g in grids.items():
            p = positions(g, frags)
            if busiest is None or len(p) > len(bpos):
                busiest, bg, bpos = leaf, g, p
        if len(bpos) < 4:
            continue
        real = mean_nn(bpos)
        sur = []
        for _ in range(8):
            sg = surrogate(bg, rng)
            sp = positions(sg, frags)
            m = mean_nn(sp)
            if m is not None and len(sp) >= 2:
                sur.append(m)
        if not sur:
            continue
        mu, sd = statistics.mean(sur), (statistics.pstdev(sur) or 1)
        rows_out.append({
            "name": nm, "rotations": len(frags), "busiest_leaf": busiest,
            "occurrences": len(bpos), "real_nn_distance": round(real, 2),
            "surrogate_nn_mean": round(mu, 2), "z": round((real - mu) / sd, 2)})

    zs = [r["z"] for r in rows_out]
    mean_z = round(statistics.mean(zs), 2) if zs else None
    glued = sum(1 for r in rows_out if r["z"] < -1)  # negative z = tighter than surrogate
    res = {
        "names": len(rows_out),
        "glued_tighter_than_surrogate": glued,
        "mean_z": mean_z,
        "note": "z < 0 means the family is glued TIGHTER than a same-flow surrogate (supports the "
                "one-entity reading); z ~ 0 means the gluing is just the shared letters.",
        "per_name": sorted(rows_out, key=lambda r: r["z"]),
        "conclusion": "",
    }
    if mean_z is not None:
        if mean_z < -1:
            verdict = ("CONFIRMADO NOVO: the rotation-families really do sit glued tighter than their "
                       "letter-flow predicts - the branches of a name cluster on the leaf beyond chance.")
        elif mean_z > 1:
            verdict = "the rotations sit FARTHER apart than flow predicts - they avoid each other."
        else:
            verdict = ("DESCRIPTIVE: the families cluster exactly as much as their shared letters force, "
                       "no tighter - the gluing he sees is real on the page but not placed beyond letter-flow.")
        res["conclusion"] = (
            "%d names tested; the rotation-family is glued tighter than its surrogate for %d of them. "
            "Mean z = %.2f. %s" % (len(rows_out), glued, mean_z, verdict))
    load.save_result("72_rotation_family", res)
    return res


if __name__ == "__main__":
    r = run()
    print("name      rots  leaf   occ   real_nn  surr_nn   z")
    for x in r["per_name"]:
        print("  %-8s %3d  %-5s %4d  %7.2f  %7.2f  %6.2f" % (
            x["name"], x["rotations"], x["busiest_leaf"], x["occurrences"],
            x["real_nn_distance"], x["surrogate_nn_mean"], x["z"]))
    print("\n" + r["conclusion"])
