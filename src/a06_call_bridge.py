"""
06 - Bridge between the Loagaeth and the 48 Calls (Keys).

Takes the word tokens from the two word-spaced leaves (1a, 1b) and counts how many
are EXACT matches (whole token) to attested Angelical word-forms from the Calls.
Compared against a null: random letter strings drawn with the same length
distribution. A handful of these matches carry known glosses (IAD, GAH, ZIR, ...),
which is the starting point for an external anchor.

This is a weak-but-real signal (small absolute count, ~10x over chance), not a
decode key.
"""
import random
import statistics
from collections import Counter

import load

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
N_NULL = 20
SEED = 1234


def run():
    lex = load.lexicon()
    forms = set(lex["attested_wordforms"])
    known = lex["known_glosses"]

    words = load.spaced_words()
    wc = Counter(words)
    matches = sorted(w for w in wc if w in forms)
    matched_known = {w: known[w] for w in matches if w in known}

    rng = random.Random(SEED)
    lengths = [len(w) for w in words]
    null_counts = []
    for _ in range(N_NULL):
        rset = set("".join(rng.choice(ALPHABET) for _ in range(L)) for L in lengths)
        null_counts.append(sum(1 for w in rset if w in forms))

    res = {
        "n_spaced_word_types": len(wc),
        "exact_lexicon_matches": len(matches),
        "match_rate_pct": round(100 * len(matches) / len(wc), 2),
        "examples": matches[:20],
        "matches_with_known_gloss": matched_known,
        "null_mean": round(statistics.mean(null_counts), 2),
        "null_sd": round(statistics.pstdev(null_counts), 2),
        "verdict": "above chance" if len(matches) > statistics.mean(null_counts) * 1.3
                   else "chance level",
    }
    load.save_result("06_call_bridge", res)
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=1))
