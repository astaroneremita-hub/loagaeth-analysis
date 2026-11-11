"""
43 - Recency: does the text remember what it has just written?

Module a42 found that long repeats fall on neighbouring sides. Here the same question inside a side,
line by line, and as a model.

  A) Echo by distance. Share of the 8-letter strings of a line that occur again d lines further down
     the same side (d = 1 ... 30), against the same side with its lines in random order (same
     content, order destroyed). And from one side to the next ones (d sides further).
  B) A model with a memory. A letter model (three letters of context) trained on half the sides
     reads the other half. Then it is given a cache: the last W letters it has just read on the same
     side also count, with weight L. If the text reuses its recent past, the cache lowers the bits
     per letter; the best W measures the span of that memory. Control: the same sides with their
     lines shuffled (a cache then finds the same material, but not nearby).
"""
import json
import random
import statistics
from collections import Counter, defaultdict, deque

import load
from a22_robustness_and_depth import base_book, tnum

V = 21


def echo(face_lines, maxd, L=8):
    sets = [{r[i:i + L] for i in range(len(r) - L + 1)} for r in face_lines]
    out = [[0, 0] for _ in range(maxd + 1)]
    for i, a in enumerate(sets):
        if not a:
            continue
        for d in range(1, maxd + 1):
            if i + d < len(sets):
                out[d][0] += len(a & sets[i + d])
                out[d][1] += len(a)
    return out


def A_lines(book, keys, rng, maxd=30):
    def total(order):
        tot = [[0, 0] for _ in range(maxd + 1)]
        for k in keys:
            ls = [r for r in book[k] if r]
            if order:
                ls = ls[:]
                rng.shuffle(ls)
            for d, (a, b) in enumerate(echo(ls, maxd)):
                tot[d][0] += a
                tot[d][1] += b
        return [a / b if b else 0 for a, b in tot]
    real = total(False)
    nul = [total(True) for _ in range(40)]
    rows = []
    for d in (1, 2, 3, 4, 5, 7, 10, 15, 20, 30):
        xs = [n[d] for n in nul]
        rows.append({"lines_apart": d, "echo_per_1000": round(1000 * real[d], 2), "shuffled_lines": round(1000 * statistics.mean(xs), 2),
                     "ratio": round(real[d] / max(1e-9, statistics.mean(xs)), 2),
                     "p": round((sum(x >= real[d] for x in xs) + 1) / (len(xs) + 1), 3)})
    return rows


def A_sides(book, keys, rng, L=8):
    sets = [{r[i:i + L] for r in book[k] for i in range(len(r) - L + 1)} for k in keys]

    def curve(order):
        out = []
        for d in (1, 2, 3, 4, 6, 8, 12, 20):
            v = [len(sets[order[i]] & sets[order[i + d]]) / max(1, min(len(sets[order[i]]), len(sets[order[i + d]])))
                 for i in range(len(order) - d)]
            out.append(statistics.mean(v))
        return out
    idx = list(range(len(keys)))
    real = curve(idx)
    nul = []
    for _ in range(200):
        sh = idx[:]
        rng.shuffle(sh)
        nul.append(curve(sh))
    return [{"sides_apart": d, "shared_per_1000": round(1000 * real[j], 1), "random_order": round(1000 * statistics.mean(n[j] for n in nul), 1),
             "p": round((sum(n[j] >= real[j] for n in nul) + 1) / 201, 3)} for j, d in enumerate((1, 2, 3, 4, 6, 8, 12, 20))]


def bits_with_cache(static, nstatic, faces, W, lam, alpha=0.1):
    import math
    tot = n = 0
    for lines in faces:
        dyn = defaultdict(Counter)
        ndyn = Counter()
        q = deque()
        for r in lines:
            s = "^^^" + r
            for i in range(3, len(s)):
                ctx, ch = s[i - 3:i], s[i]
                p = (static[ctx][ch] + lam * dyn[ctx][ch] + alpha) / (nstatic[ctx] + lam * ndyn[ctx] + alpha * V)
                tot -= math.log2(p)
                n += 1
                if W:
                    dyn[ctx][ch] += 1
                    ndyn[ctx] += 1
                    q.append((ctx, ch))
                    if len(q) > W:
                        c0, h0 = q.popleft()
                        dyn[c0][h0] -= 1
                        ndyn[c0] -= 1
    return tot / n


def B_cache(book, keys, rng):
    train = [r for k in keys[0::2] for r in book[k] if r]
    static = defaultdict(Counter)
    nstatic = Counter()
    for r in train:
        s = "^^^" + r
        for i in range(3, len(s)):
            static[s[i - 3:i]][s[i]] += 1
            nstatic[s[i - 3:i]] += 1
    test = [[r for r in book[k] if r] for k in keys[1::2]]
    shuf = []
    for ls in test:
        x = ls[:]
        rng.shuffle(x)
        shuf.append(x)
    base = bits_with_cache(static, nstatic, test, 0, 0)
    rows = []
    for W in (100, 300, 1000, 3000, 10 ** 9):
        best = min(((bits_with_cache(static, nstatic, test, W, lam), lam) for lam in (1, 4, 16)))
        ctrl = bits_with_cache(static, nstatic, shuf, W, best[1])
        rows.append({"cache_letters": "whole side so far" if W > 10 ** 6 else W, "weight": best[1], "bits_per_letter": round(best[0], 4),
                     "same_with_lines_shuffled": round(ctrl, 4), "gain_from_order": round(ctrl - best[0], 4)})
    return {"no_cache_bits_per_letter": round(base, 4), "with_cache": rows}


def C_short_echo(book, keys, rng, L=5, reps=300):
    """One planned test after the profile of A: 5-letter strings echoed 1-4 lines below, in the
    row-written tables (2-24), and whether the echo sits near the same column (within 3)."""
    faces = [[r for r in book[k] if r] for k in keys if 2 <= tnum(k) <= 24]

    def stat(fs):
        near = [0, 0]
        far = [0, 0]
        col = [0, 0]
        for ls in fs:
            pos = [{} for _ in ls]
            for i, a in enumerate(ls):
                for x in range(len(a) - L + 1):
                    pos[i].setdefault(a[x:x + L], x)
            for i in range(len(ls)):
                if not pos[i]:
                    continue
                for d in range(1, 17):
                    if i + d >= len(ls):
                        break
                    hit = [abs(pos[i + d][g] - x) for g, x in pos[i].items() if g in pos[i + d]]
                    t = near if d <= 4 else far
                    t[0] += len(hit)
                    t[1] += len(pos[i])
                    if d <= 4:
                        col[0] += sum(h <= 3 for h in hit)
                        col[1] += len(hit)
        return near[0] / near[1], far[0] / far[1], col[0] / max(1, col[1])
    real = stat(faces)
    nul = []
    for _ in range(reps):
        sh = []
        for ls in faces:
            x = ls[:]
            rng.shuffle(x)
            sh.append(x)
        nul.append(stat(sh))
    out = {}
    for j, name in enumerate(("echo_1_to_4_lines_below_per_1000", "echo_5_to_16_lines_below_per_1000", "share_of_near_echoes_within_3_columns")):
        xs = [n[j] for n in nul]
        k = 1000 if j < 2 else 1
        out[name] = {"book": round(k * real[j], 3), "lines_shuffled": round(k * statistics.mean(xs), 3),
                     "z": round((real[j] - statistics.mean(xs)) / (statistics.pstdev(xs) or 1), 1),
                     "p": round((sum(x >= real[j] for x in xs) + 1) / (reps + 1), 4)}
    return out


def run():
    rng = random.Random(43)
    book = base_book()
    keys = sorted(book, key=lambda k: (tnum(k), k))
    res = {"A_echo_by_lines": A_lines(book, keys, rng), "A_echo_by_sides": A_sides(book, keys, rng), "B_cache_model": B_cache(book, keys, rng),
           "C_short_echo": C_short_echo(book, keys, rng)}
    load.save_result("43_recency", res)
    return res


if __name__ == "__main__":
    r = run()
    for k, v in r.items():
        print(k)
        for x in (v if isinstance(v, list) else list(v.items())):
            print("  ", x)
