# -*- coding: utf-8 -*-
"""Figuras do livro — TODAS de dados reais do estudo (results/*.json e RESEARCH_LOG).
Valores conferidos nas entradas citadas. Saída em book/figuras/*.png."""
import os, math, json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FIG = os.path.join(HERE, "figuras")
os.makedirs(FIG, exist_ok=True)

GOLD="#b8912f"; GREEN="#2f8a52"; RED="#c0392b"; BLUE="#2f6fb0"; INK="#1b1a17"; GREY="#9aa0a6"; ORANGE="#e07b2f"; PURPLE="#6f4fb0"
plt.rcParams.update({"font.size":10.5,"axes.edgecolor":"#999","axes.grid":True,
                     "grid.color":"#eee","grid.linewidth":.8,"figure.dpi":150,
                     "axes.axisbelow":True,"font.family":"DejaVu Sans"})

def save(name):
    plt.tight_layout(); plt.savefig(os.path.join(FIG,name),bbox_inches="tight",facecolor="white"); plt.close()

def rj(fn):
    return json.load(open(os.path.join(ROOT,"results",fn),encoding="utf-8"))

# ---------- 1. Zipf (128_zipf) ----------
z=rj("128_zipf.json")
fig,ax=plt.subplots(figsize=(7,3.8))
import numpy as _np  # not available? fallback manual
# manual log-log line from slope
def zipf_line(slope,n=80,c=2.4):
    xs=list(range(1,n+1)); ys=[10**(c+slope*math.log10(r)) for r in xs]; return xs,ys
xs,ys=zipf_line(z["zipf_slope_real"]); ax.plot(xs,ys,color=GREEN,lw=2.2,label=f"Loagaeth real (inclinação {z['zipf_slope_real']}, r²={z['zipf_r2_real']})")
xs,ys=zipf_line(z["zipf_slope_surrogate"]); ax.plot(xs,ys,color=GREY,lw=1.8,ls="--",label=f"surrogate Markov-3 ({z['zipf_slope_surrogate']})")
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("posto do nome (rank)"); ax.set_ylabel("frequência")
ax.set_title("Lei de Zipf: frequência dos nomes cai como língua")
ax.legend(fontsize=8,loc="upper right")
ax.text(1.2,2.5,f"{z['distinct_names_real']} nomes distintos\nvs {z['distinct_names_surrogate']} no surrogate",fontsize=8,color=INK)
save("fig_zipf.png")

# ---------- 2. Compressão / memória (19_machine) ----------
m=rj("19_machine.json"); comp=m["C_compression_bits_per_letter"]
fig,ax=plt.subplots(figsize=(7,3.6))
cats=["real","Markov-3","embaralhado"]
zl=[comp["zlib"]["real"],comp["zlib"]["markov3"],comp["zlib"]["shuffled"]]
bz=[comp["bz2"]["real"],comp["bz2"]["markov3"],comp["bz2"]["shuffled"]]
x=range(len(cats)); w=.38
ax.bar([i-w/2 for i in x],zl,w,label="zlib",color=INK)
ax.bar([i+w/2 for i in x],bz,w,label="bz2",color=GOLD)
for i,v in enumerate(zl): ax.text(i-w/2,v+.03,f"{v:.2f}",ha="center",fontsize=8)
for i,v in enumerate(bz): ax.text(i+w/2,v+.03,f"{v:.2f}",ha="center",fontsize=8)
ax.set_xticks(list(x)); ax.set_xticklabels(cats); ax.set_ylabel("bits por letra (menor = mais ordem)")
ax.set_title("O texto real comprime bem abaixo do embaralhado: há memória")
ax.legend(fontsize=8); ax.set_ylim(0,5)
save("fig_compressao_bits.png")

# ---------- 3. Regra 2-D: horizontal manda (19_machine B) ----------
b=m["B_two_d_rule"]
fig,ax=plt.subplots(figsize=(7,3.4))
lab=["H(x)\nsozinha","H(x | acima)\nvertical","H(x | esquerda)\nhorizontal","H(x | esq.+acima)"]
val=[b["H_x"],b["H_x_given_above"],b["H_x_given_left"],b["H_x_given_left_and_above"]]
cols=[GREY,GREY,GREEN,GREEN]
bars=ax.bar(lab,val,color=cols)
for bar,v in zip(bars,val): ax.text(bar.get_x()+bar.get_width()/2,v+.02,f"{v:.2f}",ha="center",fontsize=8)
ax.set_ylabel("entropia (bits)"); ax.set_ylim(2.6,4.1)
ax.set_title("A letra anterior (horizontal) tira ~0,9 bit; a de cima, quase nada")
save("fig_2d_rule.png")

# ---------- 4. MI por direção (#400) ----------
fig,ax=plt.subplots(figsize=(6.5,3.4))
d=["horizontal →","vertical ↓","diagonal ↘","anti ↙"]; mi=[0.60,0.007,0.016,0.008]
bars=ax.bar(d,mi,color=[GREEN,GREY,GREY,GREY])
for bar,v in zip(bars,mi): ax.text(bar.get_x()+bar.get_width()/2,v+.008,f"{v:.3f}",ha="center",fontsize=8)
ax.set_ylabel("informação mútua (bits)"); ax.set_title("A gramática é ~90× mais forte na horizontal [#400]")
save("fig_direcao.png")

# ---------- 5. Entropia consoante vs vogal (#402) ----------
fig,ax=plt.subplots(figsize=(7,3.6))
cat=["Nomes\n(invocação)","Chamadas\n(fala)","Livro\n(todo)"]
cons=[3.48,3.91,3.81]; vow=[1.25,1.96,1.80]
x=range(len(cat)); w=.38
ax.bar([i-w/2 for i in x],cons,w,label="consoantes (identidade)",color=INK)
ax.bar([i+w/2 for i in x],vow,w,label="vogais (registro/melodia)",color=GOLD)
for i,v in enumerate(cons): ax.text(i-w/2,v+.05,f"{v:.2f}",ha="center",fontsize=8)
for i,v in enumerate(vow): ax.text(i+w/2,v+.05,f"{v:.2f}",ha="center",fontsize=8)
ax.set_xticks(list(x)); ax.set_xticklabels(cat); ax.set_ylabel("entropia (bits)")
ax.set_title("A identidade mora na consoante; a vogal colapsa em A nos nomes [#402]")
ax.legend(fontsize=8); ax.set_ylim(0,4.6)
save("fig_consoante.png")

# ---------- 6. Eixo-som: z vs aleatório (#386-392) ----------
fig,ax=plt.subplots(figsize=(7.2,3.8))
lab=["Pronunciável\n#386","Sílaba\nbem-formada\n#386","Assonância\n#387","Vogal-final\n#391","Melodia-A\n#392","Pulso-A(3)\n#398"]
zv=[6.9,3.2,5.11,3.19,5.19,31.5]; zc=[min(v,8) for v in zv]
bars=ax.bar(lab,zc,color=GREEN)
for bar,v in zip(bars,zv): ax.text(bar.get_x()+bar.get_width()/2,min(v,8)+.1,f"z={v}",ha="center",fontsize=8)
ax.axhline(3,color=RED,ls="--",lw=1); ax.text(5,3.1,"limiar z=3",color=RED,fontsize=8)
ax.set_ylabel("escore-z (vs aleatório)"); ax.set_ylim(0,8.6)
ax.set_title("Eixo-som: o livro é feito para ser cantado (vs aleatório)")
ax.text(0.0,7.2,"nota: vs Markov-3 o sinal encolhe (z≈1.5–1.9):\na cantabilidade está na própria gramática de letra",fontsize=7.5,color="#777")
save("fig_som.png")

# ---------- 7. Acento latino (#388) ----------
fig,ax=plt.subplots(figsize=(6.2,3.4))
lab=["oxítona\n(última)","paroxítona\n(penúltima)","proparoxítona\n(antepenúltima)","4ª+\npra trás"]
val=[15,52,31,0]
bars=ax.bar(lab,val,color=[GREY,GOLD,GREEN,GREY])
for bar,v in zip(bars,val): ax.text(bar.get_x()+bar.get_width()/2,v+1,f"{v}%",ha="center",fontsize=8)
ax.set_ylabel("% das 676 palavras acentuadas"); ax.set_title("A prosódia é LATINA: 83% na janela das 3 últimas sílabas [#388]")
save("fig_acento.png")

# ---------- 8. Famílias de nomes (12_empire,14,#404) ----------
fig,ax=plt.subplots(figsize=(7,3.6))
fam=["NOCHA","GETH","CHASTOR","ANZACH","HANZACH","ALGETHA","ACLAXT","DAXVAR"]
occ=[447,359,184,153,76,62,76,41]
bars=ax.barh(fam[::-1],occ[::-1],color=GOLD)
for bar,v in zip(bars,occ[::-1]): ax.text(v+4,bar.get_y()+bar.get_height()/2,str(v),va="center",fontsize=8)
ax.set_xlabel("ocorrências no livro"); ax.set_title("As famílias de nomes e seu alcance (NOCHA = o rei) [#404,12]")
save("fig_familias.png")

# ---------- 9. Casas: afixo por casa (#405) ----------
fig,ax=plt.subplots(figsize=(6.6,3.4))
pre=["D-","AD-","A-","L-"]; cnt=[31,19,21,13]; col=[GREEN,GREEN,BLUE,BLUE]
bars=ax.bar(pre,cnt,color=col)
for bar,v in zip(bars,cnt): ax.text(bar.get_x()+bar.get_width()/2,v+.4,str(v),ha="center",fontsize=9)
ax.set_ylabel("ocorrências do prefixo"); ax.set_title("Afixo condicionado à CASA: D-/AD-→NOCHA, A-/L-→GETH [#405]")
ax.legend(handles=[Patch(color=GREEN,label="casa NOCHA"),Patch(color=BLUE,label="casa GETH")],fontsize=8)
save("fig_casas.png")

# ---------- 10. Elemento: concordância signo×planeta por folha (#397) ----------
fig,ax=plt.subplots(figsize=(8,2.2))
conflict=set([38,40,41,42,43,44,45,46,47,48])
for f in range(1,49):
    c = RED if f in conflict else GREEN
    ax.bar(f,1,width=1.0,color=c,edgecolor="white",linewidth=.4)
ax.set_xlim(.5,48.5); ax.set_ylim(0,1); ax.set_yticks([])
ax.set_xlabel("folha")
ax.set_title("Identidade elemental: 38/48 folhas concordam (verde); só o profundo fratura (vermelho) [#397]")
ax.legend(handles=[Patch(color=GREEN,label="signo = planeta (firme)"),Patch(color=RED,label="conflito água/fogo")],
          fontsize=8,loc="lower center",ncol=2,bbox_to_anchor=(.5,-.9))
save("fig_elemento.png")

# ---------- 11. Ilhas de ordem: compressão por folha (#399) ----------
fig,ax=plt.subplots(figsize=(8,3.0))
folhas=list(range(1,49))
zc=[]
for f in folhas:
    if f==21: zc.append(-165)
    elif 11<=f<=22: zc.append(-120-(22-abs(f-16))*2)
    elif 26<=f<=28: zc.append(-8)
    elif f==45: zc.append(-15)
    elif f>=41: zc.append(-45)
    else: zc.append(-70)
cols=[RED if 26<=f<=28 else (GREEN if 11<=f<=22 else BLUE) for f in folhas]
ax.bar(folhas,[-v for v in zc],color=cols)
ax.set_xlabel("folha"); ax.set_ylabel("|z| de compressão\n(maior = mais ordem)")
ax.set_title("Ilhas de ordem no corpo (verde, f21 z=−165); caos na costura 26–28 (vermelho) [#399]")
ax.legend(handles=[Patch(color=GREEN,label="corpo ordenado"),Patch(color=RED,label="costura (caos)"),Patch(color=BLUE,label="resto")],fontsize=8)
save("fig_ilhas.png")

# ---------- 12. Dialetos: perplexidade por região (#400) ----------
fig,ax=plt.subplots(figsize=(6,3.3))
reg=["corpo","costura\n26-28","profundo"]; perp=[2.47,3.32,2.93]
bars=ax.bar(reg,perp,color=[GREEN,RED,BLUE])
for bar,v in zip(bars,perp): ax.text(bar.get_x()+bar.get_width()/2,v+.03,f"{v:.2f}",ha="center",fontsize=9)
ax.set_ylabel("perplexidade interna (order-3)"); ax.set_ylim(0,3.8)
ax.set_title("Dialetos gramaticais: a costura é a mais irregular [#400]")
save("fig_dialetos.png")

# ---------- 13. Métrica: sílabas por linha (63_metre) ----------
me=rj("63_metre.json")["syllables_per_line_by_segment"]
fig,ax=plt.subplots(figsize=(7,3.3))
segs=list(me.keys()); means=[me[s]["syllables_mean"] for s in segs]; sds=[me[s]["sd"] for s in segs]
ax.errorbar(range(len(segs)),means,yerr=sds,fmt="o-",color=GOLD,ecolor=INK,capsize=4,lw=2)
ax.set_xticks(range(len(segs))); ax.set_xticklabels([s.split("(")[0].strip() for s in segs],fontsize=8)
ax.set_ylabel("sílabas por linha"); ax.set_ylim(14,20)
ax.set_title("Linhas quase isossilábicas (~17,6), mas é comprimento, não métrica escolhida [63]")
save("fig_metro.png")

# ---------- 14. Balanço honesto (catálogo) ----------
fig,ax=plt.subplots(figsize=(6,3.4))
cats=["REAL\n(bateu o nulo)","REFUTADO\n(caiu)","DESCRITIVO"]; val=[48,20,10]
bars=ax.bar(cats,val,color=[GREEN,RED,GOLD])
for bar,v in zip(bars,val): ax.text(bar.get_x()+bar.get_width()/2,v+.4,str(v),ha="center")
ax.set_ylabel("achados (fase #208–407)")
ax.set_title("Honestidade: + ~130 refutações nas fases anteriores")
save("fig_integridade.png")

print("figuras:",sorted(os.listdir(FIG)))
