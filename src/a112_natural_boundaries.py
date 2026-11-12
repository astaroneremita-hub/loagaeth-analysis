"""
112 (Bloco B) - Discover the grid's OWN word boundaries (branching entropy), then ask if the natural units are
real words above chance.

Instead of imposing a dictionary (a107/a110/a111 showed that is noise at every min length), we let the text cut
itself: at a true word boundary the number of possible next letters jumps (Harris 1955 / branching entropy). We
segment each row by the rise of right-branching entropy, using statistics learned from the book itself. Then we ask:
of the natural units, how many are dictionary words (Dee+dict+Leitch, len>=3) or attested name roots? And - the null
- does the REAL book's self-segmentation yield more real words than a Markov-3 surrogate segmented by its own stats?
If real >> surrogate, the book carries word structure at boundaries we were cutting wrong. If real ~ surrogate, the
grid has no more lexical structure than noise and the honest model is a name-field.
"""
import json
import math
import random
import unicodedata
from collections import defaultdict, Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def merged_vocab():
    v = set()
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for w in c["palavras"]:
            v.add(da(w["chave"]))
    for path in ("/viz/dict_enoq_lexicon.json", "/viz/leitch_extra_lexicon.json"):
        try:
            for k in json.load(open(load.ROOT + path, encoding="utf-8")):
                v.add(da(k))
        except Exception:
            pass
    return {w for w in v if len(w) >= 3}


def name_roots():
    try:
        ent = json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"]
        return {da(n) for n in ent if len(n) >= 3}
    except Exception:
        return set()


def right_entropy_table(rows, maxk=6):
    """For each substring (len<=maxk) return right-branching entropy over the corpus."""
    nxt = defaultdict(Counter)
    for r in rows:
        for i in range(len(r)):
            for k in range(1, maxk + 1):
                if i + k <= len(r):
                    sub = r[i:i + k]
                    nc = r[i + k] if i + k < len(r) else "$"
                    nxt[sub][nc] += 1
    H = {}
    for sub, c in nxt.items():
        tot = sum(c.values())
        H[sub] = -sum((v / tot) * math.log2(v / tot) for v in c.values())
    return H


def segment(row, H, thr=None, maxk=6):
    """Scale-invariant: cut after position i where right-branching entropy PEAKS (local max).
    A spike in how-many-letters-can-follow marks a word end (Harris 1955 / Tanaka-Ishii)."""
    n = len(row)
    if n <= 2:
        return [row]
    # h[i] = BE of the segment ending at position i (suffix up to maxk), measured over the corpus
    h = []
    for i in range(n):
        best = 0.0
        for k in range(1, maxk + 1):
            if i - k + 1 >= 0:
                best = max(best, H.get(row[i - k + 1:i + 1], 0.0))
        h.append(best)
    cuts = []
    for i in range(1, n - 1):
        if h[i] > h[i - 1] and h[i] >= h[i + 1] and h[i] > 0:
            cuts.append(i)
    segs, start = [], 0
    for c in cuts:
        if c + 1 - start >= 1:
            segs.append(row[start:c + 1])
            start = c + 1
    if start < n:
        segs.append(row[start:])
    return segs


def classify(segs, vocab, roots):
    words = names = 0
    for s in segs:
        if len(s) < 3:
            continue
        if s in vocab:
            words += 1
        elif s in roots or any(s.startswith(r) or s.endswith(r) for r in roots if len(r) >= 4):
            names += 1
    return words, names


def seg_stats(rows, H, thr, vocab, roots):
    allsegs = []
    for r in rows:
        allsegs += segment(r, H, thr)
    w, nm = classify(allsegs, vocab, roots)
    total = sum(1 for s in allsegs if len(s) >= 3)
    return {"segments_ge3": total, "words": w, "names": nm,
            "word_rate": round(w / total, 4) if total else 0,
            "name_rate": round(nm / total, 4) if total else 0,
            "mean_len": round(sum(len(s) for s in allsegs) / len(allsegs), 2) if allsegs else 0}


def run(thr=1.6):
    vocab = merged_vocab()
    roots = name_roots()
    book = base_book()
    rows = [r for k in book for r in book[k] if r]

    H = right_entropy_table(rows)
    real = seg_stats(rows, H, thr, vocab, roots)

    full = "".join(rows)
    surs = []
    for s in range(6):
        st = "".join(markov3(full, random.Random(1120 + s)))
        srows, p = [], 0
        for r in rows:
            srows.append(st[p:p + len(r)])
            p += len(r)
        Hs = right_entropy_table(srows)       # surrogate segmented by its OWN stats (fair)
        surs.append(seg_stats(srows, Hs, thr, vocab, roots))

    sw = sum(x["word_rate"] for x in surs) / len(surs)
    sw_max = max(x["word_rate"] for x in surs)
    sd = (sum((x["word_rate"] - sw) ** 2 for x in surs) / len(surs)) ** 0.5
    z = (real["word_rate"] - sw) / sd if sd else 0.0

    verdict = ("REAL: a auto-segmentação do livro produz %.1f%% de unidades que são palavras de verdade, vs %.1f%% "
               "no surrogate (z=%.1f) - a grade tem estrutura de palavra nas fronteiras naturais, estávamos cortando "
               "no lugar errado." % (real["word_rate"] * 100, sw * 100, z)) \
        if real["word_rate"] > sw_max and z >= 3 else \
        ("sem estrutura: as fronteiras naturais do livro dão %.1f%% de palavras reais vs %.1f%% do surrogate (z=%.1f) "
         "- a grade não tem mais estrutura lexical que o ruído; o campo de nomes (%.1f%% das unidades batem raiz de "
         "nome) é o que resta." % (real["word_rate"] * 100, sw * 100, z, real["name_rate"] * 100))

    res = {"threshold": thr, "vocab": len(vocab), "name_roots": len(roots),
           "real": real, "surrogate_word_rate_mean": round(sw, 4), "surrogate_word_rate_max": round(sw_max, 4),
           "z": round(z, 1), "finding": verdict}
    load.save_result("112_natural_boundaries", res)
    return res


if __name__ == "__main__":
    r = run()
    a = r["real"]
    print("máximo-local | mean_len %.2f | unidades>=3 %d | palavra %.1f%% (surr %.1f%%, max %.1f%%, z=%.1f) | nome %.1f%%" % (
        a["mean_len"], a["segments_ge3"], a["word_rate"] * 100,
        r["surrogate_word_rate_mean"] * 100, r["surrogate_word_rate_max"] * 100, r["z"], a["name_rate"] * 100))
    print("\n" + r["finding"])
