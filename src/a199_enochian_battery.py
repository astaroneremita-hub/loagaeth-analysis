# -*- coding: utf-8 -*-
"""a199 - broad Enochian/human hypothesis battery. Try everything, report each lens.

A) ELS (equidistant letter sequence, "Torah-code" / the way governors are read by SKIP
   paths): each canonical Tower name sought in the book's linear stream at constant skip
   d = 1..26, forward AND reverse. observed vs null (shuffled stream).
B) OTHER ENOCHIAN SYSTEMS in the Loag (straight, 8 dirs): 91 Governors, 30 Aethyrs, 49
   Tabula Collecta names. observed vs null.
C) GEMATRIA: Enochian letter values of each canonical name (exposed for operation), and a
   light test: do name-values coincide with per-folha letter-value totals?

Reports each hypothesis from both lenses. Writes results/199_enochian_battery.json.
Seed 1583. stdlib only.
"""
import os
import sys
import json
import random
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
import enoch
from a190_tower_traces import side_grids

SEED = 1583
DATA = os.path.join(os.path.dirname(HERE), "engine", "data")
DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


def canonical_names():
    nm = enoch.derive_names()
    def grp(k):
        return "senior" if k.startswith("senior") else k
    out = []
    seen = set()
    for n in nm:
        g = grp(n["kind"])
        if g in ("god name", "king", "senior") and n["name"] not in seen:
            seen.add(n["name"]); out.append((n["name"], g))
    return out


def els_found(word, S, pos0, N, maxskip):
    """True if word appears as equidistant letters at some skip 1..maxskip (forward)."""
    W = word
    L = len(W)
    for d in range(1, maxskip + 1):
        for i in pos0:
            end = i + d * (L - 1)
            if end >= N:
                break
            ok = True
            for k in range(1, L):
                if S[i + d * k] != W[k]:
                    ok = False; break
            if ok:
                return True
    return False


def els_any(word, S, idx, N, maxskip):
    pos0 = idx.get(word[0], [])
    if els_found(word, S, pos0, N, maxskip):
        return True
    rw = word[::-1]
    return els_found(rw, S, idx.get(rw[0], []), N, maxskip)


def search2d(word, grids):
    W = word.upper(); L = len(W)
    for g in grids:
        H = len(g); Wd = len(g[0])
        for r in range(H):
            for c in range(Wd):
                if g[r][c] != W[0]:
                    continue
                for dr, dc in DIRS8:
                    er, ec = r + dr * (L - 1), c + dc * (L - 1)
                    if 0 <= er < H and 0 <= ec < Wd and all(g[r + dr * i][c + dc * i] == W[i] for i in range(L)):
                        return True
    return False


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(SEED)
    result = {"seed": SEED}

    # ---------- A: ELS ----------
    S = load.dense_stream()
    N = len(S)
    idx = defaultdict(list)
    for i, ch in enumerate(S):
        idx[ch].append(i)
    names = canonical_names()
    MAXSKIP = 26
    print(f"[A] ELS stream={N} letras, {len(names)} nomes canônicos, skip 1..{MAXSKIP}", flush=True)

    def els_count(nmlist, stream, index):
        return sum(1 for (w, g) in nmlist if els_any(w, stream, index, len(stream), MAXSKIP))

    obsA = {}
    for g in ("god name", "king", "senior"):
        sub = [(w, gg) for (w, gg) in names if gg == g]
        obsA[g] = sum(1 for (w, _) in sub if els_any(w, S, idx, N, MAXSKIP))
    obs_total = sum(obsA.values())
    TRIALS_A = 12
    sims = []
    for t in range(TRIALS_A):
        sh = list(S); rng.shuffle(sh); sh = "".join(sh)
        sidx = defaultdict(list)
        for i, ch in enumerate(sh):
            sidx[ch].append(i)
        sims.append(els_count(names, sh, sidx))
        print(f"[A] null {t+1}/{TRIALS_A} = {sims[-1]}", flush=True)
    m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
    z = (obs_total - m) / sd if sd else 0.0
    result["A_ELS"] = {"maxskip": MAXSKIP, "by_group": obsA, "found_total": obs_total,
                       "n_names": len(names), "null_mean": round(m, 2), "null_sd": round(sd, 2),
                       "z": round(z, 2)}
    print(f"[A] ELS found {obs_total}/{len(names)}  (deus {obsA['god name']}, rei {obsA['king']}, ancião {obsA['senior']})  null {m:.1f}±{sd:.1f} z={z:+.2f}", flush=True)

    # ---------- B: other Enochian systems (2D straight 8) ----------
    grids = list(side_grids().values())
    gov = json.load(open(os.path.join(DATA, "governadores.json"), encoding="utf-8"))
    hept = json.load(open(os.path.join(DATA, "heptarquia.json"), encoding="utf-8"))
    governors = sorted(set((x.get("nome") or "").upper() for x in gov["governadores"] if x.get("nome")))
    aethyrs = sorted(set((x.get("nome_dee_confirmado_em_fonte_primaria") or x.get("nome_crowley_1911") or "").upper()
                         for x in gov["aethyrs"]))
    collecta = sorted(set((x.get("nome") or "").upper() for x in hept["tabula_collecta"]["nomes"] if x.get("nome")))
    systems = {"governadores (91)": governors, "aethyrs (30)": aethyrs, "tabula_collecta (49)": collecta}

    def count2d(words, gs):
        return sum(1 for w in words if len(w) >= 2 and search2d(w, gs))

    def shuffled_grid(grid):
        flat = [ch for row in grid for ch in row]; rng.shuffle(flat); Wd = len(grid[0])
        return ["".join(flat[i:i + Wd]) for i in range(0, len(flat), Wd)]

    TRIALS_B = 20
    result["B_systems"] = {}
    for sysname, words in systems.items():
        words = [w for w in words if len(w) >= 2]
        obs = count2d(words, grids)
        sims = []
        for _ in range(TRIALS_B):
            sg = [shuffled_grid(g) for g in grids]
            sims.append(count2d(words, sg))
        m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
        z = (obs - m) / sd if sd else 0.0
        result["B_systems"][sysname] = {"n": len(words), "found": obs, "null_mean": round(m, 2),
                                        "null_sd": round(sd, 2), "z": round(z, 2),
                                        "lens": [len(w) for w in words[:0]]}
        print(f"[B] {sysname:22s} found {obs:3d}/{len(words):3d}  null {m:5.1f}±{sd:4.1f}  z={z:+.2f}", flush=True)

    # ---------- C: gematria values of canonical names ----------
    gem = json.load(open(os.path.join(DATA, "gematria_enoquiana.json"), encoding="utf-8"))
    # find a letter->value map inside the structure
    valmap = {}
    def dig(o):
        if isinstance(o, dict):
            # heuristic: dict with single-letter keys mapping to ints
            if o and all(len(str(k)) == 1 and isinstance(v, (int, float)) for k, v in o.items()):
                for k, v in o.items():
                    valmap.setdefault(k.upper(), v)
            for v in o.values():
                dig(v)
        elif isinstance(o, list):
            for v in o:
                dig(v)
    dig(gem)
    gematria = None
    if valmap:
        gematria = {w: sum(valmap.get(ch, 0) for ch in w) for (w, g) in names}
    result["C_gematria"] = {"have_values": bool(valmap), "values_sample": dict(list(valmap.items())[:10]),
                            "name_values": gematria}
    print(f"[C] gematria letras achadas: {len(valmap)}  (ex {dict(list(valmap.items())[:6])})", flush=True)

    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "199_enochian_battery.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
