# -*- coding: utf-8 -*-
"""
a187 — É língua? Bateria de leis linguísticas no Loag vs Chamadas vs latim/hebraico/grego/
inglês/aleatório. Zipf, Heaps, entropia de ordem 0-4, Menzerath, e árvore por compressão (NCD).
Só stdlib (zlib, math). seed 1583.
"""
import json,re,math,zlib,random,collections,unicodedata
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w="".join(c for c in unicodedata.normalize("NFD",str(w)) if unicodedata.category(c)!="Mn")
    return re.sub(r"[^a-z]","",w.lower())
V=set("aeiou")

# --- corpora ---
grd=json.load(open(ROOT+r"\engine\data\loagaeth_grades_simples.json",encoding="utf-8"))
book=[]; f1words=[]
for k in grd:
    if k and k[0].isdigit():
        for ln in grd[k]:
            s=norm(ln)
            if s: book.append(s)
for k in ("1a","1b"):
    for ln in grd[k]: f1words+=[norm(w) for w in ln.split() if len(norm(w))>=1]
LOAG="".join(book)
ch=json.load(open(ROOT+r"\engine\data\chamadas.json",encoding="utf-8"))
callwords=[]
for c in ch["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        if k: callwords.append(k)
CALLS="".join(callwords)

LATIN=norm("""in principio creavit deus caelum et terram terra autem erat inanis et vacua et tenebrae
super faciem abyssi et spiritus dei ferebatur super aquas dixitque deus fiat lux et facta est lux
et vidit deus lucem quod esset bona et divisit lucem a tenebris appellavitque lucem diem et tenebras
noctem factumque est vespere et mane dies unus dixit quoque deus fiat firmamentum in medio aquarum""")
HEBREW=norm("""bereshit bara elohim et hashamayim veet haarets vehaarets hayetah tohu vavohu vechoshech
al penei tehom veruach elohim merachefet al penei hamayim vayomer elohim yehi or vayehi or vayar
elohim et haor ki tov vayavdel elohim bein haor uvein hachoshech""")
GREEK=norm("""en archi en o logos kai o logos en pros ton theon kai theos en o logos outos en en archi
pros ton theon panta di autou egeneto kai choris autou egeneto ode en o gegonen en auto zoe en kai
i zoe en to phos ton anthropon kai to phos en ti skotia fainei""")
ENGLISH=norm("""in the beginning god created the heaven and the earth and the earth was without form
and void and darkness was upon the face of the deep and the spirit of god moved upon the face of the
waters and god said let there be light and there was light and god saw the light that it was good""")
RANDOM="".join(random.choice(LOAG) for _ in range(len(LATIN)))

def H(s,k):  # entropia condicional de ordem k (bits/letra)
    ctx=collections.Counter(); joint=collections.Counter()
    for i in range(len(s)-k):
        c=s[i:i+k]; ctx[c]+=1; joint[s[i:i+k+1]]+=1
    h=0; tot=sum(joint.values())
    for g,n in joint.items():
        p=n/tot; pc=n/ctx[g[:k]]; h-=p*math.log2(pc)
    return h
def zipf(words):
    c=collections.Counter(words); r=sorted(c.values(),reverse=True)
    xs=[math.log(i+1) for i in range(len(r))]; ys=[math.log(v) for v in r]
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    b=sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/sum((x-mx)**2 for x in xs)
    return b  # inclinacao (~-1 em lingua)
def heaps(words):
    seen=set(); N=[]; Vv=[]
    for i,w in enumerate(words):
        seen.add(w);
        if (i+1)%50==0: N.append(math.log(i+1)); Vv.append(math.log(len(seen)))
    if len(N)<3: return float('nan')
    n=len(N); mx=sum(N)/n; my=sum(Vv)/n
    return sum((N[i]-mx)*(Vv[i]-my) for i in range(n))/sum((x-mx)**2 for x in N)  # beta (~0.4-0.6)
def menzerath(words):
    # correlacao: comprimento da palavra vs tamanho medio do grupo vocalico (deve ser NEGATIVA em lingua)
    xs=[];ys=[]
    for w in words:
        if len(w)<2: continue
        groups=re.findall(r"[aeiou]+|[^aeiou]+",w)
        xs.append(len(w)); ys.append(sum(len(g) for g in groups)/len(groups))
    if len(xs)<5: return float('nan')
    n=len(xs); mx=sum(xs)/n; my=sum(ys)/n
    den=(sum((x-mx)**2 for x in xs)*sum((y-my)**2 for y in ys))**.5
    return sum((xs[i]-mx)*(ys[i]-my) for i in range(n))/den if den else 0

print("=== ZIPF (inclinação rank-freq; língua ~ -1) ===")
print(f"  folha1 palavras: {zipf(f1words):.2f}   Chamadas: {zipf(callwords):.2f}")
print("=== HEAPS (beta vocabulário; língua ~0.4-0.6) ===")
print(f"  folha1: {heaps(f1words):.2f}   Chamadas: {heaps(callwords):.2f}")
print("=== MENZERATH (corr comprimento×grupo; língua NEGATIVA) ===")
print(f"  folha1: {menzerath(f1words):+.2f}   Chamadas: {menzerath(callwords):+.2f}   latim: {menzerath(LATIN.split()):+.2f}")
print("\n=== ENTROPIA condicional (bits/letra) por ordem ===")
corp={"LOAG":LOAG[:4000],"Chamadas":CALLS[:4000],"latim":LATIN,"hebraico":HEBREW,"inglês":ENGLISH,"aleatório":RANDOM}
print(f"  {'corpus':<10} H0    H1    H2    H3")
for nm,s in corp.items():
    print(f"  {nm:<10} "+"  ".join(f"{H(s,k):.2f}" for k in range(4)))

print("\n=== NCD (distância por compressão; 0=idêntico, 1=sem relação) ===")
def C(s): return len(zlib.compress(s.encode(),9))
def ncd(a,b):
    ca,cb=C(a),C(b); cab=C(a+b); return (cab-min(ca,cb))/max(ca,cb)
L=min(len(LATIN),len(HEBREW),len(GREEK),len(ENGLISH),900)
samp={"LOAG":LOAG[:L],"Chamadas":CALLS[:L],"latim":LATIN[:L],"hebraico":HEBREW[:L],"grego":GREEK[:L],"inglês":ENGLISH[:L],"aleatório":RANDOM[:L]}
print("  vizinho mais próximo de cada um:")
for a in samp:
    ds=sorted(((ncd(samp[a],samp[b]),b) for b in samp if b!=a))
    print(f"    {a:<10} -> {ds[0][1]} ({ds[0][0]:.3f}) | {ds[1][1]} ({ds[1][0]:.3f})")
print("\n  distâncias do LOAG:")
for b in samp:
    if b!="LOAG": print(f"    LOAG–{b:<10} {ncd(samp['LOAG'],samp[b]):.3f}")
