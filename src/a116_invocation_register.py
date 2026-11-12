"""
116 - Does the readable vocabulary of the squares skew to the INVOCATION register above chance?

The Google-translate 'sermon' felt coherent because the glosses that survive (the Nine, the First, is all One, the
Spirits, with darkness, visit us) are invocation-register words - the language of calling powers. But presence of
Call words is letter-driven (a107/a110), so maybe short invocation words just happen to be frequent. Honest test:
of the gloss TOKENS the real book yields (greedy tiling, Dee vocab), what fraction are invocation-register? Compare
to the same tiling on Markov-3 surrogate books (same letter statistics). If the real fraction beats the surrogate,
the squares' readable layer really leans toward invocation beyond what letter frequency forces.
"""
import json
import random
import re
import unicodedata

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book

INVOC = re.compile(r"\b(god|lord|spirit|spirits|holy|nine|first|one|heaven|heavens|power|powre|name|names|"
                   r"darknes|darkness|mighty|sound|sounds|voice|voices|elder|elders|visit|worship|worshipper|"
                   r"creation|creator|reign|governe?|everlasting|liveth|flame|comfort|highest)\b", re.I)


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def lexicon():
    lex = {}
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for w in c["palavras"]:
            k = da(w["chave"])
            g = (w.get("ingles_sl3191") or "").strip()
            if len(k) >= 2 and g and k not in lex:
                lex[k] = g
    return lex


def invoc_fraction(rows, lex, minlen=2):
    vocab = set(lex)
    inv = tot = 0
    for r in rows:
        i, n = 0, len(r)
        while i < n:
            hit = 0
            for L in range(min(9, n - i), minlen - 1, -1):
                if r[i:i + L] in vocab:
                    hit = L
                    break
            if hit:
                tot += 1
                if INVOC.search(lex[r[i:i + hit]]):
                    inv += 1
                i += hit
            else:
                i += 1
    return inv / tot if tot else 0, tot


def run():
    lex = lexicon()
    book = base_book()
    rows = [r for k in book for r in book[k] if r]
    real, ntok = invoc_fraction(rows, lex)

    full = "".join(rows)
    surs = []
    for s in range(10):
        st = "".join(markov3(full, random.Random(1160 + s)))
        srows, p = [], 0
        for r in rows:
            srows.append(st[p:p + len(r)]); p += len(r)
        surs.append(invoc_fraction(srows, lex)[0])
    mean = sum(surs) / len(surs)
    mx = max(surs)
    sd = (sum((x - mean) ** 2 for x in surs) / len(surs)) ** 0.5
    z = (real - mean) / sd if sd else 0.0

    verdict = ("CONFIRMADO: o vocabulário legível dos quadrados pende pro registro de invocação acima do acaso - "
               "%.1f%% dos tokens são palavras de invocação (Deus/Nove/Primeiro/Espíritos/trevas/nome) vs %.1f%% no "
               "surrogate (máx %.1f%%), z=%.1f. O tema de invocação é real, não só acaso de letra." % (
                   real * 100, mean * 100, mx * 100, z)) \
        if real > mx and z >= 3 else \
        ("sem viés: a fração de invocação é %.1f%% real vs %.1f%% surrogate (máx %.1f%%), z=%.1f - o 'tema' vem de as "
         "palavras curtas frequentes serem essas, não de um viés real de sentido." % (
             real * 100, mean * 100, mx * 100, z))

    res = {"tokens": ntok, "invoc_real_pct": round(real * 100, 1), "invoc_surr_pct": round(mean * 100, 1),
           "invoc_surr_max_pct": round(mx * 100, 1), "z": round(z, 1), "finding": verdict}
    load.save_result("116_invocation_register", res)
    return res


if __name__ == "__main__":
    r = run()
    print("tokens glosados: %d | invocação: real %.1f%% vs surrogate %.1f%% (máx %.1f%%) z=%.1f" % (
        r["tokens"], r["invoc_real_pct"], r["invoc_surr_pct"], r["invoc_surr_max_pct"], r["z"]))
    print("\n" + r["finding"])
