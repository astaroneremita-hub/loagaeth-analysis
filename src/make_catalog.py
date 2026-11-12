"""
Builds viz/names_catalog.html: a visual catalogue of the recurring names of the book.

One card per name (the 13 master names, the 49 discovered by a23, the 8 found under them by a28):
how often it is written, on which sides (a strip of the 94 sides), its family and house, its longer
forms and one-letter variants, the letters around it, passages, and its letters spelled with Dee's
letter names. The meanings of the letters are the practitioner's own layer (a26) and are labelled so.

Everything is computed from the decoded book (a22.base_book); nothing of the transcription itself is
shipped beyond short passages around each name.
"""
import json
import os
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum
from a26_letter_names import FOLD, MEANINGS, dee_names
from a42_repeat_map import part

MASTERS = ["CHASTOR", "CHUSTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"]
# family = the core a name is built on (first match wins)
ROOTS = [("CHASTOR", ["CHASTOR", "CHUSTOR"]), ("NACHO", ["NACHO"]), ("NOCHA", ["NOCHA", "NACHE", "NACHAP"]),
         ("ACLAX", ["ACLAX"]), ("GETH", ["GETH"]), ("ANZACH", ["ANZACH"]), ("ANTANTOX", ["ANTANTOX"]),
         ("CHADAX", ["CHADAX", "CHARDAX"]), ("ALGRA", ["ALGRA"]), ("OXAD", ["OXAD", "OXAR"])]
HOUSE = {"GETH": "GETH · ACLAX", "ACLAX": "GETH · ACLAX", "NOCHA": "NOCHA", "NACHO": "NOCHA"}
ALPHA = "ABCDEFGHILMNOPQRSTUVXYZ"


def run():
    book = base_book()
    keys = sorted(book, key=lambda k: (tnum(k), k))
    # a49: on the row-written tables and the diamonds the lines of a side are one stream (the end of
    # a line runs on into the next), so names are counted over the joined lines; on the chessboard
    # leaves 25b-28b the order of the diagonals is not settled and lines stay apart ("|").
    joined = lambda k: not ((tnum(k) == 25 and k.endswith("b")) or 26 <= tnum(k) <= 28)
    text, brk = {}, {}
    for k in keys:
        ls = [r for r in book[k] if r]
        if joined(k):
            text[k] = "".join(ls)
            pos, b = 0, set()
            for r in ls[:-1]:
                pos += len(r)
                b.add(pos)
            brk[k] = b
        else:
            text[k], brk[k] = "|".join(ls), set()
    S = "|".join(text[k] for k in keys)

    def show(k, a, b):
        return "".join(("/" if p in brk[k] and p > a else "") + text[k][p] for p in range(a, b))
    d23 = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    d28 = json.load(open(os.path.join(load.RESULTS, "28_names_deep.json"), encoding="utf-8"))
    stat = {x["name"]: x for x in d23}
    hidden = [x[0] for x in d28["B5_hidden_names"]["not_seen_before"]]
    order = MASTERS + [x["name"] for x in d23 if x["name"] not in MASTERS] + [h for h in hidden if h not in MASTERS and h not in stat]
    dn = dee_names()
    names = []
    for n in order:
        per = [text[k].count(n) for k in keys]
        tot = sum(per)
        if not tot:
            continue
        fam = next((root for root, pats in ROOTS if any(p in n for p in pats)), "—")
        longer = sorted(((m, S.count(m)) for m in order if m != n and n in m and S.count(m)), key=lambda x: -x[1])
        inside = sorted(((m, S.count(m)) for m in order if m != n and m in n), key=lambda x: -len(x[0]))
        var = []
        for i in range(len(n)):
            for c in ALPHA:
                if c != n[i]:
                    v = n[:i] + c + n[i + 1:]
                    k = S.count(v)
                    if k >= max(3, tot // 40):
                        var.append((v, k, i))
        var.sort(key=lambda x: -x[1])
        before, after = Counter(), Counter()
        ex, cut = [], []
        for k in keys:
            t = text[k]
            i = t.find(n)
            while i >= 0:
                if i and t[i - 1] != "|":
                    before[t[i - 1]] += 1
                j = i + len(n)
                if j < len(t) and t[j] != "|":
                    after[t[j]] += 1
                a, b = t.rfind("|", 0, i) + 1, t.find("|", j)
                b = len(t) if b < 0 else b
                e = (k, show(k, max(a, i - 12), i), show(k, i, j), ("/" if j in brk[k] else "") + show(k, j, min(b, j + 12)).lstrip("/"))
                if any(i < p < j for p in brk[k]):
                    cut.append(e)
                elif len(ex) < 60:
                    ex.append(e)
                i = t.find(n, i + 1)
        step = max(1, len(ex) // 4)
        ex = ex[::step][:4 - min(2, len(cut))] + cut[:2]
        parts = [0] * 6
        for k, c in zip(keys, per):
            parts[part(k)] += c
        st = stat.get(n, {})
        names.append({
            "n": n, "c": tot, "per": per, "fam": fam, "house": HOUSE.get(fam, ""),
            "kind": "master" if n in MASTERS else "hidden" if n in hidden and n not in stat else "discovered",
            "sides": sum(1 for c in per if c), "parts": parts[1:],
            "top": sorted(((keys[i], c) for i, c in enumerate(per) if c), key=lambda x: -x[1])[:5],
            "longer": longer[:10], "inside": inside[:4], "var": [(v, k) for v, k, _ in var[:8]],
            "before": before.most_common(4), "after": after.most_common(4), "nb": sum(before.values()), "na": sum(after.values()),
            "ex": [list(e) for e in ex], "cut": len(cut),
            "z": st.get("z"), "exp": st.get("markov3_expected"),
            "letters": [[c, dn.get(FOLD.get(c, c), "?"), MEANINGS.get(FOLD.get(c, c), "")] for c in n]})
    data = {"keys": keys, "part": [part(k) for k in keys], "names": names,
            "letters_in_book": sum(len(r) for k in keys for r in book[k])}
    tpl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog_template.html"), encoding="utf-8").read()
    out = os.path.join(os.path.dirname(load.DATA), "viz", "names_catalog.html")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(tpl.replace("/*DATA*/null", json.dumps(data, ensure_ascii=False, separators=(",", ":"))))
    print("wrote", out, os.path.getsize(out), "bytes;", len(names), "names")
    return {"names": len(names)}


if __name__ == "__main__":
    run()
