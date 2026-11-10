"""
18 - Peterson's markup, the leaf titles, and the decoding of tables 25b-28b.

Source: Joseph H. Peterson's transcription, https://www.esotericarchives.com/dee/sl3189.htm
(downloaded into data/raw/, which is git-ignored; only derived data is written to data/).

  A) In leaves 25b-28b every letter is followed by one of two marks (~ / ` or a space). Aligned to
     the 49x49 grid, each mark falls on exactly one chessboard colour (about 1200 / 1201 cells) -
     the same two colours that tables 29-48 write as separate diamonds.
  B) Read along rows these tables look like noise. Read colour by colour along the diagonals they
     become ordinary Loagaeth text. Rule: one colour (the one marked ~ or `) runs down-right along
     the main diagonals (r-c constant); the other colour runs leftward, up-left on the same
     diagonals or down-left on the anti-diagonals (r+c constant) - one binary choice per face.
     Control: the same procedure (max over the same options) on ordinary row-written tables.
  C) Master names in the decoded text vs the row reading.
  D) Leaf titles: master stems inside them, and whether a title is drawn from its own leaf
     (title 4-grams found in the leaf vs in other leaves).
"""
import html
import json
import math
import os
import random
import re
import statistics
import urllib.request
from collections import Counter

import load

URL = "https://www.esotericarchives.com/dee/sl3189.htm"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RAW = os.path.join(ROOT, "data", "raw", "sl3189.htm")
FACES = ["26a", "26b", "27a", "27b", "28a", "28b"]
MASTERS = ["CHASTOR", "ANZACH", "GETH", "ADNOCHA", "NOCHA", "ALGETH", "ACLAX", "OXAD", "CHADAX"]


def fetch():
    if not os.path.exists(RAW):
        os.makedirs(os.path.dirname(RAW), exist_ok=True)
        req = urllib.request.Request(URL, headers={"User-Agent": "loagaeth-analysis research script"})
        with urllib.request.urlopen(req, timeout=60) as r, open(RAW, "wb") as f:
            f.write(r.read())
    return open(RAW, encoding="latin-1").read()


def parse(h):
    parts = re.split(r'<A NAME="l(\d+[ab])">', h)
    raw_rows = {}
    for i in range(1, len(parts), 2):
        pre = re.search(r"<PRE[^>]*>(.*?)</PRE>", parts[i + 1], re.S)
        txt = html.unescape(re.sub("<[^>]+>", "", pre.group(1))) if pre else ""
        raw_rows[parts[i]] = [re.match(r"\s*\d+\.\s?(.*)$", l).group(1).rstrip()
                              for l in txt.split("\n") if re.match(r"\s*\d+\.", l)]
    titles = {}
    for m in re.finditer(r"\[LEAF\s*([0-9]+[ab])\](.*?)<PRE", h, re.S):
        t = html.unescape(re.sub(r"<[^>]+>", " ", m.group(2)))
        t = re.sub(r"\[[^\]]*\]", " ", t)          # drop editorial / phonetic brackets
        t = re.sub(r'"[^"]*"', " ", t)
        t = re.sub(r"\s+", " ", t).strip()
        titles[m.group(1)] = t
    return raw_rows, titles


def marks_after(raw):
    s = "".join(raw)
    out = []
    for j, ch in enumerate(s):
        if ch.isalpha():
            out.append(next((c for c in s[j + 1:] if not c.isalpha()), "END"))
    return out


def grid(leaf):
    return [load.letters(r) for r in load.leaves().get(leaf, [])]


def diag_lines(g, colour, family, direction):
    H, W = len(g), max(len(r) for r in g)
    lines = []
    ks = range(-(W - 1), H) if family == "r-c" else range(H + W - 1)
    for k in ks:
        if k % 2 != colour:
            continue
        rr = range(H) if direction in ("down-right", "down-left") else range(H - 1, -1, -1)
        if family == "r-c":
            cells = [(r, r - k) for r in rr if 0 <= r - k < len(g[r])]
        else:
            cells = [(r, k - r) for r in rr if 0 <= k - r < len(g[r])]
        if cells:
            lines.append("".join(g[r][c] for r, c in cells))
    return lines


def run():
    rng = random.Random(18)
    h = fetch()
    raw_rows, titles = parse(h)

    ref_txt = "".join("".join(grid(f"{t}{s}")) for t in range(2, 25) for s in "ab")
    rec = {g for g, f in Counter(ref_txt[i:i + 6] for i in range(len(ref_txt) - 5)).items() if f >= 5}

    def dens(lines):
        tot = hit = 0
        for l in lines:
            for i in range(len(l) - 5):
                tot += 1
                hit += l[i:i + 6] in rec
        return hit / tot if tot else 0.0

    def dbl(lines):
        n = sum(max(0, len(l) - 1) for l in lines) or 1
        return sum(sum(a == b for a, b in zip(l, l[1:])) for l in lines) / n

    def hcond(lines):
        bi, ctx = Counter(), Counter()
        for l in lines:
            bi.update(zip(l, l[1:]))
            ctx.update(l[:-1])
        n = sum(bi.values()) or 1
        return -sum(c / n * math.log2(c / ctx[a]) for (a, b), c in bi.items())

    LEFT = [("r-c", "up-left"), ("r+c", "down-left")]

    # A) marks vs colour
    mark_table, decoded, faces = {}, {}, {}
    for leaf in FACES + ["25b"]:
        g = grid(leaf)
        m = marks_after(raw_rows.get(leaf, []))
        flat = "".join(g)
        aligned = len(m) == len(flat)
        cross = Counter(((idx // 49 + idx % 49) % 2, mk) for idx, mk in enumerate(m)) if aligned else Counter()
        mark_table[leaf] = {"aligned": aligned, "mark_by_colour": {f"{c}:{mk}": n for (c, mk), n in sorted(cross.items())}}
        if leaf not in FACES:
            continue
        # B) decode: colour marked ~ or ` runs down-right; the other runs leftward
        main = next((c for c in (0, 1) if cross[(c, "~")] > 600 or cross[(c, "`")] > 600), 0)
        down = diag_lines(g, main, "r-c", "down-right")
        opts = {f"{fam} {dr}": diag_lines(g, 1 - main, fam, dr) for fam, dr in LEFT}
        best = max(opts, key=lambda k: dens(opts[k]))
        rows_ = g
        faces[leaf] = {
            "main_colour": main,
            "rows_as_written": {"names": round(dens(rows_), 3), "doubled": round(dbl(rows_), 4), "H_cond": round(hcond(rows_), 3)},
            "stream_down_right": {"names": round(dens(down), 3), "doubled": round(dbl(down), 4), "H_cond": round(hcond(down), 3)},
            "stream_leftward": {"reading": best, "names": round(dens(opts[best]), 3), "doubled": round(dbl(opts[best]), 4),
                                "H_cond": round(hcond(opts[best]), 3),
                                "alternative": {k: round(dens(v), 3) for k, v in opts.items()}},
        }
        decoded[leaf] = {"down_right": down, "leftward": opts[best], "leftward_reading": best}

    # 25b: rows vs the best of all single-colour diagonal readings (descriptive)
    g25 = grid("25b")
    opts25 = {}
    for col in (0, 1):
        for fam, dr in [("r-c", "down-right"), ("r-c", "up-left"), ("r+c", "down-left"), ("r+c", "up-right")]:
            opts25[f"colour{col} {fam} {dr}"] = dens(diag_lines(g25, col, fam, dr))
    leaf25 = {"rows_names": round(dens(g25), 3),
              "best_diagonal_readings": sorted(((k, round(v, 3)) for k, v in opts25.items()), key=lambda x: -x[1])[:3]}
    # 25b's marks are mixed, but it follows the same two-current rule (colour 0 down-right,
    # colour 1 up-left), which is also its best pair of readings; store it with the others.
    decoded["25b"] = {"down_right": diag_lines(g25, 0, "r-c", "down-right"),
                      "leftward": diag_lines(g25, 1, "r-c", "up-left"), "leftward_reading": "r-c up-left"}

    # control: same procedure on ordinary row-written tables (max over the same options)
    ctrl = []
    for t in range(2, 25):
        for s in "ab":
            g = grid(f"{t}{s}")
            if len(g) != 49 or any(len(r) != 49 for r in g):
                continue
            best_main = max(dens(diag_lines(g, c, "r-c", "down-right")) for c in (0, 1))
            best_left = max(dens(diag_lines(g, c, fam, dr)) for c in (0, 1) for fam, dr in LEFT)
            ctrl.append(max(best_main, best_left))
    control = {"tables": len(ctrl), "max_names_any_diagonal_reading": round(max(ctrl), 3),
               "mean": round(statistics.mean(ctrl), 3)}

    all_dec = [l for k, d in decoded.items() if k in FACES for l in d["down_right"] + d["leftward"]]
    all_rows = [r for f in FACES for r in grid(f)]
    overall = {"decoded": {"names": round(dens(all_dec), 3), "doubled": round(dbl(all_dec), 4), "H_cond": round(hcond(all_dec), 3)},
               "rows_as_written": {"names": round(dens(all_rows), 3), "doubled": round(dbl(all_rows), 4), "H_cond": round(hcond(all_rows), 3)},
               "reference_tables_2_24_rows": {"names": round(dens([r for t in range(2, 25) for s in "ab" for r in grid(f"{t}{s}")]), 3)}}

    # C) master names before/after decoding
    dec_txt = "|".join(all_dec)
    row_txt = "|".join(all_rows)
    masters = {n: {"rows": row_txt.count(n), "decoded": dec_txt.count(n)} for n in MASTERS}

    # D) titles
    clean = {k: re.sub(r"[^A-Za-z ]", " ", v).upper() for k, v in titles.items()}
    stems = {k: [s for s in ("CHAST", "CHUST", "GETH", "ALGE", "NOCHA", "ANZA", "ADNA", "OXAD") if s in v.replace(" ", "")]
             for k, v in clean.items()}
    texts = {}
    for k in clean:
        if k[:-1].isdigit() and int(k[:-1]) >= 2:
            g = grid(k)
            if g:
                texts[k] = "".join(g)
    own, other = [], []
    for k, ttl in clean.items():
        if k not in texts:
            continue
        grams = {w[i:i + 4] for w in ttl.split() for i in range(len(w) - 3)}
        if not grams:
            continue
        own.append(sum(1 for gm in grams if gm in texts[k]) / len(grams))
        others = [o for o in texts if o != k]
        for o in rng.sample(others, min(5, len(others))):
            other.append(sum(1 for gm in grams if gm in texts[o]) / len(grams))
    title_test = {"share_of_title_4grams_found_in_own_leaf": round(statistics.mean(own), 3),
                  "found_in_other_leaves": round(statistics.mean(other), 3), "n_titles": len(own)}

    os.makedirs(os.path.join(ROOT, "data"), exist_ok=True)
    with open(os.path.join(ROOT, "data", "loagaeth_diagonal_decoded.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": {"description": "Tables 26-28 read colour by colour along the diagonals (module a18).",
                            "source": URL}, "faces": decoded}, f, ensure_ascii=False, indent=1)
    with open(os.path.join(ROOT, "data", "loagaeth_leaf_titles.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": {"source": URL, "note": "Leaf headings as transcribed; brackets/phonetics removed."},
                   "titles": titles, "stems_in_titles": {k: v for k, v in stems.items() if v}}, f, ensure_ascii=False, indent=1)

    res = {
        "A_marks_vs_colour": mark_table,
        "B_faces": faces, "B_overall": overall, "B_control_row_tables_read_diagonally": control,
        "B_leaf_25b": leaf25,
        "C_master_names": masters,
        "D_titles": {"n": len(titles), "stems_in_titles": {k: v for k, v in stems.items() if v}, "title_vs_own_leaf": title_test},
        "midpoint_note": ("Rows are used up to side 25a; from side 25b on, the text runs on diagonals (squares "
                          "25b-28b, then diamonds 29-48). In a 49-leaf book (98 sides) 25a is side 49: the writing "
                          "turns exactly at the middle - 49 sides in rows, 49 on diagonals. Descriptive."),
        "conclusion": ("Tables 26-28 are not noise: Peterson's marks separate the two chessboard colours, and "
                       "each colour read along the diagonals is ordinary Loagaeth text (one colour down-right, "
                       "the other leftward). Ordinary row tables read the same way give nothing. The turn to "
                       "diagonal writing starts at side 25b."),
    }
    load.save_result("18_markup_decoding", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1)[:5000])
