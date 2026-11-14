# -*- coding: utf-8 -*-
"""
a163 — O lexico-lista da folha 1 e feito da MESMA lingua das Chamadas (que tem sintaxe+traducao)?
Se sim: folha 1 = estoque de palavras; Chamadas = frases montadas com esse estoque.

Vocab das Chamadas: todas as 'chave' (enoquiano normalizado) das 19 Chamadas, com gloss.
Teste: overlap(folha1 tipos, vocab Chamadas) vs null (strings aleatorias com mesmos
comprimentos + freq de letra da folha 1, intersectadas com o mesmo vocab).
"""
import json, re, random, collections, os
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"

def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

# ---- vocab Chamadas: chave -> gloss ----
d=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
call_vocab={}
for c in d["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or p.get("enoquiano") or "")
        if len(k)>=2:
            call_vocab.setdefault(k, p.get("ingles_sl3191") or "?")
call_set=set(call_vocab)
print(f"vocab Chamadas (tipos >=2 letras): {len(call_set)}")

# ---- folha 1 tipos ----
g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
toks=[]
for key in ("1a","1b"):
    for ln in g[key]:
        toks+=[norm(w) for w in ln.split()]
toks=[t for t in toks if len(t)>=2]
f1_types=collections.Counter(toks)
f1_set=set(f1_types)
print(f"folha 1 tokens={len(toks)} tipos={len(f1_set)}")

# ---- overlap real ----
overlap=f1_set & call_set
tok_cover=sum(c for w,c in f1_types.items() if w in call_set)
print(f"\noverlap tipos: {len(overlap)}  | cobertura de tokens: {tok_cover}/{len(toks)} = {tok_cover/len(toks)*100:.0f}%")

# ---- null: strings aleatorias, mesmos comprimentos, freq de letra da folha 1 ----
letters=list("".join(toks))
tl=[len(w) for w in f1_set]
def rand_types():
    s=set()
    for L in tl:
        s.add("".join(random.choice(letters) for _ in range(L)))
    return s
no=[]
for _ in range(2000):
    no.append(len(rand_types() & call_set))
mu=sum(no)/len(no); sd=(sum((x-mu)**2 for x in no)/len(no))**0.5
z=(len(overlap)-mu)/sd if sd else 0
print(f"null overlap: {mu:.1f}+-{sd:.1f}  z={z:+.1f}")

# ---- quais palavras, ranqueadas por freq na folha 1 ----
print("\npalavras da folha 1 que SAO vocab das Chamadas (por freq na folha 1):")
rows=sorted(overlap, key=lambda w:-f1_types[w])
for w in rows[:50]:
    print(f"   {w:<10} {f1_types[w]:>3}x   = {call_vocab[w]}")

json.dump({"call_vocab":len(call_set),"f1_types":len(f1_set),"overlap":len(overlap),
           "token_coverage_pct":tok_cover/len(toks)*100,"null_mu":mu,"z":z,
           "words":[[w,f1_types[w],call_vocab[w]] for w in rows]},
          open(os.path.join(ROOT,"results","163_folha1_vs_calls.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/163_folha1_vs_calls.json")
