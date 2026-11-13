"""
151 - The Watchtowers' OWN grammar, attacked standalone (not via the Loagaeth), and bridged to the
Enochian Calls and the governor/king name-system.

We did this for the Loagaeth (root-and-pattern, anti-hiatus, affixes, compounding, matrix). Now the
same battery on the Watchtower name-system, with its own classes:
  HOLY   - the 3 Holy Names per tablet (Linea Spiritus Sancti): ORO IBAH AOZPI ...  (12 words)
  ANGEL  - the angel/god names read off the Great Table squares (quadrados)
  GOV    - the 91 Governors of the Aethyrs (read off the tablets letter by letter)
  KING   - the 12 tribe Kings
  CALL   - the vocabulary of the 19 Enochian Calls (spoken keys), for the bridge test

Questions:
  1. Phonotactics: do Tower names avoid vowel-vowel (like the Loagaeth) or not?
  2. Root-and-pattern: do Tower names share consonant skeletons above a vowel-shuffle null?
  3. Affixes: are there recurring prefixes/suffixes (an onomastic morphology of its own)?
  4. Internal bridges: the Governors are READ FROM the tablets - do their skeletons match the ANGEL
     names (positive control)? Are HOLY/ANGEL/GOV one language or several?
  5. Call bridge: do Call words share skeletons with the Tower names, or live inside the Great Table?
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


def skeleton(w):
    return "".join(ch for ch in w if ch not in VOW)


# ---------- corpora ----------
def corpora():
    g = json.load(open(load.ROOT + "/engine/data/governadores.json", encoding="utf-8"))
    q = json.load(open(load.ROOT + "/engine/data/quadrados.json", encoding="utf-8"))
    c = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))

    gov = [up(x["nome"]) for x in g["governadores"] if x.get("nome") and up(x["nome"])]
    king = [up(x["nome"]) for x in g["reis_angelicos_12_tribos"]["reis"] if x.get("nome")]
    holy = []
    for k, t in g["torres"].items():
        holy += [up(w) for w in t.get("linea_spiritus_sancti", "").split() if up(w)]
    angel = set()
    grid_lines = []
    for quad in ("ar", "agua", "terra", "fogo"):
        rows = {}
        for cell in q.get(quad, []):
            # only tablet-derived Enochian angel names, NOT the Golden Dawn god-names (Egyptian/Greek)
            for nm in cell.get("names", []) + [cell.get("angel")]:
                if nm and up(nm) and len(up(nm)) >= 3:
                    angel.add(up(nm))
            if "letter" in cell and "row" in cell and "col" in cell:
                rows.setdefault(cell["row"], {})[cell["col"]] = up(cell["letter"])
        for r in sorted(rows):
            grid_lines.append("".join(rows[r][cc] for cc in sorted(rows[r])))
    call = set()
    for ch in c["chamadas"]:
        for p in ch.get("palavras", []):
            w = up(p.get("enoquiano") or p.get("chave") or "")
            if len(w) >= 2:
                call.add(w)
    return {"HOLY": holy, "ANGEL": sorted(angel), "GOV": gov, "KING": king,
            "CALL": sorted(call), "_grid": grid_lines}


# ---------- 1. phonotactics ----------
def hiatus(names):
    vv = tot = 0
    for w in names:
        for i in range(len(w) - 1):
            tot += 1
            if w[i] in VOW and w[i + 1] in VOW:
                vv += 1
    return round(100 * vv / max(1, tot), 1)


def meanlen(names):
    return round(statistics.mean(len(w) for w in names), 1) if names else 0


# ---------- 2. root-and-pattern ----------
def rootpat(names):
    """fraction of names whose consonant skeleton is shared by >=2 names."""
    sk = Counter(skeleton(w) for w in names if skeleton(w))
    shared = sum(1 for w in names if sk[skeleton(w)] >= 2 and skeleton(w))
    return shared / max(1, len(names))


def rootpat_null(names, rng, trials=200):
    nul = []
    cons = [c for w in names for c in w if c not in VOW]
    vows = [c for w in names for c in w if c in VOW]
    for _ in range(trials):
        rng.shuffle(cons)
        rng.shuffle(vows)
        ci = vi = 0
        fake = []
        for w in names:
            nc = sum(1 for c in w if c not in VOW)
            nv = len(w) - nc
            sk = cons[ci:ci + nc]; ci += nc
            vw = vows[vi:vi + nv]; vi += nv
            # re-interleave in original C/V pattern
            out = []
            si = wi = 0
            for ch in w:
                if ch in VOW:
                    out.append(vw[wi] if wi < len(vw) else ch); wi += 1
                else:
                    out.append(sk[si] if si < len(sk) else ch); si += 1
            fake.append("".join(out))
        nul.append(rootpat(fake))
    return statistics.mean(nul), statistics.pstdev(nul) or 1e-9


# ---------- 3. affixes ----------
def affixes(names, n=2):
    pre = Counter(w[:n] for w in names if len(w) > n)
    suf = Counter(w[-n:] for w in names if len(w) > n)
    return pre.most_common(6), suf.most_common(6)


# ---------- 4/5. skeleton overlap between two sets ----------
def skel_overlap(a, b):
    sa = {skeleton(w) for w in a if len(skeleton(w)) >= 2}
    sb = {skeleton(w) for w in b if len(skeleton(w)) >= 2}
    inter = sa & sb
    return {"shared_skeletons": len(inter), "of_a": len(sa), "of_b": len(sb),
            "jaccard": round(len(inter) / max(1, len(sa | sb)), 3), "examples": sorted(inter)[:10]}


def substring_in_grid(words, grid, rng, trials=200):
    def hits(ws):
        return sum(1 for w in ws if len(w) >= 4 and any(w in line for line in grid))
    real = hits([w for w in words if len(w) >= 4])
    long = [w for w in words if len(w) >= 4]
    nul = []
    for _ in range(trials):
        fake = []
        for w in long:
            cs = list(w); rng.shuffle(cs); fake.append("".join(cs))
        nul.append(hits(fake))
    m = statistics.mean(nul); sd = statistics.pstdev(nul) or 1e-9
    return {"words_tested": len(long), "hits_real": real, "hits_null": round(m, 2),
            "z": round((real - m) / sd, 2), "p": round((sum(1 for x in nul if x >= real) + 1) / (trials + 1), 4)}


def run():
    rng = random.Random(151)
    C = corpora()
    classes = ["HOLY", "ANGEL", "GOV", "KING"]

    phon = {}
    for k in classes:
        names = C[k]
        m, sd = rootpat_null(names, rng)
        rp = rootpat(names)
        phon[k] = {"n": len(names), "mean_len": meanlen(names), "anti_hiatus_vv_pct": hiatus(names),
                   "root_pattern_pct": round(100 * rp, 1), "root_pattern_null_pct": round(100 * m, 1),
                   "z": round((rp - m) / sd, 1)}
    # all tower names pooled
    pool = C["HOLY"] + C["ANGEL"] + C["GOV"] + C["KING"]
    m, sd = rootpat_null(pool, rng)
    rp = rootpat(pool)
    phon["ALL_TOWER"] = {"n": len(pool), "mean_len": meanlen(pool), "anti_hiatus_vv_pct": hiatus(pool),
                         "root_pattern_pct": round(100 * rp, 1), "root_pattern_null_pct": round(100 * m, 1),
                         "z": round((rp - m) / sd, 1)}
    # reference numbers (loagaeth, from parentesco)
    phon["LOAG_ref"] = {"anti_hiatus_vv_pct": 1.0, "root_pattern_pct_ref": "~40 (a134)"}

    aff = {k: {"prefixes": affixes(C[k])[0], "suffixes": affixes(C[k])[1]} for k in classes}

    # internal bridges
    bridges = {
        "GOV_vs_ANGEL": skel_overlap(C["GOV"], C["ANGEL"]),   # governors read from tablet -> should match
        "HOLY_vs_ANGEL": skel_overlap(C["HOLY"], C["ANGEL"]),
        "KING_vs_ANGEL": skel_overlap(C["KING"], C["ANGEL"]),
        "GOV_vs_HOLY": skel_overlap(C["GOV"], C["HOLY"]),
    }
    # call bridge
    call_bridge = {
        "CALL_vs_TOWER_skeletons": skel_overlap(C["CALL"], pool),
        "CALL_words_in_Great_Table": substring_in_grid(C["CALL"], C["_grid"], rng),
        "GOV_names_in_Great_Table(control)": substring_in_grid(C["GOV"], C["_grid"], rng),
    }

    res = {"counts": {k: len(C[k]) for k in classes + ["CALL"]},
           "grammar_by_class": phon, "affixes": aff,
           "internal_bridges_skeleton_overlap": bridges,
           "call_bridge": call_bridge}
    load.save_result("151_tower_grammar", res)
    return res


if __name__ == "__main__":
    r = run()
    print("THE WATCHTOWER GRAMMAR\n")
    print("counts:", r["counts"], "\n")
    print("%-11s %4s %5s %8s %10s %7s" % ("class", "n", "len", "hiatus%", "rootpat%", "z"))
    for k, v in r["grammar_by_class"].items():
        if "n" in v:
            print("%-11s %4d %5.1f %8.1f %10.1f %7s" % (k, v["n"], v["mean_len"], v["anti_hiatus_vv_pct"], v["root_pattern_pct"], v["z"]))
    print("\nInternal bridges (skeleton overlap, jaccard):")
    for k, v in r["internal_bridges_skeleton_overlap"].items():
        print("  %-16s shared %d jaccard %s  ex %s" % (k, v["shared_skeletons"], v["jaccard"], v["examples"][:5]))
    print("\nCall bridge:")
    cb = r["call_bridge"]
    print("  CALL vs TOWER skeletons: shared %d jaccard %s" % (cb["CALL_vs_TOWER_skeletons"]["shared_skeletons"], cb["CALL_vs_TOWER_skeletons"]["jaccard"]))
    print("  CALL words in Great Table: hits %d vs null %s z=%s" % (cb["CALL_words_in_Great_Table"]["hits_real"], cb["CALL_words_in_Great_Table"]["hits_null"], cb["CALL_words_in_Great_Table"]["z"]))
    print("  GOV names in Great Table (control): hits %d vs null %s z=%s" % (cb["GOV_names_in_Great_Table(control)"]["hits_real"], cb["GOV_names_in_Great_Table(control)"]["hits_null"], cb["GOV_names_in_Great_Table(control)"]["z"]))
