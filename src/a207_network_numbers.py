# -*- coding: utf-8 -*-
"""a207 - three untouched angles.

NETWORK  - distributional communities: build a name x folha matrix, connect names that
           share folhas, cluster. Do DISTRIBUTIONAL families (hang out in same folhas)
           differ from the MORPHOLOGICAL family (#344)? Also folha x folha via shared names.
NUMBERS  - per-folha Enochian gematria sum sequence + distinct-name richness sequence; trend,
           first differences, any match to Dee numbers (49/91/30/2401).
OPERATORS- in the recurring names, which prefixes/suffixes are most productive (data table).

Writes results/207_network_numbers.json + viz/network.json. Seed 1583. stdlib only.
"""
import os
import sys
import json
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

GEM = {"A": 1, "B": 2, "C": 20, "D": 4, "E": 5, "F": 6, "G": 3, "H": 8, "I": 10, "L": 30,
       "M": 40, "N": 50, "O": 70, "P": 80, "Q": 90, "R": 100, "S": 200, "T": 300, "U": 400,
       "X": 60, "Z": 7, "V": 400}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nums = load.table_numbers()
    ftext = {n: load.table_text(n) for n in nums}
    full = "".join(ftext[n] for n in nums)

    # distinct name units: recurring 6-grams, dedup by 4-gram overlap (maximal-ish)
    c6 = Counter(full[i:i + 6] for i in range(len(full) - 5))
    cand = sorted([g for g, v in c6.items() if v >= 15], key=lambda g: -c6[g])
    def g4(s):
        return set(s[i:i + 4] for i in range(len(s) - 3))
    names = []
    for v in cand:
        gv = g4(v)
        if all(not (gv & g4(u)) for u in names):
            names.append(v)
        if len(names) >= 24:
            break
    print("nomes distintos:", names, flush=True)

    # name x folha presence
    pres = {v: set(n for n in nums if v in ftext[n]) for v in names}

    # ---------- NETWORK: name-name shared folhas ----------
    edges = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            sh = len(pres[a] & pres[b])
            un = len(pres[a] | pres[b])
            j = sh / un if un else 0
            edges.append((a, b, round(j, 3), sh))
    edges.sort(key=lambda x: -x[2])
    # greedy communities: threshold jaccard, connected components
    thr = 0.6
    adj = defaultdict(set)
    for a, b, j, sh in edges:
        if j >= thr:
            adj[a].add(b); adj[b].add(a)
    seen = set(); comms = []
    for v in names:
        if v in seen:
            continue
        stack = [v]; comp = []
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x); comp.append(x)
            stack.extend(adj[x] - seen)
        comms.append(comp)
    comms.sort(key=len, reverse=True)
    print(f"[NET] comunidades distribucionais (jaccard>={thr}): {[len(c) for c in comms]}", flush=True)
    for c in comms[:4]:
        print("   ", c, flush=True)

    # ---------- NUMBERS ----------
    gsum = [sum(GEM.get(ch, 0) for ch in ftext[n]) for n in nums]
    richness = [len([v for v in names if v in ftext[n]]) for n in nums]
    diffs = [gsum[i + 1] - gsum[i] for i in range(len(gsum) - 1)]
    dee = {"49": 49, "91": 91, "30": 30, "2401": 2401, "7209": 7209}
    # which per-folha sums or diffs are near a Dee number (within 1%)
    print(f"[NUM] soma gematria por folha: min {min(gsum)} max {max(gsum)} média {sum(gsum)//len(gsum)}", flush=True)
    print(f"[NUM] riqueza de nomes por folha (prim/últ): {richness[:6]} ... {richness[-6:]}", flush=True)

    # ---------- OPERATORS ----------
    roots = ["NOCHA", "CHASTO", "ANZACH", "GETH", "ACLAX", "GEDOR"]
    pre = Counter(); suf = Counter()
    allnames = [g for g, v in c6.items() if v >= 15]
    for v in allnames:
        for r in roots:
            k = v.find(r)
            if k >= 0:
                if k > 0:
                    pre[v[:k]] += c6[v]
                tail = v[k + len(r):]
                if tail:
                    suf[tail] += c6[v]
    print(f"[OP] prefixos top: {pre.most_common(8)}", flush=True)
    print(f"[OP] sufixos top: {suf.most_common(8)}", flush=True)

    result = {
        "seed": 1583, "names": names,
        "network": {"threshold": thr, "communities": comms,
                    "top_edges": [[a, b, j, sh] for a, b, j, sh in edges[:12]]},
        "numbers": {"gematria_sum": gsum, "richness": richness, "diffs_sample": diffs[:10],
                    "min": min(gsum), "max": max(gsum)},
        "operators": {"prefixes": pre.most_common(12), "suffixes": suf.most_common(12)},
    }
    viz = {"folhas": nums, "gematria_sum": gsum, "richness": richness,
           "communities": comms, "top_edges": result["network"]["top_edges"],
           "operators": result["operators"]}
    with open(os.path.join(os.path.dirname(HERE), "viz", "network.json"), "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "207_network_numbers.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
