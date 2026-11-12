"""
115 - Do the tables have distinct ELEMENTAL identities in their name-field? (kabbalistic/spatial lens)

a114 found the name-field leans Fire/Air. Here: does each table carry its OWN elemental balance - some tables more
fiery, others more watery - or is the element spread evenly across the book? For each table we take its name-field
letters, get the Golden Dawn element profile, and measure the spread (between-table variance) of the Fire fraction.
Null: pool every name-letter of the whole book and redeal into tables of the same sizes; if the real between-table
spread beats that, the tables are elementally differentiated - a real spatial organization, not noise.
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


def names_set():
    return set(json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8")))


def name_letters(rows, names):
    out = []
    for r in rows:
        i, n = 0, len(r)
        while i < n:
            nm = 0
            for L in range(min(11, n - i), 3, -1):
                if r[i:i + L] in names:
                    nm = L
                    break
            if nm:
                out += list(r[i:i + nm]); i += nm
            else:
                i += 1
    return out


def fire_frac(letters, L):
    c = Counter(L.get(ch, {}).get("element") or "?" for ch in letters)
    tot = sum(c.values()) or 1
    return c.get("Fogo", 0) / tot


def run():
    L = load_letters()
    names = names_set()
    book = base_book()
    order = [k for k in book]

    per = {}
    for k in order:
        rows = [r for r in book[k] if r]
        nl = name_letters(rows, names)
        if len(nl) >= 30:
            per[k] = nl
    # real spread of Fire fraction across tables
    fires = {k: fire_frac(v, L) for k, v in per.items()}
    vals = list(fires.values())
    mean = sum(vals) / len(vals)
    real_var = sum((x - mean) ** 2 for x in vals) / len(vals)

    # null: pool all name-letters, redeal into same-size buckets
    pool = [ch for v in per.values() for ch in v]
    sizes = [len(v) for v in per.values()]
    rng = random.Random(115)
    null_var = []
    for _ in range(500):
        rng.shuffle(pool)
        p, vs = 0, []
        for s in sizes:
            vs.append(fire_frac(pool[p:p + s], L)); p += s
        m = sum(vs) / len(vs)
        null_var.append(sum((x - m) ** 2 for x in vs) / len(vs))
    nmean = sum(null_var) / len(null_var)
    ge = sum(1 for x in null_var if x >= real_var)
    pval = (ge + 1) / (len(null_var) + 1)

    top = sorted(fires.items(), key=lambda kv: -kv[1])
    res = {
        "tables": len(per), "fire_spread_real": round(real_var, 5), "fire_spread_null": round(nmean, 5),
        "p": round(pval, 4),
        "most_fiery": [(k, round(v * 100, 1)) for k, v in top[:6]],
        "least_fiery": [(k, round(v * 100, 1)) for k, v in top[-6:]],
        "finding": (
            "REAL: as tabelas têm identidade elemental própria no campo de nomes - a dispersão do Fogo entre tabelas "
            "(%.4f) bate o acaso (%.4f), p=%.3f. Umas tabelas são mais ígneas que outras, uma organização espacial "
            "do elemento." % (real_var, nmean, pval) if pval < 0.05 else
            "sem identidade: o Fogo se espalha igual entre as tabelas (real %.4f vs null %.4f, p=%.3f) - nenhuma "
            "organização elemental por tabela." % (real_var, nmean, pval)),
    }
    load.save_result("115_table_element_identity", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("mais ígneas (%% Fogo no campo de nomes):", r["most_fiery"])
    print("menos ígneas:", r["least_fiery"])
