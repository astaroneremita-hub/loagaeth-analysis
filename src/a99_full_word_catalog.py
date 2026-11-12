"""
99 - The complete recurring-word catalogue: every repeated 2- to 8-gram in the whole book.

The earlier name set (195) was the generative-grammar families only. The practitioner is right that the book
holds thousands more recurring words (e.g. OLGEM, 18x). This walks the whole book and, for each length 2..8,
lists every substring that recurs at or above a sensible threshold, with its count and how many tables it spans.
It also builds a broad set (len 4-9, freq>=8) with element tags for the grid viewer, so tables.html lights up
everything, not only the catalogued families.
"""
import json
from collections import Counter

import load
from a22_robustness_and_depth import base_book
from a85_entity_attributes import load_letters

L = load_letters()
THR = {2: 400, 3: 150, 4: 50, 5: 14, 6: 8, 7: 5, 8: 4,
       9: 4, 10: 3, 11: 3, 12: 2, 13: 2, 14: 2}


def elem(nm):
    c = Counter((L.get(ch) or {}).get("element") for ch in nm)
    for k in ("?", None, "Espirito", "CaputDraconis", "CaudaDraconis"):
        c.pop(k, None)
    return c.most_common(1)[0][0] if c else "?"


def run():
    book = base_book()
    tabs = {}
    for k in book:
        tabs.setdefault(k[:-1], "")
        tabs[k[:-1]] += "".join(r for r in book[k] if r)
    full = "".join(tabs.values())

    catalog = {}
    grid_words = {}
    for n in range(2, 15):
        c = Counter(full[i:i + n] for i in range(len(full) - n + 1))
        th = THR[n]
        items = [(w, f) for w, f in c.items() if f >= th and len(set(w)) >= 2]
        items.sort(key=lambda t: -t[1])
        def tabn(w):
            return sum(1 for t in tabs.values() if w in t)
        catalog[n] = [{"w": w, "count": f, "tables": tabn(w), "element": elem(w)} for w, f in items[:400]]
        # grid set: len 4-9, freq>=8
        if 4 <= n <= 8:
            for w, f in c.items():
                if f >= 8 and len(set(w)) >= 2:
                    grid_words[w] = f

    res = {
        "lengths": {str(n): {"distinct_recurring": len(catalog[n]), "threshold": THR[n]} for n in catalog},
        "grid_word_count": len(grid_words),
        "catalog": catalog,
        "olgem_count": full.count("OLGEM"),
        "note": "Por comprimento 2-8: toda palavra (substring) que recorre >= limiar, com contagem e n de tabelas. "
                "O conjunto da grade (len 4-9, freq>=8) alimenta o tables.html completo.",
    }
    load.save_result("99_full_word_catalog", res)
    with open(load.ROOT + "/viz/word_catalog.json", "w", encoding="utf-8") as f:
        json.dump({"lengths": {str(n): catalog[n] for n in catalog}, "olgem": full.count("OLGEM")}, f, ensure_ascii=False)
    with open(load.ROOT + "/viz/grid_words.json", "w", encoding="utf-8") as f:
        json.dump(sorted(grid_words, key=len, reverse=True), f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print("OLGEM no livro:", r["olgem_count"], "| conjunto da grade:", r["grid_word_count"], "palavras\n")
    for n in range(2, 15):
        print("n=%d: %d recorrentes (freq>=%d). top:" % (n, r["lengths"][str(n)]["distinct_recurring"], r["lengths"][str(n)]["threshold"]),
              ", ".join("%s(%d)" % (x["w"], x["count"]) for x in r["catalog"][n][:8]))
