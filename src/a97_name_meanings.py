"""
97 - Meaning on the grid: where translated Call words sit in the Loagaeth.

Our own name-stems (NOCHA, CHASTOR, GETH ...) carry NO external meaning - 0 of 195 match any Call word, so
their sense stays sealed (a sui-generis lexicon). But the Calls ARE a translated lexicon, and some Call words
appear inside the Loagaeth (a94). So we CAN place real, Dee-given meanings on the grid wherever a translated
Call word occurs. This builds that overlay: each translated Call word (len>=4) found in the Loagaeth, with its
English meaning, count, tables and sample positions. It is honest decipherment - meaning only where an anchor
reaches, never invented.
"""
import json
from collections import Counter, defaultdict

import load


def run():
    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    lex = defaultdict(Counter)
    for c in calls:
        for w in (c.get("palavras") or []):
            if isinstance(w, dict):
                en = "".join(ch for ch in str(w.get("enoquiano") or "").upper() if ch.isalpha())
                gl = str(w.get("ingles_sl3191") or "").strip()
                if en and len(en) >= 4 and gl and gl.lower() != "none":
                    lex[en][gl] += 1
    lexicon = {w: g.most_common(1)[0][0] for w, g in lex.items()}

    lv = load.leaves()
    grids, order = {}, []
    for leaf, rows in lv.items():
        g = ["".join(load.letters(r)) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            grids[leaf] = g
    order = sorted(grids, key=lambda k: (int(k[:-1]), k[-1]))

    def positions(word, cap=30):
        pos = []
        for leaf in order:
            g = grids[leaf]
            for r in range(49):
                i = g[r].find(word)
                while i >= 0:
                    pos.append({"leaf": leaf, "row": r, "col": i})
                    if len(pos) >= cap:
                        return pos
                    i = g[r].find(word, i + 1)
        return pos

    overlay = {}
    for w, gl in lexicon.items():
        pos = positions(w)
        if pos:
            overlay[w] = {"meaning": gl, "count": len(pos),
                          "tables": len({p["leaf"][:-1] for p in pos}), "pos": pos}

    # sort by length (longest = most meaningful) then count
    ordered = dict(sorted(overlay.items(), key=lambda kv: (-len(kv[0]), -kv[1]["count"])))
    res = {
        "call_words_translated": len(lexicon),
        "found_in_loagaeth": len(overlay),
        "overlay": ordered,
        "note": "Palavras das Chamadas (traduzidas por Dee) que aparecem na Loagaeth, com o sentido e a posicao. "
                "Os nomes proprios da Loagaeth (NOCHA etc.) nao tem ancora: 0 de 195 batem com o lexico das "
                "Chamadas, entao seu sentido fica selado.",
        "finding": (
            "Dos %d termos traduzidos das Chamadas, %d aparecem na Loagaeth e recebem sentido na grade (ex.: GOHO "
            "= saith, SONF = reigneth, IADNAH = ark of knowledge). Os nomes proprios da Loagaeth (NOCHA, CHASTOR, "
            "GETH...) NAO batem com o lexico das Chamadas (0/195): sao lexico proprio, sentido selado. A "
            "decifracao coloca sentido so onde ha ancora." % (len(lexicon), len(overlay))),
    }
    load.save_result("97_name_meanings", res)
    with open(load.ROOT + "/viz/meaning_overlay.json", "w", encoding="utf-8") as f:
        json.dump(ordered, f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("palavras das Chamadas com sentido, achadas na Loagaeth:")
    for w, d in list(r["overlay"].items())[:24]:
        print("  %-10s = %-24s %2d x em %2d tabelas" % (w, d["meaning"][:24], d["count"], d["tables"]))
