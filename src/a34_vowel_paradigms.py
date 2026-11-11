"""
34 - Vowel paradigms: is changing one vowel a mechanism of the language?

Lead: Dee's own glosses give POLA "two together" vs PALA "two separated" - one vowel apart - and
CANSE "mighty" vs CRISCANSE "more mighty". The tables have NOCHA / NACHO and the A->U register.

  A) Leaf 1 (Dee's own word division, 2,300+ distinct words of 4+ letters): pairs of words that
     differ in exactly one vowel, and "series" (one frame attested with 3 or more vowels, like
     DATH / DETH / DOTH / DUTH). Null: all vowels shuffled among the vowel slots of the word list and
     all consonants among the consonant slots (keeps every word's shape and the letter counts).
     Also the ratio vowel-pairs / consonant-pairs, to separate "vowel alternation" from "the words
     simply come in families".
  B) The same on the tables' frequent strings vs Markov-3 surrogates.
  C) Which vowel pairs alternate (A/O, A/E, A/U...).
"""
import json
import random
import statistics
from collections import Counter, defaultdict

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book
from a33_diary_anchors import leaf1_words

VOW = set("AEIOU")


def analyse(words):
    idx = defaultdict(set)
    for g in words:
        for i in range(len(g)):
            idx[(g[:i], g[i + 1:])].add(g[i])
    v = c = series = 0
    vp = Counter()
    ex_series, ex_pairs = [], []
    for (a, b), ls in idx.items():
        vs = sorted(x for x in ls if x in VOW)
        cs = [x for x in ls if x not in VOW]
        v += len(vs) * (len(vs) - 1) // 2
        c += len(cs) * (len(cs) - 1) // 2
        for i in range(len(vs)):
            for j in range(i + 1, len(vs)):
                vp[vs[i] + vs[j]] += 1
        if len(vs) >= 3:
            series += 1
            ex_series.append(" / ".join(a + x + b for x in vs))
        elif len(vs) == 2 and len(ex_pairs) < 30:
            ex_pairs.append(f"{a}{vs[0]}{b} ~ {a}{vs[1]}{b}")
    return {"vowel_pairs": v, "consonant_pairs": c, "ratio": v / c if c else 0, "series": series,
            "by_vowel_pair": dict(vp.most_common()), "ex_series": sorted(ex_series, key=len, reverse=True), "ex_pairs": ex_pairs}


def slot_shuffle(words, rng):
    vs = [ch for w in words for ch in w if ch in VOW]
    cs = [ch for w in words for ch in w if ch not in VOW]
    rng.shuffle(vs)
    rng.shuffle(cs)
    vi = ci = 0
    out = set()
    for w in words:
        s = []
        for ch in w:
            if ch in VOW:
                s.append(vs[vi]); vi += 1
            else:
                s.append(cs[ci]); ci += 1
        out.add("".join(s))
    return out


def zs(obs, nul):
    return round((obs - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1)


def A_leaf1(rng):
    W = sorted({w for w in leaf1_words() if len(w) >= 4})
    o = analyse(W)
    N = [analyse(slot_shuffle(W, rng)) for _ in range(300)]
    out = {"words": len(W)}
    for k in ("vowel_pairs", "consonant_pairs", "ratio", "series"):
        xs = [n[k] for n in N]
        out[k] = {"observed": round(o[k], 3), "null_mean": round(statistics.mean(xs), 3), "null_max": round(max(xs), 3), "z": zs(o[k], xs)}
    out["by_vowel_pair"] = o["by_vowel_pair"]
    out["series_examples"] = o["ex_series"][:25]
    out["pair_examples"] = o["ex_pairs"][:20]
    return out


def freq_strings(lines, kmin=5, kmax=8, mc=8):
    c = Counter()
    for r in lines:
        r = r.replace("V", "U")
        for k in range(kmin, kmax + 1):
            c.update(r[i:i + k] for i in range(len(r) - k + 1))
    return [g for g, v in c.items() if v >= mc]


def B_tables(rng):
    book = base_book()
    lines = [r for v in book.values() for r in v]
    o = analyse(freq_strings(lines))
    N = []
    for _ in range(8):
        sur = markov3("".join(lines), rng)
        sl, i = [], 0
        for r in lines:
            sl.append(sur[i:i + len(r)])
            i += len(r)
        N.append(analyse(freq_strings(sl)))
    out = {}
    for k in ("vowel_pairs", "consonant_pairs", "ratio", "series"):
        xs = [n[k] for n in N]
        out[k] = {"observed": round(o[k], 3), "surrogate_mean": round(statistics.mean(xs), 3), "surrogate_max": round(max(xs), 3), "z": zs(o[k], xs)}
    out["by_vowel_pair"] = o["by_vowel_pair"]
    out["by_vowel_pair_surrogate_mean"] = {k: round(statistics.mean(n["by_vowel_pair"].get(k, 0) for n in N), 1) for k in o["by_vowel_pair"]}
    return out


def run():
    rng = random.Random(34)
    res = {"A_leaf1_words": A_leaf1(rng), "B_tables_frequent_strings": B_tables(rng)}
    load.save_result("34_vowel_paradigms", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
