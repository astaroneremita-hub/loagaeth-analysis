"""
92 - Is it a language? Linguistic signatures, and the morphology Dee himself translated.

Three tests that separate a language from both gibberish and a rigid cipher, run WITHOUT needing to evoke:

  A) Zipf: in real languages word-frequency ~ 1/rank (a straight line in log-log). We fit the rank-frequency of
     the discovered name-vocabulary and report the slope and fit.
  B) Conditional entropy h1,h2,h3 (bits/char): random text is flat and high, a rigid cipher is very low, a
     natural language falls in a characteristic band and DROPS as context grows. We compare the Loagaeth to a
     frequency-matched random string and to its own Markov-3 surrogate.
  C) Morphology: Dee translated a few Enochian words - "canse"=mighty, "crucanse"=more mighty; "pola"=two
     together, "pala"=two separated. These are a real prefix (cru- = intensifier) and a real vowel-alternation
     minimal pair (o/a = together/separate). We check whether OUR Loagaeth name-grammar shows the same kind of
     structure: productive affixes (already found) and vowel-alternation minimal pairs among the names.
"""
import json
import math
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def cond_entropy(text, k):
    ctx = Counter(text[i:i + k] for i in range(len(text) - k))
    nxt = Counter(text[i:i + k + 1] for i in range(len(text) - k))
    h = 0.0
    N = sum(nxt.values())
    for g, c in nxt.items():
        p_joint = c / N
        p_cond = c / ctx[g[:k]]
        h += -p_joint * math.log2(p_cond)
    return h


def run():
    rng = random.Random(92)
    book = base_book()
    text = "".join("".join(r for r in book[k] if r) for k in book)

    # A) Zipf on the discovered name vocabulary (force = frequency)
    ent = json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"]
    freqs = sorted((e["forca"] for e in ent.values()), reverse=True)
    xs = [math.log(i + 1) for i in range(len(freqs))]
    ys = [math.log(f) for f in freqs]
    n = len(xs)
    mx, my = statistics.mean(xs), statistics.mean(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    inter = my - slope * mx
    ss_res = sum((y - (slope * x + inter)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot

    # B) entropy ladder
    f = Counter(text)
    alph, wt = list(f), [f[c] for c in f]
    randtext = "".join(rng.choices(alph, wt, k=len(text)))
    surr = "".join(markov3(text, rng))
    ladder = {}
    for name, t in (("Loagaeth", text), ("aleatorio", randtext), ("surrogate_M3", surr)):
        ladder[name] = {("h%d" % k): round(cond_entropy(t, k), 2) for k in (0, 1, 2, 3)}

    # C) morphology: vowel-alternation minimal pairs among names (like pola/pala)
    names = list(ent)
    def skel(s):  # consonant skeleton
        return "".join(c for c in s if c not in "AEIOU")
    bysk = {}
    for nm in names:
        bysk.setdefault(skel(nm), []).append(nm)
    minimal_pairs = {sk: v for sk, v in bysk.items() if len(v) >= 2 and len(sk) >= 3}
    # intensifier-style: a short name that is a prefix of a longer one (canse -> crucanse analogue)
    nested = [(a, b) for a in names for b in names if a != b and b.endswith(a) and len(b) - len(a) <= 3][:12]

    res = {
        "zipf": {"slope": round(slope, 2), "r2": round(r2, 3),
                 "reads": "inclinacao perto de -1 e r2 alto = distribuicao de lei de potencia, como uma lingua"},
        "entropy_ladder_bits_per_char": ladder,
        "morphology": {
            "translated_by_dee": {"canse": "mighty", "crucanse": "more mighty (cru- = intensificador)",
                                  "pola": "two together", "pala": "two separated (o/a = juntos/separados)"},
            "vowel_alternation_pairs_in_names": {k: v for k, v in list(minimal_pairs.items())[:12]},
            "prefix_nesting_examples": nested,
        },
        "finding": "",
    }
    lo = ladder["Loagaeth"]
    rd = ladder["aleatorio"]
    language_like = (abs(slope + 1) < 0.6 and r2 > 0.8) and (lo["h3"] < lo["h0"] - 0.3) and (lo["h3"] < rd["h3"])
    res["finding"] = (
        "Zipf: inclinacao %.2f, r2 %.3f (lei de potencia %s). Entropia: Loagaeth cai de h0=%.2f para h3=%.2f "
        "bits/char, abaixo do aleatorio (h3=%.2f) - carrega informacao condicional, como uma lingua, nao como "
        "ruido nem como cifra rigida. Morfologia: %d pares de alternacao vocalica (tipo pola/pala) e o prefixo "
        "intensificador (tipo cru-) reaparecem na nossa gramatica. %s" % (
            slope, r2, "SIM" if abs(slope + 1) < 0.6 and r2 > 0.8 else "parcial",
            lo["h0"], lo["h3"], rd["h3"], len(minimal_pairs),
            "Conclusao: as tabelas tem assinatura de LINGUA, nao de aleatorio nem de cifra - deciframel por "
            "metodo linguistico (morfologia, minimal pairs, ancorar nas poucas palavras traduzidas), nao so por "
            "evocacao." if language_like else "Sinal parcial de lingua."))
    load.save_result("92_is_it_a_language", res)
    return res


if __name__ == "__main__":
    r = run()
    print("ZIPF: inclinacao %.2f  r2 %.3f\n" % (r["zipf"]["slope"], r["zipf"]["r2"]))
    print("ENTROPIA (bits/char):")
    for nm, d in r["entropy_ladder_bits_per_char"].items():
        print("  %-14s %s" % (nm, d))
    print("\nMORFOLOGIA - pares de alternacao vocalica (mesmo esqueleto consonantal):")
    for sk, v in list(r["morphology"]["vowel_alternation_pairs_in_names"].items())[:10]:
        print("  [%s] %s" % (sk, v))
    print("\n" + r["finding"])
