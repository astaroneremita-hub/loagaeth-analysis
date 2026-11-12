"""
85 - The attribute algorithm: from a name's Enochian letters to its full profile (element, planet, form).

Each Enochian letter carries a Golden Dawn correspondence - a sign, a planetary condition, an element. So a
name is read as the SUM of its letters' correspondences: an elemental balance, a ruling planet, a dominant
modality, and from those a traditional "forma do ser". This is the algorithm the user asked for, run for every
name in the system. It is a reading built on a documented correspondence table - deterministic, reproducible -
not a claim that the name denotes a literal spirit; it says what attributes the alphabet assigns to that name.
"""
import json
from collections import Counter

import load

SIGN_ELEMENT = {
    "Aries": "Fogo", "Leao": "Fogo", "Sagitario": "Fogo", "Fogo": "Fogo",
    "Touro": "Terra", "Virgem": "Terra", "Capricornio": "Terra", "Terra": "Terra",
    "Gemeos": "Ar", "Libra": "Ar", "Aquario": "Ar", "Ar": "Ar",
    "Cancer": "Agua", "Escorpiao": "Agua", "Peixes": "Agua", "Agua": "Agua",
}
# forma do ser: traditional reading from dominant element + dominant planet (a correspondence, labelled)
FORMA = {
    "Fogo": "forma ígnea - luz, chama, impulso que irrompe",
    "Terra": "forma densa - corpo, pedra, raiz, o que sustenta",
    "Ar": "forma sutil - sopro, voz, pensamento que corre",
    "Agua": "forma fluida - onda, espelho, emoção que dissolve",
    "?": "forma indefinida",
}


def _norm(s):
    if not s:
        return ""
    for a, b in zip("áâãéêíóôúç", "aaaeeioouc"):
        s = s.replace(a, b)
    return s


def load_letters():
    d = json.load(open(load.ROOT + "/engine/data/gematria_enoquiana.json", encoding="utf-8"))
    b = d["b_correspondencias_astrologicas"]["por_letra"]
    out = {}
    for ch, v in b.items():
        sign = _norm(v.get("F04_signo_ou_elemento") or "")
        planet = (v.get("F04_condicao_planetaria") or "")
        pl = _norm(planet).split(" de ")[0].split(" em ")[0].strip() if planet else None
        out[ch] = {"dee": v.get("nome_dee"), "sign": sign, "planet": pl,
                   "element": SIGN_ELEMENT.get(sign, "?" if sign in ("Espirito", "CaputDraconis", "CaudaDraconis") else "?")}
    return out


def ficha(name, L):
    els = Counter()
    signs = Counter()
    planets = Counter()
    special = []
    for ch in name:
        info = L.get(ch)
        if not info:
            continue
        if info["sign"] in ("Espirito", "CaputDraconis", "CaudaDraconis"):
            special.append(info["sign"])
            continue
        if info["element"] in ("Fogo", "Terra", "Ar", "Agua"):
            els[info["element"]] += 1
            signs[info["sign"]] += 1
        if info["planet"]:
            planets[info["planet"]] += 1
    tot = sum(els.values()) or 1
    dom_el = els.most_common(1)[0][0] if els else "?"
    return {
        "name": name,
        "element_balance": {e: round(100 * els[e] / tot) for e in ("Fogo", "Terra", "Ar", "Agua")},
        "dominant_element": dom_el,
        "ruling_planet": planets.most_common(1)[0][0] if planets else None,
        "planets": dict(planets.most_common()),
        "signs": dict(signs.most_common()),
        "special_points": special,  # Spirit / dragon's head-tail letters (D, T, F)
        "forma": FORMA.get(dom_el, FORMA["?"]),
    }


def run():
    L = load_letters()
    ent = json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"]
    fichas = {nm: ficha(nm, L) for nm in ent}
    res = {"letters": L, "fichas": fichas, "count": len(fichas),
           "note": "Algoritmo: cada letra enoquiana carrega signo+planeta+elemento (Golden Dawn); o nome e a "
                   "soma. Balanco elemental, planeta regente, signos, forma. Correspondencia documentada, "
                   "determinista - define os atributos que o alfabeto atribui, nao prova um espirito literal."}
    load.save_result("85_entity_attributes", res)
    with open(load.ROOT + "/viz/entity_astro.json", "w", encoding="utf-8") as f:
        json.dump({"letters": L, "fichas": fichas}, f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print("fichas geradas:", r["count"], "\n")
    for nm in ["NOCHA", "CHASTOR", "ADNOCHA", "NOCHASTOR", "DAHAHOXOM", "ANZACH", "GETH"]:
        if nm in r["fichas"]:
            f = r["fichas"][nm]
            print("%-11s elem=%s %s | planeta=%s | forma: %s" % (
                nm, f["dominant_element"], f["element_balance"], f["ruling_planet"], f["forma"]))
            print("            signos:", f["signs"], "| planetas:", f["planets"],
                  ("| pontos: " + ",".join(f["special_points"]) if f["special_points"] else ""))
