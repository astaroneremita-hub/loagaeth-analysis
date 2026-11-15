# -*- coding: utf-8 -*-
"""a216 - analysis C (delivery): each Call beside the table it opens, with that table's
heaviest names. Not a test - a usable instrument. Writes viz/calls_tables.json.
"""
import os
import sys
import json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

DATA = os.path.join(os.path.dirname(HERE), "engine", "data")
NAMES = ['NACHO','NOCHAP','NOCHASTOR','NOCHAPH','ADNOCHAP','ACLAXTO','GRADAX','AXALGRA',
 'NOCHASTORA','ICHASTOR','PHANGE','ANTANTOX','VOXAR','NECHASTOR','ACLAXTOR','ICHASTORA',
 'ZICHASTOR','ANCHANO','NADAB','CHARDAX','AOXARD','ALCHADAX','OXARDRAH','OLCHADNA',
 'NACLANSA','DONCHAL','ACHARDAN','CHIDAXTO','GASTA','NODALGA','UCHER','ALGETH','GETH',
 'ACLAX','ANZACH','DAXVAR','ACLAXT','CHIDNO','NTAGNA','ACHEPH','GRAPHA']


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ch = json.load(open(os.path.join(DATA, "chamadas.json"), encoding="utf-8"))["chamadas"]
    ftext = {n: load.table_text(n) for n in load.table_numbers()}

    def top_names(tnum):
        if tnum not in ftext:
            return []
        t = ftext[tnum]
        cnt = [(nm, t.count(nm)) for nm in NAMES]
        cnt = sorted([x for x in cnt if x[1] > 0], key=lambda x: -x[1])
        return cnt[:6]

    out = []
    for c in ch:
        num = c["numero"]
        tab = c.get("tabua_que_move_segundo_o_tfr")
        pal = c.get("palavras") or []
        eno = " ".join(p.get("enoquiano", "") for p in pal if p.get("enoquiano"))
        eng = " ".join((p.get("ingles_sl3191") or p.get("ingles") or "") for p in pal).strip()
        tfr = c.get("tfr") or {}
        trad = tfr.get("traducao") or tfr.get("ingles") or ""
        out.append({
            "numero": num, "nome": c.get("nome"), "tabua": tab,
            "inicio": c.get("inicio_sl3191", ""),
            "enoquiano": eno[:600], "ingles": (eng or trad)[:600],
            "nomes_pesados": top_names(tab) if isinstance(tab, int) else [],
        })

    viz = {"calls": out, "nota": "Chamada N move a folha indicada (TFR); a folha 1 não tem Chamada."}
    with open(os.path.join(os.path.dirname(HERE), "viz", "calls_tables.json"), "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    for c in out[:6]:
        print(f"Chamada {c['numero']} -> folha {c['tabua']}: {c['inicio']!r}  nomes {[(n,k) for n,k in c['nomes_pesados'][:3]]}", flush=True)
    print(f"total chamadas: {len(out)}", flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
