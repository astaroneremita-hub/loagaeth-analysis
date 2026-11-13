"""
a143 - Is the Loagaeth grammar the UNIVERSAL Enochian grammar? Test it on the other systems.

The grand hypothesis: if the Watchtower / Governor / Heptarchy / Call names obey the SAME grammar as the Loagaeth
(anti-hiatus phonotactics + root-and-pattern: consonant skeleton + vowel melody), then one grammar generates the
whole Enochian corpus and the Loagaeth is its key. For each system we measure: (1) anti-hiatus (vowel-vowel adjacency
rate - low = same phonotactics), (2) root-and-pattern (fraction of names sharing a consonant skeleton with vowel
variation - the Semitic signature). Compared to the Loagaeth and to an English baseline. If the Enochian systems
match the Loagaeth and not English, the grammar is universal across Enochian.
"""
import json
import re
import unicodedata
from collections import defaultdict

import load

VOW = set("AEIOU")


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").upper()


def harvest(o, acc):
    if isinstance(o, str):
        w = da(o)
        if re.fullmatch(r"[A-Z]{3,14}", w):
            acc.add(w)
    elif isinstance(o, dict):
        for v in o.values():
            harvest(v, acc)
    elif isinstance(o, list):
        for v in o:
            harvest(v, acc)


def antihiato(words):
    tot = vv = 0
    for w in words:
        for i in range(len(w) - 1):
            tot += 1
            if w[i] in VOW and w[i + 1] in VOW:
                vv += 1
    return 100 * vv / tot if tot else 0


def root_pattern(words):
    sk = defaultdict(set)
    for w in words:
        s = "".join(c for c in w if c not in VOW)
        if len(s) >= 2:
            sk[s].add(w)
    shared = sum(len(v) for v in sk.values() if len(v) >= 2)
    return 100 * shared / len(words) if words else 0


def system_words(fname):
    acc = set()
    harvest(json.load(open(load.ROOT + "/engine/data/" + fname, encoding="utf-8")), acc)
    return acc


def run():
    loag = {da(w) for w in json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))}
    gov = system_words("governadores.json")
    hep = system_words("heptarquia.json")
    cham = set()
    for c in json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]:
        for wd in c["palavras"]:
            cham.add(da(wd["chave"]))
    cham = {w for w in cham if len(w) >= 3}
    eng = set("TOGETHER BROTHER MOTHER FATHER WONDER UNDER MASTER CHAPTER CENTER NUMBER WINTER SUMMER DINNER LETTER "
              "MONSTER SINISTER REGISTER CHARACTER PROSPER WHISPER".split())

    systems = {"Loagaeth": loag, "Governadores+Torres": gov, "Heptarquia": hep, "Chamadas (vocab)": cham, "Inglês (controle)": eng}
    out = {}
    for name, ws in systems.items():
        out[name] = {"n": len(ws), "anti_hiato_pct": round(antihiato(ws), 1), "root_pattern_pct": round(root_pattern(ws), 1)}

    L = out["Loagaeth"]
    en = out["Inglês (controle)"]
    match = [k for k in ("Governadores+Torres", "Heptarquia", "Chamadas (vocab)")
             if out[k]["anti_hiato_pct"] < en["anti_hiato_pct"] * 0.7 and out[k]["root_pattern_pct"] > en["root_pattern_pct"] * 1.5]
    res = {
        "systems": out, "match_loagaeth": match,
        "finding": (
            "Gramática do Loagaeth (anti-hiato %.1f%%, raiz-e-padrão %.1f%%) aplicada aos outros sistemas enoquianos. "
            "Casam com o padrão do Loagaeth (anti-hiato baixo + raiz-e-padrão alto, ao contrário do inglês): %s. %s" % (
                L["anti_hiato_pct"], L["root_pattern_pct"], ", ".join(match) or "nenhum",
                ("CONFIRMADO: a gramática raiz-e-padrão/anti-hiato é UNIVERSAL no enochiano — o Loagaeth e os demais "
                 "sistemas obedecem a mesma lei. Uma gramática descreve todo o corpus enoquiano."
                 if len(match) >= 2 else
                 "a gramática do Loagaeth NÃO se estende limpa aos outros sistemas - cada um tem forma própria."))),
    }
    load.save_result("143_universal_grammar", res)
    return res


if __name__ == "__main__":
    r = run()
    print("sistema | n | anti-hiato%% (baixo=mesma fonotática) | raiz-e-padrão%% (alto=semítico)")
    for k, v in r["systems"].items():
        print("  %-22s %4d  anti-hiato %5.1f  raiz-padrão %5.1f" % (k, v["n"], v["anti_hiato_pct"], v["root_pattern_pct"]))
    print("\n" + r["finding"])
