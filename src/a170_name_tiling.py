# -*- coding: utf-8 -*-
"""
a170 — CONFIRMA: os 90 nomes reais se decompoem nas pecas curtas atestadas?
Se a folha 1 lista pecas (B particulas + afixos + raizes), os nomes das grades
devem 'ladrilhar' bem com essas pecas. Null = vocabulario aleatorio do mesmo tamanho.
seed 1583.
"""
import json, re, os, random, collections
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower()
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=[norm(n) for n in fg["real_names"]]
AFF=[a.lower() for a in fg["prefixes"]+fg["suffixes"]]
RTS=[r.lower() for r in fg["roots"]]

g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
alltok=[]
for key in ("1a","1b"):
    for ln in g[key]: alltok+=[norm(w) for w in ln.split()]
F=collections.Counter(t for t in alltok if len(t)>=2)
gloss_keys=set()  # excluir glosadas para isolar B
d=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
for c in d["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        if len(k)>=2: gloss_keys.add(k)
B=[w for w in F if w not in gloss_keys and len(w)<=3 and F[w]>=2]

# vocabulario de pecas atestadas (B + afixos + raizes), 2+ letras
V=set(w for w in B+AFF+RTS if len(w)>=2)

def tile(name,vocab):
    """greedy longest-match left->right; retorna letras cobertas por pecas do vocab."""
    i=0; cov=0; pieces=[]
    maxlen=max((len(v) for v in vocab),default=0)
    while i<len(name):
        matched=None
        for L in range(min(maxlen,len(name)-i),1,-1):
            if name[i:i+L] in vocab:
                matched=name[i:i+L]; break
        if matched:
            pieces.append(matched); cov+=len(matched); i+=len(matched)
        else:
            i+=1  # letra nao coberta
    return cov,pieces

# real
tot_letters=sum(len(n) for n in NAMES)
cov_real=sum(tile(n,V)[0] for n in NAMES)
full_real=sum(1 for n in NAMES if tile(n,V)[0]==len(n))
print(f"Vocabulario de pecas atestadas: {len(V)} unidades")
print(f"REAL: cobertura {100*cov_real/tot_letters:.0f}% das letras | {full_real}/{len(NAMES)} nomes 100% ladrilhados\n")

# null: vocabulario aleatorio, mesma distribuicao de tamanhos, letras do corpus
letpool="".join(t for t in alltok if len(t)>=2)
sizes=[len(v) for v in V]
NTRIAL=1000
covs=[];fulls=[]
for _ in range(NTRIAL):
    Vr=set("".join(random.choice(letpool) for _ in range(s)) for s in sizes)
    c=sum(tile(n,Vr)[0] for n in NAMES)
    f=sum(1 for n in NAMES if tile(n,Vr)[0]==len(n))
    covs.append(c);fulls.append(f)
mu=sum(covs)/NTRIAL; sd=(sum((x-mu)**2 for x in covs)/NTRIAL)**.5
z=(cov_real-mu)/sd if sd else 0
muf=sum(fulls)/NTRIAL
print(f"NULL cobertura: {100*mu/tot_letters:.0f}% das letras (z={z:+.1f})")
print(f"NULL 100%-ladrilhados: {muf:.1f}/{len(NAMES)}  (real {full_real})\n")

# exemplos
print("Exemplos de decomposicao:")
for n in ["nochastor","adnochapha","zichastora","antantoxal","achadax","gr",]:
    if n in [x for x in NAMES] or True:
        c,p=tile(n,V); print(f"  {n:<12} = {' + '.join(p) if p else '(nada)'}  [{100*c/len(n):.0f}%]")

json.dump({"vocab_size":len(V),"cov_real_pct":round(100*cov_real/tot_letters,1),
  "cov_null_pct":round(100*mu/tot_letters,1),"z_cov":round(z,1),
  "full_real":full_real,"full_null":round(muf,1),"n_names":len(NAMES)},
  open(os.path.join(ROOT,"results","170_name_tiling.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/170_name_tiling.json")
