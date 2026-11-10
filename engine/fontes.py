# -*- coding: utf-8 -*-
"""Loader for Dee's primary data collected under data/ (the engine's bundled sources).

Exposes, through one interface, the variants of the Great Table (Golden Dawn x the
1584 dictation x the 1587 recension), the 19 Calls with their text and numeric words,
the 91 governors, the Sigillum and the Enochian gematria value systems.

Each table is returned as a dict tower->grid 13x12 (0-based) of UPPERCASE letters;
a missing/illegible cell = "?". Tower ids: ar=Air, agua=Water, terra=Earth, fogo=Fire.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FE = os.path.join(HERE, "data")


def _load(name):
    return json.load(open(os.path.join(FE, name), encoding="utf-8"))


# tower names in Dee's JSON keys -> our ids
_TOWER_KEY = {"ORO": "ar", "MOR": "terra", "OIP": "fogo", "MPH": "agua",
              "ar": "ar", "agua": "agua", "terra": "terra", "fogo": "fogo"}


def _norm_grid(raw):
    g = [["?"] * 12 for _ in range(13)]
    for r in range(min(13, len(raw))):
        row = raw[r]
        for c in range(min(12, len(row))):
            v = row[c]
            g[r][c] = (v or "?").upper()[:1] if isinstance(v, str) else "?"
    return g


def dee_1584():
    """The 1584-dictation table (Cotton/Sloane reference grids). dict tower->grid."""
    d = _load("tabuas_dee1584.json")
    grades = d["grades_de_referencia"]["ditado_cotton_1584"]["grades"]
    return {_TOWER_KEY[k]: _norm_grid(v) for k, v in grades.items() if k in _TOWER_KEY}


def raphael_1587():
    """The 1587 reformed table (recension). dict tower->grid, from the per-source grids."""
    d = _load("tabuas_raphael1587.json")
    for key in ("grades_de_referencia", "grades_por_fonte"):
        blk = d.get(key, {})
        cand = blk
        if isinstance(blk, dict) and "grades" in blk:
            cand = blk["grades"]
        for sub in ([cand] + list(cand.values()) if isinstance(cand, dict) else []):
            if isinstance(sub, dict) and all(t in sub for t in ("ORO", "MOR", "OIP", "MPH")):
                return {_TOWER_KEY[k]: _norm_grid(v) for k, v in sub.items() if k in _TOWER_KEY}
    return {}


def calls():
    """The 19 Calls: list of dicts (number, name, Enochian text, words)."""
    return _load("chamadas.json")["chamadas"]


def call_numbers():
    """Numeric words of the Calls (cardinals) with the value Dee gives them."""
    return _load("numeros_nas_chamadas.json")


def governors():
    return _load("governadores.json")


def sigillum():
    return _load("sigillum.json")


def gematria_systems():
    """List of per-letter value systems (id, name, values, evidence grade)."""
    return _load("gematria_enoquiana.json")["c_sistemas_de_valores"]


def gematria_value_tables():
    """dict system_id -> {LETTER: value} to feed the gematria lab."""
    out = {}
    for s in gematria_systems():
        v = s.get("valores")
        if isinstance(v, dict) and v:
            out[s["id"]] = {k.upper(): n for k, n in v.items() if isinstance(n, (int, float))}
    return out


if __name__ == "__main__":
    import sys
    sys.stdout.reconfigure(encoding="utf-8")
    d84 = dee_1584()
    print("1584 towers:", list(d84))
    for el in d84:
        print(el, "".join(d84[el][6]))  # Spirit line
    print("Calls:", len(calls()))
    print("gematria systems with values:", list(gematria_value_tables()))
