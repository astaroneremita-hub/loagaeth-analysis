# -*- coding: utf-8 -*-
"""
a167 — Monta o Loag COMPLETO num doc: os NOMES (Forja) + as PALAVRAS (significado) +
as PARTICULAS, e a folha 1 inteira marcada mostrando tudo junto.
Gera docs/LOAG_COMPLETO.md
"""
import json, re, collections, os
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
names=fg["real_names"]; roots=[r.lower() for r in fg["roots"]]; LET=fg["letters"]; DOM=fg["domains"]
def elem_of(w):
    c=collections.Counter()
    for ch in w.upper():
        e=LET.get(ch,{}).get("e","?"); c[e]+=1
    return c.most_common(1)[0][0] if c else "?"
def root_of(w):
    n=w.lower()
    for r in sorted(roots,key=len,reverse=True):
        if r in n: return r.upper()
    return "-"

# glosas
d=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
gloss={}
for c in d["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        gl=(p.get("ingles_sl3191") or "").strip()
        if len(k)>=2 and gl and not re.fullmatch(r"[\d:.\- ]+", gl): gloss.setdefault(k,gl)
PT={"that":"que","I":"eu","over":"sobre","art":"és","in them.":"neles","the first":"o primeiro",
    "therefore,":"portanto","with darknes.":"com trevas","know":"saber","of":"de","nor ende":"nem fim",
    "and":"e","The Spirits":"os Espíritos","the God":"o Deus","None":"nenhum","Cursed":"Maldito",
    "vomit out":"vomitar","of the same yor God,":"do mesmo vosso Deus","a half:":"metade","sayeth":"diz","for":"para"}

g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
alltok=[]
for key in ("1a","1b"):
    for ln in g[key]: alltok+=[norm(w) for w in ln.split()]
F=collections.Counter(t for t in alltok if len(t)>=2)
def is_particle(n): return (n not in gloss) and len(n)<=3 and F.get(n,0)>=2

# nomes Forja que tocam a folha 1 (token exato ou raiz presente)
tokset=set(t for t in alltok if t)
name_roots_present=set()
for n in names:
    rt=root_of(n)
    if rt!="-" and rt.lower() in {norm(x) for x in tokset}: name_roots_present.add(rt)

O=[]
O.append("# O Loagaeth COMPLETO — nomes, palavras e partículas\n")
O.append("# The complete Loagaeth — names, words and particles\n\n")
O.append("## Resposta direta / Short answer\n")
O.append("**SIM — entre os nomes há palavras.** O Loag mistura (1) NOMES de entidades, (2) PALAVRAS-língua com significado "
         "traduzido, e (3) PARTÍCULAS curtas sem glosa. Os 90 nomes da Forja são lidos das GRADES (folhas 2-48) como tabela; "
         "a folha 1 é a página de palavras segmentadas pelo Dee, onde as palavras-língua aparecem. _Yes — there are real words among the names._\n\n")
O.append("---\n\n")

# 1. NOMES
O.append("## 1. OS NOMES (Forja) — 90 nomes reais recorrentes das grades\n")
O.append("Cada um: raiz (família), elemento dominante das letras, domínio.\n\n")
O.append("| nome | raiz | elemento | domínio |\n|---|---|---|---|\n")
for n in sorted(names, key=lambda x:(root_of(x),x)):
    e=elem_of(n); O.append(f"| {n} | {root_of(n)} | {e} | {DOM.get(e,'')} |\n")
O.append(f"\n_As 10 raízes/famílias: {', '.join(r.upper() for r in roots)}._\n")
O.append(f"_Raízes que também aparecem na folha 1 como palavra: {', '.join(sorted(name_roots_present)) or '—'}._\n\n")
O.append("---\n\n")

# 2. PALAVRAS com significado
O.append("## 2. AS PALAVRAS com significado — língua angelical traduzida (folha 1)\n\n")
O.append("| palavra | freq | inglês (Sloane 3191) | português |\n|---|---|---|---|\n")
A=[(w,F[w],gloss[w]) for w in F if w in gloss]
for w,fr,gl in sorted(A,key=lambda x:-x[1]):
    O.append(f"| {w} | {fr}x | {gl} | {PT.get(gl,gl)} |\n")
O.append("\n---\n\n")

# 3. PARTICULAS
O.append("## 3. AS PARTÍCULAS — curtas, recorrentes, sem tradução conhecida (folha 1)\n\n")
B=sorted([(w,F[w]) for w in F if is_particle(w)], key=lambda x:-x[1])
O.append(" ".join(f"`{w}`×{c}" for w,c in B) + "\n\n")
O.append(f"_{len(B)} tipos, {sum(c for _,c in B)} ocorrências. Provável camada gramatical; sentido aberto._\n\n")
O.append("---\n\n")

# 4. TEXTO folha 1 marcado
O.append("## 4. A PÁGINA 1 inteira, marcada (tudo junto)\n")
O.append("**NOME** = token que é/contém nome ou raiz da Forja · **_palavra_=sig** = palavra com significado · _itálico_ = partícula · normal = outra palavra do campo de nomes.\n\n")
for key,title in (("1a","Lado 1a"),("1b","Lado 1b")):
    O.append(f"\n### {key.upper()} — {title}\n\n")
    for i,ln in enumerate(g[key]):
        pcs=[]
        for w in ln.split():
            n=norm(w)
            if len(n)<2: pcs.append(w); continue
            rt=root_of(n)
            if n in gloss:
                gl=gloss[n]; pcs.append(f"**_{w}_**={PT.get(gl,gl)}")
            elif rt!="-" and (n in tokset and rt.lower() in n) and len(n)>=4:
                pcs.append(f"__{w.upper()}__")
            elif is_particle(n): pcs.append(f"_{w}_")
            else: pcs.append(w)
        O.append(f"**{i+1:>2}.** " + " ".join(pcs) + "\n\n")

O.append("---\n\n")
O.append("## Honesto\n")
O.append("- Os NOMES vivem nas grades 2-48 (lidos como tabela); 2 batem exato na folha 1 (anzach, geth), poucas raízes tocam a folha 1.\n")
O.append("- As PALAVRAS com significado (21) e as PARTÍCULAS (162) são da folha 1, a página segmentada em palavras pelo Dee.\n")
O.append("- A ordem das palavras NÃO forma frase (#332). O Loag LISTA; não sentencia. Significado só nas 21 (o resto é nome ou partícula de sentido aberto).\n")

path=os.path.join(ROOT,"docs","LOAG_COMPLETO.md")
open(path,"w",encoding="utf-8").write("".join(O))
print("escrito:",path)
print(f"nomes=90 palavras={len(A)} particulas={len(B)}")
