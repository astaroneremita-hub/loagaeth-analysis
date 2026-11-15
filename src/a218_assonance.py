# -*- coding: utf-8 -*-
"""a218 - sound axis: assonance / rhyme between NEIGHBOURING names (chant-linking).

If the book is chanted, consecutive names in reading order may share vowels (assonance) or
endings (rhyme) more than chance - a sound-linking device. For each folha, take the recurring
names in reading-position order; measure, for adjacent pairs, (a) vowel-skeleton overlap
(assonance) and (b) same final vowel (rhyme). Compare to shuffling the name order within the
folha (null preserves which names, kills the order).

stdlib only. seed 1583.
"""
import os
import sys
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

VOW = set("AEIOU")
NAMES = ['NACHO','NOCHAP','NOCHASTOR','NOCHAPH','ADNOCHAP','ACLAXTO','GRADAX','AXALGRA',
 'NOCHASTORA','ICHASTOR','PHANGE','ANTANTOX','VOXAR','NECHASTOR','ACLAXTOR','ICHASTORA',
 'ZICHASTOR','ANCHANO','NADAB','CHARDAX','AOXARD','ALCHADAX','OXARDRAH','OLCHADNA',
 'NACLANSA','DONCHAL','ACHARDAN','CHIDAXTO','GASTA','NODALGA','UCHER','ALGETH','ANZACH','DAXVAR']


def vskel(w):
    return "".join(c for c in w if c in VOW)


def seq_of(text):
    hits = []
    for nm in NAMES:
        start = 0
        while True:
            k = text.find(nm, start)
            if k < 0:
                break
            hits.append((k, nm)); start = k + 1
    hits.sort()
    return [nm for _, nm in hits]


def assonance(seq):
    if len(seq) < 2:
        return None, None
    ov, rh, n = 0.0, 0, 0
    for a, b in zip(seq, seq[1:]):
        va, vb = set(vskel(a)), set(vskel(b))
        ov += len(va & vb) / len(va | vb) if (va | vb) else 0
        rh += 1 if (vskel(a) and vskel(b) and vskel(a)[-1] == vskel(b)[-1]) else 0
        n += 1
    return ov / n, rh / n


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    nums = load.table_numbers()
    seqs = {n: seq_of(load.table_text(n)) for n in nums}

    ovs, rhs, w = [], [], 0
    for n, s in seqs.items():
        a, r = assonance(s)
        if a is not None:
            ovs.append(a * len(s)); rhs.append(r * len(s)); w += len(s)
    obs_ov = sum(ovs) / w; obs_rh = sum(rhs) / w

    def null():
        tov, trh, tw = 0.0, 0, 0
        for s in seqs.values():
            if len(s) < 2:
                continue
            sh = s[:]; rng.shuffle(sh)
            a, r = assonance(sh)
            tov += a * len(sh); trh += r * len(sh); tw += len(sh)
        return tov / tw, trh / tw
    nov, nrh = [], []
    for _ in range(500):
        a, r = null(); nov.append(a); nrh.append(r)
    def z(obs, arr):
        m = sum(arr) / len(arr); sd = (sum((x - m) ** 2 for x in arr) / len(arr)) ** 0.5
        return m, sd, (obs - m) / sd if sd else 0
    mo, so, zo = z(obs_ov, nov); mr, sr, zr = z(obs_rh, nrh)
    print(f"[ASS] assonância (overlap de vogais) obs {obs_ov:.3f} vs null {mo:.3f}±{so:.3f}  z={zo:+.2f}", flush=True)
    print(f"[RIM] rima (mesma vogal final) obs {obs_rh:.3f} vs null {mr:.3f}±{sr:.3f}  z={zr:+.2f}", flush=True)
    result = {"seed": 1583,
              "assonance": {"obs": round(obs_ov, 3), "null": round(mo, 3), "sd": round(so, 3), "z": round(zo, 2)},
              "rhyme": {"obs": round(obs_rh, 3), "null": round(mr, 3), "sd": round(sr, 3), "z": round(zr, 2)}}
    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "218_assonance.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
