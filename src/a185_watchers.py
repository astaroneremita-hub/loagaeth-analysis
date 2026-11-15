# -*- coding: utf-8 -*-
"""
a185 — Os Vigilantes (anjos caídos do Livro de Enoque) são geráveis pela gramática do Loag?
Testa cada nome + variações contra núcleo / rico-90 / rico-livro, e o grupo vs null. seed 1583.
"""
import json,re,unicodedata,random,collections,statistics
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
Vw=set("aeiou")
def da(s): return "".join(c for c in unicodedata.normalize("NFD",str(s)) if unicodedata.category(c)!="Mn")
def norm(w): return re.sub(r"[^a-z]","",da(w).lower())
fg=json.load(open(ROOT+r"\viz\forge_grammar.json",encoding="utf-8"))
names=[norm(n) for n in fg["real_names"]]
def parse(w):
    sk="".join(c for c in w if c not in Vw); ml="".join(c for c in w if c in Vw)
    tm="".join("C" if c not in Vw else "V" for c in w); return sk,ml,tm
SK=set();ML=set();TM=set()
for n in names: s,m,t=parse(n);SK.add(s);ML.add(m);TM.add(t)
SKb=set(norm(s) for s in fg["skeletons"]); MLb=set(norm(m) for m in fg["melodies"])
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
def rico90(n): s,m,t=parse(n); return s in SK and m in ML and t in TM
def ricoBook(n): s,m,t=parse(n); return s in SKb and m in MLb

WATCHERS="""Samyaza Shemyazaz Semihazah Urakabarameel Arakiba Artqoph Akibeel Tamiel Tumael
Ramuel Ramiel Rameel Danel Daniel Danjal Azkeel Ezeqeel Asael Saraknyal Sariel Sarakiel
Azazel Armers Armaros Batraal Baraqel Batarjal Anane Ananel Hananel Samsaveel Samsiel
Turel Turael Yomyael Yomiel Arazyal Araqiel""".split()
W=sorted(set(norm(x) for x in WATCHERS if len(norm(x))>=2))
print(f"{len(W)} nomes de Vigilantes (com variações)\n")
print(f"{'nome':<14}{'núcleo':>7}{'rico90':>8}{'livro':>7}  esqueleto/melodia")
hitN=hitR=hitB=0
for n in sorted(W):
    a,b,c=nucleo(n),rico90(n),ricoBook(n); hitN+=a;hitR+=b;hitB+=c
    s,m,t=parse(n)
    print(f"{n:<14}{'✓' if a else '·':>7}{'✓' if b else '·':>8}{'✓' if c else '·':>7}  {s}/{m}")
print(f"\nTOTAL: núcleo {hitN}/{len(W)} · rico90 {hitR}/{len(W)} · livro {hitB}/{len(W)}")
# NULL para livro (permissivo)
letpool="".join(names); sizes=[len(x) for x in W]; NT=4000; hb=[]
for _ in range(NT):
    rs=["".join(random.choice(letpool) for _ in range(s)) for s in sizes]
    hb.append(sum(1 for x in rs if ricoBook(x)))
mu=sum(hb)/NT; sd=statistics.pstdev(hb) or 1
print(f"NULL livro (mesmos tamanhos): {mu:.1f}/{len(W)} ({100*mu/len(W):.0f}%)  z(real vs null)={(hitB-mu)/sd:+.1f}")
# quais passaram no livro
pb=[n for n in W if ricoBook(n)]
print("passaram no livro:",", ".join(pb) or "nenhum")
PY2="""
"""
