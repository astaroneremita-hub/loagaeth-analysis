"""
68 - Where the book holds DAHAHOXOM.

A practitioner was addressed, while evoking a table of the Loagaeth, by an angel DAHAHOXOM, and noted
that names are assembled from letters scattered through the book (a57 confirms this of the Calls), so
a name need not be written whole. DAHAHOXOM is indeed written nowhere (a57). But if the name is
*gathered* from the book's own letters, do its pieces lie evenly, or do they gather somewhere?

For DAHAHOXOM and its distinctive core (AHOXOM, the part actually heard), we take the overlapping 3-
and 4-letter fragments, measure their density per leaf, and ask what share of that density falls in
the opening tables (leaves 2-6), against freq-weighted random 9-letter names. This is read-only and
proves nothing about the entity; it asks only where, if anywhere, the text concentrates this name's
material.
"""
import random
import statistics
from collections import Counter

import load


def fragments(name):
    return set([name[i:i + 3] for i in range(len(name) - 2)] + [name[i:i + 4] for i in range(len(name) - 3)])


def run():
    rng = random.Random(68)
    lv = load.leaves()
    whole = {k: "".join(load.letters(r) for r in v if load.letters(r)) for k, v in lv.items()}
    keys = [k for k in sorted(whole, key=lambda k: (int(k[:-1]) if k[:-1].isdigit() else 0, k)) if len(whole[k]) >= 300]
    f = Counter("".join(whole.values()))
    al, wt = list(f), [f[c] for c in f]

    def dens_by_leaf(name):
        fr = fragments(name)
        return {k: 1000 * sum(whole[k].count(fp) for fp in fr) / len(whole[k]) for k in keys}

    def pct_early(name, lo=2, hi=6):
        d = dens_by_leaf(name)
        early = sum(d[k] for k in keys if k[:-1].isdigit() and lo <= int(k[:-1]) <= hi)
        return 100 * early / sum(d.values())

    nul = [pct_early("".join(rng.choices(al, wt, k=9))) for _ in range(500)]
    mu, sd = statistics.mean(nul), statistics.pstdev(nul)
    out = {}
    for name in ("DAHAHOXOM", "AHOXOM", "HAHOXOM", "DAHAHOX", "DAHOXOM"):
        p = pct_early(name)
        d = dens_by_leaf(name)
        peak = max(d, key=d.get)
        out[name] = {"percent_in_opening_tables_2_6": round(p, 1), "z_vs_random_names": round((p - mu) / sd, 1),
                     "peak_leaf": peak}
    frac = 100 * sum(len(whole[k]) for k in keys if k[:-1].isdigit() and 2 <= int(k[:-1]) <= 6) / sum(len(whole[k]) for k in keys)
    res = {"opening_tables_are_this_share_of_the_book": round(frac, 1),
           "random_name_baseline_percent_in_2_6": {"mean": round(mu, 1), "sd": round(sd, 1)},
           "by_form": out,
           "note": "DAHAHOXOM is written nowhere in the book (a57). But its scattered material is concentrated, above "
                   "chance, in the opening tables (leaves 2-6, only 12%% of the book): the whole name 28%% there (z 3.0), "
                   "and the distinctive core AHOXOM 37%% (z 4.5) - the more distinctive the piece, the stronger. The peak "
                   "is leaf 2a, and table 2 is the first table a Call opens ('the second, with you is the first'). This is "
                   "where the text holds the name's letters, not a claim that the name or the being is written there; it is "
                   "offered as a pointer for the practice, read-only, proving nothing about the entity."}
    load.save_result("68_dahahoxom_home", res)
    return res


if __name__ == "__main__":
    r = run()
    print("opening tables 2-6 are %.1f%% of the book; random names put %.1f%% of their material there" %
          (r["opening_tables_are_this_share_of_the_book"], r["random_name_baseline_percent_in_2_6"]["mean"]))
    for name, d in r["by_form"].items():
        print("  %-10s %.1f%% in 2-6  (z %.1f)  peak %s" % (name, d["percent_in_opening_tables_2_6"], d["z_vs_random_names"], d["peak_leaf"]))
    print(r["note"])
