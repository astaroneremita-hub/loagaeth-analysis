"""
102 - Maximal words: separate real words from fragments by branching entropy (plan item 2).

Thousands of substrings recur, but most are fragments of a few real words. A real word boundary is where MANY
different letters can follow (or precede): high branching entropy on both sides. A fragment always sits inside a
longer word, so one side has near-zero branching. For each frequent substring we compute left and right branching
entropy; the ones high on BOTH sides are the maximal, word-like units - the real lexicon.
"""
import json
import math
from collections import Counter, defaultdict

import load
from a22_robustness_and_depth import base_book


def entropy(counter):
    tot = sum(counter.values())
    if tot == 0:
        return 0.0
    return -sum((v / tot) * math.log2(v / tot) for v in counter.values())


def run():
    book = base_book()
    full = "".join("".join(r for r in book[k] if r) for k in book)
    N = len(full)

    cat = json.load(open(load.ROOT + "/viz/word_catalog.json", encoding="utf-8"))["lengths"]
    cand = set()
    for n in range(4, 11):
        for x in cat.get(str(n), [])[:200]:
            cand.add(x["w"])

    rows = []
    for w in cand:
        left, right = Counter(), Counter()
        cnt = 0
        start = 0
        while True:
            i = full.find(w, start)
            if i < 0:
                break
            cnt += 1
            left[full[i - 1] if i > 0 else "^"] += 1
            right[full[i + len(w)] if i + len(w) < N else "$"] += 1
            start = i + 1
        if cnt < 6:
            continue
        le, re = entropy(left), entropy(right)
        rows.append({"w": w, "count": cnt, "left_entropy": round(le, 2), "right_entropy": round(re, 2),
                     "boundary": round(min(le, re), 2)})
    rows.sort(key=lambda d: -d["boundary"])

    # a word is "maximal/word-like" if both sides branch a lot (boundary high)
    maximal = [r for r in rows if r["boundary"] >= 2.5]
    res = {
        "candidates": len(rows),
        "maximal_wordlike": len(maximal),
        "top_wordlike": rows[:30],
        "note": "boundary = min(entropia de ramificacao esquerda, direita). Alto nos dois lados = unidade de "
                "palavra (muitos contextos); baixo num lado = fragmento preso dentro de palavra maior.",
        "finding": (
            "Of %d frequent substrings, %d behave like MAXIMAL WORDS (high branching entropy on both sides, "
            ">=2.5 bits) - they stand free in many contexts, not stuck inside a longer word. These are the real "
            "lexical units; the rest are fragments. Top: %s." % (
                len(rows), len(maximal), ", ".join(r["w"] for r in rows[:8]))),
    }
    load.save_result("102_maximal_words", res)
    with open(load.ROOT + "/viz/maximal_words.json", "w", encoding="utf-8") as f:
        json.dump(rows[:200], f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("palavras mais 'livres' (contagem | ent.esq | ent.dir | fronteira):")
    for x in r["top_wordlike"][:18]:
        print("  %-10s %4d  L=%.2f R=%.2f  fronteira=%.2f" % (x["w"], x["count"], x["left_entropy"], x["right_entropy"], x["boundary"]))
