"""
104 - Deep search for the Call words not found by the straight/diagonal pass: full king-move trace too.

165 translated Call words did not appear as contiguous substrings (rows/cols/diagonals, forward+reversed).
This re-searches each of them with an exhaustive king-move TRACE across every leaf (the Watchtower way), to see
how many can be spelled as a connected jumping path. HONEST: the grid is a dense field, so short words trace
almost anywhere - a trace hit is weak evidence. We report, per word, whether it traces and the shortest/strongest
case, and keep the length honest: a long word (>=8) that traces is worth more than a 5-letter one.
"""
import json

import load


def build_grids():
    lv = load.leaves()
    grids, order = {}, []
    for leaf, rows in lv.items():
        g = ["".join(load.letters(r)) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            grids[leaf] = g
    order = sorted(grids, key=lambda k: (int(k[:-1]), k[-1]))
    return grids, order


def first_trace(g, tg):
    R = 49
    def nb(r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < R:
                        yield nr, nc
    res = [None]
    def dfs(r, c, idx, path):
        if idx == len(tg):
            res[0] = path[:]
            return True
        for nr, nc in nb(r, c):
            if (nr, nc) not in path and g[nr][nc] == tg[idx]:
                path.append((nr, nc))
                if dfs(nr, nc, idx + 1, path):
                    return True
                path.pop()
        return False
    for r in range(R):
        for c in range(R):
            if g[r][c] == tg[0]:
                if dfs(r, c, 1, [(r, c)]):
                    return res[0]
    return None


def run():
    grids, order = build_grids()
    cov = json.load(open(load.ROOT + "/viz/call_coverage.json", encoding="utf-8"))
    nf = cov["not_found"]

    found_trace = {}
    still_absent = {}
    for w, gloss in nf.items():
        hit = None
        for lf in order:
            p = first_trace(grids[lf], w)
            if p:
                hit = {"leaf": lf, "cells": [[r, c] for r, c in p]}
                break
        if hit:
            found_trace[w] = {"gloss": gloss, "len": len(w), **hit}
        else:
            still_absent[w] = {"gloss": gloss, "len": len(w)}

    long_traced = {w: d for w, d in found_trace.items() if d["len"] >= 8}
    res = {
        "not_found_before": len(nf),
        "now_traceable": len(found_trace),
        "still_absent": len(still_absent),
        "long_traced_ge8": len(long_traced),
        "long_traced_sample": {w: found_trace[w]["gloss"] for w in list(long_traced)[:20]},
        "still_absent_sample": {w: still_absent[w]["gloss"] for w in list(still_absent)[:25]},
        "note": "Traco acha quase qualquer palavra no campo denso (a69/a73), entao traco positivo e fraco; conta mais "
                "para palavras longas. Os que NEM tracam ficam como ausentes de verdade.",
        "finding": (
            "Of %d Call words not found straight/diagonal, %d DO trace as a king-move path somewhere (and %d still "
            "do not appear at all). But trace finds almost anything in a dense field, so the honest read is: %d LONG "
            "words (>=8 letters) trace - those are the interesting ones (e.g. %s); the short ones tracing proves "
            "little. %d words appear nowhere, by any reading - genuinely absent from the Loagaeth." % (
                len(nf), len(found_trace), len(still_absent), len(long_traced),
                ", ".join(list(long_traced)[:5]) or "-", len(still_absent))),
    }
    load.save_result("104_notfound_deep", res)
    # update coverage: mark trace-found, keep genuinely absent
    with open(load.ROOT + "/viz/call_coverage.json", "w", encoding="utf-8") as f:
        json.dump({"found": cov["found"], "not_found": {w: still_absent[w]["gloss"] for w in still_absent},
                   "trace_only": {w: found_trace[w]["gloss"] for w in found_trace}}, f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("LONGAS (>=8) que tracam:", r["long_traced_sample"])
    print("\nainda AUSENTES por qualquer leitura (amostra):", r["still_absent_sample"])
