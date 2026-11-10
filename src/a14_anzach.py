"""
14 - ANZACH, the second great stem, profiled like CHASTOR and compared with it.

  A) Profile: occurrences, reach, left/right context entropy (head-stem vs closing element),
     top preceding/following strings, title-nesting (HANZACH, NOCHANZACH, ADNOCHANZACH).
  B) Vowel twins (HONZACH, HENZACH...) - reported, but vowel alternation is language-wide (a12).
  C) Territory vs CHASTOR: per-table counts, Pearson r against frequency-matched random
     strings (tables differ in density, so raw correlation must be compared to a null).
  D) Ordering: in tables holding both, does ANZACH precede or follow CHASTOR more than chance?
  E) Leaf 1 (the prophecy): forms carrying the stem.

Data: data/loagaeth_tables.json.
"""
import json
import math
import random
import statistics
from collections import Counter

import load


def positions(s, sub):
    out, i = [], s.find(sub)
    while i >= 0:
        out.append(i)
        i = s.find(sub, i + 1)
    return out


def entropy(c):
    t = sum(c.values()) or 1
    return -sum(v / t * math.log2(v / t) for v in c.values() if v)


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else 0.0


def profile(stem, tabs, S):
    P = positions(S, stem)
    left = Counter(S[max(0, i - 3):i] for i in P)
    right = Counter(S[i + len(stem):i + len(stem) + 3] for i in P)
    return {
        "occurrences": len(P),
        "tables": sum(1 for s in tabs.values() if stem in s),
        "left_entropy": round(entropy(left), 2),
        "right_entropy": round(entropy(right), 2),
        "top_before": left.most_common(6),
        "top_after": right.most_common(6),
    }


def run():
    rng = random.Random(14)
    tabs = {n: s for n, s in load.all_tables().items() if n != 1}
    order = sorted(tabs)
    S = "|".join(tabs[n] for n in order)

    prof = {"ANZACH": profile("ANZACH", tabs, S), "CHASTOR": profile("CHASTOR", tabs, S)}
    nesting = {f: S.count(f) for f in ["ANZACH", "HANZACH", "NOCHANZACH", "ADNOCHANZACH",
                                        "ANZACHA", "ONZACH", "HONZACH", "HENZACH"]}

    va = [tabs[n].count("ANZACH") for n in order]
    vc = [tabs[n].count("CHASTOR") for n in order]
    r = pearson(va, vc)
    target = sum(va)
    pool = Counter(S[i:i + 6] for i in range(len(S) - 5))
    cands = [g for g, f in pool.items() if abs(f - target) <= max(8, target * 0.2) and "|" not in g
             and g not in ("ANZACH", "CHASTOR")]
    null = [pearson([tabs[n].count(g) for n in order], vc) for g in rng.sample(cands, min(200, len(cands)))]
    mu, sd = statistics.mean(null), statistics.pstdev(null) or 1

    # ordering inside shared tables: first occurrence of each
    first_a = first_c = 0
    for n in order:
        s = tabs[n]
        a, c = s.find("ANZACH"), s.find("CHASTOR")
        if a >= 0 and c >= 0:
            if a < c:
                first_a += 1
            else:
                first_c += 1
    shared = first_a + first_c

    lv = load.leaves()
    w1 = [load.letters(w) for k in ("1a", "1b") for row in lv.get(k, []) for w in row.split() if load.letters(w)]
    leaf1 = sorted({w for w in w1 if "NZA" in w and ("ANZ" in w or "HANZ" in w)})

    only_a = sum(1 for i in range(len(order)) if va[i] and not vc[i])
    only_c = sum(1 for i in range(len(order)) if vc[i] and not va[i])
    both = sum(1 for i in range(len(order)) if va[i] and vc[i])

    res = {
        "A_profiles": prof,
        "A_nesting_and_twins": nesting,
        "C_territory_vs_CHASTOR": {
            "pearson": round(r, 2), "null_mean": round(mu, 2), "null_sd": round(sd, 2),
            "z": round((r - mu) / sd, 1),
            "tables_both": both, "only_ANZACH": only_a, "only_CHASTOR": only_c,
            "verdict": ("shared court beyond chance" if r > mu + 3 * sd else
                        "separate territories beyond chance" if r < mu - 3 * sd else
                        "no territorial relation beyond table density"),
        },
        "D_order_in_shared_tables": {"ANZACH_first": first_a, "CHASTOR_first": first_c, "shared_tables": shared},
        "E_leaf1_forms": leaf1[:20],
        "series_per_table": {"tables": order, "ANZACH": va, "CHASTOR": vc},
    }
    load.save_result("14_anzach", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
