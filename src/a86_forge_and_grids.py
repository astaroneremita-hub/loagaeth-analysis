"""
86 - Data for two tools: the name-forge (inverse generator) and the table viewer (names on the grid).

Exports:
  viz/forge_data.json  - affix profiles (each prefix/suffix: its element push, typical force, attestations)
                         + roots + the attested names, so a page can filter by desired element/force and
                         return the prefixes/infixes that build such a name.
  viz/table_grids.json - every 49x49 leaf as rows + the positions (row, col, len) of each system-name on it,
                         so a page can light the names up on the original table.
Also reports the size of the name space.
"""
import json
from collections import Counter, defaultdict

import load
from a85_entity_attributes import load_letters, SIGN_ELEMENT

ROOTS = ["NOCHA", "NACHO", "GETH", "CHASTOR", "CHADAX", "ACLAX", "ANZACH", "GRADAX", "ANTANTOX", "PHANGE"]
PRE = ["AD", "AL", "I", "NO", "NE", "ZI", "AX", "A", "AN", "DN"]
SUF = ["P", "PH", "STOR", "TO", "TOR", "A", "AL", "AD", "AX", "OR", "AN"]


def elem_of_string(s, L):
    c = Counter()
    for ch in s:
        e = L.get(ch, {}).get("element")
        if e in ("Fogo", "Terra", "Ar", "Agua"):
            c[e] += 1
    return c


def run():
    L = load_letters()
    ent = json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"]

    # derive prefix/suffix for every entity from its root
    def split_root(nm):
        cand = [(len(r), r) for r in ROOTS if r in nm]
        if not cand:
            return None, "", ""
        r = max(cand)[1]
        i = nm.index(r)
        return r, nm[:i], nm[i + len(r):]
    for n, e in ent.items():
        rt, pre, suf = split_root(n)
        e["_pre"], e["_suf"] = pre, suf

    # affix profiles: element the affix's own letters add, and mean force/potencia of names using it
    def affix_profile(affix, side):
        add = elem_of_string(affix, L)
        dom = add.most_common(1)[0][0] if add else "?"
        users = [n for n, e in ent.items()
                 if (e["_pre"] == affix if side == "pre" else e["_suf"] == affix)]
        forcas = [ent[n]["forca"] for n in users]
        return {"affix": affix, "side": side, "adds_element": dom, "element_counts": dict(add),
                "used_by": len(users), "mean_force": round(sum(forcas) / len(forcas)) if forcas else 0,
                "examples": sorted(users, key=lambda n: -ent[n]["forca"])[:4]}

    prefixes = [affix_profile(a, "pre") for a in PRE]
    suffixes = [affix_profile(a, "suf") for a in SUF]

    # roots with their base element + force
    roots = []
    for r in ROOTS:
        e = ent.get(r, {})
        roots.append({"root": r, "element": e.get("elemento", "?"), "force": e.get("forca", 0)})

    # name space size
    space = len(ROOTS) * (1 + len(PRE)) * (1 + len(SUF))  # depth-1 combos
    space2 = space * (1 + len(SUF))  # allow a second suffix layer (recursion)
    attested = len(ent)

    forge = {
        "roots": roots, "prefixes": prefixes, "suffixes": suffixes,
        "elements": ["Fogo", "Terra", "Ar", "Agua"],
        "name_space_depth1": space, "name_space_depth2": space2, "attested_names": attested,
        "entities": {n: {"forca": e["forca"], "elemento": e["elemento"], "potencia": e["potencia"],
                         "classe": e["classe"], "raiz": e.get("raiz"),
                         "prefix": e["_pre"], "suffix": e["_suf"]} for n, e in ent.items()},
    }
    with open(load.ROOT + "/viz/forge_data.json", "w", encoding="utf-8") as f:
        json.dump(forge, f, ensure_ascii=False)

    # table grids + name positions
    lv = load.leaves()
    grids = {}
    for leaf, rows in lv.items():
        g = ["".join(load.letters(r)) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            grids[leaf] = g
    order = sorted(grids, key=lambda k: (int(k[:-1]), k[-1]))
    names = sorted(ent, key=lambda n: -len(n))  # longer first so highlights prefer the fuller name
    table_out = {}
    for leaf in order:
        g = grids[leaf]
        occ = []
        for r in range(49):
            row = g[r]
            for nm in names:
                start = 0
                while True:
                    i = row.find(nm, start)
                    if i < 0:
                        break
                    occ.append({"name": nm, "row": r, "col": i, "len": len(nm),
                                "element": ent[nm]["elemento"]})
                    start = i + 1
        table_out[leaf] = {"grid": g, "names": occ, "distinct": len({o["name"] for o in occ})}
    with open(load.ROOT + "/viz/table_grids.json", "w", encoding="utf-8") as f:
        json.dump({"order": order, "leaves": table_out}, f, ensure_ascii=False)

    res = {"name_space_depth1": space, "name_space_depth2": space2, "attested_names": attested,
           "tables_exported": len(order),
           "note": "name space counts root x (1+prefixes) x (1+suffixes); attested = names actually found >=3x."}
    load.save_result("86_forge_and_grids", res)
    return res, forge


if __name__ == "__main__":
    res, forge = run()
    print("name space (1 afixo cada lado): %d combinacoes | com 2a camada: %d | atestados no livro: %d" % (
        res["name_space_depth1"], res["name_space_depth2"], res["attested_names"]))
    print("tabelas exportadas:", res["tables_exported"])
    print("\nprefixos (elemento que adicionam | forca media | usados por):")
    for p in forge["prefixes"]:
        print("  %-3s +%-6s forca~%-4d  n=%d  ex=%s" % (p["affix"], p["adds_element"], p["mean_force"], p["used_by"], p["examples"][:3]))
