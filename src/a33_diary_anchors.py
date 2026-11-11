"""
33 - Dee's own record put to the test (Sloane 3188, Liber Quintus and Appendix, March-May 1583;
     True & Faithful Relation, 1583-1585).

Dee's margins give meanings for about 30 words of leaf 1, and the angels make statements about the
book. Each is turned into a test on the tables.

  A) The glossed words of leaf 1 (GLOSSES below, Dee's own marginal notes): do they occur in the
     tables 2-48 beyond a Markov-3 expectation, and as words (varied neighbours)?
  B) "Read from the right hand to the left" (26 Mar 1583). Which direction of our transcription is the
     reading direction? Leaf 1 is written out in reading order with spaces. A letter model of leaf-1
     words (and one of the Calls' words) reads the table rows as transcribed and reversed.
  C) "The first leaf is the last of the book" (18 Jun 1583). Is leaf 1 closest to the end of the book?
     Models of the five parts (a27) read leaf 1; and the 21 words dictated that day as "the words of
     the first leaf" (table 49).
  D) "Call 1 belongs to table 2" (11 Jul 1584): Calls 1-18 -> tables 2-19. Does Call n share more
     letter 4-grams with table n+1 than with the other tables? Permutation of the assignment.
  E) "The eighteenth leaf was of the spirits of the earth" (15 Apr 1583): what sets table 18 apart
     (descriptive).
"""
import json
import math
import os
import random
import statistics
from collections import Counter, defaultdict

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a23_name_discovery import M3, H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Dee's marginal glosses on leaf 1 (Sloane 3188, 3-6 April 1583), spelling normalised to A-Z.
GLOSSES = {
    "GOHED": "one everlasting, all things descending upon one", "CANSE": "mighty", "CRISCANSE": "more mighty",
    "POLA": "two together", "PALA": "two separated", "GIALSAGEN": "the divine power creating the angel of the sun",
    "NA": "the name of the Trinity", "GASCAMPHO": "why didst thou so (as God said to Lucifer)",
    "ARGEDCO": "with humility we call thee", "BEFES": "vocative of Befafes", "ARZULGH": "spirit contrary to Befafes",
    "ORH": "God without end", "TOHCOTH": "name comprehending all the fairies", "PADGZE": "justice from divine power",
    "CONGAMPHLGH": "faith that reviveth man's breast; the Holy Ghost", "IUSMACH": "begotten",
    "PHAMAH": "I will give", "ARPHE": "I desire thee, O God", "APACHANA": "the slimy things made of dust",
    "LU": "from one", "IUREHOH": "what Christ did in hell", "NOSTOAH": "it was in the beginning",
    "AMGEDPHA": "I will begin anew", "ADGMACH": "much glory", "GEMEGANZA": "your will be done",
    "GAHOACHMA": "I am that I am", "CHRAMSA": "be it made with power", "IAISG": "everlasting one and indivisible God",
}
WORDS_21 = ("LOAGAETH SEG LOVI BRTNC LARZED DOX NER HABZILB ADNOR DONCHA LARB VORS HIROBRA EXI VR ZEDNIP "
            "TAIIP CHIMVANE CHERMACH LENDIX NOR ZANDOX").split()
PARTS = {"I 2-12": range(2, 13), "II 13-25": range(13, 26), "III 26-33": range(26, 34),
         "IV 34-40": range(34, 41), "V 41-48": range(41, 49)}


def norm(s):
    import a21_index_heptarchy_numbers as a21
    return a21.norm(s)


def A_glossed_words(book):
    lines = [r.replace("V", "U") for v in book.values() for r in v]
    m3 = M3(lines)
    npos = sum(len(r) for r in lines)
    out = []
    for w, g in GLOSSES.items():
        w = w.replace("V", "U")
        if len(w) < 4:
            continue
        L, R, c = Counter(), Counter(), 0
        for r in lines:
            st = 0
            while True:
                i = r.find(w, st)
                if i < 0:
                    break
                c += 1
                L[r[i - 1] if i else "#"] += 1
                R[r[i + len(w)] if i + len(w) < len(r) else "#"] += 1
                st = i + 1
        e = m3.expected(w, npos)
        out.append({"word": w, "gloss": g, "in_tables": c, "markov3_expected": round(e, 2),
                    "z": round((c - e) / math.sqrt(e), 1) if e > 0 else None,
                    "h_left": round(H(L), 2) if c else None, "h_right": round(H(R), 2) if c else None})
    out.sort(key=lambda r: -(r["in_tables"]))
    return {"glossed_words_tested": len(out), "found_at_all": sum(1 for r in out if r["in_tables"]),
            "total_found": sum(r["in_tables"] for r in out),
            "total_expected": round(sum(r["markov3_expected"] for r in out), 1), "words": out}


def leaf1_words():
    import a21_index_heptarchy_numbers as a21
    lv = load.leaves()
    return [t for leaf in ["1a", "1b"] for r in lv[leaf] if len(r.split()) > 1 for t in a21.wtoks(r) if len(t) >= 3]


def call_words():
    c = json.load(open(os.path.join(ROOT, "engine", "data", "chamadas.json"), encoding="utf-8"))["chamadas"]
    return c, [norm(w["enoquiano"]) for ch in c for w in ch["palavras"] if len(norm(w["enoquiano"])) >= 3]


def B_direction(book):
    rows = [r.replace("V", "U") for k, v in book.items() if tnum(k) <= 24 for r in v]
    dia = [r.replace("V", "U") for k, v in book.items() if 29 <= tnum(k) <= 43 for r in v]
    out = {}
    for lab, words in (("leaf-1 words (Dee's spaced text)", leaf1_words()), ("words of the Calls", call_words()[1])):
        m = CharLM(2, alpha=0.5).fit(words)
        # words are short: score the inside of rows only, in windows, so that word-edge effects of the
        # training do not favour either direction; both directions use the same windows
        def bits(L, rev):
            segs = [(r[::-1] if rev else r) for r in L]
            return m.bits(segs)
        out[lab] = {"rows_2_24_as_transcribed": round(bits(rows, False), 3), "rows_2_24_reversed": round(bits(rows, True), 3),
                    "diamonds_as_stored": round(bits(dia, False), 3), "diamonds_reversed": round(bits(dia, True), 3)}
    return out


def C_first_is_last(book):
    l1 = leaf1_words()
    w21 = [norm(w) for w in WORDS_21]
    out = {}
    for p, rg in PARTS.items():
        L = [r.replace("V", "U") for k, v in book.items() if tnum(k) in rg for r in v]
        m = CharLM(2, alpha=0.5).fit(L)
        out[p] = {"leaf1_words_bits": round(m.bits(l1), 3), "the_21_words_bits": round(m.bits(w21), 3)}
    return out


def D_calls_to_tables(book, rng):
    calls, _ = call_words()
    by_t = defaultdict(list)
    for k, v in book.items():
        by_t[tnum(k)] += v
    def g4(strings):
        c = set()
        for s in strings:
            s = s.replace("V", "U")
            c.update(s[i:i + 4] for i in range(len(s) - 3))
        return c
    T = {t: g4(by_t[t]) for t in range(2, 20)}
    C = {}
    for ch in calls:
        try:
            n = int(ch["numero"])
        except ValueError:
            continue
        if 1 <= n <= 18:
            C[n] = g4(["".join(norm(w["enoquiano"]) for w in ch["palavras"])]) | g4([norm(w["enoquiano"]) for w in ch["palavras"]])
    ns = sorted(C)
    S = {(n, t): len(C[n] & T[t]) / max(1, len(C[n])) for n in ns for t in T}
    def score(assign):
        return sum(S[(n, assign[n])] for n in ns)
    obs = score({n: n + 1 for n in ns})
    ts = [n + 1 for n in ns]
    nul = []
    for _ in range(5000):
        p = ts[:]
        rng.shuffle(p)
        nul.append(score(dict(zip(ns, p))))
    rank = [sorted(T, key=lambda t: -S[(n, t)]).index(n + 1) for n in ns]
    return {"calls": len(ns), "shared_4gram_share_own_table_sum": round(obs, 3), "permuted_mean": round(statistics.mean(nul), 3),
            "p": round((sum(v >= obs for v in nul) + 1) / 5001, 4),
            "rank_of_own_table_per_call_0_best_of_18": rank, "mean_rank": round(statistics.mean(rank), 2), "chance_mean_rank": 8.5}


def E_table18(book):
    by_t = defaultdict(list)
    for k, v in book.items():
        by_t[tnum(k)] += v
    def grams(L, k=6):
        return Counter(g for r in L for g in (r[i:i + k] for i in range(len(r) - k + 1)))
    g18 = grams(by_t[18])
    rest = Counter()
    for t, L in by_t.items():
        if t != 18:
            rest.update(grams(L))
    n18, nr = sum(g18.values()), sum(rest.values())
    dist = sorted(((g, c, rest[g]) for g, c in g18.items() if c >= 4), key=lambda x: -(x[1] / n18) / ((x[2] + 0.5) / nr))[:10]
    letters = Counter("".join(by_t[18]))
    allc = Counter("".join(r for L in by_t.values() for r in L))
    en = {L: round((letters[L] / sum(letters.values())) / (allc[L] / sum(allc.values())), 2) for L in allc if allc[L] > 500}
    return {"most_distinctive_6grams": [{"string": g, "in_18": c, "elsewhere": r} for g, c, r in dist],
            "letters_most_enriched": sorted(en.items(), key=lambda kv: -kv[1])[:4],
            "letters_most_depleted": sorted(en.items(), key=lambda kv: kv[1])[:4]}


def run():
    rng = random.Random(33)
    book = base_book()
    res = {"source": "Dee's marginal glosses and the angels' statements, Sloane 3188 (Peterson's edition) and "
                     "A True & Faithful Relation (EEBO-TCP A37412).",
           "A_glossed_words_in_tables": A_glossed_words(book),
           "B_reading_direction": B_direction(book),
           "C_first_leaf_is_last": C_first_is_last(book),
           "D_call_n_to_table_n_plus_1": D_calls_to_tables(book, rng),
           "E_table_18": E_table18(book)}
    load.save_result("33_diary_anchors", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
