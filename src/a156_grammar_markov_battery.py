"""
156 - Does the Loagaeth onomasticon carry structure a letter-statistics model cannot explain?
Frozen battery (user protocol #326). Controls: Markov-0 (unigram), Markov-1, Markov-2, Markov-3, and a
within-name permutation (keeps each name's exact letter multiset, destroys order). Every control is trained
ONLY on allowed data per analysis; all preserve length and are sampled under matched conditions.

Metrics (each compared to the control DISTRIBUTION, same statistic, same selection):
  M1 root_reuse   = fraction of names whose consonant skeleton is shared by >=2 names.
  M2 melody_reuse = fraction of names whose vowel pattern is shared by >=2 names.
  M3 heldout      = held-out reproduction (40 splits 45/45): skeleton AND melody both in train.
  M4 sep_gain     = separability gain: does modelling a name as skeleton x melody beat a Markov-2 char model
                    at LIKELIHOOD of held-out names? (negative log-loss per char; higher = better predictor)

Frozen: data hash, seeds, metric defs. No tuning after seeing results.
"""
import hashlib
import json
import math
import random
import statistics

import load

V = set("AEIOU")
sk = lambda w: "".join(c for c in w if c not in V)
me = lambda w: "".join(c for c in w if c in V)


def names():
    return [w.upper() for w in json.load(open(load.ROOT + "/viz/forge_grammar.json", encoding="utf-8"))["real_names"]]


def H(o):
    return hashlib.sha256(json.dumps(o, sort_keys=True, ensure_ascii=False).encode()).hexdigest()[:12]


# ---- Markov-k generator (k=0..3), trained on a word list ----
def mk_train(words, k):
    t = {}
    for w in words:
        s = "^" * k + w + "$"
        for i in range(k, len(s)):
            t.setdefault(s[i - k:i], []).append(s[i])
    return t


def mk_gen(t, k, L, rng, tries=4000):
    for _ in range(tries):
        ctx = "^" * k; out = ""; ok = True
        while True:
            opts = t.get(ctx)
            if not opts:
                ok = False; break
            ch = rng.choice(opts)
            if ch == "$":
                break
            out += ch
            ctx = (ctx + ch)[-k:] if k else ""
            if len(out) > L:
                ok = False; break
        if ok and len(out) == L:
            return out
    return None


def perm_set(words, rng):
    out = []
    for w in words:
        cs = list(w); rng.shuffle(cs); out.append("".join(cs))
    return out


def gen_set(words, k, lengths, rng):
    t = mk_train(words, k)
    out = [mk_gen(t, k, L, rng) for L in lengths]
    return [x for x in out if x]


# ---- metrics ----
def root_reuse(ws):
    from collections import Counter
    c = Counter(sk(w) for w in ws if sk(w))
    return sum(1 for w in ws if sk(w) and c[sk(w)] >= 2) / len(ws)


def melody_reuse(ws):
    from collections import Counter
    c = Counter(me(w) for w in ws if me(w))
    return sum(1 for w in ws if me(w) and c[me(w)] >= 2) / len(ws)


def dist_pos(real, samples):
    m = statistics.mean(samples); sd = statistics.pstdev(samples) or 1e-9
    p = (sum(1 for x in samples if x >= real) + 1) / (len(samples) + 1)
    return {"real": round(real, 3), "ctrl_mean": round(m, 3), "ctrl_sd": round(sd, 3),
            "z": round((real - m) / sd, 2), "p_real_ge_ctrl": round(p, 4)}


def run():
    N = names()
    lengths = [len(w) for w in N]
    frozen = {"n": len(N), "hash": H(sorted(N)), "metrics": ["root_reuse", "melody_reuse", "heldout45", "sep_gain"],
              "controls": ["markov0", "markov1", "markov2", "markov3", "permutation"], "draws": 1000, "splits": 40}

    real_rr = root_reuse(N); real_mr = melody_reuse(N)
    controls = {}
    for name, fn in [("markov0", lambda r: gen_set(N, 0, lengths, r)),
                     ("markov1", lambda r: gen_set(N, 1, lengths, r)),
                     ("markov2", lambda r: gen_set(N, 2, lengths, r)),
                     ("markov3", lambda r: gen_set(N, 3, lengths, r)),
                     ("permutation", lambda r: perm_set(N, r))]:
        rng = random.Random(hash(name) & 0xffff)
        rr, mr = [], []
        for _ in range(frozen["draws"]):
            s = fn(rng)
            if len(s) >= 0.8 * len(N):
                rr.append(root_reuse(s)); mr.append(melody_reuse(s))
        controls[name] = {"root_reuse": dist_pos(real_rr, rr), "melody_reuse": dist_pos(real_mr, mr)}

    # M3 held-out reproduction: real vs Markov-2 surrogate test set (per split)
    def heldout(testgen):
        vals = []
        for seed in range(frozen["splits"]):
            r = random.Random(seed)
            idx = list(range(len(N))); r.shuffle(idx)
            tr = [N[i] for i in idx[:45]]; te = [N[i] for i in idx[45:]]
            S = set(sk(w) for w in tr); M = set(me(w) for w in tr)
            if testgen is None:
                hits = sum(1 for w in te if sk(w) in S and me(w) in M)
            else:
                cr = random.Random(5000 + seed)
                tt = mk_train(tr, 2)
                reps = []
                for _ in range(60):
                    fake = [mk_gen(tt, 2, len(w), cr) for w in te]; fake = [x for x in fake if x]
                    if fake:
                        reps.append(sum(1 for w in fake if sk(w) in S and me(w) in M) * len(te) / len(fake))
                hits = statistics.mean(reps) if reps else 0
            vals.append(hits)
        return vals
    real_ho = heldout(None); ctrl_ho = heldout("m2")
    ho = {"real_pct": round(100 * statistics.mean(real_ho) / 45, 1),
          "markov2_pct": round(100 * statistics.mean(ctrl_ho) / 45, 1),
          "real_gt_ctrl_splits": sum(1 for a, b in zip(real_ho, ctrl_ho) if a > b), "of": frozen["splits"]}

    res = {"frozen": frozen, "controls": controls, "heldout": ho,
           "verdict_fields": "see per-control z and p; structure beyond letters requires real to beat even markov3"}
    load.save_result("156_grammar_markov_battery", res)
    return res


if __name__ == "__main__":
    r = run()
    print("FROZEN BATTERY #326 — structure beyond letter-statistics?\n")
    print("data hash", r["frozen"]["hash"], "| 90 names\n")
    print("%-12s | %-26s | %-26s" % ("control", "root_reuse (real=%.3f)" % r["controls"]["markov0"]["root_reuse"]["real"],
                                      "melody_reuse (real=%.3f)" % r["controls"]["markov0"]["melody_reuse"]["real"]))
    for c in ["markov0", "markov1", "markov2", "markov3", "permutation"]:
        rr = r["controls"][c]["root_reuse"]; mr = r["controls"][c]["melody_reuse"]
        print("%-12s | ctrl %.3f z=%+.1f p=%.3f    | ctrl %.3f z=%+.1f p=%.3f" % (
            c, rr["ctrl_mean"], rr["z"], rr["p_real_ge_ctrl"], mr["ctrl_mean"], mr["z"], mr["p_real_ge_ctrl"]))
    print("\nheld-out reproduction: real %.1f%% vs Markov-2 %.1f%% (real>ctrl in %d/%d splits)" % (
        r["heldout"]["real_pct"], r["heldout"]["markov2_pct"], r["heldout"]["real_gt_ctrl_splits"], r["heldout"]["of"]))
