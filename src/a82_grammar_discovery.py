"""
82 - Discover new names with the grammar: generate root+affix, keep the ones the book actually carries.

If the generative grammar (a81) is real - roots plus a small set of productive affixes - then root+affix
combinations we never listed should ALSO be present in the book, above what the letter-flow alone would give.
So: generate every prefix x root x suffix, count each in the book (forward + reversed), and compare to the
count a Markov-3 surrogate of the book gives (same local letter-flow, no planted names). Combinations that
beat the surrogate and appear in >= 2 tables are newly-confirmed names and branches, predicted by the grammar
and verified in the text - not hand-picked.
"""
import json
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]
PRE = ["", "AD", "AL", "I", "NO", "NE", "ZI", "AX", "A", "AN", "DN"]
SUF = ["", "P", "PH", "STOR", "TO", "TOR", "A", "AL", "AD", "AX", "OR", "AN"]


def count_both(text, nm):
    return text.count(nm) + (text.count(nm[::-1]) if nm != nm[::-1] else 0)


def run():
    rng = random.Random(82)
    book = base_book()
    text = "".join("".join(r for r in book[k] if r) for k in book)
    # per-table texts to count how many tables a name appears in
    tabs = {k: "".join(r for r in book[k] if r) for k in book}

    known = set(ROOTS)
    try:
        cat = json.load(open(load.RESULTS + "/23_name_discovery.json", encoding="utf-8"))["A_candidates"]["top"]
        known |= {x["name"] for x in cat}
    except Exception:
        pass

    # candidates
    cands = set()
    for root in ROOTS:
        for p in PRE:
            for s in SUF:
                nm = p + root + s
                if len(nm) >= 5:
                    cands.add((nm, root, p, s))

    # surrogate expected counts: build 6 Markov-3 surrogates of the book, count each candidate
    surrs = ["".join(markov3(text, rng)) for _ in range(6)]

    rows = []
    for nm, root, p, s in cands:
        real = count_both(text, nm)
        if real == 0:
            continue
        tabn = sum(1 for t in tabs.values() if count_both(t, nm) > 0)
        exp = statistics.mean(count_both(su, nm) for su in surrs)
        ratio = real / max(exp, 0.3)
        rows.append({"name": nm, "root": root, "prefix": p, "suffix": s,
                     "count": real, "tables": tabn, "surrogate_expected": round(exp, 1),
                     "ratio": round(ratio, 1), "new": nm not in known})

    # keep the ones that beat the surrogate and span tables
    confirmed = [r for r in rows if r["ratio"] >= 1.5 and r["tables"] >= 3 and r["count"] >= 5]
    confirmed.sort(key=lambda r: -r["ratio"])
    new_names = [r for r in confirmed if r["new"]]

    res = {
        "candidates_tested": len(cands),
        "present_in_book": len(rows),
        "confirmed_above_surrogate": len(confirmed),
        "newly_confirmed_names": len(new_names),
        "note": "A candidate is 'confirmed' when it occurs >=5x across >=3 tables and at least 1.5x more than a "
                "Markov-3 surrogate of the book predicts. 'new' = not in the prior catalogue or root list.",
        "top_new_names": new_names[:40],
        "top_confirmed_all": confirmed[:25],
        "by_affix": {},
    }
    # which affixes produced the most confirmed names
    pc = Counter(r["prefix"] for r in confirmed if r["prefix"])
    sc = Counter(r["suffix"] for r in confirmed if r["suffix"])
    res["by_affix"] = {"productive_prefixes": pc.most_common(), "productive_suffixes": sc.most_common()}
    res["finding"] = (
        "The grammar predicts real names. Of %d root+affix candidates, %d occur in the book and %d beat a "
        "Markov-3 surrogate across >=3 tables; %d of those were NOT in the prior catalogue - new branches the "
        "grammar generated and the text confirms. Most productive prefixes: %s; suffixes: %s." % (
            len(cands), len(rows), len(confirmed), len(new_names),
            ", ".join("%s(%d)" % x for x in pc.most_common(4)),
            ", ".join("%s(%d)" % x for x in sc.most_common(4))))
    load.save_result("82_grammar_discovery", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("NEW names the grammar found (ratio vs surrogate | count | tables):")
    for x in r["top_new_names"][:30]:
        aff = ("%s-" % x["prefix"] if x["prefix"] else "") + x["root"] + ("-%s" % x["suffix"] if x["suffix"] else "")
        print("  %-13s %-16s x%-3d in %2d tables  ratio %.1f" % (x["name"], aff, x["count"], x["tables"], x["ratio"]))
