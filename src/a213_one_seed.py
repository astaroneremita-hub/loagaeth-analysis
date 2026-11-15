# -*- coding: utf-8 -*-
"""a213 - analysis B: is there ONE seed for all names? ("they are but one Name")

The 49 recurring names (a23) fall in 7 families, each a core + measured affixes (prefix,
suffix, A<->O). Those rules DO NOT change the consonant skeleton, so 7 distinct cores
can't share one seed by them alone. a28 measured a deeper rule: consonants that interchange
share MANNER of articulation. Does adding that rule collapse the 49 names to one (or few)
generating seed(s)?

Method: reduce each name to its consonant skeleton (collapse doubles). Union two names when
one skeleton is a prefix/suffix extension of the other (affix), OR they differ by a single
consonant within the same manner class (measured mutation), OR equal after A<->O (already
vowel-free). Count connected components = number of independent seeds. Compare to a null of
49 surrogate names (same length distribution, letters by the book's frequency).

stdlib only. seed 1583.
"""
import os
import sys
import json
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

NAMES = ['NACHO','NOCHAP','NOCHASTOR','NOCHAPH','ADNOCHAP','ACLAXTO','GRADAX','AXALGRA','NACHOA',
 'NOCHASTORA','ICHASTOR','PHANGE','ANTANTOX','VOXAR','DNOCHAPA','TAXALGRA','NECHASTOR','DRAGRA',
 'ACLAXTOR','ICHASTORA','NACHOAL','ADNOCHAPHA','RONZIN','ZICHASTOR','ANCHANO','NADAB','CHARDAX',
 'AXACHAR','NACHOAD','ADNACHEPHA','ZIDNOPHA','PHADOL','AOXARD','ALCHADAX','AXTALGETHA','AXACLAXTO',
 'HNAXAD','ANTANTOXAL','OXARDRAH','OLCHADNA','NACLANSA','ACHADNACHO','DONCHAL','ACHARDAN','CHIDAXTO',
 'GASTA','ONDANVAGE','NODALGA','UCHER']

VOW = set("AEIOU")
# manner-of-articulation classes (a28-style): consonants that interchange share manner
MANNER = {}
for g, cls in [("BCDGPTQ", "oclusiva"), ("NM", "nasal"), ("LR", "liquida"),
               ("SZXF", "sibilante"), ("HV", "aspirada"), ("K", "oclusiva")]:
    for ch in g:
        MANNER[ch] = cls


def skel(name):
    out = []
    for ch in name:
        if ch in VOW:
            continue
        if out and out[-1] == ch:
            continue
        out.append(ch)
    return "".join(out)


def related(a, b):
    if a == b:
        return True
    # affix extension: one is a contiguous substring of the other at an end
    if a in b or b in a:
        return True
    # single-consonant manner-preserving substitution (same length)
    if len(a) == len(b):
        diff = [(x, y) for x, y in zip(a, b) if x != y]
        if len(diff) == 1:
            x, y = diff[0]
            if MANNER.get(x) and MANNER.get(x) == MANNER.get(y):
                return True
    # one insertion/deletion (affix of 1 consonant) at any position
    if abs(len(a) - len(b)) == 1:
        lo, hi = (a, b) if len(a) < len(b) else (b, a)
        for i in range(len(hi)):
            if hi[:i] + hi[i+1:] == lo:
                return True
    return False


def components(skels):
    parent = list(range(len(skels)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i in range(len(skels)):
        for j in range(i + 1, len(skels)):
            if related(skels[i], skels[j]):
                parent[find(i)] = find(j)
    roots = Counter(find(i) for i in range(len(skels)))
    return roots


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    skels = [skel(n) for n in NAMES]
    comp = components(skels)
    n_comp = len(comp)
    biggest = max(comp.values())
    print(f"[SEED] {len(NAMES)} nomes -> {n_comp} sementes independentes (maior cobre {biggest} nomes)", flush=True)
    # show the components
    parent_map = {}
    # recompute membership
    idx_root = {}
    # build groups
    groups = {}
    # redo union to list members
    parent = list(range(len(skels)))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]; x = parent[x]
        return x
    for i in range(len(skels)):
        for j in range(i+1, len(skels)):
            if related(skels[i], skels[j]):
                parent[find(i)] = find(j)
    for i in range(len(skels)):
        groups.setdefault(find(i), []).append(NAMES[i])
    glist = sorted(groups.values(), key=len, reverse=True)
    for g in glist[:6]:
        print("   ", g, flush=True)

    # null: 49 surrogate names, same lengths, letters by frequency
    full = load.dense_stream()
    freq = Counter(full); letters = list(freq); weights = [freq[c] for c in letters]
    lens = [len(n) for n in NAMES]
    null_comps = []
    for _ in range(300):
        sur = ["".join(rng.choices(letters, weights, k=L)) for L in lens]
        null_comps.append(len(components([skel(s) for s in sur])))
    m = sum(null_comps) / len(null_comps); sd = (sum((x - m) ** 2 for x in null_comps) / len(null_comps)) ** 0.5
    z = (n_comp - m) / sd if sd else 0
    print(f"[SEED] null (nomes surrogados): {m:.1f} ± {sd:.1f} sementes  | real {n_comp}  z={z:+.2f}", flush=True)

    result = {"seed": 1583, "n_names": len(NAMES), "n_seeds_real": n_comp,
              "biggest_seed_covers": biggest, "null_mean": round(m, 2), "null_sd": round(sd, 2),
              "z": round(z, 2), "groups": glist}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "213_one_seed.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
