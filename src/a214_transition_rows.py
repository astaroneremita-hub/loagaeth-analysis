# -*- coding: utf-8 -*-
"""a214 - analysis D: do the grid-names assemble in the transitional cluster-words of leaf 1?

Leaf 1 (word-spaced) carries 213 hyphenated syllable-clusters (oro-dax-va, a-mas-ca-ba-lo-
no-cha, chom-gas-naph-geth-nag ...) - long 'cluster-words found nowhere else' (a55). The
record places leaf-1 side 2 between word-language and table-language. Test: do the catalogue
grid-roots (NOCHA/CHAST/GETH/ACLAX/DAX...) appear in these clusters MORE than in ordinary
leaf-1 words? If so, the clusters are where the two languages meet - the grid-names first
assembling out of syllables.

stdlib only.
"""
import os
import sys
import json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load

ROOTS = ["NOCHA", "NOCH", "CHAST", "CHASTOR", "ANZACH", "GETH", "ACLAX", "NACHO",
         "CHARDAX", "CHARD", "OXAR", "DAX", "ALGETH", "ALGRA", "DNOCH", "ADNOCH",
         "ANTANT", "GRADAX", "NADAB", "VOXAR"]


def tokens():
    lv = load.leaves()
    clusters, words = [], []
    for key in ("1a", "1b"):
        for r in lv[key]:
            for tok in r.split():
                L = load.letters(tok)
                if len(L) < 4:
                    continue
                if tok.count("-") >= 2:
                    clusters.append(L)
                else:
                    words.append(L)
    return clusters, words


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    clusters, words = tokens()

    def hits(toks):
        found = []
        for t in toks:
            r = [root for root in ROOTS if root in t]
            if r:
                found.append((t, r))
        return found

    ch = hits(clusters); wh = hits(words)
    rate_c = len(ch) / len(clusters)
    rate_w = len(wh) / len(words)
    # per-root counts in clusters
    root_c = Counter(root for _, rs in ch for root in rs)
    root_w = Counter(root for _, rs in wh for root in rs)

    print(f"[D] aglomerados: {len(clusters)}, com raiz de grade: {len(ch)} ({rate_c:.0%})", flush=True)
    print(f"[D] palavras comuns: {len(words)}, com raiz: {len(wh)} ({rate_w:.0%})", flush=True)
    print(f"[D] razão aglomerado/palavra: {rate_c/rate_w if rate_w else float('inf'):.2f}x", flush=True)
    print(f"[D] raízes nos aglomerados: {root_c.most_common(10)}", flush=True)
    print(f"[D] exemplos (aglomerado -> raízes):", flush=True)
    for t, rs in ch[:14]:
        print(f"     {t}  <- {rs}", flush=True)

    result = {"n_clusters": len(clusters), "n_words": len(words),
              "clusters_with_root": len(ch), "words_with_root": len(wh),
              "rate_clusters": round(rate_c, 3), "rate_words": round(rate_w, 3),
              "ratio": round(rate_c / rate_w, 2) if rate_w else None,
              "root_counts_clusters": root_c.most_common(),
              "examples": ch[:30]}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "214_transition_rows.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
