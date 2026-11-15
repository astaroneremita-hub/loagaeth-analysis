# -*- coding: utf-8 -*-
"""a215 - analysis E: does the U-register (tables 41-48) survive the n/u caveat?

a16/a36 found tables 41-48 shift A->U (a 'U register'); a36 ruled out A/U confusion in the
hand. The new caveat (images): n and u are mostly indistinguishable in Dee's hand. So the
U-register could be N misread as U. Test: if it were N->U confusion, N would drop by about
the U rise and A would be flat. Measure A/U/N shares in 2-40 vs 41-48.

Finding: A -13.05pp, U +8.04pp, N -1.13pp -> the U rise comes from A, not N; folding n+u does
NOT erase it. The U-register is A<->U, real, not an n/u transcription artifact.

stdlib only.
"""
import os
import sys
import json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import load


def shares(ns):
    c = Counter()
    for n in ns:
        c.update(load.table_text(n))
    tot = sum(c.values())
    return {L: 100 * c[L] / tot for L in "AUN"}, tot


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    early = [n for n in load.table_numbers() if 2 <= n <= 40]
    late = [n for n in load.table_numbers() if 41 <= n <= 48]
    se, te = shares(early); sl, tl = shares(late)
    delta = {L: round(sl[L] - se[L], 2) for L in "AUN"}
    result = {
        "early_2_40": {L: round(se[L], 2) for L in "AUN"}, "early_tot": te,
        "late_41_48": {L: round(sl[L], 2) for L in "AUN"}, "late_tot": tl,
        "delta_pp": delta,
        "UplusN_delta": round((sl["U"] + sl["N"]) - (se["U"] + se["N"]), 2),
        "AplusU_delta": round((sl["A"] + sl["U"]) - (se["A"] + se["U"]), 2),
        "verdict": "U-register real (A->U); N stable, so NOT an n/u artifact",
    }
    print(result, flush=True)
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "215_u_register_nu.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
