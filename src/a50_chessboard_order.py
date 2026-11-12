"""
50 - Leaves 25b-28b: in which order do the diagonals of a colour follow one another?

Module a37 fixed, for each chessboard colour of these seven leaves, the road of each line (rows for
some top rows, a diagonal direction for the rest). Module a49 showed that elsewhere in the book the
lines of a side are one stream: the end of a line tells the start of the next. That gives a way to
order the diagonals: for each colour and block, read the lines in the stored order and in the
opposite order, and ask which order makes the end of a line predict the start of the following one
(letter model of the row-written tables, three letters of context), against the lines in random
order.

A block is called "forwards" or "backwards" when one order reaches z >= 2.5 and beats the other by
1.5; otherwise it stays unsettled. The decision is then checked with two signs it did not use:
the same letter on both sides of a junction (the book avoids it), and catalogue names split between
two lines. The same checks are run on the rejected order as a control.

Writes data/loagaeth_chessboard_streams.json (lines of each block in reading order, with status).
"""
import json
import math
import os
import random
import statistics

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum

WORDS = {"↘": "down-right", "↖": "up-left", "↙": "down-left", "↗": "up-right", "→ rows": "rows, left to right"}
# stored order of the lines for each road (a37.read sorts by r-c for the two "diag" roads and by r+c for the two "anti" roads)
STORED = {"↘": "from the top-right corner to the bottom-left", "↖": "from the top-right corner to the bottom-left",
          "↙": "from the top-left corner to the bottom-right", "↗": "from the top-left corner to the bottom-right",
          "→ rows": "from the top row down"}


def names():
    d = json.load(open(os.path.join(load.RESULTS, "23_name_discovery.json"), encoding="utf-8"))["A_candidates"]["top"]
    return sorted({x["name"] for x in d} | {"CHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX", "OXAD", "CHADAX", "NACHO", "ANTANTOX", "GRADAX"})


def straddle(v, nm):
    k = 0
    for i in range(len(v) - 1):
        for n in nm:
            L = len(n)
            a = v[i][-(L - 1):]
            j = a + v[i + 1][:L - 1]
            p = j.find(n)
            while p >= 0:
                if p < len(a) < p + L:
                    k += 1
                p = j.find(n, p + 1)
    return k


def run():
    rng = random.Random(50)
    book = base_book()
    m = CharLM(3, alpha=0.1).fit([r for k, v in book.items() if 2 <= tnum(k) <= 24 for r in v if r])
    d = json.load(open(os.path.join(load.DATA, "loagaeth_mixed_decoded.json"), encoding="utf-8"))
    nm = names()

    def cost(a, b):
        ctx, t = a[-3:], 0.0
        for ch in b[:3]:
            t -= math.log2(m.prob(ctx, ch))
            ctx = ctx[1:] + ch
        return t

    def z_order(L):
        if len(L) < 6:
            return None
        real = statistics.mean(cost(L[i], L[i + 1]) for i in range(len(L) - 1))
        nul = []
        for _ in range(300):
            sh = L[:]
            rng.shuffle(sh)
            nul.append(statistics.mean(cost(sh[i], sh[i + 1]) for i in range(len(sh) - 1)))
        return round((statistics.mean(nul) - real) / (statistics.pstdev(nul) or 1e-9), 1)

    blocks, streams = [], {}
    for f in d["by_colour"]:
        for col in (0, 1):
            lines = [r for r in d["by_colour"][f][col]]
            lay = d["layout"][f][col]
            R = lay["rows_by_row"]
            zones = lay["zones"]
            parts = []
            if R:
                parts.append(("rows 1-%d" % R, "→ rows", lines[:R]))
                rest = lines[R:]
                parts.append(("rest" if len(zones) == 2 else "rest (several zones)", zones[1][1] if len(zones) == 2 else "mixed", rest))
            else:
                parts.append(("whole colour", zones[0][1], lines))
            for label, road, L in parts:
                L = [r for r in L if len(r) >= 6]
                zf, zb = z_order(L), z_order(L[::-1])
                if zf is None:
                    continue
                status = "forwards" if zf >= 2.5 and zf - zb >= 1.5 else "backwards" if zb >= 2.5 and zb - zf >= 1.5 else "unsettled"
                blocks.append({"leaf": f, "colour": col, "block": label, "road": WORDS.get(road, road), "lines": len(L),
                               "letters": sum(len(r) for r in L), "z_stored_order": zf, "z_opposite_order": zb, "order": status,
                               "stored_order_means": STORED.get(road, "")})
                streams.setdefault(f, []).append({"colour": col, "block": label, "road": WORDS.get(road, road), "order": status,
                                                  "lines": L[::-1] if status == "backwards" else L})

    def check(groups):
        same = sum(v[i][-1] == v[i + 1][0] for v in groups for i in range(len(v) - 1))
        st = sum(straddle(v, nm) for v in groups)
        ns, nt = [], []
        for _ in range(500):
            a = b = 0
            for v in groups:
                sh = v[:]
                rng.shuffle(sh)
                a += sum(sh[i][-1] == sh[i + 1][0] for i in range(len(sh) - 1))
                b += straddle(sh, nm)
            ns.append(a)
            nt.append(b)
        return {"junctions": sum(len(v) - 1 for v in groups),
                "same_letter_across_junction": {"count": same, "random_order": round(statistics.mean(ns), 1),
                                                "z": round((same - statistics.mean(ns)) / (statistics.pstdev(ns) or 1e-9), 1)},
                "names_split_between_lines": {"count": st, "random_order": round(statistics.mean(nt), 1),
                                              "z": round((st - statistics.mean(nt)) / (statistics.pstdev(nt) or 1e-9), 1)}}
    # pooled by road: one block alone is short (about 43 junctions), blocks that share a road can be added
    by_road = {}
    for b in blocks:
        if b["road"] in ("down-right", "up-left", "down-left", "up-right"):
            by_road.setdefault(b["road"], []).append(b)
    pooled = {}
    rule = {}
    for road, bs in by_road.items():
        zf = sum(b["z_stored_order"] for b in bs) / math.sqrt(len(bs))
        zb = sum(b["z_opposite_order"] for b in bs) / math.sqrt(len(bs))
        rule[road] = "forwards" if zf >= 2.5 and zf > zb else "backwards" if zb >= 2.5 and zb > zf else "unsettled"
        pooled[road] = {"blocks": len(bs), "z_stored_order_pooled": round(zf, 1), "z_opposite_order_pooled": round(zb, 1), "order": rule[road]}
    # check the rule on the blocks that did not settle alone (so the check is not the selection)
    by_rule, against = [], []
    for v in streams.values():
        for s in v:
            r = rule.get(s["road"], "unsettled")
            if s["order"] == "unsettled" and r != "unsettled":
                L = s["lines"][::-1] if r == "backwards" else s["lines"]
                by_rule.append(L)
                against.append(L[::-1])
                s["order_by_road_rule"] = r
    settled = [s["lines"] for v in streams.values() for s in v if s["order"] != "unsettled"]
    unsettled = [s["lines"] for v in streams.values() for s in v if s["order"] == "unsettled"]
    res = {"blocks": blocks,
           "settled_blocks": sum(1 for b in blocks if b["order"] != "unsettled"), "of": len(blocks),
           "letters_in_settled_blocks": sum(b["letters"] for b in blocks if b["order"] != "unsettled"),
           "letters_in_all_blocks": sum(b["letters"] for b in blocks),
           "check_in_the_chosen_order": check(settled) if settled else None,
           "control_in_the_rejected_order": check([v[::-1] for v in settled]) if settled else None,
           "unsettled_blocks_in_stored_order": check(unsettled) if unsettled else None,
           "pooled_by_road": pooled,
           "rule_checked_on_blocks_not_settled_alone": check(by_rule) if by_rule else None,
           "rule_reversed_on_the_same_blocks": check(against) if against else None}
    for v in streams.values():
        for s in v:
            if s["order"] == "unsettled" and s.get("order_by_road_rule") == "backwards":
                s["lines"] = s["lines"][::-1]
    with open(os.path.join(load.DATA, "loagaeth_chessboard_streams.json"), "w", encoding="utf-8") as fh:
        json.dump({"meta": {"description": "Leaves 25b-28b: lines of each colour block in reading order where the order is settled (module a50)."},
                   "leaves": streams}, fh, ensure_ascii=False, indent=0)
    load.save_result("50_chessboard_order", res)
    return res


if __name__ == "__main__":
    r = run()
    for b in r["blocks"]:
        print(b["leaf"], b["colour"], b["block"], "|", b["road"], "|", b["lines"], "lines", b["z_stored_order"], b["z_opposite_order"], b["order"])
    for k in ("settled_blocks", "of", "letters_in_settled_blocks", "letters_in_all_blocks", "check_in_the_chosen_order", "control_in_the_rejected_order", "unsettled_blocks_in_stored_order"):
        print(k, r[k])
