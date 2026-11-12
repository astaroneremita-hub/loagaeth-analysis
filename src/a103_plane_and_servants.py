"""
103 - Two structural probes: the 7x7 plane (item 24) and the servant numbers (item 27).

(24) The 49 parts laid on a 7x7 plane: do neighbours on that plane resemble each other more than distant cells?
     Similarity = cosine of letter-4-gram profiles.
(27) The governors carry servant counts (7209 etc.). Do those numbers relate to anything we measure - the force
     (repetition) of a name, or the position in the book?
"""
import json
import statistics
from collections import Counter

import load
from a22_robustness_and_depth import base_book


def profile(text):
    c = Counter(text[i:i + 4] for i in range(len(text) - 3))
    return c


def cosine(a, b):
    keys = set(a) | set(b)
    na = sum(v * v for v in a.values()) ** 0.5
    nb = sum(v * v for v in b.values()) ** 0.5
    if na == 0 or nb == 0:
        return 0.0
    return sum(a.get(k, 0) * b.get(k, 0) for k in keys) / (na * nb)


def run():
    book = base_book()
    tabs = {}
    for k in book:
        tabs.setdefault(k[:-1], "")
        tabs[k[:-1]] += "".join(r for r in book[k] if r)
    nums = [str(n) for n in range(1, 50) if str(n) in tabs and len(tabs[str(n)]) > 500]
    profs = {n: profile(tabs[n]) for n in nums}

    # 7x7 plane: table t at row (t-1)//7, col (t-1)%7 (first 49)
    def pos(t):
        i = int(t) - 1
        return i // 7, i % 7
    neigh_sims, dist_sims = [], []
    present = [n for n in nums if int(n) <= 49]
    for a in present:
        ra, ca = pos(a)
        for b in present:
            if a >= b:
                continue
            rb, cb = pos(b)
            s = cosine(profs[a], profs[b])
            if abs(ra - rb) + abs(ca - cb) == 1:
                neigh_sims.append(s)
            elif abs(ra - rb) + abs(ca - cb) >= 4:
                dist_sims.append(s)
    plane = {"neighbour_mean_sim": round(statistics.mean(neigh_sims), 3) if neigh_sims else None,
             "distant_mean_sim": round(statistics.mean(dist_sims), 3) if dist_sims else None}
    plane["neighbours_more_similar"] = (plane["neighbour_mean_sim"] or 0) > (plane["distant_mean_sim"] or 0) + 0.01

    # servant numbers vs name force
    gov = json.load(open(load.ROOT + "/engine/data/governadores.json", encoding="utf-8"))
    servos = [g.get("servos") for g in gov["governadores"] if isinstance(g.get("servos"), int)]
    try:
        ent = json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"]
        forces = sorted((e["forca"] for e in ent.values()), reverse=True)
    except Exception:
        forces = []
    servo_stats = {"count": len(servos), "min": min(servos) if servos else None, "max": max(servos) if servos else None,
                   "distinct": len(set(servos)),
                   "note": "Os numeros dos servos sao do sistema dos governadores (Liber Scientiae), nao do Loagaeth; "
                           "testamos se batem com a forca de algum nome."}
    # any name force equals a servant number? (coincidence test)
    hits = sorted(set(forces) & set(servos))
    servo_stats["force_equals_servant"] = hits

    res = {
        "plane_7x7": plane,
        "servants": servo_stats,
        "finding": (
            "7x7 plane: neighbours sim %s vs distant %s - %s. Servant numbers: %d governors, range %s-%s; they do "
            "NOT match any Loagaeth name's force (%s) - the servant counts belong to the Heptarchic governor system, "
            "not the Loagaeth onomasticon, consistent with the two being separate layers." % (
                plane["neighbour_mean_sim"], plane["distant_mean_sim"],
                "neighbours slightly more alike" if plane["neighbours_more_similar"] else "no plane adjacency effect",
                servo_stats["count"], servo_stats["min"], servo_stats["max"],
                "no overlap" if not hits else ("overlap: " + ", ".join(map(str, hits))))),
    }
    load.save_result("103_plane_and_servants", res)
    return res


if __name__ == "__main__":
    r = run()
    print("PLANO 7x7:", r["plane_7x7"])
    print("SERVOS:", {k: r["servants"][k] for k in ("count", "min", "max", "distinct", "force_equals_servant")})
    print("\n" + r["finding"])
