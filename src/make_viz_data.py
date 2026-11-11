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


def row_occurrences(rows, names=NAMES):
    occ = []
    for r, s in enumerate(rows):
        for k, name in enumerate(names):
            for c in find_all(s, name):
                occ.append([k, r, c, len(name), 0, 1])
    return occ


def diagonal_cells(rows, d):
    """Cells (r, c) on the r-c = d diagonal, ordered by increasing r."""
    return [(r, r - d) for r in range(N) if 0 <= r - d < N and r < len(rows) and r - d < len(rows[r])]


def diagonal_occurrences(rows, names=NAMES, drp_fixed=None):
    """Names along the r-c diagonals read as two currents. drp = parity of the down-right current;
    if not given (no decoded file), the parity with more master-name hits is used."""
    best = None
    for drp in ((drp_fixed,) if drp_fixed is not None else (0, 1)):
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
            for k, name in enumerate(names):
                for i in find_all(s, name):
                    r0, c0 = cells[i]
                    occ.append([k, r0, c0, len(name), step, step])
        if best is None or len(occ) > len(best[1]):
            best = (drp, occ)
    return best


def decoded_parity(rows, key):
    """Down-right parity taken from data/loagaeth_diagonal_decoded.json (module a18), if present."""
    p = os.path.join(ROOT, "data", "loagaeth_diagonal_decoded.json")
    try:
        face = json.load(open(p, encoding="utf-8"))["faces"][key]
    except (OSError, KeyError, ValueError):
        return None
    diags = {d: "".join(rows[r][c] for r, c in diagonal_cells(rows, d)) for d in range(-(N - 1), N)}
    votes = {0: 0, 1: 0}
    for line in face.get("down_right", []):
        for d, s in diags.items():
            if len(line) > 2 and s == line:
                votes[d % 2] += 1
    return None if votes[0] == votes[1] else max(votes, key=votes.get)


def load_result(name):
    p = os.path.join(ROOT, "results", name)
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        print(f"  (results/{name} not found - related views will be empty)")
        return None


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


def make_blocks(div):
    """Same blocks as the viewer: 2 -> four 24x24 quadrants + central cross (row/col 25);
    4 -> sixteen 12x12 + central cross; 7 -> 49 blocks of 7x7."""
    rect = lambda r0, r1, c0, c1: [r * N + c for r in range(r0, r1 + 1) for c in range(c0, c1 + 1)]
    if div == 7:
        return [rect(br * 7, br * 7 + 6, bc * 7, bc * 7 + 6) for br in range(7) for bc in range(7)]
    parts = [(0, 23), (25, 48)] if div == 2 else [(0, 11), (12, 23), (25, 36), (37, 48)]
    blocks = [rect(r0, r1, c0, c1) for r0, r1 in parts for c0, c1 in parts]
    blocks.append([24 * N + k for k in range(N)] + [k * N + 24 for k in range(N) if k != 24])
    return blocks


def block_majority(vals, th, cells):
    cnt = [0, 0, 0, 0]
    for i in cells:
        cnt[element_of(vals[i], th)] += 1
    mx = max(cnt)
    tied = [k for k in range(4) if cnt[k] == mx]
    mean_el = element_of(sum(vals[i] for i in cells) / len(cells), th)
    tied.sort(key=lambda k: (abs(k - mean_el), -k))  # nearest to the block-mean element, then hotter
    return tied[0], mx / len(cells), len(tied) > 1


def majority_report(label, obs, nul):
    th = quartiles(obs)
    for div in (2, 7):
        blocks = make_blocks(div)
        print(f"majority by block ({'2x2 + cross' if div == 2 else '7x7'}) on {label}  [W/E/A/F, * = tie]")
        for name, vals in (("observed", obs), ("null", nul)):
            res = [block_majority(vals, th, b) for b in blocks]
            cell = lambda m: "WEAF"[m[0]] + ("*" if m[2] else " ") + f"{round(m[1] * 100):3d}%"
            n = 2 if div == 2 else 7
            for r in range(n):
                print(f"  {name if r == 0 else '':8s} " + "  ".join(cell(m) for m in res[r * n:(r + 1) * n]))
            if div == 2:
                print(f"  {'':8s} cross: {cell(res[-1])}")


def element_report(label, obs, nul):
    majority_report(label, obs, nul)
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
    for L in ("A", "H", "X"):
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


CONST_MASTER = ["CHASTOR", "ANZACH", "GETH", "NOCHA", "ADNOCHA", "ALGETH", "ACLAX", "CHUSTOR", "OXAD", "CHADAX"]


def discovered_names(tables):
    """Discovered names (results/23_name_discovery.json, A_candidates.top) searched on the same reading:
    rows for 2a-25a, the two decoded diagonal currents for 25b-28b, the stored lines (rows) for 29-48."""
    res = load_result("23_name_discovery.json")
    if not res:
        return None
    names = [c["name"] for c in res["A_candidates"]["top"]]
    fams = res.get("C_families", {}).get("largest", [])
    fam = {n: -1 for n in names}
    for i, f in enumerate(fams):
        for n in f:
            if n in fam:
                fam[n] = i
    total, per_cur = 0, [0, 0]
    for key, e in tables.items():
        if e["f"] == "square-diagonal":
            _, occ = diagonal_occurrences(e["rows"], names, e["drp"])
            for o in occ:
                per_cur[0 if o[4] > 0 else 1] += 1
        else:
            occ = row_occurrences(e["rows"], names)
        e["docc"] = occ
        total += len(occ)
    meta = {k: v for k, v in res["A_candidates"].items() if k != "top"}
    print(f"discovered names: {len(names)}, occurrences {total} (25b-28b currents: down-right {per_cur[0]}, leftward {per_cur[1]})")
    return {"names": names, "family": [fam[n] for n in names], "families": fams,
            "info": [{k: c.get(k) for k in ("count", "tables", "z", "markov3_expected")} for c in res["A_candidates"]["top"]],
            "meta": meta}


def constellation(tables, stack_sides, disc_names):
    """Start cells of each name on the 36 exact 49x49 sides: flat list [side_index, row, col, ...]."""
    bridges = load_result("25_bridges.json")
    pts = {}
    for n in dict.fromkeys(CONST_MASTER + list(disc_names)):
        a = []
        for si, k in enumerate(stack_sides):
            for r, row in enumerate(tables[k]["rows"]):
                for c in find_all(row, n):
                    a += [si, r, c]
        if a:
            pts[n] = a
    nocha = len(pts.get("NOCHA", [])) // 3
    print(f"constellation: {len(pts)} names with starts on the stack (NOCHA {nocha})")
    return {"pts": pts, "B": (bridges or {}).get("B_constellation", {})}


def book_order():
    """Similarity matrix, segment boundaries, dialects and the two-current figures (results/24_book_architecture.json).
    The full greedy order is recomputed like a24: start at 2a, repeatedly take the most similar unused side
    (ties -> earliest in book order)."""
    res = load_result("24_book_architecture.json")
    if not res:
        return None
    D = res["D_book_order"]
    keys, M = D["similarity_matrix_keys"], D["similarity_matrix"]
    # The stored matrix is rounded to 3 decimals, which creates ties that a24 (full precision) did not have,
    # so the stored first 30 are kept as the prefix and the rest is continued greedily from the 30th side.
    stored = [keys.index(k) for k in D.get("greedy_order_first_30", []) if k in keys] or [0]
    ser, cur = stored[:], stored[-1]
    left = [j for j in range(len(keys)) if j not in ser]
    while left:
        nxt = max(left, key=lambda j: (M[cur][j], -j))
        ser.append(nxt)
        left.remove(nxt)
        cur = nxt
    greedy = [keys[i] for i in ser]
    same30 = greedy[:30] == D.get("greedy_order_first_30")
    print(f"order: greedy = stored first {len(stored)} + continuation; prefix {'matches' if same30 else 'DIFFERS'}")
    segs = [("opening", 2, 5), ("heartland", 6, 25), ("decoded 26-28", 26, 28), ("diamonds", 29, 43), ("end", 44, 48)]
    return {"keys": keys, "sim": [[int(round(v * 1000)) for v in row] for row in M], "greedy": greedy,
            "greedy_matches_stored30": same30, "segs": segs,
            "stats": {k: D.get(k) for k in ("path_similarity_dee_order", "random_orders_mean", "random_orders_max",
                                             "greedy_seriation", "a_vs_b_same_table_mean", "b_vs_next_a_mean",
                                             "mirror_t_vs_49_minus_t_mean", "random_distant_pairs_mean", "same_plan_column_mean")},
            "dialects": res.get("C_dialects"), "currents": res.get("E_two_currents")}


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
            drp, occ = diagonal_occurrences(rows, NAMES, decoded_parity(rows, key))
            entry["drp"] = drp
            entry["occ"] = row_occurrences(rows) + occ
        else:
            entry["occ"] = row_occurrences(rows)
        tables[key] = entry
        counts[key] = len(entry["occ"])

    stack = build_stack(tables)
    rev = reversed_names(tables)
    sig = signatures(tables)
    disc = discovered_names(tables)
    const = constellation(tables, stack["sides"], disc["names"] if disc else [])
    order = book_order()

    data = {
        "stack": stack,
        "rev": rev,
        "sig": sig,
        "disc": disc,
        "const": const,
        "order": order,
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
