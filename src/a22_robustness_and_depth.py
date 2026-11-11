"""
22 - Are we looking wrong? Robustness of the main findings, and a deeper mathematical sweep.

  A) Transcription robustness. The core findings are recomputed on the book as transcribed and
     on altered versions: Z and X merged, U and V merged, U turned into A, only sides whose rows are
     exactly 49 letters, and 10 copies with 2% of letters swapped for their palaeographic look-alikes
     (Z/X, U/B, N/U, R/X, A/E). A finding that survives all of them does not hang on a reading.
  B) Segmentation, calibrated. Peterson's division of the dense lines of leaf 1b (a21) is used to
     tune our word model by leave-one-line-out cross-validation (tuned on 8 lines, scored on the 9th).
  C) Other roads through the diamonds. Each diamond pair (29-43) is rebuilt as its 49x49 square and
     read along every simple path: rows, columns, both diagonals, both directions, boustrophedon,
     spiral. Scored with a letter model trained on the row-written heartland, and by names found.
  D) Deeper sweep:
     D1 mutual information between letters d apples apart (d = 1..64) vs a Markov-3 surrogate;
     D2 longest strings repeated between different tables vs the surrogate;
     D3 compression (LZMA) of the book vs surrogate and shuffle;
     D4 Zipf and Heaps laws on Dee's own word division (leaf 1) vs the Calls;
     D5 vertical structure: letters above/below each other in the full squares vs row-order shuffle.
"""
import json
import lzma
import math
import os
import random
import statistics
from collections import Counter, defaultdict

import load
from a15_book_geometry import rebuild
from a19_machine import CharLM, markov3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NAMES = ["CHASTOR", "CHUSTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "CHADAX"]
CONFUSE = {"Z": "X", "X": "Z", "U": "B", "B": "U", "N": "U", "R": "X", "A": "E", "E": "A"}
SEGMENTS = {"opening": range(2, 6), "heartland": range(6, 26), "diamonds": range(29, 44), "end": range(44, 49)}


# ------------------------------------------------------------------ the book as lines
def base_book():
    lv = load.leaves()
    faces = json.load(open(os.path.join(load.DATA, "loagaeth_diagonal_decoded.json"), encoding="utf-8"))["faces"]
    mixed_path = os.path.join(load.DATA, "loagaeth_mixed_decoded.json")  # a37: row blocks + zones
    mixed = json.load(open(mixed_path, encoding="utf-8"))["faces"] if os.path.exists(mixed_path) else {}
    book = {}
    for t in range(2, 49):
        for s in "ab":
            k = f"{t}{s}"
            if k in mixed:
                book[k] = mixed[k]
            elif k in faces:
                book[k] = faces[k]["down_right"] + faces[k]["leftward"]
            elif k in lv:
                book[k] = [load.letters(r) for r in lv[k] if load.letters(r)]
    return book


def tnum(k):
    return int(k[:-1])


def variant(book, kind, rng=None):
    if kind == "as_transcribed":
        return book
    if kind == "Z_equals_X":
        return {k: [r.replace("Z", "X") for r in v] for k, v in book.items()}
    if kind == "U_equals_V":
        return {k: [r.replace("V", "U") for r in v] for k, v in book.items()}
    if kind == "U_read_as_A":
        return {k: [r.replace("U", "A").replace("V", "A") for r in v] for k, v in book.items()}
    if kind == "only_clean_49_sides":
        out = {}
        for k, v in book.items():
            if tnum(k) <= 25 and k not in ("25b",):
                if len(v) == 49 and all(len(r) == 49 for r in v):
                    out[k] = v
            else:
                out[k] = v
        return out
    if kind == "noise_2pct":
        out = {}
        for k, v in book.items():
            rows = []
            for r in v:
                rows.append("".join(CONFUSE[c] if c in CONFUSE and rng.random() < 0.02 else c for c in r))
            out[k] = rows
        return out
    raise ValueError(kind)


FOLD = {"Z_equals_X": lambda s: s.replace("Z", "X"), "U_equals_V": lambda s: s.replace("V", "U"),
        "U_read_as_A": lambda s: s.replace("U", "A").replace("V", "A")}


def metrics(book, rng, fold=lambda s: s):
    # 1. doubled letters: observed / expected
    obs = n = 0
    cnt = Counter()
    for v in book.values():
        for r in v:
            cnt.update(r)
            obs += sum(a == b for a, b in zip(r, r[1:]))
            n += max(0, len(r) - 1)
    tot = sum(cnt.values())
    exp = sum((c / tot) ** 2 for c in cnt.values())
    doubled = (obs / n) / exp
    # 2. names
    S = "|".join("|".join(v) for v in book.values())
    names = {m: S.count(fold(m)) for m in ("CHASTOR", "CHUSTOR", "ANZACH", "GETH", "NOCHA")}
    # 3. territory: lag-1 autocorrelation of CHASTOR per 1000 letters, table by table (2-48)
    dens = []
    for t in range(2, 49):
        rows_t = [r for s in "ab" for r in book.get(f"{t}{s}", [])]
        L = sum(len(r) for r in rows_t)
        dens.append("|".join(rows_t).count(fold("CHASTOR")) / L * 1000 if L else 0)

    def ac(x):
        m = statistics.mean(x)
        d = sum((a - m) ** 2 for a in x) or 1
        return sum((a - m) * (b - m) for a, b in zip(x, x[1:])) / d
    a0 = ac(dens)
    nulls = []
    for _ in range(1000):
        y = dens[:]
        rng.shuffle(y)
        nulls.append(ac(y))
    terr_z = (a0 - statistics.mean(nulls)) / (statistics.pstdev(nulls) or 1)
    # 4. row edges (row-written sides 2a-25a): letter mix at position 0 and 48 vs the interior
    first, last, mid = Counter(), Counter(), Counter()
    rows = [r for k, v in book.items() if tnum(k) <= 25 and k != "25b" for r in v if len(r) >= 45]
    for r in rows:
        first[r[0]] += 1
        last[r[-1]] += 1
        mid.update(r[5:-5])

    def tvd(a, b):
        A, B = sum(a.values()), sum(b.values())
        return 0.5 * sum(abs(a[c] / A - b[c] / B) for c in set(a) | set(b))
    e0 = tvd(first, mid) + tvd(last, mid)
    en = []
    for _ in range(50):
        f2, l2 = Counter(), Counter()
        for r in rows:
            j = rng.randrange(len(r))
            rr = r[j:] + r[:j]
            f2[rr[0]] += 1
            l2[rr[-1]] += 1
        en.append(tvd(f2, mid) + tvd(l2, mid))
    edge_z = (e0 - statistics.mean(en)) / (statistics.pstdev(en) or 1)
    # 5. segments differ (chi2 over letter counts) vs tables permuted among segments
    tabs = {t: Counter("".join(r for s in "ab" for r in book.get(f"{t}{s}", []))) for rg in SEGMENTS.values() for t in rg}

    def chi(assign):
        seg = defaultdict(Counter)
        for t, g in assign.items():
            seg[g].update(tabs[t])
        allc = Counter()
        for c in seg.values():
            allc.update(c)
        N = sum(allc.values())
        x = 0
        for c in seg.values():
            n_ = sum(c.values())
            for L, v in allc.items():
                e = n_ * v / N
                if e > 0:
                    x += (c[L] - e) ** 2 / e
        return x
    assign = {t: g for g, rg in SEGMENTS.items() for t in rg}
    c0 = chi(assign)
    ts = list(assign)
    labels = list(assign.values())
    cn = []
    for _ in range(100):
        rng.shuffle(labels)
        cn.append(chi(dict(zip(ts, labels))))
    # 6. U register: 5-grams of the end found in the heartland, as is vs with U->A
    def grams(rg):
        c = Counter()
        for t in rg:
            for s in "ab":
                for r in book.get(f"{t}{s}", []):
                    c.update(r[i:i + 5] for i in range(len(r) - 4))
        return c
    end, heart = grams(range(44, 49)), grams(range(6, 26))
    rec = [g for g, c in end.items() if c >= 3]
    hset = {g for g, c in heart.items() if c >= 3}
    u_as_is = sum(g in hset for g in rec)
    u_swap = sum(g.replace("U", "A") in hset for g in rec)
    return {"doubled_obs_over_exp": round(doubled, 3), "names": names,
            "territory_lag1": round(a0, 3), "territory_z": round(terr_z, 1),
            "row_edge_tvd": round(e0, 3), "row_edge_z": round(edge_z, 1),
            "segments_chi2": round(c0), "segments_null_max": round(max(cn)),
            "u_register": [u_as_is, u_swap]}


def A_robustness(book):
    out = {}
    for kind in ["as_transcribed", "Z_equals_X", "U_equals_V", "U_read_as_A", "only_clean_49_sides"]:
        out[kind] = metrics(variant(book, kind), random.Random(22), FOLD.get(kind, lambda s: s))
    noisy = [metrics(variant(book, "noise_2pct", random.Random(100 + i)), random.Random(22)) for i in range(10)]
    keys = ["doubled_obs_over_exp", "territory_z", "row_edge_z", "segments_chi2"]
    out["noise_2pct_x10"] = {k: [min(m[k] for m in noisy), max(m[k] for m in noisy)] for k in keys}
    out["noise_2pct_x10"]["CHASTOR"] = [min(m["names"]["CHASTOR"] for m in noisy), max(m["names"]["CHASTOR"] for m in noisy)]
    out["noise_2pct_x10"]["u_register"] = [[min(m["u_register"][0] for m in noisy), max(m["u_register"][0] for m in noisy)],
                                          [min(m["u_register"][1] for m in noisy), max(m["u_register"][1] for m in noisy)]]
    return out


# ------------------------------------------------------------------ B. calibrated segmentation
def B_calibrated_segmentation():
    import a21_index_heptarchy_numbers as a21
    lv = load.leaves()
    _, refs = a21.parse_index(a21.fetch())
    dense = [j for j, r in enumerate(lv["1b"]) if len(r.split()) == 1 and len(a21.norm(r)) >= 40]
    train = [t for leaf in ["1a", "1b"] for j, r in enumerate(lv[leaf])
             if not (leaf == "1b" and j in dense) for t in a21.wtoks(r)]
    by_row = defaultdict(list)
    for w, leaf, ln, c in refs:
        if leaf == "1b":
            for j in a21.rows_for(leaf, ln):
                if j in dense:
                    by_row[j] += [a21.norm(w)] * c
    lines = [(a21.norm(lv["1b"][j]), a21.gold_cuts(a21.norm(lv["1b"][j]), by_row[j])[0]) for j in dense]

    class Seg2(a21.Seg):
        def __init__(self, words, pen, lenw):
            super().__init__(words)
            self.pen, self.lenw = pen, lenw

        def cost(self, w):
            base = (-math.log(self.wc[w] / (self.N + 1)) if w in self.wc else
                    -math.log(1 / (self.N + 1)) + self.pen - sum(self.lp_char.get(c, -8) for c in w))
            return base - self.lenw * min(len(w), 10)

    grid = [(p, l) for p in (0, 2, 4, 6, 8, 12, 16) for l in (0, 0.5, 1, 2, 3)]
    models = {g: Seg2(train, *g) for g in grid}
    cuts = {g: [models[g].cuts(s) for s, _ in lines] for g in grid}

    def f1(g, idx):
        tp = sum(len(cuts[g][i] & lines[i][1]) for i in idx)
        P = sum(len(cuts[g][i]) for i in idx)
        G = sum(len(lines[i][1]) for i in idx)
        p, r = (tp / P if P else 0), (tp / G if G else 0)
        return 2 * p * r / (p + r) if p + r else 0
    tp = P = G = 0
    chosen = []
    for i in range(len(lines)):
        rest = [k for k in range(len(lines)) if k != i]
        g = max(grid, key=lambda g: f1(g, rest))
        chosen.append(g)
        tp += len(cuts[g][i] & lines[i][1])
        P += len(cuts[g][i])
        G += len(lines[i][1])
    p, r = tp / P, tp / G
    return {"default_F1": round(f1((4, 0), range(len(lines))), 3),
            "cross_validated_F1": round(2 * p * r / (p + r), 3),
            "cv_precision": round(p, 3), "cv_recall": round(r, 3),
            "settings_chosen": Counter(f"pen={a},len={b}" for a, b in chosen).most_common(3),
            "note": "Tuned on 8 lines, scored on the held-out 9th; random breaks score ~0.16."}


# ------------------------------------------------------------------ C. roads through the diamonds
def paths(G):
    n = 49
    out = {}
    out["rows L→R"] = ["".join(G[r][c] for c in range(n)) for r in range(n)]
    out["rows R→L"] = [x[::-1] for x in out["rows L→R"]]
    out["columns down"] = ["".join(G[r][c] for r in range(n)) for c in range(n)]
    out["columns up"] = [x[::-1] for x in out["columns down"]]
    out["boustrophedon"] = [x if i % 2 == 0 else x[::-1] for i, x in enumerate(out["rows L→R"])]
    out["diagonals ↘ (r−c)"] = ["".join(G[r][r - k] for r in range(n) if 0 <= r - k < n) for k in range(-(n - 1), n)]
    out["diagonals ↖"] = [x[::-1] for x in out["diagonals ↘ (r−c)"]]
    out["anti-diagonals ↙ (r+c)"] = ["".join(G[r][k - r] for r in range(n) if 0 <= k - r < n) for k in range(2 * n - 1)]
    out["anti-diagonals ↗"] = [x[::-1] for x in out["anti-diagonals ↙ (r+c)"]]
    sp, top, bot, lef, rig = [], 0, n - 1, 0, n - 1
    while top <= bot and lef <= rig:
        sp += [G[top][c] for c in range(lef, rig + 1)]
        sp += [G[r][rig] for r in range(top + 1, bot + 1)]
        if top < bot:
            sp += [G[bot][c] for c in range(rig - 1, lef - 1, -1)]
        if lef < rig:
            sp += [G[r][lef] for r in range(bot - 1, top, -1)]
        top, bot, lef, rig = top + 1, bot - 1, lef + 1, rig - 1
    s = "".join(sp)
    out["spiral"] = [s[i:i + 49] for i in range(0, len(s), 49)]
    return out


def C_diamond_roads():
    lv = load.leaves()
    train = [load.letters(r) for t in range(2, 25) for s in "ab" for r in lv.get(f"{t}{s}", []) if load.letters(r)]
    lm = CharLM(4)
    lm.fit(train)
    agg = defaultdict(lambda: [0.0, 0, 0])
    for t in range(29, 44):
        G = rebuild(t)
        if not G or any(c is None for row in G for c in row):
            continue
        for name, lines in paths(G).items():
            L = sum(len(x) for x in lines)
            agg[name][0] += lm.bits(lines) * L
            agg[name][1] += L
            agg[name][2] += sum("|".join(lines).count(m) for m in NAMES)
    res = {k: {"bits_per_letter": round(v[0] / v[1], 3), "names_per_1000": round(v[2] / v[1] * 1000, 2)}
           for k, v in agg.items()}
    return dict(sorted(res.items(), key=lambda kv: kv[1]["bits_per_letter"]))


# ------------------------------------------------------------------ D. deeper sweep
def heart_stream():
    lv = load.leaves()
    return "".join(load.letters(r) for t in range(2, 25) for s in "ab" for r in lv.get(f"{t}{s}", []))


def mi_at(s, d):
    pairs = Counter(zip(s, s[d:]))
    a, b = Counter(s[:-d]), Counter(s[d:])
    n = len(s) - d
    return sum(c / n * math.log2(c * n / (a[x] * b[y])) for (x, y), c in pairs.items())


def D1_mutual_information(s, sur):
    ds = [1, 2, 3, 4, 5, 6, 8, 10, 12, 16, 20, 24, 32, 48, 49, 50, 64, 128, 512]
    sh = list(s)
    random.Random(3).shuffle(sh)
    sh = "".join(sh)
    base = mi_at(sh, 1)  # finite-sample bias floor
    # control for non-stationarity: shuffle letters inside each side (keeps each side's letter mix)
    lv = load.leaves()
    rng = random.Random(5)
    parts = []
    for t in range(2, 25):
        for side in "ab":
            x = list("".join(load.letters(r) for r in lv.get(f"{t}{side}", [])))
            rng.shuffle(x)
            parts.append("".join(x))
    ws = "".join(parts)
    # control for row position: shuffle whole rows' contents but keep each letter at its column
    return {"distance": ds,
            "loagaeth": [round(mi_at(s, d), 4) for d in ds],
            "markov3_surrogate": [round(mi_at(sur, d), 4) for d in ds],
            "shuffled_within_each_side": [round(mi_at(ws, d), 4) for d in ds],
            "shuffled_floor": round(base, 4),
            "note": "Excess over 'shuffled within each side' at long range = structure beyond the "
                    "side-to-side change of letter mix."}


def longest_cross_table_repeat(tables):
    best = (0, None)
    for k in range(10, 80):
        seen = {}
        hit = None
        for t, txt in tables.items():
            for i in range(len(txt) - k + 1):
                g = txt[i:i + k]
                if g in seen and seen[g] != t:
                    hit = g
                    break
                seen.setdefault(g, t)
            if hit:
                break
        if not hit:
            break
        best = (k, hit)
    return best


def D2_repeats(book, rng):
    tables = {t: "".join(r for s in "ab" for r in book.get(f"{t}{s}", [])) for t in range(2, 25)}
    k, g = longest_cross_table_repeat(tables)
    allt = "".join(tables.values())
    sur = markov3(allt, rng)
    st, i = {}, 0
    for t, txt in tables.items():
        st[t] = sur[i:i + len(txt)]
        i += len(txt)
    ks, _ = longest_cross_table_repeat(st)
    # how many 12-grams are shared between different tables
    def shared(tb, k=12):
        where = defaultdict(set)
        for t, txt in tb.items():
            for j in range(len(txt) - k + 1):
                where[txt[j:j + k]].add(t)
        return sum(1 for v in where.values() if len(v) > 1)
    return {"longest_repeat_between_tables": k, "example": g, "surrogate_longest": ks,
            "shared_12grams": shared(tables), "shared_12grams_surrogate": shared(st)}


def D3_compression(s, sur):
    sh = list(s)
    random.Random(4).shuffle(sh)

    def bpl(x):
        return round(len(lzma.compress(x.encode(), preset=9)) * 8 / len(x), 3)
    return {"loagaeth_bits_per_letter": bpl(s), "markov3_surrogate": bpl(sur), "shuffled": bpl("".join(sh))}


def zipf_heaps(words):
    c = Counter(words)
    f = sorted(c.values(), reverse=True)[:300]
    xs = [math.log(i + 1) for i in range(len(f))]
    ys = [math.log(v) for v in f]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    # Heaps: V(N) ~ N^beta
    seen, pts = set(), []
    for i, w in enumerate(words, 1):
        seen.add(w)
        if i in (100, 200, 400, 800, 1600, 3200):
            pts.append((math.log(i), math.log(len(seen))))
    hx, hy = [p[0] for p in pts], [p[1] for p in pts]
    mx, my = statistics.mean(hx), statistics.mean(hy)
    beta = sum((x - mx) * (y - my) for x, y in zip(hx, hy)) / sum((x - mx) ** 2 for x in hx)
    return {"tokens": len(words), "types": len(c), "zipf_slope": round(slope, 2), "heaps_beta": round(beta, 2),
            "hapax_share": round(sum(1 for v in c.values() if v == 1) / len(c), 2)}


def D4_zipf():
    import a21_index_heptarchy_numbers as a21
    lv = load.leaves()
    leaf1 = [t for leaf in ["1a", "1b"] for r in lv[leaf] for t in a21.wtoks(r) if len(r.split()) > 1]
    calls = json.load(open(os.path.join(ROOT, "engine", "data", "chamadas.json"), encoding="utf-8"))["chamadas"]
    cw = [a21.norm(w["enoquiano"]) for ch in calls for w in ch["palavras"] if a21.norm(w["enoquiano"])]
    return {"leaf1_dee_words": zipf_heaps(leaf1), "calls": zipf_heaps(cw),
            "leaf1_first_tokens_same_size_as_calls": zipf_heaps(leaf1[:len(cw)]),
            "note": "Natural language: Zipf slope near -1, Heaps beta 0.4-0.7. A list of unique names "
                    "gives a flat curve and beta near 1."}


def D5_vertical(book, rng):
    grids = [v for k, v in book.items() if tnum(k) <= 25 and k != "25b" and len(v) == 49 and all(len(r) == 49 for r in v)]

    def vmi(gs):
        s1 = "".join(g[r][c] for g in gs for r in range(48) for c in range(49))
        s2 = "".join(g[r + 1][c] for g in gs for r in range(48) for c in range(49))
        pairs = Counter(zip(s1, s2))
        a, b, n = Counter(s1), Counter(s2), len(s1)
        return sum(v / n * math.log2(v * n / (a[x] * b[y])) for (x, y), v in pairs.items())
    obs = vmi(grids)
    nul = []
    for _ in range(20):
        gs = []
        for g in grids:
            g2 = g[:]
            rng.shuffle(g2)
            gs.append(g2)
        nul.append(vmi(gs))
    return {"sides": len(grids), "vertical_MI_bits": round(obs, 4), "row_order_shuffled_mean": round(statistics.mean(nul), 4),
            "z": round((obs - statistics.mean(nul)) / (statistics.pstdev(nul) or 1), 1)}


def run():
    rng = random.Random(22)
    book = base_book()
    s = heart_stream()
    sur = markov3(s, random.Random(7))
    res = {
        "A_robustness": A_robustness(book),
        "B_calibrated_segmentation": B_calibrated_segmentation(),
        "C_diamond_roads": C_diamond_roads(),
        "D1_mutual_information": D1_mutual_information(s, sur),
        "D2_repeats": D2_repeats(book, rng),
        "D3_compression": D3_compression(s, sur),
        "D4_zipf_heaps": D4_zipf(),
        "D5_vertical": D5_vertical(book, rng),
    }
    load.save_result("22_robustness_and_depth", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
