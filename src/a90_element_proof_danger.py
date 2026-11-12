"""
90 - Element re-proof by several independent variables, plus a danger reading.

The first element assignment (a85) used ONE variable: the letter's zodiac sign -> triplicity element. The
practitioner asked to prove the element with OTHER variables too - the pyramid-style layering the Golden Dawn
puts on each letter. Each Enochian letter carries three correspondences we can read independently:

  1. F04 zodiac sign  -> element by triplicity (Fire: Aries/Leo/Sag; Earth: Taurus/Virgo/Cap; Air: Gem/Lib/Aq;
     Water: Can/Sco/Pis).
  2. F05 zodiac sign (a second recension) -> element the same way.
  3. the ruling PLANET -> element by the classical scheme (Fire: Sun/Mars/Jupiter; Earth: Venus/Saturn;
     Air: Mercury; Water: Moon).

These disagree for some letters (N = Scorpio -> Water by sign, but Mars -> Fire by planet). A name's element is
ROBUST when the sign-reading and the planet-reading agree; AMBIGUOUS when they split. That is the honest proof.

Danger reading (a labelled correspondence, not a measurement): caution rises with Fire, with the martial/Saturn
(malefic) planets, and with the dragon's-head/tail nodal letters (T, F) and Spirit (D) - the fated, forceful,
boundary-crossing letters. Reported 0-100 with the dominant cautions named.
"""
import json
from collections import Counter

import load

TRIPL = {"Aries": "Fogo", "Leao": "Fogo", "Sagitario": "Fogo", "Fogo": "Fogo",
         "Touro": "Terra", "Virgem": "Terra", "Capricornio": "Terra", "Terra": "Terra",
         "Gemeos": "Ar", "Libra": "Ar", "Aquario": "Ar", "Ar": "Ar",
         "Cancer": "Agua", "Escorpiao": "Agua", "Peixes": "Agua", "Agua": "Agua"}
PLANET_EL = {"Sol": "Fogo", "Marte": "Fogo", "Jupiter": "Fogo", "Venus": "Terra", "Saturno": "Terra",
             "Mercurio": "Ar", "Lua": "Agua"}


def _norm(s):
    if not s:
        return ""
    for a, b in zip("áâãéêíóôúç", "aaaeeioouc"):
        s = s.replace(a, b)
    return s


def letter_table():
    d = json.load(open(load.ROOT + "/engine/data/gematria_enoquiana.json", encoding="utf-8"))
    b = d["b_correspondencias_astrologicas"]["por_letra"]
    out = {}
    for ch, v in b.items():
        s4 = _norm(v.get("F04_signo_ou_elemento") or "")
        s5 = _norm(v.get("F05_signo_ou_elemento") or "")
        pl = _norm((v.get("F04_condicao_planetaria") or "").split(" de ")[0].split(" em ")[0]).strip()
        node = s4 in ("CaputDraconis", "CaudaDraconis") or s4 == "Espirito"
        out[ch] = {"sign_el": TRIPL.get(s4), "sign2_el": TRIPL.get(s5), "planet": pl or None,
                   "planet_el": PLANET_EL.get(pl), "sign": s4, "node": node}
    return out


def name_element(name, L):
    def dom(key):
        c = Counter()
        for ch in name:
            e = (L.get(ch) or {}).get(key)
            if e in ("Fogo", "Terra", "Ar", "Agua"):
                c[e] += 1
        return c.most_common(1)[0][0] if c else None
    by_sign = dom("sign_el")
    by_sign2 = dom("sign2_el")
    by_planet = dom("planet_el")
    votes = [x for x in (by_sign, by_sign2, by_planet) if x]
    tally = Counter(votes)
    winner, n = (tally.most_common(1)[0] if tally else (None, 0))
    robust = "robusto" if n >= 2 and len(set(votes)) == 1 else ("maioria" if n >= 2 else "ambiguo")
    return {"by_sign": by_sign, "by_sign2": by_sign2, "by_planet": by_planet,
            "element": winner, "agreement": robust, "votes": dict(tally)}


def danger(name, L):
    n = len(name) or 1
    fire = sum(1 for ch in name if (L.get(ch) or {}).get("sign_el") == "Fogo" or (L.get(ch) or {}).get("planet_el") == "Fogo")
    mars = sum(1 for ch in name if (L.get(ch) or {}).get("planet") == "Marte")
    saturn = sum(1 for ch in name if (L.get(ch) or {}).get("planet") == "Saturno")
    nodes = sum(1 for ch in name if (L.get(ch) or {}).get("node"))
    score = round(100 * (0.9 * fire + 1.0 * mars + 0.7 * saturn + 1.1 * nodes) / (n * 1.3))
    score = min(100, score)
    cautions = []
    if mars:
        cautions.append("marcial (Marte)")
    if nodes:
        cautions.append("nodal/limiar (Dragao/Espirito)")
    if saturn:
        cautions.append("saturnino (restricao)")
    if fire > n / 2:
        cautions.append("igneo (impulso)")
    band = "alto" if score >= 55 else ("medio" if score >= 30 else "baixo")
    return {"score": score, "band": band, "cautions": cautions or ["brando"]}


def run():
    L = letter_table()
    ent = json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"]
    out = {}
    for nm in ent:
        el = name_element(nm, L)
        dg = danger(nm, L)
        out[nm] = {"element_multi": el, "danger": dg, "prev_element": ent[nm]["elemento"]}
    # how often the multi-variable element matches the single-variable one
    agree_prev = sum(1 for nm in out if out[nm]["element_multi"]["element"] == out[nm]["prev_element"])
    robust_n = sum(1 for nm in out if out[nm]["element_multi"]["agreement"] == "robusto")
    res = {
        "letter_table": L, "entities": out,
        "names": len(out), "robust_element": robust_n,
        "matches_single_variable": agree_prev,
        "note": "element_multi: elemento por signo (F04), por signo2 (F05) e por planeta; 'robusto' = todos "
                "concordam, 'maioria' = 2 de 3, 'ambiguo' = divergem. danger: leitura tradicional (Fogo + "
                "Marte + Saturno + nodos/Espirito), 0-100.",
    }
    load.save_result("90_element_proof_danger", res)
    with open(load.ROOT + "/viz/entity_power.json", "w", encoding="utf-8") as f:
        json.dump({nm: {"element_multi": out[nm]["element_multi"], "danger": out[nm]["danger"]} for nm in out},
                  f, ensure_ascii=False)
    return res


if __name__ == "__main__":
    r = run()
    print("%d entidades | elemento robusto (3 concordam): %d | bate com 1-variavel: %d\n" % (
        r["names"], r["robust_element"], r["matches_single_variable"]))
    for nm in ["NOCHA", "NACHO", "CHASTOR", "ADNOCHA", "ANZACH", "CHADAX", "DAHAHOXOM", "GETH", "GRADAX"]:
        if nm in r["entities"]:
            e = r["entities"][nm]["element_multi"]
            d = r["entities"][nm]["danger"]
            print("%-11s elem=%s (%s) [sign %s/%s · planeta %s] | PERIGO %d (%s): %s" % (
                nm, e["element"], e["agreement"], e["by_sign"], e["by_sign2"], e["by_planet"],
                d["score"], d["band"], ", ".join(d["cautions"])))
