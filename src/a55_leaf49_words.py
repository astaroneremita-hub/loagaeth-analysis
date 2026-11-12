"""
55 - The 21 words of the 49th leaf, given in the diary.

The 49th leaf (the "first leaf which is the last of the Book") was never in our data. Galvah dictates
its words on 18 June 1583 (A True and Faithful Relation, PDF 113-114): twenty-one words, to be set in
five small tables of 21 letters. As printed they are:

    Loagaeth seg lovi brtnc | Larzed dox ner habzilb adnor | doncha Larb vors hirobra |
    exi vr zednip taiip chimvane | chermach lendix nor zandox

(22 tokens as printed; one division is doubtful. Galvah: "There are onely the words of the first
leaf"; of them "not to be uttered".)

Tested here, read-only, against the rest:
  A) Do these words occur in the tables (2-48), and in leaf 1 (Dee's spaced words)?
  B) How do they read under a letter model of the tables, of leaf 1, and of the Calls? Where do they
     sit between those registers?
  C) Are any of them, or their pieces, the recurring names of the catalogue?
  D) Their letters: the vowel share, the doubled-letter rate, and the three consonant clusters
     (brtnc, habzilb, zednip) that do not look like table text - do they fit the tables or leaf 1?
"""
import json
import os
import statistics
from collections import Counter

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a33_diary_anchors import call_words

WORDS = ["LOAGAETH", "SEG", "LOVI", "BRTNC", "LARZED", "DOX", "NER", "HABZILB", "ADNOR", "DONCHA",
         "LARB", "VORS", "HIROBRA", "EXI", "VR", "ZEDNIP", "TAIIP", "CHIMVANE", "CHERMACH", "LENDIX", "NOR", "ZANDOX"]
VOW = set("AEIOUVY")


def fold(s):
    return s.replace("V", "U").replace("J", "I").replace("Y", "I").replace("K", "C").replace("W", "U")


def run():
    book = base_book()
    S = "|".join(r for k, v in book.items() for r in v if r)
    one = [load.letters(w) for r in load.leaves().get("1a", []) + load.leaves().get("1b", []) for w in r.split() if load.letters(w)]
    oneS = "|".join(one)
    words = [w for w in WORDS]

    # A: occurrence
    occ = []
    for w in words:
        occ.append({"word": w, "in_tables": S.count(w), "in_leaf_1_words": sum(w == x for x in one),
                    "as_substring_of_a_leaf_1_word": sum(w in x for x in one)})

    # B: registers
    tab = CharLM(3, alpha=0.3).fit([r for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if r])
    lf1 = CharLM(3, alpha=0.3).fit(one)
    cal = CharLM(2, alpha=0.5).fit([fold(w) for w in call_words()[1]])
    reg = {"the 49th-leaf words": {"under tables model": round(tab.bits(words), 2), "under leaf-1 model": round(lf1.bits(words), 2),
                                   "under Calls model": round(cal.bits([fold(w) for w in words]), 2)},
           "for scale - leaf 1 words": {"under tables model": round(tab.bits(one[:200]), 2), "under leaf-1 model": round(lf1.bits(one[:200]), 2)},
           "for scale - a table row": {"under tables model": round(tab.bits([r for r in book["6a"] if r][:20]), 2)}}

    # C: names of the catalogue
    d23 = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    names = sorted({x["name"] for x in d23} | {"CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"}, key=len, reverse=True)
    pieces = {}
    for w in words:
        hits = [n for n in names if n in w or w in n]
        if hits:
            pieces[w] = hits
    # DONCHA vs DONCHAL (catalogue), ADNOR vs ADNOCHA, NOR fragment
    allw = "".join(words)
    C = {"words_holding_or_held_by_a_catalogue_name": pieces,
         "note": "DONCHA is the catalogue name DONCHAL minus its last letter; ADNOR shares AD-NO- with ADNOCHA; NOR, VORS, DOX recur widely as fragments."}

    # D: letter statistics
    def stat(ws):
        s = "".join(ws)
        f = Counter(s)
        n = len(s)
        pairs = sum(len(w) - 1 for w in ws)
        same = sum(a == b for w in ws for a, b in zip(w, w[1:]))
        cc3 = sum(all(x not in VOW for x in t) for w in ws for t in zip(w, w[1:], w[2:]))
        return {"letters": n, "vowel_share": round(sum(v for c, v in f.items() if c in VOW) / n, 3),
                "doubled_letters": same, "three_consonant_clusters": cc3,
                "mean_word_length": round(statistics.mean(len(w) for w in ws), 2)}
    D = {"the 49th-leaf words": stat(words), "leaf 1 words": stat(one),
         "clusters_flagged": [w for w in words if any(all(c not in VOW for c in w[i:i + 3]) for i in range(len(w) - 2))]}

    res = {"A_occurrence": occ, "B_registers_bits_per_letter": reg, "C_catalogue_names": C, "D_letters": D,
           "words": words, "token_count": len(words), "note": "21 words as printed give 22 tokens; one division is doubtful (notes_tfr.md)."}
    load.save_result("55_leaf49_words", res)
    return res


if __name__ == "__main__":
    r = run()
    print("occurrence in tables / leaf-1-words / as substring:")
    for o in r["A_occurrence"]:
        print("  %-9s %2d %2d %2d" % (o["word"], o["in_tables"], o["in_leaf_1_words"], o["as_substring_of_a_leaf_1_word"]))
    print("registers:", json.dumps(r["B_registers_bits_per_letter"], ensure_ascii=False))
    print("catalogue pieces:", r["C_catalogue_names"]["words_holding_or_held_by_a_catalogue_name"])
    print("letters:", json.dumps(r["D_letters"], ensure_ascii=False))
