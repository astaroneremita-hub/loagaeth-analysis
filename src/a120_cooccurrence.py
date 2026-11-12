"""
120 - Which names TRAVEL TOGETHER across the sheets? Distributional co-occurrence network.

a118 gave a shared lexicon; a119 killed fixed seats. Next distributional question: do names cluster by which sheets
they appear in - do some names always co-occur (a family that travels together) while others are complementary (one
where the other is absent)? We build the name x table incidence matrix (restricted to names with variable incidence,
5..31 of 36 tables, so the ubiquitous and the ultra-rare don't swamp it), take phi-correlations between every pair,
and test the strongest against a null that permutes each name's table membership. Positive pairs = families; strong
negative pairs = complementary distributions (candidate opposing houses).
"""
import json
import random
import statistics

import load
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
    out = []
    for r in range(R):
        out.append(g[r])
    for c in range(R):
        out.append("".join(g[r][c] for r in range(R)))
    for s in range(R):
        out.append("".join(g[s + k][k] for k in range(R - s)))
        if s:
            out.append("".join(g[k][s + k] for k in range(R - s)))
    return out


def phi(a, b):
    n = len(a)
    s1 = sum(a); s2 = sum(b)
    both = sum(1 for i in range(n) if a[i] and b[i])
    num = both * n - s1 * s2
    den = (s1 * (n - s1) * s2 * (n - s2)) ** 0.5
    return num / den if den else 0.0


def run():
    book = base_book()
    grids = square_grids(book)
    T = len(grids)
    texts = ["\n".join(lines(g)) for g in grids]
    rtexts = ["\n".join(l[::-1] for l in lines(g)) for g in grids]
    names = json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))

    inc = {}
    for w in names:
        v = [1 if (w in texts[i] or w in rtexts[i]) else 0 for i in range(T)]
        if 5 <= sum(v) <= T - 5:
            inc[w] = v
    ns = list(inc)

    pairs = []
    for i in range(len(ns)):
        for j in range(i + 1, len(ns)):
            p = phi(inc[ns[i]], inc[ns[j]])
            pairs.append((p, ns[i], ns[j]))
    pairs.sort(reverse=True)

    # null: permute each name's vector, recompute max |phi|
    rng = random.Random(120)
    null_max = []
    for _ in range(100):
        perm = {w: random.sample(v, len(v)) for w, v in inc.items()}
        mx = 0
        for i in range(len(ns)):
            for j in range(i + 1, len(ns)):
                mx = max(mx, abs(phi(perm[ns[i]], perm[ns[j]])))
        null_max.append(mx)
    thr = statistics.mean(null_max)

    pos = [(round(p, 2), a, b) for p, a, b in pairs if p > thr][:15]
    neg = [(round(p, 2), a, b) for p, a, b in sorted(pairs)[:15] if p < -thr]

    res = {"names_variable": len(ns), "tables": T, "null_max_phi_mean": round(thr, 2),
           "families_sample": pos, "complementary_sample": neg,
           "finding": (
               "%d nomes têm incidência variável entre folhas. Pares que VIAJAM JUNTOS (phi acima do null %.2f): %s. "
               "Pares COMPLEMENTARES (um onde o outro falta): %s. %s" % (
                   len(ns), thr,
                   ", ".join("%s+%s" % (a, b) for _, a, b in pos[:5]) or "nenhum forte",
                   ", ".join("%s|%s" % (a, b) for _, a, b in neg[:5]) or "nenhum forte",
                   ("Há estrutura distribucional: nomes se agrupam por folha." if pos or neg
                    else "Sem co-ocorrência acima do acaso: a presença de cada nome é independente."))),
           }
    load.save_result("120_cooccurrence", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("FAMÍLIAS (viajam juntas) - phi | nomes:")
    for p, a, b in r["families_sample"][:10]:
        print("  %+.2f  %s + %s" % (p, a, b))
    print("\nCOMPLEMENTARES (um exclui o outro):")
    for p, a, b in r["complementary_sample"][:10]:
        print("  %+.2f  %s | %s" % (p, a, b))
