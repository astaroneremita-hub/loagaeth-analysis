"""
75 - Row stratification: is every line a balanced inventory of the alphabet?

Chased down from a74. Under a small ordinal value-map the row-sums of a leaf are far more uniform than
any shuffle of its own letters - and that survives a column-preserving shuffle too. The cause is not
arithmetic and not column grammar: each LETTER is spread across the 49 rows more evenly than chance
(sub-Poisson, anti-clumped), so every row carries a near-equal share of every letter - a balanced
inventory. This asks whether that is real, whether it holds for consonants (not just the vowels that
the known ~constant-syllables-per-line metre would already even out), and how strong it is.

Metric per leaf: index of dispersion D = variance/mean of a letter's 49 per-row counts, averaged over
letters (common letters only). D < 1 = regular/stratified, D = 1 = Poisson (what a random scatter gives).
Null: 200 full shuffles of the leaf's own letters (same multiset, same row lengths). z = (D_real - D_shuf)/sd.
Reported for ALL letters, VOWELS only, CONSONANTS only. Consonant stratification = a rule beyond metre.
"""
import random
import statistics

import load

VOWELS = set("AEIOU")


def dispersion(rows, subset=None):
    alph = set("".join(rows))
    if subset:
        alph &= subset
    ds = []
    for ch in alph:
        counts = [row.count(ch) for row in rows]
        tot = sum(counts)
        if tot >= 49:  # common enough for the statistic to mean something
            m = statistics.mean(counts)
            ds.append(statistics.pvariance(counts) / (m if m else 1))
    return statistics.mean(ds) if ds else None


def shuffle_leaf(grid, rng):
    flat = [ch for row in grid for ch in row]
    rng.shuffle(flat)
    out, i = [], 0
    for row in grid:
        out.append("".join(flat[i:i + len(row)]))
        i += len(row)
    return out


def run():
    rng = random.Random(75)
    lv = load.leaves()
    grids = {}
    for leaf, rows in lv.items():
        g = [load.letters(r) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            grids[leaf] = ["".join(r) for r in g]

    cons = set("BCDFGHLMNPQRSTXZ")
    per = {}
    for leaf, rows in grids.items():
        real = {k: dispersion(rows, s) for k, s in (("all", None), ("vowels", VOWELS), ("cons", cons))}
        nul = {"all": [], "vowels": [], "cons": []}
        for _ in range(200):
            sg = shuffle_leaf([list(r) for r in rows], rng)
            for k, s in (("all", None), ("vowels", VOWELS), ("cons", cons)):
                d = dispersion(sg, s)
                if d is not None:
                    nul[k].append(d)
        row = {}
        for k in real:
            if real[k] is None or not nul[k]:
                continue
            mu, sd = statistics.mean(nul[k]), (statistics.pstdev(nul[k]) or 1e-9)
            row[k] = {"real": round(real[k], 3), "shuffle": round(mu, 3),
                      "ratio": round(real[k] / mu, 2), "z": round((real[k] - mu) / sd, 1)}
        per[leaf] = row

    def agg(k, field):
        xs = [per[l][k][field] for l in per if k in per[l]]
        return round(statistics.mean(xs), 2)

    summary = {k: {"mean_ratio": agg(k, "ratio"), "mean_z": agg(k, "z"),
                   "leaves_z_lt_-3": sum(1 for l in per if k in per[l] and per[l][k]["z"] < -3)}
               for k in ("all", "vowels", "cons")}

    cz = summary["cons"]["mean_z"]
    strong = cz < -3 and summary["cons"]["mean_ratio"] < 0.85
    verdict = (
        "CONFIRMADO NOVO: every line is a balanced inventory of the alphabet - each letter, consonants "
        "included, is spread across the 49 rows far more evenly than chance (sub-Poisson). This is a "
        "global compositional rule beyond the known metre, the no-doubling rule and the positional "
        "grammar; a plain shuffle of the same letters does not reproduce it."
        if strong else
        "the row-evenness is weak or confined to vowels (metre), not a general rule.")
    res = {
        "leaves": len(grids), "shuffles_per_leaf": 200,
        "summary": summary,
        "note": "index of dispersion D = var/mean of each letter's 49 per-row counts; D<1 regular, D=1 "
                "Poisson. ratio = D_real / D_shuffle. z over shuffles; strongly negative = stratified.",
        "conclusion": "%s Consonants: ratio %.2f, z %.1f over %d leaves (vowels ratio %.2f; all %.2f)." % (
            verdict, summary["cons"]["mean_ratio"], cz, len(grids),
            summary["vowels"]["mean_ratio"], summary["all"]["mean_ratio"]),
        "per_leaf": per,
    }
    load.save_result("75_row_stratification", res)
    return res


if __name__ == "__main__":
    r = run()
    for k in ("all", "vowels", "cons"):
        s = r["summary"][k]
        print("%-6s ratio %.2f | z %6.1f | leaves z<-3: %d" % (k, s["mean_ratio"], s["mean_z"], s["leaves_z_lt_-3"]))
    print("\n" + r["conclusion"])
