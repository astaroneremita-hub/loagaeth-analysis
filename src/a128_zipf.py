"""
Passo 15 (a128) - Does the name-lexicon follow Zipf's law? A linguistic frequency signature.

Natural lexicons are Zipfian: frequency ~ 1/rank, a straight line in log-log. We rank the attested names by total
occurrences across the 36 sheets and fit the log-rank/log-freq line; a clean, steep power law is a language-like
signature. Null: the same names counted on Markov-3 surrogate sheets (same letters, no lexicon). If the real lexicon
is markedly more Zipfian (better fit / proper slope) than the surrogate, the name-frequency structure is linguistic,
not an artifact of letter statistics.
"""
import json
import math
import random

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def square_grids(book):
    out = []
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            out.append(g)
    return out


def lines(g):
    R = 49
    out = [g[r] for r in range(R)]
    out += ["".join(g[r][c] for r in range(R)) for c in range(R)]
    for s in range(R):
        out.append("".join(g[s + k][k] for k in range(R - s)))
        if s:
            out.append("".join(g[k][s + k] for k in range(R - s)))
    return out


def freqs(grids, names):
    text = "\n".join("\n".join(lines(g)) for g in grids)
    rtext = "\n".join("\n".join(l[::-1] for l in lines(g)) for g in grids)
    f = {}
    for w in names:
        c = text.count(w) + rtext.count(w)
        if c > 0:
            f[w] = c
    return f


def zipf_fit(freq):
    """log-log least squares of rank vs freq; return slope and R^2."""
    fs = sorted(freq.values(), reverse=True)
    xs = [math.log(i + 1) for i in range(len(fs))]
    ys = [math.log(v) for v in fs]
    n = len(xs)
    if n < 5:
        return 0, 0
    mx = sum(xs) / n; my = sum(ys) / n
    sxy = sum((xs[i] - mx) * (ys[i] - my) for i in range(n))
    sxx = sum((x - mx) ** 2 for x in xs)
    syy = sum((y - my) ** 2 for y in ys)
    slope = sxy / sxx if sxx else 0
    r2 = (sxy ** 2) / (sxx * syy) if sxx and syy else 0
    return slope, r2


def run():
    book = base_book()
    grids = square_grids(book)
    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))

    real = freqs(grids, names)
    rslope, rr2 = zipf_fit(real)

    # surrogate sheets
    full = "".join("".join(g) for g in grids)
    R = 49
    sres = []
    for s in range(6):
        st = "".join(markov3(full, random.Random(1280 + s)))
        sg = []
        p = 0
        for _ in range(len(grids)):
            sg.append([st[p + i * R:p + (i + 1) * R] for i in range(R)]); p += R * R
        sf = freqs(sg, names)
        sl, r2 = zipf_fit(sf) if sf else (0, 0)
        sres.append((sl, r2, len(sf)))
    s_r2 = sum(x[1] for x in sres) / len(sres)
    s_slope = sum(x[0] for x in sres) / len(sres)
    s_types = sum(x[2] for x in sres) / len(sres)

    top = sorted(real.items(), key=lambda kv: -kv[1])[:15]
    res = {
        "distinct_names_real": len(real), "distinct_names_surrogate": round(s_types, 1),
        "zipf_slope_real": round(rslope, 2), "zipf_r2_real": round(rr2, 3),
        "zipf_slope_surrogate": round(s_slope, 2), "zipf_r2_surrogate": round(s_r2, 3),
        "top_freq": [(w, c) for w, c in top],
        "finding": (
            "O léxico de nomes atestados segue Zipf com inclinação %.2f e R²=%.3f (ajuste lei-de-potência), sobre %d "
            "nomes distintos; o surrogate Markov-3 atesta só %.0f nomes (R²=%.3f). %s" % (
                rslope, rr2, len(real), s_types, s_r2,
                ("CONFIRMADO: a distribuição de frequência é linguística (Zipf) e o surrogate mal sustenta um léxico - "
                 "a estrutura de frequência dos nomes é real."
                 if rr2 >= 0.9 and len(real) > s_types * 2 else
                 "fraco: a distribuição não é claramente mais Zipfiana que o surrogate."))),
    }
    load.save_result("128_zipf", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("real: %d nomes, Zipf slope %.2f, R²=%.3f | surrogate: %.0f nomes, R²=%.3f" % (
        r["distinct_names_real"], r["zipf_slope_real"], r["zipf_r2_real"],
        r["distinct_names_surrogate"], r["zipf_r2_surrogate"]))
    print("mais frequentes:", r["top_freq"][:10])
