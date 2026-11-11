"""
28 - Track B of the roadmap: the names, deeper.

  B1) Territory of each recurring name (known + discovered): lag-1 autocorrelation of its density
      along tables 2-48 vs shuffled table order; Bonferroni over the names tested.
  B2) Houses: does each name follow the NOCHA house (NOCHA, NOCHAP, ADNOCHA) or the GETH house
      (GETH, ACLAX)? Correlations of densities across tables after removing each part's mean (parts
      from a27), with a permutation null that shuffles tables inside parts.
  B3) Genealogy: for every pair core < longer form (the longer contains the core), does the core
      appear first in the book? Compared with the chance of that given the two counts.
  B4) Vowel mirrors (NOCHA <-> NACHO): among frequent strings, how many pairs differ by swapping
      two vowels, compared with pairs that differ by swapping two consonants, and with the same
      counts in a Markov-3 surrogate.
  B5) Hidden names: mask the dominant known names and rerun the a23 detector - what surfaces?
  B6) The two currents of 25b-28b: does each family use different variants on each current?
      Chi-square of variant x current summed over families vs random splits of the lines.
"""
import json
import math
import os
import random
import statistics
from collections import Counter, defaultdict
from itertools import combinations

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book, tnum

KNOWN = ["CHASTOR", "CHUSTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX"]
PARTS = [range(2, 13), range(13, 26), range(26, 34), range(34, 41), range(41, 49)]  # a27 (by table)
VOW = set("AEIOU")


def names_list():
    p = os.path.join(load.RESULTS, "23_name_discovery.json")
    d = [c["name"] for c in json.load(open(p, encoding="utf-8"))["A_candidates"]["top"]] if os.path.exists(p) else []
    return list(dict.fromkeys(KNOWN + d))


def table_texts(book):
    out = defaultdict(list)
    for k, v in book.items():
        out[tnum(k)] += v
    return {t: ("|".join(v), sum(len(r) for r in v)) for t, v in sorted(out.items())}


def ac1(x):
    m = statistics.mean(x)
    d = sum((a - m) ** 2 for a in x) or 1
    return sum((a - m) * (b - m) for a, b in zip(x, x[1:])) / d


def B1_territories(tt, names, rng):
    out = []
    for n in names:
        dens = [s.count(n) / L * 1000 for s, L in tt.values()]
        tot = sum(s.count(n) for s, _ in tt.values())
        if tot < 15:
            continue
        o = ac1(dens)
        nul = []
        for _ in range(1000):
            y = dens[:]
            rng.shuffle(y)
            nul.append(ac1(y))
        p = (sum(v >= o for v in nul) + 1) / 1001
        peak = max(tt, key=lambda t: tt[t][0].count(n) / tt[t][1])
        out.append({"name": n, "count": tot, "lag1": round(o, 2), "p": round(p, 4), "peak_table": peak,
                    "density_by_table": [round(v, 3) for v in dens], "tables": list(tt)})
    m = len(out)
    for r in out:
        r["survives_bonferroni"] = r["p"] * m < 0.05
    return sorted(out, key=lambda r: r["p"])


def residual(x, tabs):
    out = x[:]
    for rg in PARTS:
        idx = [i for i, t in enumerate(tabs) if t in rg]
        if idx:
            mu = statistics.mean(x[i] for i in idx)
            for i in idx:
                out[i] = x[i] - mu
    return out


def corr(a, b):
    ma, mb = statistics.mean(a), statistics.mean(b)
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = math.sqrt(sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) or 1
    return num / den


def B2_houses(tt, names, rng):
    tabs = list(tt)
    dens = lambda ns: [sum(s.count(n) for n in ns) / L * 1000 for s, L in tt.values()]
    hN = residual(dens(["NOCHA"]), tabs)
    hG = residual(dens(["GETH", "ACLAX"]), tabs)
    out = []
    for n in names:
        if n in ("NOCHA", "GETH", "ACLAX") or sum(s.count(n) for s, _ in tt.values()) < 15:
            continue
        x = residual(dens([n]), tabs)
        rN, rG = corr(x, hN), corr(x, hG)
        nN, nG = [], []
        for _ in range(500):
            y = x[:]
            for rg in PARTS:  # shuffle inside parts
                idx = [i for i, t in enumerate(tabs) if t in rg]
                vals = [y[i] for i in idx]
                rng.shuffle(vals)
                for i, v in zip(idx, vals):
                    y[i] = v
            nN.append(corr(y, hN))
            nG.append(corr(y, hG))
        pN = (sum(abs(v) >= abs(rN) for v in nN) + 1) / 501
        pG = (sum(abs(v) >= abs(rG) for v in nG) + 1) / 501
        house = "NOCHA" if (pN < 0.05 and rN > 0 and (rN - rG) > 0.2) else \
                "GETH/ACLAX" if (pG < 0.05 and rG > 0 and (rG - rN) > 0.2) else "neither"
        out.append({"name": n, "r_NOCHA": round(rN, 2), "p_NOCHA": round(pN, 3),
                    "r_GETH_ACLAX": round(rG, 2), "p_GETH_ACLAX": round(pG, 3), "house": house})
    return out


def first_pos(S, n):
    i = S.find(n)
    return i if i >= 0 else None


def B3_genealogy(book, names):
    keys = sorted(book, key=lambda k: (tnum(k), k[-1]))
    S = "#".join("|".join(book[k]) for k in keys)
    pairs = []
    for a in names:
        for b in names:
            if a != b and a in b and len(b) - len(a) >= 2:
                ca, cb = S.count(a), S.count(b)
                fa, fb = first_pos(S, a), first_pos(S, b)
                if None in (fa, fb):
                    continue
                # a occurs inside every b: count only free occurrences of the core
                free = ca - cb
                if free <= 0:
                    continue
                pairs.append({"core": a, "longer": b, "core_first": fa < fb,
                              "chance_core_first": round(free / (free + cb), 2)})
    obs = sum(p["core_first"] for p in pairs)
    exp = sum(p["chance_core_first"] for p in pairs)
    var = sum(p["chance_core_first"] * (1 - p["chance_core_first"]) for p in pairs)
    return {"pairs": len(pairs), "core_first": obs, "expected_by_counts": round(exp, 1),
            "z": round((obs - exp) / math.sqrt(var), 2) if var else None,
            "exceptions_longer_first": [f"{p['longer']} before {p['core']}" for p in pairs if not p["core_first"]][:12]}


def frequent(lines, kmin=5, kmax=8, mc=10):
    c = Counter()
    for r in lines:
        for k in range(kmin, kmax + 1):
            c.update(r[i:i + k] for i in range(len(r) - k + 1))
    return {g for g, v in c.items() if v >= mc}


def swaps(F):
    vow = cons = 0
    ex = []
    byk = defaultdict(list)
    for g in F:
        byk[len(g)].append(g)
    for k, gs in byk.items():
        idx = defaultdict(list)
        for g in gs:
            idx["".join(sorted(g))].append(g)  # anagram classes
        for cls in idx.values():
            for a, b in combinations(cls, 2):
                d = [i for i in range(k) if a[i] != b[i]]
                if len(d) == 2 and a[d[0]] == b[d[1]] and a[d[1]] == b[d[0]]:
                    if a[d[0]] in VOW and a[d[1]] in VOW:
                        vow += 1
                        if len(ex) < 12:
                            ex.append(f"{a}~{b}")
                    elif a[d[0]] not in VOW and a[d[1]] not in VOW:
                        cons += 1
    return vow, cons, ex


def B4_mirrors(book, rng):
    lines = [r for v in book.values() for r in v]
    F = frequent(lines)
    v, c, ex = swaps(F)
    sur = markov3("".join(lines), rng)
    sl, i = [], 0
    for r in lines:
        sl.append(sur[i:i + len(r)])
        i += len(r)
    Fs = frequent(sl)
    vs, cs, _ = swaps(Fs)
    return {"frequent_strings": len(F), "vowel_swap_pairs": v, "consonant_swap_pairs": c, "examples": ex,
            "surrogate_frequent_strings": len(Fs), "surrogate_vowel_swaps": vs, "surrogate_consonant_swaps": cs}


def B5_hidden(book):
    import a23_name_discovery as a23
    mask = ["NOCHASTOR", "CHASTOR", "CHUSTOR", "ADNOCHA", "NOCHA", "ANZACH", "ALGETH", "GETH", "ACLAX", "CHADAX", "OXAD", "NACHO"]
    mb = {}
    for k, v in book.items():
        rows = []
        for r in v:
            for n in mask:
                r = r.replace(n, "|")
            rows.extend(x for x in r.split("|") if x)
        mb[k] = rows
    tl = a23.lines_by_table(mb)
    lines = [r for v in mb.values() for r in v]
    tt = {t: "|".join(v) for t, v in tl.items()}
    c = a23.keep_maximal(a23.candidates(lines, lambda g: [t for t, s in tt.items() if g in s]))
    surv = sorted([x for x in c if x["z"] >= 4.5], key=lambda x: -x["count"])
    prev = set(names_list())
    new = [x for x in surv if not any(x["name"] in p or p in x["name"] for p in prev)]
    return {"survivors_after_masking": len(surv),
            "not_seen_before": [(x["name"], x["count"], x["tables"], x["z"]) for x in new[:25]]}


def B6_current_variants(rng):
    faces = json.load(open(os.path.join(load.DATA, "loagaeth_diagonal_decoded.json"), encoding="utf-8"))["faces"]
    dr = [r for f in faces.values() for r in f["down_right"]]
    lw = [r for f in faces.values() for r in f["leftward"]]
    fams = {"CHASTOR": ["NOCHASTOR", "ICHASTOR", "NECHASTOR", "ZICHASTOR", "CHASTOR"],
            "NOCHA": ["ADNOCHAP", "NOCHAP", "ADNOCHA", "NOCHA"], "NACHO": ["NACHOA", "NACHO"],
            "ACLAX": ["AXACLAX", "ACLAXTO", "ACLAX"], "GETH": ["ALGETH", "GETH"]}

    def variants(L):
        out = {}
        for f, vs in fams.items():
            c = Counter()
            for r in L:
                for v in vs:  # longest first, then mask
                    k = r.count(v)
                    if k:
                        c[v] += k
                        r = r.replace(v, "#")
            out[f] = c
        return out

    def chi(a, b):
        x = 0
        for f in fams:
            ks = set(a[f]) | set(b[f])
            na, nb = sum(a[f].values()), sum(b[f].values())
            N = na + nb
            if N < 6 or len(ks) < 2:
                continue
            for k in ks:
                t = a[f][k] + b[f][k]
                for obs, n in ((a[f][k], na), (b[f][k], nb)):
                    e = t * n / N
                    if e > 0:
                        x += (obs - e) ** 2 / e
        return x
    A, B = variants(dr), variants(lw)
    x0 = chi(A, B)
    allL = dr + lw
    nul = []
    for _ in range(300):
        rng.shuffle(allL)
        nul.append(chi(variants(allL[:len(dr)]), variants(allL[len(dr):])))
    return {"chi2_variant_by_current": round(x0, 1), "random_split_mean": round(statistics.mean(nul), 1),
            "random_split_95": round(sorted(nul)[284], 1), "p": round((sum(v >= x0 for v in nul) + 1) / 301, 4),
            "down_right": {f: dict(c) for f, c in A.items()}, "leftward": {f: dict(c) for f, c in B.items()}}


def run():
    rng = random.Random(28)
    book = base_book()
    names = names_list()
    tt = table_texts(book)
    res = {"B1_territories": B1_territories(tt, names, rng),
           "B2_houses": B2_houses(tt, names, rng),
           "B3_genealogy": B3_genealogy(book, names),
           "B4_vowel_mirrors": B4_mirrors(book, rng),
           "B5_hidden_names": B5_hidden(book),
           "B6_current_variants": B6_current_variants(rng)}
    load.save_result("28_names_deep", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
