"""
a135 - Do the VOWEL MELODIES carry grammar? (Semitic binyan test on the root-and-pattern language)

a134 proved the name-language is root-and-pattern: consonant root + vowel melody. In Semitic the vowel template is
grammatical (active/passive/causative: KaTaB vs KuTiB). So: does the vowel melody predict a measurable feature -
element or force - beyond chance? We group the names by vowel melody and ask whether melody explains variance in
element (categorical) and force (numeric) more than a shuffle null. If a melody like O-A systematically carries one
element and A-O another, the vowels are semantic operators and we have decoded part of the grammar's meaning.
"""
import json
import random
import statistics
import unicodedata
from collections import defaultdict, Counter

import load
from a85_entity_attributes import load_letters

VOWELS = set("AEIOUY")


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def melody(w):
    return "".join(c for c in w if c in VOWELS)


def whole_element(w, L):
    c = Counter(L.get(ch, {}).get("element") or "?" for ch in w)
    return c.most_common(1)[0][0] if c else "?"


def purity(groups):
    """mean within-group element purity (fraction that is the group's modal element), weighted."""
    tot = n = 0
    for g, els in groups.items():
        if len(els) >= 2:
            modal = Counter(els).most_common(1)[0][1]
            tot += modal
            n += len(els)
    return tot / n if n else 0


def run():
    L = load_letters()
    tr = json.load(open(load.ROOT + "/viz/name_translation.json", encoding="utf-8"))["names"]
    names = [(x["name"], x["whole_element"], x.get("force")) for x in tr]

    by_mel_el = defaultdict(list)
    by_mel_force = defaultdict(list)
    for nm, el, fc in names:
        m = melody(nm)
        if len(m) >= 2:
            by_mel_el[m].append(el)
            if fc:
                by_mel_force[m].append(fc)

    real_purity = purity(by_mel_el)
    # force: between-melody variance ratio
    big = {m: fs for m, fs in by_mel_force.items() if len(fs) >= 2}
    grand = statistics.mean([f for fs in big.values() for f in fs]) if big else 0
    between = sum(len(fs) * (statistics.mean(fs) - grand) ** 2 for fs in big.values()) if big else 0

    # null: shuffle melodies across names
    mels = [melody(nm) for nm, _, _ in names if len(melody(nm)) >= 2]
    els = [el for nm, el, _ in names if len(melody(nm)) >= 2]
    rng = random.Random(135)
    null_pur = []
    for _ in range(500):
        rng.shuffle(els)
        g = defaultdict(list)
        for m, e in zip(mels, els):
            g[m].append(e)
        null_pur.append(purity(g))
    npm = statistics.mean(null_pur)
    nmax = max(null_pur)
    sd = statistics.pstdev(null_pur)
    z = (real_purity - npm) / sd if sd else 0

    # which melody -> which element (descriptive)
    mel_el = {}
    for m, els2 in sorted(by_mel_el.items(), key=lambda kv: -len(kv[1]))[:10]:
        c = Counter(els2)
        mel_el[m] = {"n": len(els2), "dominant": c.most_common(1)[0][0], "dist": dict(c)}

    res = {
        "melodies": len(by_mel_el), "element_purity_real": round(real_purity, 3),
        "element_purity_null": round(npm, 3), "null_max": round(nmax, 3), "z": round(z, 1),
        "melody_element": mel_el,
        "finding": (
            "Pureza elemental por melodia vocálica: real %.0f%% vs %.0f%% no acaso (máx %.0f%%, z=%.1f). %s" % (
                real_purity * 100, npm * 100, nmax * 100, z,
                ("CONFIRMADO: a melodia vocálica carrega gramática - vogais iguais tendem ao mesmo elemento, como os "
                 "binyanim semíticos. Decodificamos parte do 'padrão'."
                 if real_purity > nmax and z >= 3 else
                 "a melodia NÃO prediz o elemento acima do acaso - as vogais não são operador semântico detectável "
                 "aqui; são inflexão formal sem carga medível."))),
    }
    load.save_result("135_vowel_grammar", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("melodia -> elemento dominante (n):")
    for m, d in r["melody_element"].items():
        print("  %-5s %-6s n=%d  %s" % (m, d["dominant"], d["n"], d["dist"]))
