# -*- coding: utf-8 -*-
"""
244 - Bateria exploratória no Sigillum Dei Aemeth: caçar padrão escondido.
Várias hipóteses independentes, cada uma com null quando cabe. Honesto: imprime os
candidatos crus (pra eyeball) e marca só o que supera o acaso.
stdlib only, seed 1583.
"""
import json, os, random, statistics, math
from collections import Counter, defaultdict
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583
LOAG = ["NOCHA", "GETH", "ALGETH", "CHASTOR", "ANZACH", "ACLAX", "NACHO", "DAXVAR", "CHIDNO", "GETHACLAX"]


def up(s): return "".join(ch for ch in (s or "").upper() if ch.isalpha())


def load_sda():
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        return json.load(f)


def ring_data(sda):
    L, NUM, ABV = [], [], []
    for c in sda["anel_externo_40"]["casas"]:
        L.append(up(c["letra"].replace("ω", "O")))
        NUM.append(c["numero"]); ABV.append(c["posicao_numero"] == "acima")
    return L, NUM, ABV


def word_score(s, loagset):
    # conta nomes-família do Loag + vogais-consoantes plausível
    return sum(s.count(nm) for nm in loagset)


def run():
    rng = random.Random(SEED)
    sda = load_sda()
    L, NUM, ABV = ring_data(sda)
    ring = "".join(L)
    out = {}

    # ---- H1: passo constante k ao redor do anel (fwd/rev) ----
    h1 = []
    base = "".join(L)  # 41 chars
    L40 = L  # 40 casas (algumas com 2 letras)
    for k in range(1, 20):
        for rev in (False, False):
            idx = list(range(0, 40 * 1, 1))
        seqf = "".join(L40[(i * k) % 40] for i in range(40))
        seqr = seqf[::-1]
        for tag, s in (("fwd", seqf), ("rev", seqr)):
            sc = word_score(s, LOAG)
            if sc > 0:
                h1.append({"k": k, "dir": tag, "score": sc, "seq": s[:60]})
    out["H1_passo_constante"] = h1

    # ---- H2: número como índice -> letra daquela casa ----
    idxread = "".join(L40[NUM[i] % 40] for i in range(40) if NUM[i] is not None)
    out["H2_numero_como_indice"] = {"string": idxread, "loag_score": word_score(idxread, LOAG)}

    # ---- H3: números como letras (1=A..) na ordem do anel ----
    AL = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numseq = [NUM[i] for i in range(40) if NUM[i] is not None]
    numletters = "".join(AL[(n - 1) % 26] for n in numseq)
    out["H3_numeros_como_letras"] = {"numbers": numseq, "as_A1Z26": numletters,
                                     "sum": sum(numseq), "count": len(numseq)}

    # ---- H4: acrósticos dos grupos de nomes ----
    gods = [up("".join(ch for ch in r["com_anotacoes"] if ch.isalpha())) for r in sda["nomes_de_deus_7"]["nomes"]]
    angels = [up(a["leitura_da_tabela"]) for a in sda["anjos_7"]["anjos"]]
    ringnames = [up(n.replace("ω", "O")) for n in sda["anel_externo_40"]["regra_de_leitura_declarada"]["ordem_final_dos_nomes"]]
    def acro(names):
        return {"primeiras": "".join(n[0] for n in names if n), "ultimas": "".join(n[-1] for n in names if n)}
    out["H4_acrosticos"] = {"nomes_de_deus": acro(gods), "anjos": acro(angels), "nomes_anel": acro(ringnames),
                            "gods_full": gods}

    # ---- H5: gematria ordinal (A=1..) — valores iguais entre SDA e Loag? ----
    def gem(s):  # ordinal, I/J=9 etc (21 letras enoquianas tratadas como latim)
        return sum((ord(c) - 64) for c in s if c.isalpha())
    sda_names = gods + angels + ringnames + [up(sda["angulos_7"]["leitura"].split()[0])]
    loag_vals = {nm: gem(nm) for nm in LOAG}
    sda_vals = {nm: gem(nm) for nm in sda_names}
    shared = []
    for a, va in sda_vals.items():
        for b, vb in loag_vals.items():
            if va == vb and va > 0:
                shared.append({"sda": a, "loag": b, "value": va})
    out["H5_gematria_ordinal"] = {"sda": sda_vals, "loag": loag_vals, "valores_iguais": shared}

    # ---- H6: o anel contém nomes de gramática Loag (raiz+afixo) acima de Markov? ----
    gram = ["NOCHA", "GETH", "CHA", "NOC", "OCHA", "ADN", "GET", "ETH", "OCH"]
    rr = ring + ring
    realc = sum(rr.count(g) for g in gram)
    # null: embaralha o anel
    def null():
        l = list(ring); rng.shuffle(l); r2 = "".join(l) * 2
        return sum(r2.count(g) for g in gram)
    nn = [null() for _ in range(500)]
    z = (realc - statistics.mean(nn)) / (statistics.pstdev(nn) or 1e-9)
    out["H6_gramatica_no_anel"] = {"real": realc, "null_mean": round(statistics.mean(nn), 1), "z": round(z, 2)}

    # ---- H7: letras do anel NÃO usadas pelos 7 nomes de salto ----
    used = set()
    starts = {"Galas": 1, "Gethog": 17, "Thaoth": 0, "Horlwn": 19, "Innon": 27, "Aaoth": 31, "Galethog": 33}
    for nm, st in starts.items():
        pos = st
        used.add(pos); steps = 0
        while NUM[pos] is not None and steps < 45:
            pos = (pos + (NUM[pos] if ABV[pos] else -NUM[pos])) % 40
            used.add(pos); steps += 1
            if NUM[pos] is None: break
    leftover = "".join(L40[i] for i in range(40) if i not in used)
    out["H7_letras_sobrando"] = {"usadas": len(used), "sobrando": leftover}

    with open(os.path.join(ROOT, "results", "244_sigillum_explore.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    return out


if __name__ == "__main__":
    r = run()
    print("RING:", "".join([]) or "")
    print("H1 passo constante — leituras com nome-Loag:", r["H1_passo_constante"] or "nenhuma")
    print("H2 número-como-índice:", r["H2_numero_como_indice"]["string"], "| loag_score", r["H2_numero_como_indice"]["loag_score"])
    h3 = r["H3_numeros_como_letras"]
    print("H3 números:", h3["numbers"])
    print("   soma =", h3["sum"], "| count =", h3["count"], "| como A1Z26 =", h3["as_A1Z26"])
    h4 = r["H4_acrosticos"]
    print("H4 acrósticos:")
    for g in ("nomes_de_deus", "anjos", "nomes_anel"):
        print("   %-14s primeiras=%s ultimas=%s" % (g, h4[g]["primeiras"], h4[g]["ultimas"]))
    print("   7 nomes de Deus:", h4["gods_full"])
    h5 = r["H5_gematria_ordinal"]
    print("H5 gematria — valores iguais SDA×Loag:", h5["valores_iguais"] or "nenhum")
    print("   Loag:", h5["loag"])
    h6 = r["H6_gramatica_no_anel"]
    print("H6 gramática no anel: real %d vs null %.1f (z %.2f)" % (h6["real"], h6["null_mean"], h6["z"]))
    print("H7 letras sobrando (fora dos 7 nomes):", r["H7_letras_sobrando"]["sobrando"])
