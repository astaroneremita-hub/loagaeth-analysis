# -*- coding: utf-8 -*-
"""a208 - the 3 distributional loners + the expanded name inventory.

Why do ACLAXT, DAXVAR, CHIDNO sit OUTSIDE the main blob? Which folhas, how many, and
what element/texture is their neighbourhood. And catalogue the expanded roots.

stdlib only.
"""
import os
import sys
import json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

GD_EL = {"A": "Ar", "E": "Ar", "T": "Ar", "I": "Agua", "L": "Agua", "M": "Agua",
         "O": "Fogo", "P": "Fogo", "R": "Fogo", "F": "Fogo",
         "G": "Terra", "N": "Terra", "S": "Terra", "C": "Terra"}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nums = load.table_numbers()
    ftext = {n: load.table_text(n) for n in nums}
    loners = ["ACLAXT", "DAXVAR", "CHIDNO"]
    fam = ["DNOCHA", "CHASTO", "ANZACH"]
    expanded = ["GRAPHA", "ACHEPH", "ANTANT", "XALGRA", "ANTOXA", "AXARGE", "NTAGNA",
                "ACLAXT", "ALGETH", "CHIDNO", "DAXVAR", "NADOXA", "ADMACH", "NOXADN"]

    full = "".join(ftext[n] for n in nums)
    c = Counter(full[i:i+6] for i in range(len(full)-5))

    def report(v):
        fs = [n for n in nums if v in ftext[n]]
        cnt = c.get(v, 0)
        el = Counter(GD_EL.get(ch, "?") for ch in v).most_common(1)[0][0]
        return fs, cnt, el

    print("=== 3 SOLITÁRIOS ===", flush=True)
    for v in loners:
        fs, cnt, el = report(v)
        print(f"  {v}: {cnt}x em {len(fs)} folhas {fs[:10]} elem~{el}", flush=True)
    print("=== FAMÍLIA (comparar) ===", flush=True)
    for v in fam:
        fs, cnt, el = report(v)
        print(f"  {v}: {cnt}x em {len(fs)} folhas elem~{el}", flush=True)
    print("=== INVENTÁRIO AMPLIADO ===", flush=True)
    inv = []
    for v in expanded:
        fs, cnt, el = report(v)
        inv.append({"nome": v, "ocorr": cnt, "folhas": len(fs), "elem": el, "primeira_folha": fs[0] if fs else None})
        print(f"  {v}: {cnt}x em {len(fs)} folhas elem~{el}", flush=True)

    out = {"loners": {v: {"ocorr": report(v)[1], "folhas": report(v)[0], "elem": report(v)[2]} for v in loners},
           "inventario_ampliado": inv}
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "208_loners.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
