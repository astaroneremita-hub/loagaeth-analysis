"""
Generate every figure of the project as a standalone SVG in figures/.

Run after the analyses (run_all.py calls this at the end):
    python src/make_figures.py

Each figure is drawn from the JSON results (or the bundled data), so the pictures stay
reproducible and update when the data or the analyses change. Pure standard library.
"""
import json
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


def svg(name, w, h, title, subtitle, body):
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
               "Occurrences per table. All three vanish together in the void tables 26–28.", body)


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
    noise = {int(t) for t in r["C_tables_26_28"]}

    def cat(t):
        f = per[str(t)]["format"] if str(t) in per else ""
        if t == 1:
            return ("prophecy (word-spaced)", GRAY)
        if t in noise:
            return ("noise tables", CORAL)
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
               "Top: format of each table. Bottom: share of text made of recurring names.", body)


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
             ("Tables 26–28", r["tables_26_28"], CORAL)]
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
               "Share of adjacent identical letters. The Loagaeth avoids them ~11× below chance; tables 26–28 do not.", body)


FIGURES = [fig_territory, fig_digits, fig_head_regime, fig_nesting, fig_hive, fig_series, fig_letter_grammar,
           fig_book_formats, fig_diamond, fig_doubled]


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
