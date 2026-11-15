# -*- coding: utf-8 -*-
"""a198 - advanced fragment engine for every Watchtower name.

For each Tower name: break it into contiguous pieces of length k = 2,3,... up to the full
name. For each piece, how often and where it appears in the Loagaeth (straight, 8 dirs).
Then the patterns:
  - coverage curve per name: how many of its k-pieces appear, for each k (short all appear,
    long vanish - the fragmentation profile);
  - the LONGEST living piece of each name (the biggest contiguous chunk present);
  - shared pieces: k-grams that appear across MANY names (the common building blocks).

Fast: one pass over the grids emits every directed k-gram (k=2..8) that is a piece of SOME
name into a Counter + first location. Then per-name lookup is O(1).

Writes viz/fragments.json (compact) + results/198_fragment_engine.json (summary). stdlib only.
"""
import os
import sys
import json
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import enoch
from a190_tower_traces import side_grids

DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
KMAX = 8


def grp(k):
    return "senior" if k.startswith("senior") else k


def substrings(word, kmin=2):
    out = set()
    L = len(word)
    for k in range(kmin, L + 1):
        for i in range(0, L - k + 1):
            out.add(word[i:i + k])
    return out


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    sides = side_grids()
    names = enoch.derive_names()
    meta = {}
    for n in names:
        meta.setdefault(n["name"], {"group": grp(n["kind"]), "tower": n["tower"],
                                    "sub": n.get("sub"), "len": len(n["name"])})
    uniq = list(meta)

    # target set: every 2..8 substring of every name
    target = set()
    for nm in uniq:
        target |= substrings(nm, 2)
    print("names", len(uniq), "| alvos (substrings 2..8)", len(target), flush=True)

    # one pass: count every directed k-gram that is a target, + first location
    count = Counter()
    firstloc = {}   # gram -> [side, r, c, dir]
    sidescount = defaultdict(Counter)  # gram -> Counter(side)
    for side, g in sides.items():
        H = len(g); W = len(g[0])
        for r in range(H):
            for c in range(W):
                for di, (dr, dc) in enumerate(DIRS8):
                    # walk up to KMAX, break when out of bounds
                    s = []
                    rr, cc = r, c
                    for k in range(1, KMAX + 1):
                        if not (0 <= rr < H and 0 <= cc < W):
                            break
                        s.append(g[rr][cc])
                        if k >= 2:
                            gram = "".join(s)
                            if gram in target:
                                count[gram] += 1
                                sidescount[gram][side] += 1
                                if gram not in firstloc:
                                    firstloc[gram] = [side, r, c, di]
                        rr += dr; cc += dc
    print("grams achados", len(count), "de", len(target), flush=True)

    # per-name coverage + longest living piece
    name_rows = {}
    for nm in uniq:
        L = len(nm)
        cov = {}
        for k in range(2, L + 1):
            pieces = [nm[i:i + k] for i in range(0, L - k + 1)]
            appear = [p for p in pieces if count.get(p, 0) > 0]
            cov[k] = {"pieces": len(pieces), "appear": len(appear),
                      "occ": sum(count.get(p, 0) for p in appear)}
        # longest contiguous substring present
        longest = ""
        for k in range(L, 1, -1):
            found = None
            for i in range(0, L - k + 1):
                p = nm[i:i + k]
                if count.get(p, 0) > 0:
                    found = p; break
            if found:
                longest = found; break
        name_rows[nm] = {
            "group": meta[nm]["group"], "tower": meta[nm]["tower"], "sub": meta[nm]["sub"],
            "len": L, "cov": cov,
            "longest": longest, "longest_len": len(longest),
            "longest_occ": count.get(longest, 0) if longest else 0,
            "longest_loc": firstloc.get(longest) if longest else None,
        }

    # shared pieces: for k>=3, how many distinct names contain this piece AS A SUBSTRING,
    # among pieces that actually appear in the book
    piece_in_names = defaultdict(set)
    for nm in uniq:
        for p in substrings(nm, 3):
            if count.get(p, 0) > 0:
                piece_in_names[p].add(nm)
    shared = sorted(((p, len(s), count[p]) for p, s in piece_in_names.items()),
                    key=lambda x: (-x[1], -len(x[0])))
    top_shared = [{"piece": p, "names": nnames, "occ": occ} for p, nnames, occ in shared[:60]]

    # compact per-gram index for the screen (only appearing grams): count + nsides + firstloc
    gram_index = {gram: {"n": count[gram], "sides": len(sidescount[gram]),
                         "loc": firstloc[gram]} for gram in count}

    viz = {
        "grids": sides,
        "meta": meta,
        "names": name_rows,
        "grams": gram_index,
        "shared": top_shared,
        "group_pt": {"god name": "Nome de Deus", "king": "Rei", "senior": "Ancião",
                     "kerubic archangel": "Arcanjo querúbico", "kerub": "Querubim",
                     "calvary-flame": "Cruz (chama)", "calvary-command": "Cruz (comando)",
                     "lesser angel": "Anjo menor"},
        "dirs": DIRS8,
    }
    with open(os.path.join(os.path.dirname(HERE), "viz", "fragments.json"), "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)

    # summary to results (no grids)
    summary = {"test": "fragment coverage of Watchtower names in the Loagaeth",
               "n_names": len(uniq), "n_target_substrings": len(target),
               "n_appearing": len(count),
               "longest_by_group": {}, "top_shared": top_shared[:25]}
    bygroup = defaultdict(list)
    for nm, row in name_rows.items():
        bygroup[row["group"]].append(row["longest_len"])
    for g, arr in bygroup.items():
        summary["longest_by_group"][g] = {"max": max(arr), "mean": round(sum(arr) / len(arr), 2), "n": len(arr)}
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "198_fragment_engine.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=1)

    print("maior pedaço vivo por grupo:")
    for g in ["god name", "king", "senior", "kerubic archangel", "calvary-flame", "calvary-command", "kerub", "lesser angel"]:
        if g in summary["longest_by_group"]:
            s = summary["longest_by_group"][g]
            print(f"  {g:18s} max {s['max']}  media {s['mean']}  (n={s['n']})", flush=True)
    print("top pedaços compartilhados:", [(p['piece'], p['names']) for p in top_shared[:10]], flush=True)
    print("done", flush=True)


if __name__ == "__main__":
    main()
