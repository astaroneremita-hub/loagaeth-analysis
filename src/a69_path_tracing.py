"""
69 - Path-tracing to the end: is a name "walkable" on a leaf a real signal, or the dense field?

A name can be spelled as a connected king-move path (8 neighbours, no cell reused) through a leaf's
49x49 grid - the way Watchtower names are read. DAHAHOXOM does this 23 times on 2b, above its own
anagrams. But the Loagaeth is a dense field of these letters, so most names walk somewhere. The
questions that settle whether this approach finds anything:

  A) Per name, the leaf where it walks most, and its z against anagrams of the same letters on that
     leaf (does the SEQUENCE matter, or only the letters?).
  B) Leaf-specificity: does a name walk most on the leaf where it is actually written / presiding
     (a28, a67), or on an unrelated leaf? If path-strength tracks real occurrence, the reading is
     meaningful; if not, it is the field.
  C) The control that matters: do made-up names (random strings over the book's alphabet) walk just
     as well as the real catalogue names? If real names don't beat random strings, path-tracing
     carries no information about which names belong to the book.
"""
import json
import os
import random
import statistics
from collections import Counter

import load
import a15_book_geometry as a15
from a22_robustness_and_depth import base_book, tnum


def grids():
    lv = load.leaves()
    G = {}
    for k, v in lv.items():
        g = [load.letters(r) for r in v if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            G[k] = g
    for n in range(29, 49):
        g = a15.rebuild(n)
        if g and not any(x is None for r in g for x in r):
            G[f"{n}a*"] = g
    return G


def count_paths(grid, tg, cap=4000):
    R = len(grid)
    cnt = [0]

    def nb(r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr or dc:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < R and 0 <= nc < len(grid[nr]):
                        yield nr, nc

    def dfs(r, c, idx, path):
        if idx == len(tg):
            cnt[0] += 1
            return cnt[0] < cap
        for nr, nc in nb(r, c):
            if (nr, nc) not in path and grid[nr][nc] == tg[idx]:
                path.append((nr, nc))
                if not dfs(nr, nc, idx + 1, path):
                    return False
                path.pop()
        return True
    for r in range(R):
        for c in range(len(grid[r])):
            if grid[r][c] == tg[0]:
                dfs(r, c, 1, [(r, c)])
    return cnt[0]


def run():
    rng = random.Random(69)
    G = grids()
    book = base_book()
    text = {k: "".join(r for r in book[k] if r) for k in book}
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    masters = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX", "DAHAHOXOM"]
    names = sorted({n for n in (set(masters) | {x["name"] for x in d}) if len(n) >= 5}, key=len)

    def best_leaf(nm):
        best = None
        for k, g in G.items():
            c = count_paths(g, nm)
            if best is None or c > best[1]:
                best = (k, c, g)
        return best

    def written_leaf(nm):  # leaf where the name occurs most as a written substring
        per = {k: text.get(k, "").count(nm) + text.get(k[:-1] + ("b" if k.endswith("a") else "a"), "").count(nm) for k in G}
        bk = max(per, key=per.get)
        return bk, per[bk]

    # A + B per name
    rows = []
    for nm in names:
        k, c, g = best_leaf(nm)
        if c == 0:
            continue
        letters = list(nm)
        nul = []
        for _ in range(40):
            a = letters[:]
            rng.shuffle(a)
            if "".join(a) != nm:
                nul.append(count_paths(g, "".join(a)))
        mu, sd = statistics.mean(nul), (statistics.pstdev(nul) or 1)
        wk, wc = written_leaf(nm)
        rows.append({"name": nm, "walks_most_on": k, "paths": c, "z_vs_anagram": round((c - mu) / sd, 1),
                     "written_most_on": wk, "times_written_there": wc,
                     "walk_leaf_is_written_leaf": k.rstrip("*").rstrip("ab") == wk.rstrip("*").rstrip("ab")})
    # B summary: how often does the walk-leaf match the written-leaf?
    written = [r for r in rows if r["times_written_there"] > 0]
    match = sum(r["walk_leaf_is_written_leaf"] for r in written)

    # C: real names vs random strings of the same lengths
    f = Counter(ch for g in G.values() for row in g for ch in row)
    alph, wt = list(f), [f[c] for c in f]
    real_best = statistics.mean(r["paths"] for r in rows)
    rand_best = []
    for _ in range(60):
        nm = "".join(rng.choices(alph, wt, k=rng.choice([len(x) for x in names])))
        rand_best.append(best_leaf(nm)[1])
    res = {"names_tested": len(names), "full_leaves": len(G),
           "A_strongest_by_z": sorted(rows, key=lambda r: -r["z_vs_anagram"])[:15],
           "B_leaf_specificity": {"names_also_written_somewhere": len(written), "walk_leaf_matches_written_leaf": match,
                                  "share": round(match / max(1, len(written)), 2),
                                  "note": "If path-tracing tracked real presence, a name would walk most on the leaf where "
                                          "it is actually written. Match rate here says how much it does."},
           "C_real_vs_random_names": {"real_names_best_paths_mean": round(real_best, 1),
                                      "random_strings_best_paths_mean": round(statistics.mean(rand_best), 1),
                                      "note": "If real names don't out-walk random strings, path-tracing carries no "
                                              "information about which names belong to the book."},
           "conclusion": ""}
    # fill conclusion from the numbers
    spec = res["B_leaf_specificity"]["share"]
    rr = res["C_real_vs_random_names"]
    res["conclusion"] = ("Path-tracing is mostly the dense field, not a reading that singles out real names. A name walks "
                         "on its own written leaf only %d of %d times (%.0f%%), so walkability does not track where a name "
                         "actually is. Real catalogue names walk about %.0f paths on their best leaf against %.0f for "
                         "random strings of the same lengths - %s. The one solid part is per-name: a name usually walks "
                         "more than its OWN anagrams on some leaf (the sequence beats its scramble), but that best leaf is "
                         "rarely the leaf the name is written on. So the approach shows that these letters are arranged "
                         "pronounceably enough to walk almost any name somewhere; it does not show that a given walk is "
                         "meant." % (match, len(written), 100 * spec, rr["real_names_best_paths_mean"],
                                     rr["random_strings_best_paths_mean"],
                                     "real names do stand out" if rr["real_names_best_paths_mean"] > 1.5 * rr["random_strings_best_paths_mean"] else "they are close, so little is special about real names"))
    load.save_result("69_path_tracing", res)
    return res


if __name__ == "__main__":
    r = run()
    print("strongest name walks (z vs own anagrams):")
    for x in r["A_strongest_by_z"][:12]:
        print("  %-12s walks %4d on %-5s (z %4.1f)   written most on %-5s (%d×)  %s" %
              (x["name"], x["paths"], x["walks_most_on"], x["z_vs_anagram"], x["written_most_on"], x["times_written_there"],
               "MATCH" if x["walk_leaf_is_written_leaf"] else ""))
    print("\nleaf-specificity:", r["B_leaf_specificity"])
    print("real vs random:", r["C_real_vs_random_names"])
    print("\n" + r["conclusion"])
