# -*- coding: utf-8 -*-
"""a235 - root x affix grammar: free combination (#335) or selectional CLASSES?

If the Loagaeth has grammatical classes (like gender/declension), some affixes would attach
only to some roots. Build the root x prefix and root x suffix co-occurrence from the recurring
names; is it full (free) or structured (affixes cluster by root)? Do the two houses (NOCHA vs
GETH/ACLAX) take different affixes? Null: shuffle which affix goes with which root.
stdlib only. seed 1583.
"""
import os
import sys
import json
import math
import random
import re
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

rng = random.Random(1583)
ROOTS = ["NOCHAST","CHASTOR","NOCHA","NOCH","ANZACH","NZACH","ALGETH","GETH","ACLAX","ACLAXT",
         "CHARD","DAX","GRAPH","ACHEPH","ANTANT","NTAG","NADAB","VOXAR","GEDOR"]
HOUSE = {"NOCHA":"NOCHA","NOCH":"NOCHA","NOCHAST":"NOCHA","CHASTOR":"NOCHA","ANZACH":"NOCHA","NZACH":"NOCHA",
         "GETH":"GETH","ALGETH":"GETH","ACLAX":"GETH","ACLAXT":"GETH","DAX":"GETH","CHARD":"GETH"}


def decomp(w):
    for r in sorted(ROOTS, key=len, reverse=True):
        k = w.find(r)
        if k >= 0:
            return w[:k], r, w[k+len(r):]
    return None


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    # recurring names (>=12)
    full = load.dense_stream()
    c6 = Counter(full[i:i+6] for i in range(len(full)-5))
    names = sorted({g for g, v in c6.items() if v >= 10}, key=lambda g: -c6[g])
    # also longer recurring forms
    for k in (7, 8, 9, 10):
        ck = Counter(full[i:i+k] for i in range(len(full)-k+1))
        names += [g for g, v in ck.items() if v >= 8]
    names = list(dict.fromkeys(names))

    pre_by_root = defaultdict(Counter); suf_by_root = defaultdict(Counter)
    pairs = []
    for w in names:
        d = decomp(w)
        if not d: continue
        pre, r, suf = d
        if pre: pre_by_root[r][pre] += 1
        if suf: suf_by_root[r][suf] += 1
        pairs.append((r, pre, suf))

    # which prefixes appear, and are they shared across roots or root-specific?
    allpre = Counter(); allsuf = Counter()
    for r in pre_by_root:
        for p, n in pre_by_root[r].items(): allpre[p] += n
    for r in suf_by_root:
        for s, n in suf_by_root[r].items(): allsuf[s] += n
    print("prefixos globais:", allpre.most_common(10), flush=True)
    print("sufixos globais:", allsuf.most_common(10), flush=True)

    # house analysis: do NOCHA-house and GETH-house take different affixes?
    house_pre = defaultdict(Counter)
    for r in pre_by_root:
        h = HOUSE.get(r, "?")
        for p, n in pre_by_root[r].items(): house_pre[h][p] += n
    print("\nprefixos por CASA:", flush=True)
    for h in ("NOCHA", "GETH"):
        print(f"   {h}: {house_pre[h].most_common(8)}", flush=True)

    # structure: for the top prefixes, how many distinct roots take each? (shared vs specific)
    pre_roots = defaultdict(set)
    for r in pre_by_root:
        for p in pre_by_root[r]: pre_roots[p].add(r)
    shared = [(p, len(rs)) for p, rs in pre_roots.items() if allpre[p] >= 3]
    shared.sort(key=lambda x: -x[1])
    print("\nprefixo -> em quantas raízes distintas (compartilhado vs específico):", shared[:10], flush=True)

    out = {"prefixes": allpre.most_common(), "suffixes": allsuf.most_common(),
           "house_prefixes": {h: house_pre[h].most_common() for h in ("NOCHA", "GETH")},
           "prefix_root_spread": shared}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "235_root_affix_grammar.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
