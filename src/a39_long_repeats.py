"""
39 - Long repeats and phrases (a lead raised in discussion of this study).

  A) How many distinct strings of length L occur at least twice in the book (inside one line, never
     across a line end)? Compared with Markov-3 and order-5 surrogates of the same line lengths.
  B) The longest repeats, where they occur, and how they split into the names found by module a23.
  C) Are there phrases? Cut every line into names (longest known name first). Where one name is
     followed directly by another, is the choice of the second tied to the first (mutual
     information of adjacent names) more than when the same names are shuffled inside each side?
     And is the order fixed (A then B without B then A)?
"""
import json
import math
import os
import random
import statistics
from collections import Counter

import load
from a19_machine import CharLM, markov3
from a22_robustness_and_depth import base_book

MASTERS = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"]


def repeats(lines, L):
    c = Counter(r[i:i + L] for r in lines for i in range(len(r) - L + 1))
    return {k: v for k, v in c.items() if v > 1}


def surrogate3(lines, rng):
    s = markov3("".join(lines), rng)
    out, i = [], 0
    for r in lines:
        out.append(s[i:i + len(r)])
        i += len(r)
    return out


def tokens(line, names):
    out, i = [], 0
    while i < len(line):
        for n in names:
            if line.startswith(n, i):
                out.append((i, n))
                i += len(n)
                break
        else:
            i += 1
    return out


def adj_pairs(seq):
    return [(a[1], b[1]) for a, b in zip(seq, seq[1:]) if a[0] + len(a[1]) == b[0]]


def mi(pairs):
    n = len(pairs)
    if not n:
        return 0.0
    ab, a, b = Counter(pairs), Counter(p[0] for p in pairs), Counter(p[1] for p in pairs)
    return sum(v / n * math.log2(v * n / (a[x] * b[y])) for (x, y), v in ab.items())


def run():
    rng = random.Random(39)
    book = base_book()
    lines = [r for v in book.values() for r in v if r]
    where = {}
    for k, v in book.items():
        for r in v:
            where.setdefault(r, k)

    # A
    m5 = CharLM(5, alpha=0.05).fit(lines)
    sur3 = [surrogate3(lines, rng) for _ in range(5)]
    sur5 = [[m5.sample(len(r), rng) for r in lines] for _ in range(3)]
    A = {}
    for L in (8, 10, 12, 14, 16, 20):
        A[L] = {"book": len(repeats(lines, L)),
                "markov3_mean": round(statistics.mean(len(repeats(s, L)) for s in sur3), 1),
                "order5_mean": round(statistics.mean(len(repeats(s, L)) for s in sur5), 1)}

    # B: maximal repeats of 12+
    names = sorted(set(MASTERS) | {x["name"] for x in json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]}, key=len, reverse=True) \
        if hasattr(load, "RESULTS") else sorted(MASTERS, key=len, reverse=True)
    found = {}
    for L in range(30, 11, -1):
        for s, n in repeats(lines, L).items():
            if not any(s in t for t in found):
                found[s] = n
    longest = []
    for s, n in sorted(found.items(), key=lambda x: (-len(x[0]), -x[1]))[:25]:
        faces = sorted({k for k, v in book.items() if any(s in r for r in v)})
        longest.append({"string": s, "length": len(s), "count": n, "faces": faces[:8],
                        "names_inside": [t[1] for t in tokens(s, names)]})
    covered = sum(1 for s in found if len(tokens(s, names)) >= 2)

    # C
    by_face = {k: [tokens(r, names) for r in v if r] for k, v in book.items()}
    real = [p for v in by_face.values() for seq in v for p in adj_pairs(seq)]
    obs = mi(real)
    nul = []
    for _ in range(300):
        sh = []
        for v in by_face.values():
            pool = [t[1] for seq in v for t in seq]
            rng.shuffle(pool)
            i = 0
            for seq in v:
                new = [(t[0], pool[i + j]) for j, t in enumerate(seq)]
                i += len(seq)
                # adjacency pattern kept from the real line (positions), names swapped
                sh += [(a[1], b[1]) for (a, b), (x, y) in zip(zip(new, new[1:]), zip(seq, seq[1:])) if x[0] + len(x[1]) == y[0]]
        nul.append(mi(sh))
    c = Counter(real)
    top = [{"pair": a + " + " + b, "count": n, "reverse_count": c.get((b, a), 0)} for (a, b), n in c.most_common(15)]
    asym = sum(abs(n - c.get((b, a), 0)) for (a, b), n in c.items() if a < b or (b, a) not in c) / max(1, len(real))
    res = {"A_repeated_strings_by_length": A,
           "B_longest_repeats": longest,
           "B_maximal_repeats_12plus": len(found), "B_of_which_hold_two_or_more_names": covered,
           "C_adjacent_name_pairs": len(real),
           "C_mutual_information_bits": round(obs, 3),
           "C_shuffled_mean_max": [round(statistics.mean(nul), 3), round(max(nul), 3)],
           "C_p": round(sum(v >= obs for v in nul) / len(nul), 4),
           "C_order_asymmetry": round(asym, 3),
           "C_top_pairs": top}
    load.save_result("39_long_repeats", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
