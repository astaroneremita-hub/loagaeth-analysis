"""
113 (Bloco C) - Does any square literally spell a CALL in order? The decisive 'sense' test.

A square makes literal sense if, reading along a line, the Call words appear in the SAME order Dee received them.
For every line (rows, columns, both diagonals, forward + reversed) we tile the Dee Call vocabulary and then find the
longest run of consecutive matched words that all belong to ONE Call with strictly increasing position-in-call. A
long ordered run = the grid encodes a passage of that Call. Null: the same pipeline on a Markov-3 surrogate book. If
the real book's best ordered run beats the surrogate with margin, there is a literal reading; if not, the squares do
not hide the Calls in order - they are a name-field, as Blocos A/B concluded.
"""
import json
import random
import unicodedata
from collections import defaultdict

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def call_index():
    """chave -> set of (call#, pos_in_call); and the Dee vocab set (len>=2)."""
    idx = defaultdict(set)
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for w in c["palavras"]:
            k = da(w["chave"])
            if len(k) >= 2:
                idx[k].add((c["numero"], w["pos"]))
    return idx


def lines_of(grid):
    R = len(grid)
    out = []
    for r in range(R):
        out.append([(r, cc) for cc in range(R)])
    for cc in range(R):
        out.append([(r, cc) for r in range(R)])
    for s in range(R):
        out.append([(s + k, k) for k in range(R - s)])
        if s:
            out.append([(k, s + k) for k in range(R - s)])
    for s in range(R):
        out.append([(s + k, R - 1 - k) for k in range(R - s)])
        if s:
            out.append([(k, R - 1 - s - k) for k in range(R - s)])
    return out


def tile_words(text, vocab, minlen=2, maxw=9):
    """greedy longest-first; return list of matched words in reading order."""
    seq, i, n = [], 0, len(text)
    while i < n:
        hit = 0
        for L in range(min(maxw, n - i), minlen - 1, -1):
            if text[i:i + L] in vocab:
                hit = L
                break
        if hit:
            seq.append(text[i:i + hit])
            i += hit
        else:
            i += 1
    return seq


def longest_ordered_run(words, idx):
    """longest run of consecutive words assignable to one call with strictly increasing pos."""
    best = 0
    best_call = None
    # dp over calls: for each call, track current run length ending here
    cur = defaultdict(lambda: (0, -1))  # call -> (runlen, last_pos)
    for w in words:
        posset = idx.get(w)
        newcur = defaultdict(lambda: (0, -1))
        if posset:
            for (cnum, pos) in posset:
                rl, lastp = cur.get(cnum, (0, -1))
                if rl > 0 and pos > lastp:
                    cand = (rl + 1, pos)
                else:
                    cand = (1, pos)
                if cand[0] > newcur[cnum][0]:
                    newcur[cnum] = cand
                if cand[0] > best:
                    best = cand[0]
                    best_call = cnum
        cur = newcur
    return best, best_call


def book_best(book, idx, vocab):
    best = 0
    where = None
    for leaf in book:
        g = [r for r in book[leaf] if r]
        if len(g) != 49 or not all(len(r) == 49 for r in g):
            continue
        for cells in lines_of(g):
            fwd = "".join(g[r][c] for r, c in cells)
            for text in (fwd, fwd[::-1]):
                seq = tile_words(text, vocab, 2)
                run, cnum = longest_ordered_run(seq, idx)
                if run > best:
                    best = run
                    where = (leaf, cnum)
    return best, where


def run():
    idx = call_index()
    vocab = set(idx)
    book = base_book()
    real_best, where = book_best(book, idx, vocab)

    rows = [r for k in book for r in book[k] if r]
    full = "".join(rows)
    surr_best = []
    for s in range(5):
        st = "".join(markov3(full, random.Random(1140 + s)))
        sbook, p = {}, 0
        for k in book:
            sbook[k] = []
            for r in book[k]:
                if r:
                    sbook[k].append(st[p:p + len(r)])
                    p += len(r)
                else:
                    sbook[k].append(r)
        b, _ = book_best(sbook, idx, vocab)
        surr_best.append(b)
    mean = sum(surr_best) / len(surr_best)
    mx = max(surr_best)

    verdict = ("REAL: um quadrado soletra %d palavras de uma Chamada EM ORDEM (Chamada %s, tabela %s) vs melhor "
               "surrogate %d - há leitura literal de Chamada na grade." % (real_best, where[1], where[0], mx)) \
        if real_best > mx + 1 else \
        ("sem leitura literal: a melhor corrida em ordem no livro é %d palavras (Chamada %s, tabela %s), surrogate "
         "faz %d (média %.1f) - igual ao acaso. Os quadrados NÃO escondem as Chamadas em ordem; são campo de nomes." % (
             real_best, where[1] if where else "-", where[0] if where else "-", mx, mean))

    res = {"real_best_run": real_best, "where": {"call": where[1], "leaf": where[0]} if where else None,
           "surrogate_best_mean": round(mean, 1), "surrogate_best_max": mx, "finding": verdict}
    load.save_result("113_call_in_order", res)
    return res


if __name__ == "__main__":
    r = run()
    print("maior corrida de palavras de Chamada EM ORDEM: real %d | surrogate media %.1f (max %d)" % (
        r["real_best_run"], r["surrogate_best_mean"], r["surrogate_best_max"]))
    print("onde:", r["where"])
    print("\n" + r["finding"])
