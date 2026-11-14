# -*- coding: utf-8 -*-
"""
a169 — O que SAO as particulas (grupo B) da folha 1 e pra que servem?
Tres populacoes: A=glosadas(sentido), B=particulas(curtas recorrentes), C=nomes.
Hipotese H1 (morfologia): B = pecas do gerador de nomes (afixos/raizes/fragmentos).
Hipotese H2 (gramatica): B = classe-funcao independente (como artigos/preposicoes).
Testes discriminam, cada um contra um null. seed 1583.
"""
import json, re, collections, os, random, math
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=[norm(n) for n in fg["real_names"]]
PREF=[p.lower() for p in fg["prefixes"]]
SUFF=[s.lower() for s in fg["suffixes"]]
ROOTS=[r.lower() for r in fg["roots"]]
AFFIX=set(PREF)|set(SUFF)

# glosas (grupo A)
d=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
gloss={}
for c in d["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        gl=(p.get("ingles_sl3191") or "").strip()
        if len(k)>=2 and gl and not re.fullmatch(r"[\d:.\- ]+", gl): gloss.setdefault(k,gl)

# corpus folha 1
g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
lines=[]
for key in ("1a","1b"):
    for ln in g[key]:
        toks=[norm(w) for w in ln.split()]
        toks=[t for t in toks if len(t)>=2]
        if toks: lines.append(toks)
alltok=[t for ln in lines for t in ln]
F=collections.Counter(alltok)

A=set(w for w in F if w in gloss)
B=set(w for w in F if w not in gloss and len(w)<=3 and F[w]>=2)
C=set(w for w in F if w not in A and w not in B)

# letras para nulls (freq do corpus)
letpool="".join(alltok)
def rand_like(tok):
    return "".join(random.choice(letpool) for _ in tok)

print(f"A={len(A)} tipos  B={len(B)} tipos  C={len(C)} tipos")
print(f"B tokens={sum(F[w] for w in B)}  ({100*sum(F[w] for w in B)/len(alltok):.0f}% do corpus)\n")

res={}

# ---- T1: B sao afixos conhecidos do gerador de nomes? ----
def is_affix(w): return w in AFFIX
realA=sum(1 for w in B if is_affix(w))
NTRIAL=2000
nullA=[]
for _ in range(NTRIAL):
    c=sum(1 for w in B if rand_like(w) in AFFIX)
    nullA.append(c)
mu=sum(nullA)/NTRIAL; sd=(sum((x-mu)**2 for x in nullA)/NTRIAL)**.5
z=(realA-mu)/sd if sd else 0
res["T1_affix_exact"]={"real":realA,"null_mu":round(mu,2),"z":round(z,1),
    "lista":sorted(w for w in B if is_affix(w))}
print(f"T1 afixo-exato: {realA}/{len(B)} particulas SAO prefixo/sufixo da Forja | null {mu:.1f} z={z:+.1f}")
print(f"   {sorted(w for w in B if is_affix(w))}\n")

# ---- T2: B sao borda (prefixo/sufixo) de algum nome real? ----
def edge_of_name(w):
    for n in NAMES:
        if n!=w and (n.startswith(w) or n.endswith(w)): return True
    return False
def sub_of_name(w):
    for n in NAMES:
        if n!=w and w in n: return True
    return False
realE=sum(1 for w in B if edge_of_name(w))
realS=sum(1 for w in B if sub_of_name(w))
nullE=[];nullS=[]
for _ in range(NTRIAL):
    rs=[rand_like(w) for w in B]
    nullE.append(sum(1 for r in rs if edge_of_name(r)))
    nullS.append(sum(1 for r in rs if sub_of_name(r)))
def zof(real,null):
    mu=sum(null)/len(null); sd=(sum((x-mu)**2 for x in null)/len(null))**.5
    return mu,(real-mu)/sd if sd else 0
muE,zE=zof(realE,nullE); muS,zS=zof(realS,nullS)
res["T2_edge_of_name"]={"real":realE,"null_mu":round(muE,1),"z":round(zE,1),"frac":round(realE/len(B),2)}
res["T2_substr_of_name"]={"real":realS,"null_mu":round(muS,1),"z":round(zS,1),"frac":round(realS/len(B),2)}
print(f"T2 borda-de-nome: {realE}/{len(B)} ({100*realE/len(B):.0f}%) | null {muE:.1f} z={zE:+.1f}")
print(f"   substring-de-nome: {realS}/{len(B)} ({100*realS/len(B):.0f}%) | null {muS:.1f} z={zS:+.1f}\n")

# ---- T3: prefixo produtivo (c + stem onde stem tambem e token) ----
# para cada consoante inicial, quantos B=c+resto onde 'resto' tambem e token atestado
tokall=set(F)
prod={}
for w in B:
    if len(w)>=2:
        head,tail=w[0],w[1:]
        if head in fg["consonants"][0].lower()+"".join(fg["consonants"]).lower():
            if tail in tokall:
                prod.setdefault(head,[]).append(w)
realP=sum(len(v) for v in prod.values())
# null: mesma contagem sobre strings aleatorias
nullP=[]
for _ in range(NTRIAL):
    cnt=0
    for w in B:
        r=rand_like(w)
        if len(r)>=2 and r[1:] in tokall: cnt+=1
    nullP.append(cnt)
muP,zP=zof(realP,nullP)
topprod={k:len(v) for k,v in sorted(prod.items(),key=lambda x:-len(x[1]))}
res["T3_productive_prefix"]={"real":realP,"null_mu":round(muP,1),"z":round(zP,1),"por_inicial":topprod}
print(f"T3 prefixo+stem(atestado): {realP}/{len(B)} | null {muP:.1f} z={zP:+.1f}")
print(f"   por inicial: {topprod}\n")

# ---- T4: fonotatica — B mais perto de A (gramatica) ou C (nomes)? ----
def bigram_vec(words):
    c=collections.Counter()
    for w in words:
        s="^"+w+"$"
        for i in range(len(s)-1): c[s[i:i+2]]+=1
    t=sum(c.values())
    return {k:v/t for k,v in c.items()}
def cos(a,b):
    keys=set(a)|set(b); dot=sum(a.get(k,0)*b.get(k,0) for k in keys)
    na=math.sqrt(sum(v*v for v in a.values())); nb=math.sqrt(sum(v*v for v in b.values()))
    return dot/(na*nb) if na and nb else 0
vA=bigram_vec(A); vB=bigram_vec(B); vC=bigram_vec(C)
cBA=cos(vB,vA); cBC=cos(vB,vC)
res["T4_phonotactics"]={"cos_B_A":round(cBA,3),"cos_B_C":round(cBC,3),
    "mais_perto":"C_nomes" if cBC>cBA else "A_gramatica"}
print(f"T4 fonotatica: cos(B,A_gloss)={cBA:.3f}  cos(B,C_nomes)={cBC:.3f}  -> B mais perto de {'C(nomes)' if cBC>cBA else 'A(gramatica)'}\n")

# ---- T5: vies posicional (gramatica prende em borda de linha) ----
def pos_bias(S):
    # fracao de ocorrencias de tokens da classe em INICIO ou FIM de linha
    tot=ini=fim=0
    for ln in lines:
        for i,t in enumerate(ln):
            if t in S:
                tot+=1
                if i==0: ini+=1
                if i==len(ln)-1: fim+=1
    return tot,ini/tot if tot else 0,fim/tot if tot else 0
for name,S in (("A_gloss",A),("B_part",B),("C_nome",C)):
    tot,fi,ff=pos_bias(S)
    print(f"T5 {name}: inicio={fi:.2f} fim={ff:.2f} (base~{1/ (sum(len(l) for l in lines)/len(lines)):.2f})")
    res.setdefault("T5_position",{})[name]={"ini":round(fi,2),"fim":round(ff,2)}

# veredito
H1 = (zE>3 or z>3) and cBC>cBA
res["veredito"]={
 "H1_morfologia_de_nome": bool(H1),
 "resumo": "B = pecas do gerador de nomes (afixos/fragmentos), nao classe-funcao" if H1 else "indefinido"
}
print("\nVEREDITO:", res["veredito"]["resumo"])
json.dump(res, open(os.path.join(ROOT,"results","169_particle_function.json"),"w"),ensure_ascii=False,indent=1)
print("saved results/169_particle_function.json")
