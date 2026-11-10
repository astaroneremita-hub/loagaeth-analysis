"""
13 - The governors' numbers: the generative architecture behind the 2/3/6 anomaly.

Dee gives each of the 91 governors (Parts of the Earth) a number of servants. The digits
2, 3, 6 dominate (59% of digits, z~11 vs random numbers). Here we go further, with nulls that
PRESERVE the global digit distribution (so nothing below is explained by 2/3/6 being common):

  A) Block tests: 2,3,6 together in one number; contiguous permutations of 236 (632, 362...);
     last three digits a permutation of 236; trailing zero; exact duplicates; anagram pairs.
     Null = shuffle all digits across the 91 numbers, keeping each number's length.
  B) Head digit: do the governors of the same Aethyr share their first digit?
     Null = shuffle numbers across governors. Split into Aethyrs 1-14 vs 15-30.
  C) What else could set the head digit: part, tribe (1-12), tribal king, name initial.
  D) Dee's declared per-Aethyr sums vs the sum of the parts.

Data: engine/data/governadores.json.
"""
import itertools
import json
import math
import os
import random
import statistics
from collections import Counter

import load

HERE = os.path.dirname(os.path.abspath(__file__))
GOV = os.path.join(os.path.dirname(HERE), "engine", "data", "governadores.json")
PERM = {"".join(p) for p in itertools.permutations("236")}


def mi(a, b):
    n = len(a)
    ja, pa, pb = Counter(zip(a, b)), Counter(a), Counter(b)
    return sum(c / n * math.log2((c / n) / ((pa[x] / n) * (pb[y] / n))) for (x, y), c in ja.items())


def run():
    rng = random.Random(236)
    d = json.load(open(GOV, encoding="utf-8"))
    g = d["governadores"]
    N = [str(x["servos"]) for x in g]
    A = [x["aethyr"] for x in g]

    def shuffle_digits(nums):
        dg = list("".join(nums))
        rng.shuffle(dg)
        out, i = [], 0
        for n in nums:
            out.append("".join(dg[i:i + len(n)]))
            i += len(n)
        return out

    tests = {
        "contains_2_3_6_together": lambda ns: sum(1 for n in ns if all(c in n for c in "236")),
        "contiguous_236_permutation": lambda ns: sum(1 for n in ns if any(p in n for p in PERM)),
        "last3_is_236_permutation": lambda ns: sum(1 for n in ns if n[-3:] in PERM),
        "ends_in_zero": lambda ns: sum(1 for n in ns if n.endswith("0")),
        "exact_duplicate_pairs": lambda ns: sum(c * (c - 1) // 2 for c in Counter(ns).values()),
        "anagram_pairs": lambda ns: sum(c * (c - 1) // 2 for c in Counter("".join(sorted(n)) for n in ns).values()),
    }
    block = {}
    for k, f in tests.items():
        obs = f(N)
        sims = [f(shuffle_digits(N)) for _ in range(3000)]
        mu, sd = statistics.mean(sims), statistics.pstdev(sims) or 1
        block[k] = {"observed": obs, "null_mean": round(mu, 1), "z": round((obs - mu) / sd, 1)}

    def head_agree(nums, lo, hi):
        by = {}
        for n, a in zip(nums, A):
            if lo <= a <= hi:
                by.setdefault(a, []).append(n[0])
        return sum(sum(c * (c - 1) // 2 for c in Counter(v).values()) for v in by.values())
    head = {}
    for lo, hi in [(1, 30), (1, 14), (15, 30)]:
        obs = head_agree(N, lo, hi)
        sims = []
        for _ in range(5000):
            q = N[:]
            rng.shuffle(q)
            sims.append(head_agree(q, lo, hi))
        mu, sd = statistics.mean(sims), statistics.pstdev(sims) or 1
        head[f"aethyrs_{lo}_{hi}"] = {"same_head_pairs": obs, "null_mean": round(mu, 1), "z": round((obs - mu) / sd, 1)}

    heads = [n[0] for n in N]
    feats = {
        "aethyr": A,
        "part_in_aethyr": [x["parte_no_aethyr"] for x in g],
        "tribe_1_12": [x["anjo_tribo"].get("liber_scientiae_S4") for x in g],
        "name_initial": [x["nome"][0] for x in g],
    }
    drivers = {}
    for k, v in feats.items():
        pairs = [(h, f) for h, f in zip(heads, v) if f is not None]
        a, b = [p[0] for p in pairs], [p[1] for p in pairs]
        obs = mi(a, b)
        sims = []
        for _ in range(2000):
            bb = b[:]
            rng.shuffle(bb)
            sims.append(mi(a, bb))
        p = sum(1 for x in sims if x >= obs - 1e-12) / len(sims)
        drivers[k] = {"MI": round(obs, 3), "null_mean": round(statistics.mean(sims), 3), "p": round(p, 3)}

    by = {}
    for x, h in zip(g, heads):
        by.setdefault(x["aethyr"], []).append(h)
    uniform = {a: v[0] for a, v in by.items() if len(set(v)) == 1}

    # E) which order of the 2-3-6 block? (each of the 6 orders equally likely under any digit shuffle)
    perms = ["".join(p) for p in itertools.permutations("236")]
    used = [next((p for p in perms if p in n), None) for n in N]
    used = [u for u in used if u]
    cnt = Counter(used)
    k, n_ = cnt.get("236", 0), len(used)
    p_asc = sum(math.comb(n_, i) * (1 / 6) ** i * (5 / 6) ** (n_ - i) for i in range(k, n_ + 1))
    order = {"counts": dict(cnt.most_common()), "ascending_236": k, "of": n_,
             "expected_if_uniform": round(n_ / 6, 1), "p_binomial": round(p_asc, 5)}

    # F) search for a rule giving the shared head digit in Aethyrs 15-30, with a null that
    #    re-runs the whole search on shuffled heads (controls for trying many rules)
    import sys
    sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
    try:
        import fontes
        G = fontes.gematria_value_tables()
    except Exception:
        G = {}
    import unicodedata

    def norm(s):
        s = "".join(c for c in unicodedata.normalize("NFD", (s or "").upper()) if "A" <= c <= "Z")
        return s.translate(str.maketrans("YJVWK", "IIUUC"))

    def dr(v):
        return str(1 + (v - 1) % 9) if v else "0"
    names = {a["numero"]: norm(a.get("nome_crowley_1911", "")) for a in d["aethyrs"]}
    AE = list(range(15, 31))
    modal = {a: Counter(v).most_common(1)[0][0] for a, v in by.items()}
    target = [modal[a] for a in AE]
    rules = {}
    for sid, tab in G.items():
        rules["gematria_root:" + sid] = [dr(sum(tab[c] for c in names[a])) if all(c in tab for c in names[a]) else None for a in AE]
        rules["gematria_last:" + sid] = [str(sum(tab[c] for c in names[a]))[-1] if all(c in tab for c in names[a]) else None for a in AE]
    rules["aethyr_root"] = [dr(a) for a in AE]
    rules["reverse_index_root"] = [dr(31 - a) for a in AE]
    rules["aethyr_last_digit"] = [str(a % 10) for a in AE]
    rules["parts_sum_root"] = [dr(sum(int(x) for x in [s for s, aa in zip(N, A) if aa == a])) for a in AE]

    def score(vals, tgt):
        return sum(1 for v, t in zip(vals, tgt) if v is not None and v == t)
    best = max(score(v, target) for v in rules.values()) if rules else 0
    null = []
    for _ in range(2000):
        t = target[:]
        rng.shuffle(t)
        null.append(max(score(v, t) for v in rules.values()) if rules else 0)
    head_rule = {"rules_tried": len(rules), "best_matches_of_16": best,
                 "null_mean_of_best": round(statistics.mean(null), 1),
                 "p": round(sum(1 for x in null if x >= best) / len(null), 3),
                 "verdict": "no known rule sets the head digit" if best <= sorted(null)[int(0.95 * len(null))] else "candidate rule found"}

    sums = []
    for a in d["aethyrs"]:
        sums.append({"aethyr": a["numero"], "declared": a.get("soma_ministros_declarada_tfr"),
                     "parts": a.get("soma_ministros_partes"), "match": a.get("soma_confere")})
    mismatch = [s for s in sums if s["match"] is False]

    res = {
        "A_block_tests": block,
        "B_head_digit_by_aethyr": head,
        "B_uniform_head_aethyrs": uniform,
        "C_head_digit_drivers": drivers,
        "E_block_order": order,
        "F_head_rule_search": head_rule,
        "D_declared_sums_mismatch": mismatch,
        "D_note": ("Aethyr 2 (ARN): Dee declares 6660 but the parts sum to 14960 (3636+2362+8962). "
                   "6660 would fit exactly if the third number were 662; every source gives 8962, "
                   "so the declared sum is the likelier slip. Hypothesis only."),
        "conclusion": ("Architecture: number = [an Aethyr's head digit] + [the 2-3-6 block, permuted, "
                       "sometimes zero-padded]. The head digit is shared within an Aethyr only in the "
                       "second half (Aethyrs 15-30); in 1-14 it is free - a change of construction "
                       "regime at the midpoint. No link to tribe, part or name. The exact rule choosing "
                       "each head digit and each permutation is still unknown."),
    }
    load.save_result("13_numbers", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
