"""
106 - How strong is the word-order syntax? Directional collocation across many words (extends a101).

a101 found GETH-before-ACLAX fixed. Here we test the top recurring words (not just the 10 roots): for every
ordered pair, is the adjacency AB far from BA (fixed order) and above chance? If many pairs are strongly ordered
beyond a shuffled-word null, the Loagaeth has a real word-order grammar between units, not just inside them.
"""
import json
import random
import statistics

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def count_ordered(text, words, freq, N):
    """Unordered pairs (a<b) that chain >=3x and are >=3:1 asymmetric in direction."""
    pairs, ordered = 0, []
    for i, a in enumerate(words):
        for b in words[i + 1:]:
            ab = text.count(a + b)
            ba = text.count(b + a)
            if ab + ba >= 3:
                pairs += 1
                strong, weak = max(ab, ba), min(ab, ba)
                if strong >= 3 and strong >= 3 * max(1, weak):
                    ordered.append({"pair": (a + ">" + b) if ab >= ba else (b + ">" + a),
                                    "strong": strong, "weak": weak,
                                    "asym": round(strong / max(1, weak), 1)})
    return pairs, ordered


def run():
    rng = random.Random(106)
    book = base_book()
    full = "".join("".join(r for r in book[k] if r) for k in book)
    N = len(full)

    mx = json.load(open(load.ROOT + "/viz/maximal_words.json", encoding="utf-8"))
    words = [x["w"] for x in mx[:60]]
    freq = {w: full.count(w) for w in words}

    pairs, ordered = count_ordered(full, words, freq, N)
    ordered.sort(key=lambda p: (-p["asym"], -p["strong"]))

    # null: Markov-3 surrogate keeps local letter flow but destroys word-order grammar.
    surr_pairs_l, surr_ord_l = [], []
    for s in range(5):
        surr = "".join(markov3(full, random.Random(1060 + s)))
        sp, so = count_ordered(surr, words, freq, N)
        surr_pairs_l.append(sp)
        surr_ord_l.append(len(so))
    surr_ord = sum(surr_ord_l) / len(surr_ord_l)
    surr_pairs = sum(surr_pairs_l) / len(surr_pairs_l)

    real = len(ordered)
    verdict = ("CONFIRMADO: a ordem entre palavras é gramática real — %d pares fortemente ordenados no livro vs "
               "%.1f no surrogate Markov-3 (que preserva o fluxo de letras mas não a ordem das palavras). A "
               "assimetria não é ruído de contagem baixa; ela some quando a gramática some." % (real, surr_ord)) \
        if real >= surr_ord * 1.8 and real - surr_ord >= 6 else \
        ("ordem fraca: %d pares ordenados no livro vs %.1f no surrogate — a assimetria é compatível com ruído de "
         "contagem baixa, não prova sintaxe ampla." % (real, surr_ord))

    res = {
        "word_pairs_tested": pairs,
        "strongly_ordered_real": real,
        "strongly_ordered_surrogate_mean": round(surr_ord, 1),
        "pairs_surrogate_mean": round(surr_pairs, 1),
        "top_ordered": ordered[:25],
        "finding": verdict,
    }
    load.save_result("106_syntax_broad", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("real %d | surrogate medio %.1f pares ordenados\n" % (r["strongly_ordered_real"], r["strongly_ordered_surrogate_mean"]))
    print("pares com ordem fixa (forte/fraca | assimetria):")
    for p in r["top_ordered"][:16]:
        print("  %-16s %3d / %-3d  %.1fx" % (p["pair"], p["strong"], p["weak"], p["asym"]))
