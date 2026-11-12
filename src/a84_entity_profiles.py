"""
84 - Entity profiles: define every name by MEASURED attributes, not borrowed Watchtower ranks.

The Rei/Arcanjo/Anjo labels were a metaphor and do not hold. Each name is instead profiled by what we can
measure over the whole book (tables 2-48, diamonds included):

  - forca (size of the force): total occurrences in the book (forward + reversed).
  - alcance (reach): number of tables it appears in (0-47) - how far its domain spreads.
  - potencia (how real): occurrences / what a Markov-3 surrogate predicts - how far above letter-flow it is
    placed. High = deliberately woven; ~1 = just the letters.
  - elemento: dominant Golden Dawn element of its letters (Fogo/Terra/Ar/Agua).
  - natureza: the traditional temperament of that element (a correspondence, labelled as such, not a
    measurement): Fogo ardente, Agua fluida, Ar mental, Terra firme.
  - classe (measured from the grammar): raiz (a root, pure), derivado (root + affix), ponte (two roots).
  - profundidade: letters added to the root.

This is the honest profile that the interactive atlas renders.
"""
import json
import random
import statistics
from collections import Counter

import load
from a19_machine import markov3
from a22_robustness_and_depth import base_book

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]
NATURE = {"Fogo": "ardente (vontade, impulso)", "Agua": "fluida (emocao, intuicao)",
          "Ar": "mental (pensamento, palavra)", "Terra": "firme (materia, corpo)", "?": "indefinida"}


def roots_in(name):
    found = [r for r in ROOTS if r in name]
    return [r for r in found if not any(r != o and r in o for o in found)]


def run():
    rng = random.Random(84)
    book = base_book()
    tabs = {k: "".join(x for x in book[k] if x) for k in book}
    text = "".join(tabs.values())
    surrs = ["".join(markov3(text, rng)) for _ in range(6)]

    le = json.load(open(load.RESULTS + "/79_hierarchy_powers.json", encoding="utf-8"))["letter_element_map"]

    def element(nm):
        c = Counter(le.get(ch, "?") for ch in nm)
        for k in ("?", "Espirito", "CaputDraconis", "CaudaDraconis"):
            c.pop(k, None)
        return c.most_common(1)[0][0] if c else "?"

    def count_both(t, nm):
        return t.count(nm) + (t.count(nm[::-1]) if nm != nm[::-1] else 0)

    # name universe: roots + catalogue + a82 discoveries
    names = set(ROOTS)
    g = json.load(open(load.ROOT + "/viz/grammar_data.json", encoding="utf-8"))
    names |= set(g["names"])
    try:
        cat = json.load(open(load.RESULTS + "/23_name_discovery.json", encoding="utf-8"))["A_candidates"]["top"]
        names |= {x["name"] for x in cat if len(x["name"]) >= 5}
    except Exception:
        pass

    def best_root(nm):
        cand = [(len(r), r) for r in ROOTS if r in nm]
        return max(cand)[1] if cand else None

    entities = {}
    for nm in names:
        if len(nm) < 5:
            continue
        forca = count_both(text, nm)
        if forca < 3:
            continue
        alcance = sum(1 for t in tabs.values() if count_both(t, nm) > 0)
        exp = statistics.mean(count_both(su, nm) for su in surrs)
        potencia = round(forca / max(exp, 0.3), 1)
        rr = roots_in(nm)
        root = best_root(nm)
        depth = (len(nm) - len(root)) if root else None
        classe = "ponte" if len(rr) >= 2 else ("raiz" if nm in ROOTS else "derivado")
        el = element(nm)
        entities[nm] = {
            "forca": forca, "alcance": alcance, "potencia": potencia,
            "elemento": el, "natureza": NATURE.get(el, "indefinida"),
            "classe": classe, "raiz": root, "profundidade": depth,
            "roots": rr,
        }

    # scales for the atlas
    fmax = max(e["forca"] for e in entities.values())
    pmax = max(e["potencia"] for e in entities.values())
    amax = max(e["alcance"] for e in entities.values())
    res = {
        "entities_count": len(entities),
        "force_max": fmax, "potencia_max": pmax, "tables_max": amax,
        "elements": ["Fogo", "Terra", "Ar", "Agua"],
        "classes": ["raiz", "derivado", "ponte"],
        "entities": entities,
        "note": "forca=ocorrencias totais; alcance=tabelas; potencia=ocorrencias/surrogate Markov-3; "
                "elemento+natureza=correspondencia GD das letras; classe+profundidade=gramatica medida.",
    }
    load.save_result("84_entity_profiles", res)
    # also write straight to the site
    with open(load.ROOT + "/viz/entity_data.json", "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print("entities %d | force max %d | potencia max %.1f" % (r["entities_count"], r["force_max"], r["potencia_max"]))
    top = sorted(r["entities"].items(), key=lambda kv: -kv[1]["forca"])[:18]
    print("\n%-13s %6s %6s %7s  %-6s %-9s" % ("nome", "forca", "alcance", "potenc", "elem", "classe"))
    for nm, e in top:
        print("%-13s %6d %6d %7.1f  %-6s %-9s" % (nm, e["forca"], e["alcance"], e["potencia"], e["elemento"], e["classe"]))
