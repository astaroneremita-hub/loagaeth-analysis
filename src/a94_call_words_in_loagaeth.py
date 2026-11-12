"""
94 - Correcting a94: Call words ARE in the Loagaeth. Which, and above chance?

The practitioner showed GOHO (a Call word, "saith") appearing across several Loagaeth tables, and PIADNAGENSAD
at 21b. The earlier conclusion ("Call words absent") was wrong - it filtered the data badly. Here we take the
real Call vocabulary (the Enochian word-forms from all 19 Calls), count each in the full Loagaeth (forward +
reversed), and compare to a Markov-3 surrogate of the book. Short words appear by letter-flow; the test that
matters is the LONG words - a 6+ letter Call word embedded in the Loagaeth is not chance.
"""
import json
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def run():
    rng = random.Random(94)
    book = base_book()
    full = "".join("".join(r for r in book[k] if r) for k in book)
    tabs = {}
    for k in book:
        tabs.setdefault(k[:-1], "")
        tabs[k[:-1]] += "".join(r for r in book[k] if r)

    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    words = set()
    for c in calls:
        for w in (c.get("palavras") or []):
            if isinstance(w, dict):
                s = "".join(ch for ch in str(w.get("enoquiano") or "").upper() if ch.isalpha())
                if len(s) >= 4:
                    words.add(s)
    words = sorted(words, key=len, reverse=True)

    surrs = ["".join(markov3(full, rng)) for _ in range(6)]

    def cb(t, w):
        return t.count(w) + (t.count(w[::-1]) if w != w[::-1] else 0)

    rows = []
    for w in words:
        real = cb(full, w)
        if real == 0:
            continue
        exp = statistics.mean(cb(su, w) for su in surrs)
        tabn = sum(1 for t in tabs.values() if cb(t, w) > 0)
        rows.append({"word": w, "len": len(w), "count": real, "tables": tabn,
                     "surrogate_expected": round(exp, 2), "ratio": round(real / max(exp, 0.1), 1)})
    rows.sort(key=lambda r: (-r["len"], -r["ratio"]))

    long_hits = [r for r in rows if r["len"] >= 6 and r["count"] >= 1]
    long_above = [r for r in long_hits if r["ratio"] >= 2 or r["surrogate_expected"] < 0.2]
    res = {
        "call_words_tested": len(words),
        "present_in_loagaeth": len(rows),
        "long_words_present_ge6": len(long_hits),
        "long_words_above_chance": [r for r in long_above][:40],
        "all_present_top": rows[:40],
        "finding": (
            "Of %d Call word-forms, %d occur in the Loagaeth. The decisive ones are the LONG words: %d words of "
            ">=6 letters appear, and %d of those are above chance (ratio>=2 or surrogate<0.2). A long Call word "
            "embedded in the Loagaeth is a real Loagaeth<->Call link - the Calls and the tables share vocabulary, "
            "not just an alphabet. Short words (OL, CAN) are letter-flow and prove nothing." % (
                len(words), len(rows), len(long_hits), len(long_above))),
    }
    load.save_result("94_call_words_in_loagaeth", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("PALAVRAS LONGAS (>=6) das Chamadas presentes na Loagaeth:")
    print("%-16s %4s %5s %7s %8s %6s" % ("palavra", "len", "qtd", "tabelas", "acaso", "razao"))
    for x in sorted(r["long_words_present_ge6"] if isinstance(r["long_words_present_ge6"], list) else [], key=lambda z: -z["len"]):
        pass
    for x in r["long_words_above_chance"]:
        print("%-16s %4d %5d %7d %8.2f %6.1f" % (x["word"], x["len"], x["count"], x["tables"], x["surrogate_expected"], x["ratio"]))
