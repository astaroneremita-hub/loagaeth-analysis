# -*- coding: utf-8 -*-
"""a212 - the OPEN half of analysis A: reading DIRECTION.

a158 recovered Dee's leaf sequence from content but scored max over sequence AND its reverse
(reflection symmetry) - so it never decided which END is the start. The diary: "Write the Book
backward ... the first leaf is the last." This tests direction.

Method: a directional order-3 letter model trained on within-leaf text (no boundary crossing).
For a leaf ORDER, score the cross-boundary flow: predict the first W letters of each leaf from
the last 3 of the previous leaf; mean per-letter surprise (bits) over the 47 junctions. Lower =
smoother flow. Compare forward [2..48], backward [48..2], and random leaf orders (null).
If forward != backward and one beats the null band, the book has a natural direction.

stdlib only. seed 1583.
"""
import os
import sys
import json
import math
import random
from collections import defaultdict, Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

K = 3
W = 8  # letters predicted after each junction


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    nums = [n for n in load.table_numbers() if n != 1]  # clean square leaves 2..48
    leaf = {n: load.table_text(n) for n in nums}

    # train order-3 model on within-leaf text (next-letter given 3-gram)
    ctx = defaultdict(Counter)
    for n in nums:
        s = leaf[n]
        for i in range(len(s) - K):
            ctx[s[i:i + K]][s[i + K]] += 1
    V = len(set("".join(leaf.values())))
    def surprise(prev3, nxt):
        c = ctx.get(prev3)
        if not c:
            return math.log2(V)
        tot = sum(c.values())
        p = (c.get(nxt, 0) + 0.5) / (tot + 0.5 * V)  # add-0.5 smoothing
        return -math.log2(p)

    def junction_cost(order):
        bits = 0.0; cnt = 0
        for a, b in zip(order, order[1:]):
            sa = leaf[a]; sb = leaf[b]
            prev3 = sa[-K:]
            for j in range(min(W, len(sb))):
                bits += surprise(prev3, sb[j])
                prev3 = (prev3 + sb[j])[-K:]
            cnt += min(W, len(sb))
        return bits / cnt

    fwd = junction_cost(nums)
    bwd = junction_cost(list(reversed(nums)))
    sims = []
    for _ in range(500):
        o = nums[:]; rng.shuffle(o); sims.append(junction_cost(o))
    m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
    zf = (fwd - m) / sd if sd else 0
    zb = (bwd - m) / sd if sd else 0

    print(f"[DIR] custo de junção (bits/letra, MENOR=flui melhor):", flush=True)
    print(f"  1->48 (transcrição): {fwd:.4f}  z={zf:+.2f}", flush=True)
    print(f"  48->1 (ordem de Dee): {bwd:.4f}  z={zb:+.2f}", flush=True)
    print(f"  null (ordem aleatória): {m:.4f} ± {sd:.4f}", flush=True)
    verd = ("1->48" if fwd < bwd else "48->1")
    diff_z = (bwd - fwd) / sd if sd else 0
    print(f"  melhor fluxo: {verd}  (diferença frente-ré = {diff_z:+.2f} sd)", flush=True)

    result = {"seed": 1583, "k": K, "W": W,
              "fwd_1to48": round(fwd, 4), "fwd_z": round(zf, 2),
              "bwd_48to1": round(bwd, 4), "bwd_z": round(zb, 2),
              "null_mean": round(m, 4), "null_sd": round(sd, 4),
              "smoother": verd, "dir_gap_sd": round(diff_z, 2)}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "212_reading_direction.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
