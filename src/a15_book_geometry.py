"""
15 - The physical geometry of the book: three formats, and which way the language runs.

Findings reproduced here:
  A) Format per table, from the row-length profile of each side:
       full     - 49 rows of 49 letters (tables 2-28)
       diamond  - row lengths 1,3,5..49..5,3,1 (1201 cells) on one side and 2,4..48,48..4,2
                  (1200 cells) on the other (tables 29-48). 1201 + 1200 = 2401 = 49x49.
     Those are exactly the two colours of a chessboard on a 49x49 grid, each written along the
     anti-diagonals (the paper turned 45 degrees). Both sides together = one 49x49 table.
  B) Which way does the language run in the diamond tables? We rebuild the 49x49 grid (side b
     on the even anti-diagonals r+c=2u, side a on the odd ones) and compare reading along the
     diamond rows (= diagonals) vs the rebuilt horizontal and vertical rows.
  C) Tables 26-28 (the last full tables): is there any sequential structure at all?
     Conditional entropy vs a letter-shuffle of the same table; doubled-letter rate.
  D) The no-doubled-letter rule: adjacent identical letters in each kind of text vs chance.
  E) Name density per table, normalised by length (the diamond tables hold half the letters
     per side, so raw per-table counts must not be compared across the two formats).

Data: data/loagaeth_tables.json; engine/data/chamadas.json for the Calls.
"""
import json
import math
import os
import random
from collections import Counter

import load

HERE = os.path.dirname(os.path.abspath(__file__))
CALLS = os.path.join(os.path.dirname(HERE), "engine", "data", "chamadas.json")


def side_rows(key):
    return [load.letters(r) for r in load.leaves().get(key, [])]


def hcond(s):
    bi = Counter(zip(s, s[1:]))
    ctx = Counter(s[:-1])
    n = sum(bi.values()) or 1
    return -sum(c / n * math.log2(c / ctx[a]) for (a, b), c in bi.items())


def doubled(lines):
    n = sum(max(0, len(l) - 1) for l in lines) or 1
    return sum(sum(a == b for a, b in zip(l, l[1:])) for l in lines) / n


def shape(rows):
    L = [len(r) for r in rows if r]
    if not L:
        return "missing"
    if len(L) >= 45 and all(x >= 45 for x in L):
        return "full"
    odd = [2 * min(i, len(L) - 1 - i) + 1 for i in range(len(L))]
    even = [2 * min(i, len(L) - 1 - i) + 2 for i in range(len(L))]
    if L == odd:
        return "diamond-odd"
    if L == even:
        return "diamond-even"
    return "other"


def rebuild(t):
    sides = {s: side_rows(f"{t}{s}") for s in "ab"}
    odd = next((s for s in "ab" if shape(sides[s]) == "diamond-odd"), None)
    even = next((s for s in "ab" if shape(sides[s]) == "diamond-even"), None)
    if not odd or not even:
        return None
    G = [[None] * 49 for _ in range(49)]
    for u, row in enumerate(sides[odd]):
        cells = [(r, 2 * u - r) for r in range(49) if 0 <= 2 * u - r < 49]
        if len(cells) != len(row):
            return None
        for (r, c), ch in zip(cells, row):
            G[r][c] = ch
    for u, row in enumerate(sides[even]):
        cells = [(r, 2 * u + 1 - r) for r in range(49) if 0 <= 2 * u + 1 - r < 49]
        if len(cells) != len(row):
            return None
        for (r, c), ch in zip(cells, row):
            G[r][c] = ch
    return G


def run():
    rng = random.Random(15)
    lv = load.leaves()
    tables = sorted({int(k[:-1]) for k in lv if k[:-1].isdigit()})

    # A) formats
    fmt = {}
    for t in tables:
        if t == 1:
            fmt[t] = "word-spaced (prophecy)"
            continue
        shapes = sorted(shape(side_rows(f"{t}{s}")) for s in "ab")
        if shapes == ["full", "full"]:
            fmt[t] = "full"
        elif shapes == ["diamond-even", "diamond-odd"]:
            fmt[t] = "diamond pair"
        else:
            fmt[t] = "/".join(shapes)

    # reference name inventory from the full tables 2-25
    full_txt = "".join("".join(side_rows(f"{t}{s}")) for t in range(2, 26) for s in "ab")
    rec = {g for g, f in Counter(full_txt[i:i + 6] for i in range(len(full_txt) - 5)).items() if f >= 5}

    def density(lines):
        tot = hit = 0
        for l in lines:
            for i in range(len(l) - 5):
                tot += 1
                hit += l[i:i + 6] in rec
        return hit / tot if tot else 0.0

    # B) direction in the diamond tables
    diag = [r for t in tables if fmt[t] == "diamond pair" for s in "ab" for r in side_rows(f"{t}{s}")]
    H, V, rebuilt = [], [], 0
    for t in tables:
        if fmt[t] != "diamond pair":
            continue
        G = rebuild(t)
        if G is None:
            continue
        rebuilt += 1
        H += ["".join(ch for ch in G[r] if ch) for r in range(49)]
        V += ["".join(G[r][c] for r in range(49) if G[r][c]) for c in range(49)]
    ref = [r for t in range(2, 26) for s in "ab" for r in side_rows(f"{t}{s}")]
    direction = {
        "diamond_rows_as_written": {"name_density": round(density(diag), 3), "H_cond": round(hcond("".join(diag)), 3), "doubled": round(doubled(diag), 4)},
        "rebuilt_horizontal": {"name_density": round(density(H), 3), "H_cond": round(hcond("".join(H)), 3), "doubled": round(doubled(H), 4)},
        "rebuilt_vertical": {"name_density": round(density(V), 3), "H_cond": round(hcond("".join(V)), 3), "doubled": round(doubled(V), 4)},
        "reference_full_tables_2_25": {"name_density": round(density(ref), 3), "H_cond": round(hcond("".join(ref)), 3), "doubled": round(doubled(ref), 4)},
        "tables_rebuilt": rebuilt,
    }

    # C) tables 26-28
    void = {}
    for t in (26, 27, 28):
        s = "".join("".join(side_rows(f"{t}{x}")) for x in "ab")
        sh = list(s)
        rng.shuffle(sh)
        void[t] = {"H_cond": round(hcond(s), 3), "H_cond_shuffled": round(hcond("".join(sh)), 3),
                   "doubled": round(doubled([s]), 4), "name_density": round(density([s]), 3)}

    # D) doubled-letter rule
    l1 = [load.letters(w) for k in ("1a", "1b") for r in lv.get(k, []) for w in r.split()]
    try:
        C = json.load(open(CALLS, encoding="utf-8"))["chamadas"]
        cw = [load.letters(p.get("enoquiano", "")) for c in C for p in c.get("palavras", []) if isinstance(p, dict)]
    except Exception:
        cw = []
    f = Counter(full_txt)
    n = len(full_txt)
    rule = {
        "full_tables_2_25": round(doubled(ref), 4),
        "diamond_tables_29_48": round(doubled(diag), 4),
        "tables_26_28": round(doubled([r for t in (26, 27, 28) for s in "ab" for r in side_rows(f"{t}{s}")]), 4),
        "leaf1_words": round(doubled(l1), 4),
        "calls_words": round(doubled(cw), 4) if cw else None,
        "chance_from_letter_freq": round(sum((v / n) ** 2 for v in f.values()), 4),
    }

    # E) normalised name density per table
    per_table = {}
    for t in tables:
        if t == 1:
            continue
        lines = [r for s in "ab" for r in side_rows(f"{t}{s}")]
        per_table[t] = {"format": fmt[t], "letters": sum(len(l) for l in lines),
                        "name_density": round(density(lines), 3)}

    res = {
        "A_formats": fmt,
        "B_text_direction_in_diamond_tables": direction,
        "C_tables_26_28": void,
        "D_no_doubled_letters": rule,
        "E_per_table": per_table,
        "conclusion": ("Three formats: word-spaced prophecy (table 1), full 49x49 grids written in rows "
                       "(2-28), and 49x49 grids split into the two chessboard colours, each written as a "
                       "diamond along the diagonals (29-48). In the diamond tables the language runs along "
                       "the diagonals; the rebuilt square's rows are noise. Tables 26-28 show no sequential "
                       "structure at all and break the no-doubled-letter rule. Raw per-table counts must be "
                       "normalised: the diamond tables hold half the letters per side."),
    }
    load.save_result("15_book_geometry", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
