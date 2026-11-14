# -*- coding: utf-8 -*-
"""
a172 — PONTES: o Loag se liga aos outros sistemas enoquianos?
Testa se os nomes de cada sistema (governadores 91, aethyrs 30, torres,
heptarquia, palavras das Chamadas) aparecem como SUBSTRING no livro inteiro
(48 folhas), contra null pareado por tamanho/letras. Mede regiao e raizes. seed 1583.
"""
import json, re, os, random, collections
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=str(w).lower()
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)
def upwords(obj):
    """tokens MAIUSCULOS len>=4 em qualquer subtree (nomes enoquianos)."""
    out=[]
    def walk(o):
        if isinstance(o,str):
            for t in re.split(r"[^A-Za-z]+",o):
                if len(t)>=4 and t.isupper(): out.append(norm(t))
        elif isinstance(o,dict):
            for v in o.values(): walk(v)
        elif isinstance(o,list):
            for v in o: walk(v)
    walk(obj); return out

G=json.load(open(os.path.join(ROOT,"engine","data","governadores.json"),encoding="utf-8"))
H=json.load(open(os.path.join(ROOT,"engine","data","heptarquia.json"),encoding="utf-8"))
CH=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
ROOTS=[r.lower() for r in fg["roots"]]

systems={}
systems["GOV_91"]=sorted(set(norm(r["nome"]) for r in G["governadores"] if r.get("nome")))
systems["AETHYR"]=sorted(set(norm(r.get("nome_dee_confirmado_em_fonte_primaria","")) for r in G["aethyrs"]))
# lineas das torres
tl=[]
for v in G["torres"].values():
    for t in re.split(r"\s+", v.get("linea_spiritus_sancti","")):
        if len(norm(t))>=4: tl.append(norm(t))
systems["TORRE_linea"]=sorted(set(tl))
systems["HEPT"]=sorted(set(upwords(H["reis_e_principes"])+upwords(H.get("nomes_derivados_das_tabelas",[]))+upwords(H.get("tabula_collecta",[]))))
callw=set()
for c in CH["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        if len(k)>=4: callw.add(k)
systems["CALL"]=sorted(callw)

# livro inteiro: por linha, letras concatenadas
grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
faces=[k for k in grd if k and k[0].isdigit()]
book_lines=[]   # (folha_idx, letras_da_linha)
for k in faces:
    folha=int(re.match(r"(\d+)",k).group(1))
    for ln in grd[k]:
        s=norm(ln)
        if s: book_lines.append((folha,s))
BOOK="".join(s for _,s in book_lines)
letpool=BOOK
def hit_in_book(name):
    for _,s in book_lines:
        if name in s: return True
    return False

print(f"Livro: {len(faces)} lados, {len(book_lines)} linhas, {len(BOOK)} letras\n")

def rand_like(n): return "".join(random.choice(letpool) for _ in n)

NT=500
res={}
for sysname,names in systems.items():
    names=[n for n in names if len(n)>=4]
    if not names: continue
    real=sum(1 for n in names if hit_in_book(n))
    nulls=[]
    for _ in range(NT):
        nulls.append(sum(1 for n in names if hit_in_book(rand_like(n))))
    mu=sum(nulls)/NT; sd=(sum((x-mu)**2 for x in nulls)/NT)**.5
    z=(real-mu)/sd if sd else 0
    res[sysname]={"n":len(names),"hits_real":real,"null_mu":round(mu,1),"z":round(z,1),
                  "frac":round(real/len(names),2)}
    print(f"{sysname:<12} {real:>3}/{len(names):<3} batem ({100*real/len(names):>3.0f}%) | null {mu:5.1f} z={z:+5.1f}")

# regiao: onde batem (por terco do livro) — usa GOV_91 e CALL
def region_profile(names):
    folhas=sorted(set(f for f,_ in book_lines))
    import bisect
    prof=collections.Counter()
    for n in names:
        if len(n)<4: continue
        for f,s in book_lines:
            if n in s:
                prof[f]+=1
    return prof
print()
for sysname in ("GOV_91","CALL","HEPT"):
    prof=region_profile([n for n in systems[sysname] if len(n)>=4])
    if prof:
        top=prof.most_common(6)
        print(f"{sysname} regiao (folha:hits): {', '.join(f'{f}:{c}' for f,c in top)}")

# raizes do gerador x nomes dos sistemas
print("\nRaizes do gerador dentro dos nomes dos sistemas:")
for sysname,names in systems.items():
    cnt=collections.Counter()
    for n in names:
        for r in ROOTS:
            if r in n: cnt[r]+=1
    if cnt: print(f"  {sysname}: {dict(cnt.most_common())}")

json.dump(res, open(os.path.join(ROOT,"results","172_bridges.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/172_bridges.json")
