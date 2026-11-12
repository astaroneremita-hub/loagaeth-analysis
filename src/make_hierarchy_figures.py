"""
Figures for the weave / hierarchy phase (a75-a80), saved as PNG into figures/.
All documentation lives in the repository with images - no external artifacts.
"""
import json
import os
import random

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

import load
from a75_row_stratification import shuffle_leaf
from a77_names_woven import FAMILIES, trace_vs_scramble

FIG = os.path.join(load.ROOT, "figures")
os.makedirs(FIG, exist_ok=True)
COL = {"CHADAX": "#D85A30", "NOCHA": "#7F77DD", "GETH": "#1D9E75", "CHASTOR": "#378ADD", "DAHAHOXOM": "#BA7517"}


def fig_stratification():
    lv = load.leaves()
    rows = [load.letters(r) for r in lv["2b"] if load.letters(r)]
    rng = random.Random(1)
    sh = shuffle_leaf([list(r) for r in rows], rng)
    fig, axes = plt.subplots(2, 1, figsize=(9, 5), sharex=True)
    for ax, ch in zip(axes, ["A", "N"]):
        real = [r.count(ch) for r in rows]
        shuf = [r.count(ch) for r in sh]
        ax.plot(range(49), shuf, color="#888780", lw=1, label="embaralhado (mesmas letras)")
        ax.plot(range(49), real, color="#D85A30", lw=2, label="livro de Dee")
        ax.set_ylabel("vezes na linha")
        ax.set_title("letra %s por linha  (folha 2b)" % ch, loc="left", fontsize=10)
        ax.legend(fontsize=8, loc="upper right")
        ax.set_ylim(bottom=0)
    axes[1].set_xlabel("linha (0-48)")
    fig.suptitle("Estratificacao: cada letra espalhada por igual entre as linhas", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_row_stratification.png"), dpi=130)
    plt.close(fig)


def fig_territory():
    d = json.load(open(os.path.join(load.RESULTS, "78_territory_map.json"), encoding="utf-8"))
    order, terr = d["order"], d["territory"]
    fig, ax = plt.subplots(figsize=(11, 2.4))
    for i, k in enumerate(order):
        fam = terr[k]["home"]
        ax.add_patch(plt.Rectangle((i, 0), 0.92, 1, color=COL.get(fam, "#888780"), alpha=0.9))
        ax.text(i + 0.46, -0.18, k, ha="center", va="top", fontsize=6, rotation=90, color="#444")
    ax.set_xlim(0, len(order))
    ax.set_ylim(-0.9, 1.1)
    ax.axis("off")
    handles = [plt.Rectangle((0, 0), 1, 1, color=COL[f]) for f in ("CHADAX", "NOCHA", "CHASTOR", "GETH")]
    ax.legend(handles, ["CHADAX (abre)", "NOCHA (frente)", "CHASTOR (espinha)", "GETH (fundo)"],
              ncol=4, fontsize=8, loc="upper center", bbox_to_anchor=(0.5, 1.25), frameon=False)
    ax.set_title("Territorios: familia que tece cada folha mais forte (ordem do livro)", fontsize=11, pad=22)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_territory_map.png"), dpi=130)
    plt.close(fig)


def fig_hierarchy():
    d = json.load(open(os.path.join(load.RESULTS, "80_full_hierarchy.json"), encoding="utf-8"))
    gh = d["global_hierarchy"]
    tiers = [("Rei", gh[0]["name"], gh[0]["total"], "#854F0B"),
             ("Nome de Deus", gh[1]["name"], gh[1]["total"], "#BA7517"),
             ("Nome do Espirito", gh[2]["name"], gh[2]["total"], "#EF9F27"),
             ("Arcanjo", gh[3]["name"], gh[3]["total"], "#1D9E75"),
             ("Senior", gh[4]["name"], gh[4]["total"], "#378ADD"),
             ("Anjos da corte", "ACLAX / NOCHAP / ALGETH", 0, "#7F77DD"),
             ("Anjos menores", "nomes que aparecem 1x", 0, "#888780")]
    fig, ax = plt.subplots(figsize=(8, 6))
    n = len(tiers)
    for i, (tier, name, tot, c) in enumerate(tiers):
        wt = 2 + 7 * (i / (n - 1))
        wb = 2 + 7 * ((i + 1) / (n - 1))
        y = n - i
        ax.add_patch(Polygon([(-wt / 2, y), (wt / 2, y), (wb / 2, y - 1), (-wb / 2, y - 1)],
                             closed=True, color=c, alpha=0.9))
        lbl = "%s  -  %s" % (tier, name) + ("  (%dx)" % tot if tot else "")
        ax.text(0, y - 0.5, lbl, ha="center", va="center", color="white", fontsize=10,
                fontweight="bold" if i < 5 else "normal")
    ax.set_xlim(-5, 5)
    ax.set_ylim(0, n + 0.5)
    ax.axis("off")
    ax.set_title("Hierarquia por repeticao - quem mais repete, mais domina", fontsize=12)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_hierarchy_pyramid.png"), dpi=130)
    plt.close(fig)


def fig_names_woven():
    d = json.load(open(os.path.join(load.RESULTS, "77_names_woven.json"), encoding="utf-8"))
    pn = d["per_name"]
    names = sorted(pn, key=lambda n: pn[n]["leaves_woven"], reverse=True)
    woven = [pn[n]["leaves_woven"] for n in names]
    present = [pn[n]["leaves_present"] for n in names]
    fig, ax = plt.subplots(figsize=(9, 5))
    y = range(len(names))
    ax.barh(list(y), present, color="#e0e0d8", label="folhas onde aparece")
    ax.barh(list(y), woven, color="#D85A30", label="folhas onde esta 'tecido' (bate o embaralhamento)")
    ax.set_yticks(list(y))
    ax.set_yticklabels(names, fontsize=8)
    ax.invert_yaxis()
    ax.set_xlabel("numero de folhas")
    ax.legend(fontsize=8, loc="lower right")
    ax.set_title("Nomes tecidos na grade: real traca acima das proprias letras embaralhadas", fontsize=11)
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "fig_names_woven.png"), dpi=130)
    plt.close(fig)


def run():
    fig_stratification()
    fig_territory()
    fig_hierarchy()
    fig_names_woven()
    return ["fig_row_stratification.png", "fig_territory_map.png", "fig_hierarchy_pyramid.png", "fig_names_woven.png"]


if __name__ == "__main__":
    for f in run():
        print("wrote figures/" + f)
