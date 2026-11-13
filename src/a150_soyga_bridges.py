"""
150 - Soyga <-> Loagaeth <-> Watchtowers: direct bridge tests.

The Book of Soyga (Aldaraia) is a different Dee manuscript, but eight of its 36x36 tables are copied
at the back of the same Sloane 3189 that holds the Loagaeth (a36), and Reeds (1998) gave their exact
generator (a cell = cell-above + f(cell-left) mod 23). a61 already showed the Loagaeth is NOT built by
that neighbour rule (a Soyga cell is fully determined; a Loagaeth cell keeps most of its entropy).

This asks the questions a61 did not:
  1. Do Loagaeth names or Watchtower names LIVE inside the Soyga tables (substring, rows+cols), above a
     shuffle null? And the reverse - Soyga rows inside the Loagaeth/Towers?
  2. Does Soyga share the SOUND system (letter frequency, bigrams) with the Loagaeth and the Towers, or
     stand apart? (The Towers and Loagaeth are sisters of one alphabet - is Soyga a third sister, or
     unrelated latin text?)
  3. The anti-hiatus (vowel-vowel avoidance) that marks the Loagaeth - does Soyga have it?

Soyga is written in the 23-letter latin alphabet; Loagaeth/Towers in romanised Enochian (same latin
letters). All normalised to upper case for comparison.
"""
import json
import math
import random
import statistics
from collections import Counter

import load
import a36_soyga_calibration as a36

VOW = set("AEIOU")


def up(s):
    return "".join(ch for ch in s.upper() if ch.isalpha())


# ---------- corpora ----------
def soyga_streams():
    """Rows and columns of the 8 generated (clean) Soyga tables + the real transcribed ones."""
    gen_rows, gen_cols = [], []
    for w in a36.WORDS:
        G = a36.generate(w)
        for r in range(36):
            gen_rows.append(up("".join(G[r])))
        for c in range(36):
            gen_cols.append(up("".join(G[r][c] for r in range(36))))
    real_rows = []
    for T in a36.parse():
        for row in T:
            if len(row) >= 4:
                real_rows.append(up("".join(row)))
    return gen_rows, gen_cols, real_rows


def tower_data():
    q = json.load(open(load.ROOT + "/engine/data/quadrados.json", encoding="utf-8"))
    names, grids = set(), []
    for quad in ("ar", "agua", "terra", "fogo"):
        cells = q.get(quad, [])
        for cell in cells:
            for nm in cell.get("names", []):
                if nm:
                    names.add(up(nm))
        # rebuild the quadrant grid from letter/row/col
        rows = {}
        for cell in cells:
            if "letter" in cell and "row" in cell and "col" in cell:
                rows.setdefault(cell["row"], {})[cell["col"]] = up(cell["letter"])
        for r in sorted(rows):
            line = "".join(rows[r][c] for c in sorted(rows[r]))
            if len(line) >= 4:
                grids.append(line)
    # also the governors / tribe kings as attested Tower-system names
    g = json.load(open(load.ROOT + "/engine/data/governadores.json", encoding="utf-8"))
    for gov in g.get("governadores", []):
        nm = up(gov.get("nome", "") if isinstance(gov, dict) else str(gov))
        if len(nm) >= 4:
            names.add(nm)
    return {w for w in names if len(w) >= 4}, grids


def loag_names():
    return [up(w) for w in json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8")) if len(up(w)) >= 4]


# ---------- 1. substring presence ----------
def count_hits(names, streams):
    hits = 0
    for w in names:
        if any(w in s for s in streams):
            hits += 1
    return hits


def shuffle_streams(streams, rng):
    out = []
    for s in streams:
        cs = list(s)
        rng.shuffle(cs)
        out.append("".join(cs))
    return out


def substring_test(names, streams, rng, label, trials=200):
    real = count_hits(names, streams)
    null = []
    for _ in range(trials):
        null.append(count_hits(names, shuffle_streams(streams, rng)))
    m = statistics.mean(null)
    sd = statistics.pstdev(null) or 1e-9
    return {"corpus": label, "names": len(names), "hits_real": real, "hits_null_mean": round(m, 2),
            "z": round((real - m) / sd, 2), "p": round((sum(1 for x in null if x >= real) + 1) / (trials + 1), 4)}


# ---------- 2. sound similarity ----------
def letter_vec(stream):
    c = Counter(ch for s in stream for ch in s)
    return c


def bigram_vec(stream):
    c = Counter()
    for s in stream:
        for i in range(len(s) - 1):
            c[s[i:i + 2]] += 1
    return c


def cosine(a, b):
    keys = set(a) | set(b)
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in keys)
    na = math.sqrt(sum(v * v for v in a.values()))
    nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


# English letter/bigram baseline from a fixed sample
ENG = ("the quick brown fox jumps over the lazy dog while seven bright angels of heaven descended upon "
       "the mountain and spoke words of power to the prophet who wrote them in a great book of names")


def eng_streams():
    return [up(w) for w in ENG.split() if len(up(w)) >= 2]


# ---------- 3. anti-hiatus ----------
def hiatus_rate(stream):
    vv = tot = 0
    for s in stream:
        for i in range(len(s) - 1):
            tot += 1
            if s[i] in VOW and s[i + 1] in VOW:
                vv += 1
    return round(100 * vv / max(1, tot), 1)


def run():
    rng = random.Random(150)
    gen_rows, gen_cols, real_rows = soyga_streams()
    soyga_all = gen_rows + gen_cols
    tower_names, tower_grids = tower_data()
    loag = loag_names()

    # 1. do Loag / Tower names live in Soyga?
    sub = [
        substring_test(loag, soyga_all, rng, "Loag names in Soyga (gen)"),
        substring_test(sorted(tower_names), soyga_all, rng, "Tower names in Soyga (gen)"),
        substring_test(loag, real_rows, rng, "Loag names in Soyga (real transcribed)"),
    ]
    # reverse: Soyga rows (>=4) as 'words' inside Loag letter stream and Tower grids
    soyga_words = sorted({s for s in real_rows if 4 <= len(s) <= 12})
    sub.append(substring_test(soyga_words, [ "".join(loag) ], rng, "Soyga rows in Loag stream"))
    sub.append(substring_test(soyga_words, tower_grids, rng, "Soyga rows in Tower grids"))

    # 2. sound similarity (letter + bigram), Soyga vs Loag vs Towers vs English
    L_let = letter_vec(loag); T_let = letter_vec(tower_grids); S_let = letter_vec(soyga_all); E_let = letter_vec(eng_streams())
    L_big = bigram_vec(loag); T_big = bigram_vec(tower_grids); S_big = bigram_vec(soyga_all); E_big = bigram_vec(eng_streams())
    sound = {
        "letter_cos": {
            "Soyga-Loag": round(cosine(S_let, L_let), 3), "Soyga-Towers": round(cosine(S_let, T_let), 3),
            "Soyga-English": round(cosine(S_let, E_let), 3), "Loag-Towers": round(cosine(L_let, T_let), 3),
        },
        "bigram_cos": {
            "Soyga-Loag": round(cosine(S_big, L_big), 3), "Soyga-Towers": round(cosine(S_big, T_big), 3),
            "Soyga-English": round(cosine(S_big, E_big), 3), "Loag-Towers": round(cosine(L_big, T_big), 3),
        },
    }

    # 3. anti-hiatus
    hiat = {"Soyga": hiatus_rate(soyga_all), "Loag_names": hiatus_rate(loag),
            "Tower_grids": hiatus_rate(tower_grids), "English": hiatus_rate(eng_streams())}

    res = {
        "soyga_tables_generated": len(a36.WORDS), "soyga_rows_real": len(real_rows),
        "loag_names": len(loag), "tower_names": len(tower_names),
        "substring_tests": sub,
        "sound_similarity": sound,
        "anti_hiatus_vowel_vowel_pct": hiat,
        "prior": "a61: Loagaeth is NOT generated by the Soyga neighbour rule. a36: 8 Soyga tables share Sloane 3189.",
    }
    load.save_result("150_soyga_bridges", res)
    return res


if __name__ == "__main__":
    r = run()
    print("SOYGA BRIDGE TESTS\n")
    print("1) Names living inside the other book (substring vs shuffle null):")
    for s in r["substring_tests"]:
        print("   %-42s hits %d vs null %.1f  z=%s p=%s" % (s["corpus"], s["hits_real"], s["hits_null_mean"], s["z"], s["p"]))
    print("\n2) Sound similarity (1.0 = identical profile):")
    print("   letter:", r["sound_similarity"]["letter_cos"])
    print("   bigram:", r["sound_similarity"]["bigram_cos"])
    print("\n3) Anti-hiatus (vowel-vowel %, low = strict CV like Loag):")
    print("  ", r["anti_hiatus_vowel_vowel_pct"])
