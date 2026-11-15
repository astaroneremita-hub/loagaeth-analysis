# -*- coding: utf-8 -*-
"""
a186 — Nomes sagrados (hebraico/cabala) aparecem como substring no Loag inteiro?
YHVH e permutações, nomes de Deus, sefirot, anjos planetários. Contra null pareado. seed 1583.
"""
import json,re,unicodedata,random,collections,statistics,itertools
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w="".join(c for c in unicodedata.normalize("NFD",str(w)) if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z]","",w.lower())
grd=json.load(open(ROOT+r"\engine\data\loagaeth_grades_simples.json",encoding="utf-8"))
lines=[]
for k in grd:
    if k and k[0].isdigit():
        for ln in grd[k]:
            s=norm(ln)
            if s: lines.append(s)
BOOK="".join(lines)
def hit(name): return any(name in s for s in lines)

groups={
 "nomes_de_Deus":["elohim","adonai","ehyeh","shaddai","tzabaoth","yahweh","jehovah","eloah"],
 "sefirot":["kether","chokmah","binah","chesed","geburah","tiphareth","netzach","hod","yesod","malkuth"],
 "YHVH_perm":["".join(p) for p in set(itertools.permutations("yhvh"))],
 "anjos_planet":["michael","gabriel","raphael","haniel","tzadkiel","kamael","tzaphkiel","sandalphon","metatron","raziel"],
 "controle_random":[]  # preenchido com strings aleatorias "parecendo nomes"
}
# controle: nomes inventados plausíveis (mesma letra-fonte)
letp="".join(lines)
groups["controle_random"]=["".join(random.choice(letp) for _ in range(random.choice([5,6,7]))) for _ in range(20)]

def rate(lst):
    lst=[n for n in set(norm(x) for x in lst) if len(n)>=4]
    if not lst: return (0,0,[])
    h=[n for n in lst if hit(n)]
    return (len(h),len(lst),h)

print(f"livro: {len(lines)} linhas, {len(BOOK)} letras\n")
print(f"{'grupo':<18}{'batem':>8}  (quais)")
allnames=[]
for g,lst in groups.items():
    h,n,hits=rate(lst); allnames+= [norm(x) for x in lst if len(norm(x))>=4]
    print(f"{g:<18}{h}/{n:<5}  {', '.join(hits)[:50]}")

# null: strings aleatorias mesmos tamanhos de todos os alvos (excl. controle)
targets=[norm(x) for g in ("nomes_de_Deus","sefirot","YHVH_perm","anjos_planet") for x in groups[g] if len(norm(x))>=4]
targets=sorted(set(targets))
real=sum(1 for n in targets if hit(n))
sizes=[len(n) for n in targets]; NT=3000; nul=[]
for _ in range(NT):
    nul.append(sum(1 for s in sizes if hit("".join(random.choice(letp) for _ in range(s)))))
mu=sum(nul)/NT; sd=statistics.pstdev(nul) or 1
print(f"\nTODOS os sagrados (len>=4): {real}/{len(targets)} batem")
print(f"NULL (mesmos tamanhos): {mu:.1f}/{len(targets)} ({100*mu/len(targets):.0f}%)  z={(real-mu)/sd:+.1f}")
PY2=0
