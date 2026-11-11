"""
44 - Positive control: can our tests see sentences where sentences exist?

Modules a39-a43 found no sign of sentences in the tables. That only means something if the same
tests, run blind on a text that does have sentences, report them. Every text below is treated the
way the tables reach us: letters only, no spaces, cut into lines of 49 and sides of 49 lines.

  texts with syntax:    King James Bible (opening 177,000 letters; data/raw/kjv.txt, fetched from
                        Project Gutenberg, not redistributed); the 19 Calls in the angelic language
  texts without syntax: the same Bible with the order of its words shuffled inside each side;
                        a Markov-3 surrogate of the tables
  the tables:           the row-written tables 2-24

Three blind tests, identical for all:
  T1 next unit. Units = the 60 commonest strings of 4-7 letters of the text itself. Is the next unit
     in a line (at least 3 letters further on) tied to the previous one more than when units are
     shuffled inside each side? (Touching units are reported apart: they also score in surrogates.)
  T2 order of lines. A letter model with a cache of the last 1000 letters: how many bits per letter
     are lost when the lines of each side are shuffled?
  T3 echo. 5-letter strings recurring 1-4 lines below, against lines shuffled.

Small texts (the Calls: about 5,000 letters) are cut into sides of 12 lines, and the Bible and the
tables are also run at that size, to show what the tests can see with so little.
"""
import json
import os
import random
import re
import statistics
from collections import Counter, defaultdict

import load
from a22_robustness_and_depth import base_book, tnum
from a39_long_repeats import mi, surrogate3, tokens
from a40_formulas import shuffled_faces
from a43_recency import bits_with_cache, echo

KJV = os.path.join(load.DATA, "raw", "kjv.txt")
URL = "https://www.gutenberg.org/cache/epub/10/pg10.txt"


def kjv_words(n_letters):
    if not os.path.exists(KJV):
        import urllib.request
        with urllib.request.urlopen(URL, timeout=60) as r, open(KJV, "wb") as fh:
            fh.write(r.read())
    t = open(KJV, encoding="utf-8", errors="ignore").read()
    t = t[t.find("In the beginning God created"):]
    out, n = [], 0
    for w in re.findall(r"[A-Za-z]+", t):
        out.append(w.upper())
        n += len(w)
        if n >= n_letters:
            break
    return out


def call_stream():
    c = json.load(open(os.path.join(os.path.dirname(load.DATA), "engine", "data", "chamadas.json"), encoding="utf-8"))["chamadas"]
    return [re.sub(r"[^A-Z]", "", w["enoquiano"].upper()) for ch in c for w in ch["palavras"]]


def cut(s, side_lines, width=49):
    lines = [s[i:i + width] for i in range(0, len(s) - width + 1, width)]
    return [lines[i:i + side_lines] for i in range(0, len(lines) - side_lines + 1, side_lines)]


def units(sides, n=60):
    c = Counter()
    for ls in sides:
        for r in ls:
            for k in range(4, 8):
                for i in range(len(r) - k + 1):
                    c[r[i:i + k]] += 1
    out = []
    for s, v in sorted(c.items(), key=lambda x: -x[1] * (len(x[0]) - 2)):
        if not any(s in t or t in s for t in out):
            out.append(s)
        if len(out) == n:
            break
    return sorted(out, key=len, reverse=True)


def T1(sides, rng, reps=200, gap=3):
    """gap: letters that must lie between the two units. With gap 0 two pieces of one word count as a
    pair and any text with word-like chunks scores (surrogates too); gap 3 keeps units apart."""
    names = units(sides)
    by = {i: [tokens(r, names) for r in ls] for i, ls in enumerate(sides)}
    succ = [(a[1], b[1]) for v in by.values() for seq in v for a, b in zip(seq, seq[1:]) if b[0] - a[0] - len(a[1]) >= gap]
    obs = mi(succ)
    nul = []
    for _ in range(reps):
        sh = shuffled_faces(by, rng)
        nul.append(mi([(a[1], b[1]) for v in sh.values() for seq in v for a, b in zip(seq, seq[1:]) if b[0] - a[0] - a[2] >= gap]))
    return {"pairs": len(succ), "bits": round(obs, 3), "shuffled": round(statistics.mean(nul), 3),
            "z": round((obs - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1)}


def T2(sides, rng, reps=12):
    train = [r for ls in sides[0::2] for r in ls]
    static, nstatic = defaultdict(Counter), Counter()
    for r in train:
        s = "^^^" + r
        for i in range(3, len(s)):
            static[s[i - 3:i]][s[i]] += 1
            nstatic[s[i - 3:i]] += 1
    test = sides[1::2]
    real = bits_with_cache(static, nstatic, test, 1000, 4)
    nul = []
    for _ in range(reps):
        sh = []
        for ls in test:
            x = ls[:]
            rng.shuffle(x)
            sh.append(x)
        nul.append(bits_with_cache(static, nstatic, sh, 1000, 4))
    return {"bits_per_letter": round(real, 4), "lines_shuffled": round(statistics.mean(nul), 4),
            "lost_by_shuffling": round(statistics.mean(nul) - real, 4),
            "z": round((statistics.mean(nul) - real) / (statistics.pstdev(nul) or 1e-9), 1)}


def T3(sides, rng, reps=100):
    def stat(fs):
        a = b = 0
        for ls in fs:
            for d, (x, y) in enumerate(echo(ls, 4, 5)):
                a += x
                b += y
        return a / max(1, b)
    real = stat(sides)
    nul = []
    for _ in range(reps):
        sh = []
        for ls in sides:
            x = ls[:]
            rng.shuffle(x)
            sh.append(x)
        nul.append(stat(sh))
    return {"per_1000": round(1000 * real, 2), "lines_shuffled": round(1000 * statistics.mean(nul), 2),
            "z": round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1)}


def battery(sides, rng):
    return {"sides": len(sides), "letters": sum(len(r) for ls in sides for r in ls),
            "T1_next_unit": T1(sides, rng), "T1_touching_units": T1(sides, rng, 100, 0), "T2_order_of_lines": T2(sides, rng), "T3_echo_1_to_4_lines": T3(sides, rng)}


def run():
    rng = random.Random(44)
    book = base_book()
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 2 <= tnum(k) <= 24]
    tables = [[r for r in book[k] if r] for k in keys]
    n = sum(len(r) for ls in tables for r in ls)
    words = kjv_words(n)
    bible = cut("".join(words), 49)
    # words shuffled inside each side: same vocabulary per side, no order
    sh_words, i = [], 0
    per = 49 * 49
    buf, cnt = [], 0
    for w in words:
        buf.append(w)
        cnt += len(w)
        if cnt >= per:
            rng.shuffle(buf)
            sh_words += buf
            buf, cnt = [], 0
    bible_shuf = cut("".join(sh_words), 49)
    flat = [r for ls in tables for r in ls]
    sur = surrogate3(flat, rng)
    surrogate, i = [], 0
    for ls in tables:
        surrogate.append(sur[i:i + len(ls)])
        i += len(ls)
    bsur = surrogate3([r for ls in bible for r in ls], rng)
    bible_sur = [bsur[j:j + 49] for j in range(0, len(bsur) - 48, 49)]
    calls = "".join(call_stream())
    m = len(calls)
    small = lambda s: cut(s[:m], 12)
    res = {"full_size": {"tables_2_24": battery(tables, rng),
                         "bible_english": battery(bible, rng),
                         "bible_words_shuffled": battery(bible_shuf, rng),
                         "markov3_surrogate_of_tables": battery(surrogate, rng),
                         "markov3_surrogate_of_bible": battery(bible_sur, rng)},
           "size_of_the_calls": {"calls_angelic": battery(cut(calls, 12), rng),
                                 "bible_english": battery(small("".join(words)), rng),
                                 "tables_2_24": battery(small("".join(flat)), rng)}}
    load.save_result("44_positive_control", res)
    return res


if __name__ == "__main__":
    r = run()
    for g, v in r.items():
        print(g)
        for name, b in v.items():
            print("  ", name, b["sides"], b["letters"])
            for t in ("T1_next_unit", "T1_touching_units", "T2_order_of_lines", "T3_echo_1_to_4_lines"):
                print("      ", t, b[t])
