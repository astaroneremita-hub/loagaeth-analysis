# -*- coding: utf-8 -*-
"""a206 - TWO genuinely new questions (not re-proving the name field).

LOCALITY: is each recurring name global (everywhere) or are some LOCAL to one folha
  (place-specific entities)? Per name, count distinct folhas it appears in. Spectrum +
  list of folha-exclusive names. Null: shuffle which folha each occurrence sits in.
ORDER: does the SEQUENCE of names follow a consistent order across folhas (a liturgical
  syntax of names)? For global marker names, record first-appearance position per folha,
  measure rank-consistency across folhas vs shuffled order.

Writes results/206_locality_order.json + viz/locality.json. Seed 1583. stdlib only.
"""
import os
import sys
import json
import random
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    nums = load.table_numbers()
    folha_text = {n: load.table_text(n) for n in nums}
    full = "".join(folha_text[n] for n in nums)

    # vocabulary: recurring 6-grams (count >= 12), kept if not a substring of a longer kept one
    c6 = Counter(full[i:i + 6] for i in range(len(full) - 5))
    cand = [g for g, v in c6.items() if v >= 12]
    cand.sort(key=lambda g: -c6[g])
    vocab = cand[:60]
    print(f"vocabulário: {len(vocab)} unidades recorrentes (6-gramas, ≥12×)", flush=True)

    # ---------- LOCALITY ----------
    folhas_of = {}
    for v in vocab:
        fs = [n for n in nums if v in folha_text[n]]
        folhas_of[v] = fs
    spectrum = Counter(len(fs) for fs in folhas_of.values())
    local = sorted([(v, folhas_of[v][0], c6[v]) for v in vocab if len(folhas_of[v]) == 1], key=lambda x: -x[2])
    globalish = sorted([(v, len(folhas_of[v]), c6[v]) for v in vocab], key=lambda x: -x[1])[:8]
    nfolha = len(nums)
    # null: distribute each vocab's total occurrences randomly over folhas (by folha size), count distinct folhas
    sizes = [len(folha_text[n]) for n in nums]
    tot = sum(sizes)
    def null_distinct(total_occ):
        hit = set()
        for _ in range(total_occ):
            r = rng.random() * tot; acc = 0
            for i, s in enumerate(sizes):
                acc += s
                if r <= acc:
                    hit.add(i); break
        return len(hit)
    obs_mean_folhas = sum(len(fs) for fs in folhas_of.values()) / len(vocab)
    null_vals = []
    for _ in range(200):
        null_vals.append(sum(min(nfolha, null_distinct(min(c6[v], 400))) for v in vocab) / len(vocab))
    nm = sum(null_vals) / len(null_vals); nsd = (sum((x - nm) ** 2 for x in null_vals) / len(null_vals)) ** 0.5
    z_loc = (obs_mean_folhas - nm) / nsd if nsd else 0
    print(f"[LOCALITY] média de folhas por nome: obs {obs_mean_folhas:.1f} vs null {nm:.1f}±{nsd:.1f} (de {nfolha}) z={z_loc:+.2f}", flush=True)
    print(f"[LOCALITY] nomes exclusivos de 1 folha: {len(local)}  {[(v,f) for v,f,_ in local[:8]]}", flush=True)

    # ---------- ORDER ----------
    # DISTINCT name roots: greedily drop any that shares a 4-gram with a kept one
    # (avoids overlapping-substring artifacts like CHASTO vs HASTOR)
    def grams4(s):
        return set(s[i:i + 4] for i in range(len(s) - 3))
    distinct = []
    for v, nf, _ in globalish[:1] + sorted([(v, len(folhas_of[v]), c6[v]) for v in vocab], key=lambda x: -x[2]):
        g = grams4(v)
        if all(not (g & grams4(u)) for u in distinct):
            distinct.append(v)
        if len(distinct) >= 7:
            break
    markers = distinct[:6]
    print(f"[ORDER] marcadores distintos: {markers}", flush=True)
    # per folha, first-occurrence index of each marker (if present)
    seqs = {}
    for n in nums:
        t = folha_text[n]
        pos = {m: t.find(m) for m in markers if m in t}
        if len(pos) >= 3:
            seqs[n] = [m for m, _ in sorted(pos.items(), key=lambda x: x[1])]
    # consistency: for each ordered pair (a,b), fraction of folhas where a before b
    pair_before = defaultdict(lambda: [0, 0])
    for n, order in seqs.items():
        idx = {m: i for i, m in enumerate(order)}
        for a in markers:
            for b in markers:
                if a != b and a in idx and b in idx:
                    pair_before[(a, b)][0] += 1 if idx[a] < idx[b] else 0
                    pair_before[(a, b)][1] += 1
    # a consistent syntax -> some pairs near 100% or 0%; measure max |frac-0.5|
    consist = []
    for (a, b), (bef, tot2) in pair_before.items():
        if tot2 >= 8 and a < b:
            frac = bef / tot2
            consist.append((f"{a}<{b}", round(frac, 2), tot2))
    consist.sort(key=lambda x: -abs(x[1] - 0.5))
    mean_dev = sum(abs(f - 0.5) for _, f, _ in consist) / len(consist) if consist else 0
    print(f"[ORDER] folhas com >=3 marcadores: {len(seqs)}; pares mais consistentes: {consist[:5]}", flush=True)
    print(f"[ORDER] desvio médio de 0.5 (0=ordem aleatória, 0.5=ordem fixa): {mean_dev:.3f}", flush=True)

    result = {
        "seed": 1583, "vocab_size": len(vocab),
        "locality": {"spectrum": dict(spectrum), "mean_folhas_obs": round(obs_mean_folhas, 2),
                     "null_mean": round(nm, 2), "null_sd": round(nsd, 2), "z": round(z_loc, 2),
                     "n_folhas": nfolha, "exclusive_1folha": [[v, f, c6[v]] for v, f, _ in local],
                     "most_global": [[v, nf] for v, nf, _ in globalish]},
        "order": {"markers": markers, "n_folhas_used": len(seqs),
                  "pair_consistency": consist[:12], "mean_dev_from_random": round(mean_dev, 3)},
    }
    viz = {"spectrum": dict(spectrum), "n_folhas": nfolha,
           "most_global": result["locality"]["most_global"],
           "exclusive": result["locality"]["exclusive_1folha"][:20],
           "order": result["order"]}
    with open(os.path.join(os.path.dirname(HERE), "viz", "locality.json"), "w", encoding="utf-8") as f:
        json.dump(viz, f, ensure_ascii=False)
    rdir = os.path.join(os.path.dirname(HERE), "results"); os.makedirs(rdir, exist_ok=True)
    with open(os.path.join(rdir, "206_locality_order.json"), "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
