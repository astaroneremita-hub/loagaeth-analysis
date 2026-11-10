"""
10 - Territorial map: which master-name rules each table.

For every table we record the CHASTOR and CHUSTOR counts and the single most frequent
recurring 6-gram (its "local ruler" = the dominant recurring name of that zone), then
classify each table into a domain. The map shows the Loagaeth is partitioned into
name-dynasties: CHASTOR rules the centre-and-majority, CHUSTOR (its A->U twin) rules the
end, a -MACH family holds the opening, with void/border tables between.

The spatial structure is not chance: the per-table CHASTOR counts have lag-1
autocorrelation ~0.51 vs a shuffle null ~0.26 (95th ~0.36) - CHASTOR occupies a real
contiguous territory, not scattered positions.

"Ruler" here is a STATISTICAL label (most frequent recurring name), not an attested
angelic king. See docs/SESSION_FINDINGS.md for what these names are and are not.

Writes results/10_territory.json and data/loagaeth_territories.json.
"""
import json
import os
import random
import statistics
from collections import Counter

import load


def ruler(s, k=6, minf=3):
    c = Counter(s[i:i + k] for i in range(len(s) - k + 1))
    c = {g: f for g, f in c.items() if f >= minf}
    return max(c, key=c.get) if c else None


def run():
    tables = load.all_tables()
    tabs = sorted(tables)
    rows = []
    counts = []
    for n in tabs:
        s = tables[n]
        ch, cu = s.count("CHASTOR"), s.count("CHUSTOR")
        counts.append(ch)
        if n == 1:
            zone = "prophecy"
        elif ch >= 3:
            zone = "CHASTOR"
        elif cu >= 1 and ch == 0:
            zone = "CHUSTOR"
        elif ch > 0:
            zone = "border"
        elif len(s) < 400 or ruler(s) is None:
            zone = "void"
        else:
            zone = "frontier"
        rows.append({"table": n, "chastor": ch, "chustor": cu,
                     "local_ruler": ruler(s), "zone": zone})

    # zonation significance: lag-1 autocorrelation vs shuffle null
    mean = sum(counts) / len(counts)
    den = sum((c - mean) ** 2 for c in counts) or 1

    def ac1(seq):
        m = sum(seq) / len(seq)
        d = sum((x - m) ** 2 for x in seq) or 1
        return sum((seq[i] - m) * (seq[i + 1] - m) for i in range(len(seq) - 1)) / d
    obs = ac1(counts)
    rng = random.Random(10)
    null = []
    for _ in range(1000):
        c = counts[:]
        rng.shuffle(c)
        null.append(ac1(c))
    p95 = sorted(null)[949]

    res = {
        "n_tables": len(tabs),
        "zonation_lag1_autocorr": round(obs, 2),
        "null_mean": round(statistics.mean(null), 2),
        "null_95th": round(p95, 2),
        "zonation_verdict": "REAL contiguous territory" if obs > p95 else "no spatial structure",
        "tables": rows,
    }
    load.save_result("10_territory", res)
    # also publish the territory dataset
    with open(os.path.join(load.DATA, "loagaeth_territories.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": {"description": "Per-table master-name territory of the Loagaeth. "
                            "local_ruler = most frequent recurring 6-gram (statistical, not an attested king)."},
                   "tables": rows}, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
