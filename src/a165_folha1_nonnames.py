# -*- coding: utf-8 -*-
"""
a165 — Da folha 1, o que NAO e nome? E tem significado?
Tiers honestos:
  A. COM significado  = tem glosa (nao-numerica) nas Chamadas. Nao e nome.
  B. SEM significado conhecido, mas forma de particula = curta (<=3) e recorrente (>=2x),
     sem glosa. Provavel palavra gramatical, sentido desconhecido.
  C. Resto = nomes / palavras longas (campo de nomes).
"""
import json, re, collections, os
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

d=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
gloss={}
for c in d["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        gl=(p.get("ingles_sl3191") or "").strip()
        if len(k)>=2 and gl and not re.fullmatch(r"[\d:.\- ]+", gl):
            gloss.setdefault(k, gl)

g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
toks=[]
for key in ("1a","1b"):
    for ln in g[key]:
        toks+=[norm(w) for w in ln.split()]
toks=[t for t in toks if len(t)>=2]
T=collections.Counter(toks)

A={w:gloss[w] for w in T if w in gloss}
B={w:T[w] for w in T if w not in gloss and len(w)<=3 and T[w]>=2}
rest=[w for w in T if w not in A and w not in B]

print(f"folha 1: {len(toks)} tokens, {len(T)} tipos\n")
print(f"A. COM significado (glosa das Chamadas) = {len(A)} tipos, {sum(T[w] for w in A)} tokens")
for w,gl in sorted(A.items(), key=lambda x:-T[x[0]]):
    print(f"   {w:<8} {T[w]:>3}x  = {gl}")

print(f"\nB. SEM significado conhecido, forma de particula (<=3 letras, 2+x) = {len(B)} tipos, {sum(B.values())} tokens")
for w,c in sorted(B.items(), key=lambda x:-x[1]):
    print(f"   {w:<6} {c:>3}x", end="   ")
print()

print(f"\nC. resto (nomes / palavras longas) = {len(rest)} tipos, {sum(T[w] for w in rest)} tokens")
# amostra dos recorrentes longos (provaveis nomes recorrentes)
longrec=sorted([w for w in rest if T[w]>=2 and len(w)>=4], key=lambda w:-T[w])[:20]
print("   recorrentes longos (provaveis nomes):", ", ".join(f"{w}({T[w]})" for w in longrec))

json.dump({"A_meaning":{w:[T[w],gl] for w,gl in A.items()},
           "B_particle_nogloss":{w:c for w,c in sorted(B.items(),key=lambda x:-x[1])},
           "C_rest_count":len(rest)},
          open(os.path.join(ROOT,"results","165_folha1_nonnames.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/165_folha1_nonnames.json")
