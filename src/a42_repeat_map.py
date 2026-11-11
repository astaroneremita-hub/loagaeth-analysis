"""
42 - Where the repeated passages are: sister sides, distance, drift of spelling, compounds.

  A) Sister sides. Which pairs of sides share strings of 12 letters? Distance in tables between the
     two occurrences, share falling on the two sides of one leaf, against sides relabelled inside
     their own part of the book (so the known dialects of the parts are kept).
  B) Pairs of sides that share far more than their sizes predict.
  C) Drift. In passages that recur with one letter changed (a40), does one letter belong to the
     earlier side and the other to the later? (A spelling that moves as the book goes on.)
  D) Compounds: every pair of names written together at least 3 times, against names shuffled
     inside each side; which names lead and which follow.
"""
import json
import math
import random
import statistics
from collections import Counter, defaultdict

import load
from a22_robustness_and_depth import base_book, tnum
from a39_long_repeats import surrogate3
from a40_formulas import name_list


def part(k):
    t, b = tnum(k), k.endswith("b")
    if t <= 1:
        return 0
    if t <= 12:
        return 1
    if t < 25 or (t == 25 and not b):
        return 2
    if t < 33 or (t == 33 and not b):
        return 3
    if t <= 40:
        return 4
    return 5


def A_sisters(book, keys, rng, L=12):
    occ = defaultdict(set)
    for k in keys:
        for r in book[k]:
            for i in range(len(r) - L + 1):
                occ[r[i:i + L]].add(k)
    pair = Counter()
    for s, fs in occ.items():
        fs = sorted(fs, key=keys.index)
        for i, a in enumerate(fs):
            for b in fs[i + 1:]:
                pair[(a, b)] += 1
    # collapse overlapping windows: one long shared passage gives many 12-grams; count pairs of sides, weight 1
    links = list(pair)

    def stats(mapping):
        d = [abs(tnum(mapping[a]) - tnum(mapping[b])) for a, b in links]
        return (statistics.mean(d), sum(x == 0 for x in d) / len(d), sum(x <= 1 for x in d) / len(d),
                sum(part(mapping[a]) == part(mapping[b]) for a, b in links) / len(d))
    real = stats({k: k for k in keys})
    byp = defaultdict(list)
    for k in keys:
        byp[part(k)].append(k)
    nul = []
    for _ in range(1000):
        m = {}
        for p, ks in byp.items():
            sh = ks[:]
            rng.shuffle(sh)
            m.update(zip(ks, sh))
        nul.append(stats(m))
    allk = keys[:]
    nul_part = []
    for _ in range(1000):
        sh = allk[:]
        rng.shuffle(sh)
        m = dict(zip(allk, sh))
        nul_part.append(sum(part(m[a]) == part(m[b]) for a, b in links) / len(links))
    names = ["mean_distance_in_tables", "share_same_leaf", "share_within_one_table"]
    out = {"pairs_of_sides_sharing_a_12_letter_string": len(links)}
    for i, n in enumerate(names):
        xs = [v[i] for v in nul]
        lo = sum(x <= real[i] for x in xs) / len(xs)
        out[n] = {"book": round(real[i], 3), "relabelled_inside_parts": round(statistics.mean(xs), 3),
                  "p": round(min(lo, 1 - lo + 1 / len(xs)), 4)}
    out["share_inside_one_part"] = {"book": round(real[3], 3), "relabelled_anywhere": round(statistics.mean(nul_part), 3),
                                    "p": round(sum(x >= real[3] for x in nul_part) / len(nul_part), 4)}
    hist = Counter(min(abs(tnum(a) - tnum(b)), 12) for a, b in links)
    out["distance_histogram_0_to_12plus"] = [hist.get(i, 0) for i in range(13)]
    # B: surprising pairs (configuration model)
    deg = Counter()
    for (a, b), n in pair.items():
        deg[a] += n
        deg[b] += n
    S = sum(pair.values())
    top = []
    for (a, b), n in pair.items():
        e = deg[a] * deg[b] / (2 * S)
        if n >= 8:
            top.append({"sides": a + " – " + b, "shared_12_letter_strings": n, "expected": round(e, 1), "ratio": round(n / e, 1)})
    top.sort(key=lambda x: -x["shared_12_letter_strings"])
    return out, top[:15]


def C_drift(book, keys):
    lines, face = [], []
    for k in keys:
        for r in book[k]:
            if r:
                lines.append(r)
                face.append(k)
    idx = defaultdict(list)
    for li, r in enumerate(lines):
        for i in range(len(r) - 13):
            idx[(0, r[i:i + 7])].append((li, i))
            idx[(1, r[i + 7:i + 14])].append((li, i))
    subs = {}
    for v in idx.values():
        if len(v) < 2 or len(v) > 200:
            continue
        for x in range(len(v)):
            la, ia = v[x]
            for y in range(x + 1, len(v)):
                lb, ib = v[y]
                if face[la] == face[lb]:
                    continue
                A, B = lines[la][ia:ia + 14], lines[lb][ib:ib + 14]
                d = [j for j in range(14) if A[j] != B[j]]
                if len(d) == 1 and 3 <= d[0] <= 10:
                    j = d[0]
                    (l1, i1, c1), (l2, i2, c2) = sorted([(la, ia + j, A[j]), (lb, ib + j, B[j])])
                    subs[(l1, i1, l2, i2)] = (c1, c2, face[l1], face[l2])
    c = Counter((a, b) for a, b, _, _ in subs.values())
    out = []
    seen = set()
    for (a, b), n in c.most_common():
        key = tuple(sorted((a, b)))
        if key in seen:
            continue
        seen.add(key)
        m = c.get((b, a), 0)
        tot = n + m
        if tot < 6:
            continue
        p = min(1.0, 2 * sum(math.comb(tot, i) for i in range(max(n, m), tot + 1)) / 2 ** tot)
        out.append({"earlier_then_later": a + " then " + b, "count": n, "opposite": m, "p_two_sided": round(p, 3)})
    same_part = sum(part(f1) == part(f2) for _, _, f1, f2 in subs.values()) / max(1, len(subs))
    bypart = Counter((part(f1), part(f2)) for _, _, f1, f2 in subs.values())
    return {"variants_between_different_sides": len(subs), "share_inside_one_part": round(same_part, 3),
            "by_parts": {f"{a}-{b}": n for (a, b), n in sorted(bypart.items())}, "direction_tests": out,
            "tests": len(out)}


def D_compounds(book, names, rng):
    """Two names written together. The null is the Markov-3 surrogate, searched for the same string:
    a shuffle of names is misled by names that overlap (OXAD + NOCHA is also OX + ADNOCHA)."""
    lines = [r for v in book.values() for r in v if r]
    S = "|".join(lines)
    sur = ["|".join(surrogate3(lines, rng)) for _ in range(20)]
    cand = [(a, b) for a in names for b in names if a != b and a[-1] != b[0] and S.count(a + b) >= 3
            and not any(a + b in n for n in names)]
    out = []
    for a, b in cand:
        n = S.count(a + b)
        xs = [t.count(a + b) for t in sur]
        mu = max(statistics.mean(xs), 0.05)
        pv = 1 - sum(math.exp(-mu) * mu ** i / math.factorial(i) for i in range(n))
        out.append({"compound": a + b, "parts": a + " + " + b, "count": n, "reverse": S.count(b + a),
                    "markov3_mean": round(statistics.mean(xs), 2), "p_poisson": float("%.2g" % pv),
                    "survives_bonferroni": pv * len(cand) < 0.05})
    out.sort(key=lambda x: x["p_poisson"])
    return {"candidates": len(cand), "survivors": sum(x["survives_bonferroni"] for x in out), "compounds": out[:20],
            "overlap_check": {"OXADNOCH": [S.count("OXADNOCH"), round(statistics.mean(t.count("OXADNOCH") for t in sur), 1)],
                              "GETHACLAX": [S.count("GETHACLAX"), round(statistics.mean(t.count("GETHACLAX") for t in sur), 1)]}}


def run():
    rng = random.Random(42)
    book = base_book()
    keys = sorted(book, key=lambda k: (tnum(k), k))
    A, B = A_sisters(book, keys, rng)
    res = {"A_sister_sides": A, "B_surprising_pairs": B, "C_drift_of_spelling": C_drift(book, keys),
           "D_compounds": D_compounds(book, name_list(), rng)}
    load.save_result("42_repeat_map", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
