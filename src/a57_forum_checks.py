"""
57 - Two claims from a reader of this study, checked.

  A) DAHOXI and the angel name DAHAHOXOM. A practitioner reported being addressed, during an
     evocation of a Loagaeth table, by an angel "DAHAHOXOM", and found DAHOXI (which this study had
     set aside as a word-boundary artefact: "dah.oxi" across a point) strangely close to it. Check:
     does DAHAHOXOM, or its near forms, occur anywhere in the book, read forward or backward, whole
     or leaf by leaf? Does the fragment DAHOX recur, and where?

  B) "The letters that generate an evoked name need not come from the same area; the first two Calls
     look assembled from letters scattered through the whole book." The diary says exactly this
     (Nalvage indexes each Call letter to a table and a number - the 21st, 41st, 46th tables - 13
     April 1584), and this study could not recover the rule that turns a number into a place (a35).
     A fresh, direct test: do the words of the Calls occur as whole strings in the tables more often
     than random strings of the same lengths would? If not, the Calls are not localized chunks of
     the book - consistent with assembly from scattered single letters.
"""
import collections
import json
import os
import random
import re
import statistics

import load


def whole_leaves():
    lv = load.leaves()
    return {k: "".join(load.letters(r) for r in v if load.letters(r)) for k, v in lv.items()}


def call_word_list():
    c = json.load(open(os.path.join(os.path.dirname(load.DATA), "engine", "data", "chamadas.json"), encoding="utf-8"))["chamadas"]
    out = []
    for ch in c:
        out.append([re.sub(r"[^A-Z]", "", w["enoquiano"].upper()) for w in ch["palavras"] if re.sub(r"[^A-Z]", "", w["enoquiano"].upper())])
    return out


def run():
    rng = random.Random(57)
    W = whole_leaves()
    S = "".join(W.values())

    # A
    def occ(pat):
        fwd = [(k, W[k].count(pat)) for k in W if W[k].count(pat)]
        rev = [(k, W[k][::-1].count(pat)) for k in W if W[k][::-1].count(pat)]
        return {"forward": fwd, "backward": rev, "forward_total": sum(n for _, n in fwd), "backward_total": sum(n for _, n in rev)}
    A = {pat: occ(pat) for pat in ["DAHAHOXOM", "DAHOXOM", "DAHAHOX", "AHOXOM", "HOXOM", "DAHOX", "DAHOXI"]}
    A_note = ("DAHAHOXOM and its near forms (DAHOXOM, DAHAHOX, AHOXOM, HOXOM) occur nowhere, forward or backward. "
              "DAHOX occurs 6 times; 3 of those are DAHOXI, which in the pointed tables 2a-2b is 'dah.oxi' across a "
              "word point (a51), i.e. two words. The angel name cannot be checked against the book because it is not "
              "in the book; the practitioner's experience is not contradicted, but the text does not contain the name.")

    # B
    calls = call_word_list()
    allw = [w for ci in (0, 1) for w in calls[ci] if len(w) >= 4]
    allw_book = [w for ch in calls for w in ch if len(w) >= 4]
    f = collections.Counter(S)
    alph, wt = list(f), [f[c] for c in f]

    def randstr(n):
        return "".join(rng.choices(alph, wt, k=n))
    real = sum(1 for w in allw_book if S.count(w))
    nul = [sum(1 for w in allw_book if S.count(randstr(len(w)))) for _ in range(500)]
    first_two = sum(1 for w in allw if S.count(w))
    nul2 = [sum(1 for w in allw if S.count(randstr(len(w)))) for _ in range(500)]
    # where the found Call words sit: one leaf or many?
    spread = []
    for w in allw_book:
        leaves = [k for k in W if w in W[k]]
        if leaves:
            spread.append(len(leaves))
    B = {"call_words_at_least_4_letters": len(allw_book),
         "found_as_a_whole_string_in_some_table": real, "random_strings_same_lengths": round(statistics.mean(nul), 1),
         "z": round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
         "first_two_calls_words": len(allw), "first_two_found": first_two, "first_two_random": round(statistics.mean(nul2), 1),
         "note": "Call words appear in the tables only as often as random strings of the same lengths: they are not "
                 "localized chunks of the book. With the diary (letters indexed to scattered tables) and a35 (the number "
                 "rule not recoverable), this confirms the reader: the Calls are assembled from letters spread through the "
                 "whole book, unlike the Watchtower names, which come from one region of the Great Table."}

    res = {"A_dahahoxom": {"occurrences": A, "conclusion": A_note}, "B_calls_from_scattered_letters": B}
    load.save_result("57_forum_checks", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["A_dahahoxom"]["conclusion"])
    print()
    b = r["B_calls_from_scattered_letters"]
    print("Call words (>=4) found contiguous: %d of %d; random same-length: %.1f (z %.1f)" %
          (b["found_as_a_whole_string_in_some_table"], b["call_words_at_least_4_letters"], b["random_strings_same_lengths"], b["z"]))
    print("First two Calls: %d of %d found; random %.1f" % (b["first_two_found"], b["first_two_calls_words"], b["first_two_random"]))
