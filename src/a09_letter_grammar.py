"""
09 - Letter-level grammar: do the letters carry positional roles, and is the grammar
shared with the 48 Calls?

Two findings reproduced here:
  A) Letters have real positional roles (onset / terminator). Measured as the mutual
     information MI(letter; position-class) where position is initial / medial / final,
     tested against a strong null that shuffles letters WITHIN each word (keeps the word
     set and letter composition, destroys only the position-letter link). A large MI
     over null means the alphabet assigns letters to positions on purpose.
  B) The word-ending grammar is SHARED with the Calls. We correlate each letter's
     P(final) profile between the Loagaeth and the Calls, and against English as a
     control. Loagaeth<->Calls far above Loagaeth<->English means the two are the same
     Angelical tongue (different lexicon), not just universal phonotactics.

Data: data/loagaeth_tables.json (leaf-1 spaced words) + engine/data/chamadas.json (Calls).
"""
import json
import math
import os
import random
import statistics
from collections import Counter, defaultdict

import load

VOW = set("AEIOU")
HERE = os.path.dirname(os.path.abspath(__file__))
CALLS = os.path.join(os.path.dirname(HERE), "engine", "data", "chamadas.json")


def leaf1_words():
    lv = load.leaves()
    out = []
    for k in ("1a", "1b"):
        for r in lv.get(k, []):
            for w in r.split():
                w = load.letters(w)
                if len(w) >= 3:
                    out.append(w)
    return out


def call_words():
    try:
        C = json.load(open(CALLS, encoding="utf-8"))["chamadas"]
    except Exception:
        return []
    out = []
    for c in C:
        for p in c.get("palavras", []):
            if isinstance(p, dict):
                w = load.letters(p.get("enoquiano", ""))
                if len(w) >= 3:
                    out.append(w)
    return out


def mi_letter_pos(words):
    joint = Counter()
    pl = Counter()
    pp = Counter()
    N = 0
    for w in words:
        for i, c in enumerate(w):
            p = 0 if i == 0 else (2 if i == len(w) - 1 else 1)
            joint[(c, p)] += 1
            pl[c] += 1
            pp[p] += 1
            N += 1
    mi = 0.0
    for (c, p), n in joint.items():
        pxy = n / N
        mi += pxy * math.log2(pxy / ((pl[c] / N) * (pp[p] / N)))
    return mi


def final_profile(words):
    pos = defaultdict(lambda: [0, 0])
    for w in words:
        for i, c in enumerate(w):
            pos[c][1] += 1
            if i == len(w) - 1:
                pos[c][0] += 1
    return {c: pos[c][0] / pos[c][1] for c in pos if pos[c][1] >= 8}


def pearson(a, b):
    k = sorted(set(a) & set(b))
    xs, ys = [a[c] for c in k], [b[c] for c in k]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = (sum((x - mx) ** 2 for x in xs) * sum((y - my) ** 2 for y in ys)) ** 0.5
    return (num / den if den else 0), n


ENGLISH = ("the of and to in that have it for not on with he as you do at this but his by from they we "
           "say her she or an will my one all would there their what so up out if about who get which go "
           "me when make can like time no just him know take people into year your good some could them "
           "see other than then now look only come over think also back after use two how work first well "
           "way even new want because any give day most man find here thing great little world long old down").split()


def run():
    rng = random.Random(5)
    loa = leaf1_words()
    calls = call_words()

    obs = mi_letter_pos(loa)
    nulls = []
    for _ in range(300):
        shuf = ["".join(rng.sample(w, len(w))) for w in loa]
        nulls.append(mi_letter_pos(shuf))
    mu, sd = statistics.mean(nulls), statistics.pstdev(nulls)

    lp = final_profile(loa)
    cp = final_profile(calls) if calls else {}
    ep = final_profile([load.letters(w) for w in ENGLISH])
    r_lc, n_lc = pearson(lp, cp) if cp else (None, 0)
    r_le, _ = pearson(lp, ep)
    r_ce, _ = pearson(cp, ep) if cp else (None, 0)

    # onset / terminator inventory
    pos = defaultdict(lambda: [0, 0, 0])
    for w in loa:
        for i, c in enumerate(w):
            pos[c][0 if i == 0 else (2 if i == len(w) - 1 else 1)] += 1
    onset = sorted(c for c in pos if sum(pos[c]) >= 20 and pos[c][0] / sum(pos[c]) >= .55)
    term = sorted(c for c in pos if sum(pos[c]) >= 20 and pos[c][2] / sum(pos[c]) >= .55)

    res = {
        "A_positional_grammar": {
            "mi_observed_bits": round(obs, 4),
            "mi_null_mean": round(mu, 4), "mi_null_sd": round(sd, 5),
            "z": round((obs - mu) / sd, 1) if sd else None,
            "verdict": "REAL positional grammar" if obs > mu + 3 * sd else "no beyond-chance role",
            "onset_letters": onset, "terminator_letters": term,
        },
        "B_shared_grammar_with_calls": {
            "r_final_loagaeth_vs_calls": round(r_lc, 2) if r_lc is not None else None,
            "r_final_loagaeth_vs_english": round(r_le, 2),
            "r_final_calls_vs_english": round(r_ce, 2) if r_ce is not None else None,
            "n_letters": n_lc,
            "verdict": ("same Angelical tongue (shared ending-grammar, different lexicon)"
                        if (r_lc or 0) > (r_le or 0) + 0.2 else "inconclusive"),
        },
    }
    load.save_result("09_letter_grammar", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
