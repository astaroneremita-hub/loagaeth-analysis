# -*- coding: utf-8 -*-
"""a210 - unsupervised segmentation by branching entropy (Harris 1955).

At each position the successor entropy of the k-gram ending there is computed over the
whole book. A boundary is placed where branching entropy rises (a morpheme/name edge).
Segment the stream, report the segment-length distribution and the most common segments -
does an unsupervised cut rediscover the names (NOCHA etc)?

Null: segment a shuffled stream the same way; compare how 'name-like' the segments are.
stdlib only. seed 1583.
"""
import os
import sys
import json
import math
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

K = 3
FAM = ("NOCHA", "CHASTOR", "ANZACH", "ALGETH", "GETH", "NOCH", "CHAST", "ADNOCH")


def branching_table(S, k):
    succ = defaultdict(Counter)
    for i in range(len(S) - k):
        succ[S[i:i + k]][S[i + k]] += 1
    be = {}
    for g, c in succ.items():
        n = sum(c.values())
        be[g] = -sum((v / n) * math.log2(v / n) for v in c.values() if v)
    return be


def segment(S, be, k):
    cuts = [0]
    for i in range(k, len(S) - k):
        g0 = S[i - k:i]; g1 = S[i - k + 1:i + 1]
        if g0 in be and g1 in be and be[g1] > be[g0] + 0.5:
            cuts.append(i)
    cuts.append(len(S))
    segs = [S[cuts[j]:cuts[j + 1]] for j in range(len(cuts) - 1)]
    return [s for s in segs if s]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    S = load.dense_stream()
    be = branching_table(S, K)
    segs = segment(S, be, K)
    lens = Counter(len(s) for s in segs)
    top = Counter(s for s in segs if len(s) >= 3).most_common(15)
    meanlen = sum(len(s) for s in segs) / len(segs)
    namelike = sum(1 for s in segs if any(f in s for f in FAM)) / len(segs)

    # null
    sh = list(S); rng.shuffle(sh); sh = "".join(sh)
    be2 = branching_table(sh, K)
    segs2 = segment(sh, be2, K)
    meanlen2 = sum(len(s) for s in segs2) / len(segs2)
    namelike2 = sum(1 for s in segs2 if any(f in s for f in FAM)) / len(segs2)

    result = {"seed": 1583, "k": K, "n_segments": len(segs), "mean_len": round(meanlen, 2),
              "len_hist": {str(k): v for k, v in sorted(lens.items())[:12]},
              "top_segments": top, "name_like_frac": round(namelike, 4),
              "null_mean_len": round(meanlen2, 2), "null_name_like": round(namelike2, 4)}
    print(f"[SEG] {len(segs)} segmentos, comprimento médio {meanlen:.2f} (null {meanlen2:.2f})", flush=True)
    print(f"[SEG] fração 'parece nome' {namelike:.3f} vs null {namelike2:.3f}", flush=True)
    print(f"[SEG] top segmentos (>=3): {top[:8]}", flush=True)
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "210_boundary_seg.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
