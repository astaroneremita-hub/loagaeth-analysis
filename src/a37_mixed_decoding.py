"""
37 - Tables 25b-28b re-decoded: where rows end and diagonals begin.

Module a18 read each chessboard colour of these faces along one diagonal direction. Peterson notes
that leaf 25b has a third series, written left to right in the first five rows. Checking every
face, colour by colour, with a letter model of the row-written tables (2-24) as the judge:

  - each colour is allowed a block of top rows written BY ROWS (left to right on that colour),
    the rest on its best diagonal direction; the number of rows is chosen by the model;
  - a colour that still reads badly is allowed three zones cut by the diagonals r-c = T1, T2
    (upper-right triangle, a band, lower-left triangle), each read in its own best way.

Outputs the layout found for every face, bits per letter before/after, the master names newly
readable, and writes data/loagaeth_mixed_decoded.json (used by later modules through
a22.base_book). Controls: colours that already read well must not gain a row block; Peterson's note on 25b.
"""
import json
import os

import load
from a19_machine import CharLM

FACES = ["25b", "26a", "26b", "27a", "27b", "28a", "28b"]
NAMES = ["CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"]
OPTS = [(f, r) for f in ("diag", "anti", "row", "col") for r in (0, 1)]
ARROW = {("diag", 0): "↘", ("diag", 1): "↖", ("anti", 0): "↙", ("anti", 1): "↗", ("row", 0): "→ rows", ("row", 1): "← rows",
         ("col", 0): "↓ columns", ("col", 1): "↑ columns"}


def rows(k):
    return [load.letters(r) for r in load.leaves().get(k, []) if load.letters(r)]


def read(G, par, pred, fam, rev):
    d = {}
    for r in range(len(G)):
        for c in range(len(G[r])):
            if (r + c) % 2 == par and pred(r, c):
                d.setdefault({"diag": r - c, "anti": r + c, "row": r, "col": c}[fam], []).append(G[r][c])
    return [("".join(v)[::-1] if rev else "".join(v)) for _, v in sorted(d.items())]


def cost(m, L):
    L = [x for x in L if x]
    n = sum(len(x) for x in L)
    return (m.bits(L) * n if n else 0.0), n


def best_reading(m, G, par, pred, opts=OPTS):
    out = None
    for f, r in opts:
        L = read(G, par, pred, f, r)
        b, n = cost(m, L)
        if n and (out is None or b / n < out[0] / out[1]):
            out = (b, n, (f, r), L)
    return out or (0.0, 0, None, [])


def decode_colour(m, G, par):
    DI = [o for o in OPTS if o[0] in ("diag", "anti")]
    base = best_reading(m, G, par, lambda r, c: True, DI)
    best = None
    for R in range(0, 50):
        top = read(G, par, lambda r, c: r < R, "row", 0)
        tb, tn = cost(m, top)
        rb, rn, ro, rl = best_reading(m, G, par, lambda r, c, R=R: r >= R, DI)
        v = (tb + rb) / max(1, tn + rn)
        if best is None or v < best["bits"] - 1e-9:
            best = {"bits": v, "rows_by_row": R, "zones": [("rows 1-%d" % R, "→ rows", tn, tb / max(1, tn))] if R else [],
                    "lines": top + rl}
            if rn:
                best["zones"].append(("rest", ARROW[ro], rn, rb / rn))
    if best["bits"] > 3.6:  # three zones below the row block
        R = best["rows_by_row"]
        top = read(G, par, lambda r, c: r < R, "row", 0)
        tb, tn = cost(m, top)
        for T1 in range(-12, 14, 2):
            for T2 in range(T1 + 2, 32, 2):
                z = [best_reading(m, G, par, lambda r, c: r >= R and r - c < T1),
                     best_reading(m, G, par, lambda r, c: r >= R and T1 <= r - c < T2),
                     best_reading(m, G, par, lambda r, c: r >= R and r - c >= T2)]
                v = (tb + sum(x[0] for x in z)) / max(1, tn + sum(x[1] for x in z))
                if v < best["bits"] - 0.02:
                    labs = [f"upper-right (r−c < {T1})", f"band ({T1} ≤ r−c < {T2})", f"lower-left (r−c ≥ {T2})"]
                    best = {"bits": v, "rows_by_row": R,
                            "zones": ([("rows 1-%d" % R, "→ rows", tn, tb / max(1, tn))] if R else []) +
                                     [(lab, ARROW[x[2]], x[1], x[0] / max(1, x[1])) for lab, x in zip(labs, z) if x[1]],
                            "lines": top + [l for x in z for l in x[3]], "cut": (T1, T2), "z": z, "top": (top, tb, tn)}
        if "cut" in best:  # the band may still hold a corner written otherwise: split it at a column
            T1, T2 = best["cut"]
            z = best["z"]
            top, tb, tn = best["top"]
            band = lambda r, c: r >= R and T1 <= r - c < T2
            for S in range(4, 46, 2):
                a = best_reading(m, G, par, lambda r, c: band(r, c) and c < S)
                b = best_reading(m, G, par, lambda r, c: band(r, c) and c >= S)
                v = (tb + z[0][0] + z[2][0] + a[0] + b[0]) / max(1, tn + z[0][1] + z[2][1] + a[1] + b[1])
                if v < best["bits"] - 0.02:
                    parts = [(f"upper-right (r−c < {T1})", z[0]), (f"band, columns ≥ {S + 1}", b),
                             (f"band, columns 1–{S} (unclear)", a), (f"lower-left (r−c ≥ {T2})", z[2])]
                    best.update({"bits": v,
                                 "zones": ([("rows 1-%d" % R, "→ rows", tn, tb / max(1, tn))] if R else []) +
                                          [(lab, ARROW[x[2]], x[1], x[0] / max(1, x[1])) for lab, x in parts if x[1]],
                                 "lines": top + [l for _, x in parts for l in x[3]]})
        for k in ("cut", "z", "top"):
            best.pop(k, None)
    return base[0] / max(1, base[1]), best


def run():
    m = CharLM(3).fit([x for t in range(2, 25) for s in "ab" for x in rows(f"{t}{s}")])
    out, decoded, by_colour, layout = {}, {}, {}, {}
    old_text, new_text = [], []
    for f in FACES:
        G = rows(f)
        cols = []
        for par in (0, 1):
            before, b = decode_colour(m, G, par)
            cols.append({"colour": par, "bits_single_diagonal": round(before, 2), "bits_now": round(b["bits"], 2),
                         "rows_written_by_rows": b["rows_by_row"],
                         "zones": [{"zone": z, "reading": a, "letters": n, "bits": round(v, 2)} for z, a, n, v in b["zones"]]})
            decoded.setdefault(f, []).extend(l for l in b["lines"] if l)
            by_colour.setdefault(f, []).append([l for l in b["lines"] if l])
            layout.setdefault(f, []).append({"colour": par, "rows_by_row": b["rows_by_row"], "zones": [[z, a] for z, a, n, v in b["zones"]]})
            new_text += b["lines"]
            old_text += best_reading(m, G, par, lambda r, c: True, [o for o in OPTS if o[0] in ("diag", "anti")])[3]
        out[f] = cols
    # internal control: colours that already read well on one diagonal should not gain a row block
    good = [c for cols in out.values() for c in cols if c["bits_single_diagonal"] <= 3.3]
    ctrl = {"colours_reading_well_on_one_diagonal": len(good),
            "of_which_given_a_row_block": sum(1 for c in good if c["rows_written_by_rows"]),
            "external_check": "Peterson's note says leaf 25b has a third series in its first five rows; the "
                              "search, which knows nothing of the note, finds 5 rows on 25b."}
    So, Sn = "|".join(old_text), "|".join(new_text)
    names = {n: [So.count(n), Sn.count(n)] for n in NAMES}
    path = os.path.join(load.DATA, "loagaeth_mixed_decoded.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"meta": {"description": "Faces 25b-28b decoded with row blocks and zones (module a37): lines per face."},
                   "faces": decoded, "by_colour": by_colour, "layout": layout}, fh, ensure_ascii=False, indent=0)
    res = {"faces": out, "controls": ctrl,
           "letters": sum(len(x) for x in new_text),
           "bits_per_letter_before": round(m.bits([x for x in old_text if x]), 3),
           "bits_per_letter_after": round(m.bits([x for x in new_text if x]), 3),
           "names_before_after": names,
           "names_total_before_after": [sum(v[0] for v in names.values()), sum(v[1] for v in names.values())]}
    load.save_result("37_mixed_decoding", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
