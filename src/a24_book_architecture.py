"""
24 - The book's architecture: centres and acrostics, the pyramids' cross, dialects, book order,
     the two currents, rows as verses.

  A) Acrostics. In the 36 exact 49x49 sides, the first letters of the rows read downwards (and the
     last letters) are searched for names (known stems + the a23 lexicon), against the same search
     on interior columns. The centre cells (25,25) of all squares, read in book order, likewise.
  B) The pyramid's cross. Seen from above, a diamond rebuilt as a square shows the two diagonals.
     Do names gather near the main diagonal r=c (the centre of every stored line = the seam where
     the two stepped pyramids meet) or near the square's centre? Null: each name moved to a random
     position inside its own line.
  C) Dialects. A letter model trained on each segment reads every other segment (cross bits):
     which realms speak alike.
  D) Book order. Similarity of sides (letter + trigram profile). Is Dee's order smoother than random
     orders? Are a/b sides of a table more alike than neighbours? Are tables t and 49-t (the book
     folded on itself) alike?
  E) The two currents of 25b-28b: do they share vocabulary like one text, or split like two houses?
  F) Rows as verses: in the row-written sides, do row breaks fall on word breaks more often than
     random positions (word breaks from a segmenter that never sees the row breaks)?
"""
import json
import math
import os
import random
import statistics
from collections import Counter, defaultdict

import load
from a15_book_geometry import rebuild
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum

KNOWN = ["CHASTOR", "CHUSTOR", "ANZACH", "GETH", "NOCHA", "ACLAX", "CHADAX", "OXAD"]


def lexicon():
    names = list(KNOWN)
    p = os.path.join(load.RESULTS, "23_name_discovery.json")
    if os.path.exists(p):
        names += [c["name"] for c in json.load(open(p, encoding="utf-8"))["A_candidates"]["top"]]
    return sorted(set(n for n in names if len(n) >= 4))


def full_sides(book):
    return {k: v for k, v in book.items() if tnum(k) <= 25 and k != "25b" and len(v) == 49 and all(len(r) == 49 for r in v)}


def hits(s, names):
    return sum(s.count(n) for n in names)


def A_acrostics(book, names, rng):
    fs = full_sides(book)
    col = lambda v, c: "".join(r[c] for r in v)
    first = sum(hits(col(v, 0), names) for v in fs.values())
    last = sum(hits(col(v, 48), names) for v in fs.values())
    interior = [sum(hits(col(v, c), names) for v in fs.values()) for c in range(3, 46)]
    centres = "".join(v[24][24] for k, v in sorted(fs.items(), key=lambda kv: (tnum(kv[0]), kv[0][-1])))
    rand_cells = []
    for _ in range(500):
        r_, c_ = rng.randrange(49), rng.randrange(49)
        rand_cells.append(hits("".join(v[r_][c_] for k, v in sorted(fs.items(), key=lambda kv: (tnum(kv[0]), kv[0][-1]))), names))
    return {"sides": len(fs),
            "names_in_first_letter_columns": first, "names_in_last_letter_columns": last,
            "names_in_interior_columns_mean": round(statistics.mean(interior), 2),
            "names_in_interior_columns_max": max(interior),
            "centre_cells_in_book_order": centres,
            "names_in_centre_string": hits(centres, names),
            "names_in_random_cell_strings_mean": round(statistics.mean(rand_cells), 2)}


def B_cross(names, rng):
    """Name cells by distance to the main diagonal and to the centre, in rebuilt diamonds 29-43."""
    obs_d, obs_c, nul_d, nul_c = [], [], [], []
    for t in range(29, 44):
        G = rebuild(t)
        if not G:
            continue
        # stored lines are anti-diagonals r+c = k; read r ascending (the stored direction)
        for k in range(97):
            cells = [(r, k - r) for r in range(49) if 0 <= k - r < 49]
            line = "".join(G[r][c] for r, c in cells)
            if None in [G[r][c] for r, c in cells]:
                continue
            for n in names:
                st = 0
                while True:
                    i = line.find(n, st)
                    if i < 0:
                        break
                    for j in range(i, i + len(n)):
                        r, c = cells[j]
                        obs_d.append(abs(r - c))
                        obs_c.append(max(abs(r - 24), abs(c - 24)))
                    # null: same name length placed uniformly in the same line
                    i2 = rng.randrange(len(line) - len(n) + 1)
                    for j in range(i2, i2 + len(n)):
                        r, c = cells[j]
                        nul_d.append(abs(r - c))
                        nul_c.append(max(abs(r - 24), abs(c - 24)))
                    st = i + 1
    m = statistics.mean
    return {"name_cells": len(obs_d),
            "mean_distance_to_main_diagonal": round(m(obs_d), 2), "null": round(m(nul_d), 2),
            "mean_ring_from_centre": round(m(obs_c), 2), "null_ring": round(m(nul_c), 2),
            "z_diagonal": round((m(obs_d) - m(nul_d)) / (statistics.pstdev(nul_d) / math.sqrt(len(nul_d))), 1),
            "z_centre": round((m(obs_c) - m(nul_c)) / (statistics.pstdev(nul_c) / math.sqrt(len(nul_c))), 1)}


SEGS = {"opening": range(2, 6), "heartland": range(6, 26), "decoded 26-28": range(26, 29),
        "diamonds": range(29, 44), "end": range(44, 49)}


def C_dialects(book):
    seg_lines = {s: [r for k, v in book.items() if tnum(k) in rg and k != "25b" for r in v] for s, rg in SEGS.items()}
    rng = random.Random(24)
    train, test = {}, {}
    for s, L in seg_lines.items():
        L = L[:]
        rng.shuffle(L)
        h = len(L) // 2
        train[s], test[s] = L[:h], L[h:]
    models = {}
    for s in SEGS:
        m = CharLM(3)
        m.fit(train[s])
        models[s] = m
    mat = {a: {b: round(models[a].bits(test[b]), 3) for b in SEGS} for a in SEGS}
    return {"rows_trained_on_cols_read": mat,
            "note": "Lower = the realm's model reads the other realm easily; the diagonal is each realm on itself."}


def profile(lines):
    c = Counter()
    for r in lines:
        c.update(r)
        c.update(r[i:i + 3] for i in range(len(r) - 2))
    return c


def cos(a, b):
    num = sum(a[k] * b.get(k, 0) for k in a)
    return num / (math.sqrt(sum(v * v for v in a.values())) * math.sqrt(sum(v * v for v in b.values())))


def D_order(book, rng):
    keys = sorted(book, key=lambda k: (tnum(k), k[-1]))
    P = {k: profile(book[k]) for k in keys}
    S = {(a, b): cos(P[a], P[b]) for a in keys for b in keys if a < b}
    sim = lambda a, b: 1.0 if a == b else S[(a, b) if a < b else (b, a)]
    path = lambda order: sum(sim(order[i], order[i + 1]) for i in range(len(order) - 1))
    real = path(keys)
    rnd = []
    for _ in range(500):
        o = keys[:]
        rng.shuffle(o)
        rnd.append(path(o))
    # greedy seriation (nearest neighbour from the first side) as a reference for "smoothest"
    left, cur, ser = set(keys[1:]), keys[0], [keys[0]]
    while left:
        cur = max(left, key=lambda k: sim(cur, k))
        ser.append(cur)
        left.remove(cur)
    tabs = sorted({tnum(k) for k in keys})
    ab = [sim(f"{t}a", f"{t}b") for t in tabs if f"{t}a" in P and f"{t}b" in P]
    nb = [sim(f"{t}b", f"{t+1}a") for t in tabs if f"{t}b" in P and f"{t+1}a" in P]
    mir = [sim(f"{t}a", f"{49-t}a") for t in range(2, 24) if f"{t}a" in P and f"{49-t}a" in P]
    mir_ctrl = []
    for _ in range(300):
        t1, t2 = rng.sample(range(2, 48), 2)
        if abs(t1 - t2) > 3 and f"{t1}a" in P and f"{t2}a" in P:
            mir_ctrl.append(sim(f"{t1}a", f"{t2}a"))
    # same column of the 7x7 plan (table n at plan position n-1)
    plan_same_col = [sim(f"{a}a", f"{b}a") for a in range(2, 49) for b in range(a + 7, 49, 7)
                     if f"{a}a" in P and f"{b}a" in P]
    return {"path_similarity_dee_order": round(real, 2),
            "random_orders_mean": round(statistics.mean(rnd), 2), "random_orders_max": round(max(rnd), 2),
            "greedy_seriation": round(path(ser), 2),
            "greedy_order_first_30": ser[:30],
            "a_vs_b_same_table_mean": round(statistics.mean(ab), 3),
            "b_vs_next_a_mean": round(statistics.mean(nb), 3),
            "mirror_t_vs_49_minus_t_mean": round(statistics.mean(mir), 3),
            "random_distant_pairs_mean": round(statistics.mean(mir_ctrl), 3),
            "same_plan_column_mean": round(statistics.mean(plan_same_col), 3),
            "similarity_matrix_keys": keys,
            "similarity_matrix": [[round(sim(a, b), 3) for b in keys] for a in keys]}


def E_currents(names, rng):
    faces = json.load(open(os.path.join(load.DATA, "loagaeth_diagonal_decoded.json"), encoding="utf-8"))["faces"]
    dr = [r for f in faces.values() for r in f["down_right"]]
    lw = [r for f in faces.values() for r in f["leftward"]]
    mp = os.path.join(load.DATA, "loagaeth_mixed_decoded.json")  # a37: refined reading, same two colours
    if os.path.exists(mp):
        bc = json.load(open(mp, encoding="utf-8")).get("by_colour", {})
        if bc:
            # colour 0 / colour 1 of each face; which colour is the "down-right" one follows a18's marks
            dr, lw = [], []
            for k, (c0, c1) in bc.items():
                a = set(faces[k]["down_right"]) if k in faces else set()
                first_is_dr = len(a & set(c0)) >= len(a & set(c1))
                dr += c0 if first_is_dr else c1
                lw += c1 if first_is_dr else c0

    def grams(L):
        return Counter(g for r in L for g in (r[i:i + 5] for i in range(len(r) - 4)))

    def jac(a, b):
        A = {g for g, c in a.items() if c >= 2}
        B = {g for g, c in b.items() if c >= 2}
        return len(A & B) / max(1, len(A | B))
    j0 = jac(grams(dr), grams(lw))
    allL = dr + lw
    js = []
    for _ in range(100):
        rng.shuffle(allL)
        h = len(dr)
        js.append(jac(grams(allL[:h]), grams(allL[h:])))
    per = {n: [sum(r.count(n) for r in dr), sum(r.count(n) for r in lw)] for n in KNOWN + ["NOCHAP", "ALGETH", "ADNOCHA"]}
    return {"jaccard_5grams_between_currents": round(j0, 3),
            "random_line_split_mean": round(statistics.mean(js), 3), "random_min": round(min(js), 3),
            "names_down_right_vs_leftward": per}


def F_verses(book, names, rng):
    import a21_index_heptarchy_numbers as a21
    lv = load.leaves()
    train = [t for leaf in ["1a", "1b"] for r in lv[leaf] if len(r.split()) > 1 for t in a21.wtoks(r)]
    seg = a21.Seg(train + [n for n in names for _ in range(20)])
    fs = full_sides(book)
    at_break = rand_pos = n_break = n_rand = 0
    for k, v in list(fs.items())[:20]:
        s = "".join(v)
        cuts = set()
        for i in range(0, len(s), 400):  # segment in chunks that straddle row breaks
            chunk = s[i:i + 420]
            cuts |= {i + c for c in seg.cuts(chunk)}
        for b in range(49, len(s), 49):
            n_break += 1
            at_break += b in cuts
        for _ in range(48):
            p = rng.randrange(1, len(s))
            if p % 49:
                n_rand += 1
                rand_pos += p in cuts
    return {"row_breaks_that_are_word_breaks": round(at_break / n_break, 3),
            "random_positions_that_are_word_breaks": round(rand_pos / n_rand, 3),
            "ratio": round((at_break / n_break) / (rand_pos / n_rand), 2)}


def run():
    rng = random.Random(24)
    book = base_book()
    names = lexicon()
    res = {"lexicon_size": len(names),
           "A_acrostics_and_centres": A_acrostics(book, names, rng),
           "B_pyramid_cross": B_cross(names, rng),
           "C_dialects": C_dialects(book),
           "D_book_order": D_order(book, rng),
           "E_two_currents": E_currents(names, rng),
           "F_rows_as_verses": F_verses(book, names, rng)}
    load.save_result("24_book_architecture", res)
    return res


if __name__ == "__main__":
    r = run()
    r["D_book_order"].pop("similarity_matrix")
    r["D_book_order"].pop("similarity_matrix_keys")
    print(json.dumps(r, ensure_ascii=False, indent=1))
