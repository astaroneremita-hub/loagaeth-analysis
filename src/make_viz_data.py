"""Build viz/loagaeth_viz_data.js for the 3D viewer (viz/loagaeth_3d.html).

Reads data/loagaeth_tables.json and data/loagaeth_territories.json and writes a
classic script that sets ``window.LOAGAETH`` so the page works from file://.

Per table side it stores:
  f    format: "square-rows" (2a-25a), "square-diagonal" (25b-28b), "diamond" (29-48)
  rows list of row strings (A-Z only; any other character is stripped)
  occ  occurrences of the master names: [name_index, row, col, length, dr, dc]
       (dr, dc) is the reading step: (0, 1) along a row; (1, 1) down-right and
       (-1, -1) up-left along an r-c diagonal (square-diagonal tables only).
  drp  (square-diagonal only) chessboard parity (r+c) % 2 of the current that
       reads down-right; the other parity reads up-left. Chosen per side as the
       assignment under which the master names occur most often.

Usage:  python src/make_viz_data.py
"""
import json
import os
import random
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "data", "loagaeth_tables.json")
TERR = os.path.join(ROOT, "data", "loagaeth_territories.json")
OUT = os.path.join(ROOT, "viz", "loagaeth_viz_data.js")

NAMES = ["CHASTOR", "ANZACH", "GETH", "NOCHA", "ADNOCHA", "ALGETH", "ACLAX", "CHUSTOR"]
N = 49


def clean(row):
    return re.sub(r"[^A-Z]", "", row.upper())


def table_format(t, side):
    if t <= 24 or (t == 25 and side == "a"):
        return "square-rows"
    if t <= 28:
        return "square-diagonal"
    return "diamond"


def find_all(s, name):
    out, i = [], s.find(name)
    while i != -1:
        out.append(i)
        i = s.find(name, i + 1)
    return out


def row_occurrences(rows):
    occ = []
    for r, s in enumerate(rows):
        for k, name in enumerate(NAMES):
            for c in find_all(s, name):
                occ.append([k, r, c, len(name), 0, 1])
    return occ


def diagonal_cells(rows, d):
    """Cells (r, c) on the r-c = d diagonal, ordered by increasing r."""
    return [(r, r - d) for r in range(N) if 0 <= r - d < N and r < len(rows) and r - d < len(rows[r])]


def diagonal_occurrences(rows):
    best = None
    for drp in (0, 1):
        occ = []
        for d in range(-(N - 1), N):
            cells = diagonal_cells(rows, d)
            if len(cells) < 2:
                continue
            down_right = (d % 2) == drp  # parity of r+c equals parity of r-c
            if not down_right:
                cells = cells[::-1]
            s = "".join(rows[r][c] for r, c in cells)
            step = 1 if down_right else -1
            for k, name in enumerate(NAMES):
                for i in find_all(s, name):
                    r0, c0 = cells[i]
                    occ.append([k, r0, c0, len(name), step, step])
        if best is None or len(occ) > len(best[1]):
            best = (drp, occ)
    return best


NULL_SEED = 1583  # fixed seed for the shuffled ("null") stack


def enc(counts):
    """Encode small non-negative ints (< 75) as one character each (chr(48 + n))."""
    return "".join(chr(48 + n) for n in counts)


def stack_counts(sides_rows):
    """Per-cell counts across sides: letters[L][cell] and names[k][cell] (k = 8 means any name)."""
    letters = {ch: [0] * (N * N) for ch in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
    names = [[0] * (N * N) for _ in range(len(NAMES) + 1)]
    for rows in sides_rows:
        for r, row in enumerate(rows):
            for c, ch in enumerate(row):
                letters[ch][r * N + c] += 1
        per_name = [set() for _ in NAMES]
        for k, r, c, ln, _dr, _dc in row_occurrences(rows):
            for i in range(ln):
                per_name[k].add(r * N + c + i)
        for k, cells in enumerate(per_name):
            for cell in cells:
                names[k][cell] += 1
        for cell in set().union(*per_name):
            names[len(NAMES)][cell] += 1
    letters = {ch: v for ch, v in letters.items() if sum(v)}
    return letters, names


def build_stack(tables):
    """Stack of the clean 49x49 row-written sides (2a-25a) plus a shuffled null stack.

    Clean = 49 rows of exactly 49 letters after stripping non-letters. The null
    shuffles the letters inside each side (fixed seed), keeping each side's
    letter composition but destroying position.
    """
    keys = sorted((k for k, e in tables.items() if e["f"] == "square-rows"
                   and len(e["rows"]) == N and all(len(r) == N for r in e["rows"])),
                  key=lambda k: (int(k[:-1]), k[-1]))
    obs_rows = [tables[k]["rows"] for k in keys]
    rng = random.Random(NULL_SEED)
    null_rows = []
    for rows in obs_rows:
        cells = list("".join(rows))
        rng.shuffle(cells)
        s = "".join(cells)
        null_rows.append([s[i * N:(i + 1) * N] for i in range(N)])
    lo, no = stack_counts(obs_rows)
    ln_, nn = stack_counts(null_rows)
    freq = sorted(lo, key=lambda ch: -sum(lo[ch]))
    excluded = sorted((k for k, e in tables.items() if e["f"] == "square-rows" and k not in keys),
                      key=lambda k: (int(k[:-1]), k[-1]))
    print("stack sides:", len(keys), " excluded (not 49x49 after cleaning):", " ".join(excluded))
    print("letter frequency order in stack:", "".join(freq[:14]))
    return {
        "sides": keys,
        "excluded": excluded,
        "seed": NULL_SEED,
        "freq": "".join(freq),
        "obs": {"letters": {ch: enc(v) for ch, v in lo.items()}, "names": [enc(v) for v in no]},
        "nul": {"letters": {ch: enc(v) for ch, v in ln_.items()}, "names": [enc(v) for v in nn],
                "rows": {k: r for k, r in zip(keys, null_rows)}},
    }


def main():
    with open(SRC, encoding="utf-8") as fh:
        leaves = json.load(fh)["leaves"]
    with open(TERR, encoding="utf-8") as fh:
        terr = json.load(fh)["tables"]

    zones, rulers = {}, {}
    for t in terr:
        z = t.get("zone")
        if t["table"] in (26, 27, 28):
            z = "CHASTOR"  # recent finding: 26-28 belong to the CHASTOR zone
        zones[t["table"]] = z
        rulers[t["table"]] = t.get("local_ruler")

    tables = {}
    counts = {}
    for key, raw in leaves.items():
        t, side = int(key[:-1]), key[-1]
        if t < 2:
            continue  # leaf 1 is word-spaced prose, not a grid
        rows = [clean(r) for r in raw]
        f = table_format(t, side)
        entry = {"t": t, "s": side, "f": f, "rows": rows}
        if f == "square-diagonal":
            drp, occ = diagonal_occurrences(rows)
            entry["drp"] = drp
            entry["occ"] = row_occurrences(rows) + occ
        else:
            entry["occ"] = row_occurrences(rows)
        tables[key] = entry
        counts[key] = len(entry["occ"])

    stack = build_stack(tables)

    data = {
        "stack": stack,
        "meta": {
            "source": "John Dee, Liber Loagaeth (Sloane MS 3189); transcription in data/loagaeth_tables.json",
            "note": "Non A-Z characters stripped; table 49 missing; leaf 1 is prose.",
        },
        "names": NAMES,
        "zones": zones,
        "rulers": rulers,
        "tables": tables,
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    js = "window.LOAGAETH=" + json.dumps(data, separators=(",", ":")) + ";\n"
    with open(OUT, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("// Generated by src/make_viz_data.py - do not edit by hand.\n")
        fh.write(js)

    total = sum(counts.values())
    print(f"sides: {len(tables)}  name occurrences: {total}")
    print(f"wrote {OUT}  ({os.path.getsize(OUT):,} bytes)")


if __name__ == "__main__":
    main()
