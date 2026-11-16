# -*- coding: utf-8 -*-
"""
243 - Os nomes do Loagaeth estão nas POSIÇÕES do Sigillum, na ordem? (ideia do usuário)

Não como substring contíguo (já testado), mas como SUBSEQUÊNCIA: as letras do nome
aparecem em ordem nas posições do selo (anel circular + tabelas), pulando outras.
Ex.: GETH = G…E…T…H nas casas certas. Problema: subsequência num monte de letras casa
quase tudo (Babel). Então os testes honestos são comparativos:
  (A) nomes REAIS do Loag são subsequência do SDA mais que nomes ALEATÓRIOS de mesmo
      tamanho e distribuição de letras do Loag?
  (B) a ORDEM REAL das letras casa melhor que a ORDEM EMBARALHADA do mesmo nome?
Anel tratado como círculo (todas as 40 rotações). stdlib only, seed 1583.
"""
import json, os, random, statistics
from collections import Counter
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583

TOP = ["NOCHA", "GETH", "CHASTOR", "ANZACH", "ALGETH", "ACLAX", "NACHO", "ADNOCHA",
       "DAXVAR", "HANZACH", "ACLAXT", "GETHACLAX", "CHIDNO", "DNOCHA"]


def up(s):
    return "".join(ch for ch in s.upper() if ch.isalpha())


def sda_streams():
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        sda = json.load(f)
    ring = "".join(up(c["letra"].replace("ω", "O")) for c in sda["anel_externo_40"]["casas"])
    # tabelas 7x7 (central + cestos) em todas as direcoes
    cel = sda["tabela_7x7"]["celulas"]
    gc = [[up(c["letra"] or "") or "." for c in row] for row in cel]
    gb = [[up(x) if x != "+" else "." for x in r["letras"]] for r in sda["tabela_dos_cestos_49"]["linhas"]]
    def grid_streams(g):
        n, m = len(g), len(g[0]); out = []
        out += ["".join(g[r][c] for c in range(m)) for r in range(n)]
        out += ["".join(g[r][c] for r in range(n)) for c in range(m)]
        for s in range(-(n - 1), m):
            out.append("".join(g[r][r - s] for r in range(n) if 0 <= r - s < m))
        for s in range(0, n + m - 1):
            out.append("".join(g[r][s - r] for r in range(n) if 0 <= s - r < m))
        return [x for x in out if x]
    tables = grid_streams(gc) + grid_streams(gb)
    return ring, tables


def is_subseq(name, stream):
    it = iter(stream)
    return all(ch in it for ch in name)


def in_sda(name, ring, tables):
    # anel como circulo: qualquer rotacao; + tabelas; + concatenacao
    rr = ring + ring  # permite dar a volta
    if is_subseq(name, rr):
        return True
    joined = "".join(tables)
    if is_subseq(name, joined):
        return True
    for t in tables:
        if is_subseq(name, t):
            return True
    return False


def run():
    rng = random.Random(SEED)
    ring, tables = sda_streams()

    # distribuicao de letras do Loag p/ nomes aleatorios
    book = load.dense_stream()
    letters = [c for c in book]

    rows = []
    realhits = 0
    for nm in TOP:
        nm = up(nm)
        hit = in_sda(nm, ring, tables)
        realhits += hit
        # null A: nomes aleatorios de mesmo tamanho, distribuicao Loag
        na = sum(in_sda("".join(rng.choice(letters) for _ in range(len(nm))), ring, tables) for _ in range(200)) / 200
        # null B: ordem embaralhada do mesmo nome
        shuffhit = 0
        for _ in range(200):
            l = list(nm); rng.shuffle(l)
            shuffhit += in_sda("".join(l), ring, tables)
        nb = shuffhit / 200
        rows.append({"name": nm, "len": len(nm), "in_sda": bool(hit),
                     "null_random_rate": round(na, 3), "null_shuffled_rate": round(nb, 3)})

    # agregados
    real_rate = realhits / len(TOP)
    rnd_rate = statistics.mean(r["null_random_rate"] for r in rows)
    shuf_rate = statistics.mean(r["null_shuffled_rate"] for r in rows)

    # GETH concreto: posicoes no anel
    geth_pos = None
    seq = "GETH"; pos = []
    i = 0
    rr = ring + ring
    cur = 0
    for ch in seq:
        j = rr.find(ch, cur)
        pos.append(j % 40 if j >= 0 else None); cur = j + 1
    geth_pos = pos

    res = {
        "top_names": rows,
        "aggregate": {"real_in_sda_rate": round(real_rate, 3),
                      "null_random_rate_mean": round(rnd_rate, 3),
                      "null_shuffled_rate_mean": round(shuf_rate, 3)},
        "GETH_ring_positions": geth_pos,
        "ring": ring,
    }
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "243_sigillum_subseq.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = run()
    print("anel do SDA:", r["ring"], "(%d letras)" % len(r["ring"]))
    print("\nnome        len  é subseq do SDA?  | nulo aleatório  nulo embaralhado")
    for row in r["top_names"]:
        print("  %-10s %3d   %-5s            | %6.3f          %6.3f"
              % (row["name"], row["len"], "SIM" if row["in_sda"] else "não", row["null_random_rate"], row["null_shuffled_rate"]))
    a = r["aggregate"]
    print("\nAGREGADO: reais no SDA %.0f%% | aleatórios %.0f%% | ordem embaralhada %.0f%%"
          % (a["real_in_sda_rate"] * 100, a["null_random_rate_mean"] * 100, a["null_shuffled_rate_mean"] * 100))
    print("GETH nas casas do anel (G,E,T,H):", r["GETH_ring_positions"])
