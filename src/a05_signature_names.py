"""
05 - Per-table signature names.

For each table, find the 6-gram that is most distinctive to it: frequent inside the
table but present in only a few tables overall. Score = freq_in_table restricted to
grams that appear in at most MAX_TABLES tables. This surfaces a per-table proper
name distinct from the shared master stem.

Finding: nearly every table has its own signature name, and (reported) essentially
none of them belong to the CHASTOR family. So the structure is one shared master
stem plus a unique local name per table.
"""
from collections import Counter, defaultdict

import load

K = 6
MAX_TABLES = 3
MIN_IN_TABLE = 2


def run():
    tables = load.all_tables()
    gram_tables = defaultdict(set)
    per_table_counts = {}
    for n, s in tables.items():
        c = Counter(load.ngrams(s, K))
        per_table_counts[n] = c
        for gram in c:
            gram_tables[gram].add(n)

    signatures = {}
    for n in sorted(tables):
        best, best_score = None, -1
        for gram, f in per_table_counts[n].items():
            if f >= MIN_IN_TABLE and len(gram_tables[gram]) <= MAX_TABLES:
                score = f / len(gram_tables[gram])
                if score > best_score:
                    best, best_score = gram, score
        signatures[n] = best

    sig_list = [g for g in signatures.values() if g]
    chastor_fam = sum(1 for g in sig_list
                      if "CHAST" in g or "CHUST" in g or "NOCHA" in g)

    res = {
        "k": K,
        "max_tables_for_distinctive": MAX_TABLES,
        "n_tables_with_signature": len(sig_list),
        "signatures": {str(n): g for n, g in signatures.items()},
        "signatures_in_chastor_family": chastor_fam,
        "note": "Distinct per-table names coexisting with the shared master stem.",
    }
    load.save_result("05_signature_names", res)
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=1))
