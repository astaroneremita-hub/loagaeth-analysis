"""
117 - Linguist's dissection of table 2a: is it a morphological name-register? Root + affix paradigm.

a107-a116 killed every 'sentence' reading. A linguist faced with an undeciphered name-list stops looking for syntax
and looks for MORPHOLOGY: a small set of roots that take prefixes and suffixes by rule. We scan 2a for every
occurrence of the attested roots (NOCHA, GETH, CHASTOR, ACLAX, ANZACH, CHADAX, NACHO, PHANGE, GRADAX, ANTANTOX),
read the letters that cling to each root on its line as prefix/suffix, and build the realized paradigm. Then we test
the key claim: is 2a MORE root-saturated and more regularly affixed than a Markov-3 surrogate? If yes, 2a is a
generated name-register (its 'sense' is the grammar, not a message); if no, even the morphology is noise.
"""
import json
import random
import unicodedata
from collections import Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book

ROOTS = ["ANTANTOX", "CHASTOR", "GRADAX", "CHADAX", "ANZACH", "NOCHA", "NACHO", "ACLAX", "PHANGE", "GETH"]


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def lines(g):
    R = len(g)
    out = []
    for r in range(R):
        out.append([(r, c) for c in range(R)])
    for c in range(R):
        out.append([(r, c) for r in range(R)])
    for s in range(R):
        out.append([(s + k, k) for k in range(R - s)])
        if s:
            out.append([(k, s + k) for k in range(R - s)])
        out.append([(s + k, R - 1 - k) for k in range(R - s)])
        if s:
            out.append([(k, R - 1 - s - k) for k in range(R - s)])
    return out


def scan(g, maxaffix=3):
    """find root occurrences; capture up to maxaffix letters of prefix/suffix on the same line."""
    toks = []
    root_cov = 0
    for cells in lines(g):
        t = "".join(g[r][c] for r, c in cells)
        for root in ROOTS:
            start = 0
            while True:
                i = t.find(root, start)
                if i < 0:
                    break
                pre = t[max(0, i - maxaffix):i]
                suf = t[i + len(root):i + len(root) + maxaffix]
                toks.append((pre, root, suf))
                root_cov += len(root)
                start = i + 1
    return toks, root_cov


def profile(g):
    toks, cov = scan(g)
    pres = Counter(p[-2:] for p, r, s in toks if p)
    sufs = Counter(s[:2] for p, r, s in toks if s)
    roots = Counter(r for p, r, s in toks)
    total_letters = sum(len(row) for row in g)
    return {"root_tokens": len(toks), "root_cov": cov, "cov_frac": cov / total_letters,
            "roots": roots, "top_pre": pres.most_common(8), "top_suf": sufs.most_common(8)}


def run():
    book = base_book()
    g2a = [r for r in book["2a"] if r] if "2a" in book else None
    if not g2a or len(g2a) != 49:
        g2a = [["".join(c) for c in row] for row in []]  # fallback
    g2a = [list(r) for r in book["2a"]][:49]
    pr = profile([list(r) for r in book["2a"]])

    # null: surrogate 2a with same letter stats
    full2a = "".join("".join(r) for r in book["2a"])
    covs = []
    for s in range(20):
        st = "".join(markov3(full2a, random.Random(1170 + s)))
        R = 49
        sg = [list(st[i * R:(i + 1) * R]) for i in range(R)]
        _, c = scan(sg)
        covs.append(c / (R * R))
    mean = sum(covs) / len(covs)
    mx = max(covs)
    sd = (sum((x - mean) ** 2 for x in covs) / len(covs)) ** 0.5
    z = (pr["cov_frac"] - mean) / sd if sd else 0.0

    verdict = ("CONFIRMADO: 2a é saturada de material de raiz acima do acaso - %.1f%% das letras são raiz de nome vs "
               "%.1f%% no surrogate (máx %.1f%%), z=%.1f. 2a é um registro de nomes gerado por morfologia; o sentido é "
               "a GRAMÁTICA (raiz+afixo), não uma frase." % (
                   pr["cov_frac"] * 100, mean * 100, mx * 100, z)) \
        if pr["cov_frac"] > mx and z >= 3 else \
        ("material de raiz ~ acaso: %.1f%% real vs %.1f%% surrogate (máx %.1f%%), z=%.1f - os roots aparecem tanto "
         "quanto num campo denso qualquer; 2a não é mais saturada de nomes que o ruído." % (
             pr["cov_frac"] * 100, mean * 100, mx * 100, z))

    res = {"root_tokens": pr["root_tokens"], "root_cov_frac_pct": round(pr["cov_frac"] * 100, 1),
           "surrogate_pct": round(mean * 100, 1), "surrogate_max_pct": round(mx * 100, 1), "z": round(z, 1),
           "roots_in_2a": dict(pr["roots"]), "top_prefixes": pr["top_pre"], "top_suffixes": pr["top_suf"],
           "finding": verdict}
    load.save_result("117_morphology_2a", res)
    return res


if __name__ == "__main__":
    r = run()
    print("2a: %d ocorrências de raiz, cobrem %.1f%% das letras (surrogate %.1f%%, máx %.1f%%, z=%.1f)" % (
        r["root_tokens"], r["root_cov_frac_pct"], r["surrogate_pct"], r["surrogate_max_pct"], r["z"]))
    print("raízes em 2a:", r["roots_in_2a"])
    print("prefixos mais comuns:", r["top_prefixes"])
    print("sufixos mais comuns:", r["top_suffixes"])
    print("\n" + r["finding"])
