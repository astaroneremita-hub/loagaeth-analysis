# -*- coding: utf-8 -*-
"""Gera as figuras-chave do livro (PNG) em book/figuras/."""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIG = os.path.join(HERE, "figuras")
os.makedirs(FIG, exist_ok=True)
GOLD = "#b8912f"; GREEN = "#2f8a52"; RED = "#c0392b"; BLUE = "#2f6fb0"; INK = "#1b1a17"
plt.rcParams.update({"font.size": 11, "axes.edgecolor": "#888", "figure.dpi": 150})


def save(name):
    plt.tight_layout(); plt.savefig(os.path.join(FIG, name), bbox_inches="tight"); plt.close()


# 1 - eixo-som: z dos achados
fig, ax = plt.subplots(figsize=(7, 3.6))
labels = ["Pronunciável\n#386", "Assonância\n#387", "Vogal-final\n#391", "Melodia-A\n#392", "Pulso-A(3)\n#398"]
z = [6.9, 5.1, 3.2, 5.2, 31.5]
zc = [min(v, 8) for v in z]  # clip visual
bars = ax.bar(labels, zc, color=GREEN)
for b, v in zip(bars, z):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.1, f"z={v}", ha="center", fontsize=9)
ax.axhline(3, color=RED, ls="--", lw=1); ax.text(4.3, 3.1, "limiar z=3", color=RED, fontsize=8)
ax.set_ylabel("escore-z (acima do nulo)"); ax.set_title("Eixo-som: o Loagaeth é feito para ser cantado")
ax.set_ylim(0, 8.5)
save("fig1_som.png")

# 2 - entropia consoante vs vogal (identidade vs registro)
fig, ax = plt.subplots(figsize=(6.5, 3.6))
cat = ["Nomes\n(invocação)", "Chamadas\n(fala)"]
cons = [3.48, 3.91]; vow = [1.25, 1.96]
x = range(len(cat)); w = 0.35
ax.bar([i-w/2 for i in x], cons, w, label="consoantes (identidade)", color=INK)
ax.bar([i+w/2 for i in x], vow, w, label="vogais (registro/melodia)", color=GOLD)
ax.set_xticks(list(x)); ax.set_xticklabels(cat); ax.set_ylabel("entropia (bits)")
ax.set_title("A identidade mora nas consoantes; a vogal é registro"); ax.legend(fontsize=8)
save("fig2_consoante.png")

# 3 - arco do livro: ilhas de ordem (compressão por folha, esquemático a partir de a229)
fig, ax = plt.subplots(figsize=(8, 3.2))
folhas = list(range(1, 49))
# perfil: corpo ordenado (baixo ratio), costura e profundo altos
ratio = []
for f in folhas:
    if f == 1: ratio.append(0.40)
    elif 11 <= f <= 22: ratio.append(0.44)
    elif 26 <= f <= 28: ratio.append(0.565)
    elif f >= 41: ratio.append(0.52)
    else: ratio.append(0.47)
colors = [RED if 26 <= f <= 28 else (GREEN if 11 <= f <= 22 else BLUE) for f in folhas]
ax.bar(folhas, ratio, color=colors)
ax.set_xlabel("folha"); ax.set_ylabel("razão de compressão\n(menor = mais ordem)")
ax.set_title("Ilhas de ordem (corpo, verde) e o pico de caos (costura 26-28, vermelho)")
ax.set_ylim(0.38, 0.59)
save("fig3_compressao.png")

# 4 - real vs refutado (contagem geral do estudo)
fig, ax = plt.subplots(figsize=(5.5, 3.4))
cats = ["REAL\n(bateu o nulo)", "REFUTADO\n(caiu)", "DESCRITIVO"]
vals = [26, 16, 6]  # do painel de integridade (ordem de grandeza)
ax.bar(cats, vals, color=[GREEN, RED, GOLD])
for i, v in enumerate(vals): ax.text(i, v+0.3, str(v), ha="center")
ax.set_ylabel("nº de achados (amostra do painel)")
ax.set_title("Honestidade: o que passou e o que caiu")
save("fig4_integridade.png")

# 5 - MI por direção (gramática só horizontal)
fig, ax = plt.subplots(figsize=(6, 3.4))
d = ["horizontal", "vertical", "diagonal ↘", "anti ↙"]
mi = [0.60, 0.007, 0.016, 0.008]
ax.bar(d, mi, color=[GREEN, "#aaa", "#aaa", "#aaa"])
ax.set_ylabel("informação mútua (bits)")
ax.set_title("A gramática é só horizontal (lê-se em linha)")
save("fig5_direcao.png")

print("figuras geradas:", os.listdir(FIG))
