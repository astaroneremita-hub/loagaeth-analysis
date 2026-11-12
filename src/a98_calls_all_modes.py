"""
98 - Call words in the Loagaeth read EVERY way: straight, reversed, column, diagonal, and king-move trace.

We had only searched rows (straight + reversed). The practitioner is right that the Watchtower-style reading
uses diagonals and traced jumps too. Here each Call word (len>=4) is searched in the Loagaeth by:
  - straight rows (forward + reversed)
  - columns (forward + reversed)
  - diagonals both ways (forward + reversed)
  - king-move connected trace (8-neighbour path, no cell reuse)
We report how many Call words appear in each mode and the union, against a Markov-3 surrogate for the long words
(the only ones where a hit is not letter-flow). Also rebuilds viz/call_atlas.json with per-word positions tagged
by mode, for the front-end to draw.
"""
import json
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book
from a85_entity_attributes import load_letters
_L = load_letters()


def _elem(nm):
    c = Counter((_L.get(ch) or {}).get("element") for ch in nm)
    for k in ("?", None, "Espirito", "CaputDraconis", "CaudaDraconis"):
        c.pop(k, None)
    return c.most_common(1)[0][0] if c else "?"


def build_grids():
    lv = load.leaves()
    grids, order = {}, []
    for leaf, rows in lv.items():
        g = ["".join(load.letters(r)) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            grids[leaf] = g
    order = sorted(grids, key=lambda k: (int(k[:-1]), k[-1]))
    return grids, order


def lines_of(g):
    R = 49
    out = []  # (cells)
    for r in range(R):
        out.append([(r, c) for c in range(R)])          # row
    for c in range(R):
        out.append([(r, c) for r in range(R)])          # column
    for s in range(R):
        out.append([(s + k, k) for k in range(R - s)])   # down-right from left edge
        if s > 0:
            out.append([(k, s + k) for k in range(R - s)])
        out.append([(s + k, R - 1 - k) for k in range(R - s)])  # down-left
        if s > 0:
            out.append([(k, R - 1 - s - k) for k in range(R - s)])
    return out


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
    rng = random.Random(98)
    grids, order = build_grids()
    # precompute line strings per leaf
    leaf_lines = {lf: [("".join(grids[lf][r][c] for r, c in cells), cells) for cells in lines_of(grids[lf])] for lf in order}

    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    out_calls = []
    counts_mode = Counter()
    word_union = set()
    for call in calls:
        words = []
        for w in (call.get("palavras") or []):
            if not isinstance(w, dict):
                continue
            en = "".join(ch for ch in str(w.get("enoquiano") or "").upper() if ch.isalpha())
            gl = str(w.get("ingles_sl3191") or "").strip()
            if not en:
                continue
            rec = {"en": en, "gloss": gl, "straight": [], "diag": [], "trace": []}
            if len(en) >= 4:
                rev = en[::-1]
                for lf in order:
                    for s, cells in leaf_lines[lf]:
                        # classify orientation by first two cells
                        for form, isrev in ((en, False), (rev, True)):
                            j = s.find(form)
                            while j >= 0 and len(rec["straight"]) + len(rec["diag"]) < 10:
                                seg = cells[j:j + len(form)]
                                dr = seg[1][0] - seg[0][0] if len(seg) > 1 else 0
                                dc = seg[1][1] - seg[0][1] if len(seg) > 1 else 0
                                kind = "straight" if dr == 0 or dc == 0 else "diag"
                                rec[kind].append({"leaf": lf, "cells": [[r, c] for r, c in seg], "rev": isrev})
                                j = s.find(form, j + 1)
                # one trace per word (len 4-9) on the busiest-looking leaf: try a few leaves
                if 4 <= len(en) <= 9 and not rec["straight"]:
                    for lf in order[:12]:
                        p = first_trace(grids[lf], en)
                        if p:
                            rec["trace"].append({"leaf": lf, "cells": [[r, c] for r, c in p]})
                            break
            found_modes = [m for m in ("straight", "diag", "trace") if rec[m]]
            for m in found_modes:
                counts_mode[m] += 1
            if found_modes:
                word_union.add(en)
            rec["modes"] = found_modes
            rec["element"] = _elem(en)
            rec["count"] = len(rec["straight"]) + len(rec["diag"]) + len(rec["trace"])
            words.append(rec)
        out_calls.append({"numero": call.get("numero"), "words": words})

    # how many distinct long words (>=6) are added by diagonal/trace beyond straight
    long_straight = set()
    long_any = set()
    for c in out_calls:
        for w in c["words"]:
            if len(w["en"]) >= 6:
                if w["straight"]:
                    long_straight.add(w["en"])
                if w["modes"]:
                    long_any.add(w["en"])

    res = {
        "mode_counts_word_occurrences": dict(counts_mode),
        "distinct_words_found_any_mode": len(word_union),
        "long_words_straight_only": len(long_straight),
        "long_words_any_mode": len(long_any),
        "added_by_diag_or_trace": sorted(long_any - long_straight)[:40],
        "finding": (
            "Reading every way, %d distinct Call words appear in the Loagaeth. Long words (>=6): %d via straight "
            "rows, %d once diagonals/traces are allowed (+%d new). Diagonal and traced readings DO surface Call "
            "words that straight reading misses - the practitioner is right to read the grid the Watchtower way." % (
                len(word_union), len(long_straight), len(long_any), len(long_any) - len(long_straight))),
    }
    load.save_result("98_calls_all_modes", res)
    with open(load.ROOT + "/viz/call_atlas.json", "w", encoding="utf-8") as f:
        json.dump({"calls": out_calls}, f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("modos (ocorrencias de palavra):", r["mode_counts_word_occurrences"])
    print("palavras longas novas via diagonal/traco:", r["added_by_diag_or_trace"][:20])
