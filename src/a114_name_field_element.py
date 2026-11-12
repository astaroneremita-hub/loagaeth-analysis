"""
114 (Bloco D) - Kabbalistic lens: does the NAME-field carry a different elemental signature than the CALL-WORD field?

Blocos A-C showed the squares are a name-field, not prose. Here we ask, through the Golden Dawn letter->element
correspondence, whether the letters that make up the attested NAMES draw on a different elemental balance than the
letters that make up the glossable Call words - i.e. whether 'the language of names' is its own layer with its own
element. We tile each row into three fields (dictionary word > attested name > unstructured), collect the letters of
each, and compare the element distributions. Null: randomly relabel the same letters into fields of the same sizes;
if the real name-vs-word element divergence beats that, the name layer has a distinct signature.
"""
import json
import random
import unicodedata
from collections import Counter

import load
from a85_entity_attributes import load_letters
from a22_robustness_and_depth import base_book


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def dee_vocab():
    v = set()
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for w in c["palavras"]:
            k = da(w["chave"])
            if len(k) >= 2:
                v.add(k)
    return v


def names_set():
    try:
        return set(json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8")))
    except Exception:
        return set()


def tile_fields(rows, vocab, names):
    """return dict field->list of letters (word / name / noise)."""
    fields = {"word": [], "name": [], "noise": []}
    for r in rows:
        i, n = 0, len(r)
        while i < n:
            hit = 0
            for L in range(min(9, n - i), 1, -1):
                if r[i:i + L] in vocab:
                    hit = L
                    break
            if hit:
                fields["word"] += list(r[i:i + hit]); i += hit; continue
            nm = 0
            for L in range(min(11, n - i), 3, -1):
                if r[i:i + L] in names:
                    nm = L
                    break
            if nm:
                fields["name"] += list(r[i:i + nm]); i += nm; continue
            fields["noise"].append(r[i]); i += 1
    return fields


def elem_dist(letters, L):
    c = Counter()
    for ch in letters:
        e = L.get(ch, {}).get("element") or "?"
        c[e] += 1
    tot = sum(c.values()) or 1
    return {k: c[k] / tot for k in ("Fogo", "Terra", "Ar", "Agua", "?")}


def tv(a, b):
    return 0.5 * sum(abs(a.get(k, 0) - b.get(k, 0)) for k in set(a) | set(b))


def run():
    L = load_letters()
    vocab = dee_vocab()
    names = names_set()
    book = base_book()
    rows = [r for k in book for r in book[k] if r]

    f = tile_fields(rows, vocab, names)
    dw = elem_dist(f["word"], L)
    dn = elem_dist(f["name"], L)
    dz = elem_dist(f["noise"], L)
    real_tv = tv(dn, dw)

    # null: pool word+name letters, random relabel into same-size fields
    pool = f["word"] + f["name"]
    nw = len(f["word"])
    rng = random.Random(114)
    null_tv = []
    for _ in range(500):
        rng.shuffle(pool)
        a = elem_dist(pool[:nw], L)
        b = elem_dist(pool[nw:], L)
        null_tv.append(tv(a, b))
    mean = sum(null_tv) / len(null_tv)
    ge = sum(1 for x in null_tv if x >= real_tv)
    p = (ge + 1) / (len(null_tv) + 1)

    verdict = ("REAL: o campo de NOMES tem assinatura elemental distinta do campo de palavras (divergência TV=%.3f vs "
               "%.3f no acaso, p=%.3f) - a língua dos nomes é uma camada com seu próprio elemento." % (real_tv, mean, p)) \
        if p < 0.05 else \
        ("mesma assinatura: nomes e palavras repartem os elementos igual (TV=%.3f vs %.3f no acaso, p=%.3f) - o campo "
         "de nomes não tem elemento próprio distinto do vocabulário glosável." % (real_tv, mean, p))

    def pct(d):
        return {k: round(v * 100, 1) for k, v in d.items()}
    res = {"letters_word": len(f["word"]), "letters_name": len(f["name"]), "letters_noise": len(f["noise"]),
           "elem_word": pct(dw), "elem_name": pct(dn), "elem_noise": pct(dz),
           "tv_name_vs_word": round(real_tv, 3), "null_tv_mean": round(mean, 3), "p": round(p, 4),
           "finding": verdict}
    load.save_result("114_name_field_element", res)
    return res


if __name__ == "__main__":
    r = run()
    tot = r["letters_word"] + r["letters_name"] + r["letters_noise"]
    print("letras: palavra %d (%.0f%%) | nome %d (%.0f%%) | ruído %d (%.0f%%)" % (
        r["letters_word"], 100 * r["letters_word"] / tot, r["letters_name"], 100 * r["letters_name"] / tot,
        r["letters_noise"], 100 * r["letters_noise"] / tot))
    print("elemento (Fogo/Terra/Ar/Agua/?):")
    print("  palavra:", r["elem_word"])
    print("  nome:   ", r["elem_name"])
    print("  ruído:  ", r["elem_noise"])
    print("\n" + r["finding"])
