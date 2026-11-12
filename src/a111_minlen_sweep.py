"""
111 - At which minimum word length does the reading stop being noise? Sweep minlen 1..6 vs a null.

The square reading looks like word-salad partly because short dictionary words (2-3 letters) match everywhere by
chance. The honest way to find the "real" reading scale: for each minimum word length, tile the whole book (greedy
longest-first) with Dee's own lexicon, measure letter-coverage, and compare to 10 Markov-3 surrogate books. The
minlen whose real coverage stands FURTHEST above the surrogate (highest z) is the scale at which the Loagaeth
carries real Angelical vocabulary rather than accidental letter-runs. If even the best z is small, no minlen makes
it a sentence - the honest reading is 'Call-word fragments in a field of names', not prose.
"""
import json
import random
import unicodedata

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def dee_vocab(min_len):
    v = {}
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for w in c["palavras"]:
            k = da(w["chave"])
            if len(k) >= min_len:
                v[k] = 1
    return set(v)


def tile_cover(text, vocab, min_len, maxw=9):
    i, cov = 0, 0
    n = len(text)
    while i < n:
        hit = 0
        for L in range(min(maxw, n - i), min_len - 1, -1):
            if text[i:i + L] in vocab:
                hit = L
                break
        if hit:
            cov += hit
            i += hit
        else:
            i += 1
    return cov


def run():
    book = base_book()
    rows = [r for k in book for r in book[k] if r]
    full = "".join(rows)
    surrogates = ["".join(markov3(full, random.Random(1110 + s))) for s in range(10)]

    out = []
    for ml in range(1, 7):
        vocab = dee_vocab(ml)
        tot = sum(len(r) for r in rows)
        real = sum(tile_cover(r, vocab, ml) for r in rows) / tot
        surs = []
        for st in surrogates:
            p, cov = 0, 0
            for r in rows:
                cov += tile_cover(st[p:p + len(r)], vocab, ml)
                p += len(r)
            surs.append(cov / tot)
        mean = sum(surs) / len(surs)
        sd = (sum((x - mean) ** 2 for x in surs) / len(surs)) ** 0.5
        z = (real - mean) / sd if sd else 0.0
        out.append({"min_len": ml, "vocab": len(vocab), "real_pct": round(real * 100, 2),
                    "surr_pct": round(mean * 100, 2), "surr_max_pct": round(max(surs) * 100, 2),
                    "z": round(z, 1), "beats_null": real > max(surs) and z >= 3})

    best = max(out, key=lambda o: o["z"])
    any_real = [o for o in out if o["beats_null"]]
    verdict = ("A escala com mais sinal é minlen=%d (z=%.1f, real %.2f%% vs surrogate %.2f%%). %s" % (
        best["min_len"], best["z"], best["real_pct"], best["surr_pct"],
        ("Mas mesmo a melhor escala mal passa do ruído — nenhum comprimento mínimo transforma a leitura em frase; "
         "o honesto é 'fragmentos de palavra das Chamadas num campo de nomes'."
         if best["z"] < 4 else
         "Nessa escala a leitura carrega vocabulário real acima do acaso — é a escala a usar no frontend.")))
    res = {"sweep": out, "best_min_len": best["min_len"], "best_z": best["z"], "finding": verdict}
    load.save_result("111_minlen_sweep", res)
    return res


if __name__ == "__main__":
    r = run()
    print("minlen | vocab | real%  | surrogate% (max) | z    | bate null?")
    for o in r["sweep"]:
        print("  %d    |  %4d | %5.2f | %5.2f (%5.2f)   | %+4.1f | %s" % (
            o["min_len"], o["vocab"], o["real_pct"], o["surr_pct"], o["surr_max_pct"], o["z"],
            "SIM" if o["beats_null"] else "nao"))
    print("\n" + r["finding"])
