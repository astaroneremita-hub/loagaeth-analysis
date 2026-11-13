"""
a145 - Deep Call<->leaf link: does each Call's vocabulary concentrate in the LEAF it opens?

Tradition: Call N opens leaf N+1. If that pairing is real at the content level, Call N's distinctive words should be
MORE present in the leaf it opens than in other leaves. For each Call we take its words (>=4 letters, deaccented),
measure how many appear in its opened leaf vs the mean over all other leaves, and aggregate. If opened >> others, the
key-and-lock pairing is lexically real, not just a tradition claim - a genuine structural link between the two systems.
"""
import json
import statistics
import unicodedata

import load
from a22_robustness_and_depth import base_book


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").upper()


def lines(g):
    R = 49
    o = [g[r] for r in range(R)]
    o += ["".join(g[r][c] for r in range(R)) for c in range(R)]
    for s in range(R):
        o.append("".join(g[s + k][k] for k in range(R - s)))
        if s:
            o.append("".join(g[k][s + k] for k in range(R - s)))
    return o


def run():
    book = base_book()
    leaftext = {}
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            t = "\n".join(lines(g))
            leaftext[k] = t + "\n" + t[::-1]

    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    results = []
    for c in calls:
        opened = str(c.get("tabua_que_move_segundo_o_tfr"))
        # the opened leaf panels: both sides a/b
        tgt = [k for k in leaftext if k[:-1] == opened]
        if not tgt:
            continue
        words = sorted({da(w["chave"]) for w in c["palavras"] if len(da(w["chave"])) >= 4})
        if len(words) < 3:
            continue
        def frac_in(k):
            return sum(1 for w in words if w in leaftext[k]) / len(words)
        opened_frac = statistics.mean(frac_in(k) for k in tgt)
        others = [frac_in(k) for k in leaftext if k[:-1] != opened]
        other_frac = statistics.mean(others) if others else 0
        results.append({"call": c["numero"], "opens": opened, "words": len(words),
                        "in_opened": round(opened_frac, 3), "in_others_mean": round(other_frac, 3),
                        "ratio": round(opened_frac / other_frac, 2) if other_frac else None})

    valid = [r for r in results if r["ratio"]]
    mean_opened = statistics.mean(r["in_opened"] for r in valid)
    mean_other = statistics.mean(r["in_others_mean"] for r in valid)
    better = sum(1 for r in valid if r["in_opened"] > r["in_others_mean"])
    res = {
        "calls_tested": len(valid), "mean_in_opened": round(mean_opened, 3),
        "mean_in_others": round(mean_other, 3),
        "calls_opened_higher": better,
        "per_call": results,
        "finding": (
            "Vocabulário de cada Chamada na folha que ela abre vs nas outras folhas: média %.1f%% na aberta vs %.1f%% "
            "nas outras; %d de %d Chamadas têm MAIS vocabulário na própria folha. %s" % (
                mean_opened * 100, mean_other * 100, better, len(valid),
                ("CONFIRMADO: cada Chamada concentra seu vocabulário na folha que abre - o par chave-fechadura é real "
                 "no conteúdo, não só na tradição." if mean_opened > mean_other * 1.15 and better > len(valid) * 0.6
                 else "sem concentração: o vocabulário da Chamada não prefere a folha que abre - o par é tradicional/"
                      "estrutural, não lexical."))),
    }
    load.save_result("145_call_leaf_align", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("Chamada | abre folha | palavras | na aberta | nas outras | razão")
    for x in r["per_call"][:20]:
        print("  %2s -> %-4s  %2d palavras  %.2f vs %.2f  %sx" % (
            x["call"], x["opens"], x["words"], x["in_opened"], x["in_others_mean"], x["ratio"]))
