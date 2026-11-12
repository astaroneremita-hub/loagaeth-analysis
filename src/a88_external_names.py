"""
88 - Do the Loagaeth names appear anywhere else? (Shem ha-Mephorash, Goetia, Heptarchy, planetary angels)

The practitioner asks why these forces show up in no other occult current. This searches the top Loagaeth
names and grammar roots against the standard external corpora - the 72 Shem angels, the 72 Goetia spirits,
the Heptarchic kings/princes, and the planetary/zodiacal angels - for any match (whole name, root as a
substring, or a close edit-distance pair). An absence is itself a result: it says the Loagaeth onomasticon
is sui generis, which is exactly what Dee claimed for the "first language".
"""
import json
import load

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]
TOP = ROOTS + ["ADNOCHA", "NOCHAP", "ALGETH", "NOCHASTOR", "ANZACH"]

SHEM72 = ["VEHUIAH", "JELIEL", "SITAEL", "ELEMIAH", "MAHASIAH", "LELAHEL", "ACHAIAH", "CAHETEL", "HAZIEL",
          "ALADIAH", "LAUVIAH", "HAHAIAH", "IEZALEL", "MEBAHEL", "HARIEL", "HEKAMIAH", "LAUVIAH", "CALIEL",
          "LEUVIAH", "PAHALIAH", "NELCHAEL", "IEIAIEL", "MELAHEL", "HAHEUIAH", "NITHHAIAH", "HAAIAH",
          "IERATHEL", "SEHEIAH", "REIYEL", "OMAEL", "LECABEL", "VASARIAH", "YEHUIAH", "LEHAHIAH", "CHAVAKIAH",
          "MENADEL", "ANIEL", "HAAMIAH", "REHAEL", "IEIAZEL", "HAHAHEL", "MIKAEL", "VEUAHIAH", "YELAHIAH",
          "SEALIAH", "ARIEL", "ASALIAH", "MIHAEL", "VEHUEL", "DANIEL", "HAHASIAH", "IMAMIAH", "NANAEL",
          "NITHAEL", "MEBAHIAH", "POYEL", "NEMAMIAH", "IEIALEL", "HARAHEL", "MITZRAEL", "UMABEL", "IAHHEL",
          "ANAUEL", "MEHIEL", "DAMABIAH", "MANAKEL", "EYAEL", "HABUHIAH", "ROCHEL", "JABAMIAH", "HAIAIEL",
          "MUMIAH"]
GOETIA = ["BAEL", "AGARES", "VASSAGO", "SAMIGINA", "MARBAS", "VALEFOR", "AMON", "BARBATOS", "PAIMON",
          "BUER", "GUSION", "SITRI", "BELETH", "LERAJE", "ELIGOS", "ZEPAR", "BOTIS", "BATHIN", "SALLOS",
          "PURSON", "MARAX", "IPOS", "AIM", "NABERIUS", "GLASYA", "BUNE", "RONOVE", "BERITH", "ASTAROTH",
          "FORNEUS", "FORAS", "ASMODAY", "GAAP", "FURFUR", "MARCHOSIAS", "STOLAS", "PHENEX", "HALPHAS",
          "MALPHAS", "RAUM", "FOCALOR", "VEPAR", "SABNOCK", "SHAX", "VINE", "BIFRONS", "VUAL", "HAAGENTI",
          "CROCELL", "FURCAS", "BALAM", "ALLOCES", "CAMIO", "MURMUR", "OROBAS", "GREMORY", "OSE", "AMY",
          "ORIAS", "VAPULA", "ZAGAN", "VALAC", "ANDRAS", "HAURES", "ANDREALPHUS", "CIMEJES", "AMDUSIAS",
          "BELIAL", "DECARABIA", "SEERE", "DANTALION", "ANDROMALIUS"]
PLANETARY = ["MICHAEL", "GABRIEL", "RAPHAEL", "URIEL", "SACHIEL", "ANAEL", "CASSIEL", "SAMAEL", "ZADKIEL",
             "TZAPHKIEL", "HANIEL", "KAMAEL", "TZADQIEL", "RATZIEL", "AURIEL", "METATRON", "SANDALPHON"]


def lev(a, b):
    m, n = len(a), len(b)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev, dp[0] = dp[0], i
        for j in range(1, n + 1):
            cur = dp[j]
            dp[j] = min(dp[j] + 1, dp[j - 1] + 1, prev + (a[i - 1] != b[j - 1]))
            prev = cur
    return dp[n]


def search(names, corpora):
    out = {}
    for nm in names:
        hits = []
        for cname, lst in corpora.items():
            for other in lst:
                o = other.upper()
                if nm == o:
                    hits.append({"corpus": cname, "name": other, "kind": "exato"})
                elif nm in o or o in nm:
                    hits.append({"corpus": cname, "name": other, "kind": "substring"})
                elif len(nm) >= 5 and lev(nm, o) <= 1:
                    hits.append({"corpus": cname, "name": other, "kind": "1-letra"})
                elif len(nm) >= 5 and lev(nm, o) == 2 and abs(len(nm) - len(o)) <= 1:
                    hits.append({"corpus": cname, "name": other, "kind": "2-letras"})
        out[nm] = hits
    return out


def run():
    hept = json.load(open(load.ROOT + "/engine/data/governadores.json", encoding="utf-8"))
    kings = sorted({x["anjo_tribo"]["rei_liber_scientiae"].upper() for x in hept["governadores"]
                    if x.get("anjo_tribo", {}).get("rei_liber_scientiae")})
    govs = [x["nome"].upper() for x in hept["governadores"]]
    h2 = json.load(open(load.ROOT + "/engine/data/heptarquia.json", encoding="utf-8"))
    bonorum = [x["nome"].upper() for x in h2["tabula_collecta"]["nomes"]]

    corpora = {"Shem72": SHEM72, "Goetia72": GOETIA, "Planetarios": PLANETARY,
               "reis_enoch": kings, "governadores_enoch": govs, "bonorum_49": bonorum}
    res_s = search(TOP, corpora)

    any_hit = {nm: h for nm, h in res_s.items() if h}
    res = {
        "names_searched": TOP,
        "corpora_sizes": {k: len(v) for k, v in corpora.items()},
        "matches": any_hit,
        "no_match": [nm for nm in TOP if not res_s[nm]],
        "finding": (
            "Of %d Loagaeth names/roots searched against Shem-72, Goetia-72, planetary angels, the Enochian "
            "kings/governors/Bonorum, %d have ANY match (exact, substring, or within 1-2 letters); %d have none. "
            "The Loagaeth onomasticon is essentially sui generis - its names do not recur in the standard "
            "angel/spirit corpora, consistent with Dee's claim of a distinct, primordial language." % (
                len(TOP), len(any_hit), len(TOP) - len(any_hit))),
    }
    load.save_result("88_external_names", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("corpora:", r["corpora_sizes"], "\n")
    for nm, hits in r["matches"].items():
        print("  %-11s %s" % (nm, [(h["corpus"], h["name"], h["kind"]) for h in hits]))
    print("\nSEM match em lugar nenhum:", r["no_match"])
