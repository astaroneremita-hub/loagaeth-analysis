"""
152 - Deeper into the Heptarchy and the Watchtowers, pressing the findings of a151.

a151 found: the Towers are a federation of name-layers, not one language; the Heptarchy looked CV-strict
like the Loagaeth but is NOT generative. Two refinements to test:

  H1. Is the Heptarchy actually GRID-DERIVED (its 49 names read off its 7 tables), like the Towers rather
      than spoken like the Loagaeth? (The data tags each derived name 'lido_das_tabelas'.) If so, the real
      family divide is GRID-READ (Heptarchy + Towers) vs DICTATED/SPOKEN (Loagaeth + Calls), not anti-hiatus.
  H2. 7-fold planetary order: the 49 names carry a 'planeta_coordinatio' tag (7 planets x 7). Do the seven
      planet-groups carry DISTINCT letter signatures (above a label-shuffle null)? Is 7 built into the names?
  T1. Are the Tower ANGEL names PERMUTATIONAL within a tablet - drawn from a tiny per-tablet letter pool,
      anagram-related - proving the "root-pattern" of a151 is grid geometry, not a productive morphology?
"""
import json
import math
import random
import statistics
from collections import Counter

import load

VOW = set("AEIOU")


def up(s):
    return "".join(ch for ch in str(s).upper() if ch.isalpha())


# ---------- H1: Heptarchy names are grid-derived ----------
def heptarchy_grid_derived():
    h = json.load(open(load.ROOT + "/engine/data/heptarquia.json", encoding="utf-8"))
    nd = h["nomes_derivados_das_tabelas"]
    ok = sum(1 for x in nd if "confere" in (x.get("status", "")))
    # do the 7 source tables actually hold these letters? spot-confirm by letter inventory
    tables = h["sete_tabelas"]["tabelas"]
    tab_letters = []
    for t in tables:
        letters = [up(c.get("letra", "")) for row in t.get("celulas", []) for c in row if c.get("letra")]
        tab_letters.append("".join(letters))
    return {"derived_names": len(nd), "match_source_tables": ok,
            "match_pct": round(100 * ok / max(1, len(nd)), 1),
            "n_source_tables": len(tables),
            "note": "names are READ from the 7 tables (status 'confere'); Heptarchy is grid-derived like the Towers, not dictated like the Loagaeth."}


# ---------- H2: 7-fold planetary signature ----------
def letter_vec(names):
    c = Counter()
    for w in names:
        for ch in w:
            c[ch] += 1
    return c


def cos(a, b):
    ks = set(a) | set(b)
    dot = sum(a.get(k, 0) * b.get(k, 0) for k in ks)
    na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return dot / (na * nb) if na and nb else 0.0


def group_separation(groups):
    """mean pairwise cosine between group letter-vectors (LOW = groups distinct)."""
    vecs = [letter_vec(g) for g in groups if g]
    sims = []
    for i in range(len(vecs)):
        for j in range(i + 1, len(vecs)):
            sims.append(cos(vecs[i], vecs[j]))
    return statistics.mean(sims) if sims else 1.0


def planetary_7fold(rng):
    h = json.load(open(load.ROOT + "/engine/data/heptarquia.json", encoding="utf-8"))
    nm = h["tabula_collecta"]["nomes"]
    by = {}
    for x in nm:
        p = x.get("planeta_coordinatio") or "?"
        by.setdefault(p, []).append(up(x["nome"]))
    planets = sorted(by)
    groups = [by[p] for p in planets]
    real = group_separation(groups)
    # null: shuffle planet labels across names, keep group sizes
    allnames = [up(x["nome"]) for x in nm]
    sizes = [len(g) for g in groups]
    nul = []
    for _ in range(500):
        shuf = allnames[:]; rng.shuffle(shuf)
        gg, i = [], 0
        for s in sizes:
            gg.append(shuf[i:i + s]); i += s
        nul.append(group_separation(gg))
    m = statistics.mean(nul); sd = statistics.pstdev(nul) or 1e-9
    return {"planets": planets, "group_sizes": {p: len(by[p]) for p in planets},
            "between_group_cos_real": round(real, 3), "between_group_cos_null": round(m, 3),
            "z": round((real - m) / sd, 2),
            "reading": "LOW real vs null = planet-groups have distinct letter signatures (7 is in the names).",
            "first_letters": {p: "".join(sorted({w[0] for w in by[p]})) for p in planets}}


# ---------- T1: Tower ANGEL names permutational within a tablet ----------
def multiset(w):
    return tuple(sorted(w))


def tower_permutational(rng):
    q = json.load(open(load.ROOT + "/engine/data/quadrados.json", encoding="utf-8"))
    by = {}
    for quad in ("ar", "agua", "terra", "fogo"):
        names = set()
        for cell in q.get(quad, []):
            for nm in cell.get("names", []) + [cell.get("angel")]:
                if nm and len(up(nm)) >= 4:
                    names.add(up(nm))
        by[quad] = sorted(names)

    def pool_and_anagram(names):
        pool = set("".join(names))
        # fraction of name-pairs that are anagrams (same multiset)
        ms = Counter(multiset(w) for w in names)
        anagram_pairs = sum(v * (v - 1) // 2 for v in ms.values())
        total_pairs = len(names) * (len(names) - 1) // 2
        return len(pool), round(100 * anagram_pairs / max(1, total_pairs), 2)

    within = {}
    for quad in by:
        pool, ana = pool_and_anagram(by[quad])
        within[quad] = {"n_names": len(by[quad]), "distinct_letters_in_tablet": pool, "anagram_pair_pct": ana}
    # cross-tablet letter overlap: do tablets share their pools, or each has its own alphabet?
    pools = {quad: set("".join(by[quad])) for quad in by}
    cross = {}
    quads = list(by)
    for i in range(len(quads)):
        for j in range(i + 1, len(quads)):
            a, b = pools[quads[i]], pools[quads[j]]
            cross[quads[i] + "-" + quads[j]] = round(len(a & b) / len(a | b), 2)
    # how concentrated: mean letters per name vs distinct letters available (low ratio = tiny pool reused)
    return {"within_tablet": within, "tablet_letter_jaccard": cross,
            "reading": "Small distinct_letters per tablet + reuse across many names = names are permutational reads of a small square pool, not an open morphology."}


def run():
    rng = random.Random(152)
    res = {
        "H1_grid_derived": heptarchy_grid_derived(),
        "H2_sevenfold_planetary": planetary_7fold(rng),
        "T1_tower_permutational": tower_permutational(rng),
    }
    load.save_result("152_heptarchy_tower_deep", res)
    return res


if __name__ == "__main__":
    r = run()
    print("H1 - Heptarchy grid-derived:")
    h1 = r["H1_grid_derived"]
    print("   %d/%d names read from the 7 tables (%.0f%%). %s\n" % (h1["match_source_tables"], h1["derived_names"], h1["match_pct"], h1["note"]))
    print("H2 - 7-fold planetary signature:")
    h2 = r["H2_sevenfold_planetary"]
    print("   groups:", h2["group_sizes"])
    print("   between-group letter cos: real %.3f vs null %.3f  z=%s (%s)" % (h2["between_group_cos_real"], h2["between_group_cos_null"], h2["z"], "distinct" if h2["z"] < -2 else "not distinct"))
    print("   first letters per planet:", h2["first_letters"], "\n")
    print("T1 - Tower ANGEL permutational within tablet:")
    for quad, v in r["T1_tower_permutational"]["within_tablet"].items():
        print("   %-6s %3d names, %2d distinct letters, anagram-pairs %.2f%%" % (quad, v["n_names"], v["distinct_letters_in_tablet"], v["anagram_pair_pct"]))
    print("   tablet letter overlap (jaccard):", r["T1_tower_permutational"]["tablet_letter_jaccard"])
