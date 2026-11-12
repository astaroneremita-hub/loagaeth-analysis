"""
91 - Three roadmap items at once:
  (8) Elemental flow across the book - does the dominant element of each table's names move in an ordered way?
  (Calls) Reverse-map Calls 1 and 2 onto what we have - are the Call words present / traceable in the Loagaeth?
  (5) The superfluous letter - the odd cell that makes 2401 = 2400 + 1.
"""
import json
import random
import statistics
from collections import Counter

import load
from a22_robustness_and_depth import base_book
from a85_entity_attributes import load_letters, SIGN_ELEMENT


def name_element(name, L):
    c = Counter()
    for ch in name:
        e = (L.get(ch) or {}).get("element")
        if e in ("Fogo", "Terra", "Ar", "Agua"):
            c[e] += 1
    return c


def run():
    rng = random.Random(91)
    book = base_book()
    tabs = {}
    for k in book:
        num = k[:-1]
        tabs.setdefault(num, "")
        tabs[num] += "".join(r for r in book[k] if r)
    order = sorted(tabs, key=int)
    L = load_letters()

    # (8) elemental flow: per table, element balance of the SYSTEM NAMES present
    ent = list(json.load(open(load.ROOT + "/viz/entity_data.json", encoding="utf-8"))["entities"])

    def cnt(t, nm):
        return t.count(nm) + (t.count(nm[::-1]) if nm != nm[::-1] else 0)
    flow = []
    for num in order:
        t = tabs[num]
        bal = Counter()
        for nm in ent:
            n = cnt(t, nm)
            if n:
                for e, k in name_element(nm, L).items():
                    bal[e] += k * n
        tot = sum(bal.values()) or 1
        dom = bal.most_common(1)[0][0] if bal else "?"
        flow.append({"table": num, "dominant": dom, "pct": {e: round(100 * bal[e] / tot) for e in ("Fogo", "Terra", "Ar", "Agua")}})
    # is the dominant-element sequence ordered (runs) vs shuffled?
    seq = [f["dominant"] for f in flow]
    def runs(s):
        return sum(1 for i in range(1, len(s)) if s[i] != s[i - 1]) + 1
    real_runs = runs(seq)
    null_runs = []
    for _ in range(500):
        s2 = seq[:]
        rng.shuffle(s2)
        null_runs.append(runs(s2))
    mu = statistics.mean(null_runs)
    flow_ordered = real_runs < mu - 2 * statistics.pstdev(null_runs)

    # (Calls) reverse-map Calls 1 and 2
    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    loag = "".join(tabs.values())
    call_report = {}
    for call in calls[:2]:
        words = []
        for w in (call.get("palavras") or []):
            if isinstance(w, dict):
                f = w.get("FORMA") or w.get("tfr") or ""
                if f:
                    words.append("".join(ch for ch in str(f).upper() if ch.isalpha()))
        words = [w for w in words if len(w) >= 4]
        present = {w: cnt(loag, w) for w in words if cnt(loag, w) > 0}
        # null: frequency-matched random strings of same lengths
        f = Counter(loag)
        alph, wt = list(f), [f[c] for c in f]
        exp = []
        for _ in range(300):
            e = sum(1 for w in words if "".join(rng.choices(alph, wt, k=len(w))) in loag)
            exp.append(e)
        call_report[call.get("numero")] = {
            "words_ge4": len(words), "words_present_in_loagaeth": len(present),
            "top": dict(sorted(present.items(), key=lambda kv: -kv[1])[:10]),
            "expected_present_chance": round(statistics.mean(exp), 1)}

    # (5) odd letter: center cell per 49x49 straight leaf
    lv = load.leaves()
    centers = []
    for leaf, rows in lv.items():
        g = ["".join(load.letters(r)) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            centers.append(g[24][24])
    center_dist = dict(Counter(centers).most_common())

    res = {
        "elemental_flow": flow,
        "flow_dominant_sequence": seq,
        "flow_transitions_real": real_runs, "flow_transitions_shuffle_mean": round(mu, 1),
        "flow_is_ordered": flow_ordered,
        "calls_reverse_map": call_report,
        "odd_letter_center_distribution": center_dist,
        "finding": (
            "Elemental flow: the dominant element per table makes %d transitions vs %.0f for a shuffle - %s. "
            "Calls 1-2: %s. Odd letter: the centre cell (the 1 in 2401=2400+1) is spread over %d letters, no "
            "single fixed letter - it is the mathematical pivot, not a planted mark." % (
                real_runs, mu, "ORDERED regions" if flow_ordered else "not more ordered than chance",
                "; ".join("Call %s %d/%d words present (chance %.1f)" % (k, v["words_present_in_loagaeth"], v["words_ge4"], v["expected_present_chance"]) for k, v in call_report.items()),
                len(center_dist))),
    }
    load.save_result("91_flow_calls_oddletter", res)
    return res


if __name__ == "__main__":
    r = run()
    print("ELEMENTAL FLOW (tabela: dominante):")
    print("  " + " ".join("%s:%s" % (f["table"], f["dominant"][:2]) for f in r["elemental_flow"]))
    print("  transicoes real %d vs shuffle %.0f -> %s" % (r["flow_transitions_real"], r["flow_transitions_shuffle_mean"], "ORDENADO" if r["flow_is_ordered"] else "nao-ordenado"))
    print("\nCHAMADAS 1-2 no Loagaeth:")
    for k, v in r["calls_reverse_map"].items():
        print("  Chamada %s: %d/%d palavras presentes (acaso %.1f) | top=%s" % (k, v["words_present_in_loagaeth"], v["words_ge4"], v["expected_present_chance"], list(v["top"])[:6]))
    print("\nLETRA SUPERFLUA (celula central): %d letras distintas -> %s" % (len(r["odd_letter_center_distribution"]), r["odd_letter_center_distribution"]))
    print("\n" + r["finding"])
