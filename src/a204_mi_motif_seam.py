# -*- coding: utf-8 -*-
"""a204 - three more lenses.

MI   - mutual information between column positions within a row, MI(X_c ; X_{c+k}) for
       k=1..10, averaged, vs null (shuffle each row). Is there columnar grammar beyond
       the immediate neighbour?
MOTIF- 2x2 block mining: most frequent 2x2 tiles vs null; does the field reuse motifs?
SEAM - dissect folhas 26-28 (the seam dialect): letter enrichment, bigram entropy, the
       most over/under-represented bigrams vs the rest of the book.

Writes results/204_mi_motif_seam.json. Seed 1583. stdlib only.
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
from a190_tower_traces import side_grids


def mi(pairs):
    """mutual information of a list of (a,b) pairs, in bits."""
    n = len(pairs)
    if n == 0:
        return 0.0
    pa = Counter(a for a, b in pairs); pb = Counter(b for a, b in pairs); pab = Counter(pairs)
    m = 0.0
    for (a, b), c in pab.items():
        pxy = c / n; px = pa[a] / n; py = pb[b] / n
        if pxy > 0:
            m += pxy * math.log2(pxy / (px * py))
    return m


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    sides = side_grids()
    grids = list(sides.values())
    result = {"seed": 1583}

    # ---------- MI between columns ----------
    def mi_at(gs, k):
        pairs = []
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H):
                for c in range(W - k):
                    pairs.append((g[r][c], g[r][c + k]))
        return mi(pairs)
    mis = {str(k): round(mi_at(grids, k), 4) for k in range(1, 11)}
    # null: shuffle each row
    def shuffle_rows(gs):
        out = []
        for g in gs:
            ng = []
            for row in g:
                l = list(row); rng.shuffle(l); ng.append("".join(l))
            out.append(ng)
        return out
    null_mi = defaultdict(list)
    for _ in range(10):
        sg = shuffle_rows(grids)
        for k in range(1, 11):
            null_mi[k].append(mi_at(sg, k))
    mi_report = {}
    for k in range(1, 11):
        m = sum(null_mi[k]) / len(null_mi[k]); sd = (sum((x - m) ** 2 for x in null_mi[k]) / len(null_mi[k])) ** 0.5
        z = (mis[str(k)] - m) / sd if sd else 0
        mi_report[str(k)] = {"obs": mis[str(k)], "null": round(m, 4), "z": round(z, 2)}
    result["MI_columns"] = mi_report
    print("[MI] por distância de coluna:", {k: v["obs"] for k, v in mi_report.items()}, flush=True)
    print("[MI] z:", {k: v["z"] for k, v in mi_report.items()}, flush=True)

    # ---------- 2x2 motif mining ----------
    def tiles(gs):
        c = Counter()
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H - 1):
                for cc in range(W - 1):
                    t = g[r][cc] + g[r][cc + 1] + g[r + 1][cc] + g[r + 1][cc + 1]
                    if "?" not in t:
                        c[t] += 1
        return c
    obs_t = tiles(grids)
    obs_top = obs_t.most_common(1)[0]
    # null: shuffle whole grids
    sims_top = []
    for _ in range(10):
        sg = []
        for g in grids:
            flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
            sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
        sims_top.append(tiles(sg).most_common(1)[0][1])
    m = sum(sims_top) / len(sims_top); sd = (sum((x - m) ** 2 for x in sims_top) / len(sims_top)) ** 0.5
    z = (obs_top[1] - m) / sd if sd else 0
    result["motif_2x2"] = {"top_tile": obs_top[0], "top_count": obs_top[1],
                           "null_top_mean": round(m, 1), "null_top_sd": round(sd, 1), "z": round(z, 2),
                           "top10": obs_t.most_common(10), "distinct": len(obs_t)}
    print(f"[MOTIF] tile 2x2 mais comum '{obs_top[0]}' {obs_top[1]}x vs null top {m:.0f}±{sd:.0f} z={z:+.2f} | {len(obs_t)} tiles distintos", flush=True)

    # ---------- seam 26-28 dissection ----------
    def is_seam(s):
        num = int("".join(ch for ch in s if ch.isdigit())); return 26 <= num <= 28
    seam_g = [g for s, g in sides.items() if is_seam(s)]
    rest_g = [g for s, g in sides.items() if not is_seam(s)]
    def letfreq(gs):
        c = Counter(ch for g in gs for row in g for ch in row if ch != "?")
        n = sum(c.values()); return {k: v / n for k, v in c.items()}, c
    sf, sc = letfreq(seam_g); rf, rc = letfreq(rest_g)
    enrich = sorted(((l, round(sf.get(l, 0) / rf.get(l, 1e-9), 2)) for l in set(sf) | set(rf)),
                    key=lambda x: -x[1])
    def bigram_entropy(gs):
        c = Counter()
        for g in gs:
            H = len(g); W = len(g[0])
            for r in range(H):
                for cc in range(W - 1):
                    c[g[r][cc] + g[r][cc + 1]] += 1
        n = sum(c.values())
        return -sum((v / n) * math.log2(v / n) for v in c.values() if v)
    result["seam_2628"] = {"letter_enrichment_top": enrich[:8], "letter_enrichment_bottom": enrich[-5:],
                           "bigram_entropy_seam": round(bigram_entropy(seam_g), 3),
                           "bigram_entropy_rest": round(bigram_entropy(rest_g), 3)}
    print("[SEAM] letras enriquecidas na costura:", enrich[:6], flush=True)
    print(f"[SEAM] entropia bigrama costura={bigram_entropy(seam_g):.3f} vs resto={bigram_entropy(rest_g):.3f}", flush=True)

    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "204_mi_motif_seam.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
