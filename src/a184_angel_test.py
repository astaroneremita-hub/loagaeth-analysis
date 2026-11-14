# -*- coding: utf-8 -*-
"""
a184 — Nomes de anjos (venusianos, Filhos da Luz) são geráveis pela gramática do Loag?
HONESTO: o que importa é o FALSO-POSITIVO. Testa grupos-alvo vs controles (anjos de
outros sistemas) vs null (strings aleatórias). Se os venusianos não passam mais que o
acaso, achar um não prova nada. seed 1583.
"""
import json,re,unicodedata,random,collections
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
V=set("aeiou")
def da(s): return "".join(c for c in unicodedata.normalize("NFD",str(s)) if unicodedata.category(c)!="Mn")
def norm(w): return re.sub(r"[^a-z]","",da(w).lower())
fg=json.load(open(ROOT+r"\viz\forge_grammar.json",encoding="utf-8"))
names=[da(n).upper() for n in fg["real_names"]]
def parse(w):
    sk="".join(c for c in w if c not in V); ml="".join(c for c in w if c in V)
    tm="".join("C" if c not in V else "V" for c in w); return sk,ml,tm
SK=set();ML=set();TM=set()
for n in names: s,m,t=parse(n.lower());SK.add(s);ML.add(m);TM.add(t)
# nucleo
PREF=sorted((p.lower() for p in fg["prefixes"]),key=len,reverse=True)
SUF=sorted((s.lower() for s in fg["suffixes"]),key=len,reverse=True)
RTS=sorted((r.lower() for r in fg["roots"]),key=len,reverse=True)
def nucleo(n):
    for p in [""]+PREF:
        if not n.startswith(p): continue
        i=len(p)
        for r in RTS:
            if n[i:].startswith(r):
                j=i+len(r)
                while j<len(n):
                    h=next((s for s in SUF if n[j:].startswith(s)),None)
                    if not h: break
                    j+=len(h)
                if j==len(n): return True
    return False
def rico(n): s,m,t=parse(n); return s in SK and m in ML and t in TM
LETP={k.lower():fg["letters"][k]["p"] for k in fg["letters"]}
def venus(n):  # dominante Venus?
    c=collections.Counter()
    for ch in n:
        p=LETP.get(ch,"-")
        if p not in ("-","?"): c[p]+=1
    return c and c.most_common(1)[0][0]=="Venus"

# grupos
VENUS_ANGELS="hanael haniel anael hagiel kedemel noguel asmodel ihrlaa".split()
# Filhos da Luz / Heptarquia (atestados nos dados de Dee)
h=json.load(open(ROOT+r"\engine\data\heptarquia.json",encoding="utf-8"))
HEPT=set()
for row in h.get("reis_e_principes",[]):
    for k in ("rei","principe"):
        if row.get(k): HEPT.add(norm(row[k]))
FILII="el me ese iana akele azdobn stimcul esemeli ilemese hipotga lhiansa arinnap ligdisa bnapsen".split()
CONTROL="michael gabriel raphael samael azrael metatron sandalphon lucifer belial asmodeus leviathan moloch dagon baal astaroth".split()
def clean(lst): return sorted(set(norm(x) for x in lst if len(norm(x))>=2))
groups={"VENUS_angels":clean(VENUS_ANGELS),"Filii_Lucis":clean(FILII),
        "Heptarquia_reis":clean(HEPT),"CONTROLE_outros":clean(CONTROL)}

def rates(lst):
    if not lst: return (0,0,0)
    n=len(lst); r=sum(1 for x in lst if rico(x)); nu=sum(1 for x in lst if nucleo(x))
    return n,r,nu
print(f"inventario rico: {len(SK)} esqueletos, {len(ML)} melodias, {len(TM)} templates\n")
print(f"{'grupo':<18} {'n':>3} {'rico':>6} {'nucleo':>7}")
for g,lst in groups.items():
    n,r,nu=rates(lst)
    print(f"{g:<18} {n:>3} {r:>5}  {nu:>6}   {' '.join(x+('*' if rico(x) else '') for x in lst)[:60]}")

# NULL: strings aleatorias com a MESMA distribuicao de tamanhos de todos os alvos
allt=[x for lst in groups.values() for x in lst]
letpool="".join(n.lower() for n in names)
NT=3000; rico_hits=[];nuc_hits=[]
sizes=[len(x) for x in allt]
for _ in range(NT):
    rs=["".join(random.choice(letpool) for _ in range(s)) for s in sizes]
    rico_hits.append(sum(1 for x in rs if rico(x))); nuc_hits.append(sum(1 for x in rs if nucleo(x)))
import statistics
mu_r=sum(rico_hits)/NT; mu_n=sum(nuc_hits)/NT
real_r=sum(rates(lst)[1] for lst in groups.values()); real_n=sum(rates(lst)[2] for lst in groups.values())
print(f"\nTODOS os alvos: rico {real_r}/{len(allt)}, nucleo {real_n}/{len(allt)}")
print(f"NULL (mesmos tamanhos, letras do Loag): rico {mu_r:.1f}/{len(allt)} ({100*mu_r/len(allt):.0f}%), nucleo {mu_n:.1f}/{len(allt)} ({100*mu_n/len(allt):.0f}%)")
# falso-positivo por si
sd_r=statistics.pstdev(rico_hits) or 1
print(f"z (alvos rico vs null): {(real_r-mu_r)/sd_r:+.1f}")
PY