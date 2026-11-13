"""
a146 - Is there a 7-fold structure in the Loagaeth? (49 = 7x7; 7 is the sacred number of the whole Enochian system)

The 49x49 grid is 7^4. The Heptarchy, the 7 planets, the 7 days - 7 pervades Enochian. Kabbalistic lens: do the
names organize on a 7 grid? We measure, per table, the name-start density per row (0-48) and test (A) period-7
autocorrelation (do name-dense rows recur every 7?) and (B) 7-band concentration (do names cluster in specific of the
7 bands of 7 rows?), each against a null that shuffles the row densities (destroys any 7-structure, keeps the totals).
If the real book shows 7-fold organization beyond the shuffle, the sacred number is built into the name-field.
"""
import json
import random
import statistics

import load
from a22_robustness_and_depth import base_book


def square_grids():
    book = base_book()
    out = []
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            out.append(g)
    return out


def row_density(g, names):
    R = 49
    d = [0] * R
    for r in range(R):
        row = g[r]
        for w in names:
            if len(w) >= 4:
                i = row.find(w)
                while i >= 0:
                    d[r] += 1
                    i = row.find(w, i + 1)
    return d


def autocorr(d, lag):
    n = len(d)
    m = statistics.mean(d)
    num = sum((d[i] - m) * (d[i + lag] - m) for i in range(n - lag))
    den = sum((x - m) ** 2 for x in d)
    return num / den if den else 0


def band7(d):
    # 49 rows -> 7 bands of 7; variance of band totals (high = concentrated)
    bands = [sum(d[b * 7:(b + 1) * 7]) for b in range(7)]
    m = statistics.mean(bands)
    return statistics.pvariance(bands)


def run():
    gs = square_grids()
    names = [w for w in json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8")) if len(w) >= 4]
    alld = [0] * 49
    for g in gs:
        d = row_density(g, names)
        for i in range(49):
            alld[i] += d[i]

    real_ac7 = autocorr(alld, 7)
    real_band = band7(alld)

    rng = random.Random(146)
    ac7_null, band_null = [], []
    for _ in range(1000):
        s = alld[:]
        rng.shuffle(s)
        ac7_null.append(autocorr(s, 7))
        band_null.append(band7(s))
    # p-values (two-sided for autocorr magnitude, one-sided high for band var)
    p_ac = (sum(1 for x in ac7_null if abs(x) >= abs(real_ac7)) + 1) / 1001
    p_band = (sum(1 for x in band_null if x >= real_band) + 1) / 1001

    # compare lag7 vs neighbor lags to see if 7 is special
    neigh = {lag: autocorr(alld, lag) for lag in (5, 6, 7, 8, 9)}

    res = {
        "tables": len(gs), "autocorr_lag7": round(real_ac7, 3), "p_autocorr7": round(p_ac, 4),
        "band7_variance_real": round(real_band, 1), "band7_variance_null_mean": round(statistics.mean(band_null), 1),
        "p_band7": round(p_band, 4), "autocorr_neighbors": {k: round(v, 3) for k, v in neigh.items()},
        "finding": (
            "Estrutura 7-fold (49=7x7). Autocorrelação de densidade de nomes no lag 7: %.2f (p=%.3f). Concentração em "
            "7 bandas: variância %.0f vs %.0f no acaso (p=%.3f). Vizinhos (lags 5-9): %s. %s" % (
                real_ac7, p_ac, real_band, statistics.mean(band_null), p_band,
                {k: round(v, 2) for k, v in neigh.items()},
                ("CONFIRMADO: há organização de período 7 na distribuição dos nomes - o número sagrado está no campo."
                 if p_ac < 0.05 or p_band < 0.05 else
                 "sem estrutura 7-fold: a densidade de nomes não tem período 7 nem concentração em bandas acima do "
                 "acaso - o 7 do formato (49x49) não se reflete na distribuição dos nomes."))),
    }
    load.save_result("146_sevenfold", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("autocorr lag7 %.3f (p=%.3f) | banda-7 var %.0f vs null %.0f (p=%.3f)" % (
        r["autocorr_lag7"], r["p_autocorr7"], r["band7_variance_real"], r["band7_variance_null_mean"], r["p_band7"]))
    print("vizinhos (lag->autocorr):", r["autocorr_neighbors"])
