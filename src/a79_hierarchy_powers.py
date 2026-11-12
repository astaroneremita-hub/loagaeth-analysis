"""
79 - Hierarchy and powers: each name's element from the Enochian alphabet, each house's dominant power.

We have territories (a78): CHADAX opens, the NOCHA house holds the front, the GETH house the back, CHASTOR
is the spine. This gives each name a POWER, the way the Watchtowers give each square an element: every
Enochian letter has a Golden Dawn correspondence (a sign or element), so every name has an elemental
signature, and its dominant element is its power. Then we ask whether a FAMILY shares a power - whether a
house is, elementally, one thing - and whether the four houses divide the four elements, like a hierarchy.

Letter -> element via the GD sign of each Enochian letter (b_correspondencias_astrologicas, F04).
"""
import json
import statistics
from collections import Counter

import load
from a77_names_woven import FAMILIES

SIGN_ELEMENT = {
    "Aries": "Fogo", "Leao": "Fogo", "Sagitario": "Fogo",
    "Touro": "Terra", "Virgem": "Terra", "Capricornio": "Terra",
    "Gemeos": "Ar", "Libra": "Ar", "Aquario": "Ar",
    "Cancer": "Agua", "Escorpiao": "Agua", "Peixes": "Agua",
}
DIRECT = {"C": "Fogo", "X": "Terra", "H": "Ar", "Q": "Agua"}  # letters named as an element outright
SPECIAL = {"D": "Espirito", "T": "CaputDraconis", "F": "CaudaDraconis"}


def _norm(s):
    return (s.replace("á", "a").replace("â", "a").replace("ã", "a").replace("é", "e")
             .replace("ê", "e").replace("í", "i").replace("ó", "o").replace("ô", "o")
             .replace("ç", "c").replace("â", "a"))


def letter_elements():
    d = json.load(open(load.ROOT + "/engine/data/gematria_enoquiana.json", encoding="utf-8"))
    b = d["b_correspondencias_astrologicas"]["por_letra"]
    out = {}
    for ch, v in b.items():
        if ch in DIRECT:
            out[ch] = DIRECT[ch]
            continue
        if ch in SPECIAL:
            out[ch] = SPECIAL[ch]
            continue
        sign = _norm(str(v.get("F04_signo_ou_elemento") or ""))
        out[ch] = SIGN_ELEMENT.get(sign, "?")
    return out


def signature(name, le):
    c = Counter(le.get(ch, "?") for ch in name)
    for k in ("?", "Espirito", "CaputDraconis", "CaudaDraconis"):
        c.pop(k, None)
    return c


def dominant(name, le):
    c = signature(name, le)
    return c.most_common(1)[0][0] if c else "?"


def run():
    le = letter_elements()
    TERRITORY = {"CHADAX": "abertura (2a-8a)", "NOCHA": "casa da frente (12a-14b)",
                 "GETH": "casa do fundo (16a-27b)", "CHASTOR": "espinha (picos 15b/18b)",
                 "DAHAHOXOM": "porta 2b"}

    houses = {}
    for fam, names in FAMILIES.items():
        sigs = Counter()
        rows = []
        for nm in names:
            s = signature(nm, le)
            sigs += s
            rows.append({"name": nm, "power": dominant(nm, le),
                         "signature": dict(s.most_common())})
        tot = sum(sigs.values()) or 1
        dom = sigs.most_common(1)[0][0] if sigs else "?"
        share = round(100 * sigs[dom] / tot)
        agree = sum(1 for r in rows if r["power"] == dom)
        houses[fam] = {
            "territory": TERRITORY.get(fam, ""),
            "house_power": dom, "power_share_pct": share,
            "members_agreeing": "%d/%d" % (agree, len(rows)),
            "house_signature": dict(sigs.most_common()),
            "members": rows,
        }

    # do the four houses divide distinct elements?
    powers = {f: houses[f]["house_power"] for f in houses}
    distinct = len(set(powers.values()))
    res = {
        "letter_element_map": le,
        "houses": houses,
        "house_powers": powers,
        "distinct_powers_among_houses": distinct,
        "note": "Each Enochian letter carries a Golden Dawn element; a name's dominant element is its power; "
                "a house's power is its members' combined dominant element.",
        "finding": (
            "Each name carries an elemental power read straight off the Enochian alphabet, and the houses do "
            "not all share one: " + "; ".join("%s = %s (%d%%, %s agree)" % (
                f, houses[f]["house_power"], houses[f]["power_share_pct"], houses[f]["members_agreeing"])
                for f in ("CHADAX", "NOCHA", "GETH", "CHASTOR", "DAHAHOXOM") if f in houses)),
    }
    load.save_result("79_hierarchy_powers", res)
    return res


if __name__ == "__main__":
    r = run()
    print("letter -> element:")
    print("  " + "  ".join("%s:%s" % (k, v[:4]) for k, v in sorted(r["letter_element_map"].items())))
    print("\nhouses (territory | power | members):")
    for f, h in r["houses"].items():
        print("\n  %s  [%s]  POWER=%s (%s agree)" % (f, h["territory"], h["house_power"], h["members_agreeing"]))
        print("    signature:", h["house_signature"])
        for m in h["members"]:
            print("      %-11s %-6s %s" % (m["name"], m["power"], m["signature"]))
    print("\n" + r["finding"])
