# -*- coding: utf-8 -*-
"""
a162 — As palavras da folha 1 tem SINTAXE? (ordem importa, ou e so saco de palavras?)

Corpus: folha 1 (1a+1b), 98 linhas, ordem preservada, palavras separadas por espaco pelo Dee.
Testes:
  S1. Colocacao: pares adjacentes (bigramas de palavra) que repetem 2+x.
      Null = embaralhar a ORDEM das palavras (preserva multiconjunto). Se sintaxe,
      bigramas recorrentes > null.
  S2. Previsibilidade: entropia condicional media H(prox | atual) sobre palavras
      recorrentes, vs ordem embaralhada. Menor entropia = ordem carrega informacao.
  S3. Posicao na linha: palavras traduzidas/recorrentes preferem inicio ou fim de linha?
      (teste sinal vs 50/50 na metade da linha).
"""
import json, re, random, collections, math, os
random.seed(1583)
ROOT = r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"

def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
lines=[]
for key in ("1a","1b"):
    for ln in g[key]:
        toks=[norm(w) for w in ln.split()]
        toks=[t for t in toks if len(t)>=2]
        if toks: lines.append(toks)
stream=[t for ln in lines for t in toks_ for toks_ in [ln] for t in [t]] if False else [t for ln in lines for t in ln]
# simpler:
stream=[t for ln in lines for t in ln]
N=len(stream); types=collections.Counter(stream)
print(f"linhas={len(lines)} tokens={N} tipos={len(types)}")

# ---------- S1: colocacao (bigramas recorrentes) ----------
def bigrams(seq_lines):
    b=collections.Counter()
    for ln in seq_lines:
        for i in range(len(ln)-1):
            b[(ln[i],ln[i+1])]+=1
    return b
real_b=bigrams(lines)
real_recur_bg=sum(1 for p,c in real_b.items() if c>=2)

# null: embaralhar a ordem de TODAS as palavras, re-quebrar nos mesmos tamanhos de linha
flat=stream[:]
lens=[len(ln) for ln in lines]
def shuffled_lines():
    random.shuffle(flat)
    out=[]; i=0
    for L in lens:
        out.append(flat[i:i+L]); i+=L
    return out
nb=[]
for _ in range(2000):
    nb.append(sum(1 for p,c in bigrams(shuffled_lines()).items() if c>=2))
mu=sum(nb)/len(nb); sd=(sum((x-mu)**2 for x in nb)/len(nb))**0.5
z=(real_recur_bg-mu)/sd if sd else 0
print(f"\nS1 bigramas recorrentes (2+x): real={real_recur_bg}  null={mu:.0f}+-{sd:.1f}  z={z:+.1f}")
print("   top bigramas:", ", ".join(f"{a}+{b}:{c}" for (a,b),c in real_b.most_common(12)))

# ---------- S2: entropia condicional (ordem carrega info?) ----------
def cond_entropy(seq_lines):
    nxt=collections.defaultdict(collections.Counter)
    for ln in seq_lines:
        for i in range(len(ln)-1):
            nxt[ln[i]][ln[i+1]]+=1
    tot=0.0; wsum=0
    for w,cc in nxt.items():
        s=sum(cc.values())
        if s<3: continue   # so palavras com >=3 ocorrencias de transicao
        H=-sum((n/s)*math.log2(n/s) for n in cc.values())
        tot+=H*s; wsum+=s
    return tot/wsum if wsum else 0
realH=cond_entropy(lines)
nH=[cond_entropy(shuffled_lines()) for _ in range(500)]
muH=sum(nH)/len(nH); sdH=(sum((x-muH)**2 for x in nH)/len(nH))**0.5
zH=(realH-muH)/sdH if sdH else 0
print(f"\nS2 entropia H(prox|atual): real={realH:.2f} bits  null={muH:.2f}+-{sdH:.2f}  z={zH:+.1f} (negativo=ordem informa)")

# ---------- S3: posicao na linha ----------
# fracao posicional media (0=inicio,1=fim) por palavra; teste contra 0.5
pos=collections.defaultdict(list)
for ln in lines:
    L=len(ln)
    if L<2: continue
    for i,w in enumerate(ln):
        pos[w].append(i/(L-1))
known={"ol":"eu/I","ar":"that","od":"and","de":"of","om":"know","vors":"over","iad":"God",
       "la":"first","ca":"therefore","par":"in-them","ors":"with-dark","geh":"art","lap":"for","mad":"God"}
print("\nS3 posicao media na linha (0=inicio 1=fim), palavras traduzidas + top recorrentes:")
cand=list(known)+[w for w,_ in types.most_common(25) if w not in known]
for w in cand:
    if w in pos and len(pos[w])>=4:
        m=sum(pos[w])/len(pos[w]); n=len(pos[w])
        tag=known.get(w,"")
        bias="INICIO" if m<0.38 else ("FIM" if m>0.62 else "meio")
        print(f"   {w:<6} n={n:<3} pos={m:.2f} {bias:<7} {tag}")

json.dump({"lines":len(lines),"tokens":N,"S1_real":real_recur_bg,"S1_null":mu,"S1_z":z,
           "S2_realH":realH,"S2_nullH":muH,"S2_z":zH,
           "top_bigrams":[[f"{a}+{b}",c] for (a,b),c in real_b.most_common(20)]},
          open(os.path.join(ROOT,"results","162_folha1_syntax.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/162_folha1_syntax.json")
