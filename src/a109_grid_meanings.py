"""
109 - Rebuild viz/table_grids.json meanings from a MERGED lexicon (Dee's Calls + Leitch Vol II), source-tagged.

Each square's `meanings` becomes the list of dictionary words found on the grid, read straight (rows, cols) and on
both diagonals, forward, each hit carrying its gloss, cells, mode, and source ('dee' = Dee's own interlinear from
Sloane 3191 / chamadas.json; 'leitch' = Aaron Leitch Vol II encyclopedic lexicon). Words present in both keep Dee's
gloss as primary and Leitch's as an alternate. `straight` keeps the Loagaeth system-names (the untranslated roots).
The frontend can then filter by source (Dee / Leitch / both) and show or hide the untranslated words.
"""
import json
import unicodedata

import load


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def _load(path):
    try:
        return {da(k): v for k, v in json.load(open(load.ROOT + path, encoding="utf-8")).items()
                if not k.endswith("_") and v and "(untranslated)" not in str(v)}
    except Exception:
        return {}


def build_lexicon():
    dee = {}
    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    for c in calls:
        for w in c["palavras"]:
            k = da(w["chave"])
            g = (w.get("ingles_sl3191") or "").strip()
            if k and g and k not in dee:
                dee[k] = g
    dic = _load("/viz/dict_enoq_lexicon.json")       # Enochian dictionary (mentoria), English glosses
    leitch = _load("/viz/leitch_extra_lexicon.json")  # Leitch Vol II extras

    keys = set(dee) | set(dic) | set(leitch)
    lex = {}
    for k in keys:
        srcs = []
        entry = {}
        if k in dee:
            srcs.append("dee"); entry["dee"] = dee[k]
        if k in dic:
            srcs.append("dict"); entry["dict"] = dic[k]
        if k in leitch:
            srcs.append("leitch"); entry["leitch"] = leitch[k]
        # preferred gloss: Dee > dict > Leitch
        entry["gloss"] = dee.get(k) or dic.get(k) or leitch.get(k)
        entry["srcs"] = srcs
        entry["src"] = srcs[0] if len(srcs) == 1 else "multi"
        lex[k] = entry
    return lex


def grid_lines(g):
    """Return list of (mode, cells[]) for rows, cols, both diagonals (forward)."""
    R = len(g)
    lines = []
    for r in range(R):
        lines.append(("reta", [(r, c) for c in range(R)]))
    for c in range(R):
        lines.append(("coluna", [(r, c) for r in range(R)]))
    for s in range(R):  # down-right ↘
        lines.append(("diagonal", [(s + k, k) for k in range(R - s)]))
        if s:
            lines.append(("diagonal", [(k, s + k) for k in range(R - s)]))
    for s in range(R):  # down-left ↙
        lines.append(("diagonal", [(s + k, R - 1 - k) for k in range(R - s)]))
        if s:
            lines.append(("diagonal", [(k, R - 1 - s - k) for k in range(R - s)]))
    return lines


def run(min_len=2):
    lex = build_lexicon()
    words = sorted(lex, key=len, reverse=True)
    words = [w for w in words if len(w) >= min_len]

    tg = json.load(open(load.ROOT + "/viz/table_grids.json", encoding="utf-8"))
    order = tg["order"]

    total_hits = 0
    per_leaf_counts = {}
    for leaf in order:
        g = tg["leaves"][leaf]["grid"]
        R = len(g)
        hits = []
        seen = set()
        for mode, cells in grid_lines(g):
            text = "".join(g[r][c] for r, c in cells)
            for w in words:
                start = 0
                while True:
                    i = text.find(w, start)
                    if i < 0:
                        break
                    cseq = cells[i:i + len(w)]
                    key = (w, cseq[0][0], cseq[0][1], mode)
                    if key not in seen:
                        seen.add(key)
                        e = lex[w]
                        hit = {"word": w, "meaning": e["gloss"], "src": e["src"],
                               "srcs": e["srcs"], "cells": [[r, c] for r, c in cseq], "mode": mode}
                        for s in ("dee", "dict", "leitch"):
                            if s in e:
                                hit[s] = e[s]
                        hits.append(hit)
                    start = i + 1
        hits.sort(key=lambda h: (h["cells"][0][0], h["cells"][0][1]))
        tg["leaves"][leaf]["meanings"] = hits
        per_leaf_counts[leaf] = len(hits)
        total_hits += len(hits)

    with open(load.ROOT + "/viz/table_grids.json", "w", encoding="utf-8") as f:
        json.dump(tg, f, ensure_ascii=False)

    dee_n = sum(1 for v in lex.values() if "dee" in v["srcs"])
    dic_n = sum(1 for v in lex.values() if "dict" in v["srcs"])
    lei_n = sum(1 for v in lex.values() if "leitch" in v["srcs"])
    res = {
        "lexicon_total": len(lex), "dee_words": dee_n, "dict_words": dic_n, "leitch_words": lei_n,
        "tables": len(order), "total_hits": total_hits,
        "hits_2a": per_leaf_counts.get("2a"), "hits_sample": dict(list(per_leaf_counts.items())[:6]),
        "finding": ("meanings reconstruídas de lexicon mesclado: %d palavras (Dee %d, Dicionário %d, Leitch %d), %d "
                    "ocorrências em %d tabelas, cada hit com fontes. Frontend filtra por fonte." % (
                        len(lex), dee_n, dic_n, lei_n, total_hits, len(order))),
    }
    load.save_result("109_grid_meanings", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"])
    print("2a hits:", r["hits_2a"], "| amostra:", r["hits_sample"])
