# -*- coding: utf-8 -*-
"""
242 - Nomes das DIAGONAIS da tabela 7x7 do Sigillum buscados no Loagaeth.

A tabela 7x7 central do SDA gera, por leitura diagonal/anti-diagonal (como o Loag lê
25b-28b): os 7 anjos, as 4 famílias (Filiae Bonitatis, Filii Lucis, Filiae Filiarum,
Filii Filiorum) e, pelas linhas, os 7 nomes de Deus. Último método do selo ainda não
cruzado com o Livro. Busca cada nome (>=3 letras) no Loagaeth vs surrogate Markov-3.
stdlib only, seed 1583.
"""
import json, os, random, statistics
from collections import defaultdict
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583


def up(s):
    return "".join(ch for ch in s.upper() if ch.isalpha())


def sda_table_names():
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        sda = json.load(f)
    names = {}
    for a in sda["anjos_7"]["anjos"]:
        names.setdefault("anjo", []).append(up(a["leitura_da_tabela"]))
    for key, fam in sda["familias_4"].items():
        for nm in fam["nomes"]:
            names.setdefault(key, []).append(up(nm["nome"]))
    for r in sda["nomes_de_deus_7"]["nomes"]:
        names.setdefault("nome_de_deus", []).append(up("".join(ch for ch in r["com_anotacoes"] if ch.isalpha())))
    return names


def markov3(stream, n, rng):
    trans = defaultdict(list)
    for i in range(len(stream) - 3):
        trans[stream[i:i + 3]].append(stream[i + 3])
    s = list(stream[:3])
    while len(s) < n:
        nxt = trans.get("".join(s[-3:]))
        s.append(rng.choice(nxt) if nxt else rng.choice("AEIOU"))
    return "".join(s[:n])


def run():
    rng = random.Random(SEED)
    groups = sda_table_names()
    book = load.dense_stream()
    surs = [markov3(book, len(book), rng) for _ in range(8)]

    rows = []
    seen = set()
    for grp, lst in groups.items():
        for nm in lst:
            if len(nm) < 3 or nm in seen:
                continue
            seen.add(nm)
            real = book.count(nm)
            nul = [s.count(nm) for s in surs]
            z = (real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9)
            rows.append({"group": grp, "name": nm, "len": len(nm), "loag": real,
                         "null_mean": round(statistics.mean(nul), 2), "z": round(z, 2)})
    rows.sort(key=lambda r: -r["z"])
    hits = [r for r in rows if r["z"] >= 3]

    res = {"n_names": len(rows), "names_beating_null(z>=3)": hits, "all": rows}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "242_sigillum_table.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = run()
    print("nomes testados (>=3 letras):", r["n_names"])
    print("bateram o acaso (z>=3):", r["names_beating_null(z>=3)"] or "NENHUM")
    print("\ntop por z:")
    for row in r["all"][:20]:
        print("  %-10s %-16s len %d | Loag %4d vs null %6s | z %6s" %
              (row["group"], row["name"], row["len"], row["loag"], row["null_mean"], row["z"]))
