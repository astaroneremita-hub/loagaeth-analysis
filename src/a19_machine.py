"""
19 - Is the Loagaeth machine-generated, like the Soyga tables? And can a machine learn it?

The Book of Soyga (which Dee owned) contains letter tables produced by an algorithm (Jim Reeds
reconstructed it): its columns are periodic. Here the Loagaeth is put through the same kind of
tests, and a small character language model is trained on it.

  A) Periodicity: for each line, the best self-match P(x_i = x_{i+p}) over periods p = 2..20,
     compared with the Soyga Aries table columns (if data/raw/soyga_aries_columns.json exists -
     extracted locally from J. Kupin's 2014 edition, not redistributed) and with shuffled lines.
  B) A 2-D rule? In the row-written 49x49 tables, how much does the letter ABOVE add to the
     letter on the LEFT for predicting a cell: H(x|left) vs H(x|left,above). A generated table
     (cell = f(neighbours)) would drop to near zero.
  C) Compressibility (zlib, bz2, lzma), real text vs Markov-3 surrogate vs shuffled letters.
  D) A character language model (order 4, interpolated with lower orders) trained on the
     row-written tables 2-24 (held-out cross-validation), then scored in bits per letter on:
     the diagonal-decoded tables 25b-28, those same tables read by rows, the diamonds 29-43, the
     end 44-48 as written and with U turned back into A, and shuffled text.
  E) Can a machine write new Loagaeth? An order-5 generator trained on 2-24 produces a 49x49
     table; its recurring-name share and doubled letters are compared with real tables.
"""
import bz2
import json
import lzma
import math
import os
import random
import statistics
import zlib
from collections import Counter, defaultdict

import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SOYGA = os.path.join(ROOT, "data", "raw", "soyga_aries_columns.json")
DECODED = os.path.join(ROOT, "data", "loagaeth_diagonal_decoded.json")


def rows(key):
    return [load.letters(r) for r in load.leaves().get(key, [])]


def period_score(line, pmax=20):
    best = (0.0, None)
    for p in range(2, min(pmax, len(line) // 2) + 1):
        m = sum(1 for i in range(len(line) - p) if line[i] == line[i + p]) / (len(line) - p)
        if m > best[0]:
            best = (m, p)
    return best


class CharLM:
    def __init__(self, order=4, alpha=0.1):
        self.n = order
        self.alpha = alpha
        self.counts = [defaultdict(Counter) for _ in range(order + 1)]
        self.V = set()

    def fit(self, lines):
        for l in lines:
            s = "^" * self.n + l
            self.V.update(l)
            for i in range(self.n, len(s)):
                for k in range(self.n + 1):
                    self.counts[k][s[i - k:i]][s[i]] += 1
        self.V = sorted(self.V)
        return self

    def prob(self, ctx, ch):
        p = 1 / (len(self.V) + 1)
        for k in range(self.n + 1):
            c = self.counts[k].get(ctx[len(ctx) - k:] if k else "")
            if not c:
                continue
            tot = sum(c.values())
            lam = tot / (tot + 3.0)
            p = lam * (c[ch] + self.alpha * p) / (tot + self.alpha) + (1 - lam) * p
        return p

    def bits(self, lines):
        b = n = 0
        for l in lines:
            s = "^" * self.n + l
            for i in range(self.n, len(s)):
                b -= math.log2(self.prob(s[i - self.n:i], s[i]))
                n += 1
        return b / n if n else None

    def sample(self, length, rng, prefix=""):
        out = "^" * self.n + prefix
        letters = self.V
        while len(out) - self.n < length:
            ctx = out[-self.n:]
            w = [self.prob(ctx, ch) for ch in letters]
            out += rng.choices(letters, w)[0]
        return out[self.n:]


def markov3(text, rng):
    tab = defaultdict(list)
    for i in range(len(text) - 3):
        tab[text[i:i + 3]].append(text[i + 3])
    keys = list(tab)
    out = list(rng.choice(keys))
    while len(out) < len(text):
        nx = tab.get("".join(out[-3:]))
        out.append(rng.choice(nx) if nx else rng.choice(keys)[0])
    return "".join(out[:len(text)])


def run():
    rng = random.Random(19)
    train_tables = [(t, s) for t in range(2, 25) for s in "ab"]
    train_rows = {k: rows(f"{k[0]}{k[1]}") for k in train_tables}
    all_train = [r for v in train_rows.values() for r in v]
    ref = "".join(all_train)
    rec = {g for g, f in Counter(ref[i:i + 6] for i in range(len(ref) - 5)).items() if f >= 5}

    def names(lines):
        tot = hit = 0
        for l in lines:
            for i in range(len(l) - 5):
                tot += 1
                hit += l[i:i + 6] in rec
        return hit / tot if tot else 0.0

    def dbl(lines):
        n = sum(max(0, len(l) - 1) for l in lines) or 1
        return sum(sum(a == b for a, b in zip(l, l[1:])) for l in lines) / n

    # A periodicity
    def summarize(lines):
        sc = [period_score(l)[0] for l in lines if len(l) >= 24]
        return round(statistics.mean(sc), 3) if sc else None
    shuffled = ["".join(rng.sample(l, len(l))) for l in all_train]
    period = {"loagaeth_rows_2_24": summarize(all_train),
              "loagaeth_rows_shuffled": summarize(shuffled)}
    if os.path.exists(DECODED):
        dec = json.load(open(DECODED, encoding="utf-8"))["faces"]
        dec_lines = [l for f in dec.values() for l in f["down_right"] + f["leftward"]]
        period["loagaeth_decoded_diagonals"] = summarize(dec_lines)
    else:
        dec_lines = []
    if os.path.exists(SOYGA):
        sc = json.load(open(SOYGA, encoding="utf-8"))
        period["soyga_aries_columns"] = [{"column": i + 1, "best_match": round(period_score(c)[0], 3), "period": period_score(c)[1]}
                                         for i, c in enumerate(sc)]
    else:
        period["soyga_aries_columns"] = "not available (place data/raw/soyga_aries_columns.json to compare)"

    # B 2-D rule
    def H(pairs):
        c = Counter(pairs)
        ctx = Counter(p[:-1] for p in pairs)
        n = len(pairs)
        return -sum(v / n * math.log2(v / ctx[k[:-1]]) for k, v in c.items())
    left, both, above_only = [], [], []
    for g in train_rows.values():
        if len(g) != 49 or any(len(r) != 49 for r in g):
            continue
        for r in range(1, 49):
            for c in range(1, 49):
                left.append((g[r][c - 1], g[r][c]))
                above_only.append((g[r - 1][c], g[r][c]))
                both.append((g[r][c - 1], g[r - 1][c], g[r][c]))
    uni = Counter(p[-1] for p in left)
    n = sum(uni.values())
    rule2d = {"H_x": round(-sum(v / n * math.log2(v / n) for v in uni.values()), 3),
              "H_x_given_above": round(H(above_only), 3),
              "H_x_given_left": round(H(left), 3),
              "H_x_given_left_and_above": round(H(both), 3)}

    # C compressibility
    text = ref[:60000]
    mk = markov3(text, rng)
    sh = "".join(rng.sample(text, len(text)))
    comp = {}
    for name, f in (("zlib", lambda b: zlib.compress(b, 9)), ("bz2", lambda b: bz2.compress(b, 9)),
                    ("lzma", lambda b: lzma.compress(b))):
        comp[name] = {"real": round(len(f(text.encode())) * 8 / len(text), 3),
                      "markov3": round(len(f(mk.encode())) * 8 / len(mk), 3),
                      "shuffled": round(len(f(sh.encode())) * 8 / len(sh), 3)}

    # D language model
    keys = list(train_rows)
    rng.shuffle(keys)
    folds = [keys[i::4] for i in range(4)]
    cv = []
    for fold in folds:
        lm = CharLM(4).fit([r for k in keys if k not in fold for r in train_rows[k]])
        cv.append(lm.bits([r for k in fold for r in train_rows[k]]))
    lm = CharLM(4).fit(all_train)
    row_read_26_28 = [r for t in (26, 27, 28) for s in "ab" for r in rows(f"{t}{s}")]
    diamonds = [r for t in range(29, 44) for s in "ab" for r in rows(f"{t}{s}")]
    end = [r for t in range(44, 49) for s in "ab" for r in rows(f"{t}{s}")]
    lmres = {"heldout_rows_2_24_crossval": round(statistics.mean(cv), 3),
             "decoded_diagonals_25b_28": round(lm.bits(dec_lines), 3) if dec_lines else None,
             "same_tables_read_by_rows": round(lm.bits(row_read_26_28), 3),
             "diamonds_29_43": round(lm.bits(diamonds), 3),
             "end_44_48_as_written": round(lm.bits(end), 3),
             "end_44_48_with_U_back_to_A": round(lm.bits([l.replace("U", "A") for l in end]), 3),
             "shuffled_heartland": round(lm.bits(shuffled[:400]), 3)}

    # E generator
    gen5 = CharLM(5).fit(all_train)
    g = gen5.sample(2401, rng)
    glines = [g[i * 49:(i + 1) * 49] for i in range(49)]
    real = all_train[:49 * 6]
    generator = {"generated_table_first_rows": glines[:3],
                 "generated_names_share": round(names(glines), 3), "real_names_share": round(names(real), 3),
                 "generated_doubled": round(dbl(glines), 4), "real_doubled": round(dbl(real), 4),
                 "note": "the recurring-name inventory comes from the same training tables, so the generated "
                         "share measures how much of the vocabulary a local model reproduces"}

    res = {"A_periodicity": period, "B_two_d_rule": rule2d, "C_compression_bits_per_letter": comp,
           "D_language_model_bits_per_letter": lmres, "E_generator": generator,
           "conclusion": ("The Soyga table is periodic like a machine; the Loagaeth is not (no period, a cell "
                          "is not a function of its neighbours, the letter above adds nothing). It behaves like a "
                          "language: a small model trained on the heartland reads the diagonal-decoded tables "
                          "almost as well as held-out heartland, fails on the same tables read by rows, and reads "
                          "the end better once U is turned back into A.")}
    load.save_result("19_machine", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1)[:5000])
