"""
02 - Name-network structure (the "hive").

Build a graph whose nodes are recurring 6-grams (frequency >= MIN_FREQ) and whose
edges link two 6-grams that occur adjacently in the stream (the end of one is the
start of the next within a short gap). Then:
  - degree distribution
  - power-law exponent alpha via the Hill maximum-likelihood estimator
  - the top hubs by degree

Claim tested: the degree distribution is heavy-tailed (scale-free-like), i.e. a few
names act as hubs. The null-model comparison for "is this beyond chance" lives in
08_refutations / 07_null_models; here we report the observed structure and alpha.
"""
import math
from collections import Counter, defaultdict

import load

MIN_FREQ = 5
K = 6


def hill_alpha(degrees, xmin=1):
    xs = [d for d in degrees if d >= xmin]
    if len(xs) < 10:
        return None
    s = sum(math.log(x / (xmin - 0.5)) for x in xs)
    return 1 + len(xs) / s


def run():
    s = load.dense_stream()
    g = Counter(load.ngrams(s, K))
    nodes = {gram for gram, f in g.items() if f >= MIN_FREQ}

    # adjacency: step through the stream, link consecutive recurring grams
    adj = defaultdict(set)
    positions = []
    for i in range(len(s) - K + 1):
        gram = s[i:i + K]
        if gram in nodes:
            positions.append((i, gram))
    for (i1, g1), (i2, g2) in zip(positions, positions[1:]):
        if 0 < i2 - i1 <= K and g1 != g2:
            adj[g1].add(g2)
            adj[g2].add(g1)

    degrees = {n: len(adj[n]) for n in nodes}
    deg_seq = [d for d in degrees.values() if d > 0]
    alpha = hill_alpha(deg_seq, xmin=1)
    top = sorted(degrees.items(), key=lambda kv: kv[1], reverse=True)[:25]

    res = {
        "k": K,
        "min_freq": MIN_FREQ,
        "n_nodes": len(nodes),
        "n_edges": sum(len(v) for v in adj.values()) // 2,
        "mean_degree": round(sum(deg_seq) / len(deg_seq), 2) if deg_seq else 0,
        "max_degree": max(deg_seq) if deg_seq else 0,
        "powerlaw_alpha_hill": round(alpha, 3) if alpha else None,
        "top_hubs": [{"gram": gr, "degree": d, "freq": g[gr]} for gr, d in top],
        "note": "alpha in the ~2-3 band is the scale-free / heavy-tail signature.",
    }
    load.save_result("02_network", res)
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=1))
