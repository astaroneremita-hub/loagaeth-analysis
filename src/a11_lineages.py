"""
11 - The two houses: CHAST (the queen root) vs GETH (the rival lineage).

Questions, each with a null:
  A) Family: how many distinct prefixed variants does each root take, how often, how far?
  B) Morphology: is the root word-INITIAL-ish (takes prefixes, continues) or word-FINAL
     (closes a word)? Measured by left/right context diversity and by what follows the root.
  C) Territory: do the two houses divide the tables (rivals) or share them (same court)?
     Pearson correlation of per-table counts, against frequency-matched random roots.
  D) Co-location: inside a table, does GETH sit near CHAST more than chance?
     Distance from each GETH to the nearest CHAST vs GETH positions shuffled in the table.

Data: data/loagaeth_tables.json (dense stream per table; leaf 1 excluded).
"""
import json
import math
import random
import statistics
from collections import Counter

import load

ROOTS = ["CHAST", "GETH"]
PREFIXES = ["UOL", "PLI", "PRI", "NO", "NE", "NA", "ZI", "ZU", "AL", "AR", "UOR", "UA", "UL", "UN", "PAL", "OX"]


def tables_dense():
    return {n: s for n, s in load.all_tables().items() if n != 1}


def positions(s, sub):
    out, i = [], s.find(sub)
    while i >= 0:
        out.append(i)
        i = s.find(sub, i + 1)
    return out


def entropy(counter):
    t = sum(counter.values()) or 1
    return -sum((c / t) * math.log2(c / t) for c in counter.values() if c)


def family(root, tabs):
    pre = Counter()
    left, right = Counter(), Counter()
    occ, reach = 0, 0
    for s in tabs.values():
        ps = positions(s, root)
        if ps:
            reach += 1
        occ += len(ps)
        for i in ps:
            left[s[max(0, i - 2):i]] += 1
            right[s[i + len(root):i + len(root) + 2]] += 1
            for p in sorted(PREFIXES, key=len, reverse=True):
                if s[max(0, i - len(p)):i] == p:
                    pre[p] += 1
                    break
    return {
        "occurrences": occ, "tables_reached": reach,
        "prefix_variants": dict(pre.most_common()),
        "n_prefix_types": len(pre),
        "left_context_entropy": round(entropy(left), 2),
        "right_context_entropy": round(entropy(right), 2),
        "top_following": right.most_common(6),
        "top_preceding": left.most_common(6),
    }


def pearson(a, b):
    n = len(a)
    ma, mb = sum(a) / n, sum(b) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(a, b))
    den = (sum((x - ma) ** 2 for x in a) * sum((y - mb) ** 2 for y in b)) ** 0.5
    return num / den if den else 0.0


def run():
    rng = random.Random(11)
    tabs = tables_dense()
    order = sorted(tabs)
    fam = {r: family(r, tabs) for r in ROOTS}

    # C) territory correlation vs frequency-matched null
    vec = {r: [tabs[n].count(r) for n in order] for r in ROOTS}
    r_obs = pearson(vec["CHAST"], vec["GETH"])
    # pool of 4-5-grams with total frequency close to GETH's
    target = sum(vec["GETH"])
    whole = "".join(tabs[n] for n in order)
    pool = Counter(whole[i:i + 4] for i in range(len(whole) - 3))
    cands = [g for g, f in pool.items() if abs(f - target) <= max(5, target * 0.15) and "?" not in g]
    null_r = []
    for g in rng.sample(cands, min(300, len(cands))):
        null_r.append(pearson(vec["CHAST"], [tabs[n].count(g) for n in order]))
    mu, sd = statistics.mean(null_r), statistics.pstdev(null_r) or 1

    # D) co-location
    def mean_nearest(shuffle=False):
        ds = []
        for n in order:
            s = tabs[n]
            c = positions(s, "CHAST")
            g = positions(s, "GETH")
            if not c or not g:
                continue
            if shuffle:
                g = [rng.randrange(len(s)) for _ in g]
            for gi in g:
                ds.append(min(abs(gi - ci) for ci in c))
        return statistics.mean(ds) if ds else None
    d_obs = mean_nearest()
    d_null = [mean_nearest(True) for _ in range(300)]
    dmu, dsd = statistics.mean(d_null), statistics.pstdev(d_null) or 1

    both = sum(1 for n in order if vec["CHAST"][order.index(n)] and vec["GETH"][order.index(n)])
    only_c = sum(1 for i in range(len(order)) if vec["CHAST"][i] and not vec["GETH"][i])
    only_g = sum(1 for i in range(len(order)) if vec["GETH"][i] and not vec["CHAST"][i])

    res = {
        "A_B_families": fam,
        "C_territory": {
            "pearson_CHAST_GETH": round(r_obs, 2),
            "null_mean": round(mu, 2), "null_sd": round(sd, 2),
            "z": round((r_obs - mu) / sd, 1),
            "tables_both": both, "only_CHAST": only_c, "only_GETH": only_g,
            "verdict": ("SHARED court (co-occur beyond chance)" if r_obs > mu + 3 * sd else
                        "RIVAL territories (avoid each other)" if r_obs < mu - 3 * sd else
                        "independent (no territorial relation beyond chance)"),
        },
        "D_colocation": {
            "mean_distance_GETH_to_nearest_CHAST": round(d_obs, 1) if d_obs else None,
            "null_mean": round(dmu, 1), "null_sd": round(dsd, 1),
            "z": round((d_obs - dmu) / dsd, 1) if d_obs else None,
            "verdict": ("GETH clusters NEAR CHAST" if d_obs and d_obs < dmu - 3 * dsd else
                        "GETH keeps AWAY from CHAST" if d_obs and d_obs > dmu + 3 * dsd else
                        "no local attraction"),
        },
        "series_per_table": {"tables": order, "CHAST": vec["CHAST"], "GETH": vec["GETH"]},
    }
    load.save_result("11_lineages", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
