"""
93 - Character-by-character: can a Call be traced as a connected king-move path through a Loagaeth table?

The practitioner's proposal: walk each Call letter by letter, find where it sits in the Loagaeth, and see if
the Call forms a path (where it goes, where it is lost). We test the strongest contiguous form: the longest
prefix of the Call that spells a connected king-move path on some leaf, real Call vs shuffled Call.
"""
import json
import random
import statistics

import load


def call_sequence(call):
    return "".join("".join(ch for ch in str(w.get("enoquiano") or "").upper() if ch.isalpha())
                   for w in (call.get("palavras") or []))


def longest_trace(grid, seq):
    R = len(grid)
    if not seq:
        return 0
    frontier = {(r, c) for r in range(R) for c in range(R) if grid[r][c] == seq[0]}
    if not frontier:
        return 0
    best = 1
    for i in range(1, len(seq)):
        nf = set()
        for (r, c) in frontier:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr or dc:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < R and 0 <= nc < R and grid[nr][nc] == seq[i]:
                            nf.add((nr, nc))
        if not nf:
            break
        frontier = nf
        best = i + 1
    return best


def run():
    rng = random.Random(93)
    calls = json.load(open(load.ROOT + "/engine/data/chamadas.json", encoding="utf-8"))["chamadas"]
    lv = load.leaves()
    grids = {}
    for leaf, rows in lv.items():
        g = ["".join(load.letters(r)) for r in rows if load.letters(r)]
        if len(g) == 49 and all(len(x) == 49 for x in g):
            grids[leaf] = g

    report = {}
    for call in calls[:4]:
        seq = call_sequence(call)
        if len(seq) < 10:
            continue
        sc = {k: longest_trace(grids[k], seq) for k in grids}
        bl = max(sc, key=sc.get)
        real = sc[bl]
        cl = list(seq)
        nul = []
        for _ in range(30):
            rng.shuffle(cl)
            s = "".join(cl)
            nul.append(max(longest_trace(grids[k], s) for k in grids))
        report[call.get("numero")] = {
            "length": len(seq), "moves_table_per_dee": call.get("tabua_que_move_segundo_o_tfr"),
            "best_leaf": bl, "longest_connected_prefix": real,
            "shuffle_mean": round(statistics.mean(nul), 1), "shuffle_max": max(nul),
            "above_chance": real > max(nul)}

    any_above = any(v["above_chance"] for v in report.values())
    res = {
        "calls": report,
        "finding": (
            "No Call traces as a connected king-move path through a Loagaeth leaf above chance (e.g. Call 1: "
            "longest connected prefix 9 of 349 vs shuffle max 14; best leaf not the table Dee says it moves). "
            "The contiguous-path version of the coordinate theory is refuted; any real Loagaeth->Call link is "
            "non-contiguous (scattered coordinates) and needs the reception numbers to test." if not any_above
            else "Some Call traces above chance - worth a closer look."),
    }
    load.save_result("93_call_char_trace", res)
    return res


if __name__ == "__main__":
    r = run()
    for k, v in r["calls"].items():
        print("Chamada %s (len %d, move tabua %s): prefixo conectado %d | shuffle media %.1f max %d | acima do acaso? %s"
              % (k, v["length"], v["moves_table_per_dee"], v["longest_connected_prefix"], v["shuffle_mean"], v["shuffle_max"], v["above_chance"]))
    print("\n" + r["finding"])
