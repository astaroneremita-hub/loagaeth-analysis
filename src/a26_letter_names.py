"""
26 - The letter names as a reading layer (a construction, clearly labelled).

The 21 letters of the Angelic alphabet have names in Dee's own table (Pa, Veh, Ged, Gal, Or, Un,
Graph, Tal, Gon, Na, Ur, Mals, Ger, Drux, Pal, Med, Don, Ceph, Van, Fam, Gisg - bundled in
engine/data/gematria_enoquiana.json). Dee gives the names, not meanings. The meanings used here are
a modern attribution supplied by the practitioner (MEANINGS below); they are a lens, not evidence.

  A) Readings: every master and discovered name spelled out as letter names and meanings.
  B) Positional grammar in this lens: which letters (and so which meanings) open words, close
     words, and fill them - from the measured onset/terminator profile, not from the meanings.
  C) Meaning profile of each side: share of each letter vs the book average (enrichment), so each
     square gets a "letter chart". Which letters set the segments apart.
  D) Theme test: do the recurring names use letters of some meanings more than random strings of
     the same book (same lengths)? This only re-expresses letter frequencies in names, and says so.
"""
import json
import os
import random
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# practitioner-supplied meanings (modern attribution, not in Dee)
MEANINGS = {
    "A": "indomitable, pulsing force", "B": "vessel, container", "C": "crowned conquest",
    "D": "physicality", "E": "power of being", "F": "connection", "G": "nourishment, reward, sustenance",
    "H": "life", "I": "spirituality", "L": "learning", "M": "fulfilment, completion",
    "N": "emergence", "O": "insight", "P": "speech", "Q": "righteousness", "R": "growth",
    "S": "cosmic vessel", "T": "goodness / cosmic nourishment", "U": "true law", "X": "support",
    "Z": "movement",
}
FOLD = {"V": "U", "J": "I", "Y": "I", "K": "C", "W": "U"}


def dee_names():
    g = json.load(open(os.path.join(ROOT, "engine", "data", "gematria_enoquiana.json"), encoding="utf-8"))
    out = {}
    for e in g["a_alfabeto_dee"]["ordem_da_tabela_de_dee"]:
        L = e.get("letra_canonica")
        if L and L not in out and not e.get("forma_variante_de"):
            out[L] = e["nome"]
    return out


def reading(name, names):
    s = [FOLD.get(c, c) for c in name]
    return {"name": name,
            "letters": " · ".join(names.get(c, c) for c in s),
            "meanings": " → ".join(MEANINGS.get(c, "?") for c in s)}


def run():
    rng = random.Random(26)
    names = dee_names()
    book = base_book()
    disc = []
    p23 = os.path.join(load.RESULTS, "23_name_discovery.json")
    if os.path.exists(p23):
        disc = [c["name"] for c in json.load(open(p23, encoding="utf-8"))["A_candidates"]["top"]]
    masters = ["CHASTOR", "CHUSTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX"]
    A = [reading(n, names) for n in masters + [d for d in disc if d not in masters]]

    # B) onset / terminator / interior profile on row-written squares (positions 0, 48, 5..43)
    first, last, mid = Counter(), Counter(), Counter()
    for k, v in book.items():
        if tnum(k) <= 25 and k != "25b":
            for r in v:
                if len(r) >= 45:
                    r = "".join(FOLD.get(c, c) for c in r)
                    first[r[0]] += 1
                    last[r[-1]] += 1
                    mid.update(r[5:-5])

    def enrich(c):
        n, m = sum(c.values()), sum(mid.values())
        return {L: round((c[L] / n) / (mid[L] / m), 2) for L in MEANINGS if mid[L]}
    ef, el = enrich(first), enrich(last)
    B = {"opens_rows": [{"letter": L, "name": names.get(L), "meaning": MEANINGS[L], "x_interior": ef[L]}
                        for L in sorted(ef, key=lambda L: -ef[L])[:5]],
         "closes_rows": [{"letter": L, "name": names.get(L), "meaning": MEANINGS[L], "x_interior": el[L]}
                         for L in sorted(el, key=lambda L: -el[L])[:5]],
         "never_opens": [L for L in ef if ef[L] < 0.15], "never_closes": [L for L in el if el[L] < 0.15]}

    # C) per-side letter profile and enrichment
    tot = Counter()
    side = {}
    for k, v in book.items():
        c = Counter(FOLD.get(ch, ch) for r in v for ch in r)
        side[k] = c
        tot.update(c)
    T = sum(tot.values())
    prof = {}
    for k in sorted(side, key=lambda k: (tnum(k), k[-1])):
        c = side[k]
        n = sum(c.values())
        prof[k] = {L: [c[L], round((c[L] / n) / (tot[L] / T), 2) if tot[L] else 0] for L in MEANINGS}
    SEG = {"opening": range(2, 6), "heartland": range(6, 26), "decoded 26-28": range(26, 29),
           "diamonds": range(29, 44), "end": range(44, 49)}
    segtop = {}
    for s, rg in SEG.items():
        c = Counter()
        for k in side:
            if tnum(k) in rg:
                c.update(side[k])
        n = sum(c.values())
        en = {L: (c[L] / n) / (tot[L] / T) for L in MEANINGS if tot[L] > 200}
        segtop[s] = [{"letter": L, "name": names.get(L), "meaning": MEANINGS[L], "x_book": round(en[L], 2)}
                     for L in sorted(en, key=lambda L: -en[L])[:3]]

    # D) letters of the recurring names vs random book strings of the same lengths
    lines = [r for v in book.values() for r in v if len(r) > 15]
    nm = Counter(FOLD.get(c, c) for n in disc for c in n)
    rnd = Counter()
    for _ in range(200):
        for n in disc:
            r = rng.choice(lines)
            i = rng.randrange(len(r) - len(n))
            rnd.update(FOLD.get(c, c) for c in r[i:i + len(n)])
    a, b = sum(nm.values()), sum(rnd.values())
    D = sorted(({"letter": L, "name": names.get(L), "meaning": MEANINGS[L],
                 "x_random": round((nm[L] / a) / (rnd[L] / b), 2)} for L in MEANINGS if rnd[L]),
               key=lambda d: -d["x_random"])
    res = {"provenance": "Letter names: Dee's alphabet table (bundled). Meanings: modern attribution "
                         "supplied by the practitioner; not in Dee. Construction, not evidence.",
           "letter_names": names,
           "A_readings": A, "B_positions": B, "C_side_profiles": prof, "C_segment_signature": segtop,
           "D_letters_of_names_vs_random": D}
    load.save_result("26_letter_names", res)
    return res


if __name__ == "__main__":
    r = run()
    print(json.dumps({k: v for k, v in r.items() if k != "C_side_profiles"}, ensure_ascii=False, indent=1)[:5000])
