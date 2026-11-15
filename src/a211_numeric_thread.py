# -*- coding: utf-8 -*-
"""a211 - dissect THE loose thread (EXPLORED.md): digits 2/3/6 dominate the 91 governors'
servant numbers (~60% vs 30%, p<3e-4), 62/91 contain a 6. Flagged unexplained.

New tests (not done before):
 1) WHERE is the excess - by digit position (thousands/hundreds/tens/units)?
 2) Leading-digit vs Benford - do the numbers just live in the 2000s/3000s/6000s?
 3) Is the servant count DERIVED from the governor name (gematria / letter-count)? If yes,
    the thread is construction, not mystery.
 4) Arithmetic structure: common divisor, roundness, parity.
Null where relevant. stdlib only. seed 1583.
"""
import os
import sys
import json
import math
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "engine", "data")
GEM = {"A": 1, "B": 2, "C": 20, "D": 4, "E": 5, "F": 6, "G": 3, "H": 8, "I": 10, "L": 30,
       "M": 40, "N": 50, "O": 70, "P": 80, "Q": 90, "R": 100, "S": 200, "T": 300, "U": 400,
       "X": 60, "Z": 7, "V": 400}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    g = json.load(open(os.path.join(DATA, "governadores.json"), encoding="utf-8"))
    govs = [x for x in g["governadores"] if x.get("servos")]
    serv = [x["servos"] for x in govs]
    names = [(x.get("nome") or "").upper() for x in govs]

    # 1) digit excess by position (align to 4 digits, pad left)
    pos = {"milhar": Counter(), "centena": Counter(), "dezena": Counter(), "unidade": Counter()}
    labels = ["milhar", "centena", "dezena", "unidade"]
    for s in serv:
        ds = str(s).zfill(4)[-4:]
        for i, lab in enumerate(labels):
            pos[lab][ds[i]] += 1
    print("[POS] share de 2/3/6 por posição:")
    for lab in labels:
        n = sum(pos[lab].values())
        share = sum(pos[lab][d] for d in "236") / n
        print(f"  {lab:8s}: 2={pos[lab]['2']:2d} 3={pos[lab]['3']:2d} 6={pos[lab]['6']:2d}  share(2,3,6)={share:.0%}  top={pos[lab].most_common(3)}", flush=True)

    # 2) leading digit vs Benford
    lead = Counter(str(s)[0] for s in serv)
    nL = sum(lead.values())
    benford = {str(d): math.log10(1 + 1 / d) for d in range(1, 10)}
    print("[LEAD] dígito líder vs Benford:")
    for d in "123456789":
        print(f"   {d}: obs {lead[d]/nL:.0%}  benford {benford[d]:.0%}", flush=True)

    # 3) servant count derived from name? correlation with gematria & letter count
    gem = [sum(GEM.get(ch, 0) for ch in nm) for nm in names]
    lc = [len(nm) for nm in names]
    def corr(a, b):
        n = len(a); ma = sum(a) / n; mb = sum(b) / n
        cov = sum((a[i] - ma) * (b[i] - mb) for i in range(n))
        va = sum((x - ma) ** 2 for x in a); vb = sum((x - mb) ** 2 for x in b)
        return cov / math.sqrt(va * vb) if va and vb else 0
    r_gem = corr(serv, gem); r_lc = corr(serv, lc)
    print(f"[DERIV] corr(servos, gematria_nome)={r_gem:+.3f}  corr(servos, n_letras)={r_lc:+.3f}", flush=True)

    # 4) arithmetic structure
    from math import gcd
    from functools import reduce
    G = reduce(gcd, serv)
    even = sum(1 for s in serv if s % 2 == 0)
    mult6 = sum(1 for s in serv if s % 6 == 0)
    end0 = sum(1 for s in serv if s % 10 == 0)
    print(f"[ARIT] GCD de todos={G}  pares {even}/{len(serv)}  múltiplos de 6: {mult6}  terminam em 0: {end0}", flush=True)
    print(f"[ARIT] soma total servos={sum(serv)}  média={sum(serv)//len(serv)}", flush=True)
    # distinct values (repeats?)
    rep = Counter(serv)
    print(f"[ARIT] valores distintos {len(rep)}/{len(serv)}; repetidos: {[(v,c) for v,c in rep.most_common(5) if c>1]}", flush=True)

    result = {"pos_236_share": {lab: round(sum(pos[lab][d] for d in '236') / sum(pos[lab].values()), 3) for lab in labels},
              "leading_vs_benford": {d: [round(lead[d]/nL, 3), round(benford[d], 3)] for d in "123456789"},
              "corr_servos_gematria": round(r_gem, 3), "corr_servos_nletras": round(r_lc, 3),
              "gcd": G, "even": even, "mult6": mult6, "end0": end0,
              "distinct": len(rep), "total": sum(serv)}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "211_numeric_thread.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
