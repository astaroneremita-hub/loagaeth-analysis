# -*- coding: utf-8 -*-
"""a193 - Do the Watchtower angels' element/power match WHERE they fall in the book?

Two honest tests on the found straight-line traces:

A) ELEMENT-MATCH: each angel carries a Tower element (ar/agua/terra/fogo). Each Loagaeth
   folha has a dominant element (from the book's own letter->element profile, pilha_data).
   Does an angel land on a folha of its own element more than chance? Null = the SAME
   names searched in each folha's own letters shuffled (preserves letter frequency), so a
   positive result means the real arrangement aligns angel-element to folha-element beyond
   what the letter mix alone gives.

B) DEEP DECLINE: the user noticed names thin out toward the end. Measure traces-per-folha
   for shallow (2-25) vs deep (26-48), observed vs the within-folha shuffle null. If the
   decline just matches the null, the names thin because the letter mix changes (entropy up),
   not because angels were placed; if it declines MORE than null, something beyond letters.

Honest by construction: names ARE there as straight lines; these tests ask whether their
PLACEMENT carries the angels' meaning, or is a by-product of the letters.

Writes results/193_power_position.json and viz/power_position.json. stdlib only. Seed 1583.
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
import enoch
from a190_tower_traces import side_grids, search_all

SEED = 1583
TRIALS = 60
TOWER_ELEM = {"ar": "Ar", "agua": "Agua", "terra": "Terra", "fogo": "Fogo"}


def folha_elements():
    """{folha_int: dominant element label} from the book's own elemental profile."""
    d = json.load(open(os.path.join(os.path.dirname(HERE), "viz", "pilha_data.json"), encoding="utf-8"))
    out = {}
    for row in d:
        el = row.get("elem") or {}
        if el:
            out[row["f"]] = max(el, key=el.get)
    return out


def side_to_folha(side):
    return int("".join(ch for ch in side if ch.isdigit()))


def find_positions(grids, strings):
    """{string: folha_int or None} first straight-line hit."""
    pos = {}
    for s in strings:
        hit = search_all(s, grids)
        pos[s] = side_to_folha(hit[0]) if hit else None
    return pos


def shuffled(grid, rng):
    flat = [ch for row in grid for ch in row]
    rng.shuffle(flat)
    W = len(grid[0])
    return ["".join(flat[i:i + W]) for i in range(0, len(flat), W)]


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    grids = side_grids()
    felem = folha_elements()
    names = enoch.derive_names()  # 456 tower-tagged entries (duplicates across towers kept)
    uniq = sorted(set(n["name"] for n in names))

    # observed positions
    obs_pos = find_positions(grids, uniq)

    # ---- Test A: element match ----
    def match_rate(pos):
        hit = 0
        tot = 0
        for n in names:
            f = pos.get(n["name"])
            if f is None or f not in felem:
                continue
            tot += 1
            if felem[f] == TOWER_ELEM[n["tower"]]:
                hit += 1
        return hit, tot

    obs_hit, obs_tot = match_rate(obs_pos)
    obs_rate = obs_hit / obs_tot if obs_tot else 0

    # ---- Test B: deep decline (traces per folha band) ----
    def band_counts(pos):
        shallow = deep = 0
        for n in names:
            f = pos.get(n["name"])
            if f is None:
                continue
            if 2 <= f <= 25:
                shallow += 1
            elif 26 <= f <= 48:
                deep += 1
        return shallow, deep

    obs_sh, obs_dp = band_counts(obs_pos)

    # per-folha observed trace count (distinct tower-tagged entries)
    perfolha = {}
    for n in names:
        f = obs_pos.get(n["name"])
        if f is not None:
            perfolha[f] = perfolha.get(f, 0) + 1

    # ---- null: within-folha shuffle ----
    rng = random.Random(SEED)
    rates, declines, shs, dps = [], [], [], []
    for t in range(TRIALS):
        sg = {k: shuffled(g, rng) for k, g in grids.items()}
        pos = find_positions(sg, uniq)
        h, tt = match_rate(pos)
        rates.append(h / tt if tt else 0)
        s, d = band_counts(pos)
        shs.append(s)
        dps.append(d)
        declines.append((s - d))  # shallow minus deep
        print(f"trial {t+1}/{TRIALS} rate={rates[-1]:.3f} shallow={s} deep={d}", flush=True)

    def z(obs, arr):
        m = sum(arr) / len(arr)
        sd = (sum((x - m) ** 2 for x in arr) / len(arr)) ** 0.5
        return m, sd, ((obs - m) / sd if sd else 0.0)

    mA, sA, zA = z(obs_rate, rates)
    obs_decl = obs_sh - obs_dp
    mD, sD, zD = z(obs_decl, declines)
    mSh, _, _ = z(obs_sh, shs)
    mDp, _, _ = z(obs_dp, dps)

    verdictA = "REAL" if zA > 3 else ("ANTI" if zA < -3 else "REFUTADO")
    # decline beyond letters: observed shallow-deep gap bigger than null gap
    verdictB = "REAL (além das letras)" if zD > 3 else "DESCRITIVO (= mistura de letras)"

    result = {
        "test": "Watchtower angel element/power vs position in the Loagaeth",
        "seed": SEED, "trials": TRIALS,
        "A_element_match": {
            "observed_rate": round(obs_rate, 4), "matches": obs_hit, "placed": obs_tot,
            "null_mean": round(mA, 4), "null_sd": round(sA, 4), "z": round(zA, 2),
            "chance_baseline": 0.25, "verdict": verdictA,
        },
        "B_deep_decline": {
            "obs_shallow_2_25": obs_sh, "obs_deep_26_48": obs_dp,
            "obs_gap": obs_decl, "null_gap_mean": round(mD, 2), "null_gap_sd": round(sD, 2),
            "z_gap": round(zD, 2),
            "null_shallow_mean": round(mSh, 1), "null_deep_mean": round(mDp, 1),
            "verdict": verdictB,
        },
    }
    load.save_result("193_power_position", result)

    viz = {
        "perfolha": perfolha,
        "folha_elem": felem,
        "tower_elem": TOWER_ELEM,
        "A": result["A_element_match"],
        "B": result["B_deep_decline"],
    }
    with open(os.path.join(os.path.dirname(HERE), "viz", "power_position.json"), "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)

    print("\n=== A element-match ===")
    print(f"observed {obs_rate:.3f} ({obs_hit}/{obs_tot}) vs null {mA:.3f}+-{sA:.3f}  z={zA:+.2f}  [{verdictA}]  chance=0.25")
    print("=== B deep decline ===")
    print(f"shallow(2-25)={obs_sh} deep(26-48)={obs_dp} | null shallow~{mSh:.0f} deep~{mDp:.0f} | gap z={zD:+.2f}  [{verdictB}]")


if __name__ == "__main__":
    main()
