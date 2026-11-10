"""
01 - Basic linguistic statistics of the Loagaeth letter stream.

Computes, over the whole dense stream:
  - unigram (H1) and conditional bigram (H2|1) Shannon entropy in bits/letter
  - index of coincidence (IC)
  - type/token ratio over the word-spaced leaves
  - Zipf slope of the 6-gram frequency rank distribution

These are descriptive. No null model: they characterize the text, they do not
claim a hidden code. Interpretation: higher-than-random structure at the letter
level, consistent with a constructed name-language rather than noise.
"""
import math
from collections import Counter

import load


def entropy_bits(counter):
    total = sum(counter.values())
    return -sum((c / total) * math.log2(c / total) for c in counter.values())


def run():
    s = load.dense_stream()
    uni = Counter(s)
    H1 = entropy_bits(uni)

    # conditional entropy H(next | current) from bigrams
    bi = Counter(load.ngrams(s, 2))
    ctx = Counter()
    for (a, b), c in bi.items():
        ctx[a] += c
    Hcond = 0.0
    N = sum(bi.values())
    for (a, b), c in bi.items():
        p_ab = c / N
        p_b_given_a = c / ctx[a]
        Hcond -= p_ab * math.log2(p_b_given_a)

    # index of coincidence
    n = sum(uni.values())
    ic = sum(c * (c - 1) for c in uni.values()) / (n * (n - 1))

    # type/token on spaced words
    words = load.spaced_words()
    ttr = len(set(words)) / len(words) if words else None

    # Zipf slope: log rank vs log freq of 6-grams, least squares
    g6 = Counter(load.ngrams(s, 6))
    freqs = sorted(g6.values(), reverse=True)
    xs = [math.log(i + 1) for i in range(len(freqs))]
    ys = [math.log(f) for f in freqs]
    m = len(xs)
    mx, my = sum(xs) / m, sum(ys) / m
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    var = sum((x - mx) ** 2 for x in xs)
    zipf_slope = cov / var

    res = {
        "n_letters": n,
        "alphabet_size": len(uni),
        "H1_bits_per_letter": round(H1, 4),
        "H_conditional_bits": round(Hcond, 4),
        "index_of_coincidence": round(ic, 5),
        "ic_uniform_reference": round(1 / len(uni), 5),
        "type_token_ratio_spaced": round(ttr, 4) if ttr else None,
        "zipf_slope_6gram": round(zipf_slope, 3),
        "note": "H_conditional well below H1 means strong local predictability (syllable structure).",
    }
    load.save_result("01_basic_stats", res)
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=1))
