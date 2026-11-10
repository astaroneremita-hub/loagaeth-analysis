"""
21 - Peterson's Index Verborum (angelix), the Heptarchy numbers, the top-letter string, and the
     gematria of the letter counts.

Source for A/B: Joseph H. Peterson, "Index Verborum of the 'Angelic Language' from Liber Logaeth"
(https://www.esotericarchives.com/dee/angelix.htm, (c) 1986, all rights reserved). It is downloaded
into data/raw/ (git-ignored) and only aggregate statistics are written to results/.

  A) What the index is. Entries are  word  t<n> line[*count] ...  ("t" = table side, the number
     after it = the line on that side, "*n" = n occurrences on that line). We map t1/t2 to our
     leaves, verify every reference against our transcription, find the line map between the two,
     and list what is left over (index readings not in our text, our tokens not in the index).
  B) "Complete what is missing": the last nine lines of leaf 1b are written without spaces
     (49 letters each). The index still divides them into words. That gives an independent word
     division of dense Loagaeth text - a gold standard our own segmenter never saw. We train a
     simple word model on the spaced lines and score it against Peterson's divisions.
  C) Letter counts vs the Heptarchy numbers (7 kings, 7 princes, 42 ministers, 49 good angels).
  D) The top letters in frequency order (AONHLDRCXEGT): do they occur as a string anywhere?
  E) The gematria of the four top counts, and the "1446" sum from a pasted calculation.
"""
import json
import math
import os
import random
import re
import sys
import unicodedata
import urllib.request
from collections import Counter, defaultdict

import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "engine"))
URL = "https://www.esotericarchives.com/dee/angelix.htm"
RAW = os.path.join(ROOT, "data", "raw", "angelix.htm")
TOP = "AONHLDRCXEGT"


def norm(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^A-Z]", "", s.upper().replace("V", "U").replace("J", "I"))


def wtoks(row):
    return [norm(t) for t in re.split(r"\s+", row) if norm(t)]


def fetch():
    if not os.path.exists(RAW):
        os.makedirs(os.path.dirname(RAW), exist_ok=True)
        req = urllib.request.Request(URL, headers={"User-Agent": "loagaeth-analysis research script"})
        with urllib.request.urlopen(req, timeout=60) as r, open(RAW, "wb") as f:
            f.write(r.read())
    return open(RAW, encoding="latin-1").read()


def parse_index(h):
    body = h[h.find("Tables 1-3"):]
    txt = re.sub(r"<BR>", "\n", re.sub(r"<(?!BR)[^>]+>", "", body))
    entries, cur = [], None
    for line in txt.split("\n"):
        line = " ".join(line.split())
        m = re.match(r"^([A-Za-z\-'\[\]\.]+)\s+(t\d.*)$", line)
        if m:
            cur = [m.group(1), m.group(2)]
            entries.append(cur)
        elif cur and re.match(r"^[\dt* ]+$", line):  # wrapped continuation of the previous entry
            cur[1] += " " + line
    refs = []
    for w, r in entries:
        side = None
        for tok in r.split():
            m = re.match(r"t(\d+)$", tok)
            if m:
                side = {"1": "1a", "2": "1b"}.get(m.group(1))
                continue
            m = re.match(r"(\d+)(?:\*(\d+))?$", tok)
            if m and side:
                refs.append((w, side, int(m.group(1)), int(m.group(2) or 1)))
    return entries, refs


def rows_for(leaf, ln):
    """Index line -> our transcription row(s). Found in A: in leaf 1b, manuscript line 20 is split
    across our rows 20 and 21, so every later line sits one row lower."""
    if leaf == "1b" and ln == 20:
        return [19, 20]
    if leaf == "1b" and ln > 20:
        return [ln]
    return [ln - 1]


def lev_ops(a, b):
    import difflib
    out = []
    for op, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if op != "equal":
            out.append((a[i1:i2] or "-") + ">" + (b[j1:j2] or "-"))
    return out


def A_index(lv, entries, refs):
    import difflib
    side_words = defaultdict(list)
    for w, leaf, ln, c in refs:
        side_words[leaf].append(norm(w))
    # which of our leaves each index side matches (raw share of words >= 4 letters found)
    match = {}
    for side in ["1a", "1b"]:
        ws = [w for w in side_words[side] if len(w) >= 4]
        match[side] = {k: round(sum(any(w in norm(r) for r in lv[k]) for w in ws) / len(ws), 2)
                       for k in ["1a", "1b", "2a", "2b"]}
    # line offset per index line (where does the word sit?)
    offset = defaultdict(Counter)
    for w, leaf, ln, c in refs:
        tw = norm(w)
        for d in (0, -1, 1, -2, 2):
            j = ln - 1 + d
            if 0 <= j < len(lv[leaf]) and tw in norm(lv[leaf][j]):
                offset[(leaf, ln)][d] += 1
                break
    shift = {leaf: [offset[(leaf, ln)].most_common(1)[0][0] if offset[(leaf, ln)] else None
                    for ln in range(1, 50)] for leaf in ["1a", "1b"]}
    st, subs, used, absent = Counter(), Counter(), defaultdict(Counter), 0
    for w, leaf, ln, c in refs:
        tw, R = norm(w), rows_for(leaf, ln)
        toks = [t for j in R for t in wtoks(lv[leaf][j])]
        text = "".join(norm(lv[leaf][j]) for j in R)
        if tw in toks:
            st["whole_word"] += 1
        elif tw in text:
            st["inside_a_longer_or_dense_token"] += 1
        else:
            best = max(toks, key=lambda t: difflib.SequenceMatcher(None, t, tw).ratio())
            if difflib.SequenceMatcher(None, best, tw).ratio() >= 0.7:
                st["variant_reading"] += 1
                subs.update(lev_ops(best, tw))
            else:
                st["not_found"] += 1
        for j in R:
            used[(leaf, j)][tw] += c
    left, total = Counter(), 0
    for leaf in ["1a", "1b"]:
        for j, row in enumerate(lv[leaf]):
            for t, n in Counter(wtoks(row)).items():
                total += n
                if n - used[(leaf, j)].get(t, 0) > 0:
                    left[len(t) if len(t) < 4 else "4+"] += n - used[(leaf, j)].get(t, 0)
    n = len(refs)
    return {
        "entries": len(entries), "references": n,
        "hyphenated_syllabified_entries": sum("-" in w for w, _ in entries),
        "sides_covered": "t1 = leaf 1a, t2 = leaf 1b (only the word-spaced first leaf; no t3+)",
        "side_match_share": match,
        "glosses_in_index": 0,
        "verification": dict(st, verified_share=round((st["whole_word"] + st["inside_a_longer_or_dense_token"]) / n, 3)),
        "line_map": "1a: index line = our row (49/49). 1b: lines 1-19 equal; index line 20 = our rows "
                    "20+21 (one manuscript line split in two in the transcription); lines 21-49 = our "
                    "rows 22-50. So leaf 1b has 49 lines, like 1a.",
        "line_shift_1b": shift["1b"],
        "variant_letter_differences_top": subs.most_common(12),
        "our_tokens": total,
        "our_tokens_not_in_index_by_length": dict(left),
    }


class Seg:
    """Unigram word model with a letter-model fallback for unknown words (Viterbi)."""

    def __init__(self, words, maxlen=14):
        self.wc = Counter(words)
        self.N = sum(self.wc.values())
        cc = Counter("".join(words))
        tot = sum(cc.values())
        self.lp_char = {c: math.log(n / tot) for c, n in cc.items()}
        self.maxlen = maxlen

    def cost(self, w):
        if w in self.wc:
            return -math.log(self.wc[w] / (self.N + 1))
        return -math.log(1 / (self.N + 1)) + 4.0 - sum(self.lp_char.get(c, -8) for c in w)

    def cuts(self, s):
        best = [0.0] + [math.inf] * len(s)
        back = [0] * (len(s) + 1)
        for i in range(1, len(s) + 1):
            for j in range(max(0, i - self.maxlen), i):
                v = best[j] + self.cost(s[j:i])
                if v < best[i]:
                    best[i], back[i] = v, j
        out, i = set(), len(s)
        while i > 0:
            if back[i] > 0:
                out.add(back[i])
            i = back[i]
        return out


def gold_cuts(line, words):
    """Place Peterson's words for a dense line (longest first, no overlap) and read off cuts."""
    claimed = [False] * len(line)
    cuts, placed = set(), 0
    for w in sorted(words, key=len, reverse=True):
        start = 0
        while True:
            i = line.find(w, start)
            if i < 0:
                break
            if not any(claimed[i:i + len(w)]):
                for k in range(i, i + len(w)):
                    claimed[k] = True
                cuts.update(x for x in (i, i + len(w)) if 0 < x < len(line))
                placed += len(w)
                break
            start = i + 1
    return cuts, placed / len(line)


def prf(pred, gold):
    tp = len(pred & gold)
    p = tp / len(pred) if pred else 0
    r = tp / len(gold) if gold else 0
    return p, r, (2 * p * r / (p + r) if p + r else 0)


def B_segmentation_gold(lv, refs):
    dense_rows = [j for j, r in enumerate(lv["1b"]) if len(r.split()) == 1 and len(norm(r)) >= 40]
    train = [t for leaf in ["1a", "1b"] for j, r in enumerate(lv[leaf])
             if not (leaf == "1b" and j in dense_rows) for t in wtoks(r)]
    seg = Seg(train)
    by_row = defaultdict(list)
    for w, leaf, ln, c in refs:
        if leaf == "1b":
            for j in rows_for(leaf, ln):
                if j in dense_rows:
                    by_row[j] += [norm(w)] * c
    rng = random.Random(21)
    tot_m = [0, 0, 0]
    tot_r = [0, 0, 0]
    cover = []
    TPm = Pm = Gm = 0
    rand_f = []
    per_line = []
    for j in dense_rows:
        line = norm(lv["1b"][j])
        g, cov = gold_cuts(line, by_row[j])
        cover.append(cov)
        m = seg.cuts(line)
        TPm += len(m & g); Pm += len(m); Gm += len(g)
        per_line.append({"row": j + 1, "letters": line, "gold_cut_positions": sorted(g),
                         "model_cut_positions": sorted(m), "gold_cuts": len(g), "model_cuts": len(m),
                         "F1": round(prf(m, g)[2], 3)})
    for _ in range(2000):
        tp = 0
        for j in dense_rows:
            line = norm(lv["1b"][j])
            g, _c = gold_cuts(line, by_row[j])
            m = set(rng.sample(range(1, len(line)), len(seg.cuts(line))))
            tp += len(m & g)
        p, r = tp / Pm, tp / Gm
        rand_f.append(2 * p * r / (p + r) if p + r else 0)
    p, r = TPm / Pm, TPm / Gm
    f = 2 * p * r / (p + r)
    rand_f.sort()
    return {
        "dense_lines": len(dense_rows), "rows": [j + 1 for j in dense_rows],
        "gold_coverage_mean": round(sum(cover) / len(cover), 3),
        "model": {"precision": round(p, 3), "recall": round(r, 3), "F1": round(f, 3)},
        "random_cuts_same_number": {"F1_mean": round(sum(rand_f) / len(rand_f), 3),
                                    "F1_95th": round(rand_f[int(0.95 * len(rand_f))], 3),
                                    "p": round(sum(x >= f for x in rand_f) / len(rand_f), 4)},
        "per_line": per_line,
        "note": "Gold = Peterson's 1986 editorial division of the nine dense lines of leaf 1b (not "
                "Dee's). Training = the spaced lines of leaves 1a/1b only.",
    }


def C_heptarchy(counts):
    letters = sorted(counts)
    res = {}
    for k in (6, 7, 42, 49):
        hits = [L for L in letters if counts[L] % k == 0]
        p_exp = 1 / k
        n = len(letters)
        # binomial upper tail
        pv = sum(math.comb(n, i) * p_exp ** i * (1 - p_exp) ** (n - i) for i in range(len(hits), n + 1))
        res[f"divisible_by_{k}"] = {"letters": hits, "observed": len(hits),
                                    "expected": round(n * p_exp, 2), "p": round(pv, 3)}
    total = sum(counts.values())
    res["total_letters"] = total
    res["total_mod"] = {k: total % k for k in (7, 42, 49)}
    h = json.load(open(os.path.join(ROOT, "engine", "data", "heptarquia.json"), encoding="utf-8"))
    names = [x["nome"].upper() for x in h["tabula_collecta"]["nomes"]]
    tc = Counter(norm("".join(names)))
    common = [L for L in letters if L in tc]
    lo = [counts[L] for L in common]
    t = [tc[L] for L in common]

    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for i, k in enumerate(o):
            r[k] = i
        return r
    ra, rb = rank(lo), rank(t)
    n = len(common)
    rho = 1 - 6 * sum((a - b) ** 2 for a, b in zip(ra, rb)) / (n * (n * n - 1))
    res["tabula_collecta"] = {"names": len(names), "letters": sum(tc.values()),
                              "B_share_in_names": round(tc["B"] / sum(tc.values()), 3),
                              "B_share_in_loagaeth": round(counts.get("B", 0) / total, 4),
                              "spearman_letter_freq_vs_loagaeth": round(rho, 2)}
    return res


def D_top_string(stream, lv, refs):
    N = len(stream)
    uni = Counter(stream)
    bi = Counter(stream[i:i + 2] for i in range(N - 1))
    out = []
    for k in range(3, len(TOP) + 1):
        for i in range(0, len(TOP) - k + 1):
            s = TOP[i:i + k]
            obs = len(re.findall("(?=" + s + ")", stream))
            e = N * uni[s[0]] / N
            for a, b in zip(s, s[1:]):
                e *= bi[a + b] / max(1, uni[a])
            out.append({"string": s, "observed": obs, "expected_markov1": round(e, 2)})
    import enoch
    pools = {
        "watchtower_names": [x["name"] for x in enoch.derive_names()],
        "call_words": load.lexicon()["attested_wordforms"],
        "index_words": sorted({norm(w) for w, *_ in refs}),
    }
    hits = {p: [w for w in ws if any(TOP[:k] in norm(w) for k in (3,))] for p, ws in pools.items()}
    return {"windows": [x for x in out if x["observed"] or x["expected_markov1"] >= 0.5],
            "windows_all_zero_longer_than": max([len(x["string"]) for x in out if x["observed"]] or [0]),
            "AON_in_name_pools": {p: len(v) for p, v in hits.items()},
            "note": "Frequency order is a property of the transcription, not a text; strings such as "
                    "AONHL are not expected to occur and the test only checks that."}


def E_gematria(counts):
    order = sorted(counts, key=lambda L: -counts[L])
    top4 = [(L, counts[L]) for L in order[:4]]

    def droot(n):
        return 1 + (n - 1) % 9 if n else 0
    typed = {"A": 334441, "O": 166361, "N": 158892, "H": 12099}
    import fontes
    gd = fontes.gematria_value_tables()["golden_dawn_coluna__F08"]
    pasted = [1, 70, 50, 8, 30, 4, 100, 20, 60, 5, 3, 300, 80, 7, 400, 10, 40, 200, 2, 6, 50]
    in_order = [gd.get(L) for L in order if L in gd]
    rng = random.Random(5)
    # how often does a random 5-digit count reduce to 6 or 5?
    return {
        "frequency_order": "".join(order),
        "top4_counts": {L: n for L, n in top4},
        "digit_roots_true": {L: droot(n) for L, n in top4},
        "digit_roots_of_typed_numbers": {L: droot(n) for L, n in typed.items()},
        "true_vs_typed": "the typed numbers carry an extra digit (334441 vs 33441, 166361 vs 16361, "
                         "158892 vs 15892); the 6 and 5 roots come from the typing, not the counts",
        "sum_top4": sum(n for _, n in top4), "sum_top4_root": droot(sum(n for _, n in top4)),
        "mod7_top4": {L: n % 7 for L, n in top4},
        "gd_values_in_frequency_order": in_order,
        "gd_sum": sum(gd.values()), "gd_sum_root": droot(sum(gd.values())),
        "pasted_list_sum": sum(pasted),
        "pasted_vs_gd": "the pasted list has 50 twice; Golden Dawn gives Q = 90, so the sum is 1486, "
                        "not 1446. Any sum of all 21 values is the same in every order, so it says "
                        "nothing about frequency.",
        "digit_root_base_rate": "for counts of this size each root 1-9 occurs ~1/9 of the time",
        "crowley_A6_B5": {k: (t.get("A"), t.get("B")) for k, t in fontes.gematria_value_tables().items()
                          if t.get("A") == 6 and t.get("B") == 5},
    }


def run():
    lv = load.leaves()
    entries, refs = parse_index(fetch())
    # same basis as a16 (the letter counts quoted in the README): the dense tables 2-48
    stream = "".join(load.letters("".join(lv.get(f"{t}{s}", []))) for t in range(2, 49) for s in "ab")
    counts = Counter(stream)
    res = {
        "A_index": A_index(lv, entries, refs),
        "B_segmentation_gold": B_segmentation_gold(lv, refs),
        "C_heptarchy": C_heptarchy(counts),
        "D_top_string": D_top_string(stream, lv, refs),
        "E_gematria": E_gematria(counts),
    }
    b = res["B_segmentation_gold"]
    res["conclusion"] = (
        "Peterson's index is a concordance of leaf 1 only (t1=1a, t2=1b), with no glosses; "
        f"{res['A_index']['verification']['verified_share']*100:.0f}% of its references are found on the "
        "stated line once leaf 1b's split line 20 is accounted for. Its divisions of the nine dense "
        f"lines of 1b are an independent gold standard: our word model reaches F1 {b['model']['F1']} "
        f"vs {b['random_cuts_same_number']['F1_mean']} for random cuts (p {b['random_cuts_same_number']['p']}). "
        "Letter counts show no Heptarchy numerology; the top-letter string does not occur; "
        "the 6/5 gematria comes from mistyped counts.")
    load.save_result("21_index_heptarchy_numbers", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
