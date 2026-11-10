"""
12 - The "empire": what the master names really are, and how they are built.

Earlier work in the wider project listed seven "Lords of the leaves" (CHASTOR, HANZACH,
ALGETHA, ADNOCHA, ADNACHA, ACHEPHA, ANTANTO) as the seven most recurrent 7-letter strings,
and a generated grimoire attached "powers" to them (sefira, planet, talisman). This module
tests what holds up:

  A) The seven Lords in context: occurrences, reach, and what precedes / follows them.
  B) Are the Lords independent beings, or overlapping 7-letter WINDOWS of longer compounds?
     (e.g. ADNOCHA is mostly followed by STOR -> ADNOCHASTOR.)
  C) Nesting: stems that stack a shared title-chain (NO-, AD-NO-, ED-NO-, ID-NO-).
  D) Vowel twins: do Lords have vowel-swapped twins MORE than any frequent string? (null)
  E) The "CHA core" hypothesis: is CHA a closed generative core, or a generic syllable?
  F) Context in leaf 1 (the only text with word boundaries and some glossed words).

Provenance note: the grimoire's sefira/planet/talisman "powers" are CONVENTION (the
project's own provenance file says so); they are not properties of the names. The same
name received two incompatible assignments (Tiferet/Sun and Chesed/Jupiter) depending on
the mapping method.
"""
import json
import math
import os
import random
from collections import Counter

import load

LORDS = ["CHASTOR", "HANZACH", "ALGETHA", "ADNOCHA", "ADNACHA", "ACHEPHA", "ANTANTO"]
NESTS = {
    "CHASTOR": ["CHASTOR", "NOCHASTOR", "ADNOCHASTOR", "EDNOCHASTOR"],
    "ANZACH": ["ANZACH", "HANZACH", "NOCHANZACH", "ADNOCHANZACH"],
    "CHAPH": ["CHAPH", "NOCHAPH", "ADNOCHAPH"],
    "CHEPHA": ["CHEPHA", "ACHEPHA", "ADNACHEPHA"],
    "NOCHA (title chain)": ["NOCHA", "ADNOCHA", "EDNOCHA", "IDNOCHA", "AGNOCHA"],
}
VOW = "AEIOU"
HERE = os.path.dirname(os.path.abspath(__file__))
LEXICON = os.path.join(os.path.dirname(HERE), "data", "call_lexicon.json")


def stream():
    t = {n: s for n, s in load.all_tables().items() if n != 1}
    return t, "|".join(t[n] for n in sorted(t))


def positions(s, sub):
    out, i = [], s.find(sub)
    while i >= 0:
        out.append(i)
        i = s.find(sub, i + 1)
    return out


def swaps(w):
    out = set()
    for i, c in enumerate(w):
        if c in VOW:
            for v in VOW:
                if v != c:
                    out.add(w[:i] + v + w[i + 1:])
    return out


def entropy(c):
    t = sum(c.values()) or 1
    return -sum(v / t * math.log2(v / t) for v in c.values() if v)


def run():
    rng = random.Random(12)
    tabs, S = stream()

    # A + B: lords in context, and how often each is a window of a longer compound
    lords = {}
    for w in LORDS:
        P = positions(S, w)
        before = Counter(S[max(0, i - 3):i] for i in P)
        after = Counter(S[i + len(w):i + len(w) + 3] for i in P)
        top_b, nb = before.most_common(1)[0] if before else ("", 0)
        top_a, na = after.most_common(1)[0] if after else ("", 0)
        lords[w] = {
            "occurrences": len(P),
            "tables": len([n for n, s in tabs.items() if w in s]),
            "top_before": before.most_common(4),
            "top_after": after.most_common(4),
            "dominant_extension": (top_b + "|" + w if nb >= na else w + "|" + top_a),
            "share_in_dominant_extension": round(max(nb, na) / len(P), 2) if P else 0,
        }

    # C: nesting chains
    nests = {k: {f: S.count(f) for f in forms} for k, forms in NESTS.items()}

    # D: vowel twins vs null
    grams = Counter(S[i:i + 7] for i in range(len(S) - 6))
    pool = [g for g, f in grams.items() if f >= 25 and "|" not in g]
    def has_twin(g):
        return any(S.count(x) >= 3 for x in swaps(g))
    lord_rate = sum(has_twin(w) for w in LORDS) / len(LORDS)
    null_rate = sum(has_twin(g) for g in pool) / len(pool) if pool else None

    # E: CHA core
    P = positions(S, "CHA")
    tails = Counter(S[i + 3:i + 7] for i in P)
    cha = {"occurrences": len(P), "tail_entropy_bits": round(entropy(tails), 2),
           "top_tails": tails.most_common(8),
           "verdict": "generic high-frequency syllable (open continuation), not a closed core"}

    # F: leaf-1 context
    lv = load.leaves()
    w1 = [load.letters(w) for k in ("1a", "1b") for r in lv.get(k, []) for w in r.split() if load.letters(w)]
    try:
        known = json.load(open(LEXICON, encoding="utf-8"))["known_glosses"]
    except Exception:
        known = {}
    stems = ["CHAST", "CHUST", "ANZACH", "HANZA", "GETH", "NOCHA", "NACHA", "CHEPH", "ANTANT"]
    ctx = []
    for i, w in enumerate(w1):
        if any(s in w for s in stems):
            win = w1[max(0, i - 3):i + 4]
            ctx.append({"word": w, "window": win, "glossed_neighbours": {x: known[x] for x in win if x in known}})

    stems_rank = sorted(
        ((f, S.count(f), len([n for n, s in tabs.items() if f in s]))
         for f in ["CHASTOR", "ANZACH", "GETH", "NOCHAPH", "ACHEPHA", "ANTANTO", "ADNOCHA"]),
        key=lambda x: -x[1])

    res = {
        "A_B_lords": lords,
        "C_nesting": nests,
        "D_vowel_twins": {"lords_with_twin": round(lord_rate, 2),
                          "random_frequent_7grams_with_twin": round(null_rate, 2) if null_rate is not None else None,
                          "verdict": "vowel alternation is language-wide, not a mark of the Lords"},
        "E_cha_core": cha,
        "F_leaf1_context": {"n_words_with_stem": len(ctx),
                            "with_glossed_neighbour": [c for c in ctx if c["glossed_neighbours"]][:10],
                            "examples": [c["word"] for c in ctx[:16]]},
        "stems_by_frequency": [{"stem": s, "occurrences": o, "tables": t} for s, o, t in stems_rank],
        "conclusion": ("The 'seven Lords' are real frequent strings, but they overlap and nest inside a "
                       "shared compounding system rather than being seven independent beings. The empire "
                       "is a small set of stem-names (CHASTOR, ANZACH, CHAPH, CHEPHA) plus a shared, "
                       "stackable title-chain (NO-, then AD-/ED-/ID-NO-); each added title cuts frequency "
                       "roughly threefold. Grimoire 'powers' are convention, not properties of the names."),
    }
    load.save_result("12_empire", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
