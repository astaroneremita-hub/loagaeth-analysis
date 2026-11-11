"""
29 - Track C of the roadmap: architecture, deeper.

  C1) The two sides of a diamond table (29-43) are the two chessboard colours of one square. Are
      they two vocabularies, like the two currents of 25b-28b? Shared recurring 5-grams between all
      a-sides and all b-sides vs random splits of each table's lines into two halves.
  C2) Where does the language change fastest? A letter model of each side reads the next side;
      the jump between consecutive sides is compared with jumps between random pairs of sides.
  C3) Leaf 1 (Dee's spaced words) inside the tables: which of its words occur in the grids beyond
      a Markov-3 expectation, and where.
  C4) Particles: the short strings (1-3 letters) that sit between two names on the same line,
      compared with all short strings of the book.
"""
import json
import math
import os
import random
import statistics
from collections import Counter, defaultdict

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a23_name_discovery import M3

PART_OF = lambda t: "I" if t <= 12 else "II" if t <= 25 else "III" if t <= 33 else "IV" if t <= 40 else "V"


def grams(L, k=5):
    return Counter(g for r in L for g in (r[i:i + k] for i in range(len(r) - k + 1)))


def jac(a, b, mc=2):
    A = {g for g, c in a.items() if c >= mc}
    B = {g for g, c in b.items() if c >= mc}
    return len(A & B) / max(1, len(A | B))


def C1_diamond_sides(book, rng):
    A = [r for t in range(29, 44) for r in book.get(f"{t}a", [])]
    B = [r for t in range(29, 44) for r in book.get(f"{t}b", [])]
    j0 = jac(grams(A), grams(B))
    nul = []
    for _ in range(200):
        x, y = [], []
        for t in range(29, 44):
            L = book.get(f"{t}a", []) + book.get(f"{t}b", [])
            L = L[:]
            rng.shuffle(L)
            h = len(book.get(f"{t}a", []))
            x += L[:h]
            y += L[h:]
        nul.append(jac(grams(x), grams(y)))
    names = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ACLAX", "OXAD", "NACHO", "GRADAX"]
    per = {n: [sum(r.count(n) for r in A), sum(r.count(n) for r in B)] for n in names}
    return {"jaccard_a_vs_b": round(j0, 3), "random_split_mean": round(statistics.mean(nul), 3),
            "random_split_min": round(min(nul), 3), "random_split_max": round(max(nul), 3),
            "p_lower": round((sum(v <= j0 for v in nul) + 1) / 201, 4), "names_a_vs_b": per}


def C2_change_rate(book, rng):
    keys = sorted(book, key=lambda k: (tnum(k), k[-1]))
    models = {}
    for k in keys:
        m = CharLM(2, alpha=0.5)
        m.fit(book[k])
        models[k] = m
    self_bits = {k: models[k].bits(book[k]) for k in keys}

    def d(a, b):
        return 0.5 * ((models[a].bits(book[b]) - self_bits[b]) + (models[b].bits(book[a]) - self_bits[a]))
    steps = [{"step": f"{keys[i]}→{keys[i+1]}", "distance": round(d(keys[i], keys[i + 1]), 3)} for i in range(len(keys) - 1)]
    rnd = []
    for _ in range(300):
        a, b = rng.sample(keys, 2)
        rnd.append(d(a, b))
    rnd.sort()
    mean_step = statistics.mean(s["distance"] for s in steps)
    top = sorted(steps, key=lambda s: -s["distance"])[:10]
    return {"mean_consecutive_distance": round(mean_step, 3), "random_pair_mean": round(statistics.mean(rnd), 3),
            "random_pair_95": round(rnd[int(0.95 * len(rnd))], 3), "largest_steps": top,
            "steps": steps}


def C3_leaf1(book):
    import a21_index_heptarchy_numbers as a21
    lv = load.leaves()
    words = Counter(t for leaf in ["1a", "1b"] for r in lv[leaf] if len(r.split()) > 1 for t in a21.wtoks(r))
    words = [w for w in words if len(w) >= 5]
    lines = [r for v in book.values() for r in v]
    m3 = M3(lines)
    npos = sum(len(r) for r in lines)
    S = "|".join(lines)
    obs = {w: S.count(w) for w in words}
    exp = {w: m3.expected(w, npos) for w in words}
    found = {w: c for w, c in obs.items() if c}
    strong = sorted(((w, obs[w], round(exp[w], 2)) for w in words if obs[w] >= 3 and obs[w] > 3 * max(exp[w], 0.3)),
                    key=lambda x: -x[1])
    byt = defaultdict(list)
    for k, v in book.items():
        byt[tnum(k)] += v
    part = Counter()
    for w, c, e in strong:
        for t, L in byt.items():
            part[PART_OF(t)] += "|".join(L).count(w)
    return {"leaf1_words_5plus": len(words), "found_in_tables": len(found),
            "total_occurrences": sum(obs.values()), "markov3_expected_total": round(sum(exp.values()), 1),
            "strong_words": strong[:25], "strong_words_by_part": dict(part)}


def C4_particles(book):
    names = ["NOCHASTOR", "CHASTOR", "CHUSTOR", "ADNOCHA", "NOCHA", "ANZACH", "ALGETH", "GETH",
             "ACLAX", "CHADAX", "OXAD", "NACHO", "GRADAX", "AXALGRA", "PHANGE", "VOXAR"]
    p = os.path.join(load.RESULTS, "23_name_discovery.json")
    if os.path.exists(p):
        names += [c["name"] for c in json.load(open(p, encoding="utf-8"))["A_candidates"]["top"]]
    names = sorted(set(names), key=len, reverse=True)
    gaps, allshort, gaplen = Counter(), Counter(), Counter()
    for v in book.values():
        for r in v:
            spans = []
            occ = [False] * len(r)
            for n in names:
                st = 0
                while True:
                    i = r.find(n, st)
                    if i < 0:
                        break
                    if not any(occ[i:i + len(n)]):
                        spans.append((i, i + len(n)))
                        for j in range(i, i + len(n)):
                            occ[j] = True
                    st = i + 1
            spans.sort()
            for (a, b), (c, d) in zip(spans, spans[1:]):
                gaplen[min(c - b, 12)] += 1
                if 1 <= c - b <= 3:
                    gaps[r[b:c]] += 1
            for k in (1, 2, 3):
                allshort.update(r[i:i + k] for i in range(len(r) - k + 1))
    tot_g = sum(gaps.values())
    out = []
    for g, c in gaps.most_common(40):
        base = allshort[g] / sum(v for k, v in allshort.items() if len(k) == len(g))
        out.append({"particle": g, "between_names": c, "share": round(c / tot_g, 3),
                    "x_vs_book": round((c / sum(v for k, v in gaps.items() if len(k) == len(g))) / base, 2)})
    return {"name_pairs_with_short_gap": tot_g, "gap_length_between_consecutive_names": dict(sorted(gaplen.items())),
            "top": out[:20]}


def run():
    rng = random.Random(29)
    book = base_book()
    res = {"C1_diamond_sides": C1_diamond_sides(book, rng),
           "C2_change_rate": C2_change_rate(book, rng),
           "C3_leaf1_in_tables": C3_leaf1(book),
           "C4_particles": C4_particles(book)}
    load.save_result("29_architecture_deep", res)
    return res


if __name__ == "__main__":
    r = run()
    r["C2_change_rate"].pop("steps")
    print(json.dumps(r, ensure_ascii=False, indent=1))
