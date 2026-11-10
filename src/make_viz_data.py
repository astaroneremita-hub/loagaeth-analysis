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

# Names searched forward and reversed on the diamond sides (29-48).
REV_BASE = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "CHUSTOR"]
REV_NAMES = [n[::-1] for n in REV_BASE]
N_SHUFFLES = 200


def count_in_rows(rows, names):
    return sum(len(find_all(r, n)) for r in rows for n in names)


def markov1_expected(rows, names):
    """Expected occurrences of the names under a first-order Markov model fitted to the side's rows."""
    uni, big, first = {}, {}, {}
    for r in rows:
        for ch in r:
            uni[ch] = uni.get(ch, 0) + 1
        for a, b in zip(r, r[1:]):
            big[(a, b)] = big.get((a, b), 0) + 1
            first[a] = first.get(a, 0) + 1
    tot = sum(uni.values())
    exp = 0.0
    for name in names:
        p = uni.get(name[0], 0) / tot
        for a, b in zip(name, name[1:]):
            p *= big.get((a, b), 0) / first[a] if first.get(a) else 0.0
        exp += p * sum(max(0, len(r) - len(name) + 1) for r in rows)
    return exp


def shuffled_mean(rows, names, rng, n=N_SHUFFLES):
    """Mean count after shuffling letters inside the side (row lengths kept)."""
    lens = [len(r) for r in rows]
    cells = list("".join(rows))
    tot = 0
    for _ in range(n):
        rng.shuffle(cells)
        s, out, o = "".join(cells), [], 0
        for ln in lens:
            out.append(s[o:o + ln])
            o += ln
        tot += count_in_rows(out, names)
    return tot / n


def reversed_names(tables):
    """Reversed master-name occurrences on diamond sides, with shuffle and Markov-1 baselines."""
    rng = random.Random(NULL_SEED + 1)
    stats = {"forward": [0, 0.0, 0.0], "reversed": [0, 0.0, 0.0]}  # observed, shuffle mean, Markov-1
    per_name = {n: [0, 0] for n in REV_BASE}  # forward, reversed observed
    for key in sorted(tables, key=lambda k: (int(k[:-1]), k[-1])):
        e = tables[key]
        if e["f"] != "diamond":
            continue
        rows = e["rows"]
        rocc = []
        for k, name in enumerate(REV_NAMES):
            for r, s in enumerate(rows):
                for c in find_all(s, name):
                    rocc.append([k, r, c, len(name)])
        e["rocc"] = rocc
        for label, names in (("forward", REV_BASE), ("reversed", REV_NAMES)):
            stats[label][0] += count_in_rows(rows, names)
            stats[label][1] += shuffled_mean(rows, names, rng)
            stats[label][2] += markov1_expected(rows, names)
        for fwd, rv in zip(REV_BASE, REV_NAMES):
            per_name[fwd][0] += count_in_rows(rows, [fwd])
            per_name[fwd][1] += count_in_rows(rows, [rv])
    print("diamond sides 29-48, names:", " ".join(REV_BASE))
    for label, (o, sh, mk) in stats.items():
        print(f"  {label:8s} observed {o:4d}   within-side shuffle mean {sh:7.2f}   Markov-1 expected {mk:7.2f}")
    print("  per name (forward / reversed):", ", ".join(f"{n} {f}/{r}" for n, (f, r) in per_name.items()))
    stats = {k: [v[0], round(v[1], 2), round(v[2], 2)] for k, v in stats.items()}
    return {"names": REV_BASE, "rev": REV_NAMES, "stats": stats, "per_name": per_name}


def signatures(tables):
    """Top-3 letters (by count, ties alphabetical) of every side."""
    sig = {}
    for key in sorted(tables, key=lambda k: (int(k[:-1]), k[-1])):
        cnt = {}
        for r in tables[key]["rows"]:
            for ch in r:
                cnt[ch] = cnt.get(ch, 0) + 1
        sig[key] = "".join(sorted(cnt, key=lambda ch: (-cnt[ch], ch))[:3])
    groups, dom = {}, {}
    for k, s in sig.items():
        groups.setdefault(s, []).append(k)
        dom[s[0]] = dom.get(s[0], 0) + 1
    print("dominant letter counts:", dom)
    print("signature groups:", ", ".join(f"{s}:{len(v)}" for s, v in sorted(groups.items(), key=lambda x: -len(x[1]))))
    return sig


ELEMENTS = ["Water", "Earth", "Air", "Fire"]  # coldest -> hottest


def quartiles(vals):
    s = sorted(vals)
    return tuple(s[min(len(s) - 1, int(p * len(s)))] for p in (0.25, 0.5, 0.75))


def element_of(v, th):
    return 3 if v > th[2] else 2 if v > th[1] else 1 if v > th[0] else 0


def region_masks():
    """Edge columns vs interior, and the four triangles around the two diagonals (diagonals excluded)."""
    reg = {"edge cols 1-2,48-49": [], "interior": [], "top": [], "right": [], "bottom": [], "left": []}
    for r in range(N):
        for c in range(N):
            i = r * N + c
            reg["edge cols 1-2,48-49" if c in (0, 1, 47, 48) else "interior"].append(i)
            if r < min(c, 48 - c):
                reg["top"].append(i)
            elif r > max(c, 48 - c):
                reg["bottom"].append(i)
            elif c < min(r, 48 - r):
                reg["left"].append(i)
            elif c > max(r, 48 - r):
                reg["right"].append(i)
    return reg


def element_report(label, obs, nul):
    th = quartiles(obs)
    reg = region_masks()
    print(f"elements on {label}: observed quartile thresholds {tuple(round(t, 3) for t in th)}")
    for name, vals in (("observed", obs), ("null", nul)):
        el = [element_of(v, th) for v in vals]
        tot = [el.count(k) / len(el) for k in range(4)]
        print(f"  {name:8s} {'all cells':20s}           " + "  ".join(f"{ELEMENTS[k]} {tot[k]*100:5.1f}%" for k in (3, 2, 1, 0)))
        for rn, idx in reg.items():
            sh = [sum(1 for i in idx if el[i] == k) / len(idx) for k in range(4)]
            mean = sum(vals[i] for i in idx) / len(idx)
            print(f"  {name:8s} {rn:20s} mean {mean:5.2f}  " + "  ".join(f"{ELEMENTS[k]} {sh[k]*100:5.1f}%" for k in (3, 2, 1, 0)))


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
    element_report("stack, any master name (sides per cell)", no[len(NAMES)], nn[len(NAMES)])
    for L in ("A", "X"):
        e = sum(lo[L]) / (N * N)
        element_report(f"stack, letter {L} obs/exp", [v / e for v in lo[L]], [v / e for v in ln_[L]])
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
    rev = reversed_names(tables)
    sig = signatures(tables)

    data = {
        "stack": stack,
        "rev": rev,
        "sig": sig,
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
