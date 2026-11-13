"""
a141 - Is the grammar G COMPATIBLE with the real names? Two honest tests.

(1) HELD-OUT PREDICTION: split the 90 names in half. Build G from one half. Does G generate the OTHER half - names
    it never saw? If a grammar built from half predicts the unseen half, it captures the real rule (not overfit).
    Compare to a RANDOM grammar (random skeletons/melodies of the same sizes): it should predict almost none.
(2) INDISTINGUISHABILITY: generate names with G and compare their letter-bigram profile to the real names (cosine).
    Also compare a random-grammar's output. If G-output looks like real and random-output does not, G is the right
    pattern; swapping G for a random one breaks the match.
"""
import json
import random
import unicodedata
from collections import Counter, defaultdict

import load

VOW = set("AEIOU")


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").upper()


def parse(w):
    skel = "".join(c for c in w if c not in VOW)
    mel = "".join(c for c in w if c in VOW)
    tmpl = "".join("C" if c not in VOW else "V" for c in w)
    return skel, mel, tmpl


def interleave(skel, mel, tmpl):
    out, si, mi = [], 0, 0
    for t in tmpl:
        if t == "C":
            if si >= len(skel):
                return None
            out.append(skel[si]); si += 1
        else:
            if mi >= len(mel):
                return None
            out.append(mel[mi]); mi += 1
    if si != len(skel) or mi != len(mel):
        return None
    return "".join(out)


def build_grammar(names):
    SK, ML, TM = set(), set(), set()
    for w in names:
        s, m, t = parse(w)
        SK.add(s); ML.add(m); TM.add(t)
    return SK, ML, TM


def generate(SK, ML, TM, cap=20000):
    out = set()
    tmpl_by = defaultdict(list)
    for t in TM:
        tmpl_by[(t.count("C"), t.count("V"))].append(t)
    for s in SK:
        for m in ML:
            for t in tmpl_by.get((len(s), len(m)), []):
                w = interleave(s, m, t)
                if w:
                    out.add(w)
                    if len(out) >= cap:
                        return out
    return out


def bigrams(words):
    c = Counter()
    for w in words:
        for i in range(len(w) - 1):
            c[w[i:i + 2]] += 1
    tot = sum(c.values()) or 1
    return {k: v / tot for k, v in c.items()}


def cosine(a, b):
    ks = set(a) | set(b)
    na = sum(v * v for v in a.values()) ** 0.5
    nb = sum(v * v for v in b.values()) ** 0.5
    return sum(a.get(k, 0) * b.get(k, 0) for k in ks) / (na * nb) if na and nb else 0


def run():
    names = [da(w) for w in json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))]
    rng = random.Random(141)

    # (1) held-out prediction, averaged over splits
    hits_G, hits_rand = [], []
    CONS = "BCDFGHLMNPQRSTXZ"
    for trial in range(10):
        shuf = names[:]
        rng.shuffle(shuf)
        half = len(shuf) // 2
        train, test = shuf[:half], set(shuf[half:])
        SK, ML, TM = build_grammar(train)
        gen = generate(SK, ML, TM)
        hits_G.append(len(test & gen) / len(test))
        # random grammar: same number of skeletons/melodies but random strings
        rSK = set("".join(rng.choice(CONS) for _ in range(len(s))) for s in SK)
        rML = set("".join(rng.choice("AEIOU") for _ in range(len(m))) for m in ML)
        rgen = generate(rSK, rML, TM)
        hits_rand.append(len(test & rgen) / len(test))
    mG = sum(hits_G) / len(hits_G)
    mR = sum(hits_rand) / len(hits_rand)

    # (2) indistinguishability
    SK, ML, TM = build_grammar(names)
    gen = list(generate(SK, ML, TM))
    rng.shuffle(gen)
    gen_sample = gen[:500]
    real_bg = bigrams(names)
    gen_bg = bigrams(gen_sample)
    # random-grammar output
    rSK = set("".join(rng.choice(CONS) for _ in range(len(s))) for s in SK)
    rgen = list(generate(rSK, ML, TM))[:500]
    rgen_bg = bigrams(rgen)
    sim_realG = cosine(real_bg, gen_bg)
    sim_realRand = cosine(real_bg, rgen_bg)

    res = {
        "heldout_G_predicts": round(mG, 3), "heldout_random_predicts": round(mR, 3),
        "bigram_sim_real_vs_G": round(sim_realG, 3), "bigram_sim_real_vs_random": round(sim_realRand, 3),
        "genspace_full": len(gen),
        "finding": (
            "(1) PREDIÇÃO: G montada com METADE dos nomes gera %.0f%% da outra metade (nomes nunca vistos); uma "
            "gramática ALEATÓRIA do mesmo tamanho gera só %.0f%%. G prevê nomes reais que não viu - captura a regra, "
            "não decora. (2) INDISTINGUIBILIDADE: o perfil de bigrama dos nomes gerados por G bate %.2f com os reais; "
            "o de uma gramática aleatória bate só %.2f. Trocar G por aleatório QUEBRA a compatibilidade - então é a "
            "gramática DECIFRADA que importa, não qualquer uma. %s" % (
                mG * 100, mR * 100, sim_realG, sim_realRand,
                "COMPATÍVEL: os nomes gerados são da mesma língua dos originais."
                if mG > mR * 2 and sim_realG > sim_realRand else
                "compatibilidade fraca - G não se distingue de uma gramática qualquer.")),
    }
    load.save_result("141_grammar_compat", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("predição held-out: G %.0f%% vs aleatório %.0f%%" % (
        r["heldout_G_predicts"] * 100, r["heldout_random_predicts"] * 100))
    print("bigrama real-vs-G %.2f | real-vs-aleatório %.2f" % (
        r["bigram_sim_real_vs_G"], r["bigram_sim_real_vs_random"]))
