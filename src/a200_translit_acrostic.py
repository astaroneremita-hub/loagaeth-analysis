# -*- coding: utf-8 -*-
"""a200 - two more Enochian lenses: Dee-alphabet transliteration, and acrostics.

TRANSLITERATION: maybe the Loag encodes names in the Enochian letter ORDER, not Latin.
Apply Dee's alphabet as a substitution to the grids, then search the canonical Tower names
(straight, 8 dirs). Two ciphers: dee_rank (Latin rank -> Dee-order letter) and atbash_dee
(first<->last in Dee order). HONEST NULL: does Dee's specific order beat RANDOM substitutions?
null = many random letter permutations applied to the same grids.

ACROSTICS: read first/last letters of rows, left column, and the main diagonal, concatenated
across the whole book into derived streams; search the names there (forward + reverse).
null = within-grid shuffle, rebuild streams.

Writes results/200_translit_acrostic.json. Seed 1583. stdlib only.
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import enoch
from a190_tower_traces import side_grids

SEED = 1583
DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
LATIN = "ABCDEFGHILMNOPQRSTUXZ"
DEE = "BCGDFAEMIHLPQNXORZUST"


def canonical():
    nm = enoch.derive_names()
    def grp(k):
        return "senior" if k.startswith("senior") else k
    out, seen = [], set()
    for n in nm:
        g = grp(n["kind"])
        if g in ("god name", "king", "senior") and n["name"] not in seen:
            seen.add(n["name"]); out.append(n["name"])
    return out


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


def apply_sub(grids, mapping):
    return [["".join(mapping.get(ch, ch) for ch in row) if isinstance(row, str) else
             [mapping.get(x, x) for x in row] for row in g] for g in grids]


def sub_grids(grids, mapping):
    out = []
    for g in grids:
        out.append(["".join(mapping.get(ch, ch) for ch in (row if isinstance(row, str) else "".join(row))) for row in g])
    return out


def count_found(words, grids):
    return sum(1 for w in words if search2d(w, grids))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(SEED)
    grids = [[ "".join(r) if not isinstance(r, str) else r for r in g] for g in side_grids().values()]
    names = canonical()
    result = {"seed": SEED, "n_names": len(names)}

    # ---------- transliteration ----------
    dee_rank = {LATIN[i]: DEE[i] for i in range(len(LATIN))}
    atbash = {DEE[i]: DEE[len(DEE) - 1 - i] for i in range(len(DEE))}
    ciphers = {"dee_rank": dee_rank, "atbash_dee": atbash, "identidade": {c: c for c in LATIN}}

    tr = {}
    for cname, cmap in ciphers.items():
        g2 = sub_grids(grids, cmap)
        obs = count_found(names, g2)
        tr[cname] = {"found": obs}
        print(f"[T] cifra {cname:12s} nomes achados {obs}/{len(names)}", flush=True)
    # null: random substitutions on the alphabet, applied to real grids
    TRIALS = 40
    sims = []
    letters = list(LATIN)
    for _ in range(TRIALS):
        perm = letters[:]; rng.shuffle(perm)
        rmap = {LATIN[i]: perm[i] for i in range(len(LATIN))}
        sims.append(count_found(names, sub_grids(grids, rmap)))
    m = sum(sims) / len(sims); sd = (sum((x - m) ** 2 for x in sims) / len(sims)) ** 0.5
    for cname in ("dee_rank", "atbash_dee"):
        z = (tr[cname]["found"] - m) / sd if sd else 0.0
        tr[cname].update({"rand_sub_mean": round(m, 2), "rand_sub_sd": round(sd, 2), "z": round(z, 2)})
    result["transliteration"] = tr
    print(f"[T] null substituicoes aleatorias: {m:.1f}±{sd:.1f}", flush=True)

    # ---------- acrostics ----------
    def streams_of(gs):
        row_first = "".join(g[r][0] for g in gs for r in range(len(g)))
        row_last = "".join(g[r][-1] for g in gs for r in range(len(g)))
        col_first = "".join(g[0][c] for g in gs for c in range(len(g[0])))
        diag = "".join(g[i][i] for g in gs for i in range(min(len(g), len(g[0]))))
        return {"primeira_letra_das_linhas": row_first, "ultima_letra_das_linhas": row_last,
                "primeira_letra_das_colunas": col_first, "diagonal_principal": diag}

    def in_stream(word, s):
        return (word in s) or (word[::-1] in s)

    streams = streams_of(grids)
    acro = {}
    for sname, s in streams.items():
        obs = sum(1 for w in names if in_stream(w, s))
        acro[sname] = {"len": len(s), "found": obs}
    # null for acrostics: shuffle each grid, rebuild
    A_TRIALS = 40
    accum = {k: [] for k in streams}
    for _ in range(A_TRIALS):
        sg = []
        for g in grids:
            flat = [ch for row in g for ch in row]; rng.shuffle(flat); W = len(g[0])
            sg.append(["".join(flat[i:i + W]) for i in range(0, len(flat), W)])
        st = streams_of(sg)
        for k, s in st.items():
            accum[k].append(sum(1 for w in names if in_stream(w, s)))
    for k in acro:
        arr = accum[k]; m = sum(arr) / len(arr); sd = (sum((x - m) ** 2 for x in arr) / len(arr)) ** 0.5
        z = (acro[k]["found"] - m) / sd if sd else 0.0
        acro[k].update({"null_mean": round(m, 2), "null_sd": round(sd, 2), "z": round(z, 2)})
        print(f"[A] {k:28s} achados {acro[k]['found']}/{len(names)}  null {m:.1f}±{sd:.1f}  z={z:+.2f}", flush=True)
    result["acrostics"] = acro

    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "200_translit_acrostic.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
