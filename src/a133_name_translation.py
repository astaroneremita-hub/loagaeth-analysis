"""
Decifração: traduzir o léxico-núcleo. Parse morfológico + glosa de cada morfema pelo sistema nativo + contexto.

Sem pedra de Roseta, um linguista decifra um onomasticon pelo sistema de correspondência que a própria tradição dá:
cada letra enoquiana tem elemento + planeta + signo (Golden Dawn / Dee). O 'sentido' de um nome é então sua
composição: a raiz dá a natureza-base (atestada em entity_data), os afixos modulam o elemento. Entregamos, para cada
nome do léxico-núcleo: o parse (prefixo·raiz·sufixo), a glosa elemental-astrológica de cada morfema, um sentido
composto legível, e o contexto (elemento, força, natureza, nº de folhas, casa). Isto é a tradução possível - não
inventada: derivada do sistema de letras e dos atributos já medidos.
"""
import json
import unicodedata
from collections import Counter

import load
from a85_entity_attributes import load_letters

ROOTS = ["ANTANTOX", "CHASTOR", "GRADAX", "CHADAX", "ANZACH", "NOCHA", "NACHO", "ACLAX", "PHANGE", "GETH"]
DOMAIN = {"Fogo": "will / force / spirit", "Terra": "matter / body / the fixed",
          "Ar": "mind / word / breath", "Agua": "emotion / flow / the deep", "?": "veiled"}
PT_DOMAIN = {"Fogo": "vontade / força / espírito", "Terra": "matéria / corpo / o fixo",
             "Ar": "mente / palavra / sopro", "Agua": "emoção / fluxo / o profundo", "?": "velado"}


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").upper()


def split(name):
    best = None
    for r in ROOTS:
        i = name.find(r)
        if i >= 0 and (best is None or len(r) > len(best[1])):
            best = (name[:i], r, name[i + len(r):])
    return best or ("", name, "")


def elem_profile(s, L):
    c = Counter()
    for ch in s:
        c[L.get(ch, {}).get("element") or "?"] += 1
    return c


def dominant(c):
    return c.most_common(1)[0][0] if c else "?"


def planets(s, L):
    ps = [L.get(ch, {}).get("planet") for ch in s]
    ps = [p for p in ps if p and p != "None"]
    return Counter(ps).most_common(2)


def run():
    L = load_letters()
    ent = json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"]
    nl = json.load(open(load.ROOT + "/viz/name_language.json", encoding="utf-8"))
    core = [x[0] for x in nl["core_lexicon"]]
    tables_of = {x[0]: x[1] for x in nl["core_lexicon"]}

    # affix glosses: element each affix's letters add
    def morph_gloss(m):
        if not m:
            return None
        d = dominant(elem_profile(m, L))
        return {"form": m, "element": d, "domain_en": DOMAIN[d], "domain_pt": PT_DOMAIN[d]}

    out = []
    for nm in core:
        pre, root, suf = split(nm)
        e = ent.get(nm, {})
        rootprof = dominant(elem_profile(root, L))
        whole = dominant(elem_profile(nm, L))
        pl = planets(nm, L)
        meaning_en = "%s power (%s)" % (root, DOMAIN[rootprof])
        if pre:
            meaning_en = "%s-modulated %s" % (morph_gloss(pre)["domain_en"].split(" / ")[0], meaning_en)
        if suf:
            meaning_en += ", %s-inflected" % morph_gloss(suf)["domain_en"].split(" / ")[0]
        out.append({
            "name": nm, "parse": {"prefix": pre, "root": root, "suffix": suf},
            "root_element": rootprof, "whole_element": whole,
            "nature_pt": e.get("natureza", "—"), "force": e.get("forca"), "class": e.get("classe"),
            "depth": e.get("profundidade"), "tables": tables_of.get(nm),
            "planets": [p for p, _ in pl],
            "prefix_gloss": morph_gloss(pre), "suffix_gloss": morph_gloss(suf),
            "meaning_en": meaning_en,
        })

    # morpheme dictionary
    morphemes = {"roots": {}, "prefixes": {}, "suffixes": {}}
    for r in ROOTS:
        d = dominant(elem_profile(r, L))
        exemplar = next((ent[n] for n in ent if ent[n].get("raiz") == r), {})
        morphemes["roots"][r] = {"element": d, "domain_en": DOMAIN[d], "domain_pt": PT_DOMAIN[d],
                                 "nature_pt": exemplar.get("natureza", "—")}
    for p, _ in nl.get("prefixes", []):
        morphemes["prefixes"][p] = morph_gloss(p)
    for s, _ in nl.get("suffixes", []):
        morphemes["suffixes"][s] = morph_gloss(s)

    res = {"morphemes": morphemes, "names": out, "legend": {"domains_en": DOMAIN, "domains_pt": PT_DOMAIN}}
    with open(load.ROOT + "/viz/name_translation.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False)
    load.save_result("133_name_translation", {"names": len(out), "roots_glossed": len(morphemes["roots"])})
    return res


if __name__ == "__main__":
    r = run()
    print("=== DICIONÁRIO DE MORFEMAS (raiz -> elemento / domínio) ===")
    for rt, d in r["morphemes"]["roots"].items():
        print("  %-9s %-6s %-22s %s" % (rt, d["element"], d["domain_en"], d["nature_pt"]))
    print("\n=== TRADUÇÃO DO LÉXICO-NÚCLEO ===")
    for x in r["names"][:16]:
        p = x["parse"]
        parse = "·".join(z for z in (p["prefix"], p["root"], p["suffix"]) if z)
        print("  %-12s = %-18s [%s, força %s, %s folhas]  %s" % (
            x["name"], parse, x["whole_element"], x["force"], x["tables"], x["meaning_en"]))
