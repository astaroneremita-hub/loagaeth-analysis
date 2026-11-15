# -*- coding: utf-8 -*-
"""a220 - test the cleanest of the 20 Dee hypotheses (IDEIAS_DEE.md).

#12 Sigillum Dei Aemeth names in the Loagaeth (vs null).
#2  Golden-ratio placement of the seam (26-28) and dissolution onset.
#5  Signature-name leaves on prime-numbered folhas.
#6  Four elemental quarters of the book.
stdlib only. seed 1583.
"""
import os
import sys
import json
import re
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
from a190_tower_traces import side_grids

DATA = os.path.join(os.path.dirname(HERE), "engine", "data")
DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]


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
    rng = random.Random(1583)
    grids = list(side_grids().values())
    result = {}

    # ---- #12 Sigillum names ----
    sig = json.load(open(os.path.join(DATA, "sigillum.json"), encoding="utf-8"))
    sdj = json.dumps(sig, ensure_ascii=False)
    stop = {"JDPP", "PDF", "INDEX", "SDA", "SECUNDUS", "SUMARIO", "DEI", "JHP"}
    sig_names = sorted(set(w for w in re.findall(r"[A-Z]{4,}", sdj) if w not in stop))
    obs = sum(1 for w in sig_names if search2d(w, grids))
    full = load.dense_stream(); freq = Counter(full); L = list(freq); W = [freq[c] for c in L]
    lens = [len(w) for w in sig_names]
    sims = []
    for _ in range(100):
        sur = ["".join(rng.choices(L, W, k=l)) for l in lens]
        sims.append(sum(1 for w in sur if search2d(w, grids)))
    m = sum(sims)/len(sims); sd = (sum((x-m)**2 for x in sims)/len(sims))**0.5
    z = (obs-m)/sd if sd else 0
    result["12_sigillum"] = {"n": len(sig_names), "found": obs, "null_mean": round(m,2), "null_sd": round(sd,2), "z": round(z,2),
                             "names": sig_names}
    print(f"[#12 Sigillum] {obs}/{len(sig_names)} achados; null {m:.1f}±{sd:.1f} z={z:+.2f}", flush=True)

    # ---- #2 golden ratio ----
    phi_pts = {"0.382x48": round(48*0.382,1), "0.618x48": round(48*0.618,1)}
    seam = 27.0; diss = 40.0  # dissolution onset ~40 (#360)
    result["2_phi"] = {"phi_points": phi_pts, "seam_leaf": seam, "dissolution_onset": diss,
                       "seam_vs_0.618x48": round(abs(seam-48*0.618),1),
                       "dissolution_vs_golden": "nenhum ponto φ próximo (0.618×48=29.7, 0.382×48=18.3)"}
    print(f"[#2 φ] costura folha 27 vs 0.618×48=29.7 (gap 2.7); dissolução ~40 longe de φ. Sem casamento limpo.", flush=True)

    # ---- #5 primes ----
    def is_prime(n):
        if n < 2: return False
        for p in range(2, int(n**0.5)+1):
            if n % p == 0: return False
        return True
    # signature events: seam leaves 26-28, dissolution 40-48, pico leaf 1
    nums = load.table_numbers()
    primes = [n for n in nums if is_prime(n)]
    event_leaves = [26,27,28,40,41,42,43,44,45,46,47,48,1,23,24]  # seam, deep, peak, mid
    on_prime = sum(1 for e in event_leaves if is_prime(e))
    exp = len(event_leaves)*len(primes)/len(nums)
    result["5_primes"] = {"n_primes_of_48": len(primes), "event_leaves": event_leaves,
                          "events_on_prime": on_prime, "expected": round(exp,1)}
    print(f"[#5 primos] {len(primes)} primos em 2-48; eventos em folha prima: {on_prime} vs esperado {exp:.1f}", flush=True)

    # ---- #6 four quarters ----
    def quarter(n):
        return (n-1)//12  # 0:1-12,1:13-24,2:25-36,3:37-48
    glob = Counter(ch for g in grids for row in g for ch in row if ch!="?")
    alpha = sorted(glob); gtot=sum(glob.values())
    qcnt = {0:Counter(),1:Counter(),2:Counter(),3:Counter()}
    for n in nums:
        q = quarter(n)
        qcnt[q].update(load.table_text(n))
    chis={}
    for q in range(4):
        cc=qcnt[q]; nn=sum(cc.values()); x2=0
        for a in alpha:
            exp=nn*glob.get(a,0)/gtot
            if exp>0: x2+=(cc.get(a,0)-exp)**2/exp
        chis[q]=round(x2,0)
    # dominant vowel per quarter
    VOW="AEIOU"
    domv={q: max(VOW, key=lambda v: qcnt[q][v]) for q in range(4)}
    result["6_quarters"] = {"chi2_per_quarter": chis, "dominant_vowel": domv}
    print(f"[#6 quartos] χ² por quarto {chis}; vogal dominante por quarto {domv}", flush=True)

    rdir = os.path.join(HERE, "..", "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "220_dee_batch.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
