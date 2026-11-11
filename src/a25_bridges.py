"""
25 - Bridges to Dee's other systems, and the constellation of names.

  A) Does a name of another system occur inside the Loagaeth more than chance, and where?
     Pools: Watchtower names (derived by rule), the 49 Heptarchic good angels, the 91 governors,
     the 30 Aethyr names, and the words of the Calls (>= 4 letters). For each pool: total occurrences
     in the book vs (i) the count expected from a Markov-3 model of the book and (ii) the same names
     with their letters shuffled (same composition). Hits are also placed by segment.
  B) Constellation: do the master names pile up on particular cells when the 36 exact 49x49 sides
     are stacked? Statistic = the busiest 3x3 window of name starts. Nulls: (i) each occurrence keeps
     its column and gets a random row; (ii) keeps its row and gets a random column that fits.
"""
import json
import os
import random
import statistics
from collections import Counter, defaultdict

import load
from a22_robustness_and_depth import base_book, tnum
from a23_name_discovery import M3

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SEG_OF = {**{t: "opening" for t in range(2, 6)}, **{t: "heartland" for t in range(6, 26)},
          **{t: "decoded 26-28" for t in range(26, 29)}, **{t: "diamonds" for t in range(29, 44)},
          **{t: "end" for t in range(44, 49)}}


def pools():
    import sys
    sys.path.insert(0, os.path.join(ROOT, "engine"))
    import enoch
    import a21_index_heptarchy_numbers as a21
    E = os.path.join(ROOT, "engine", "data")
    h = json.load(open(os.path.join(E, "heptarquia.json"), encoding="utf-8"))
    g = json.load(open(os.path.join(E, "governadores.json"), encoding="utf-8"))
    c = json.load(open(os.path.join(E, "chamadas.json"), encoding="utf-8"))["chamadas"]
    n = a21.norm
    P = {
        "watchtower": [n(x["name"]) for x in enoch.derive_names()],
        "heptarchy_49": [n(x["nome"]) for x in h["tabula_collecta"]["nomes"]],
        "governors_91": [n(x["nome"]) for x in g["governadores"]],
        "aethyrs_30": [n(x.get("nome_dee_confirmado_em_fonte_primaria") or x.get("nome_crowley_1911") or "")
                       for x in g["aethyrs"]],
        "call_words": [n(w["enoquiano"]) for ch in c for w in ch["palavras"]],
    }
    # Aethyr names are three letters; every other pool uses names of four letters or more
    return {k: sorted({x for x in v if len(x) >= (3 if k == "aethyrs_30" else 4)}) for k, v in P.items()}


def A_bridges(book, rng):
    lines = [r for v in book.values() for r in v]
    m3 = M3(lines)
    npos = sum(len(r) for r in lines)
    by_table = defaultdict(list)
    for k, v in book.items():
        by_table[tnum(k)] += v
    ttext = {t: "|".join(v) for t, v in by_table.items()}
    S = "|".join(lines)
    seg_letters = Counter()
    for t, v in by_table.items():
        seg_letters[SEG_OF[t]] += sum(len(r) for r in v)
    out = {}
    for pool, names in pools().items():
        obs = {x: S.count(x) for x in names}
        exp = sum(m3.expected(x, npos) for x in names)
        shuf = []
        for _ in range(30):
            tot = 0
            for x in names:
                l = list(x)
                rng.shuffle(l)
                tot += S.count("".join(l))
            shuf.append(tot)
        hits = {x: c for x, c in obs.items() if c}
        seg = Counter()
        for x in hits:
            for t, s in ttext.items():
                seg[SEG_OF[t]] += s.count(x)
        tot_l = sum(seg_letters.values())
        seg_ratio = {s: round(seg[s] / max(1, sum(seg.values())) / (seg_letters[s] / tot_l), 2) for s in seg_letters} if seg else {}
        out[pool] = {"names": len(names), "names_found": len(hits), "occurrences": sum(obs.values()),
                     "markov3_expected": round(exp, 1),
                     "shuffled_letters_mean": round(statistics.mean(shuf), 1),
                     "shuffled_letters_max": max(shuf),
                     "found": dict(sorted(hits.items(), key=lambda kv: -kv[1])[:15]),
                     "segment_enrichment": seg_ratio}
    return out


def B_constellation(book, rng):
    fs = {k: v for k, v in book.items() if tnum(k) <= 25 and k != "25b" and len(v) == 49 and all(len(r) == 49 for r in v)}
    names = ["CHASTOR", "ANZACH", "GETH", "NOCHA", "ACLAX", "OXAD"]
    res = {}
    for n in names:
        occ = []
        for v in fs.values():
            for r, row in enumerate(v):
                st = 0
                while True:
                    i = row.find(n, st)
                    if i < 0:
                        break
                    occ.append((r, i))
                    st = i + 1

        def busiest(pts):
            g = Counter(pts)
            best = 0
            for r in range(49):
                for c in range(49):
                    s = sum(g[(r + a, c + b)] for a in (-1, 0, 1) for b in (-1, 0, 1))
                    best = max(best, s)
            return best
        obs = busiest(occ)
        n1, n2 = [], []
        for _ in range(100):
            n1.append(busiest([(rng.randrange(49), c) for r, c in occ]))
            n2.append(busiest([(r, rng.randrange(49 - len(n) + 1)) for r, c in occ]))
        res[n] = {"occurrences": len(occ), "busiest_3x3": obs,
                  "null_random_row_mean": round(statistics.mean(n1), 1), "null_random_row_95": sorted(n1)[94],
                  "null_random_column_mean": round(statistics.mean(n2), 1), "null_random_column_95": sorted(n2)[94]}
    return res


def run():
    rng = random.Random(25)
    book = base_book()
    res = {"A_bridges": A_bridges(book, rng), "B_constellation": B_constellation(book, rng)}
    load.save_result("25_bridges", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
