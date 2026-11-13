"""160 - generate the audit figures into figures/ for the technical report (#317-#329)."""
import os
import math
import random
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from collections import Counter

import load
from a22_robustness_and_depth import base_book, tnum

FIG = os.path.join(load.ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
V = set("AEIOU")


def leaf_counts():
    book = base_book(); prof = {}
    for k in book:
        g = ["".join(r) for r in book[k] if r]
        if not g:
            continue
        prof.setdefault(tnum(k), Counter()).update(c for row in g for c in row if c.isalpha())
    return prof


prof = leaf_counts(); ns = sorted(prof)


def cos(a, b):
    ks = set(a) | set(b); d = sum(a.get(k, 0) * b.get(k, 0) for k in ks)
    na = math.sqrt(sum(v * v for v in a.values())); nb = math.sqrt(sum(v * v for v in b.values()))
    return d / (na * nb) if na and nb else 0


# ---- Fig 1: similarity vs leaf distance ----
dist, sim = [], []
for i in range(len(ns)):
    for j in range(i + 1, len(ns)):
        dist.append(abs(ns[i] - ns[j])); sim.append(cos(prof[ns[i]], prof[ns[j]]))
bins = {}
for d, s in zip(dist, sim):
    bins.setdefault(min(d // 4, 11), []).append(s)
bx = [b * 4 + 2 for b in sorted(bins)]; by = [np.mean(bins[b]) for b in sorted(bins)]
plt.figure(figsize=(7, 4))
plt.scatter(dist, sim, s=4, alpha=.12, color="#8a6d2f")
plt.plot(bx, by, "-o", color="#8a2f7d", lw=2, label="mean by distance")
plt.xlabel("leaf-index distance |i-j|"); plt.ylabel("letter-profile similarity (cosine)")
plt.title("#317/#327  Sequential gradient: similarity decays with distance\nMantel r=0.52, permutation p<1e-5")
plt.legend(); plt.tight_layout(); plt.savefig(os.path.join(FIG, "audit_gradient_decay.png"), dpi=110); plt.close()


# ---- Fig 2: A and I fraction along the book ----
A = [prof[n]["A"] / sum(prof[n].values()) for n in ns]
I = [prof[n]["I"] / sum(prof[n].values()) for n in ns]
plt.figure(figsize=(7, 4))
plt.plot(ns, A, "-o", ms=3, color="#b8862a", label="A (name-letter, Earth)")
plt.plot(ns, I, "-o", ms=3, color="#c0392b", label="I (Fire)")
plt.xlabel("leaf (Dee order)"); plt.ylabel("letter fraction")
plt.title("#318/#320  Letter axis along the book: A falls, I rises (each p=0.002)")
plt.legend(); plt.tight_layout(); plt.savefig(os.path.join(FIG, "audit_letter_axis.png"), dpi=110); plt.close()


# ---- Fig 3: reconstruction scores (from #328/#329) vs random ----
labels = ["freq\nspectral", "freq\ntsp", "freq\npca", "bi\nspectral", "bi\ntsp", "bi\npca", "tri\nspectral", "tri\ntsp", "tri\npca"]
vals = [0.688, 0.552, 0.641, 0.651, 0.867, 0.543, 0.676, 0.763, 0.501]
plt.figure(figsize=(8, 4))
plt.bar(range(len(vals)), vals, color="#2f6d8a")
plt.axhline(0.118, color="#c0392b", ls="--", label="random order mean (0.118)")
plt.axhspan(0.118 - 0.088, 0.118 + 0.088, color="#c0392b", alpha=.12)
plt.xticks(range(len(vals)), labels, fontsize=8); plt.ylabel("|Spearman| vs Dee order")
plt.title("#328  Blind order reconstruction (content only) vs random")
plt.legend(); plt.tight_layout(); plt.savefig(os.path.join(FIG, "audit_reconstruction.png"), dpi=110); plt.close()


# ---- Fig 4: detrend control (the decisive specificity test) ----
lab = ["full\norder", "pure global\ntrend", "RESIDUAL\nonly", "artificial\ngradient"]
sc = [0.552, 1.000, 0.117, 0.425]
col = ["#2f6d8a", "#6c6b62", "#c0392b", "#8a6d2f"]
plt.figure(figsize=(7, 4))
plt.bar(range(4), sc, color=col)
plt.axhline(0.118, color="#c0392b", ls="--", label="chance (0.118)")
plt.xticks(range(4), lab, fontsize=9); plt.ylabel("|Spearman| vs Dee order")
plt.title("#329  Detrend control: order-info is the GLOBAL gradient only\nresidual ≈ chance → no local encoding")
plt.legend(); plt.tight_layout(); plt.savefig(os.path.join(FIG, "audit_detrend_control.png"), dpi=110); plt.close()


# ---- Fig 5: what survived vs what fell (grammar audit #324-326) ----
plt.figure(figsize=(7, 4))
tests = ["root-reuse\nvs Markov-0", "vs Markov-1", "vs Markov-2", "vs Markov-3", "held-out\nvs Markov-2"]
z = [24.9, 9.1, 0.3, -2.1, -1.0]
colors = ["#2f8a52" if v > 2 else "#c0392b" for v in z]
plt.bar(range(len(z)), z, color=colors)
plt.axhline(2, color="#6c6b62", ls="--", label="z=2 threshold")
plt.axhline(-2, color="#6c6b62", ls=":")
plt.xticks(range(len(z)), tests, fontsize=8); plt.ylabel("z (real vs control)")
plt.title("#324-326  Name grammar: beats Markov-0/1, NOT Markov-2/3\n→ structure is order-2-3 phonotactics, not special grammar")
plt.legend(); plt.tight_layout(); plt.savefig(os.path.join(FIG, "audit_grammar_markov.png"), dpi=110); plt.close()

print("figures written:", sorted(f for f in os.listdir(FIG) if f.startswith("audit_")))
