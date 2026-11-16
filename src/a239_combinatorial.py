# -*- coding: utf-8 -*-
"""
239 - Tabela combinatória à la Llull/Trithemius: os nomes têm ALFABETOS POSICIONAIS?

Dee conhecia a Ars Magna de Llull (rodas concêntricas de princípios) e a Polygraphia de
Trithemius (tabelas onde cada posição sorteia de um sub-alfabeto fixo). Hipótese nova e
medível: cada POSIÇÃO de um nome do Loagaeth puxa de um sub-alfabeto restrito (uma "roda"
por posição) — assinatura de um gerador de TABELA COMBINATÓRIA — ou é texto livre?

Medida: n-gramas recorrentes de comprimento fixo L (os "nomes"). Para cada posição 1..L,
a entropia da letra naquela posição. Se << entropia global da letra, a posição é restrita.
Null: embaralhar as letras DENTRO de cada nome (preserva composição, destrói a posição).
Completude de Llull: nº de nomes distintos observados vs o produto dos tamanhos de
sub-alfabeto por posição (tabela cheia = enumeração total; subset = seleção).
stdlib only, seed 1583.
"""
import math, random, statistics
from collections import Counter
import load

SEED = 1583


def base_stream():
    return load.dense_stream()


def recurrent_ngrams(L, minfreq):
    s = base_stream()
    c = Counter(s[i:i + L] for i in range(len(s) - L + 1))
    grams = [g for g, f in c.items() if f >= minfreq]
    # dedup: remove um gram se for substring de outro mais frequente (mantém os "nomes" núcleo)
    return grams, c


def entropy(letters):
    c = Counter(letters); n = sum(c.values())
    return -sum(v / n * math.log2(v / n) for v in c.values())


def slot_entropies(grams, L):
    return [entropy([g[i] for g in grams]) for i in range(L)]


def run(L=6, minfreq=8):
    rng = random.Random(SEED)
    grams, counts = recurrent_ngrams(L, minfreq)
    allletters = "".join(grams)
    Hglobal = entropy(allletters)

    real = slot_entropies(grams, L)

    # null: embaralha as letras dentro de cada gram
    def null_once():
        sh = []
        for g in grams:
            l = list(g); rng.shuffle(l); sh.append("".join(l))
        return slot_entropies(sh, L)
    nulls = [null_once() for _ in range(30)]
    null_mean = [round(statistics.mean(n[i] for n in nulls), 3) for i in range(L)]
    null_sd = [statistics.pstdev(n[i] for n in nulls) or 1e-9 for i in range(L)]
    z = [round((real[i] - null_mean[i]) / null_sd[i], 2) for i in range(L)]

    # sub-alfabeto por posição: letras que cobrem 90% da massa
    subalpha = []
    for i in range(L):
        c = Counter(g[i] for g in grams); tot = sum(c.values()); acc = 0; keep = []
        for ltr, f in c.most_common():
            keep.append(ltr); acc += f
            if acc / tot >= 0.90:
                break
        subalpha.append(keep)

    product = 1
    for s in subalpha:
        product *= len(s)
    observed = len(set(grams))

    res = {
        "L": L, "minfreq": minfreq, "distinct_names": observed,
        "global_letter_entropy_bits": round(Hglobal, 3),
        "slot_entropy_real": [round(x, 3) for x in real],
        "slot_entropy_null_shuffled": null_mean,
        "slot_z_vs_shuffle": z,
        "subalphabet_per_slot_90pct": {str(i + 1): "".join(subalpha[i]) for i in range(L)},
        "subalphabet_sizes": [len(s) for s in subalpha],
        "combinatorial_product_90pct": product,
        "fill_ratio_observed_over_product": round(observed / product, 4) if product else None,
    }
    load.save_result("239_combinatorial", res)
    return res


if __name__ == "__main__":
    r = run()
    print("nomes (%d-gramas freq>=%d): %d distintos | entropia global da letra %.3f bits" %
          (r["L"], r["minfreq"], r["distinct_names"], r["global_letter_entropy_bits"]))
    print("entropia por posição (real):   ", r["slot_entropy_real"])
    print("entropia por posição (null emb):", r["slot_entropy_null_shuffled"])
    print("z vs embaralho por posição:    ", r["slot_z_vs_shuffle"])
    print("sub-alfabeto por posição (90%):")
    for k, v in r["subalphabet_per_slot_90pct"].items():
        print("   pos %s: %s" % (k, v))
    print("produto combinatório (90%%): %d | observados: %d | preenchimento: %s" %
          (r["combinatorial_product_90pct"], r["distinct_names"], r["fill_ratio_observed_over_product"]))
