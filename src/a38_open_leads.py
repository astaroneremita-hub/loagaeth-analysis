"""
38 - Three leads from the literature, tested.

  A) Laycock: the Calls could have been drawn from the tables by taking every k-th letter. Read every
     k-th letter of the row-written tables (k = 1..12, best offset) with a letter model of the Calls'
     words; compare with shuffled letters.
  B) Note on leaf 43a: tables 43-48 are a pattern, "every empty square is to be filled as these are".
     Are the sides of 43-48 copies of one another (same letter in the same cell), or more repetitive
     inside, than the diamonds 29-42?
  C) Heptarchy: the six numbered 7x7 tables (T2-T7) scatter the numbers 1-49. Is there a rule?
     Affine placement (position = a*n + b mod 49), drift of numbers down the rows, and letters
     clustering along rows, each against shuffles.
"""
import json
import os
import random
import statistics
from collections import Counter

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a33_diary_anchors import call_words

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def A_decimation(rng):
    m = CharLM(2, alpha=0.5).fit(call_words()[1])
    book = base_book()
    S = "".join(r for k, v in book.items() if tnum(k) <= 24 for r in v)
    sh = list(S)
    rng.shuffle(sh)

    def bits(s):
        return m.bits([s[i:i + 12] for i in range(0, len(s) - 12, 12)][:3000])
    return {"shuffled_letters": round(bits("".join(sh)), 3),
            "every_kth_letter": {k: round(min(bits(S[o::k]) for o in range(k)), 3) for k in range(1, 13)}}


def B_tables_43_48():
    lv = load.leaves()
    rows = lambda k: [load.letters(r) for r in lv.get(k, []) if load.letters(r)]
    keys = [f"{t}{s}" for t in range(29, 49) for s in "ab" if rows(f"{t}{s}")]

    def ident(a, b):
        n = e = 0
        for x, y in zip(a, b):
            for p, q in zip(x, y):
                n += 1
                e += p == q
        return e / n if n else 0

    def pairs(K):
        return [ident(rows(a), rows(c)) for i, a in enumerate(K) for c in K[i + 1:] if len(rows(a)) == len(rows(c))]

    def rep(k):
        c = Counter(g for r in rows(k) for g in (r[i:i + 6] for i in range(len(r) - 5)))
        n = sum(c.values())
        return sum(v for v in c.values() if v > 1) / n if n else 0
    late = [k for k in keys if int(k[:-1]) >= 43]
    early = [k for k in keys if int(k[:-1]) < 43]
    pl, pe = pairs(late), pairs(early)
    return {"same_cell_identity_43_48": [round(statistics.mean(pl), 3), round(max(pl), 3)],
            "same_cell_identity_29_42": [round(statistics.mean(pe), 3), round(max(pe), 3)],
            "repeated_6grams_inside_side_43_48": round(statistics.mean(rep(k) for k in late), 3),
            "repeated_6grams_inside_side_29_42": round(statistics.mean(rep(k) for k in early), 3),
            "empty_cells_43_48": sum("".join(lv.get(k, [])).count("?") for k in late)}


def C_heptarchy(rng):
    T = json.load(open(os.path.join(ROOT, "engine", "data", "heptarquia.json"), encoding="utf-8"))["sete_tabelas"]["tabelas"]
    out = []
    for t in T[1:]:
        cells = [c for row in t["celulas"] for c in row]
        pos = {c["numero"]: i for i, c in enumerate(cells) if c.get("numero")}
        aff = max(sum(1 for k, v in pos.items() if (a * (k - 1) + b) % 49 == v) for a in range(1, 49) for b in range(49))
        nul_aff = []
        ks = list(pos)
        for _ in range(40):
            vals = list(pos.values())
            rng.shuffle(vals)
            d = dict(zip(ks, vals))
            nul_aff.append(max(sum(1 for k, v in d.items() if (a * (k - 1) + b) % 49 == v) for a in range(1, 49) for b in range(49)))
        xs = [(c["linha"], c["numero"]) for c in cells if c.get("numero")]

        def r_(pairs):
            a, b = [p[0] for p in pairs], [p[1] for p in pairs]
            ma, mb = statistics.mean(a), statistics.mean(b)
            return sum((x - ma) * (y - mb) for x, y in zip(a, b)) / (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
        o = r_(xs)
        nums = [p[1] for p in xs]
        nul = []
        for _ in range(2000):
            rng.shuffle(nums)
            nul.append(abs(r_([(p[0], n) for p, n in zip(xs, nums)])))
        nums_all = [c.get("numero") for c in cells if c.get("numero")]
        dup = sorted(n for n, c in Counter(nums_all).items() if c > 1)
        out.append({"table": t["id"], "best_affine_hits": aff, "shuffled_best_affine_mean": round(statistics.mean(nul_aff), 1),
                    "number_vs_row_r": round(o, 2), "p": round(sum(v >= abs(o) for v in nul) / 2000, 3),
                    "duplicated_numbers": dup, "missing_numbers": sorted(set(range(1, 50)) - set(nums_all))})
    return out


def run():
    rng = random.Random(38)
    res = {"A_every_kth_letter": A_decimation(rng), "B_tables_43_48": B_tables_43_48(), "C_heptarchy_layouts": C_heptarchy(rng)}
    load.save_result("38_open_leads", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
