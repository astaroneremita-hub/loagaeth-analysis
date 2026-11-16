# -*- coding: utf-8 -*-
"""
241 - A regra do anel do Sigillum (como se tira GALETHOG) aplicada a todas as partidas,
       e os nomes gerados buscados no Loagaeth.

Regra declarada (Michael, Sloane 3188): começar numa casa; número ACIMA = andar esse
número de casas para a DIREITA (horário); número ABAIXO = para a ESQUERDA; contar a
partir da casa atual exclusive; parar ao cair numa casa SEM número (que fecha o nome).
Dois 'a' seguidos no meio: o primeiro não entra.

Passo 1: reproduzir os 7 nomes de Dee (validação).
Passo 2: rodar de todas as 40 partidas -> conjunto de nomes gerados pelo selo.
Passo 3: buscar cada nome no Loagaeth (tabelas 2-48) vs surrogate Markov-3 -> z por nome.
stdlib only, seed 1583.
"""
import json, os, random, math, statistics
from collections import defaultdict
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583


def ring():
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        casas = json.load(f)["anel_externo_40"]["casas"]
    L, NUM, ABOVE = [], [], []
    for c in casas:
        ltr = c["letra"].replace("ω", "O")
        L.append("".join(ch for ch in ltr.upper() if ch.isalpha()))
        NUM.append(c["numero"])
        ABOVE.append(c["posicao_numero"] == "acima")
    return L, NUM, ABOVE


def gen_name(start, L, NUM, ABOVE, maxstep=45):
    pos = start
    letters = [L[pos]]
    steps = 0
    while NUM[pos] is not None and steps < maxstep:
        step = NUM[pos] if ABOVE[pos] else -NUM[pos]
        pos = (pos + step) % 40
        letters.append(L[pos])
        steps += 1
        if NUM[pos] is None:
            break
    name = "".join(letters)
    # dois 'a' seguidos no meio: remove o primeiro (não final)
    out = []
    i = 0
    while i < len(name):
        if (name[i] == "A" and 0 < i and i + 1 < len(name) and name[i + 1] == "A"
                and i + 2 < len(name)):  # 'meio' = letra antes E depois do par AA
            i += 1  # pula o primeiro A
            continue
        out.append(name[i]); i += 1
    return "".join(out)


def markov3_surrogate(stream, n, rng):
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
    L, NUM, ABOVE = ring()

    known = {"Galas": 1, "Gethog": 17, "Thaoth": 0, "Horlwn": 19, "Innon": 27, "Aaoth": 31, "Galethog": 33}
    validation = {}
    for nm, st in known.items():
        validation[nm] = {"start": st, "generated": gen_name(st, L, NUM, ABOVE),
                          "match": gen_name(st, L, NUM, ABOVE).upper() == load.letters(nm.replace("w", "O")).upper()}

    # todas as 40 partidas
    generated = {}
    for st in range(40):
        g = gen_name(st, L, NUM, ABOVE)
        if len(g) >= 3:
            generated.setdefault(g, []).append(st)
    names = sorted(generated, key=lambda x: (-len(x), x))

    # busca no Loagaeth vs Markov-3
    book = load.dense_stream()
    NSUR = 8
    surs = [markov3_surrogate(book, len(book), rng) for _ in range(NSUR)]
    rows = []
    for nm in names:
        real = book.count(nm)
        nul = [s.count(nm) for s in surs]
        z = (real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9)
        rows.append({"name": nm, "len": len(nm), "starts": generated[nm],
                     "loag_count": real, "null_mean": round(statistics.mean(nul), 2), "z": round(z, 2)})
    rows.sort(key=lambda r: -r["z"])

    res = {"validation_7_names": validation,
           "n_generated_distinct": len(names),
           "generated_names": names,
           "loag_search": rows}
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "241_sigillum_ring.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = run()
    print("=== validação (regra reproduz os 7 nomes de Dee?) ===")
    for nm, v in r["validation_7_names"].items():
        print("  %-9s partida %2d -> %-10s %s" % (nm, v["start"], v["generated"], "OK" if v["match"] else "DIVERGE"))
    print("\n=== %d nomes distintos gerados pelas 40 partidas ===" % r["n_generated_distinct"])
    print("  ", r["generated_names"])
    print("\n=== busca no Loagaeth (vs Markov-3), top por z ===")
    for row in r["loag_search"]:
        flag = " <== bate o acaso" if row["z"] >= 3 else ""
        print("  %-12s len %d | Loag %4d vs null %6s | z %6s%s" %
              (row["name"], row["len"], row["loag_count"], row["null_mean"], row["z"], flag))
