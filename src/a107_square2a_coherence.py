"""
107 - Is table 2a's dense cluster of long Call vocabulary real, or chance in a dense field?

The flowing 'translation' of 2a is seductive, but most of it rests on 2-letter glosses (OL, AR, LA...) that
saturate any letter grid. The honest signal is the LONG distinct Call words (>=4 letters: MAD, SAPAH, DORPHA,
VRAN, LANSH, GOHO...). We count how many distinct Call words of length>=4 appear in 2a (straight rows+cols and both
diagonals, forward+reversed) and compare to Markov-3 surrogate grids of the same letter statistics. If 2a holds far
more long Call vocabulary than the surrogate, the cluster is real; if not, it is reading-into-noise.
"""
import json
import random
import unicodedata

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book


def deaccent(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def lines_of(grid):
    R = len(grid)
    out = []
    for r in range(R):
        out.append("".join(grid[r]))
    for c in range(R):
        out.append("".join(grid[r][c] for r in range(R)))
    # diagonals both ways
    for s in range(R):
        out.append("".join(grid[s + k][k] for k in range(R - s)))
        if s:
            out.append("".join(grid[k][s + k] for k in range(R - s)))
        out.append("".join(grid[s + k][R - 1 - k] for k in range(R - s)))
        if s:
            out.append("".join(grid[k][R - 1 - s - k] for k in range(R - s)))
    return out


def count_long(grid, vocab):
    text = "\n".join(lines_of(grid))
    rtext = "\n".join(l[::-1] for l in lines_of(grid))
    hits = set()
    for w in vocab:
        if w in text or w in rtext:
            hits.add(w)
    return hits


def flat(grid):
    return "".join("".join(row) for row in grid)


def surrogate_grid(grid, rng):
    R = len(grid)
    stream = markov3(flat(grid), rng)
    s = "".join(stream)
    # pad/truncate to R*R, refill row-major
    s = (s * ((R * R) // max(1, len(s)) + 1))[:R * R]
    return [list(s[i * R:(i + 1) * R]) for i in range(R)]


def run():
    lex = json.load(open(load.ROOT + "/viz/call_lexicon.json", encoding="utf-8"))
    vocab = {deaccent(w).upper() for w in lex if len(deaccent(w)) >= 4}

    book = base_book()
    # table 2a
    key = "2a" if "2a" in book else [k for k in book if k.startswith("2")][0]
    rows = [r for r in book[key] if r]
    grid = [list(r) for r in rows]
    R = len(grid)
    grid = [row[:R] for row in grid][:R]

    real = count_long(grid, vocab)

    surr_counts = []
    surr_samples = []
    for i in range(20):
        g = surrogate_grid(grid, random.Random(1070 + i))
        h = count_long(g, vocab)
        surr_counts.append(len(h))
        if i == 0:
            surr_samples = sorted(h)[:10]
    mean = sum(surr_counts) / len(surr_counts)
    mx = max(surr_counts)
    # z-ish
    var = sum((c - mean) ** 2 for c in surr_counts) / len(surr_counts)
    sd = var ** 0.5
    z = (len(real) - mean) / sd if sd else float("inf")

    verdict = ("CONFIRMADO: a 2a concentra MUITO mais vocabulário longo das Chamadas que o acaso — %d palavras >=4 "
               "letras reais vs media %.1f (max %d) em 20 surrogates Markov-3, z=%.1f. O agrupamento de vocábulo da "
               "1a/2a Chamada na tabela 2a é sinal real, não leitura-no-ruído." % (len(real), mean, mx, z)) \
        if len(real) > mx and z >= 3 else \
        ("fraco: a 2a tem %d palavras longas reais vs media %.1f (max %d) surrogate, z=%.1f — nao se destaca o "
         "bastante do acaso." % (len(real), mean, mx, z))

    res = {
        "table": key,
        "vocab_size_ge4": len(vocab),
        "real_long_words_found": len(real),
        "real_sample": sorted(real)[:30],
        "surrogate_mean": round(mean, 1),
        "surrogate_max": mx,
        "z": round(z, 1),
        "surrogate_sample": surr_samples,
        "finding": verdict,
    }
    load.save_result("107_square2a_coherence", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("reais (>=4) na %s: %d -> %s" % (r["table"], r["real_long_words_found"], ", ".join(r["real_sample"])))
    print("surrogate: media %.1f, max %d, z=%s" % (r["surrogate_mean"], r["surrogate_max"], r["z"]))
    print("surrogate exemplo achou:", ", ".join(r["surrogate_sample"]))
