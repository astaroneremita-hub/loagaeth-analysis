"""
52 - Where do the six-letter formulas come from? Two imprints.

  A) The imprint of a language. A letter model (two letters of context) is trained on English (King
     James Bible) and on Latin (Caesar, De Bello Gallico V-VIII), both folded to the book's 21
     letters. How well does each read the tables, leaf 1, the Calls - and each other, for scale?
     Also the share of the letter pairs that mark each language (TH, SH, WH / QU, UM, US, IS ...).
  B) The imprint of a hand producing letters "at will". People who make up sequences avoid repeating
     a letter at once, alternate too regularly, and avoid clusters. Measures: a letter following
     itself, a letter returning after one other (ABA), vowel/consonant alternation, runs of three
     or more consonants, runs of two or more vowels - each as observed / expected from the text's
     own letter frequencies. Compared across the tables, leaf 1, the Calls, English, Latin, and
     the Soyga tables of the same manuscript (made by an arithmetic rule: no hand in them).

Control texts are fetched to data/raw/ (Project Gutenberg #10 and #18837) and not redistributed.
"""
import json
import os
import re
import statistics
from collections import Counter

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a44_positive_control import call_stream, kjv_words

LATIN = os.path.join(load.DATA, "raw", "latin_caesar.txt")
FOLD = {"J": "I", "V": "U", "W": "U", "K": "C", "Y": "I"}
VOW = set("AEIOU")


def fold(s):
    return "".join(FOLD.get(c, c) for c in s)


def latin_words(n):
    if not os.path.exists(LATIN):
        import urllib.request
        with urllib.request.urlopen("https://www.gutenberg.org/cache/epub/18837/pg18837.txt", timeout=60) as r, open(LATIN, "wb") as fh:
            fh.write(r.read())
    t = open(LATIN, encoding="utf-8", errors="ignore").read()
    t = t[t.find("*** START"):t.find("*** END")]
    t = t[t.find("\n", 2000):]
    out, k = [], 0
    for w in re.findall(r"[A-Za-z]+", t):
        out.append(w.upper())
        k += len(w)
        if k >= n:
            break
    return out


def soyga_stream():
    import a36_soyga_calibration as s
    return ["".join(c.upper() for row in T for c in row) for T in s.parse()]


def chunks(s, n=40):
    return [s[i:i + n] for i in range(0, len(s) - n + 1, n)]


def hand(lines):
    f = Counter(c for r in lines for c in r)
    N = sum(f.values())
    p2 = sum((v / N) ** 2 for v in f.values())
    pv = sum(v for c, v in f.items() if c in VOW) / N
    pairs = sum(len(r) - 1 for r in lines)
    tri = sum(len(r) - 2 for r in lines)
    same = sum(a == b for r in lines for a, b in zip(r, r[1:]))
    aba = sum(a == c and a != b for r in lines for a, b, c in zip(r, r[1:], r[2:]))
    alt = sum((a in VOW) != (b in VOW) for r in lines for a, b in zip(r, r[1:]))
    ccc = sum(all(x not in VOW for x in t) for r in lines for t in zip(r, r[1:], r[2:]))
    vv = sum(a in VOW and b in VOW for r in lines for a, b in zip(r, r[1:]))
    return {"letters": N, "vowel_share": round(pv, 3),
            "letter_follows_itself": round(same / (pairs * p2), 3),
            "letter_returns_after_one_other_ABA": round(aba / (tri * (p2 - sum((v / N) ** 3 for v in f.values()))), 3),
            "vowel_consonant_alternation": round(alt / (pairs * 2 * pv * (1 - pv)), 3),
            "three_consonants_in_a_row": round(ccc / (tri * (1 - pv) ** 3), 3),
            "two_vowels_in_a_row": round(vv / (pairs * pv * pv), 3)}


def run():
    book = base_book()
    tables = [fold(r) for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if r]
    n = sum(len(r) for r in tables)
    eng_w, lat_w = [fold(w) for w in kjv_words(n)], [fold(w) for w in latin_words(n)]
    eng, lat = chunks("".join(eng_w)), chunks("".join(lat_w))
    leaf1 = chunks(fold("".join(load.spaced_words(1))))
    calls = chunks(fold("".join(call_stream())))
    soyga = [fold(x) for s in soyga_stream() for x in chunks(s)]
    texts = {"tables 2-24": tables, "leaf 1": leaf1, "the Calls": calls, "English": eng, "Latin": lat, "Soyga tables (rule-made)": soyga}

    half = lambda x: (x[0::2], x[1::2])
    (e_tr, e_te), (l_tr, l_te) = half(eng), half(lat)
    me, ml = CharLM(2, alpha=0.5).fit(e_tr), CharLM(2, alpha=0.5).fit(l_tr)
    A = {}
    for name, L in texts.items():
        test = e_te if name == "English" else l_te if name == "Latin" else L
        be, bl = me.bits(test), ml.bits(test)
        A[name] = {"bits_per_letter_read_as_English": round(be, 3), "read_as_Latin": round(bl, 3),
                   "closer_to": "English" if be < bl else "Latin", "by_bits": round(abs(be - bl), 3)}
    marks = {"English marks": ["TH", "SH", "GH", "EA", "OU", "OW", "LL", "EE", "OO"], "Latin marks": ["QU", "UM", "US", "IS", "AE", "UE", "NT", "RE", "ER"],
             "the book's own": ["CH", "AX", "OX", "DN", "NZ", "ZA", "PH", "AH", "OH"]}
    pairs = {}
    for name, L in texts.items():
        c = Counter(r[i:i + 2] for r in L for i in range(len(r) - 1))
        tot = sum(c.values())
        pairs[name] = {g: round(1000 * sum(c[x] for x in ps) / tot, 1) for g, ps in marks.items()}
        pairs[name]["commonest pairs"] = [x for x, _ in c.most_common(8)]
    B = {name: hand(L) for name, L in texts.items()}
    res = {"A_read_as_a_language": A, "A_marker_pairs_per_1000": pairs, "B_signs_of_a_hand": B}
    load.save_result("52_origin_of_formulas", res)
    return res


if __name__ == "__main__":
    r = run()
    for k, v in r.items():
        print(k)
        for a, b in v.items():
            print("  ", a, b)
