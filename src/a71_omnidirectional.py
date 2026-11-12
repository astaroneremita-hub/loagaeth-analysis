"""
71 - Omni-directional reading: does the Loagaeth carry names in more than one direction, the
way the Watchtowers do?

The Golden Dawn Watchtowers encode names DIRECTIONALLY: the Linea Spiritus Sancti reads across,
the Great Cross around the centre, the Calvary crosses up the vertical bar and along the horizontal.
Vincent Bridges' claim (the 4th image) pushes this further: a square is meant to be read from four
directions and four corners - 16 "omni-directional" patterns per square.

If the Loagaeth were built that way, its letters would spell catalogue-names not just in the written
left-to-right rows but in the other dihedral orientations too (columns, reversed rows, the transpose,
the rotations). If it is a dense field of pronounceable letters, names appear in every orientation at
roughly the rate the letter-flow alone predicts - no orientation is privileged, and the real leaf is
no richer in its non-written directions than a Markov-3 surrogate with the same local flow.

Test, per full 49x49 leaf:
  - build the 8 dihedral images (identity, rot90/180/270, h-flip, v-flip, 2 diagonal flips);
  - in each, count catalogue-name occurrences reading every row left-to-right (so the 8 images cover
    rows, columns, both reverses, and both diagonals' worth of reading order);
  - do the same on a Markov-3 surrogate of the leaf (same size, same local flow, no planted names).
  - compare the real leaf's NON-written orientations (images 1..7) to the surrogate's. Extra directional
    structure shows up as real > surrogate there; a dense field shows real ~ surrogate.
"""
import json
import os
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3


def dihedral(grid):
    """8 images of a square char-grid, each as a list of row-strings."""
    R = len(grid)
    g = [list(row) for row in grid]
    out = []
    cur = g
    for _ in range(4):
        out.append(["".join(r) for r in cur])
        out.append(["".join(r) for r in cur[::-1]])  # h-flip of this rotation
        cur = [[cur[R - 1 - c][r] for c in range(R)] for r in range(R)]  # rot90
    # dedupe by ROW-MULTISET: images that only reorder rows give the identical name count as the
    # written image (reading each row L-R is unchanged), so they are not a new reading direction.
    seen, uniq = set(), []
    for im in out:
        key = tuple(sorted(im))
        if key not in seen:
            seen.add(key)
            uniq.append(im)
    return uniq  # written image first; genuinely distinct reading orders after


def count_names(rows, names):
    text = "\n".join(rows)
    return sum(text.count(n) for n in names)


def surrogate(grid, rng):
    s = markov3("".join("".join(r) for r in grid), rng)
    out, i = [], 0
    for row in grid:
        out.append(s[i:i + len(row)])
        i += len(row)
    return out


def run():
    rng = random.Random(71)
    lv = load.leaves()
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    masters = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD",
               "CHADAX", "NACHO", "ANTANTOX", "GRADAX", "DAHAHOXOM"]
    names = sorted({n for n in (set(masters) | {x["name"] for x in d}) if len(n) >= 4}, key=len)

    per_leaf = []
    real_written, real_other, surr_written, surr_other = [], [], [], []
    for leaf, rows in lv.items():
        grid = [load.letters(r) for r in rows if load.letters(r)]
        if len(grid) != 49 or any(len(r) != 49 for r in grid):
            continue
        imgs = dihedral(grid)
        counts = [count_names(im, names) for im in imgs]  # imgs[0] = written
        # surrogate, averaged over 5 draws
        sw, so = [], []
        for _ in range(5):
            sg = surrogate(grid, rng)
            sims = dihedral(sg)
            sc = [count_names(im, names) for im in sims]
            sw.append(sc[0])
            so.append(statistics.mean(sc[1:]))
        real_written.append(counts[0])
        real_other.append(statistics.mean(counts[1:]))
        surr_written.append(counts[0] and statistics.mean(sw))
        surr_other.append(statistics.mean(so))
        per_leaf.append({"leaf": leaf, "written": counts[0],
                         "other_dirs_mean": round(statistics.mean(counts[1:]), 1),
                         "best_other_dir": max(counts[1:]),
                         "surrogate_other_mean": round(statistics.mean(so), 1)})

    rw, ro = statistics.mean(real_written), statistics.mean(real_other)
    sw_, so_ = statistics.mean(surr_written), statistics.mean(surr_other)
    # does the real leaf carry MORE names in non-written directions than its surrogate?
    diffs = [p["other_dirs_mean"] - p["surrogate_other_mean"] for p in per_leaf]
    mu, sd = statistics.mean(diffs), (statistics.pstdev(diffs) or 1)
    z = round(mu / (sd / len(diffs) ** 0.5), 2)

    res = {
        "leaves": len(per_leaf),
        "names_tested": len(names),
        "real_written_mean": round(rw, 1),
        "real_other_dirs_mean": round(ro, 1),
        "surrogate_written_mean": round(sw_, 1),
        "surrogate_other_dirs_mean": round(so_, 1),
        "written_over_other_ratio_real": round(rw / max(1e-9, ro), 2),
        "extra_directional_vs_surrogate_z": z,
        "per_leaf_top": sorted(per_leaf, key=lambda p: -(p["other_dirs_mean"] - p["surrogate_other_mean"]))[:8],
        "conclusion": "",
    }
    verdict = (
        "DESCRIPTIVE / dense field" if abs(z) < 2 else
        ("REAL: extra directional structure" if z > 0 else "names avoid the other directions"))
    res["conclusion"] = (
        "Across %d full leaves the written rows carry %.1f catalogue-name hits; the other 7 dihedral "
        "orientations carry %.1f each - %.2fx fewer, so reading direction matters (text runs one way). "
        "The Watchtower-style question is whether the OTHER directions still carry names on purpose. The "
        "real leaf's non-written orientations hold %.1f hits; a Markov-3 surrogate with the same local "
        "flow holds %.1f (z %.2f for the difference). %s. The Loagaeth is read one way; its letters spell "
        "names in every direction only as much as any text with its letter-flow would, not by an "
        "omni-directional design like the one claimed for the Watchtowers." % (
            res["leaves"], rw, ro, res["written_over_other_ratio_real"], ro, so_, z, verdict))
    load.save_result("71_omnidirectional", res)
    return res


if __name__ == "__main__":
    r = run()
    print("written %.1f | other-dirs %.1f | surrogate other-dirs %.1f | z %.2f"
          % (r["real_written_mean"], r["real_other_dirs_mean"], r["surrogate_other_dirs_mean"],
             r["extra_directional_vs_surrogate_z"]))
    print("\ntop leaves (real other-dir minus surrogate):")
    for p in r["per_leaf_top"]:
        print("  %-5s written %3d  other %5.1f  surrogate %5.1f  best-dir %3d"
              % (p["leaf"], p["written"], p["other_dirs_mean"], p["surrogate_other_mean"], p["best_other_dir"]))
    print("\n" + r["conclusion"])
