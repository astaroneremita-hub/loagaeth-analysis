"""
41 - Do the letter changes inside repeated passages follow sounds? An independent check of a40.

Module a40 found 179 passages of 14 letters that recur with one letter changed, and noticed that the
consonant changes seemed to stay inside sound classes. Those classes were drawn after looking at the
pairs. Here the classes are fixed beforehand, from ordinary phonetics, in two independent ways:

  manner: stops P B T D C G K Q | fricatives F V S Z X H | nasals M N | liquids L R
  place:  lips P B F M V | tongue tip T D S Z N L R | back C G K Q X H

and the test is run (1) on the 14-letter variants against 12 pooled Markov-3 surrogates (which have
the same letter contexts, so they measure how often context alone makes like replace like);
(2) on fresh evidence, variants of 10-letter passages at positions not used in (1);
(3) on Dee's own spaced words of leaf 1: pairs of words differing in one consonant.
"""
import json
import math
import random
import statistics
from collections import Counter, defaultdict

import load
from a22_robustness_and_depth import base_book
from a39_long_repeats import surrogate3

VOW = set("AEIOUY")
SCHEMES = {"manner": ["PBTDCGKQ", "FVSZXH", "MN", "LR"], "place": ["PBFMV", "TDSZNLR", "CGKQXH"]}


def variants(lines, W):
    h = W // 2
    idx = defaultdict(list)
    for li, r in enumerate(lines):
        for i in range(len(r) - W + 1):
            idx[(0, r[i:i + h])].append((li, i))
            idx[(1, r[i + h:i + W])].append((li, i))
    subs = {}
    for v in idx.values():
        if len(v) < 2 or len(v) > 250:
            continue
        for x in range(len(v)):
            la, ia = v[x]
            A = lines[la][ia:ia + W]
            for y in range(x + 1, len(v)):
                lb, ib = v[y]
                if la == lb and abs(ia - ib) < W:
                    continue
                B = lines[lb][ib:ib + W]
                d = [j for j in range(W) if A[j] != B[j]]
                if len(d) == 1 and 3 <= d[0] <= W - 4:
                    j = d[0]
                    subs[(la, ia + j, lb, ib + j)] = tuple(sorted((A[j], B[j])))
    return subs


def same(p, q, classes):
    return any(p in c and q in c for c in classes)


def cons_pairs(subs, skip=()):
    return [v for k, v in subs.items() if k not in skip and v[0] not in VOW and v[1] not in VOW]


def binom_tail(k, n, p):
    if p <= 0 or p >= 1:
        return 1.0 if k == 0 or p >= 1 else 0.0
    lg = lambda i: math.lgamma(n + 1) - math.lgamma(i + 1) - math.lgamma(n - i + 1) + i * math.log(p) + (n - i) * math.log(1 - p)
    return min(1.0, sum(math.exp(lg(i)) for i in range(k, n + 1)))


def freq_null(pairs_n, f, classes, rng, reps=2000):
    cons = [x for x in f if x not in VOW]
    w = [f[x] for x in cons]
    out = []
    for _ in range(reps):
        k = 0
        for _ in range(pairs_n):
            while True:
                p, q = rng.choices(cons, w, k=2)
                if p != q:
                    break
            k += same(p, q, classes)
        out.append(k / max(1, pairs_n))
    return out


def report(real, surr, f, rng):
    out = {"consonant_changes": len(real), "surrogate_consonant_changes_pooled": len(surr)}
    for name, classes in SCHEMES.items():
        k = sum(same(p, q, classes) for p, q in real)
        ks = sum(same(p, q, classes) for p, q in surr)
        ps = ks / max(1, len(surr))
        fn = freq_null(len(real), f, classes, rng)
        out[name] = {"share_inside_class": round(k / max(1, len(real)), 3),
                     "markov3_surrogates": round(ps, 3),
                     "p_vs_surrogates": round(binom_tail(k, len(real), ps), 4) if surr else None,
                     "by_letter_frequency": round(statistics.mean(fn), 3),
                     "p_vs_frequency": round(sum(v >= k / max(1, len(real)) for v in fn) / len(fn), 4)}
    return out


def leaf1(f, rng):
    words = sorted({w.upper() for w in load.spaced_words(3) if w.isalpha()})
    by = defaultdict(list)
    for w in words:
        for j in range(len(w)):
            by[(w[:j], w[j + 1:], len(w))].append(w[j])
    pairs = [tuple(sorted((a, b))) for v in by.values() for i, a in enumerate(v) for b in v[i + 1:]
             if a not in VOW and b not in VOW]
    out = {"words": len(words), "pairs_differing_in_one_consonant": len(pairs)}
    for name, classes in SCHEMES.items():
        k = sum(same(p, q, classes) for p, q in pairs)
        fn = freq_null(len(pairs), f, classes, rng)
        out[name] = {"share_inside_class": round(k / max(1, len(pairs)), 3), "by_letter_frequency": round(statistics.mean(fn), 3),
                     "p_vs_frequency": round(sum(v >= k / max(1, len(pairs)) for v in fn) / len(fn), 4)}
    return out


def run():
    rng = random.Random(41)
    book = base_book()
    lines = [r for v in book.values() for r in v if r]
    f = Counter("".join(lines))
    s14 = variants(lines, 14)
    s10 = variants(lines, 10)
    sur14, sur10 = [], []
    for _ in range(12):
        s = surrogate3(lines, rng)
        a = variants(s, 14)
        sur14 += cons_pairs(a)
        sur10 += cons_pairs(variants(s, 10), skip=a)
    res = {"classes_fixed_beforehand": SCHEMES,
           "A_14_letter_variants": report(cons_pairs(s14), sur14, f, rng),
           "B_10_letter_variants_at_new_positions": report(cons_pairs(s10, skip=s14), sur10, f, rng),
           "C_leaf1_words": leaf1(f, rng),
           "top_consonant_pairs_14": [{"pair": p + "/" + q, "count": n} for (p, q), n in Counter(cons_pairs(s14)).most_common(12)],
           "top_consonant_pairs_10_new": [{"pair": p + "/" + q, "count": n} for (p, q), n in Counter(cons_pairs(s10, skip=s14)).most_common(12)],
           "top_surrogate_pairs_10": [{"pair": p + "/" + q, "count": n} for (p, q), n in Counter(sur10).most_common(8)]}
    load.save_result("41_sound_classes", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
