"""
a144 - MISSION: link the Loagaeth to the Calls, Heptarchy and Watchtowers. Do their names live IN the Loagaeth?

The master-key hypothesis: the Loagaeth is the source, so the names of the other systems should appear inside its
tables. We take the attested names of each system (Governors+Watchtowers, Heptarchy, Call vocabulary), search them in
the Loagaeth 49x49 grids (rows, columns, both diagonals, forward+reversed), and compare to a null of random strings
of the same lengths. A system whose names appear in the Loagaeth far above chance is 'contained' in it. We report per
system and per name, honestly: in a dense grid short strings appear by chance, so length and margin matter.
"""
import json
import random
import re
import unicodedata

import load
from a22_robustness_and_depth import base_book


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").upper()


def harvest(o, acc, minlen=4):
    if isinstance(o, str):
        w = da(o)
        if re.fullmatch(r"[A-Z]{%d,14}" % minlen, w):
            acc.add(w)
    elif isinstance(o, dict):
        for v in o.values():
            harvest(v, acc, minlen)
    elif isinstance(o, list):
        for v in o:
            harvest(v, acc, minlen)


def grids():
    book = base_book()
    out = []
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            out.append(g)
    return out


def lines(g):
    R = 49
    o = [g[r] for r in range(R)]
    o += ["".join(g[r][c] for r in range(R)) for c in range(R)]
    for s in range(R):
        o.append("".join(g[s + k][k] for k in range(R - s)))
        if s:
            o.append("".join(g[k][s + k] for k in range(R - s)))
    return o


def run():
    gs = grids()
    texts = ["\n".join(lines(g)) for g in gs]
    rtexts = ["\n".join(l[::-1] for l in lines(g)) for g in gs]
    big = "\n".join(texts) + "\n" + "\n".join(rtexts)

    def present(w):
        return w in big

    gov = set(); harvest(json.load(open(load.ROOT + "/engine/data/governadores.json", encoding="utf-8")), gov)
    hep = set(); harvest(json.load(open(load.ROOT + "/engine/data/heptarquia.json", encoding="utf-8")), hep)
    cham = set()
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for wd in c["palavras"]:
            k = da(wd["chave"])
            if len(k) >= 4:
                cham.add(k)

    rng = random.Random(144)
    alpha = "ABCDEFGHILMNOPQRSTUVXZ"

    def nullrate(words):
        lens = [len(w) for w in words]
        hits = 0
        for L in lens:
            if "".join(rng.choice(alpha) for _ in range(L)) in big:
                hits += 1
        return hits / len(lens) if lens else 0

    out = {}
    for name, ws in (("Governadores+Torres", gov), ("Heptarquia", hep), ("Chamadas (>=4)", cham)):
        ws = sorted(ws)
        found = [w for w in ws if present(w)]
        nr = sum(nullrate(ws) for _ in range(5)) / 5
        out[name] = {"total": len(ws), "found_in_loagaeth": len(found),
                     "found_pct": round(100 * len(found) / len(ws), 1) if ws else 0,
                     "null_pct": round(100 * nr, 1),
                     "sample_found": [w for w in found if len(w) >= 6][:12]}

    res = {"systems": out,
           "finding": (
               "Nomes dos sistemas enoquianos procurados DENTRO das tabelas do Loagaeth (reta/coluna/diagonal, "
               "fwd+rev) vs null de strings aleatórias do mesmo tamanho: %s. %s" % (
                   "; ".join("%s %d/%d (%.0f%%) vs acaso %.0f%%" % (
                       k, v["found_in_loagaeth"], v["total"], v["found_pct"], v["null_pct"]) for k, v in out.items()),
                   ("ligação: algum sistema aparece acima do acaso." if any(
                       v["found_pct"] > v["null_pct"] * 1.5 for v in out.values()) else
                    "nenhum sistema aparece no Loagaeth acima do acaso — os nomes NÃO estão contidos nas tabelas."))),
           }
    load.save_result("144_system_links", res)
    return res


if __name__ == "__main__":
    r = run()
    print("sistema | achados no Loagaeth | % | null %")
    for k, v in r["systems"].items():
        print("  %-22s %d/%d (%.0f%%) vs acaso %.0f%%" % (
            k, v["found_in_loagaeth"], v["total"], v["found_pct"], v["null_pct"]))
        if v["sample_found"]:
            print("     ex (>=6):", ", ".join(v["sample_found"]))
    print("\n" + r["finding"])
