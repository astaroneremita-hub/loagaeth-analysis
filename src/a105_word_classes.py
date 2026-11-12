"""
105 - Grammatical classes (plan item 15): do words fall into distributional classes?

In a real language, words of the same class share contexts (nouns pattern like nouns, particles like particles).
We take the most frequent maximal words, build each word's context vector (distribution of the letter just
before + just after, across all occurrences), and cluster by cosine similarity. If distinct clusters emerge, the
Loagaeth words carry distributional classes - another language-signature. Null: the same clustering on a Markov-3
surrogate (which has the same local flow but no word grammar) should be mushier.
"""
import json
import math
import random
from collections import Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def context_vec(text, w):
    before, after = Counter(), Counter()
    start = 0
    n = 0
    while True:
        i = text.find(w, start)
        if i < 0:
            break
        before[text[i - 1] if i > 0 else "^"] += 1
        after[text[i + len(w)] if i + len(w) < len(text) else "$"] += 1
        start = i + 1
        n += 1
    v = {}
    for k, val in before.items():
        v["L" + k] = val
    for k, val in after.items():
        v["R" + k] = val
    s = sum(v.values()) or 1
    return {k: val / s for k, val in v.items()}, n


def cosine(a, b):
    keys = set(a) | set(b)
    na = sum(x * x for x in a.values()) ** 0.5
    nb = sum(x * x for x in b.values()) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return sum(a.get(k, 0) * b.get(k, 0) for k in keys) / (na * nb)


def cluster(words, vecs, thr=0.85):
    groups = []
    for w in words:
        placed = False
        for g in groups:
            if cosine(vecs[w], vecs[g[0]]) >= thr:
                g.append(w)
                placed = True
                break
        if not placed:
            groups.append([w])
    return groups


def run():
    rng = random.Random(105)
    book = base_book()
    full = "".join("".join(r for r in book[k] if r) for k in book)

    try:
        mx = json.load(open(load.ROOT + "/viz/maximal_words.json", encoding="utf-8"))
        words = [x["w"] for x in mx[:60]]
    except Exception:
        cat = json.load(open(load.ROOT + "/viz/word_catalog.json", encoding="utf-8"))["lengths"]
        words = [x["w"] for x in cat["5"][:60]]

    vecs = {w: context_vec(full, w)[0] for w in words}
    groups = [g for g in cluster(words, vecs) if len(g) >= 2]

    # null: surrogate
    surr = "".join(markov3(full, rng))
    svecs = {w: context_vec(surr, w)[0] for w in words}
    sgroups = [g for g in cluster(words, svecs) if len(g) >= 2]

    res = {
        "words": len(words),
        "clusters_real": len(groups),
        "clustered_words_real": sum(len(g) for g in groups),
        "clusters_surrogate": len(sgroups),
        "clustered_words_surrogate": sum(len(g) for g in sgroups),
        "groups_sample": [g for g in sorted(groups, key=len, reverse=True)[:8]],
        "note": "cluster = palavras com contexto (letra antes/depois) parecido (cosseno>=0.85). Mais agrupamento "
                "que o surrogate = classes distribucionais reais.",
        "finding": "",
    }
    real_c = res["clustered_words_real"]
    surr_c = res["clustered_words_surrogate"]
    verdict = ("CONFIRMADO: as palavras caem em classes distribucionais (%d agrupadas vs %d no surrogate) - "
               "palavras do mesmo tipo partilham contexto, uma assinatura de gramatica." % (real_c, surr_c)) \
        if real_c > surr_c + 4 else \
        ("classes fracas: agrupam quase como o surrogate (%d vs %d) - o contexto e dominado pelo fluxo de letras." % (real_c, surr_c))
    res["finding"] = verdict
    load.save_result("105_word_classes", res)
    return res


if __name__ == "__main__":
    r = run()
    print("real: %d grupos, %d palavras agrupadas | surrogate: %d grupos, %d palavras\n" % (
        r["clusters_real"], r["clustered_words_real"], r["clusters_surrogate"], r["clustered_words_surrogate"]))
    print("grupos (classes candidatas):")
    for g in r["groups_sample"]:
        print("  ", ", ".join(g))
    print("\n" + r["finding"])
