# -*- coding: utf-8 -*-
"""a227 - element GEOGRAPHY (new, from the #396 correction).

A) AGREEMENT MAP: per folha, dominant element by SIGN (triplicity) vs by PLANET (ruler).
   Where do they agree (robust element) vs conflict (contested)? Map across 48 folhas.
B) VOICE vs BODY: element from VOWELS only (the sung voice) vs CONSONANTS only (the skeleton).
   Does the book's voice-element differ from its body-element?
stdlib only.
"""
import os
import sys
import json
import importlib
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
a85 = importlib.import_module("a85_entity_attributes")
LET = a85.load_letters()
VOW = set("AEIOU")
EL = ("Fogo", "Terra", "Ar", "Agua")
PLANET_EL = {"Sol": "Fogo", "Marte": "Fogo", "Jupiter": "Fogo", "Venus": "Terra",
             "Saturno": "Terra", "Mercurio": "Ar", "Lua": "Agua"}


def sign_el(L):
    i = LET.get(L, {}); return a85.SIGN_ELEMENT.get(i.get("sign") or i.get("signo"))


def planet_el(L):
    i = LET.get(L, {}); return PLANET_EL.get(i.get("planet") or i.get("planeta"))


def dom(text, fn, filt=None):
    c = Counter()
    for ch in text:
        if filt == "V" and ch not in VOW:
            continue
        if filt == "C" and ch in VOW:
            continue
        e = fn(ch)
        if e in EL:
            c[e] += 1
    return (c.most_common(1)[0][0], dict(c)) if c else ("?", {})


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    nums = load.table_numbers()
    rows = []
    agree = 0
    for n in nums:
        t = load.table_text(n)
        ds = dom(t, sign_el)[0]; dp = dom(t, planet_el)[0]
        a = ds == dp
        agree += a
        rows.append({"folha": n, "signo": ds, "planeta": dp, "concordam": a})
    print(f"[A concordância] {agree}/{len(nums)} folhas com signo==planeta", flush=True)
    conflict = [r["folha"] for r in rows if not r["concordam"]]
    print(f"    folhas em CONFLITO: {conflict}", flush=True)
    # what the conflict looks like
    cc = Counter((r["signo"], r["planeta"]) for r in rows if not r["concordam"])
    print(f"    tipos de conflito (signo,planeta): {dict(cc)}", flush=True)

    # B voice vs body, per region
    regions = [("Abertura",range(1,13)),("Corpo",range(13,26)),("Costura",range(26,29)),
               ("Descida",range(29,41)),("Profundo",range(41,49))]
    vb = []
    for name, rng in regions:
        txt = "".join(load.table_text(f) for f in rng)
        voice = dom(txt, sign_el, "V")[0]
        body = dom(txt, sign_el, "C")[0]
        vb.append({"regiao": name, "voz_vogal": voice, "corpo_consoante": body})
        print(f"[B voz/corpo] {name:10s}: voz(vogais)={voice}  corpo(consoantes)={body}", flush=True)

    out = {"agreement_by_folha": rows, "n_agree": agree, "conflict_folhas": conflict,
           "conflict_types": {f"{a}|{b}": c for (a, b), c in cc.items()},
           "voice_body": vb}
    with open(os.path.join(os.path.dirname(HERE), "viz", "element_geo.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "227_element_geography.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
