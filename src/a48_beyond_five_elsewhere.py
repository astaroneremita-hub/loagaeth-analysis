"""
48 - The limit of five letters in the rest of the book.

Module a47 found no memory beyond five letters of context in the row-written tables (2-24). The same
test on the other formats, each read along its own road (a15, a37): the chessboard leaves 25b-28b,
the diamonds 29-40, the diamonds 41-48 (the U register), and leaf 1. For each group the Bible is cut
into lines of exactly the same lengths, so the positive control has the same size and shape.

Also the two order tests of a44 (bits lost when the lines of a side are shuffled; echo of 5-letter
strings one to four lines further on), where "line" is a diagonal of the board or of the diamond.

Warning built into the echo test: on a diagonal layout neighbouring lines have similar lengths, and
shuffling the lines pairs long with short, which lowers the shuffled count by itself. A text with no
memory at all then shows a ratio of about 1.4. So the echo is reported as the ratio book / shuffled
against the same ratio in Markov-3 surrogates of the same shape.
"""
import json
import random
import statistics

import load
from a22_robustness_and_depth import base_book, tnum
from a39_long_repeats import surrogate3
from a43_recency import echo
from a44_positive_control import T2, kjv_words
from a47_templates import beyond_five

GROUPS = [("leaf 1", lambda k: tnum(k) == 1),
          ("tables 2-24 (rows)", lambda k: 2 <= tnum(k) <= 24),
          ("leaves 25b-28b (chessboard)", lambda k: (tnum(k) == 25 and k.endswith("b")) or 26 <= tnum(k) <= 28),
          ("diamonds 29-40", lambda k: 29 <= tnum(k) <= 40),
          ("diamonds 41-48 (U register)", lambda k: 41 <= tnum(k) <= 48)]


def shaped_like(sides, stream):
    out, i = [], 0
    for ls in sides:
        new = []
        for r in ls:
            new.append(stream[i:i + len(r)])
            i += len(r)
        out.append(new)
    return out


def echo_ratio(sides, rng, reps=30):
    def stat(fs):
        a = b = 0
        for ls in fs:
            for x, y in echo(ls, 4, 5):
                a += x
                b += y
        return a / max(1, b)
    real = stat(sides)
    nul = []
    for _ in range(reps):
        sh = []
        for ls in sides:
            t = ls[:]
            rng.shuffle(t)
            sh.append(t)
        nul.append(stat(sh))
    return real / (statistics.mean(nul) or 1e-9)


def run():
    rng = random.Random(48)
    book = base_book()
    keys = sorted(book, key=lambda k: (tnum(k), k))
    res = {}
    for name, sel in GROUPS:
        sides = [[r for r in book[k] if len(r) >= 1] for k in keys if sel(k)]
        sides = [s for s in sides if s]
        n = sum(len(r) for ls in sides for r in ls)
        bible = shaped_like(sides, "".join(kjv_words(n + 100)))
        row = {"sides": len(sides), "letters": n, "beyond_five": {}}
        for k in (6, 7, 8, 10):
            a, b = beyond_five(sides, k, rng), beyond_five(bible, k, rng)
            row["beyond_five"][k] = {"occurrences": a["occurrences"], "z": a["z"], "bible_same_shape_z": b["z"]}
        if len(sides) >= 4:
            t2, b2 = T2(sides, rng), T2(bible, rng)
            flat = [r for ls in sides for r in ls]
            r = echo_ratio(sides, rng)
            sur = [echo_ratio(shaped_like(sides, "".join(surrogate3(flat, rng))), rng) for _ in range(8)]
            row["order_of_lines"] = {"bits_lost": t2["lost_by_shuffling"], "z": t2["z"], "bible_bits_lost": b2["lost_by_shuffling"], "bible_z": b2["z"]}
            row["echo_1_to_4_lines"] = {"ratio_book_to_shuffled": round(r, 3), "same_ratio_in_surrogates": round(statistics.mean(sur), 3),
                                        "z": round((r - statistics.mean(sur)) / (statistics.pstdev(sur) or 1e-9), 1),
                                        "bible_ratio": round(echo_ratio(bible, rng), 3)}
        res[name] = row
    load.save_result("48_beyond_five_elsewhere", res)
    return res


if __name__ == "__main__":
    for name, row in run().items():
        print(name, row["sides"], row["letters"])
        for k, v in row["beyond_five"].items():
            print("    back", k, v)
        for t in ("order_of_lines", "echo_1_to_4_lines"):
            if t in row:
                print("   ", t, row[t])
