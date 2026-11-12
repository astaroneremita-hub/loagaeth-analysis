"""
118 - The CORE LEXICON of the Loagaeth: names ranked by how many of the 36 tables they appear in.

a117 showed a single table (2a) is not self-contained: its names are at chance WITHIN 2a but recur across the whole
book far above chance (NOCHA 35/36 tables, GETH 34/36; a same-length random string ~0). So the Loagaeth is ONE text
distributed over 49 sheets, and its 'words' are the names that recur sheet-to-sheet. This builds that core lexicon -
every attested name/root ranked by table-ubiquity, each checked against the random-string null - the real answer to
'what makes sense here': a corpus-wide onomastic vocabulary, Zipfian, with a ubiquitous core and a specialised tail.
"""
import json
import random

import load
from a22_robustness_and_depth import base_book


def square_grids(book):
    out = []
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            out.append((k, g))
    return out


def lines(g):
    R = 49
    out = []
    for r in range(R):
        out.append("".join(g[r][c] for c in range(R)))
    for c in range(R):
        out.append("".join(g[r][c] for r in range(R)))
    for s in range(R):
        out.append("".join(g[s + k][k] for k in range(R - s)))
        if s:
            out.append("".join(g[k][s + k] for k in range(R - s)))
    return out


def run():
    book = base_book()
    grids = square_grids(book)
    texts = [("\n".join(lines(g)), "\n".join(l[::-1] for l in lines(g))) for _, g in grids]
    T = len(grids)

    def tables_with(w):
        return sum(1 for t, rt in texts if w in t or w in rt)

    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))
    rng = random.Random(118)
    alpha = "ABCDEFGHILMNOPQRSTUVXZ"

    # null baseline per length
    nullL = {}
    for L in range(4, 12):
        cs = [tables_with("".join(rng.choice(alpha) for _ in range(L))) for _ in range(20)]
        nullL[L] = sum(cs) / len(cs)

    ranked = []
    for w in names:
        t = tables_with(w)
        base = nullL.get(len(w), 0.1)
        if t >= 2 and t > base * 3:
            ranked.append({"name": w, "tables": t, "share": round(t / T, 2),
                           "null": round(base, 2), "enrich": round(t / max(base, 0.05), 1)})
    ranked.sort(key=lambda x: -x["tables"])

    core = [r for r in ranked if r["tables"] >= T * 0.6]
    tail = [r for r in ranked if r["tables"] <= 3]
    res = {
        "tables": T, "lexicon_size": len(ranked),
        "core_ubiquitous": [(r["name"], r["tables"]) for r in core],
        "specialised_tail_count": len(tail),
        "top20": [(r["name"], r["tables"], r["enrich"]) for r in ranked[:20]],
        "finding": (
            "Léxico-núcleo do Loagaeth: %d nomes recorrem entre tabelas acima do acaso. %d são UBÍQUOS (em >=60%% das "
            "tabelas) - o núcleo da língua: %s. O resto é cauda especializada (%d nomes raros). Uma string aleatória "
            "do mesmo tamanho aparece em ~0 tabelas, então isto é vocabulário real distribuído pelo corpus, não "
            "acaso. 2a (ou qualquer folha) só faz sentido lida contra esse léxico das 49 tabelas." % (
                len(ranked), len(core), ", ".join(r["name"] for r in core[:8]), len(tail))),
    }
    load.save_result("118_core_lexicon", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("TOP 20 do léxico-núcleo (nome | tabelas/%d | enriquecimento vs acaso):" % r["tables"])
    for nm, t, e in r["top20"]:
        print("  %-12s %2d  %.0fx" % (nm, t, e))
