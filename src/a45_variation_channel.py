"""
45 - Is the choice of a letter a channel? What decides which variant is written.

The book repeats passages with one letter changed (a40). Take every frame - three letters, one slot,
three letters - that occurs at least 12 times in the row-written tables (2-24) with two or more
fillers of at least 4 occurrences each (ADN_CHA takes O, A or E). For each occurrence we know which
filler was written. Does that choice depend on anything?

  part of the book                      (fillers permuted freely)
  table, inside the part                (permuted inside each part)
  side a or b, inside the table         (permuted inside each table)
  row third, column third               (permuted inside each side)
  the nearest vowel before / after the frame   (permuted inside each side) - vowel harmony at a distance
  the filler chosen the previous time the same frame was written on that side (agreement rate)

Statistic: mutual information between filler and feature, summed over frames (bits x occurrences),
against 300 permutations that keep everything else in place.
"""
import json
import math
import random
import statistics
from collections import Counter, defaultdict

import load
from a22_robustness_and_depth import base_book, tnum
from a42_repeat_map import part

VOW = set("AEIOUY")


def collect(book):
    occ = defaultdict(list)
    for k in sorted(book, key=lambda k: (tnum(k), k)):
        if not 2 <= tnum(k) <= 24:
            continue
        rows = [r for r in book[k] if r]
        for ri, r in enumerate(rows):
            for i in range(3, len(r) - 3):
                lv = next((c for c in reversed(r[max(0, i - 9):i - 3]) if c in VOW), "-")
                rv = next((c for c in r[i + 4:i + 10] if c in VOW), "-")
                occ[(r[i - 3:i], r[i + 1:i + 4])].append(
                    {"f": r[i], "face": k, "table": tnum(k), "part": part(k), "side": k[-1],
                     "row": min(2, 3 * ri // max(1, len(rows))), "col": min(2, 3 * i // max(1, len(r))), "lv": lv, "rv": rv,
                     "ord": (ri, i)})
    frames = {}
    for fr, xs in occ.items():
        c = Counter(x["f"] for x in xs)
        keep = {f for f, n in c.items() if n >= 4}
        if len(keep) >= 2:
            xs = [x for x in xs if x["f"] in keep]
            if len(xs) >= 12:
                frames[fr] = xs
    for xs in frames.values():  # previous filler of the same frame on the same side
        last = {}
        for x in sorted(xs, key=lambda x: (x["table"], x["face"], x["ord"])):
            x["prev"] = last.get(x["face"], "-")
            last[x["face"]] = x["f"]
    return frames


def nmi(pairs):
    n = len(pairs)
    ab, a, b = Counter(pairs), Counter(p[0] for p in pairs), Counter(p[1] for p in pairs)
    return sum(v * math.log2(v * n / (a[x] * b[y])) for (x, y), v in ab.items())


def test(frames, feat, stratum, rng, reps=300):
    def total(perm):
        t = 0.0
        for xs in frames.values():
            fs = [x["f"] for x in xs]
            if perm:
                groups = defaultdict(list)
                for j, x in enumerate(xs):
                    groups[x[stratum] if stratum else 0].append(j)
                fs2 = fs[:]
                for js in groups.values():
                    vals = [fs[j] for j in js]
                    rng.shuffle(vals)
                    for j, v in zip(js, vals):
                        fs2[j] = v
                fs = fs2
            t += nmi([(f, x[feat]) for f, x in zip(fs, xs)])
        return t
    obs = total(False)
    nul = [total(True) for _ in range(reps)]
    n = sum(len(xs) for xs in frames.values())
    return {"bits_per_occurrence": round(obs / n, 4), "permuted": round(statistics.mean(nul) / n, 4),
            "z": round((obs - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
            "p": round((sum(v >= obs for v in nul) + 1) / (reps + 1), 4)}


def persistence(frames, rng, reps=1000):
    """Same filler as the previous time the frame was written on that side, against the side's
    fillers in random order. (Mutual information is misleading here: 'no previous' is a category.)"""
    seqs = []
    for xs in frames.values():
        g = defaultdict(list)
        for x in sorted(xs, key=lambda x: x["ord"]):
            g[x["face"]].append(x["f"])
        seqs += [v for v in g.values() if len(set(v)) >= 2]
    agree = lambda S: sum(a == b for s in S for a, b in zip(s, s[1:]))
    obs = agree(seqs)
    nul = []
    for _ in range(reps):
        sh = []
        for s in seqs:
            t = s[:]
            rng.shuffle(t)
            sh.append(t)
        nul.append(agree(sh))
    return {"pairs": sum(len(s) - 1 for s in seqs), "same_as_previous": obs, "random_order": round(statistics.mean(nul), 1),
            "z": round((obs - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
            "p": round((sum(v >= obs for v in nul) + 1) / (reps + 1), 4)}


def run():
    rng = random.Random(45)
    frames = collect(base_book())
    n = sum(len(xs) for xs in frames.values())
    tests = [("part of the book", "part", None), ("table inside the part", "table", "part"), ("side a/b inside the table", "side", "table"),
             ("row third inside the side", "row", "face"), ("column third inside the side", "col", "face"),
             ("nearest vowel before the frame", "lv", "face"), ("nearest vowel after the frame", "rv", "face")]
    res = {"frames": len(frames), "occurrences": n,
           "largest_frames": [{"frame": a + "_" + b, "fillers": dict(Counter(x["f"] for x in xs).most_common())}
                              for (a, b), xs in sorted(frames.items(), key=lambda kv: -len(kv[1]))[:10]],
           "what_the_choice_depends_on": {name: test(frames, feat, st, rng) for name, feat, st in tests},
           "same_choice_as_last_time": persistence(frames, rng)}
    load.save_result("45_variation_channel", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["frames"], r["occurrences"])
    for x in r["largest_frames"]:
        print("  ", x)
    for k, v in r["what_the_choice_depends_on"].items():
        print("  ", k, v)
