"""
51 - The points between words: a gold standard that was in the source all along.

In the first tables the manuscript separates words with a point, and Peterson's transcription keeps
those points and the accents (a b í m a c h a.v o r t.n a l v m. ...). Our loader kept letters only,
so every earlier module read these tables as unbroken rows. (A reader of this study pointed the
points out; the diaries confirm they divide words.) They cover tables 2a, 2b, 3a, 3b in full and
parts of 4a, 4b, 5a: 232 rows.

  A) Inventory: rows, words, lengths, the commonest words.
  B) Do rows end where words end? Rows that end with a point; and for rows that do not, whether the
     last piece joined to the first word of the next row makes a word seen elsewhere.
  C) Our names against the points: catalogue names in these rows - a whole word, inside a word, or
     cut by a point - against the same names moved to random places in the row.
  D) Our segmenters against the points: the word model trained on leaf 1 (a21) and a letter-surprise
     cutter, scored on boundaries; chance = the same number of cuts placed at random.
  E) Accents: where the stress mark falls in the word.
  F) Word order, tested on real words at last: pairs of neighbouring words that recur, against the
     same words in random order inside each side; the Bible, cut to the same sizes, as control.

Writes data/loagaeth_word_points.json (positions of points and accents per row; no text).
"""
import html
import json
import math
import os
import random
import re
import statistics
import unicodedata
from collections import Counter

import load
from a19_machine import CharLM
from a21_index_heptarchy_numbers import Seg

RAW = os.path.join(load.DATA, "raw", "sl3189.htm")
ACC = set("́̄̀̂̋̍̈")


def parse():
    if not os.path.exists(RAW):
        import a18_markup_decoding
        a18_markup_decoding.fetch()
    h = open(RAW, encoding="latin-1").read()
    t = html.unescape(re.sub(r"<[^>]+>", "\n", h))
    lv = load.leaves()
    idx = {}
    for k, v in lv.items():
        for i, r in enumerate(v):
            idx.setdefault(load.letters(r), (k, i))
    out = {}
    for l in t.split("\n"):
        if not re.search(r"[a-zA-Z]\.[a-zA-Z]", l) or len(l) < 30 or re.search(r"[a-z]{4,} [a-z]{4,}", l):
            continue
        s = unicodedata.normalize("NFD", re.sub(r"^\s*\d+\.?\s*", "", l))
        letters, cuts, acc = [], [], []
        for ch in s:
            if ch.isalpha() and ch.upper() in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                letters.append(ch.upper())
            elif ch == ".":
                cuts.append(len(letters))
            elif ch in ACC and letters:
                acc.append(len(letters) - 1)
        L = "".join(letters)
        if L in idx:
            k, i = idx[L]
            out.setdefault(k, {})[i] = {"letters": L, "cuts": sorted(set(c for c in cuts if 0 < c <= len(L))), "accents": acc}
    return out


def words_of(row):
    L, cuts = row["letters"], [c for c in row["cuts"] if c < len(row["letters"])]
    b = [0] + cuts + [len(L)]
    return [L[x:y] for x, y in zip(b, b[1:]) if y > x]


def run():
    rng = random.Random(51)
    G = parse()
    faces = sorted(G, key=lambda k: (int(k[:-1]), k))
    rows = [(k, i, G[k][i]) for k in faces for i in sorted(G[k])]
    W = [w for _, _, r in rows for w in words_of(r)]
    wc = Counter(W)
    A = {"sides": {k: len(G[k]) for k in faces}, "rows": len(rows), "words": len(W), "different_words": len(wc),
         "mean_length": round(statistics.mean(map(len, W)), 2),
         "length_distribution": {n: c for n, c in sorted(Counter(min(len(w), 12) for w in W).items())},
         "written_once": sum(1 for c in wc.values() if c == 1),
         "commonest": [[w, c] for w, c in wc.most_common(25)]}

    # B: row ends
    end_point = sum(1 for _, _, r in rows if len(r["letters"]) in r["cuts"])
    interior = Counter(w for _, _, r in rows for w in words_of(r)[1:-1])
    pairs = []
    for k in faces:
        for i in sorted(G[k]):
            if i + 1 in G[k] and len(G[k][i]["letters"]) not in G[k][i]["cuts"]:
                pairs.append((words_of(G[k][i])[-1], words_of(G[k][i + 1])[0]))

    def score(ps):
        return (sum(a + b in interior for a, b in ps), sum(a in interior for a, _ in ps), sum(b in interior for _, b in ps))
    real = score(pairs)
    nul = []
    firsts = [b for _, b in pairs]
    for _ in range(1000):
        rng.shuffle(firsts)
        nul.append(score([(a, b) for (a, _), b in zip(pairs, firsts)])[0])
    edge_last = [len(words_of(G[k][i])[-1]) for k in faces for i in sorted(G[k])]
    edge_first = [len(words_of(G[k][i])[0]) for k in faces for i in sorted(G[k])]
    inner = [len(w) for _, _, r in rows for w in words_of(r)[1:-1]]
    sim = []
    for _ in range(20):
        ws = W[:]
        rng.shuffle(ws)
        p = 0
        for w in ws:
            a, b = p, p + len(w)
            if a // 49 != (b - 1) // 49:
                c = (b - 1) // 49 * 49
                sim += [c - a, b - c]
            p = b
    B = {"mean_length_of_last_word_of_a_row": round(statistics.mean(edge_last), 2),
         "mean_length_of_first_word_of_a_row": round(statistics.mean(edge_first), 2),
         "mean_length_of_words_inside_rows": round(statistics.mean(inner), 2),
         "mean_length_of_the_pieces_if_rows_cut_words_blindly": round(statistics.mean(sim), 2),
         "rows_ending_with_a_point": end_point, "of_rows": len(rows),
         "share_expected_if_rows_cut_words_blindly": round(1 / A["mean_length"], 3),
         "rows_without_final_point_followed_by_a_row": len(pairs),
         "last_piece_plus_first_word_is_a_known_word": real[0], "same_with_rows_paired_at_random": round(statistics.mean(nul), 2),
         "p": round((sum(v >= real[0] for v in nul) + 1) / 1001, 4),
         "last_piece_alone_is_a_known_word": real[1], "first_word_alone_is_a_known_word": real[2],
         "examples_joined": [a + "+" + b for a, b in pairs if a + b in interior][:8]}

    # C: names against the points
    d23 = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    names = sorted({x["name"] for x in d23} | {"CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"})
    tally, nulc, per = Counter(), [], Counter()
    occ = []
    for _, _, r in rows:
        L, cuts = r["letters"], set(r["cuts"]) | {0, len(r["letters"])}
        for n in names:
            p = L.find(n)
            while p >= 0:
                occ.append((len(L), cuts, p, len(n)))
                inner = any(p < c < p + len(n) for c in cuts)
                kind = "cut by a point" if inner else "a whole word" if p in cuts and p + len(n) in cuts else \
                    "starts a word" if p in cuts else "ends a word" if p + len(n) in cuts else "inside a word"
                tally[kind] += 1
                per[(n, kind)] += 1
                p = L.find(n, p + 1)
    for _ in range(500):
        k = 0
        for ln, cuts, p, n in occ:
            q = rng.randrange(0, ln - n + 1)
            k += any(q < c < q + n for c in cuts)
        nulc.append(k)
    C = {"name_occurrences_in_pointed_rows": len(occ), "how_they_sit": dict(tally),
         "cut_by_a_point_if_placed_at_random": round(statistics.mean(nulc), 1),
         "z": round((tally["cut by a point"] - statistics.mean(nulc)) / (statistics.pstdev(nulc) or 1e-9), 1),
         "by_name": {n: {k: v for (m, k), v in per.items() if m == n} for n in sorted({m for m, _ in per})}}

    # D: segmenters
    seg = Seg(load.spaced_words(2))
    lm = CharLM(3, alpha=0.1).fit([load.letters(r) for k, v in load.leaves().items() if k[:-1].isdigit() and 6 <= int(k[:-1]) <= 24 for r in v if load.letters(r)])

    def f1(pred):
        tp = fp = fn = 0
        for (_, _, r), cuts in zip(rows, pred):
            g = {c for c in r["cuts"] if 0 < c < len(r["letters"])}
            tp += len(g & cuts)
            fp += len(cuts - g)
            fn += len(g - cuts)
        p, rc = tp / max(1, tp + fp), tp / max(1, tp + fn)
        return round(2 * p * rc / max(1e-9, p + rc), 3), round(p, 3), round(rc, 3), tp + fp

    def surprise_cuts(L, thr):
        s = [-math.log2(lm.prob(("^^^" + L)[i:i + 3], L[i])) for i in range(len(L))]
        return {i for i in range(1, len(L) - 1) if s[i] > thr and s[i] >= s[i - 1] and s[i] >= s[i + 1]}
    v = f1([seg.cuts(r["letters"]) for _, _, r in rows])
    best = max((f1([surprise_cuts(r["letters"], t) for _, _, r in rows]) + (t,) for t in (2.5, 3, 3.5, 4, 4.5, 5)), key=lambda x: x[0])
    ncuts = sum(len([c for c in r["cuts"] if 0 < c < len(r["letters"])]) for _, _, r in rows)
    rnd = statistics.mean(f1([set(rng.sample(range(1, len(r["letters"])), min(len(r["letters"]) - 1, len(r["cuts"])))) for _, _, r in rows])[0] for _ in range(20))
    D = {"points_inside_rows": ncuts,
         "word_model_from_leaf_1": {"F1": v[0], "precision": v[1], "recall": v[2]},
         "letter_surprise_peaks": {"F1": best[0], "precision": best[1], "recall": best[2], "threshold_bits": best[4]},
         "random_cuts_F1": round(rnd, 3)}

    # E: accents
    pos, nacc = Counter(), Counter()
    for _, _, r in rows:
        L = r["letters"]
        b = [0] + [c for c in r["cuts"] if c < len(L)] + [len(L)]
        for x, y in zip(b, b[1:]):
            a = [i for i in r["accents"] if x <= i < y]
            nacc[min(len(a), 2)] += 1
            w = L[x:y]
            vow = [i for i, ch in enumerate(w) if ch in "AEIOUVY"]
            for i in a:
                later = sum(1 for j in vow if j > i - x)
                pos["last vowel" if later == 0 else "next to last" if later == 1 else "third from the end or earlier"] += 1
    E = {"words_without_accent": nacc[0], "with_one": nacc[1], "with_two_or_more": nacc[2], "accent_falls_on": dict(pos)}

    # F: word order
    def repeated_bigrams(seqs):
        c = Counter(p for s in seqs for p in zip(s, s[1:]))
        return sum(v for v in c.values() if v > 1)

    def order_test(seqs):
        real = repeated_bigrams(seqs)
        nul = []
        for _ in range(500):
            sh = []
            for s in seqs:
                t = s[:]
                rng.shuffle(t)
                sh.append(t)
            nul.append(repeated_bigrams(sh))
        return {"neighbouring_pairs_that_recur": real, "words_in_random_order": round(statistics.mean(nul), 1),
                "z": round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
                "p": round((sum(x >= real for x in nul) + 1) / 501, 4)}
    seqs = [[w for i in sorted(G[k]) for w in words_of(G[k][i])] for k in faces]
    from a44_positive_control import call_stream, kjv_words
    kw = kjv_words(20000)
    once = lambda ws: round(sum(1 for c in Counter(ws).values() if c == 1) / max(1, len(ws)), 3)
    bible, i = [], 0
    for s in seqs:
        bible.append(kw[i:i + len(s)])
        i += len(s)
    F = {"tables": order_test(seqs), "bible_same_number_of_words": order_test(bible),
         "share_of_words_written_once": {"tables": round(A["written_once"] / len(W), 3),
                                         "leaf_1_spaced_words": once(load.spaced_words(1)[:len(W)]),
                                         "the_calls": once(call_stream()),
                                         "bible": once(kw[:len(W)])}}

    with open(os.path.join(load.DATA, "loagaeth_word_points.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": {"description": "Word points and accents of tables 2a-5a as positions in each row (letters counted from 0; a cut at n stands before letter n). Source: Peterson's transcription. Module a51."},
                   "sides": {k: {str(i): {"cuts": G[k][i]["cuts"], "accents": G[k][i]["accents"]} for i in sorted(G[k])} for k in faces}}, fh, indent=0)
    res = {"A_inventory": A, "B_row_ends": B, "C_names_against_points": C, "D_segmenters": D, "E_accents": E, "F_word_order": F}
    load.save_result("51_word_points", res)
    return res


if __name__ == "__main__":
    r = run()
    for k, v in r.items():
        print(k)
        for a, b in v.items():
            print("  ", a, b)
