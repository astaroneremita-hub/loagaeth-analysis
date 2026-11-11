"""
40 - Formulas: how long is the memory of the text, and how do repeated passages vary?

Follow-up to a39 (long repeats are real against Markov-3, but an order-5 model trained on the whole
book reproduces them - a model that may simply have memorised the book).

  A) Held-out test. Split the sides in two halves (alternating). Strings of length L in half B that
     also occur in half A, against a fake half B written by a letter model trained on half A only
     (orders 3 and 5). If the real B shares more long strings with A than the model can produce,
     the book repeats units longer than the model's memory.
  B) Names in sequence. Successive names in a line (any gap): is the next name tied to the previous
     one more than when names are shuffled inside each side?
  C) Compounds. For the commonest directly joined pairs: count against the same shuffle.
     (Superseded by a42-D: the shuffle is misled by overlapping names; OXAD + NOCHA is OX + ADNOCHA.)
  D) Are long repeats copied in place? Start column of the two occurrences of each long repeat.
  E) Near-repeats. Windows of 20 letters that recur with at most 2 different letters. How many
     (against Markov-3), and WHICH letters differ: the spelling variation of the book itself,
     compared with the copying errors measured on the Soyga tables (a36).
"""
import json
import math
import os
import random
import statistics
from collections import Counter, defaultdict

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a39_long_repeats import MASTERS, adj_pairs, mi, repeats, surrogate3, tokens

VOW = set("AEIOUY")


def name_list():
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))
    return sorted(set(MASTERS) | {x["name"] for x in d["A_candidates"]["top"]}, key=len, reverse=True)


def A_heldout(book, rng):
    keys = sorted(book, key=lambda k: (tnum(k), k))
    HA = [r for k in keys[0::2] for r in book[k] if r]
    HB = [r for k in keys[1::2] for r in book[k] if r]
    out = {}
    models = {o: CharLM(o, alpha=0.05).fit(HA) for o in (3, 5)}
    fakes = {o: [[models[o].sample(len(r), rng) for r in HB] for _ in range(3)] for o in (3, 5)}
    for L in (8, 10, 12, 14):
        inA = {r[i:i + L] for r in HA for i in range(len(r) - L + 1)}

        def shared(lines):
            return len({r[i:i + L] for r in lines for i in range(len(r) - L + 1)} & inA)
        out[L] = {"real_half_B": shared(HB),
                  "order3_model_of_A": round(statistics.mean(shared(f) for f in fakes[3]), 1),
                  "order5_model_of_A": round(statistics.mean(shared(f) for f in fakes[5]), 1)}
    return out


def shuffled_faces(by_face, rng):
    """Names shuffled inside each side; positions (and so the adjacency pattern) kept."""
    out = {}
    for k, v in by_face.items():
        pool = [t[1] for seq in v for t in seq]
        rng.shuffle(pool)
        i, new = 0, []
        for seq in v:
            new.append([(t[0], pool[i + j], len(t[1])) for j, t in enumerate(seq)])
            i += len(seq)
        out[k] = new
    return out


def BC_names(book, names, rng):
    by_face = {k: [tokens(r, names) for r in v if r] for k, v in book.items()}
    succ = [(a[1], b[1]) for v in by_face.values() for seq in v for a, b in zip(seq, seq[1:])]
    adj = [p for v in by_face.values() for seq in v for p in adj_pairs(seq)]
    obs = mi(succ)
    nul, adjn = [], []
    for _ in range(300):
        sh = shuffled_faces(by_face, rng)
        nul.append(mi([(a[1], b[1]) for v in sh.values() for seq in v for a, b in zip(seq, seq[1:])]))
        adjn.append(Counter((a[1], b[1]) for v in sh.values() for seq in v for a, b in zip(seq, seq[1:]) if a[0] + a[2] == b[0]))
    c = Counter(adj)
    pairs = []
    for (a, b), n in c.most_common(8):
        xs = [x.get((a, b), 0) for x in adjn]
        pairs.append({"pair": a + " + " + b, "count": n, "reverse": c.get((b, a), 0),
                      "shuffled_mean": round(statistics.mean(xs), 2), "p": round(sum(x >= n for x in xs) / len(xs), 4)})
    return {"successive_names": len(succ), "mutual_information_bits": round(obs, 3),
            "shuffled_mean_max": [round(statistics.mean(nul), 3), round(max(nul), 3)],
            "p": round(sum(v >= obs for v in nul) / len(nul), 4)}, pairs


def D_columns(lines, rng):
    pos = defaultdict(list)
    for li, r in enumerate(lines):
        for i in range(len(r) - 13):
            pos[r[i:i + 14]].append((li, i))
    pairs = [(v[0][1], v[1][1]) for v in pos.values() if len(v) == 2 and v[0][0] != v[1][0]]
    same = sum(a == b for a, b in pairs) / max(1, len(pairs))
    near = sum(abs(a - b) <= 2 for a, b in pairs) / max(1, len(pairs))
    nul_s, nul_n = [], []
    bs = [b for _, b in pairs]
    for _ in range(500):
        rng.shuffle(bs)
        nul_s.append(sum(a == b for (a, _), b in zip(pairs, bs)) / max(1, len(pairs)))
        nul_n.append(sum(abs(a - b) <= 2 for (a, _), b in zip(pairs, bs)) / max(1, len(pairs)))
    return {"repeats_of_14_in_two_lines": len(pairs), "same_start_column": round(same, 3),
            "shuffled_same_column": round(statistics.mean(nul_s), 3),
            "within_2_columns": round(near, 3), "shuffled_within_2": round(statistics.mean(nul_n), 3),
            "p_within_2": round(sum(v >= near for v in nul_n) / 500, 4)}


def near_repeats(lines, W=20, K=2, collect=False):
    cuts = [(0, 7), (7, 14), (14, 20)]
    idx = defaultdict(list)
    for li, r in enumerate(lines):
        for i in range(len(r) - W + 1):
            for ci, (a, b) in enumerate(cuts):
                idx[(ci, r[i + a:i + b])].append((li, i))
    seen, subs, ex = set(), {}, {}
    for v in idx.values():
        if len(v) < 2 or len(v) > 150:
            continue
        for x in range(len(v)):
            la, ia = v[x]
            for y in range(x + 1, len(v)):
                lb, ib = v[y]
                if la == lb and abs(ia - ib) < W:
                    continue
                key = (la, lb, ib - ia)
                A, B = lines[la][ia:ia + W], lines[lb][ib:ib + W]
                d = [(j, p, q) for j, (p, q) in enumerate(zip(A, B)) if p != q]
                if len(d) > K:
                    continue
                kind = "exact" if not d else "near"
                seen.add((key, kind))
                if collect and d:
                    for j, p, q in d:
                        subs[(la, ia + j, lb, ib + j)] = tuple(sorted((p, q)))
                    ex.setdefault(key, (A, B))
    passages = {k for k, _ in seen}
    with_var = {k for k, kind in seen if kind == "near"}
    return len(passages), len(with_var), subs, ex


def E_near(book, lines, rng):
    n_all, n_var, subs, ex = near_repeats(lines, collect=True)
    sur = [near_repeats(surrogate3(lines, rng))[:2] for _ in range(2)]
    c = Counter(subs.values())
    tot = sum(c.values())
    vv = sum(n for (p, q), n in c.items() if p in VOW and q in VOW)
    cc = sum(n for (p, q), n in c.items() if p not in VOW and q not in VOW)
    # chance share of vowel-vowel among random pairs of different letters, by letter frequency
    f = Counter("".join(lines))
    N = sum(f.values())
    pv = sum(f[x] for x in f if x in VOW) / N
    den = 1 - sum((f[x] / N) ** 2 for x in f)
    vv_exp = (pv * pv - sum((f[x] / N) ** 2 for x in f if x in VOW)) / den
    examples = []
    for (la, lb, _), (A, B) in list(ex.items())[:400]:
        examples.append((A, B))
    examples = sorted(set(examples), key=lambda t: sum(p != q for p, q in zip(*t)))[:12]
    return {"passages_of_20_recurring_with_at_most_2_changes": n_all, "of_which_with_a_change": n_var,
            "markov3_surrogates": [list(s) for s in sur],
            "letter_changes": tot, "vowel_for_vowel": round(vv / max(1, tot), 3), "vowel_for_vowel_by_chance": round(vv_exp, 3),
            "consonant_for_consonant": round(cc / max(1, tot), 3),
            "top_changes": [{"pair": p + "/" + q, "count": n} for (p, q), n in c.most_common(14)],
            "scribe_pairs_from_soyga": {k: c.get(tuple(sorted(k.split("/"))), 0) for k in ("Z/X", "N/U", "A/U", "I/Y")},
            "examples": [{"a": a, "b": b} for a, b in examples]}


CLASSES = [set("PTCBDG"), set("LRMN"), set("SZX")]  # stops, liquids and nasals, sibilants


def variants14(lines):
    """Passages of 14 letters that recur with exactly one letter changed (not in the outer 3)."""
    idx = defaultdict(list)
    for li, r in enumerate(lines):
        for i in range(len(r) - 13):
            idx[(0, r[i:i + 7])].append((li, i))
            idx[(1, r[i + 7:i + 14])].append((li, i))
    subs = {}
    for v in idx.values():
        if len(v) < 2 or len(v) > 200:
            continue
        for x in range(len(v)):
            la, ia = v[x]
            for y in range(x + 1, len(v)):
                lb, ib = v[y]
                if la == lb and abs(ia - ib) < 14:
                    continue
                A, B = lines[la][ia:ia + 14], lines[lb][ib:ib + 14]
                d = [j for j in range(14) if A[j] != B[j]]
                if len(d) == 1 and 3 <= d[0] <= 10:
                    j = d[0]
                    subs[(la, ia + j, lb, ib + j)] = (tuple(sorted((A[j], B[j]))), A[j - 3:j] + "_" + A[j + 1:j + 4])
    return subs


def F_variation(lines, rng):
    s = variants14(lines)
    c = Counter(v[0] for v in s.values())
    tot = sum(c.values())
    sur = [Counter(v[0] for v in variants14(surrogate3(lines, rng)).values()) for _ in range(3)]
    f = Counter("".join(lines))
    cons = [x for x in f if x not in VOW]
    cc = {k: n for k, n in c.items() if k[0] not in VOW and k[1] not in VOW}
    ncc = sum(cc.values())

    def same(p, q):
        return any(p in C and q in C for C in CLASSES)
    obs = sum(n for (p, q), n in cc.items() if same(p, q)) / max(1, ncc)
    w = [f[x] for x in cons]
    nul = []
    for _ in range(2000):
        k = 0
        for _ in range(ncc):
            while True:
                p, q = rng.choices(cons, w, k=2)
                if p != q:
                    break
            k += same(p, q)
        nul.append(k / max(1, ncc))
    scc = Counter()
    for x in sur:
        scc.update({k: n for k, n in x.items() if k[0] not in VOW and k[1] not in VOW})
    top = []
    for (p, q), n in c.most_common(16):
        fr = Counter(v[1] for v in s.values() if v[0] == (p, q)).most_common(2)
        top.append({"pair": p + "/" + q, "count": n, "surrogates": [x.get((p, q), 0) for x in sur], "commonest_frames": [a for a, _ in fr]})
    return {"one_letter_variants_of_14_letter_passages": tot, "markov3_surrogates": [sum(x.values()) for x in sur],
            "top_changes": top,
            "scribe_confusions_measured_on_soyga": {k: c.get(tuple(sorted(k.split("/"))), 0) for k in ("X/Z", "N/U", "I/Y", "I/L", "C/E")},
            "consonant_changes": ncc, "share_inside_one_sound_class": round(obs, 3),
            "by_letter_frequency_mean": round(statistics.mean(nul), 3), "p": round(sum(v >= obs for v in nul) / len(nul), 4),
            "surrogate_share_inside_class": round(sum(n for (p, q), n in scc.items() if same(p, q)) / max(1, sum(scc.values())), 3),
            "classes": ["PTCBDG", "LRMN", "SZX"]}


def run():
    rng = random.Random(40)
    book = base_book()
    lines = [r for v in book.values() for r in v if r]
    names = name_list()
    B, C = BC_names(book, names, rng)
    res = {"A_heldout_shared_strings": A_heldout(book, rng), "B_names_in_sequence": B, "C_compounds": C,
           "D_columns_of_long_repeats": D_columns(lines, rng), "E_near_repeats": E_near(book, lines, rng), "F_variation": F_variation(lines, rng)}
    load.save_result("40_formulas", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
