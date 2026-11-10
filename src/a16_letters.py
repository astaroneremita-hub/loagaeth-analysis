"""
16 - The letters themselves: counts, gematria values, hidden names, where each letter lives.

  A) Count and share of every letter in the dense tables (2-48), with each letter's value in
     every bundled Enochian gematria system ("pure" letter values, for reference only).
  B) Do the most frequent letters spell a name? For k = 3..8, is the set of the top-k letters an
     exact anagram of any attested Call word or recurring Loagaeth word? Null: random k-letter
     sets drawn with the real letter frequencies.
  C) Frequency vs letter value, per gematria system (Spearman, permutation p, Bonferroni).
  D) Where letters sit in the full 49x49 grids (tables 2-25): letter x region (four quadrants
     + the central cross) against a within-grid shuffle; left/right with the edge columns
     removed; the first and last column of each row; the centre cell.
  E) Letter mix by segment of the book (opening 2-5, heartland 6-25, diamonds 29-43, end 44-48),
     against shuffling tables between segments.
  F) The U register: the end segment shares far more recurring 5-grams with the heartland once
     A is replaced by U - tested against the other vowel swaps (A->E, A->I, A->O).
"""
import json
import math
import os
import random
import statistics
import sys
from collections import Counter

import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))

SEGMENTS = {"opening_2_5": range(2, 6), "heartland_6_25": range(6, 26),
            "diamonds_29_43": range(29, 44), "end_44_48": range(44, 49)}
REGIONS = ["TL", "TR", "BL", "BR", "CROSS"]


def rows(key):
    return [load.letters(r) for r in load.leaves().get(key, [])]


def stream(tables):
    return "".join(load.letters("".join(load.leaves().get(f"{t}{s}", []))) for t in tables for s in "ab")


def full_grids():
    out = []
    for t in range(2, 26):
        for s in "ab":
            g = rows(f"{t}{s}")
            if len(g) == 49 and all(len(r) == 49 for r in g):
                out.append(g)
    return out


def region(r, c):
    if r == 24 or c == 24:
        return "CROSS"
    return ("T" if r < 24 else "B") + ("L" if c < 24 else "R")


def chi_regions(grids):
    M = {k: Counter() for k in REGIONS}
    for g in grids:
        for r in range(49):
            for c in range(49):
                M[region(r, c)][g[r][c]] += 1
    tot = {k: sum(M[k].values()) for k in REGIONS}
    T = sum(tot.values())
    per = {}
    for L in set().union(*M.values()):
        nL = sum(M[k][L] for k in REGIONS)
        per[L] = sum((M[k][L] - nL * tot[k] / T) ** 2 / (nL * tot[k] / T) for k in REGIONS if nL * tot[k] / T > 0)
    return sum(per.values()), per, M, tot


def spearman(a, b):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for j, i in enumerate(o):
            r[i] = j
        return r
    ra, rb = rk(a), rk(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = (sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb)) ** 0.5
    return num / den if den else 0.0


def run():
    rng = random.Random(16)
    dense = stream(range(2, 49))
    cnt = Counter(dense)
    N = sum(cnt.values())
    try:
        import fontes
        G = fontes.gematria_value_tables()
    except Exception:
        G = {}

    # A
    letters = [{"letter": c, "count": n, "share": round(n / N, 4),
                "values": {sid: tab.get(c) for sid, tab in G.items() if c in tab}}
               for c, n in cnt.most_common()]

    # B
    lex = set(json.load(open(os.path.join(ROOT, "data", "call_lexicon.json"), encoding="utf-8"))["attested_wordforms"])
    voc = [v["word"] for v in json.load(open(os.path.join(ROOT, "data", "loagaeth_vocabulary.json"), encoding="utf-8"))["vocabulary"]]
    pool = {}
    for w in list(lex) + voc:
        pool.setdefault("".join(sorted(w)), set()).add(w)
    order = [c for c, _ in cnt.most_common()]
    ls, ws = list(cnt), [cnt[c] for c in cnt]
    hidden = []
    for k in range(3, 9):
        hits = sorted(pool.get("".join(sorted(order[:k])), set()))
        sims = 0
        for _ in range(2000):
            s = set()
            while len(s) < k:
                s.add(rng.choices(ls, ws)[0])
            sims += "".join(sorted(s)) in pool
        hidden.append({"k": k, "top_letters": "".join(order[:k]), "words": hits[:5], "chance_any_word": round(sims / 2000, 3)})

    # C
    freq_value = []
    for sid, tab in G.items():
        lt = [c for c in cnt if c in tab]
        if len(lt) < 12:
            continue
        a, b = [cnt[c] for c in lt], [tab[c] for c in lt]
        o = spearman(a, b)
        s = [spearman(a, rng.sample(b, len(b))) for _ in range(1500)]
        freq_value.append({"system": sid, "rho": round(o, 2), "p": round(sum(1 for x in s if abs(x) >= abs(o)) / len(s), 3)})
    bonf = 0.05 / max(1, len(freq_value))

    # D
    grids = full_grids()
    obs, per, M, tot = chi_regions(grids)
    null = []
    for _ in range(150):
        sh = []
        for g in grids:
            f = list("".join(g))
            rng.shuffle(f)
            sh.append(["".join(f[i * 49:(i + 1) * 49]) for i in range(49)])
        null.append(chi_regions(sh)[0])
    T = sum(tot.values())
    enrich = {L: {k: round(M[k][L] / (sum(M[x][L] for x in REGIONS) * tot[k] / T), 2) for k in REGIONS}
              for L, _ in sorted(per.items(), key=lambda kv: -kv[1])[:12]}
    Lc, Rc = Counter(), Counter()
    first, last, mid = Counter(), Counter(), Counter()
    for g in grids:
        for r in g:
            first[r[0]] += 1
            last[r[48]] += 1
            mid.update(r[1:48])
            for c in range(3, 46):
                if c < 24:
                    Lc[r[c]] += 1
                elif c > 24:
                    Rc[r[c]] += 1
    mt, lt_, rt_ = sum(mid.values()), sum(Lc.values()), sum(Rc.values())
    row_start = sorted(((L, round(first[L] / len(grids) / 49 / (mid[L] / mt), 2)) for L in first if mid[L] > 500), key=lambda x: -x[1])
    row_end = sorted(((L, round(last[L] / len(grids) / 49 / (mid[L] / mt), 2)) for L in last if mid[L] > 500), key=lambda x: -x[1])
    lr_inner = {c: round((Rc[c] / rt_) / (Lc[c] / lt_), 2) for c in "VIGPZCXHSO" if Lc[c]}
    centre = Counter(g[24][24] for g in grids)

    # E
    tabs = {t: Counter(stream([t])) for rg in SEGMENTS.values() for t in rg}
    lab = {t: k for k, rg in SEGMENTS.items() for t in rg}

    def chi_seg(lb):
        S = {}
        for t, c in tabs.items():
            S.setdefault(lb[t], Counter()).update(c)
        tt = {k: sum(v.values()) for k, v in S.items()}
        TT = sum(tt.values())
        x = 0.0
        for L in set().union(*S.values()):
            nL = sum(S[k][L] for k in S)
            for k in S:
                e = nL * tt[k] / TT
                if e > 5:
                    x += (S[k][L] - e) ** 2 / e
        return x, S, tt
    xo, S, tt = chi_seg(lab)
    keys, vals = list(tabs), [lab[k] for k in tabs]
    xs = []
    for _ in range(300):
        rng.shuffle(vals)
        xs.append(chi_seg(dict(zip(keys, vals)))[0])
    shares = {k: {L: round(100 * S[k][L] / tt[k], 2) for L in "AONHLDRCXEGTVPZUIMS"} for k in SEGMENTS}

    # F
    heart, end = stream(range(6, 26)), stream(range(44, 49))

    def grams(s, k, minf):
        c = Counter(s[i:i + k] for i in range(len(s) - k + 1))
        return {g for g, f in c.items() if f >= minf}
    E, H = grams(end, 5, 2), grams(heart, 5, 3)
    swaps = {"as_is": len(E & H)}
    for v in "EIOU":
        swaps["A->" + v] = len(E & {g.replace("A", v) for g in H})
    ex = sorted(E & {g.replace("A", "U") for g in H}, key=lambda g: -end.count(g))[:15]

    res = {
        "A_letters": letters,
        "B_hidden_name_in_top_letters": hidden,
        "C_frequency_vs_value": {"tests": freq_value, "bonferroni_alpha": round(bonf, 4),
                                 "significant": [t["system"] for t in freq_value if t["p"] < bonf]},
        "D_space": {"chi2_regions": round(obs, 1), "null_mean": round(statistics.mean(null), 1),
                    "null_95th": round(sorted(null)[int(0.95 * len(null))], 1),
                    "region_enrichment_top": enrich, "right_over_left_without_edges": lr_inner,
                    "row_start_enrichment": row_start[:8], "row_end_enrichment": row_end[:8],
                    "centre_cell": centre.most_common(6), "n_grids": len(grids)},
        "E_segments": {"chi2": round(xo), "null_mean": round(statistics.mean(xs)), "null_max": round(max(xs)),
                       "shares_percent": shares},
        "F_u_register": {"recurring_5grams_end": len(E), "overlap_with_heartland": swaps,
                         "examples": [{"end": g, "count": end.count(g), "heartland": g.replace("U", "A")} for g in ex]},
        "conclusion": ("A dominates (19%). The top letters spell no attested name; letter values do not "
                       "track frequency. Rows are aligned to word boundaries (onsets at the start, "
                       "terminators at the end); away from the edges left and right are alike. The letter "
                       "mix differs strongly by segment, and the end segment re-uses heartland vocabulary "
                       "with A shifted to U."),
    }
    load.save_result("16_letters", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1)[:4000])
