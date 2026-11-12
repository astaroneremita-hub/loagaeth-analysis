"""
108 - THE decisive test: does table 2a reproduce a real Call's WORD ORDER, or just its vocabulary?

Presence already fell to the null (a107): a random grid holds as many Call words as 2a. What a surrogate CANNOT
fake is ORDER - Dee's Calls have a fixed word sequence (Sloane 3191, engine/data/chamadas.json). So: for each Call,
take the distinctive words (>=4 letters) it shares with 2a, read them off 2a in natural reading order (row-major,
first occurrence), and measure Kendall tau against their canonical position in that Call. A real encoding shows a
strong positive tau on at least one Call; noise shows tau ~ 0. Null: shuffle 2a's reading positions and recompute,
1000x, to get a p-value per Call and overall.
"""
import json
import random
import unicodedata

import load
from a22_robustness_and_depth import base_book


def deaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def kendall_tau(order_a, order_b):
    """order_a, order_b: lists of the same items; tau over their rank agreement."""
    n = len(order_a)
    if n < 3:
        return None
    ra = {w: i for i, w in enumerate(order_a)}
    rb = {w: i for i, w in enumerate(order_b)}
    items = list(order_a)
    conc = disc = 0
    for i in range(n):
        for j in range(i + 1, n):
            wi, wj = items[i], items[j]
            sa = ra[wi] - ra[wj]
            sb = rb[wi] - rb[wj]
            if sa * sb > 0:
                conc += 1
            elif sa * sb < 0:
                disc += 1
    tot = conc + disc
    return (conc - disc) / tot if tot else None


def reading_positions(grid):
    """first row-major occurrence index of each contiguous substring start; return text + a finder."""
    R = len(grid)
    rows = ["".join(grid[r]) for r in range(R)]
    full = "".join(rows)  # row-major reading order

    def first_pos(w):
        p = full.find(w)
        return p if p >= 0 else None
    return first_pos


def run():
    cham = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    calls = []
    for c in cham:
        seq = [deaccent(w["chave"]) for w in c["palavras"]]
        calls.append({"num": c["numero"], "seq": seq})

    book = base_book()
    key = "2a" if "2a" in book else [k for k in book if k.startswith("2")][0]
    grid = [list(r) for r in book[key] if r]
    R = len(grid)
    grid = [row[:R] for row in grid][:R]
    first_pos = reading_positions(grid)

    rng = random.Random(108)
    out = []
    for c in calls:
        # distinctive words of this call, >=4 letters, that appear in 2a
        uniq = []
        seen = set()
        for w in c["seq"]:
            if len(w) >= 4 and w not in seen:
                seen.add(w)
                uniq.append(w)
        present = [(w, first_pos(w)) for w in uniq]
        present = [(w, p) for w, p in present if p is not None]
        if len(present) < 4:
            continue
        # canonical order = order in uniq (already call order); reading order = sort by pos
        canon = [w for w, _ in present]
        read_order = [w for w, _ in sorted(present, key=lambda x: x[1])]
        tau = kendall_tau(canon, read_order)
        if tau is None:
            continue
        # null: random reading positions
        null_ge = 0
        NT = 1000
        for _ in range(NT):
            perm = read_order[:]
            rng.shuffle(perm)
            t = kendall_tau(canon, perm)
            if t is not None and abs(t) >= abs(tau):
                null_ge += 1
        p = (null_ge + 1) / (NT + 1)
        out.append({"call": c["num"], "n_words": len(present), "tau": round(tau, 3),
                    "p": round(p, 4), "words": canon})

    out.sort(key=lambda x: x["p"])
    best = out[0] if out else None
    sig = [o for o in out if o["p"] < 0.05]
    verdict = ("CONFIRMADO: a 2a reproduz a ORDEM de palavras de pelo menos uma Chamada acima do acaso — "
               "Chamada %d, tau=%.2f, p=%.4f sobre %d palavras. Surrogate nao fabrica ordem; isto sim e sinal." % (
                   best["call"], best["tau"], best["p"], best["n_words"]) if sig else
               ("sem ordem: nenhuma Chamada tem a sua ordem de palavras reproduzida na 2a acima do acaso "
                "(melhor p=%.3f). Confirma: a 2a tem o vocabulario, nao a sintaxe das Chamadas - e salada." % (
                    best["p"] if best else 1.0)))
    res = {"table": key, "calls_tested": len(out), "significant": len(sig),
           "best": best, "all": out, "finding": verdict}
    load.save_result("108_call_order", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("Chamada | n palavras | tau | p")
    for o in r["all"][:12]:
        print("  %2d      |   %2d       | %+.2f | %.4f  %s" % (
            o["call"], o["n_words"], o["tau"], o["p"], " ".join(o["words"][:6])))
