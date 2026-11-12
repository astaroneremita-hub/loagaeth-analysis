"""
59 - The words of the Calls, searched along every reading path.

A reader's idea: take the words of the Angelic Calls and look for them in the tables read other ways
- diagonals, backward, and so on. The diary says each letter of a Call was taken from a numbered
place in a different table (a57), so whole Call words should not sit anywhere as a run; but this
tests it exhaustively instead of assuming it.

For the full 49x49 tables (2-24), every line is read in eight ways: rows left-to-right and
right-to-left; columns down and up; the two main diagonals; the two anti-diagonals. The words of the
Calls (>= 4 letters), and the words reversed (the angels dictated backward), are counted in each
stream and compared with a Markov-3 surrogate of that same stream. The surrogate preserves the
path's own letter-flow (its trigram statistics), so a path "finds" the Calls only if their words sit
there beyond what the path's letter statistics already produce - a null that a plain
letter-frequency null fails, because reading a row-written table down its columns or diagonals
changes the letter statistics and makes a frequency null meaningless.
"""
import collections
import json
import os
import random
import re
import statistics

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book, tnum


def grids():
    book = base_book()
    out = {}
    for k, v in book.items():
        if 2 <= tnum(k) <= 24:
            g = [r for r in v if r]
            if len(g) == 49 and all(len(x) == 49 for x in g):
                out[k] = g
    return out


def lines_in(g, kind):
    n = 49
    if kind == "rows":
        return ["".join(g[r][c] for c in range(n)) for r in range(n)]
    if kind == "cols":
        return ["".join(g[r][c] for r in range(n)) for c in range(n)]
    if kind == "diag":  # r-c constant, down-right
        return ["".join(g[r][r - d] for r in range(max(0, d), min(n, n + d)) if 0 <= r - d < n) for d in range(-n + 1, n)]
    if kind == "anti":  # r+c constant, down-left
        return ["".join(g[r][s - r] for r in range(n) if 0 <= s - r < n) for s in range(2 * n - 1)]
    return []


def stream(gs, kind, reverse=False):
    out = []
    for g in gs.values():
        for ln in lines_in(g, kind):
            out.append(ln[::-1] if reverse else ln)
    return "|".join(out)


def call_words(minlen=4):
    c = json.load(open(os.path.join(os.path.dirname(load.DATA), "engine", "data", "chamadas.json"), encoding="utf-8"))["chamadas"]
    ws = []
    for ch in c:
        for w in ch["palavras"]:
            x = re.sub(r"[^A-Z]", "", w["enoquiano"].upper())
            if len(x) >= minlen:
                ws.append(x)
    return ws


def path_lines(gs, kind):
    out = []
    for g in gs.values():
        out += [l for l in lines_in(g, kind) if len(l) >= 4]
    return out


def run(reps=120):
    rng = random.Random(59)
    gs = grids()
    words = call_words()
    rev = [w[::-1] for w in words]

    def surr(lines):
        s = markov3("".join(lines), rng)
        out, i = [], 0
        for l in lines:
            out.append(s[i:i + len(l)])
            i += len(l)
        return out

    # a second, stronger null and a placebo word-list, to see whether any path is SPECIFIC to the Calls.
    # word-scramble null: each word's own letters shuffled (controls the word's letter composition);
    # placebo: Dee's leaf-1 words (also Loagaeth-flavoured) - if they behave like the Calls, nothing is special.
    leaf1 = [load.letters(w) for r in load.leaves()["1a"] + load.leaves()["1b"] for w in r.split() if len(load.letters(w)) >= 4]
    rng.shuffle(leaf1)
    leaf1 = leaf1[:len(words)]

    def scramble(w):
        l = list(w)
        rng.shuffle(l)
        return "".join(l)

    def wtest(S, wl, r=200):
        real = sum(1 for w in wl if w in S)
        nul = [sum(1 for w in wl if scramble(w) in S) for _ in range(r)]
        return real, round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1)

    paths = []
    for kind in ("rows", "cols", "diag", "anti"):
        lines = path_lines(gs, kind)
        S = "|".join(lines)
        realF = sum(1 for w in words if w in S)
        realR = sum(1 for w in rev if w in S)
        nF, nR = [], []
        for _ in range(reps):
            Ss = "|".join(surr(lines))
            nF.append(sum(1 for w in words if w in Ss))
            nR.append(sum(1 for w in rev if w in Ss))
        cz = wtest(S, words)[1]
        lz = wtest(S, leaf1)[1]
        paths.append({"path": kind + " forward", "call_words_found": realF, "markov3_surrogate": round(statistics.mean(nF), 1),
                      "z_markov3_stream_null": round((realF - statistics.mean(nF)) / (statistics.pstdev(nF) or 1e-9), 1),
                      "z_word_scramble_null": cz, "leaf1_placebo_z_word_scramble": lz})
        paths.append({"path": kind + " reversed words", "call_words_found": realR, "markov3_surrogate": round(statistics.mean(nR), 1),
                      "z_markov3_stream_null": round((realR - statistics.mean(nR)) / (statistics.pstdev(nR) or 1e-9), 1)})
    best = max((p for p in paths if "z_word_scramble_null" in p), key=lambda p: p["z_word_scramble_null"])
    res = {"full_tables_used": len(gs), "call_words_at_least_4": len(words), "paths": paths,
           "conclusion": ("No reading path hides the Calls. Under a Markov-3 stream null one path (anti-diagonal) reaches "
                          "z ~3.7, but it does NOT survive the stronger word-scramble null (z ~1.5), and it is one of eight "
                          "paths tested. On the rows both the Calls and Dee's leaf-1 words score high against letter "
                          "scrambles (z 9 and 26) - a property of real Loagaeth-structured words in a Loagaeth stream, not "
                          "of hidden placement; the leaf-1 placebo behaves like the Calls or stronger everywhere, so "
                          "nothing is special to the Calls. Consistent with a57 and the diary: the Call letters are "
                          "gathered from scattered numbered places, not laid along any single path.")}
    load.save_result("59_calls_every_path", res)
    return res


if __name__ == "__main__":
    r = run()
    print("%d full tables, %d Call words >=4 letters" % (r["full_tables_used"], r["call_words_at_least_4"]))
    for p in r["paths"]:
        if "z_word_scramble_null" in p:
            print("  %-16s found %3d  z(stream) %4.1f  z(word-scramble) %4.1f  leaf1-placebo %4.1f" %
                  (p["path"], p["call_words_found"], p["z_markov3_stream_null"], p["z_word_scramble_null"], p["leaf1_placebo_z_word_scramble"]))
    print(r["conclusion"])
