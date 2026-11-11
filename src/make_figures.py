"""
Generate every figure of the project as a standalone SVG in figures/.

Run after the analyses (run_all.py calls this at the end):
    python src/make_figures.py

Each figure is drawn from the JSON results (or the bundled data), so the pictures stay
reproducible and update when the data or the analyses change. Pure standard library.
"""
import json
import math
import os
from collections import Counter

import load

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "figures")
RES = os.path.join(ROOT, "results")
GOV = os.path.join(ROOT, "engine", "data", "governadores.json")

INK, MUTED, LINE = "#2C2C2A", "#5F5E5A", "#C3C2B7"
P6, P4, P2 = "#534AB7", "#7F77DD", "#AFA9EC"
GRAY, GRAY2 = "#B4B2A9", "#D3D1C7"
BLUE, TEAL, GREEN, AMBER, CORAL = "#378ADD", "#1D9E75", "#639922", "#BA7517", "#D85A30"


def res(name):
    with open(os.path.join(RES, name + ".json"), encoding="utf-8") as f:
        return json.load(f)


def esc(s):
    return str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def text(x, y, s, size=12, color=INK, anchor="start", weight=400):
    return (f'<text x="{x}" y="{y}" font-size="{size}" fill="{color}" text-anchor="{anchor}" '
            f'font-weight="{weight}">{esc(s)}</text>')


def rect(x, y, w, h, fill, rx=3, stroke=None):
    st = f' stroke="{stroke}" stroke-width="0.6"' if stroke else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}"{st}/>'


def _text_extent(parts):
    """Rough right-most x reached by any <text> (≈0.56·font-size per character)."""
    import re as _re
    right = 0.0
    for p in parts:
        for m in _re.finditer(r'<text x="([\d.\-]+)" y="[\d.\-]+" font-size="([\d.]+)"[^>]*text-anchor="(\w+)"[^>]*>([^<]*)</text>', p):
            x, fs, anc, s = float(m.group(1)), float(m.group(2)), m.group(3), m.group(4)
            w = len(s) * fs * 0.56
            x1 = x if anc == "end" else (x + w / 2 if anc == "middle" else x + w)
            right = max(right, x1)
    return right


def svg(name, w, h, title, subtitle, body):
    w = max(w, int(_text_extent(body + [text(24, 32, title, 16, weight=600), text(24, 52, subtitle, 12)]) + 24))
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'font-family="Segoe UI, Helvetica, Arial, sans-serif" role="img">'
            f'<title>{esc(title)}</title>'
            f'<rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#FFFFFF" stroke="#E1E0D9"/>'
            + text(24, 32, title, 16, INK, weight=600)
            + text(24, 52, subtitle, 12, MUTED))
    os.makedirs(FIG, exist_ok=True)
    path = os.path.join(FIG, name + ".svg")
    with open(path, "w", encoding="utf-8") as f:
        f.write(head + "".join(body) + "</svg>")
    return path


def legend(x, y, items):
    out, cx = [], x
    for color, label in items:
        out.append(rect(cx, y - 10, 12, 12, color, 2))
        out.append(text(cx + 18, y, label, 12, MUTED))
        cx += 26 + 7 * len(label)
    return out


# ---------------------------------------------------------------- 1. territory map
def fig_territory():
    t = res("10_territory")
    color = {"CHASTOR": P6, "CHUSTOR": BLUE, "frontier": GREEN, "prophecy": GRAY,
             "void": GRAY2, "border": TEAL}
    rows = t["tables"]
    x0, cw, y0 = 24, 15, 80
    body = []
    for i, r in enumerate(rows):
        x = x0 + i * cw
        body.append(rect(x, y0, cw - 2, 56, color.get(r["zone"], GRAY2), 2))
        if r["table"] in (1, 6, 25, 29, 43, 44, 48):
            body.append(text(x + (cw - 2) / 2, y0 + 74, r["table"], 11, MUTED, "middle"))
    body += legend(24, 190, [(P6, "CHASTOR"), (BLUE, "CHUSTOR"), (GREEN, "frontier"),
                             (TEAL, "border"), (GRAY, "prophecy"), (GRAY2, "void")])
    body.append(text(24, 220, f"Zonation is real: lag-1 autocorrelation {t['zonation_lag1_autocorr']} "
                              f"vs shuffle null 95th pct {t['null_95th']}. Reading order runs 49 → 1.", 12, MUTED))
    return svg("fig_territory", x0 * 2 + len(rows) * cw, 240,
               "Territory of the master names across the tables",
               "Each cell is one table (book order). Colour = which master name rules it.", body)


# ---------------------------------------------------------------- 2. governors' digits
def fig_digits():
    g = json.load(open(GOV, encoding="utf-8"))["governadores"]
    dc = Counter("".join(str(x["servos"]) for x in g))
    mx = max(dc.values())
    body, x0, base = [], 40, 250
    for i, d in enumerate("0123456789"):
        v = dc.get(d, 0)
        h = v / mx * 170
        x = x0 + i * 52
        c = P6 if d in "236" else GRAY
        body.append(rect(x, base - h, 36, h, c, 3))
        body.append(text(x + 18, base - h - 6, v, 12, INK, "middle"))
        body.append(text(x + 18, base + 18, d, 13, INK, "middle", 600 if d in "236" else 400))
    body.append(f'<line x1="{x0-6}" y1="{base}" x2="{x0+520}" y2="{base}" stroke="{LINE}"/>')
    tot = sum(dc.values())
    share = sum(dc[d] for d in "236") / tot
    body += legend(40, 300, [(P6, f"2, 3, 6 = {share:.0%} of all digits (chance ≈ 30%, z ≈ 11)")])
    return svg("fig_governor_digits", 600, 320, "Digits in the 91 governors' numbers",
               "Dee's servant counts are dominated by 2, 3 and 6.", body)


# ---------------------------------------------------------------- 3. head digit per Aethyr
def fig_head_regime():
    g = json.load(open(GOV, encoding="utf-8"))["governadores"]
    r13 = res("13_numbers")["B_head_digit_by_aethyr"]
    by = {}
    for x in g:
        by.setdefault(x["aethyr"], []).append(str(x["servos"])[0])
    x0, cw, y0 = 30, 20, 96
    body = []
    for a in range(1, 31):
        hs = by[a]
        x = x0 + (a - 1) * cw
        uni = len(set(hs)) == 1
        body.append(rect(x, y0, cw - 3, 18 * len(hs) + 6, P2 if uni else "#F1EFE8", 3,
                         None if uni else "#E1E0D9"))
        for k, h in enumerate(hs):
            body.append(text(x + (cw - 3) / 2, y0 + 16 + 18 * k, h, 12, INK, "middle"))
        if a in (1, 5, 10, 15, 20, 25, 30):
            body.append(text(x + (cw - 3) / 2, y0 + 96, a, 11, MUTED, "middle"))
    mid = x0 + 14 * cw - 2
    body.append(f'<line x1="{mid}" y1="{y0-14}" x2="{mid}" y2="{y0+100}" stroke="{MUTED}" stroke-dasharray="4 3"/>')
    body.append(text(x0, y0 - 18, f"Aethyrs 1–14: free (z = {r13['aethyrs_1_14']['z']})", 12, MUTED))
    body.append(text(mid + 8, y0 - 18, f"Aethyrs 15–30: head shared per Aethyr (z = {r13['aethyrs_15_30']['z']})", 12, MUTED))
    body.append(text(x0, y0 + 130, "Every number = head digit + a permuted 2·3·6 block:  7|632   9|236   5|362   2|360", 12, INK))
    body += legend(x0, y0 + 156, [(P2, "all governors of that Aethyr share the head digit")])
    return svg("fig_head_digit_regime", x0 * 2 + 30 * cw, 280,
               "Head digit of the governors' numbers, per Aethyr",
               "The construction changes regime at the midpoint of the 30 Aethyrs.", body)


# ---------------------------------------------------------------- 4. empire title nesting
def fig_nesting():
    n = res("12_empire")["C_nesting"]
    fams = [("CHASTOR", ["CHASTOR", "NOCHASTOR", "ADNOCHASTOR"]),
            ("CHAPH", ["CHAPH", "NOCHAPH", "ADNOCHAPH"]),
            ("ANZACH", ["ANZACH", "NOCHANZACH", "ADNOCHANZACH"]),
            ("CHEPHA", ["CHEPHA", "ACHEPHA", "ADNACHEPHA"])]
    vals = {}
    for fam in n.values():
        vals.update(fam)
    mx = max(vals.get(f[1][0], 1) for f in fams)
    body, base, x0 = [], 260, 40
    for gi, (name, forms) in enumerate(fams):
        gx = x0 + gi * 150
        for li, form in enumerate(forms):
            v = vals.get(form, 0)
            h = v / mx * 170
            x = gx + li * 38
            body.append(rect(x, base - h, 32, max(h, 1), [P6, P4, P2][li], 3))
            body.append(text(x + 16, base - h - 6, v, 11, INK, "middle"))
        body.append(text(gx + 54, base + 20, name, 13, INK, "middle", 600))
    body.append(f'<line x1="{x0-6}" y1="{base}" x2="{x0+590}" y2="{base}" stroke="{LINE}"/>')
    body += legend(40, 310, [(P6, "bare stem"), (P4, "+1 title (NO-/A-)"), (P2, "+2 titles (AD-NO-/AD-NA-)")])
    return svg("fig_empire_nesting", 660, 330, "Title nesting in the name-empire",
               "Each added title cuts frequency about threefold - rank-like compounding.", body)


# ---------------------------------------------------------------- 5. CHAST hive
def fig_hive():
    pv = res("11_lineages")["A_B_families"]["CHAST"]["prefix_variants"]
    items = list(pv.items())[:8]
    import math
    cx, cy, R = 330, 200, 130
    body = []
    for k, (pre, c) in enumerate(items):
        ang = -math.pi / 2 + k * 2 * math.pi / len(items)
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        body.append(f'<line x1="{cx}" y1="{cy}" x2="{x:.0f}" y2="{y:.0f}" stroke="{P4}" stroke-width="{0.6 + c/20:.1f}"/>')
    for k, (pre, c) in enumerate(items):
        ang = -math.pi / 2 + k * 2 * math.pi / len(items)
        x, y = cx + R * math.cos(ang), cy + R * math.sin(ang)
        body.append(rect(x - 52, y - 17, 104, 34, "#EEEDFE", 8, P4))
        body.append(text(x, y - 1, pre + "CHASTOR", 12, "#3C3489", "middle", 600))
        body.append(text(x, y + 12, f"{c}×", 11, "#534AB7", "middle"))
    body.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="#FAEEDA" stroke="{AMBER}"/>')
    body.append(text(cx, cy - 2, "CHAST", 15, "#633806", "middle", 600))
    body.append(text(cx, cy + 16, "the root", 11, "#854F0B", "middle"))
    body.append(text(24, 380, "Every subordinate = the queen's root + one prefix (its own mark). Shorter forms are more frequent.", 12, MUTED))
    return svg("fig_chastor_hive", 660, 400, "The CHASTOR hive",
               "The root CHAST is carried inside every prefixed name (counts = how often each prefix precedes it).", body)


# ---------------------------------------------------------------- 6. three stems across the tables
def fig_series():
    a11 = res("11_lineages")["series_per_table"]
    a14 = res("14_anzach")["series_per_table"]
    tabs = a11["tables"]
    series = [("GETH", a11["GETH"], TEAL), ("CHASTOR", a14["CHASTOR"], P6), ("ANZACH", a14["ANZACH"], CORAL)]
    mx = max(max(s) for _, s, _ in series)
    x0, w, base, hgt = 50, 560, 250, 170
    body = [f'<line x1="{x0}" y1="{base}" x2="{x0+w}" y2="{base}" stroke="{LINE}"/>']
    step = w / (len(tabs) - 1)
    for name, s, c in series:
        pts = " ".join(f"{x0 + i*step:.1f},{base - v/mx*hgt:.1f}" for i, v in enumerate(s))
        body.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round"/>')
    for i, t in enumerate(tabs):
        if t in (2, 10, 20, 26, 30, 40, 48):
            body.append(text(x0 + i * step, base + 16, t, 11, MUTED, "middle"))
    body.append(text(x0, base + 34, "table (book order)", 11, MUTED))
    body += legend(50, 300, [(TEAL, "GETH"), (P6, "CHASTOR"), (CORAL, "ANZACH")])
    return svg("fig_stems_across_tables", 640, 320, "Three great stems across the tables",
               "Occurrences per table, rows as written. The dip at 26–28 is a reading artefact: those tables run on diagonals (a18).", body)


# ---------------------------------------------------------------- 7. letter positional grammar
def fig_letter_grammar():
    r9 = res("09_letter_grammar")
    lv = load.leaves()
    words = [load.letters(w) for k in ("1a", "1b") for row in lv.get(k, []) for w in row.split()
             if len(load.letters(w)) >= 3]
    pos = {}
    for w in words:
        for i, c in enumerate(w):
            p = pos.setdefault(c, [0, 0, 0])
            p[0 if i == 0 else (2 if i == len(w) - 1 else 1)] += 1
    letters = sorted((c for c in pos if sum(pos[c]) >= 40), key=lambda c: -sum(pos[c]))[:20]
    x0, base, hgt = 40, 250, 170
    body = [f'<line x1="{x0-4}" y1="{base}" x2="{x0+len(letters)*29}" y2="{base}" stroke="{LINE}"/>']
    for i, c in enumerate(letters):
        t = sum(pos[c])
        pi, pf = pos[c][0] / t, pos[c][2] / t
        x = x0 + i * 29
        body.append(rect(x, base - pi * hgt, 11, pi * hgt, P6, 2))
        body.append(rect(x + 13, base - pf * hgt, 11, pf * hgt, TEAL, 2))
        strong = c in r9["A_positional_grammar"]["onset_letters"] + r9["A_positional_grammar"]["terminator_letters"]
        body.append(text(x + 12, base + 17, c, 12, INK, "middle", 600 if strong else 400))
    a = r9["A_positional_grammar"]
    body += legend(40, 300, [(P6, "share of the letter at word START"), (TEAL, "share at word END")])
    body.append(text(40, 322, f"MI(letter; position) = {a['mi_observed_bits']} bits vs null {a['mi_null_mean']} (z ≈ {a['z']}). "
                              f"Onsets {','.join(a['onset_letters'])}; terminator {','.join(a['terminator_letters'])}.", 12, MUTED))
    return svg("fig_letter_grammar", x0 * 2 + len(letters) * 29 + 20, 340,
               "The alphabet has positional roles", "Leaf 1 (the only word-spaced text): where each letter sits in a word.", body)


# ---------------------------------------------------------------- 8. the book's three formats
def fig_book_formats():
    r = res("15_book_geometry")
    per = r["E_per_table"]
    noise = {int(t) for t in r.get("C_tables_26_28_read_by_rows", {})}

    def cat(t):
        f = per[str(t)]["format"] if str(t) in per else ""
        if t == 1:
            return ("prophecy (word-spaced)", GRAY)
        if t in noise:
            return ("square written on diagonals (two currents)", AMBER)
        if f.startswith("full"):
            return ("full grid, written in rows", P6)
        if f == "diamond pair":
            return ("diamond pair, written on diagonals", TEAL)
        return ("diamond, irregular pairing", "#9FE1CB")
    x0, cw, y0 = 24, 13, 74
    body = []
    mx = max(v["name_density"] for v in per.values()) or 1
    for t in range(1, 49):
        name, c = cat(t)
        x = x0 + (t - 1) * cw
        body.append(rect(x, y0, cw - 2, 26, c, 2))
        d = per.get(str(t), {}).get("name_density", 0)
        h = d / mx * 110
        body.append(rect(x, y0 + 150 - h, cw - 2, max(h, 1), "#888780", 1))
        if t in (1, 5, 10, 20, 26, 29, 40, 44, 48):
            body.append(text(x + (cw - 2) / 2, y0 + 168, t, 10, MUTED, "middle"))
    body.append(text(x0, y0 + 38, "name density per table (normalised by length):", 11, MUTED))
    seen, items = set(), []
    for t in range(1, 49):
        nm, c = cat(t)
        if nm not in seen:
            seen.add(nm)
            items.append((c, nm))
    body += legend(24, y0 + 196, items[:3])
    body += legend(24, y0 + 216, items[3:])
    return svg("fig_book_formats", x0 * 2 + 48 * cw, 310, "The book has distinct physical formats",
               "Top: format of each table. Bottom: recurring-name share read by rows (26–28 need their diagonal reading, see a18).", body)


# ---------------------------------------------------------------- 9. diamond geometry
def fig_diamond():
    r = res("15_book_geometry")["B_text_direction_in_diamond_tables"]
    s, body = 3, []
    def diamond(cx, y0, odd, color):
        out = []
        n = 49 if odd else 48
        for i in range(n):
            L = 2 * min(i, n - 1 - i) + (1 if odd else 2)
            out.append(rect(cx - L * s / 2, y0 + i * s, L * s, s - 0.6, color, 0))
        return out
    body += diamond(110, 80, True, P6)
    body.append(text(110, 240, "side b: 1,3,5…49…1", 11, MUTED, "middle"))
    body.append(text(110, 254, "1201 cells", 11, MUTED, "middle"))
    body.append(text(200, 158, "+", 22, INK, "middle"))
    body += diamond(290, 80, False, TEAL)
    body.append(text(290, 240, "side a: 2,4…48,48…2", 11, MUTED, "middle"))
    body.append(text(290, 254, "1200 cells", 11, MUTED, "middle"))
    body.append(text(380, 158, "=", 22, INK, "middle"))
    body.append('<defs><pattern id="cb" width="6" height="6" patternUnits="userSpaceOnUse">'
                f'<rect width="3" height="3" fill="{P6}"/><rect x="3" y="3" width="3" height="3" fill="{P6}"/>'
                f'<rect x="3" width="3" height="3" fill="{TEAL}"/><rect y="3" width="3" height="3" fill="{TEAL}"/></pattern></defs>')
    body.append(f'<rect x="400" y="80" width="147" height="147" fill="url(#cb)"/>')
    body.append(text(473, 240, "one 49×49 table", 11, MUTED, "middle"))
    body.append(text(473, 254, "2401 = 49², chessboard colours", 11, MUTED, "middle"))
    rows_ = [("diagonals (as written)", r["diamond_rows_as_written"]["name_density"], TEAL),
             ("rebuilt rows", r["rebuilt_horizontal"]["name_density"], GRAY),
             ("rebuilt columns", r["rebuilt_vertical"]["name_density"], GRAY),
             ("full tables 2–25 (rows)", r["reference_full_tables_2_25"]["name_density"], P6)]
    body.append(text(24, 292, "Where does the language run? Share of recurring names along each reading:", 12, INK))
    for i, (lab, v, c) in enumerate(rows_):
        y = 304 + i * 22
        body.append(text(24, y + 12, lab, 12, MUTED))
        body.append(rect(200, y + 2, max(v / 0.32 * 380, 1), 13, c, 2))
        body.append(text(206 + v / 0.32 * 380, y + 13, f"{v:.3f}", 11, INK))
    return svg("fig_diamond_geometry", 620, 400, "Tables 29–48: one grid, two chessboard colours, written on the diagonals",
               "Each side of the leaf is one colour of a 49×49 chessboard, rotated 45°.", body)


# ---------------------------------------------------------------- 10. no doubled letters
def fig_doubled():
    r = res("15_book_geometry")["D_no_doubled_letters"]
    items = [("Loagaeth full tables", r["full_tables_2_25"], P6),
             ("Loagaeth diamond tables", r["diamond_tables_29_48"], TEAL),
             ("Leaf 1 (prophecy)", r["leaf1_words"], GRAY),
             ("The 48 Calls", r["calls_words"] or 0, BLUE),
             ("Tables 26–28 read on diagonals", r.get("tables_26_28_read_on_diagonals") or 0, AMBER),
             ("Tables 26–28 read by rows (wrong)", r["tables_26_28_read_by_rows"], CORAL)]
    ch = r["chance_from_letter_freq"]
    mx = max(ch, max(v for _, v, _ in items)) * 1.1
    body, x0, wmax = [], 200, 360
    for i, (lab, v, c) in enumerate(items):
        y = 80 + i * 34
        body.append(text(24, y + 15, lab, 12, INK))
        body.append(rect(x0, y + 3, max(v / mx * wmax, 1), 18, c, 3))
        body.append(text(x0 + v / mx * wmax + 6, y + 17, f"{v*100:.2f}%", 11, INK))
    cx = x0 + ch / mx * wmax
    body.append(f'<line x1="{cx:.0f}" y1="72" x2="{cx:.0f}" y2="252" stroke="{INK}" stroke-dasharray="4 3"/>')
    body.append(text(cx, 268, f"chance {ch*100:.1f}%", 11, INK, "middle"))
    return svg("fig_doubled_letters", 620, 290, "The no-doubled-letter rule",
               "Share of adjacent identical letters. The Loagaeth avoids them far below chance — when read in its own direction.", body)


# ---------------------------------------------------------------- 11. every letter, with gematria value
def fig_letter_counts():
    r = res("16_letters")["A_letters"]
    r = [x for x in r if x["count"] >= 100]
    mx = max(x["count"] for x in r)
    body, x0, base = [], 40, 250
    for i, x in enumerate(r):
        h = x["count"] / mx * 170
        bx = x0 + i * 27
        body.append(rect(bx, base - h, 20, h, P6 if i < 3 else P4, 3))
        body.append(text(bx + 10, base - h - 5, x["count"], 9, INK, "middle"))
        body.append(text(bx + 10, base + 15, x["letter"], 12, INK, "middle", 600))
        gd = x["values"].get("golden_dawn_coluna__F08")
        body.append(text(bx + 10, base + 30, gd if gd is not None else "–", 9, MUTED, "middle"))
    body.append(f'<line x1="{x0-4}" y1="{base}" x2="{x0+len(r)*27}" y2="{base}" stroke="{LINE}"/>')
    body.append(text(x0, base + 50, "Second row under each letter: its value in the Golden Dawn Enochian gematria (reference only).", 11, MUTED))
    body.append(text(x0, base + 66, "The top letters A, O, N, H, L, D… spell no attested name (tested up to 8 letters against a null).", 11, MUTED))
    return svg("fig_letter_counts", x0 * 2 + len(r) * 27, 340, "Every letter of the Loagaeth, counted",
               "Occurrences in the dense tables 2–48. A alone is 19% of the text.", body)


# ---------------------------------------------------------------- 12. letters by segment (heat table)
def fig_letters_segments():
    sh = res("16_letters")["E_segments"]["shares_percent"]
    segs = list(sh)
    lab = {"opening_2_5": "opening 2–5", "heartland_6_25": "heartland 6–25", "diamonds_29_43": "diamonds 29–43", "end_44_48": "end 44–48"}
    letters = list(sh[segs[0]])
    x0, y0, cw, ch = 120, 70, 28, 24
    body = []
    vmax = max(v for s in segs for v in sh[s].values())
    for j, L in enumerate(letters):
        body.append(text(x0 + j * cw + cw / 2, y0 - 6, L, 12, INK, "middle", 600))
    for i, s in enumerate(segs):
        body.append(text(x0 - 8, y0 + i * ch + 16, lab.get(s, s), 12, INK, "end"))
        for j, L in enumerate(letters):
            v = sh[s][L]
            a = 0.08 + 0.92 * (v / vmax) ** 0.6
            body.append(f'<rect x="{x0+j*cw}" y="{y0+i*ch}" width="{cw-2}" height="{ch-2}" rx="2" fill="{P6}" fill-opacity="{a:.2f}"/>')
            body.append(text(x0 + j * cw + cw / 2, y0 + i * ch + 15, f"{v:.0f}" if v >= 1 else f"{v:.1f}", 9,
                             "#FFFFFF" if a > 0.55 else INK, "middle"))
    s16 = res("16_letters")["E_segments"]
    body.append(text(24, y0 + 4 * ch + 26, f"Letter mix differs by segment far beyond chance (χ² {s16['chi2']} vs tables shuffled ≤ {s16['null_max']}).", 12, MUTED))
    body.append(text(24, y0 + 4 * ch + 44, "Watch A and U: in the end segment A falls from ~20% to ~6% and U rises to ~10% — the U register.", 12, MUTED))
    return svg("fig_letters_by_segment", x0 + len(letters) * cw + 30, y0 + 4 * ch + 64, "Each realm has its own letter mix",
               "Share (%) of each letter inside each segment of the book.", body)


# ---------------------------------------------------------------- 13. U register
def fig_u_register():
    u = res("16_letters")["F_u_register"]
    ov = u["overlap_with_heartland"]
    items = [("as written", ov["as_is"], GRAY), ("A→E", ov["A->E"], GRAY2), ("A→I", ov["A->I"], GRAY2),
             ("A→O", ov["A->O"], GRAY2), ("A→U", ov["A->U"], P6)]
    mx = max(v for _, v, _ in items)
    body, x0 = [], 150
    for i, (lab, v, c) in enumerate(items):
        y = 74 + i * 30
        body.append(text(24, y + 15, lab, 12, INK))
        body.append(rect(x0, y + 3, v / mx * 300, 18, c, 3))
        body.append(text(x0 + v / mx * 300 + 6, y + 17, v, 11, INK))
    body.append(text(24, 246, "Recurring 5-grams of the end tables (44–48) also found in the heartland (6–25):", 12, INK))
    ex = u["examples"][:8]
    for i, e in enumerate(ex):
        body.append(text(24 + (i % 4) * 150, 270 + (i // 4) * 20, f"{e['heartland']} → {e['end']}", 12, "#3C3489"))
    return svg("fig_u_register", 640, 320, "The end of the book speaks the heartland's names in a U register",
               "Only replacing A by U brings the two segments together; other vowel swaps push them apart.", body)


# ---------------------------------------------------------------- 14. row edges
def fig_row_edges():
    d = res("16_letters")["D_space"]
    st, en = d["row_start_enrichment"][:5], d["row_end_enrichment"][:5]
    mx = max(v for _, v in st + en)
    body = [text(24, 76, "first letter of a row", 12, INK, weight=600), text(340, 76, "last letter of a row", 12, INK, weight=600)]
    for i, (L, v) in enumerate(st):
        y = 86 + i * 28
        body.append(text(24, y + 15, L, 13, INK, weight=600))
        body.append(rect(44, y + 3, v / mx * 230, 18, P6, 3))
        body.append(text(50 + v / mx * 230, y + 17, f"{v}×", 11, INK))
    for i, (L, v) in enumerate(en):
        y = 86 + i * 28
        body.append(text(340, y + 15, L, 13, INK, weight=600))
        body.append(rect(360, y + 3, v / mx * 230, 18, TEAL, 3))
        body.append(text(366 + v / mx * 230, y + 17, f"{v}×", 11, INK))
    body.append(text(24, 246, "Ratio vs the same letter in the middle of rows. Rows open with onsets and close with terminators:", 12, MUTED))
    body.append(text(24, 262, "the 49-letter lines follow word boundaries. Away from the edges, left and right are alike.", 12, MUTED))
    return svg("fig_row_edges", 640, 280, "Rows start and end on word boundaries",
               "Full 49×49 grids, tables 2–25.", body)


# ---------------------------------------------------------------- 15. the 7x7 plan of the book
def fig_plan_7x7():
    seg = {}
    for t in range(1, 50):
        if t == 1:
            seg[t] = ("prophecy", GRAY)
        elif t <= 5:
            seg[t] = ("opening", GREEN)
        elif t <= 25:
            seg[t] = ("CHASTOR heartland", P6)
        elif t <= 28:
            seg[t] = ("squares on diagonals", AMBER)
        elif t <= 43:
            seg[t] = ("diamonds", TEAL)
        elif t <= 48:
            seg[t] = ("end · U register", BLUE)
        else:
            seg[t] = ("missing", "#F1EFE8")
    x0, y0, cs = 160, 74, 44
    body = []
    for w in range(7):
        body.append(text(x0 - 10, y0 + w * cs + 27, f"week {w+1}", 12, MUTED, "end"))
        for p in range(7):
            t = w * 7 + p + 1
            nm, c = seg[t]
            body.append(rect(x0 + p * cs, y0 + w * cs, cs - 4, cs - 4, c, 4, "#C3C2B7" if t == 49 else None))
            body.append(text(x0 + p * cs + (cs - 4) / 2, y0 + w * cs + 25, t, 12,
                             "#FFFFFF" if c in (P6, TEAL, BLUE, CORAL) else INK, "middle", 600 if t == 25 else 400))
    c25x, c25y = x0 + 3 * cs, y0 + 3 * cs
    body.append(f'<rect x="{c25x-3}" y="{c25y-3}" width="{cs+2}" height="{cs+2}" rx="6" fill="none" stroke="{AMBER}" stroke-width="2.5"/>')
    lx = x0 + 7 * cs + 20
    seen = []
    for t in range(1, 50):
        if seg[t] not in seen:
            seen.append(seg[t])
    for i, (nm, c) in enumerate(seen):
        body.append(rect(lx, y0 + i * 24, 12, 12, c, 2))
        body.append(text(lx + 18, y0 + i * 24 + 11, nm, 12, MUTED))
    body.append(text(lx, y0 + len(seen) * 24 + 16, "gold frame: table 25, centre of", 12, AMBER))
    body.append(text(lx, y0 + len(seen) * 24 + 32, "the plan; writing turns from rows", 12, AMBER))
    body.append(text(lx, y0 + len(seen) * 24 + 48, "to diagonals between 25a and 25b", 12, AMBER))
    return svg("fig_plan_7x7", lx + 230, y0 + 7 * cs + 30, "The 49 tables on the 7×7 plan",
               "49 sides in rows, then 49 sides on diagonals: the turn falls at the exact middle of the book.", body)


# ---------------------------------------------------------------- 17. the two currents (tables 25b-28b)
def fig_two_currents():
    d = res("18_markup_decoding")
    faces = d["B_faces"]
    body = []
    # schematic: a 9x9 chessboard with the two currents
    x0, y0, s = 34, 80, 18
    for r in range(9):
        for c in range(9):
            body.append(rect(x0 + c * s, y0 + r * s, s - 1, s - 1, P2 if (r + c) % 2 == 0 else "#9FE1CB", 1))
    body.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M1 1L8 5L1 9" fill="none" stroke="context-stroke" stroke-width="1.6"/></marker></defs>')
    for k in (0, 2, 4):
        body.append(f'<line x1="{x0+k*s+4}" y1="{y0+4}" x2="{x0+(8)*s+10-k*0}" y2="{y0+(8-k)*s+10}" stroke="{P6}" stroke-width="2" marker-end="url(#ah)"/>')
    for k in (1, 3, 5):
        body.append(f'<line x1="{x0+8*s+10}" y1="{y0+(8-k+1)*s-4}" x2="{x0+(k-1)*s+6}" y2="{y0+6}" stroke="{TEAL}" stroke-width="2" marker-end="url(#ah)"/>')
    body.append(text(x0, y0 + 9 * s + 18, "colour 1 flows ↘, colour 2 flows ↖", 11, MUTED))
    # bars: rows vs decoded per face
    bx, by = 250, 74
    body.append(text(bx, by, "recurring-name share", 12, INK, weight=600))
    keys = list(faces)
    for i, k in enumerate(keys):
        y = by + 14 + i * 26
        f = faces[k]
        body.append(text(bx, y + 13, k, 12, INK))
        for j, (lab, v, c) in enumerate([("rows", f["rows_as_written"]["names"], CORAL),
                                         ("↘", f["stream_down_right"]["names"], P6),
                                         ("left", f["stream_leftward"]["names"], TEAL)]):
            body.append(rect(bx + 34 + j * 112, y + 2, max(v / 0.45 * 100, 1), 15, c, 2))
            body.append(text(bx + 34 + j * 112 + max(v / 0.45 * 100, 1) + 3, y + 13, f"{v:.2f}", 10, INK))
    ctrl = d["B_control_row_tables_read_diagonally"]["max_names_any_diagonal_reading"]
    body.append(text(bx, by + 14 + len(keys) * 26 + 14,
                     f"Control: 35 ordinary row tables read the same way reach at most {ctrl:.3f}.", 11, MUTED))
    body += legend(bx, by + 14 + len(keys) * 26 + 34, [(CORAL, "read by rows"), (P6, "colour 1 ↘"), (TEAL, "colour 2 leftward")])
    return svg("fig_two_currents", 640, by + len(keys) * 26 + 70, "Tables 25b–28b: two currents on the diagonals",
               "Peterson's marks separate the chessboard colours; each colour read on its diagonals is ordinary Loagaeth.", body)


# ---------------------------------------------------------------- 18. machine vs language
def fig_machine():
    d = res("19_machine")
    lm = d["D_language_model_bits_per_letter"]
    items = [("held-out heartland", lm["heldout_rows_2_24_crossval"], P6),
             ("tables 25b–28 on diagonals", lm["decoded_diagonals_25b_28"], AMBER),
             ("diamonds 29–43", lm["diamonds_29_43"], TEAL),
             ("end 44–48 with U→A", lm["end_44_48_with_U_back_to_A"], BLUE),
             ("end 44–48 as written", lm["end_44_48_as_written"], "#85B7EB"),
             ("tables 26–28 by rows", lm["same_tables_read_by_rows"], CORAL),
             ("shuffled letters", lm["shuffled_heartland"], GRAY)]
    body, x0 = [], 210
    body.append(text(24, 76, "A character language model trained on tables 2–24: bits per letter (lower = it understands)", 12, INK, weight=600))
    for i, (lab, v, c) in enumerate(items):
        y = 86 + i * 26
        body.append(text(24, y + 14, lab, 12, INK))
        body.append(rect(x0, y + 2, v / 8 * 330, 17, c, 3))
        body.append(text(x0 + v / 8 * 330 + 6, y + 15, f"{v:.2f}", 11, INK))
    sy = 86 + len(items) * 26 + 24
    body.append(text(24, sy, "Periodicity (best self-match at a fixed period): machine vs language", 12, INK, weight=600))
    per = d["A_periodicity"]
    rows_ = []
    if isinstance(per.get("soyga_aries_columns"), list):
        for c in per["soyga_aries_columns"][:3]:
            rows_.append((f"Soyga Aries, column {c['column']} (period {c['period']})", c["best_match"], AMBER))
    rows_ += [("Loagaeth rows", per["loagaeth_rows_2_24"], P6), ("Loagaeth shuffled", per["loagaeth_rows_shuffled"], GRAY)]
    for i, (lab, v, c) in enumerate(rows_):
        y = sy + 10 + i * 24
        body.append(text(24, y + 14, lab, 12, INK))
        body.append(rect(x0 + 60, y + 2, v * 300, 16, c, 3))
        body.append(text(x0 + 66 + v * 300, y + 15, f"{v:.2f}", 11, INK))
    return svg("fig_machine_vs_language", 660, sy + 10 + len(rows_) * 24 + 24, "Machine or language?",
               "The Soyga table is generated by a rule (periodic); the Loagaeth reads like a language.", body)


# ---------------------------------------------------------------- 19. energy of letters by realm
def fig_energy():
    d = res("20_energy_fibonacci_gd")["A_energy_by_segment"]
    gd = d["golden_dawn_coluna__F08"]["mean_by_segment"]
    sp = d["surprisal_bits"]["mean_by_segment"]
    segs = list(gd)
    lab = {"opening_2_5": "opening", "heartland_6_24": "heartland", "diamonds_29_43": "diamonds", "end_44_48": "end"}
    mx = max(gd.values())
    body, x0, base = [], 60, 240
    body.append(text(x0, 74, "Mean Golden Dawn value per letter", 12, INK, weight=600))
    for i, s in enumerate(segs):
        v = gd[s]
        h = v / mx * 140
        body.append(rect(x0 + i * 70, base - h, 46, h, P6, 3))
        body.append(text(x0 + i * 70 + 23, base - h - 6, f"{v:.0f}", 11, INK, "middle"))
        body.append(text(x0 + i * 70 + 23, base + 16, lab[s], 11, INK, "middle"))
    x1 = 380
    mx2 = max(sp.values())
    mn2 = min(sp.values()) - 0.2
    body.append(text(x1, 74, "Information per letter (bits)", 12, INK, weight=600))
    for i, s in enumerate(segs):
        v = sp[s]
        h = (v - mn2) / (mx2 - mn2) * 140
        body.append(rect(x1 + i * 62, base - h, 40, h, TEAL, 3))
        body.append(text(x1 + i * 62 + 20, base - h - 6, f"{v:.2f}", 11, INK, "middle"))
        body.append(text(x1 + i * 62 + 20, base + 16, lab[s], 11, INK, "middle"))
    s20 = res("20_energy_fibonacci_gd")["A_summary"]
    body.append(text(24, 284, f"End denser than heartland in {len(s20['end_denser_after_bonferroni'])} of {s20['systems']} measures (Bonferroni);"
                              f" with U turned back into A only {len(s20['still_denser_with_U_as_A'])} remain.", 11, MUTED))
    body.append(text(24, 300, "The rise is carried mostly by the A→U shift (U = 400, A = 1 in the Golden Dawn table).", 11, MUTED))
    return svg("fig_energy_by_realm", 660, 318, "Is the end of the book 'denser'?",
               "Letter value and information per letter, by segment.", body)


# ---------------------------------------------------------------- 16. the two houses
def fig_houses():
    k = res("17_kingdom")["D_correlation_zone"]
    dens = k["house_density_per_1000_letters"]
    segs = ["opening", "heartland", "diamonds", "end"]
    hn = [("ADNOCHA", P6), ("NOCHAPH", P4), ("NODAX", P2), ("ALGETH", TEAL), ("ACLAX", "#5DCAA5")]
    mx = max(dens[n][s] for n, _ in hn for s in segs) or 1
    body, x0, base = [], 50, 230
    for si, s in enumerate(segs):
        gx = x0 + si * 140
        for ni, (n, c) in enumerate(hn):
            v = dens[n][s]
            h = v / mx * 140
            body.append(rect(gx + ni * 22, base - h, 18, max(h, 1), c, 2))
        body.append(text(gx + 52, base + 18, s, 12, INK, "middle"))
    body.append(f'<line x1="{x0-4}" y1="{base}" x2="{x0+560}" y2="{base}" stroke="{LINE}"/>')
    body += legend(50, 274, [(c, n) for n, c in hn])
    hw = k["houses_within_segments"]
    a = hw["ADNOCHA~ACLAX"]
    body.append(text(50, 302, f"Beyond overall density they exclude each other table by table — ADNOCHA × ACLAX r = {a['heartland_6_25']['r']} "
                              f"(heartland), {a['diamonds_29_43']['r']} (diamonds).", 11, MUTED))
    body.append(text(50, 318, "Purple = NOCHA house, green = GETH/ACLAX house. Bars: occurrences per 1000 letters in each segment.", 11, MUTED))
    return svg("fig_two_houses", 660, 336, "Two houses that alternate across the tables",
               "The NOCHA house leads the first half; the GETH/ACLAX house holds or grows in the second.", body)


# ---------------------------------------------------------------- 20. Peterson's index checked
def fig_index_check():
    a = res("21_index_heptarchy_numbers")["A_index"]
    v = a["verification"]
    parts = [("found as a word on the stated line", v["whole_word"], P6),
             ("inside a dense / longer token", v["inside_a_longer_or_dense_token"], P2),
             ("variant reading (1–2 letters differ)", v["variant_reading"], AMBER),
             ("not found", v["not_found"], CORAL)]
    tot = sum(n for _, n, _ in parts)
    body, x0, W = [], 24, 600
    body.append(text(x0, 78, f"{a['references']} line references of the index ({a['entries']} entries), checked against our transcription", 12, INK, weight=600))
    cx = x0
    for lab, n, c in parts:
        w = n / tot * W
        body.append(rect(cx, 88, max(w, 1.5), 22, c, 2))
        cx += w
    for i, (lab, n, c) in enumerate(parts):
        body.append(rect(x0, 124 + i * 20, 12, 12, c, 2))
        body.append(text(x0 + 18, 134 + i * 20, f"{lab}: {n} ({n / tot * 100:.1f}%)", 12, MUTED))
    y = 226
    body.append(text(x0, y, "Line map, leaf 1b: index line → our row (purple = same row, amber = one row lower)", 12, INK, weight=600))
    for i, s in enumerate(a["line_shift_1b"]):
        c = P6 if s == 0 else AMBER
        body.append(rect(x0 + i * 12, y + 10, 10, 18, c, 1))
        if (i + 1) in (1, 20, 49):
            body.append(text(x0 + i * 12 + 5, y + 44, str(i + 1), 10, MUTED, "middle"))
    body.append(text(x0, y + 64, "Manuscript line 20 of leaf 1b is split over two rows in the transcription, so 1b also has 49 lines.", 11, MUTED))
    body.append(text(x0, y + 80, "The index covers only leaf 1 (t1 = 1a, t2 = 1b) and carries no meanings: it is a concordance.", 11, MUTED))
    return svg("fig_index_check", 660, y + 98, "Peterson's Index Verborum, checked line by line",
               "Almost every reference lands on the stated line; the differences are old readings (Z/X, U/B, N/U).", body)


# ---------------------------------------------------------------- 21. dense lines: Peterson's division vs our model
def fig_dense_division():
    b = res("21_index_heptarchy_numbers")["B_segmentation_gold"]
    body, x0 = [], 24
    body.append(text(x0, 78, "The nine unspaced 49-letter lines closing leaf 1b — ▼ Peterson's word breaks, ▲ our model's", 12, INK, weight=600))
    cw = 12.4
    for k, L in enumerate(b["per_line"]):
        y = 96 + k * 40
        g, m = set(L["gold_cut_positions"]), set(L["model_cut_positions"])
        body.append(text(x0, y + 18, f"row {L['row']}", 10, MUTED))
        for i, ch in enumerate(L["letters"]):
            body.append(text(x0 + 52 + i * cw, y + 18, ch, 11, INK, "middle"))
        for p in range(1, len(L["letters"])):
            xx = x0 + 52 + (p - 0.5) * cw
            if p in g:
                body.append(text(xx, y + 6, "▼", 8, P6, "middle"))
            if p in m:
                body.append(text(xx, y + 31, "▲", 8, TEAL if p in g else GRAY, "middle"))
        body.append(text(x0 + 52 + 49 * cw + 8, y + 18, f"F1 {L['F1']:.2f}", 10, MUTED))
    yy = 96 + len(b["per_line"]) * 40 + 8
    m, r = b["model"], b["random_cuts_same_number"]
    body.append(text(x0, yy, f"Our word model (trained only on the spaced lines of leaf 1): F1 {m['F1']} (precision {m['precision']}, recall {m['recall']}).", 11, INK))
    body.append(text(x0, yy + 16, f"Random breaks, same number: F1 {r['F1_mean']} (95th pct {r['F1_95th']}); p < 0.0005. Teal ▲ = a break both agree on.", 11, MUTED))
    body.append(text(x0, yy + 32, "Peterson's breaks are an editor's reading (1986), not Dee's; the model over-cuts but finds his breaks twice as often as chance.", 11, MUTED))
    return svg("fig_dense_division", 760, yy + 50, "A gold standard for dividing dense Loagaeth text",
               "Peterson's index divides the unspaced lines into words — an independent check on word segmentation.", body)


# ---------------------------------------------------------------- 22. robustness to the transcription
def fig_robustness():
    A = res("22_robustness_and_depth")["A_robustness"]
    vs = [("as transcribed", "as_transcribed"), ("Z = X", "Z_equals_X"), ("U = V", "U_equals_V"),
          ("U read as A", "U_read_as_A"), ("only exact 49×49 sides", "only_clean_49_sides")]
    cols = [("doubled letters\n(obs/exp, <1 = rule)", "doubled_obs_over_exp", lambda v: f"{v:.2f}", lambda v: v < 0.5),
            ("row edges z", "row_edge_z", lambda v: f"{v:.0f}", lambda v: v > 3),
            ("segments χ² / null max", None, None, None),
            ("CHASTOR territory z", "territory_z", lambda v: f"{v:.1f}", lambda v: v > 1.96),
            ("CHASTOR", None, None, None)]
    body, x0, y0 = [], 24, 96
    heads = ["doubled (obs/exp)", "row edges z", "segments χ² / null", "territory z", "CHASTOR"]
    for j, h in enumerate(heads):
        body.append(text(220 + j * 96, 82, h, 11, INK, "middle", 600))
    for i, (lab, k) in enumerate(vs + [("2% look-alike noise ×10", "noise")]):
        y = y0 + i * 30
        body.append(text(x0, y + 16, lab, 12, INK))
        if k == "noise":
            m = A["noise_2pct_x10"]
            cells = [(f"{m['doubled_obs_over_exp'][0]:.2f}–{m['doubled_obs_over_exp'][1]:.2f}", True),
                     (f"{m['row_edge_z'][0]:.0f}–{m['row_edge_z'][1]:.0f}", True),
                     (f"{m['segments_chi2'][0]}–{m['segments_chi2'][1]}", True),
                     (f"{m['territory_z'][0]}–{m['territory_z'][1]}", m["territory_z"][0] > 1.96),
                     (f"{m['CHASTOR'][0]}–{m['CHASTOR'][1]}", True)]
        else:
            m = A[k]
            cells = [(f"{m['doubled_obs_over_exp']:.2f}", m["doubled_obs_over_exp"] < 0.5),
                     (f"{m['row_edge_z']:.0f}", m["row_edge_z"] > 3),
                     (f"{m['segments_chi2']} / {m['segments_null_max']}", m["segments_chi2"] > m["segments_null_max"]),
                     (f"{m['territory_z']}", m["territory_z"] > 1.96),
                     (f"{m['names']['CHASTOR']}", True)]
        for j, (s, ok) in enumerate(cells):
            body.append(rect(220 + j * 96 - 44, y + 2, 88, 22, "#E1F5EE" if ok else "#FAECE7", 3))
            body.append(text(220 + j * 96, y + 17, s, 11, INK, "middle"))
    yy = y0 + 6 * 30 + 16
    body.append(text(x0, yy, "Green = the finding holds under that reading; red = it weakens below the usual threshold.", 11, MUTED))
    body.append(text(x0, yy + 16, "The grammar (no doubled letters, row edges) and the segment differences hold everywhere. The CHASTOR", 11, MUTED))
    body.append(text(x0, yy + 32, "territory is moderate (density z ≈ 2) and fades if U is read as A: part of it is the U register at the end.", 11, MUTED))
    return svg("fig_robustness", 720, yy + 50, "Are we looking wrong? The findings under other readings",
               "Each core result recomputed on altered transcriptions.", body)


# ---------------------------------------------------------------- 23. roads through the diamonds
def fig_diamond_roads():
    C = res("22_robustness_and_depth")["C_diamond_roads"]
    body, x0 = [], 230
    body.append(text(24, 78, "Diamond pairs 29–43 rebuilt as squares, read every way (letter model of the heartland)", 12, INK, weight=600))
    for i, (k, v) in enumerate(C.items()):
        y = 90 + i * 24
        b = v["bits_per_letter"]
        body.append(text(24, y + 14, k, 12, INK))
        body.append(rect(x0, y + 2, b / 8 * 330, 16, AMBER if i == 0 else GRAY, 3))
        body.append(text(x0 + b / 8 * 330 + 6, y + 15, f"{b:.2f} bits · names {v['names_per_1000']}/1000", 11, INK))
    yy = 90 + len(C) * 24 + 16
    body.append(text(24, yy, "Only one road reads: the anti-diagonals, in the direction they are stored. Every other path is noise", 11, MUTED))
    body.append(text(24, yy + 16, "(≈ 7.8 bits, no names); the same road backwards keeps the information but loses every name.", 11, MUTED))
    return svg("fig_diamond_roads", 660, yy + 34, "Is there another way to read the diamonds?",
               "Lower bits = the model recognises the language.", body)


# ---------------------------------------------------------------- 24. memory of the text
def fig_mi_decay():
    D = res("22_robustness_and_depth")["D1_mutual_information"]
    ds = D["distance"][:17]
    series = [("Loagaeth (tables 2–25a)", D["loagaeth"], P6), ("Markov-3 surrogate", D["markov3_surrogate"], CORAL),
              ("letters shuffled inside each side", D["shuffled_within_each_side"], GRAY)]
    x0, y0, W, H = 70, 80, 540, 220

    def X(d):
        return x0 + math.log(d) / math.log(64) * W

    def Y(v):
        v = max(v, 0.003)
        return y0 + H - (math.log10(v) - math.log10(0.003)) / (math.log10(1) - math.log10(0.003)) * H
    body = [f'<line x1="{x0}" y1="{y0+H}" x2="{x0+W}" y2="{y0+H}" stroke="{LINE}"/>',
            f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+H}" stroke="{LINE}"/>']
    for d in (1, 2, 4, 8, 16, 32, 64):
        body.append(text(X(d), y0 + H + 16, str(d), 10, MUTED, "middle"))
    for v in (0.01, 0.1, 1):
        body.append(text(x0 - 6, Y(v) + 4, str(v), 10, MUTED, "end"))
    for lab, ys, c in series:
        pts = " ".join(f"{X(d):.1f},{Y(v):.1f}" for d, v in zip(ds, ys))
        body.append(f'<polyline points="{pts}" fill="none" stroke="{c}" stroke-width="2"/>')
    body += legend(x0, y0 + H + 42, [(c, l) for l, _, c in series])
    body.append(text(x0, y0 + H + 66, "Distance in letters (log). From 4 to ~12 letters the text remembers more than a 3-letter model: the length of", 11, MUTED))
    body.append(text(x0, y0 + H + 82, "its words and names. Beyond that, all memory is the change of letter mix from side to side — no long-range code.", 11, MUTED))
    return svg("fig_mi_decay", 660, y0 + H + 100, "How far does a letter 'know' its neighbours?",
               "Mutual information between letters d apart (bits, log scale).", body)


# ---------------------------------------------------------------- 25. names found without supervision
def fig_new_names():
    d = res("23_name_discovery")
    new = d["A_new_names_outside_known_families"][:18]
    a = d["A_candidates"]
    mx = max(c["count"] for c in new)
    body, x0 = [], 150
    body.append(text(24, 78, f"{a['survivors']} strings behave like recurring words beyond chance (Markov-3 surrogate of the same book: {a['surrogate_survivors']})", 12, INK, weight=600))
    for i, c in enumerate(new):
        y = 90 + i * 22
        body.append(text(24, y + 13, c["name"], 12, INK, weight=600))
        body.append(rect(x0, y + 2, c["count"] / mx * 260, 14, P6, 3))
        body.append(text(x0 + c["count"] / mx * 260 + 6, y + 13,
                         f"{c['count']}× · {c['tables']} tables · z {c['z']} · tables {c['first_last_table'][0]}–{c['first_last_table'][1]}", 10, MUTED))
    y = 90 + len(new) * 22 + 14
    body.append(text(24, y, "Families found (one name = another ± 1–2 letters at an end, or a vowel swapped):", 12, INK, weight=600))
    for i, f in enumerate(d["C_families"]["largest"][:6]):
        body.append(text(24, y + 18 + i * 17, "  ·  ".join(f), 11, P6 if i % 2 == 0 else TEAL))
    yy = y + 18 + 6 * 17 + 10
    body.append(text(24, yy, f"Families of 3+: {d['C_families']['families_size_ge3']} in the book, {d['C_families']['surrogate_families_size_ge3']} in the surrogate. "
                             "NACHO is the vowel mirror of NOCHA (N·A·CH·O vs N·O·CH·A).", 11, MUTED))
    return svg("fig_new_names", 720, yy + 20, "New recurring names, found by the text itself",
               "Strings with varied letters on both sides (word-like) that recur far beyond a Markov-3 model.", body)


# ---------------------------------------------------------------- 26. dialect map
def fig_dialects():
    m = res("24_book_architecture")["C_dialects"]["rows_trained_on_cols_read"]
    segs = list(m)
    vals = [m[a][b] for a in segs for b in segs]
    lo, hi = min(vals), max(vals)
    body, x0, y0, cw = [], 170, 100, 86
    for j, b in enumerate(segs):
        body.append(text(x0 + j * cw + cw / 2, y0 - 8, b, 11, INK, "middle", 600))
    for i, a in enumerate(segs):
        body.append(text(x0 - 8, y0 + i * 34 + 21, f"model of {a}", 11, INK, "end"))
        for j, b in enumerate(segs):
            v = m[a][b]
            t = (v - lo) / (hi - lo)
            col = f"rgb({int(83 + t * 160)},{int(74 + t * 160)},{int(183 + t * 60)})"
            body.append(rect(x0 + j * cw + 2, y0 + i * 34, cw - 4, 30, col, 3))
            body.append(text(x0 + j * cw + cw / 2, y0 + i * 34 + 20, f"{v:.2f}", 11, "#FFFFFF" if t < 0.5 else INK, "middle"))
    yy = y0 + len(segs) * 34 + 22
    body.append(text(24, yy, "Bits per letter when the model of one realm (row) reads another (column); darker = closer speech.", 11, MUTED))
    body.append(text(24, yy + 16, "Each realm reads its neighbours best: opening → heartland → 26–28 → diamonds → end is a chain, and the", 11, MUTED))
    body.append(text(24, yy + 32, "end is closest to the diamonds and farthest from the opening — the language drifts along the book.", 11, MUTED))
    return svg("fig_dialects", 660, yy + 50, "A dialect map of the book", "Cross-reading letter models trained on each realm.", body)


# ---------------------------------------------------------------- 27. two currents, two vocabularies
def fig_currents_vocab():
    e = res("24_book_architecture")["E_two_currents"]
    body = []
    body.append(text(24, 78, "Shared recurring 5-grams between the two currents of 25b–28b (Jaccard)", 12, INK, weight=600))
    for i, (lab, v, c) in enumerate([("the two currents", e["jaccard_5grams_between_currents"], AMBER),
                                     ("random halves of the same lines (mean)", e["random_line_split_mean"], GRAY),
                                     ("random halves (lowest of 100)", e["random_min"], GRAY2)]):
        y = 90 + i * 26
        body.append(text(24, y + 14, lab, 12, INK))
        body.append(rect(290, y + 2, v * 800, 16, c, 3))
        body.append(text(296 + v * 800, y + 15, f"{v:.3f}", 11, INK))
    y = 180
    body.append(text(24, y, "Names on each current (↘ down-right | ← leftward)", 12, INK, weight=600))
    per = e["names_down_right_vs_leftward"]
    for i, (n, (a, b)) in enumerate([kv for kv in per.items() if sum(kv[1]) >= 10]):
        yy = y + 12 + i * 22
        body.append(text(24, yy + 13, n, 11, INK))
        body.append(rect(260 - a * 2.5, yy + 2, a * 2.5, 14, P6, 2))
        body.append(rect(264, yy + 2, b * 2.5, 14, TEAL, 2))
        body.append(text(254 - a * 2.5, yy + 13, str(a), 10, MUTED, "end"))
        body.append(text(270 + b * 2.5, yy + 13, str(b), 10, MUTED))
    yy = y + 12 + 10 * 22 + 6
    body.append(text(24, yy, "The two currents share fewer formulas than any random split of the same lines: two vocabularies,", 11, MUTED))
    body.append(text(24, yy + 16, "with ANZACH, ACLAX, OXAD leaning ↘ and NOCHAP, CHASTOR leaning ← — like the two houses.", 11, MUTED))
    return svg("fig_currents_vocab", 660, yy + 34, "Two currents, two vocabularies",
               "Tables 25b–28b are written as two interleaved texts that do not share the same words.", body)


# ---------------------------------------------------------------- 28. similarity of sides in book order
def fig_book_order():
    d = res("24_book_architecture")["D_book_order"]
    M, keys = d["similarity_matrix"], d["similarity_matrix_keys"]
    n = len(keys)
    flat = [v for i, r in enumerate(M) for j, v in enumerate(r) if i != j]
    lo, hi = min(flat), max(flat)
    cs, x0, y0 = 5, 60, 80
    body = []
    for i in range(n):
        for j in range(n):
            t = 1 if i == j else (M[i][j] - lo) / (hi - lo)
            col = f"rgb({int(250 - t * 170)},{int(248 - t * 175)},{int(240 - t * 60)})"
            body.append(f'<rect x="{x0 + j * cs}" y="{y0 + i * cs}" width="{cs}" height="{cs}" fill="{col}"/>')
    for i, k in enumerate(keys):
        if k.endswith("a") and int(k[:-1]) % 5 == 0:
            body.append(text(x0 - 4, y0 + i * cs + 5, k[:-1], 9, MUTED, "end"))
            body.append(text(x0 + i * cs + 2, y0 - 4, k[:-1], 9, MUTED, "middle"))
    yy = y0 + n * cs + 20
    body.append(text(24, yy, f"Neighbour similarity along Dee's order {d['path_similarity_dee_order']} vs random orders {d['random_orders_mean']} (best of 500: {d['random_orders_max']});", 11, MUTED))
    body.append(text(24, yy + 16, f"a greedy 'smoothest' ordering reaches {d['greedy_seriation']} — Dee's order is almost as smooth as it can be. Blocks = the segments.", 11, MUTED))
    body.append(text(24, yy + 32, f"Mirror pairs t ↔ 49−t ({d['mirror_t_vs_49_minus_t_mean']}) and same 7×7 plan column ({d['same_plan_column_mean']}) are no closer than random pairs ({d['random_distant_pairs_mean']}).", 11, MUTED))
    return svg("fig_book_order", 640, yy + 50, "The book drifts smoothly from side to side",
               "Similarity of every side with every other (letters + trigrams), in book order 2a → 48b.", body)


# ---------------------------------------------------------------- 29. where the book really changes
def fig_borders():
    d = res("27_doubts")
    rows = d["A3_segment_borders"]["by_blocks"]
    keys = [f"{t}{s}" for t in range(2, 49) for s in "ab"]
    body, x0, y0, cw = [], 40, 96, 6.4

    def strip(y, borders, label, colour):
        body.append(text(24, y - 6, label, 11, INK, weight=600))
        cuts = {b.split("|")[1] for b in borders}
        seg = 0
        for i, k in enumerate(keys):
            if k in cuts:
                seg += 1
            col = [P6, P2, TEAL, AMBER, CORAL, BLUE, GREEN, GRAY][seg % 8]
            body.append(rect(x0 + i * cw, y, cw - 0.6, 18, col, 1))
        for i, k in enumerate(keys):
            if k.endswith("a") and int(k[:-1]) in (2, 6, 13, 25, 29, 33, 41, 44, 48):
                body.append(text(x0 + i * cw + 3, y + 30, k[:-1], 9, MUTED, "middle"))
    strip(y0, ["5b|6a", "25b|26a", "28b|29a", "43b|44a"], "Segments we assumed (opening · heartland · 26–28 · diamonds · end)", GRAY)
    five = next(r for r in rows if r["blocks"] == 5)["borders"]
    strip(y0 + 58, five, "Borders found by the data alone (5 blocks, letters + trigrams)", P6)
    y = y0 + 120
    body.append(text(24, y, "Variance of the side profiles explained by k blocks — book order vs shuffled order", 12, INK, weight=600))
    for i, r in enumerate(rows):
        yy = y + 12 + i * 20
        body.append(text(24, yy + 12, f"{r['blocks']} blocks", 11, INK))
        body.append(rect(100, yy + 2, r["variance_explained"] * 400, 12, P6, 2))
        body.append(rect(100, yy + 14, r["shuffled_order_mean"] * 400, 4, GRAY, 1))
        body.append(text(106 + r["variance_explained"] * 400, yy + 12, f"{r['variance_explained']:.2f} (shuffled {r['shuffled_order_mean']:.2f})", 10, MUTED))
    yy = y + 12 + len(rows) * 20 + 14
    body.append(text(24, yy, "Gains stop after 5 blocks. Stable borders: 12b|13a (every feature set), 40b|41a, 33a|33b, 25a|25b.", 11, MUTED))
    body.append(text(24, yy + 16, "The opening 2–5 is not a block of its own; the U register begins at table 41, not 44; a new break at 12|13", 11, MUTED))
    body.append(text(24, yy + 32, "(T and X rise, U appears). Dialect chain and U register both hold on the new parts.", 11, MUTED))
    return svg("fig_borders", 680, yy + 50, "Where does the book really change?",
               "Optimal cuts of the 94 sides into contiguous blocks, with no borders assumed.", body)


# ---------------------------------------------------------------- 30. the houses have territories
def fig_name_territories():
    d = res("28_names_deep")
    house = {h["name"]: h["house"] for h in d["B2_houses"]}
    house.update({"NOCHA": "NOCHA", "GETH": "GETH/ACLAX", "ACLAX": "GETH/ACLAX"})
    rows = [r for r in d["B1_territories"] if r["survives_bonferroni"]]
    rows.sort(key=lambda r: (house.get(r["name"], "neither") != "NOCHA", house.get(r["name"], "neither") == "neither", r["peak_table"]))
    body, x0, w = [], 150, 470
    tabs = rows[0]["tables"]
    body.append(text(24, 78, "Density along the book (tables 2 → 48) of every name whose territory survives Bonferroni", 12, INK, weight=600))
    for i, r in enumerate(rows):
        y = 92 + i * 30
        c = P6 if house.get(r["name"]) == "NOCHA" else TEAL if house.get(r["name"]) == "GETH/ACLAX" else AMBER
        mx = max(r["density_by_table"]) or 1
        pts = " ".join(f"{x0 + j / (len(tabs) - 1) * w:.1f},{y + 24 - v / mx * 22:.1f}" for j, v in enumerate(r["density_by_table"]))
        body.append(f'<polyline points="{x0},{y+24} {pts} {x0+w},{y+24}" fill="{c}" fill-opacity="0.35" stroke="{c}" stroke-width="1.2"/>')
        body.append(text(24, y + 18, r["name"], 11, INK, weight=600))
        body.append(text(x0 + w + 8, y + 18, f"peak {r['peak_table']} · lag-1 {r['lag1']}", 10, MUTED))
    yy = 92 + len(rows) * 30 + 6
    for t in (2, 13, 26, 34, 41, 48):
        x = x0 + (t - 2) / (len(tabs) - 1) * w
        body.append(f'<line x1="{x}" y1="88" x2="{x}" y2="{yy-6}" stroke="{LINE}" stroke-dasharray="2,3"/>')
        body.append(text(x, yy + 6, str(t), 9, MUTED, "middle"))
    body += legend(24, yy + 28, [(P6, "NOCHA house"), (TEAL, "GETH/ACLAX house"), (AMBER, "neither")])
    body.append(text(24, yy + 50, "The NOCHA house (NOCHA, ADNOCHA, NOCHAP, NACHO…) rules the first half; the GETH/ACLAX house (GETH, ALGETH,", 11, MUTED))
    body.append(text(24, yy + 66, "ACLAX, ACLAXTO, GRADAX) peaks around tables 25–31. Houses are assigned within the a27 parts, beyond part effects.", 11, MUTED))
    return svg("fig_name_territories", 720, yy + 84, "Each house has its own territory",
               "Dashed lines = the data-driven parts (a27).", body)


# ---------------------------------------------------------------- 31. how fast the language changes
def fig_change_rate():
    d = res("29_architecture_deep")
    st = d["C2_change_rate"]["steps"]
    c1 = d["C1_diamond_sides"]
    e = res("24_book_architecture")["E_two_currents"]
    x0, y0, W, H = 50, 90, 600, 140
    mx = max(s["distance"] for s in st)
    body = [f'<line x1="{x0}" y1="{y0+H}" x2="{x0+W}" y2="{y0+H}" stroke="{LINE}"/>']
    body.append(text(24, 78, "Distance between each side and the next (letter models reading each other, bits)", 12, INK, weight=600))
    pts = " ".join(f"{x0 + i / (len(st) - 1) * W:.1f},{y0 + H - s['distance'] / mx * H:.1f}" for i, s in enumerate(st))
    body.append(f'<polyline points="{pts}" fill="none" stroke="{P6}" stroke-width="1.6"/>')
    rp = d["C2_change_rate"]["random_pair_mean"]
    yr = y0 + H - rp / mx * H if rp <= mx else y0
    body.append(f'<line x1="{x0}" y1="{yr}" x2="{x0+W}" y2="{yr}" stroke="{CORAL}" stroke-dasharray="4,3"/>')
    body.append(text(x0 + W - 4, yr - 4, f"random pair of sides: {rp}", 10, CORAL, "end"))
    keys = [s["step"].split("→")[0] for s in st]
    for i, k in enumerate(keys):
        if k in ("12b", "25a", "33a", "40b"):
            x = x0 + (i + 0.5) / (len(st) - 1) * W
            body.append(f'<line x1="{x}" y1="{y0}" x2="{x}" y2="{y0+H}" stroke="{AMBER}" stroke-dasharray="2,3"/>')
            body.append(text(x, y0 + H + 14, k + "|", 9, AMBER, "middle"))
    y = y0 + H + 40
    body.append(text(24, y, "Two interleaved halves: separate vocabularies? (shared recurring 5-grams, Jaccard)", 12, INK, weight=600))
    items = [("currents of 25b–28b", e["jaccard_5grams_between_currents"], e["random_line_split_mean"], AMBER),
             ("a/b sides of diamonds 29–43", c1["jaccard_a_vs_b"], c1["random_split_mean"], TEAL)]
    for i, (lab, v, r, c) in enumerate(items):
        yy = y + 12 + i * 26
        body.append(text(24, yy + 14, lab, 12, INK))
        body.append(rect(230, yy + 2, v * 900, 16, c, 3))
        body.append(rect(230, yy + 18, r * 900, 4, GRAY, 1))
        body.append(text(236 + max(v, r) * 900, yy + 15, f"{v:.3f} (random split {r:.3f})", 11, INK))
    yy = y + 12 + 2 * 26 + 18
    body.append(text(24, yy, "The language drifts in small steps (1.07 bits between neighbours vs 1.72 for random pairs); the largest", 11, MUTED))
    body.append(text(24, yy + 16, "jumps crowd into tables 40–48, where the U register begins. The currents are two vocabularies; the two", 11, MUTED))
    body.append(text(24, yy + 32, "colours of a diamond are one text split in two.", 11, MUTED))
    return svg("fig_change_rate", 720, yy + 50, "How fast does the language change?",
               "Amber dashes = the data-driven borders of a27.", body)


FIGURES = [fig_territory, fig_digits, fig_head_regime, fig_nesting, fig_hive, fig_series, fig_letter_grammar,
           fig_book_formats, fig_diamond, fig_doubled, fig_letter_counts, fig_letters_segments, fig_u_register,
           fig_row_edges, fig_plan_7x7, fig_houses, fig_two_currents, fig_machine, fig_energy,
           fig_index_check, fig_dense_division, fig_robustness, fig_diamond_roads, fig_mi_decay,
           fig_new_names, fig_dialects, fig_currents_vocab, fig_book_order, fig_borders, fig_name_territories, fig_change_rate]


def run():
    made = []
    for f in FIGURES:
        try:
            made.append(os.path.relpath(f(), ROOT))
        except Exception as ex:  # a missing result should not stop the other figures
            made.append(f"{f.__name__}: skipped ({ex})")
    return made


if __name__ == "__main__":
    for m in run():
        print(m)
