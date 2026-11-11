"""
32 - Is it one language? The Loagaeth, the Calls, the Great Table and the Heptarchy compared.

  A) Letter-order test. A letter model (2-letter memory) is trained on the Loagaeth and another on
     the Calls. Each reads the other systems' strings (Great Table rows and columns, Watchtower names
     derived by rule, the 49 Heptarchic names, the 91 governors, the Calls' words). Score = bits per
     letter of the real strings minus the same strings with their letters shuffled inside each
     string (200 shuffles): negative = the ORDER of letters is the model's language, not only the
     letter mix. z from the shuffles.
  B) Letter mix: cosine similarity of letter frequencies between systems.
  C) The Great Table as a grid: is a cell predictable from its left neighbour or the one above
     (as in a rule-generated table like the Soyga's)? Conditional entropy vs shuffled grids.
     Doubled letters along rows (the Loagaeth forbids them).
"""
import json
import math
import os
import random
import statistics
import sys
from collections import Counter

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
E = os.path.join(ROOT, "engine", "data")
sys.path.insert(0, os.path.join(ROOT, "engine"))


def norm(s):
    import a21_index_heptarchy_numbers as a21
    return a21.norm(s)


def great_table():
    d = json.load(open(os.path.join(E, "tabuas_dee1584.json"), encoding="utf-8"))
    g = d["grades_por_fonte"]["tfr1659"]
    return {k: [[norm(c or "") or "?" for c in row] for row in rows] for k, rows in g.items()}


def systems():
    import enoch
    h = json.load(open(os.path.join(E, "heptarquia.json"), encoding="utf-8"))
    gv = json.load(open(os.path.join(E, "governadores.json"), encoding="utf-8"))
    c = json.load(open(os.path.join(E, "chamadas.json"), encoding="utf-8"))["chamadas"]
    gt = great_table()
    rows = ["".join(r).replace("?", "") for t in gt.values() for r in t]
    cols = ["".join(t[r][c] for r in range(len(t))).replace("?", "") for t in gt.values() for c in range(len(t[0]))]
    return {
        "great_table_rows": rows,
        "great_table_columns": cols,
        "watchtower_names": sorted({norm(x["name"]) for x in enoch.derive_names() if len(norm(x["name"])) >= 4}),
        "heptarchy_49": [norm(x["nome"]) for x in h["tabula_collecta"]["nomes"]],
        "governors_91": [norm(x["nome"]) for x in gv["governadores"]],
        "call_words": sorted({norm(w["enoquiano"]) for ch in c for w in ch["palavras"] if len(norm(w["enoquiano"])) >= 4}),
    }


def order_test(model, strings, rng, n=200):
    strings = [s for s in strings if len(s) >= 4]
    real = model.bits(strings)
    sh = []
    for _ in range(n):
        ss = []
        for s in strings:
            l = list(s)
            rng.shuffle(l)
            ss.append("".join(l))
        sh.append(model.bits(ss))
    mu, sd = statistics.mean(sh), statistics.pstdev(sh) or 1e-9
    return {"strings": len(strings), "bits_real": round(real, 3), "bits_shuffled": round(mu, 3),
            "gain": round(mu - real, 3), "z": round((mu - real) / sd, 1)}


def cosine(a, b):
    num = sum(a[k] * b.get(k, 0) for k in a)
    return num / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())))


def hcond(pairs):
    c = Counter(pairs)
    ctx = Counter(a for a, _ in pairs)
    n = len(pairs)
    return -sum(v / n * math.log2(v / ctx[a]) for (a, b), v in c.items())


def C_grid(rng):
    gt = great_table()
    def measures(tabs):
        left = [(t[r][c - 1], t[r][c]) for t in tabs for r in range(len(t)) for c in range(1, len(t[0]))]
        up = [(t[r - 1][c], t[r][c]) for t in tabs for r in range(1, len(t)) for c in range(len(t[0]))]
        dbl = sum(a == b for a, b in left) / len(left)
        return hcond(left), hcond(up), dbl
    tabs = list(gt.values())
    o = measures(tabs)
    nul = []
    for _ in range(500):
        sh = []
        for t in tabs:
            cells = [c for row in t for c in row]
            rng.shuffle(cells)
            sh.append([cells[i * len(t[0]):(i + 1) * len(t[0])] for i in range(len(t))])
        nul.append(measures(sh))
    out = {}
    for i, lab in enumerate(["H_cell_given_left", "H_cell_given_above", "doubled_along_rows"]):
        xs = [n[i] for n in nul]
        out[lab] = {"observed": round(o[i], 4), "shuffled_mean": round(statistics.mean(xs), 4),
                    "z": round((o[i] - statistics.mean(xs)) / (statistics.pstdev(xs) or 1e-9), 1)}
    return out


def run():
    rng = random.Random(32)
    book = base_book()
    lo_lines = [r for v in book.values() for r in v]
    S = systems()
    lo = CharLM(2, alpha=0.5).fit(lo_lines)
    ca = CharLM(2, alpha=0.5).fit(S["call_words"])
    A = {}
    for name, strs in S.items():
        A[name] = {"read_by_loagaeth_model": order_test(lo, strs, rng)}
        if name != "call_words":
            A[name]["read_by_calls_model"] = order_test(ca, strs, rng)
    # control: Loagaeth sample read by the Calls model
    sample = [r[i:i + 7] for r in rng.sample(lo_lines, 300) for i in (5, 20) if len(r) > 30]
    A["loagaeth_7_letter_pieces"] = {"read_by_calls_model": order_test(ca, sample, rng)}
    freq = {k: Counter("".join(v)) for k, v in S.items()}
    freq["loagaeth"] = Counter("".join(lo_lines))
    keys = ["loagaeth", "call_words", "great_table_rows", "heptarchy_49", "governors_91"]
    B = {a: {b: round(cosine(freq[a], freq[b]), 3) for b in keys} for a in keys}
    res = {"A_letter_order": A, "B_letter_mix_cosine": B, "C_great_table_grid": C_grid(rng)}
    load.save_result("32_one_language", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
