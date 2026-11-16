# -*- coding: utf-8 -*-
"""
245 - Rodada 2: AEMETH (a verdade, o próprio nome do selo) e os ponteiros numéricos.

Hipóteses:
  (A) AEMETH/EMETH/AMETH escondido no selo (todos os caminhos, exato/≤1 edit/subsequência) vs null.
  (B) os números que Uriel disse 'servir a outro propósito' (as anotações 21/8=El, 30, 26 do 7×7)
      apontam para casas do anel — ler essas letras forma uma mensagem?
  (C) ler o anel começando em cada casa SEM número (os 'fechadores': 5,11,15,20,30,36).
stdlib only, seed 1583.
"""
import json, os, random, statistics
from collections import Counter
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583


def up(s): return "".join(ch for ch in (s or "").upper() if ch.isalpha())


def is_subseq(name, stream):
    it = iter(stream)
    return all(c in it for c in name)


def run():
    rng = random.Random(SEED)
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        sda = json.load(f)
    L = [up(c["letra"].replace("ω", "O")) for c in sda["anel_externo_40"]["casas"]]
    NUM = [c["numero"] for c in sda["anel_externo_40"]["casas"]]
    ABV = [c["posicao_numero"] == "acima" for c in sda["anel_externo_40"]["casas"]]
    ring = "".join(L)

    # todos os streams (anel + tabelas + nomes)
    cel = sda["tabela_7x7"]["celulas"]
    gc = [[up(c["letra"] or "") or "." for c in row] for row in cel]
    gb = [[up(x) if x != "+" else "." for x in r["letras"]] for r in sda["tabela_dos_cestos_49"]["linhas"]]
    def gstream(g):
        n, m = len(g), len(g[0]); o = []
        o += ["".join(g[r][c] for c in range(m)) for r in range(n)]
        o += ["".join(g[r][c] for r in range(n)) for c in range(m)]
        for s in range(-(n-1), m): o.append("".join(g[r][r-s] for r in range(n) if 0 <= r-s < m))
        for s in range(0, n+m-1): o.append("".join(g[r][s-r] for r in range(n) if 0 <= s-r < m))
        return [x for x in o if x]
    streams = [ring, ring[::-1], ring*2] + gstream(gc) + gstream(gb)

    # (A) AEMETH
    targets = ["AEMETH", "EMETH", "AMETH", "ACLAXT"]  # ACLAXT = controle (nome Loag não esperado)
    A = {}
    for t in targets:
        exact = sum(s.count(t) for s in streams)
        subseq_ring = is_subseq(t, ring*2)
        A[t] = {"exato_em_streams": exact, "subsequencia_no_anel": subseq_ring}
    # null p/ AEMETH exato: embaralha cada stream, reconta
    def null_exact(t):
        tot = 0
        for s in streams:
            l = list(s); rng.shuffle(l); tot += "".join(l).count(t)
        return tot
    aemeth_null = [null_exact("AEMETH") for _ in range(200)]

    # (B) ponteiros: casas do anel cujo número é 30 ou 26 (Uriel: 'outro propósito')
    pointers = {}
    for target_num in (21, 8, 30, 26):
        hits = [(i, L[i]) for i in range(40) if NUM[i] == target_num]
        pointers[str(target_num)] = hits
    # mensagem: letras das casas apontadas, em ordem de casa
    pointed_letters = "".join(L[i] for i in range(40) if NUM[i] in (30, 26, 21, 8))

    # (C) anel a partir de cada casa sem número
    closers = [i for i in range(40) if NUM[i] is None]
    from_closers = {str(i): (ring*2)[sum(len(L[j]) for j in range(i)): sum(len(L[j]) for j in range(i)) + 20] for i in closers}

    res = {
        "A_AEMETH": A,
        "A_AEMETH_null": {"real_exato": A["AEMETH"]["exato_em_streams"],
                          "null_mean": round(statistics.mean(aemeth_null), 3),
                          "null_max": max(aemeth_null)},
        "B_ponteiros_outro_proposito": {"casas_por_numero": pointers, "letras_apontadas": pointed_letters},
        "C_anel_dos_fechadores": from_closers,
        "ring": ring,
    }
    with open(os.path.join(ROOT, "results", "245_sigillum_aemeth.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = run()
    print("ANEL:", r["ring"])
    print("\n(A) AEMETH e variantes no selo:")
    for t, d in r["A_AEMETH"].items():
        print("   %-8s exato=%d  subsequência-no-anel=%s" % (t, d["exato_em_streams"], d["subsequencia_no_anel"]))
    an = r["A_AEMETH_null"]
    print("   AEMETH exato: real %d vs null média %.3f (máx %d)" % (an["real_exato"], an["null_mean"], an["null_max"]))
    print("\n(B) ponteiros 'outro propósito' (21/8/30/26):")
    for k, v in r["B_ponteiros_outro_proposito"]["casas_por_numero"].items():
        print("   num %s -> casas %s" % (k, v))
    print("   letras apontadas (ordem de casa):", r["B_ponteiros_outro_proposito"]["letras_apontadas"])
    print("\n(C) anel lido a partir das casas sem número (fechadores):")
    for k, v in r["C_anel_dos_fechadores"].items():
        print("   casa %s: %s" % (k, v))
