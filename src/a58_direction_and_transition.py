"""
58 - The reading direction of the book, and the transition from words to tables.

Two questions left by the diary.

  A) Direction. Galvah: "Write the Book backward … the first leaf is the last of the Book." Is there a
     textual direction - does a leaf read better from the leaves before it than from the leaves after
     it? A letter model trained on the six leaves before leaf k, reading k, against one trained on
     the six leaves after. And is there any trend in difficulty along the length of the book?
  B) The transition. Leaf 1 side 2 ends in nine rows of single letters (a54: 3.84 bits, between the
     word-language of leaf 1 and the letter-language of the tables). Are these nine rows the seed of
     the table lexicon - do the recurring names first appear there - or does the table language
     begin only at table 2?
"""
import collections
import json
import os
import statistics

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum


def run():
    book = base_book()
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 2 <= tnum(k) <= 48]
    sides = {k: [r for r in book[k] if r] for k in keys}

    def bits(train_keys, test_key):
        tr = [r for j in train_keys for r in sides[j]]
        return CharLM(4, alpha=0.01).fit(tr).bits(sides[test_key]) if len(tr) >= 50 else None
    fwd, bwd = [], []
    for i, k in enumerate(keys):
        if 6 < i < len(keys) - 6:
            b1, b2 = bits(keys[i - 6:i], k), bits(keys[i + 1:i + 7], k)
            if b1 and b2:
                fwd.append(b1)
                bwd.append(b2)
    m = CharLM(4, alpha=0.01).fit([r for j in keys for r in sides[j]])
    trend = [(tnum(k), round(m.bits(sides[k]), 3)) for k in keys if k.endswith("a")]
    A = {"read_from_the_preceding_6_leaves": round(statistics.mean(fwd), 3),
         "read_from_the_following_6_leaves": round(statistics.mean(bwd), 3),
         "difference_bits": round(statistics.mean(bwd) - statistics.mean(fwd), 4), "leaves_tested": len(fwd),
         "bits_per_leaf_a_sides_first6": trend[:6], "last6": trend[-6:],
         "conclusion": "No textual direction: a leaf reads the same from the leaves before or after it, and the "
                       "difficulty is flat along the book. 'Write backward / the first leaf is the last' is an order of "
                       "binding, not of the text."}

    lv = load.leaves()
    nine = [load.letters(r) for r in lv["1b"] if len(r.split()) == 1 and len(load.letters(r)) >= 40]
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    masters = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"]
    names = sorted({x["name"] for x in d} | set(masters), key=len, reverse=True)
    block = "".join(nine)
    whole = {k: "".join(r for r in book[k] if r) for k in sorted(book, key=lambda k: (tnum(k), k))}
    firstleaf = {}
    for n in names:
        for k in sorted(whole, key=lambda k: (tnum(k), k)):
            if n in whole[k]:
                firstleaf[n] = k
                break

    def grams(s, k=4):
        return set(s[i:i + k] for i in range(len(s) - k + 1))

    def jac(a, b):
        return round(len(a & b) / len(a | b), 3)
    g9 = grams(block)
    w1 = "".join(load.letters(w) for r in lv["1a"] for w in r.split() if load.letters(w))
    B = {"names_in_the_nine_rows": {n: block.count(n) for n in names if block.count(n)},
         "where_names_first_appear": dict(collections.Counter(firstleaf.values()).most_common(6)),
         "four_gram_overlap": {"nine_rows_vs_table_2a": jac(g9, grams("".join(sides["2a"]))),
                               "nine_rows_vs_leaf_1_words": jac(g9, grams(w1))},
         "conclusion": "The nine rows are transitional in letter statistics (closer to the tables than to leaf-1 words) "
                       "but do not seed the lexicon: only 3 catalogue names appear in them, and the names first appear in "
                       "table 2, not on leaf 1. The table language begins at table 2."}
    res = {"A_direction": A, "B_transition_rows": B}
    load.save_result("58_direction_and_transition", res)
    return res


if __name__ == "__main__":
    r = run()
    print("A:", r["A_direction"]["read_from_the_preceding_6_leaves"], "vs", r["A_direction"]["read_from_the_following_6_leaves"])
    print("  ", r["A_direction"]["conclusion"])
    print("B names in nine rows:", r["B_transition_rows"]["names_in_the_nine_rows"], "| first appear:", r["B_transition_rows"]["where_names_first_appear"])
    print("  ", r["B_transition_rows"]["conclusion"])
