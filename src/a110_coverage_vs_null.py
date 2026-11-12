"""
110 - Is the Loagaeth WOVEN from Angelical vocabulary above chance? Tiling coverage vs a Markov-3 null.

a109's tiling covers ~30% of a square's letters with dictionary words (Dee + Leitch), no letter reused. But a dense
grid of these same letters will spell SOME dictionary words by chance. The honest question: does the REAL book tile
to more coverage than a surrogate with the same local letter statistics? We tile every row of every table greedily
(longest dictionary word first, min length 3 to avoid trivial 2-letter fillers) and compare the letter-coverage
fraction of the real book to 10 Markov-3 surrogate books. Metaphysical lens: if the Loagaeth is truly a tongue of
names woven from the angelic vocabulary, its own text should carry that vocabulary denser than noise does.
"""
import json
import random
import unicodedata

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def build_lexicon(min_len):
    dee = {}
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for w in c["palavras"]:
            k = da(w["chave"])
            if len(k) >= min_len and k not in dee:
                dee[k] = 1
    try:
        for k in json.load(open(load.ROOT + "/viz/leitch_extra_lexicon.json", encoding="utf-8")):
            kk = da(k)
            if len(kk) >= min_len:
                dee[kk] = 1
    except Exception:
        pass
    return set(dee)


def tile_cover(text, vocab, min_len, maxw=9):
    """greedy longest-first tiling; return covered letter count."""
    i, cov, n = 0, 0, len(text)
    while i < n:
        hit = 0
        for L in range(min(maxw, n - i), min_len - 1, -1):
            if text[i:i + L] in vocab:
                hit = L
                break
        if hit:
            cov += hit
            i += hit
        else:
            i += 1
    return cov


def book_rows(book):
    rows = []
    for k in book:
        for r in book[k]:
            if r:
                rows.append(r)
    return rows


def coverage(rows, vocab, min_len):
    tot = cov = 0
    for r in rows:
        tot += len(r)
        cov += tile_cover(r, vocab, min_len)
    return cov / tot if tot else 0


def run(min_len=3):
    vocab = build_lexicon(min_len)
    book = base_book()
    rows = book_rows(book)
    real = coverage(rows, vocab, min_len)

    full = "".join(rows)
    surr = []
    for s in range(10):
        st = "".join(markov3(full, random.Random(1100 + s)))
        # cut surrogate into rows of the same lengths
        srows, p = [], 0
        for r in rows:
            srows.append(st[p:p + len(r)])
            p += len(r)
        surr.append(coverage(srows, vocab, min_len))
    mean = sum(surr) / len(surr)
    mx = max(surr)
    var = sum((x - mean) ** 2 for x in surr) / len(surr)
    sd = var ** 0.5
    z = (real - mean) / sd if sd else float("inf")

    verdict = ("CONFIRMADO: o Loagaeth é tecido de vocabulário angelical ACIMA do acaso — %.1f%% das letras cobertas "
               "por palavras (>=%d) vs %.1f%% média no surrogate (máx %.1f%%), z=%.1f. O texto carrega a língua dos "
               "nomes mais denso que o ruído." % (real * 100, min_len, mean * 100, mx * 100, z)) \
        if real > mx and z >= 3 else \
        ("sem sinal: cobertura real %.1f%% vs surrogate média %.1f%% (máx %.1f%%), z=%.1f — a grade densa gera "
         "tanto vocabulário por acaso quanto o livro; a cobertura não prova tecelagem." % (
             real * 100, mean * 100, mx * 100, z))

    res = {"min_len": min_len, "vocab": len(vocab), "real_coverage": round(real, 4),
           "surrogate_mean": round(mean, 4), "surrogate_max": round(mx, 4), "z": round(z, 1),
           "finding": verdict}
    load.save_result("110_coverage_vs_null", res)
    return res


if __name__ == "__main__":
    for ml in (3, 4):
        r = run(ml)
        print("min_len=%d (vocab %d): real %.1f%% | surrogate %.1f%% (max %.1f%%) | z=%.1f" % (
            ml, r["vocab"], r["real_coverage"] * 100, r["surrogate_mean"] * 100, r["surrogate_max"] * 100, r["z"]))
        print("  ", r["finding"], "\n")
