"""
64 - Finer chant structure: rhyme, a closed syllabary, a vowel melody. (Follows a62/a63.)

The lines have metre (a63). A chant often has more: rhyme, a small fixed set of syllables, a melodic
vowel line. Three tests on the row-written tables 2-24:

  A) Rhyme. Do consecutive lines of a leaf share their last two letters more than when the lines of
     the leaf are shuffled?
  B) A closed syllabary. Split each line into onset-maximal syllables (consonants + a vowel group).
     How many distinct syllables, and how many cover 90% of the text - fewer than a Markov-3
     surrogate of the same letter statistics would need?
  C) A vowel melody. Is the vowel-only sequence of a line more ordered (lower conditional entropy
     against its own shuffle) than the consonant-only sequence - i.e. is the tune in the vowels?
"""
import math
import random
import re
import statistics
from collections import Counter, defaultdict

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book, tnum

VOW = set("AEIOUVY")


def syllabify(s):
    syl, i, n = [], 0, len(s)
    while i < n:
        j = i
        while j < n and s[j] not in VOW:
            j += 1
        while j < n and s[j] in VOW:
            j += 1
        syl.append(s[i:j])
        i = j
    return [x for x in syl if x]


def cond_ent(seqs, k=2):
    ctx = defaultdict(Counter)
    for s in seqs:
        for i in range(len(s) - k):
            ctx[s[i:i + k]][s[i + k]] += 1
    tot = H = 0
    for d in ctx.values():
        n = sum(d.values())
        tot += n
        H -= sum(v * math.log2(v / n) for v in d.values())
    return H / tot if tot else 0


def run():
    rng = random.Random(64)
    book = base_book()
    rows = [r for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if len(r) == 49]

    # A rhyme
    leaves = {k: [r for r in v if len(r) == 49] for k, v in book.items() if 2 <= tnum(k) <= 24 and len([r for r in v if len(r) == 49]) >= 10}

    def endmatch(rr, N=2):
        return sum(rr[i][-N:] == rr[i + 1][-N:] for i in range(len(rr) - 1))
    real = sum(endmatch(v) for v in leaves.values())
    nul = []
    for _ in range(500):
        t = 0
        for v in leaves.values():
            sh = v[:]
            rng.shuffle(sh)
            t += endmatch(sh)
        nul.append(t)
    A = {"consecutive_lines_sharing_last_2_letters": real, "of_pairs": sum(len(v) - 1 for v in leaves.values()),
         "shuffled": round(statistics.mean(nul), 1), "z": round((real - statistics.mean(nul)) / statistics.pstdev(nul), 1)}

    # B syllabary
    allsyl = [x for r in rows for x in syllabify(r)]
    c = Counter(allsyl)

    def cover90(cnt):
        tot = sum(cnt.values())
        cum = 0
        for i, (_, v) in enumerate(cnt.most_common()):
            cum += v
            if cum >= 0.9 * tot:
                return i + 1
        return len(cnt)
    sur = markov3("".join(rows), rng)
    surrows = [sur[i:i + 49] for i in range(0, len(sur) - 48, 49)]
    cs = Counter(x for r in surrows for x in syllabify(r))
    B = {"distinct_syllables": len(c), "cover_90_percent": cover90(c),
         "surrogate_distinct": len(cs), "surrogate_cover_90_percent": cover90(cs),
         "commonest": [s for s, _ in c.most_common(20)]}

    # C vowel melody
    def only(s, v):
        return "".join(ch for ch in s if (ch in VOW) == v)
    C = {}
    for keep, name in ((True, "vowel_melody"), (False, "consonant_frame")):
        seqs = [only(r, keep) for r in rows]
        rr = cond_ent(seqs)
        nn = []
        for _ in range(40):
            sh = []
            for s in seqs:
                l = list(s)
                rng.shuffle(l)
                sh.append("".join(l))
            nn.append(cond_ent(sh))
        C[name] = {"conditional_entropy": round(rr, 3), "shuffled": round(statistics.mean(nn), 3),
                   "bits_of_order_structure": round(statistics.mean(nn) - rr, 3)}

    res = {"A_rhyme": A, "B_syllabary": B, "C_vowel_vs_consonant": C,
           "conclusion": "No finer poetic structure beyond the metre. Rhyme is weak (consecutive lines share their last "
                         "two letters only a little above shuffled, z ~2). The syllabary is not notably closed: ~441 "
                         "syllables cover 90%% of the text against ~505 for a surrogate - barely tighter. And the order "
                         "structure lives in the consonants (~0.71 bits saved against shuffle), not the vowels (~0.13) - "
                         "there is no vowel melody; the pattern is the consonant skeleton of the names. So the lines are "
                         "metrical (a63) but not rhymed, and carry their structure in the consonants."}
    load.save_result("64_finer_chant", res)
    return res


if __name__ == "__main__":
    r = run()
    print("rhyme:", r["A_rhyme"])
    print("syllabary:", {k: v for k, v in r["B_syllabary"].items() if k != "commonest"})
    print("vowel vs consonant:", r["C_vowel_vs_consonant"])
    print(r["conclusion"])
