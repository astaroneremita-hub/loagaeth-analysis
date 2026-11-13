"""
155 - INDEPENDENT AUDIT of the Forja (clean-room reimplementation, user protocol #325).

Written from the FORMAL SPECIFICATION below, NOT by reusing the Forja's generation code. The only
shared input is the frozen data (the 90 names). All decomposition, splitting, grammar, controls and
statistics are reimplemented here from scratch.

FORMAL SPECIFICATION of the Loagaeth onomastic grammar being tested
-------------------------------------------------------------------
  Alphabet: Latin letters. Vowels V = {A,E,I,O,U}. Consonants = everything else.
  Decompose a name w into:
    skeleton(w) = subsequence of consonants of w, in order (the root / identity).
    melody(w)   = subsequence of vowels of w, in order (the vowel pattern / inflection).
  A grammar G = (S, M) is a set S of skeletons and a set M of melodies.
  G REPRODUCES a name w  iff  skeleton(w) in S AND melody(w) in M
    (i.e. w is a recombination of a known root with a known melody).

HYPOTHESIS: a grammar learned from a sample of the names reproduces held-out names far above
phonotactically-matched controls.

PROTOCOL
  - 40 train/test splits (seeds 0..39): shuffle the 90 names, 45 train / 45 test.
  - Grammar frozen from TRAIN only.
  - Score reproduction on the held-out TEST, and on three control sets of the same size/lengths:
      C1 uniform-random letters
      C2 letter-frequency matched (sampled from the 90-name letter distribution)
      C3 Markov order-2 (phonotactically matched; char model trained on the TRAIN names)
  - Per split: counts. Across splits: mean, bootstrap 95% CI, paired significance (sign test) real vs C3.
  - Also classify each test name: 'recombination' (both components in train) vs 'needs-new-component'
    (skeleton or melody absent from train) -> the current test measures RECOMBINATION only.
"""
import hashlib
import json
import random
import statistics

import load

V = set("AEIOU")


def skeleton(w):
    return "".join(c for c in w if c not in V)


def melody(w):
    return "".join(c for c in w if c in V)


def load_names():
    fg = json.load(open(load.ROOT + "/viz/forge_grammar.json", encoding="utf-8"))
    return [w.upper() for w in fg["real_names"] if w]


def h(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


# ---- controls (clean-room generators) ----
def c_uniform(lengths, alphabet, rng):
    return ["".join(rng.choice(alphabet) for _ in range(L)) for L in lengths]


def c_freqmatched(lengths, pool, rng):
    return ["".join(rng.choice(pool) for _ in range(L)) for L in lengths]


def markov2_train(words):
    """order-2 char model with start/end; returns transition table."""
    nxt = {}
    for w in words:
        s = "^^" + w + "$"
        for i in range(2, len(s)):
            nxt.setdefault(s[i - 2:i], []).append(s[i])
    return nxt


def markov2_gen(nxt, L, rng, tries=4000):
    # reject-sampling: return a name of EXACTLY length L generated naturally (no padding).
    # falls back to None if the chain cannot produce that length (then the caller skips it).
    for _ in range(tries):
        ctx = "^^"; out = ""
        ok = True
        while True:
            opts = nxt.get(ctx)
            if not opts:
                ok = False; break
            ch = rng.choice(opts)
            if ch == "$":
                break
            out += ch; ctx = ctx[-1] + ch
            if len(out) > L:
                ok = False; break
        if ok and len(out) == L:
            return out
    return None


def reproduces(names, S, M):
    return sum(1 for w in names if skeleton(w) in S and melody(w) in M)


def run():
    names = load_names()
    rng0 = random.Random(0)
    alphabet = sorted({c for w in names for c in w})
    pool = [c for w in names for c in w]

    frozen = {"n_names": len(names), "names_hash": h(sorted(names)),
              "alphabet": "".join(alphabet), "decomposition": "skeleton=consonants, melody=vowels (in order)",
              "reproduce_rule": "skeleton in S and melody in M"}

    SPLITS = 40
    rows = []           # per split
    recomb_frac = []    # fraction of test names that are recombination-reproducible
    newcomp_frac = []
    for seed in range(SPLITS):
        rng = random.Random(seed)
        idx = list(range(len(names))); rng.shuffle(idx)
        tr = [names[i] for i in idx[:45]]; te = [names[i] for i in idx[45:]]
        S = set(skeleton(w) for w in tr); M = set(melody(w) for w in tr)
        lengths = [len(w) for w in te]

        real = reproduces(te, S, M)
        # controls, averaged over 100 draws each per split
        cr = random.Random(1000 + seed)
        nxt = markov2_train(tr)
        c1 = statistics.mean(reproduces(c_uniform(lengths, alphabet, cr), S, M) for _ in range(100))
        c2 = statistics.mean(reproduces(c_freqmatched(lengths, pool, cr), S, M) for _ in range(100))
        def markov_set():
            got = [markov2_gen(nxt, L, cr) for L in lengths]
            return [x for x in got if x]
        c3_runs = []
        for _ in range(100):
            ms = markov_set()
            if ms:
                c3_runs.append(reproduces(ms, S, M) * len(lengths) / len(ms))  # scale to test size
        c3 = statistics.mean(c3_runs) if c3_runs else 0

        # generalization classes
        recomb = sum(1 for w in te if skeleton(w) in S and melody(w) in M)
        newc = len(te) - sum(1 for w in te if skeleton(w) in S and melody(w) in M)
        recomb_frac.append(recomb / len(te)); newcomp_frac.append(newc / len(te))

        rows.append({"seed": seed, "test_n": len(te), "real": real,
                     "c1_uniform": round(c1, 2), "c2_freq": round(c2, 2), "c3_markov": round(c3, 2)})

    reals = [r["real"] for r in rows]
    c3s = [r["c3_markov"] for r in rows]
    n = rows[0]["test_n"]

    # bootstrap 95% CI of the mean real rate across splits
    rb = random.Random(7)
    boot = []
    for _ in range(5000):
        samp = [reals[rb.randrange(len(reals))] for _ in reals]
        boot.append(statistics.mean(samp) / n)
    boot.sort()
    ci = (round(boot[int(0.025 * len(boot))], 3), round(boot[int(0.975 * len(boot))], 3))

    # paired sign test real > c3 per split
    wins = sum(1 for r, c in zip(reals, c3s) if r > c)
    ties = sum(1 for r, c in zip(reals, c3s) if r == c)
    # one-sided sign-test p (ignore ties), binomial
    import math
    m = SPLITS - ties
    k = wins
    p_sign = sum(math.comb(m, j) for j in range(k, m + 1)) / (2 ** m) if m else 1.0

    res = {
        "frozen_spec": frozen,
        "splits": SPLITS, "test_size": n,
        "real_mean": round(statistics.mean(reals), 2), "real_mean_pct": round(100 * statistics.mean(reals) / n, 1),
        "real_ci95_pct": [round(100 * ci[0], 1), round(100 * ci[1], 1)],
        "control_uniform_pct": round(100 * statistics.mean(r["c1_uniform"] for r in rows) / n, 2),
        "control_freqmatched_pct": round(100 * statistics.mean(r["c2_freq"] for r in rows) / n, 2),
        "control_markov2_pct": round(100 * statistics.mean(c3s) / n, 2),
        "sign_test_real_gt_markov": {"wins": wins, "ties": ties, "of": SPLITS, "p_one_sided": round(p_sign, 6)},
        "recombination_rate_pct": round(100 * statistics.mean(recomb_frac), 1),
        "needs_new_component_pct": round(100 * statistics.mean(newcomp_frac), 1),
        "per_split": rows,
        "interpretation": (
            "The frozen grammar reproduces held-out names at the real rate; the three controls bound chance "
            "at matched length, letter-frequency and (C3) full bigram phonotactics. A significant gap real>C3 "
            "means the reuse of components is specific to the Loagaeth lexicon, not generic pronounceability. "
            "The measured ability is RECOMBINATION of known components; discovering wholly new components is "
            "NOT demonstrated by this test."),
    }
    load.save_result("155_forja_audit", res)
    return res


if __name__ == "__main__":
    r = run()
    print("FORJA — INDEPENDENT AUDIT (clean-room, 40 splits of 45/45)\n")
    print("frozen:", r["frozen_spec"]["names_hash"], "| names", r["frozen_spec"]["n_names"])
    print("real held-out reproduction: %.1f%% (mean %.1f/%d), 95%% CI [%.1f, %.1f]%%" % (
        r["real_mean_pct"], r["real_mean"], r["test_size"], r["real_ci95_pct"][0], r["real_ci95_pct"][1]))
    print("controls:  uniform %.2f%% | freq-matched %.2f%% | Markov-2 (phonotactic) %.2f%%" % (
        r["control_uniform_pct"], r["control_freqmatched_pct"], r["control_markov2_pct"]))
    st = r["sign_test_real_gt_markov"]
    print("real > Markov in %d/%d splits (ties %d), sign-test p=%.2g" % (st["wins"], st["of"], st["ties"], st["p_one_sided"]))
    print("generalization: recombination %.1f%% | needs-new-component %.1f%%" % (
        r["recombination_rate_pct"], r["needs_new_component_pct"]))
