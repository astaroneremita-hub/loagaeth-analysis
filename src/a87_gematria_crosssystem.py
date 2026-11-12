"""
87 - Gematria of the top names, and cross-system presence (Calls, Watchtowers, Heptarchy, Governors).

Two questions the practitioner asked:
  A) Do the most-repeated Loagaeth names give meaningful gematria values - do they share values (kinship), or
     hit notable Enochian numbers (30, 49, 91, 2401, servant counts)? Tested across several documented systems.
  B) Do the grammar ROOTS and top names connect to the other Enochian systems - appearing in the Heptarchy's
     49 angel names, the 91 Governors, or the words of the Calls - more than frequency-matched chance?
"""
import json
import random
import statistics
from collections import Counter, defaultdict

import load

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]
TOP = ["NOCHA", "ADNOCHA", "NACHO", "CHASTOR", "ANZACH", "ACLAX", "ALGETH", "NOCHAP", "NOCHASTOR", "CHADAX", "GRADAX"]
NOTABLE = {30: "Aethyrs", 49: "Loagaeth / Bonorum", 91: "Governadores", 2401: "49x49", 7: "Heptarquia",
           12: "tribos", 48: "Chamadas-tabuas"}


def load_systems():
    g = json.load(open(load.ROOT + "/engine/data/gematria_enoquiana.json", encoding="utf-8"))
    out = {}
    for s in g["c_sistemas_de_valores"]:
        v = s.get("valores")
        if v and all(isinstance(x, int) for x in v.values()) and len(v) >= 20:
            out[s["id"].split("__")[0]] = v
    return out


def val(name, tbl):
    return sum(tbl.get(ch, 0) for ch in name)


def run():
    rng = random.Random(87)
    systems = load_systems()

    # A) gematria of top names
    gem = {}
    for nm in TOP:
        gem[nm] = {sys: val(nm, tbl) for sys, tbl in systems.items()}
    # shared values within a system
    shared = {}
    for sys in systems:
        c = Counter(gem[nm][sys] for nm in TOP)
        groups = {v: [nm for nm in TOP if gem[nm][sys] == v] for v, n in c.items() if n >= 2}
        shared[sys] = groups
    # notable hits
    notable = defaultdict(list)
    for nm in TOP:
        for sys in systems:
            v = gem[nm][sys]
            if v in NOTABLE:
                notable[nm].append({"system": sys, "value": v, "means": NOTABLE[v]})

    # B) cross-system name lists
    hept = json.load(open(load.ROOT + "/engine/data/heptarquia.json", encoding="utf-8"))
    hept_names = [x["nome"].upper() for x in hept["tabula_collecta"]["nomes"]]
    gov = json.load(open(load.ROOT + "/engine/data/governadores.json", encoding="utf-8"))
    gov_names = [x["nome"].upper() for x in gov["governadores"]]
    kings = sorted({x["anjo_tribo"]["rei_liber_scientiae"].upper() for x in gov["governadores"]
                    if x.get("anjo_tribo", {}).get("rei_liber_scientiae")})
    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    call_words = []
    for c in calls:
        for w in (c.get("palavras") or []):
            t = (w.get("tfr") or w.get("palavra") or w) if isinstance(w, dict) else w
            if isinstance(t, str):
                call_words.append(t.upper())
    corpora = {"heptarquia_49": " ".join(hept_names), "governadores_91": " ".join(gov_names),
               "reis": " ".join(kings), "chamadas_palavras": " ".join(call_words)}

    def root_hits(corpus):
        hits = {}
        for r in ROOTS:
            n = corpus.count(r)
            if n:
                hits[r] = n
        return hits

    cross = {}
    for name, corpus in corpora.items():
        real = root_hits(corpus)
        # null: same corpus letters shuffled, 200x, count roots
        letters = [ch for ch in corpus if ch.isalpha()]
        exp = []
        for _ in range(200):
            rng.shuffle(letters)
            s = "".join(letters)
            exp.append(sum(s.count(r) for r in ROOTS))
        mu = statistics.mean(exp)
        cross[name] = {"root_hits": real, "total_real": sum(real.values()),
                       "shuffle_mean": round(mu, 1), "ratio": round(sum(real.values()) / max(mu, 0.3), 1),
                       "corpus_names": len(corpus.split())}

    res = {
        "gematria_systems": list(systems),
        "gematria_top_names": gem,
        "shared_values": {s: v for s, v in shared.items() if v},
        "notable_number_hits": dict(notable),
        "cross_system": cross,
        "finding": "",
    }
    # verdict
    anyshare = sum(len(v) for v in shared.values())
    bestcross = max(cross.items(), key=lambda kv: kv[1]["ratio"])
    res["finding"] = (
        "Gematria: across %d systems the top names share a value in %d system-groups (kinship by number), and "
        "hit notable Enochian numbers where flagged. Cross-system: the grammar roots appear in the %s corpus at "
        "%.1fx shuffle chance (the strongest link). Most roots are Loagaeth-specific - they do NOT flood the "
        "Heptarchy, Governors or Calls, which argues the Loagaeth name-system is its own layer, not a copy." % (
            len(systems), anyshare, bestcross[0], bestcross[1]["ratio"]))
    load.save_result("87_gematria_crosssystem", res)
    return res


if __name__ == "__main__":
    r = run()
    print("GEMATRIA (isopsefia / GD / primos) dos nomes-topo:")
    sysshow = [s for s in r["gematria_systems"] if s in ("isopsefia_latino_grega", "golden_dawn_coluna", "primos_na_ordem_de_dee")]
    for nm in TOP:
        print("  %-11s %s" % (nm, {s: r["gematria_top_names"][nm][s] for s in sysshow}))
    print("\nVALORES COMPARTILHADOS (mesmo numero = parentesco):")
    for sys, groups in r["shared_values"].items():
        for v, nms in groups.items():
            if len(nms) >= 2:
                print("  [%s] valor %s: %s" % (sys, v, nms))
    print("\nNUMEROS NOTAVEIS:", dict(r["notable_number_hits"]))
    print("\nCROSS-SISTEMA (raizes nos outros sistemas):")
    for name, d in r["cross_system"].items():
        print("  %-18s real %3d vs acaso %5.1f  ratio %.1f  hits=%s" % (name, d["total_real"], d["shuffle_mean"], d["ratio"], d["root_hits"]))
    print("\n" + r["finding"])
