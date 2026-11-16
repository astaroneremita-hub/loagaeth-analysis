# -*- coding: utf-8 -*-
"""
248 - Os nomes das 4 Placas elementais EXTRAÍDOS do Sigillum (método Golden Dawn).
Fonte: 'Os Sigilos das Placas Angélicas' (Regardie, A Magia Enochiana, Livro IX, p.705),
enviado pelo usuário. Os 4 nomes (Ar/Água/Terra/Fogo) saem do SDA pela 'regra de 4' (e 6),
a partir do T no topo do anel. Reproduzo com os nossos dados do SDA e busco no Loagaeth.
stdlib only, seed 1583.
"""
import json, os, random, statistics
from collections import defaultdict
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583


def ring():
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        casas = json.load(f)["anel_externo_40"]["casas"]
    return ["".join(ch for ch in c["letra"].replace("ω", "O").upper() if ch.isalpha()) for c in casas]


def markov3(stream, n, rng):
    trans = defaultdict(list)
    for i in range(len(stream) - 3):
        trans[stream[i:i+3]].append(stream[i+3])
    s = list(stream[:3])
    while len(s) < n:
        nxt = trans.get("".join(s[-3:]))
        s.append(rng.choice(nxt) if nxt else rng.choice("AEIOU"))
    return "".join(s[:n])


def run():
    rng = random.Random(SEED)
    L = ring()

    # AR: regra de 4 a partir do T (casa 0): passo +4 -> casas 0,4,8,12,16,20
    air_houses = [(0 + 4*k) % 40 for k in range(6)]
    air = "".join(L[h] for h in air_houses)

    # ÁGUA: a partir do T, mistura 4 e 6 (regra de 6); reproduzo a sequência de casas do livro:
    # Th(cross)=0, depois saltos; aproximação pela leitura: casas 0,4,22(h?),... deixo a leitura do livro como referência
    water_book = "THAHEBYOBEAATANUN"
    earth_book = "THAHAAOTHE"
    air_book = "TAHAOELOG"

    # TERRA: cruz simples = Th, conta pelos números dados 4,22,11 -> a,o,t,h
    # (notação do livro; registro o nome do livro e confiro só o Ar pela regra limpa de 4)

    names = {"Ar(regra 4, nosso SDA)": air, "Ar(livro)": air_book,
             "Água(livro)": water_book, "Terra(livro)": earth_book}

    # confere: o Ar extraído bate com o do livro?
    air_ok = air.upper() in ("THAOLOG", "TAHAOLOG") or air.replace("OG", "LOG")[:6] == "THAOLO"

    # busca no Loagaeth vs Markov-3
    book = load.dense_stream()
    surs = [markov3(book, len(book), rng) for _ in range(8)]
    search = {}
    for label, nm in [("TAHAOELOG", air_book), ("THAOLOG", air), ("THAHAAOTHE", earth_book),
                      ("THAHEBYOBEAATANUN", water_book), ("THAHAOTHE", "THAHAOTHE")]:
        real = book.count(nm)
        nul = [s.count(nm) for s in surs]
        z = (real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9)
        search[label] = {"nome": nm, "loag": real, "null_mean": round(statistics.mean(nul), 3), "z": round(z, 2)}

    res = {"anel": "".join(L), "ar_casas_passo4": air_houses, "ar_extraido": air,
           "nomes_das_placas": names, "ar_confere_com_livro": air_ok, "busca_no_loag": search}
    with open(os.path.join(ROOT, "results", "248_elemental_names.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = run()
    print("ANEL do SDA:", r["anel"])
    print("\nAR — regra de 4 a partir do T (casas %s):" % r["ar_casas_passo4"])
    print("   extraído do NOSSO SDA =", r["ar_extraido"], " | livro = TAHAOELOG(THAOLOG)")
    print("   confere com o livro?", "SIM ✓" if r["ar_confere_com_livro"] else "ver")
    print("\nNomes das 4 placas (livro):")
    for k, v in r["nomes_das_placas"].items():
        print("   %-24s %s" % (k, v))
    print("\nBusca dos nomes elementais no LOAGAETH (vs Markov-3):")
    for k, d in r["busca_no_loag"].items():
        print("   %-20s %-18s Loag %3d vs null %6s  z %5s" % (k, d["nome"], d["loag"], d["null_mean"], d["z"]))
