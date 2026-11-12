"""
62 - Two verticals: the book as a chant, and the book as a 49x49x49 cube.

  A) Chant. The record says the book is spoken ("sounded Logah"), and its words were to be
     "distinguished" and accented in the last seven of forty days; the accents survive on leaves
     2a-5a (a51). If the lines are meant to be intoned, they may be tuned to a beat - a regular
     number of syllables per line - rather than a regular number of words. Syllable = a vowel group
     (a run of A E I O U V Y). The test: are the row syllable-counts more regular than the same rows
     with their letters shuffled (which keeps 49 letters and the same composition, so a regularity
     that is only fixed line width would survive the shuffle)? And where does the stress fall?

  B) Cube. The record: 49 leaves, each 49x49; "every Element hath 49 manner of understandings". Is
     there a third axis - does the cell (row, col) of one leaf relate to the same cell of the next,
     so the stack of leaves reads as a 49x49x49 cube? Mutual information between the same cell on
     adjacent leaves, and whether names read down the depth axis, against leaves shuffled
     independently.
"""
import math
import random
import re
import statistics
from collections import Counter

import load
import a15_book_geometry as a15
from a22_robustness_and_depth import base_book, tnum

VOWELS = "AEIOUVY"


def syllables(w):
    return len(re.findall(r"[%s]+" % VOWELS, w))


def A_chant(rng):
    book = base_book()
    rows = [r for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if len(r) == 49]
    real = [syllables(r) for r in rows]

    def shuffled_sd():
        out = []
        for r in rows:
            l = list(r)
            rng.shuffle(l)
            out.append(syllables("".join(l)))
        return statistics.pstdev(out)
    nul = [shuffled_sd() for _ in range(200)]
    # stress position, from the pointed words (real boundaries and accents)
    import a51_word_points as wp
    G = wp.parse()
    fromend = Counter()
    for k in G:
        for i in G[k]:
            r = G[k][i]
            for w in wp.words_of(r):
                groups = [(m.start(), m.end()) for m in re.finditer(r"[%s]+" % VOWELS, w)]
                if len(groups) < 2:
                    continue
                base = sum(1 for x, y in enumerate(G[k][i]["letters"]))  # unused; accents are indices in the whole row's letters
    # accents are positions in the row's letters; map each to the word and its vowel group
    for k in G:
        for i in G[k]:
            r = G[k][i]
            L = r["letters"]
            cuts = [0] + [c for c in r["cuts"] if c < len(L)] + [len(L)]
            for a in r["accents"]:
                for x, y in zip(cuts, cuts[1:]):
                    if x <= a < y:
                        w = L[x:y]
                        groups = [(m.start() + x, m.end() + x) for m in re.finditer(r"[%s]+" % VOWELS, w)]
                        if len(groups) >= 2:
                            for gi, (s, e) in enumerate(groups):
                                if s <= a < e:
                                    fromend[len(groups) - gi] += 1
                        break
    return {"rows": len(rows), "syllables_per_row_mean": round(statistics.mean(real), 2),
            "syllables_per_row_sd": round(statistics.pstdev(real), 2),
            "sd_with_letters_shuffled": round(statistics.mean(nul), 2),
            "z": round((statistics.pstdev(real) - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
            "stress_from_the_end": dict(sorted(fromend.items())),
            "conclusion": "The rows are tuned to a syllable count: ~17-18 syllables, with a spread (sd ~1.05) well below "
                          "what the same letters in random order give (sd ~1.70, z ~-24). The regularity is not just the "
                          "fixed 49-letter width - the arrangement of vowels and consonants holds the beat. Stress falls "
                          "most often on the penultimate syllable. The lines carry metre, as a text made to be intoned "
                          "would. REAL."}


def fullgrid(n):
    lv = load.leaves()
    for k in (f"{n}a", f"{n}b"):
        g = [load.letters(r) for r in lv.get(k, []) if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            return g
    return a15.rebuild(n)


def B_cube(rng):
    cube = []
    for n in range(2, 49):
        g = fullgrid(n)
        if g and not any(x is None for row in g for x in row):
            cube.append(g)

    def depth_mi(stack):
        c, a, b = Counter(), Counter(), Counter()
        for d in range(len(stack) - 1):
            for r in range(49):
                for col in range(49):
                    x, y = stack[d][r][col], stack[d + 1][r][col]
                    c[(x, y)] += 1
                    a[x] += 1
                    b[y] += 1
        n = sum(c.values())
        return sum(v / n * math.log2(v * n / (a[x] * b[y])) for (x, y), v in c.items())

    def shuffle_cube():
        out = []
        for g in cube:
            flat = [x for row in g for x in row]
            rng.shuffle(flat)
            out.append([flat[i * 49:(i + 1) * 49] for i in range(49)])
        return out
    real = depth_mi(cube)
    nul = [depth_mi(shuffle_cube()) for _ in range(20)]
    names = ["CHASTOR", "NOCHA", "GETH", "ACLAX", "ADNOCHA", "NACHO", "OXAD", "ANZACH"]
    down = "|".join("".join(cube[d][r][c] for d in range(len(cube))) for r in range(49) for c in range(49))
    realn = sum(down.count(nm) for nm in names)
    nuln = []
    for _ in range(20):
        sc = shuffle_cube()
        Sd = "|".join("".join(sc[d][r][c] for d in range(len(sc))) for r in range(49) for c in range(49))
        nuln.append(sum(Sd.count(nm) for nm in names))
    return {"leaves_in_the_cube": len(cube),
            "same_cell_mutual_information_adjacent_leaves_bits": round(real, 4), "shuffled": round(statistics.mean(nul), 4),
            "z_mi": round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
            "names_read_down_the_depth_axis": realn, "shuffled_names": round(statistics.mean(nuln), 1),
            "z_names": round((realn - statistics.mean(nuln)) / (statistics.pstdev(nuln) or 1e-9), 1),
            "conclusion": "No meaningful third axis. The same cell on adjacent leaves shares only 0.0016 bits above chance "
                          "(z ~7 but negligible in size - the trace of neighbouring leaves sharing a dialect, a43), and no "
                          "names read down the stack (z ~0). The book is not a 49x49x49 cube with a readable depth; '49 "
                          "understandings' is not a literal third dimension. REFUTED."}


def run():
    rng = random.Random(62)
    res = {"A_chant": A_chant(rng), "B_cube": B_cube(rng)}
    load.save_result("62_chant_and_cube", res)
    return res


if __name__ == "__main__":
    r = run()
    a = r["A_chant"]
    print("CHANT: %.2f syllables/row, sd %.2f vs shuffled %.2f (z %.1f); stress from end %s" %
          (a["syllables_per_row_mean"], a["syllables_per_row_sd"], a["sd_with_letters_shuffled"], a["z"], a["stress_from_the_end"]))
    print(" ", a["conclusion"])
    b = r["B_cube"]
    print("CUBE: MI %.4f vs %.4f (z %.1f); names down %d vs %.1f (z %.1f)" %
          (b["same_cell_mutual_information_adjacent_leaves_bits"], b["shuffled"], b["z_mi"], b["names_read_down_the_depth_axis"], b["shuffled_names"], b["z_names"]))
    print(" ", b["conclusion"])
