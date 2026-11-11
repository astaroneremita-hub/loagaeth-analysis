"""
47 - Templates: passages with one free slot (the residue left by the false book of a46).

  A) Count. A template is a string of L letters with one inner position left open, written at least
     4 times in tables 2-24 with at least two different fillers written twice or more. How many, for
     L = 9, 11, 13, in the book and in the false books of the machines G3, G5 and G5L?
  B) The largest templates, and what fills the slot.
  C) What kind of letter the slot takes (vowel or consonant), against the machines.
  D) Two slots. Passages of 11 letters with two open positions six letters apart
     (xx_xxxxx_xx): does the filler of the first slot tell the filler of the second? A machine with
     five letters of context cannot link them. Fillers are permuted inside each template and part
     of the book, so the dialect of the parts is not counted.
  E) Anything beyond five letters? Given the five letters before, does the letter k places back
     (k = 6, 7, 8, 10, 14) still help to tell the next letter? Next letters are permuted inside each
     (context, side), so neither the letter model nor the vocabulary of the side is counted. The
     same on a false book (G5L, which has no such memory by construction) and on the Bible cut like
     the tables (which has).
"""
import json
import math
import random
import statistics
from collections import Counter, defaultdict

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum
from a42_repeat_map import part

VOW = set("AEIOUY")


def templates(lines, L):
    occ = defaultdict(Counter)
    for r in lines:
        for i in range(len(r) - L + 1):
            w = r[i:i + L]
            for j in range(2, L - 2):
                occ[(w[:j], w[j + 1:])][w[j]] += 1
    out = {}
    for k, c in occ.items():
        if sum(c.values()) >= 4 and sum(1 for v in c.values() if v >= 2) >= 2:
            out[k] = c
    return out


def two_slot(sides_parts, rng, reps=300):
    occ = defaultdict(list)
    for p, ls in sides_parts:
        for r in ls:
            for i in range(len(r) - 10):
                w = r[i:i + 11]
                occ[w[:2] + w[3:8] + w[9:]].append((w[2], w[8], p))
    fr = {k: v for k, v in occ.items() if len(v) >= 8 and len({a for a, _, _ in v}) >= 2 and len({b for _, b, _ in v}) >= 2}

    def nmi(pairs):
        n = len(pairs)
        ab, a, b = Counter(pairs), Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
        return sum(v * math.log2(v * n / (a[x] * b[y])) for (x, y), v in ab.items())
    obs = sum(nmi([(a, b) for a, b, _ in v]) for v in fr.values())
    nul = []
    for _ in range(reps):
        t = 0.0
        for v in fr.values():
            g = defaultdict(list)
            for j, (_, b, p) in enumerate(v):
                g[p].append(j)
            bs = [b for _, b, _ in v]
            for js in g.values():
                vals = [bs[j] for j in js]
                rng.shuffle(vals)
                for j, x in zip(js, vals):
                    bs[j] = x
            t += nmi([(a, b) for (a, _, _), b in zip(v, bs)])
        nul.append(t)
    n = sum(len(v) for v in fr.values())
    top = sorted(fr.items(), key=lambda kv: -nmi([(a, b) for a, b, _ in kv[1]]))[:8]
    return {"templates": len(fr), "occurrences": n, "bits_per_occurrence": round(obs / max(1, n), 4),
            "permuted": round(statistics.mean(nul) / max(1, n), 4),
            "z": round((obs - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1),
            "p": round((sum(x >= obs for x in nul) + 1) / (reps + 1), 4),
            "strongest": [{"template": k[:2] + "_" + k[2:7] + "_" + k[7:], "pairs": dict(Counter(a + b for a, b, _ in v).most_common(5))} for k, v in top]}


def beyond_five(sides, k, rng, reps=60):
    def nmi(pairs):
        n = len(pairs)
        ab, a, b = Counter(pairs), Counter(x for x, _ in pairs), Counter(y for _, y in pairs)
        return sum(v * math.log2(v * n / (a[x] * b[y])) for (x, y), v in ab.items())
    g = defaultdict(list)
    for si, ls in enumerate(sides):
        for r in ls:
            for i in range(k, len(r)):
                g[(r[i - 5:i], si)].append((r[i - k], r[i]))
    g = {c: v for c, v in g.items() if len(v) >= 4 and len({a for a, _ in v}) > 1 and len({b for _, b in v}) > 1}
    obs = sum(nmi(v) for v in g.values())
    nul = []
    for _ in range(reps):
        t = 0.0
        for v in g.values():
            b = [y for _, y in v]
            rng.shuffle(b)
            t += nmi([(a, y) for (a, _), y in zip(v, b)])
        nul.append(t)
    n = sum(len(v) for v in g.values())
    if not n:
        return {"occurrences": 0, "bits": 0.0, "permuted": 0.0, "z": 0.0}
    return {"occurrences": n, "bits": round(obs / n, 4), "permuted": round(statistics.mean(nul) / n, 4),
            "z": round((obs - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 1)}


def run():
    rng = random.Random(47)
    book = base_book()
    keys = [k for k in sorted(book, key=lambda k: (tnum(k), k)) if 2 <= tnum(k) <= 24]
    sides = [[r for r in book[k] if r] for k in keys]
    parts = [part(k) for k in keys]
    flat = [r for ls in sides for r in ls]
    g3 = CharLM(3, alpha=0.01).fit(flat)
    g5 = CharLM(5, alpha=0.001).fit(flat)
    local = [CharLM(5, alpha=0.001).fit([r for ls in sides[max(0, i - 3):i + 4] for r in ls]) for i in range(len(sides))]
    machines = {"G3": lambda i: g3, "G5": lambda i: g5, "G5L": lambda i: local[i]}
    fake = {n: [[[f(i).sample(len(r), rng) for r in ls] for i, ls in enumerate(sides)] for _ in range(4)] for n, f in machines.items()}

    A, C = {}, {}
    for L in (9, 11, 13):
        t = templates(flat, L)
        row = {"book": len(t)}
        for n, books in fake.items():
            xs = [len(templates([r for ls in b for r in ls], L)) for b in books]
            row[n] = round(statistics.mean(xs), 1)
            row[n + "_max"] = max(xs)
        A[L] = row
        if L == 11:
            def vshare(tt):
                c = Counter()
                for fills in tt.values():
                    f = [x for x, v in fills.items() if v >= 2]
                    c["vowels" if all(x in VOW for x in f) else "consonants" if all(x not in VOW for x in f) else "mixed"] += 1
                s = sum(c.values()) or 1
                return {k: round(v / s, 3) for k, v in c.items()}
            C = {"book": vshare(t), "G5L": vshare(templates([r for ls in fake["G5L"][0] for r in ls], L))}
            big = sorted(t.items(), key=lambda kv: -sum(kv[1].values()))
            B = [{"template": a + "_" + b, "fillers": dict(c.most_common(5))} for (a, b), c in big[:15]]
    D = {"book": two_slot(list(zip(parts, sides)), rng)}
    for n in ("G5", "G5L"):
        r = [two_slot(list(zip(parts, b)), rng, 100) for b in fake[n][:3]]
        D[n] = {"z_of_each_false_book": [x["z"] for x in r], "bits_per_occurrence": [x["bits_per_occurrence"] for x in r],
                "permuted": [x["permuted"] for x in r]}
    from a44_positive_control import cut, kjv_words
    bible = cut("".join(kjv_words(sum(len(r) for r in flat))), 49)
    E = {k: {"tables_2_24": beyond_five(sides, k, rng), "false_book_G5L": beyond_five(fake["G5L"][0], k, rng),
             "bible_english": beyond_five(bible, k, rng)} for k in (6, 7, 8, 10, 14)}
    res = {"E_beyond_five_letters": E, "A_templates_with_one_slot": A, "B_largest_templates_of_11": B, "C_kind_of_slot_11": C, "D_two_slots_six_apart": D}
    load.save_result("47_templates", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
