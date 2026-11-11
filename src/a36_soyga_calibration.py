"""
36 - A ruler for the scribe: the Soyga tables copied at the back of Sloane 3189.

Eight tables of the Book of Soyga are copied in the same manuscript as the Loagaeth (fols 58-65) and
are transcribed at the end of Peterson's page. Jim Reeds (1998) found their exact generator: a
36 x 36 grid over the 23-letter alphabet a b c d e f g h i k l m n o p q r s t u x y z; the left
column is a code word and its reverse, repeated; top row X = W + f(W); elsewhere X = N + f(W)
(mod 23; N = cell above, W = cell to the left).

So for these pages we KNOW what every cell should be. Regenerating the tables and comparing with
the transcription gives the error rate, and the confusion matrix, of this hand as read by this
transcriber - the same chain that gives us the Loagaeth. The question for our study: is A <-> U a
confusion of this hand? If not, the U register of tables 41-48 is not a reading artefact.

Errors propagate in a generated table only in the original computation, not in a copy, so each cell
is compared with the value computed from the TRUE neighbours.
"""
import html
import json
import os
import re
from collections import Counter

import load

ALPHA = "abcdefghiklmnopqrstuxyz"
F = dict(zip(ALPHA, [2, 2, 3, 5, 14, 2, 6, 5, 14, 15, 20, 22, 14, 8, 13, 20, 11, 8, 8, 15, 15, 15, 2]))
IDX = {c: i + 1 for i, c in enumerate(ALPHA)}
WORDS = ["NISRAM", "MARSIN", "ROELER", "RELEOR", "IOMIOT", "TOIMOI", "ISIAPO", "OPAISI"]
RAW = os.path.join(load.DATA, "raw", "sl3189.htm")


def letter(n):
    return ALPHA[(n - 1) % 23]


def generate(word):
    w = word.lower()
    col = (w + w[::-1]) * 3
    G = [[None] * 36 for _ in range(36)]
    for r in range(36):
        G[r][0] = col[r]
    for r in range(36):
        for c in range(1, 36):
            W = G[r][c - 1]
            base = IDX[W] if r == 0 else IDX[G[r - 1][c]]
            G[r][c] = letter(base + F[W])
    return G


def parse():
    h = open(RAW, encoding="latin-1").read()
    i = h.find("TABLES OF SOYGA")
    if i < 0:
        return []
    t = html.unescape(re.sub(r"<[^>]+>", "\n", h[i:]))
    tables, cur = [], []
    for line in t.split("\n"):
        m = re.match(r"^\s*(\d+)\.\s+(.*)$", line)
        if not m:
            continue
        n = int(m.group(1))
        cells = [x.lower() for x in m.group(2).split() if len(x) == 1 and x.isalpha()]
        if n == 1 and cur:
            tables.append(cur)
            cur = []
        cur.append(cells)
    if cur:
        tables.append(cur)
    out = []
    for T in tables:  # facing tables are numbered 1-72 in the transcription: split into 36 + 36
        for i in range(0, len(T), 36):
            if len(T[i:i + 36]) >= 20:
                out.append(T[i:i + 36])
    return out


def norm(c):
    return {"v": "u", "j": "i", "w": "u"}.get(c, c)


def run():
    if not os.path.exists(RAW):
        import a18_markup_decoding
        a18_markup_decoding.fetch()
    tabs = parse()
    gens = {w: generate(w) for w in WORDS}
    conf = Counter()
    per = []
    total = wrong = 0
    for k, T in enumerate(tabs):
        best = None
        for w, G in gens.items():
            ok = n = 0
            for r in range(min(36, len(T))):
                for c in range(min(36, len(T[r]))):
                    n += 1
                    ok += norm(T[r][c]) == G[r][c]
            if n and (best is None or ok / n > best[1]):
                best = (w, ok / n, n)
        w, share, n = best
        G = gens[w]
        full = [r for r in range(min(36, len(T))) if len(T[r]) == 36]
        # a table that departs widely carries an error of the ORIGINAL computation that propagates
        # (Reeds: T13 row 18) or a misaligned row; it says nothing about letter confusions
        for r in (full if share >= 0.9 else []):
            for c in range(36):
                a, b = G[r][c], norm(T[r][c])
                total += 1
                if a != b:
                    wrong += 1
                    conf[(a, b)] += 1
        per.append({"table": k + 1, "code_word": w, "agreement": round(share, 4), "cells": n,
                    "rows_of_36": len(full), "rows": len(T)})
    true_counts = Counter(G[r][c] for p, T in zip(per, tabs) if p["agreement"] >= 0.9 for G in [gens[p["code_word"]]]
                          for r in range(min(36, len(T))) if len(T[r]) == 36 for c in range(36))

    def rate(a, b):
        return {"count": conf[(a, b)], "of": true_counts[a], "rate": round(conf[(a, b)] / max(1, true_counts[a]), 4)}
    watch = {f"{a}->{b}": rate(a, b) for a, b in [("a", "u"), ("u", "a"), ("u", "n"), ("n", "u"), ("z", "x"), ("x", "z"),
                                                 ("y", "i"), ("i", "y"), ("e", "l"), ("c", "r"), ("c", "t"), ("a", "o"), ("o", "a"), ("a", "e")]}
    res = {"tables_parsed": len(tabs), "per_table": per, "cells_compared": total, "errors": wrong,
           "error_rate": round(wrong / max(1, total), 4),
           "top_confusions_true_to_read": [{"true": a, "read": b, "count": n} for (a, b), n in conf.most_common(15)],
           "watched_pairs": watch,
           "reeds_reported": "about 1.5% error; z read as x 34 of 477; y -> i 9 times (Reeds 1998, on the manuscript itself)"}
    load.save_result("36_soyga_calibration", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
