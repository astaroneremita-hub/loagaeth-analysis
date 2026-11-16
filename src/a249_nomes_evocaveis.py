# -*- coding: utf-8 -*-
"""
249 - Lista dos nomes evocáveis recorrentes do Loagaeth, ranqueada por frequência,
com elemento, gematria (GD hebraico) e a carta/signo de cada letra (pro tarô).
stdlib only.
"""
import json, os
from collections import Counter
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# letra -> (hebraico_valor, signo/elem, ELEMENTO, trunfo do tarô)
LET = {
 "A": (6,  "Touro",          "Terra",    "V O Hierofante"),
 "B": (5,  "Áries",          "Fogo",     "IV O Imperador"),
 "C": (300,"Fogo",           "Fogo",     "XX Julgamento"),
 "D": (300,"Espírito",       "Espírito", "XXI O Mundo"),
 "E": (10, "Virgem",         "Terra",    "IX O Eremita"),
 "F": (3,  "Cauda Draconis", "Nodo",     "— (cauda do dragão)"),
 "G": (9,  "Leão",           "Fogo",     "VIII A Força"),
 "H": (1,  "Ar",             "Ar",       "0 O Louco"),
 "I": (60, "Sagitário",      "Fogo",     "XIV A Temperança"),
 "L": (8,  "Câncer",         "Água",     "VII O Carro"),
 "M": (90, "Aquário",        "Ar",       "XVII A Estrela"),
 "N": (50, "Escorpião",      "Água",     "XIII A Morte"),
 "O": (30, "Libra",          "Ar",       "XI A Justiça"),
 "P": (8,  "Câncer",         "Água",     "VII O Carro"),
 "Q": (40, "Água",           "Água",     "XII O Enforcado"),
 "R": (100,"Peixes",         "Água",     "XVIII A Lua"),
 "S": (7,  "Gêmeos",         "Ar",       "VI Os Amantes"),
 "T": (3,  "Caput Draconis", "Nodo",     "— (cabeça do dragão)"),
 "U": (70, "Capricórnio",    "Terra",    "XV O Diabo"),
 "X": (400,"Terra",          "Terra",    "XXI O Mundo"),
 "Z": (9,  "Leão",           "Fogo",     "VIII A Força"),
}

# repertório de nomes evocáveis (famílias e formas atestadas)
CAND = [
 "NOCHA","ADNOCHA","DNOCHA","NACHO","NOCHASTOR","NOCHAP","ANOCHA","OXADNOCHA","ADNOCHAPH",
 "GETH","ALGETH","ALGETHA","GETHOG","GETHACLAX","ALGRADAX","GETHALCHADAX",
 "CHASTOR","ICHASTOR","ACHASTOR","ZUCHASTOR","CHASTORACHANZA","ANOCHASTOR",
 "ANZACH","HANZACH","ANZA","CHANZA","ACHANZA",
 "ACLAX","ACLAXT","OXAD","GETHACLAXTO",
 "DAXVAR","CHIDNO","CHADAX","ALCHADAX","DAXO","CHADEX",
 "NACHOR","OXA","ADOX","ANTANT","ANTANTOXA",
]


def gem(s): return sum(LET[c][0] for c in s if c in LET)
def elem(s):
    cnt = Counter(LET[c][2] for c in s if c in LET)
    return cnt.most_common(1)[0][0] if cnt else "—", dict(cnt)


def run():
    book = load.dense_stream()
    rows = []
    for nm in set(CAND):
        c = book.count(nm)
        if c >= 3:
            dom, prof = elem(nm)
            rows.append({"nome": nm, "freq": c, "gematria": gem(nm), "elemento": dom, "perfil": prof})
    rows.sort(key=lambda r: -r["freq"])
    with open(os.path.join(ROOT, "results", "249_nomes_evocaveis.json"), "w", encoding="utf-8") as f:
        json.dump({"nomes": rows,
                   "tabela_letras": {k: {"valor": v[0], "signo": v[1], "elemento": v[2], "trunfo": v[3]} for k, v in LET.items()}},
                  f, ensure_ascii=False, indent=1)
    return rows


if __name__ == "__main__":
    rows = run()
    print("NOMES EVOCÁVEIS QUE SE REPETEM (freq no Loagaeth, >=3)\n")
    print("%-16s %5s %8s  %-8s" % ("nome", "freq", "gematria", "elemento"))
    for r in rows:
        print("%-16s %5d %8d  %-8s" % (r["nome"], r["freq"], r["gematria"], r["elemento"]))
    print("\n--- carta/signo de cada letra (pro tarô) ---")
    for k, v in LET.items():
        print("  %s = %-14s %-8s %s" % (k, v[1], v[2], v[3]))
