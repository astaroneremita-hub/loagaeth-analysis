"""
30 - Track D of the roadmap: anchors for meaning.

  D1) Words of the Calls - the only Angelic words with English glosses (Sloane 3191) - inside the
      Loagaeth. For each Call word of 4+ letters: occurrences vs Markov-3 expectation, and whether
      it behaves as a word there (varied letters on both sides = branching entropy). Words that are
      both far above expectation and word-like are the best candidate shared words, with Dee's gloss.
  D2) Dee's diaries (Sloane 3188) - the online page is a contents page; the text is in print only and
      the private corpus is not present here. Recorded as open.
  D3) Leaf titles: is each leaf's title written in its own leaf's dialect? A letter model of every
      side scores every title; the rank of the own side among all sides (0 = best) vs 0.5 by chance.
"""
import json
import math
import os
import statistics
from collections import Counter, defaultdict

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a23_name_discovery import M3, H

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def D1_call_words(book):
    import a21_index_heptarchy_numbers as a21
    calls = json.load(open(os.path.join(ROOT, "engine", "data", "chamadas.json"), encoding="utf-8"))["chamadas"]
    gloss = defaultdict(set)
    for ch in calls:
        for w in ch["palavras"]:
            n = a21.norm(w["enoquiano"])
            if len(n) >= 4 and w.get("ingles_sl3191"):
                gloss[n].add(w["ingles_sl3191"].strip())
    lines = [r for v in book.values() for r in v]
    m3 = M3(lines)
    npos = sum(len(r) for r in lines)
    left, right, cnt = defaultdict(Counter), defaultdict(Counter), Counter()
    for r in lines:
        for w in gloss:
            st = 0
            while True:
                i = r.find(w, st)
                if i < 0:
                    break
                cnt[w] += 1
                left[w][r[i - 1] if i > 0 else "#"] += 1
                right[w][r[i + len(w)] if i + len(w) < len(r) else "#"] += 1
                st = i + 1
    rows = []
    for w in gloss:
        c = cnt[w]
        if c < 3:
            continue
        e = m3.expected(w, npos)
        z = (c - e) / math.sqrt(e) if e > 0 else 99
        rows.append({"word": w, "gloss": "; ".join(sorted(gloss[w]))[:60], "count": c, "markov3_expected": round(e, 1),
                     "z": round(z, 1), "h_left": round(H(left[w]), 2), "h_right": round(H(right[w]), 2)})
    m = len(rows)
    zc = 3.5 if m < 60 else 4.0
    cand = [r for r in rows if r["z"] >= zc and r["h_left"] >= 2 and r["h_right"] >= 2]
    return {"call_words_tested": len(gloss), "occurring_3plus": m, "z_threshold": zc,
            "candidate_shared_words": sorted(cand, key=lambda r: -r["z"]),
            "all": sorted(rows, key=lambda r: -r["count"])[:30]}


def D3_titles(book):
    t = json.load(open(os.path.join(load.DATA, "loagaeth_leaf_titles.json"), encoding="utf-8"))["titles"]
    titles = {k: load.letters(v) for k, v in t.items() if k in book and len(load.letters(v)) >= 15}
    keys = sorted(book, key=lambda k: (tnum(k), k[-1]))
    models = {}
    for k in keys:
        m = CharLM(2, alpha=0.5)
        m.fit(book[k])
        models[k] = m
    ranks = []
    detail = []
    for k, s in titles.items():
        bits = {o: models[o].bits([s]) for o in keys}
        order = sorted(keys, key=lambda o: bits[o])
        r = order.index(k) / (len(keys) - 1)
        nb = [o for o in keys if abs(keys.index(o) - keys.index(k)) <= 2 and o != k]
        rnb = min(order.index(o) for o in nb) / (len(keys) - 1) if nb else None
        ranks.append(r)
        detail.append({"leaf": k, "letters": len(s), "own_rank": round(r, 2),
                       "best_neighbour_rank": round(rnb, 2) if rnb is not None else None, "best_side": order[0]})
    n = len(ranks)
    mu = statistics.mean(ranks)
    z = (0.5 - mu) / (math.sqrt(1 / 12) / math.sqrt(n))
    return {"titles_tested": n, "mean_own_rank": round(mu, 3), "chance": 0.5, "z": round(z, 2),
            "titles": sorted(detail, key=lambda d: d["own_rank"])}


def run():
    book = base_book()
    res = {"D1_call_words": D1_call_words(book),
           "D2_diaries": "Open. esotericarchives.com/dee/sl3188.htm is a contents page (the full text of the "
                         "Five Books of Mystery is in print); the British Library photos of Sloane 3188 are "
                         "linked but not reachable here; the private book corpus is not present in this repo.",
           "D3_titles": D3_titles(book)}
    load.save_result("30_anchors", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1)[:7000])
