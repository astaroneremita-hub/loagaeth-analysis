"""
23 - Name discovery without supervision, name families, and a grammar for them.

  A) Candidates. Every string of 4-14 letters that recurs (>= 6 times, in >= 3 tables) and behaves
     like a word: the letters after it and before it are varied (high branching entropy on both
     sides - Harris's criterion for a word boundary). Each candidate is compared with the count a
     Markov-3 model of the book predicts for it (z score); only those beyond Bonferroni survive.
     Positive control: the method must find CHASTOR, ANZACH, GETH, NOCHA on its own.
  B) Validation. (i) share of candidates that occur inside Dee's own spaced words of leaf 1;
     (ii) using the surviving lexicon as the dictionary of the segmenter, F1 against Peterson's
     division of the dense lines of leaf 1b (a21/a22: 0.33-0.36, random 0.16).
  C) Families. Candidates linked when one is the other plus/minus up to 2 letters at an end
     (title prefixes, endings) or differs by one vowel (A/U twins). Connected components = families.
     Null: the same procedure on candidates found in a Markov-3 surrogate of the same size.
  D) Grammar. For each family: core (longest common substring), its prefixes and suffixes, and the
     description length of the family as a list vs as core x prefixes x suffixes.
"""
import json
import math
import random
from collections import Counter, defaultdict

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book, tnum

KNOWN = ["CHASTOR", "ANZACH", "GETH", "NOCHA", "ALGETH", "ACLAX", "CHUSTOR", "ADNOCHA", "OXAD", "CHADAX"]
SEG_OF = {**{t: "opening" for t in range(2, 6)}, **{t: "heartland" for t in range(6, 26)},
          **{t: "decoded 26-28" for t in range(26, 29)}, **{t: "diamonds" for t in range(29, 44)},
          **{t: "end" for t in range(44, 49)}}


def lines_by_table(book):
    out = defaultdict(list)
    for k, v in book.items():
        out[tnum(k)] += v
    return out


def kgram_stats(lines, kmin=3, kmax=15, min_count=6):
    cnt = Counter()
    for r in lines:
        n = len(r)
        for k in range(kmin, kmax + 1):
            for i in range(n - k + 1):
                cnt[r[i:i + k]] += 1
    cnt = Counter({g: c for g, c in cnt.items() if c >= min_count})
    right = defaultdict(Counter)
    left = defaultdict(Counter)
    for r in lines:
        n = len(r)
        for k in range(kmin, kmax + 1):
            for i in range(n - k + 1):
                g = r[i:i + k]
                if g in cnt:
                    right[g][r[i + k] if i + k < n else "#"] += 1
                    left[g][r[i - 1] if i > 0 else "#"] += 1
    return cnt, left, right


def H(c):
    n = sum(c.values())
    return -sum(v / n * math.log2(v / n) for v in c.values())


class M3:
    def __init__(self, lines):
        self.c4, self.c3 = Counter(), Counter()
        for r in lines:
            for i in range(len(r) - 3):
                self.c4[r[i:i + 4]] += 1
            for i in range(len(r) - 2):
                self.c3[r[i:i + 3]] += 1
        self.N3 = sum(self.c3.values())
        self.ctx = Counter()
        for g, v in self.c4.items():
            self.ctx[g[:3]] += v

    def expected(self, s, n_positions):
        p = self.c3[s[:3]] / self.N3
        for i in range(3, len(s)):
            c = self.ctx[s[i - 3:i]]
            p *= (self.c4[s[i - 3:i + 1]] / c) if c else 0
        return n_positions * p


def candidates(lines, tables_of, min_count=6, min_tables=3):
    cnt, left, right = kgram_stats(lines, 4, 14)
    m3 = M3(lines)
    npos = sum(len(r) for r in lines)
    out = []
    for g, c in cnt.items():
        if c < min_count:
            continue
        hr, hl = H(right[g]), H(left[g])
        if hr < 2.0 or hl < 2.0:
            continue
        nt = len(tables_of(g))
        if nt < min_tables:
            continue
        e = m3.expected(g, npos)
        z = (c - e) / math.sqrt(e) if e > 0 else float("inf")
        out.append({"name": g, "count": c, "tables": nt, "h_left": round(hl, 2), "h_right": round(hr, 2),
                    "markov3_expected": round(e, 2), "z": round(z, 1) if z != float("inf") else 999})
    return out


def keep_maximal(cands):
    """Drop a candidate if a longer candidate contains it with >= 80% of its count (it is only a
    piece of the longer name)."""
    by = {c["name"]: c for c in cands}
    out = []
    for c in cands:
        g = c["name"]
        sup = [d for d in cands if len(d["name"]) > len(g) and g in d["name"] and d["count"] >= 0.8 * c["count"]]
        if not sup:
            out.append(c)
    return out


def families(names):
    names = sorted(set(names), key=len)
    S = set(names)
    adj = defaultdict(set)
    vow = "AEIOU"
    for a in names:
        for b in names:
            if a >= b:
                continue
            x, y = (a, b) if len(a) <= len(b) else (b, a)
            d = len(y) - len(x)
            link = False
            if 1 <= d <= 2 and (y.startswith(x) or y.endswith(x)):
                link = True
            elif d == 0:
                diff = [(p, q) for p, q in zip(x, y) if p != q]
                if len(diff) == 1 and diff[0][0] in vow and diff[0][1] in vow:
                    link = True
            if link:
                adj[a].add(b)
                adj[b].add(a)
    seen, comps = set(), []
    for n in names:
        if n in seen or n not in adj:
            continue
        st, comp = [n], []
        while st:
            u = st.pop()
            if u in seen:
                continue
            seen.add(u)
            comp.append(u)
            st += list(adj[u] - seen)
        comps.append(sorted(comp, key=len))
    return sorted(comps, key=len, reverse=True)


def lcs(strs):
    s0 = min(strs, key=len)
    for L in range(len(s0), 2, -1):
        for i in range(len(s0) - L + 1):
            sub = s0[i:i + L]
            if all(sub in s for s in strs):
                return sub
    return ""


def grammar(fam):
    core = lcs(fam)
    pre, suf = set(), set()
    for f in fam:
        i = f.find(core)
        pre.add(f[:i])
        suf.add(f[i + len(core):])
    list_len = sum(len(f) for f in fam)
    gram_len = len(core) + sum(len(p) for p in pre) + sum(len(s) for s in suf)
    covered = len(pre) * len(suf)
    return {"core": core, "prefixes": sorted(pre, key=len), "suffixes": sorted(suf, key=len),
            "members": len(fam), "slots_product": covered,
            "letters_as_list": list_len, "letters_as_grammar": gram_len}


def run():
    rng = random.Random(23)
    book = base_book()
    tl = lines_by_table(book)
    lines = [r for v in book.values() for r in v]
    tab_text = {t: "|".join(v) for t, v in tl.items()}

    def tables_of(g):
        return [t for t, s in tab_text.items() if g in s]
    cands = keep_maximal(candidates(lines, tables_of))
    m = len(cands)
    zcrit = 4.0 if m < 300 else 4.5  # ~Bonferroni for a few hundred tests
    surv = [c for c in cands if c["z"] >= zcrit]
    for c in surv:
        ts = tables_of(c["name"])
        seg = Counter(SEG_OF.get(t, "?") for t in ts)
        c["segments"] = dict(seg)
        c["first_last_table"] = [min(ts), max(ts)]
    surv.sort(key=lambda c: -c["count"])
    names = [c["name"] for c in surv]
    control = {k: any(k in n or n in k and len(n) >= len(k) - 1 for n in names) for k in KNOWN}

    # surrogate: same procedure on a Markov-3 copy (line lengths kept)
    flat = "".join(lines)
    sur = markov3(flat, rng)
    sl, i = [], 0
    for r in lines:
        sl.append(sur[i:i + len(r)])
        i += len(r)
    st_text = {}
    j = 0
    for t, v in tl.items():
        st_text[t] = "|".join(sl[j:j + len(v)])
        j += len(v)
    sc = keep_maximal(candidates(sl, lambda g: [t for t, s in st_text.items() if g in s]))
    s_surv = [c for c in sc if c["z"] >= zcrit]

    # validation (i): inside Dee's spaced words of leaf 1
    import a21_index_heptarchy_numbers as a21
    lv = load.leaves()
    leafwords = {t for leaf in ["1a", "1b"] for r in lv[leaf] if len(r.split()) > 1 for t in a21.wtoks(r)}
    in_leaf1 = sum(any(n in w for w in leafwords) for n in names)
    # random strings of the same lengths drawn from the book, for comparison
    rnd = []
    for n in names:
        r_ = rng.choice([x for x in lines if len(x) > len(n)])
        k = rng.randrange(len(r_) - len(n))
        rnd.append(r_[k:k + len(n)])
    in_leaf1_rand = sum(any(n in w for w in leafwords) for n in rnd)

    # validation (ii): lexicon as segmenter dictionary vs Peterson
    _, refs = a21.parse_index(a21.fetch())
    dense = [j for j, r in enumerate(lv["1b"]) if len(r.split()) == 1 and len(a21.norm(r)) >= 40]
    train = [t for leaf in ["1a", "1b"] for j, r in enumerate(lv[leaf]) if not (leaf == "1b" and j in dense) for t in a21.wtoks(r)]
    by_row = defaultdict(list)
    for w, leaf, ln, c in refs:
        if leaf == "1b":
            for jj in a21.rows_for(leaf, ln):
                if jj in dense:
                    by_row[jj] += [a21.norm(w)] * c
    seg0 = a21.Seg(train)
    seg1 = a21.Seg(train + [c["name"] for c in surv for _ in range(min(c["count"], 50))])
    res_f = {}
    for lab, sg in (("leaf1_words_only", seg0), ("plus_discovered_names", seg1)):
        tp = P = G = 0
        for jj in dense:
            line = a21.norm(lv["1b"][jj])
            g, _ = a21.gold_cuts(line, by_row[jj])
            mm = sg.cuts(line)
            tp += len(mm & g)
            P += len(mm)
            G += len(g)
        p, r = tp / P, tp / G
        res_f[lab] = round(2 * p * r / (p + r), 3)

    fams = families(names)
    sfams = families([c["name"] for c in s_surv])
    gram = [grammar(f) for f in fams if len(f) >= 3]
    new = [c for c in surv if not any(k in c["name"] or c["name"] in k for k in KNOWN)]
    res = {
        "A_candidates": {"tested": m, "z_threshold": zcrit, "survivors": len(surv),
                         "surrogate_survivors": len(s_surv),
                         "positive_control_found": control,
                         "top": surv[:60]},
        "A_new_names_outside_known_families": new[:40],
        "B_validation": {"share_inside_dee_leaf1_words": round(in_leaf1 / max(1, len(names)), 3),
                         "random_book_strings_same_lengths": round(in_leaf1_rand / max(1, len(names)), 3),
                         "segmentation_F1_vs_peterson": res_f},
        "C_families": {"families": len(fams), "largest": fams[:12],
                       "families_size_ge3": sum(len(f) >= 3 for f in fams),
                       "surrogate_families_size_ge3": sum(len(f) >= 3 for f in sfams)},
        "D_grammar": gram[:15],
    }
    load.save_result("23_name_discovery", res)
    return res


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: (v if k != "A_candidates" else {kk: vv for kk, vv in v.items() if kk != "top"})
                      for k, v in r.items()}, ensure_ascii=False, indent=1)[:6000])
