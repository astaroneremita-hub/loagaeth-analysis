# -*- coding: utf-8 -*-
"""
a168 — Folha 1 LIDA: substitui cada palavra-com-significado pela traducao,
destaca os NOMES encontrados, deixa o resto cru. Texto corrido da pagina inteira.
Gera docs/FOLHA1_LEITURA.md
"""
import json, re, collections, os
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
names=set(norm(n) for n in fg["real_names"])
roots=[r.lower() for r in fg["roots"]]
def is_name(n):
    if n in names: return True
    if len(n)>=5:
        for r in roots:
            if r in n: return True
    return False
def name_disp(w,n):
    for r in sorted(roots,key=len,reverse=True):
        if r in n: return w.upper()
    return w.upper()

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

O=[]
O.append("# Folha 1 do Loagaeth — LIDA\n\n")
O.append("Cada palavra: **_significado_** (quando traduzível) · **NOME** (maiúsculo, nome/raiz da Forja) · resto = palavra crua (nome desconhecido ou partícula).\n\n")
O.append("> Honesto: NÃO é frase gramatical (a ordem não encadeia, #332) — é a página lida palavra a palavra, trocando o que tem sentido e destacando os nomes.\n\n---\n\n")
nA=nN=0
for key,title in (("1a","Lado 1a"),("1b","Lado 1b")):
    O.append(f"## {key.upper()} — {title}\n\n")
    for i,ln in enumerate(g[key]):
        pcs=[]
        for w in ln.split():
            n=norm(w)
            if len(n)<2: continue
            if n in gloss:
                gl=gloss[n]; pcs.append(f"**_{PT.get(gl,gl)}_**"); nA+=1
            elif is_name(n):
                pcs.append(f"**{name_disp(w,n)}**"); nN+=1
            else:
                pcs.append(w)
        O.append(f"**{i+1:>2}.** " + " ".join(pcs) + "\n\n")
O.append("---\n\n")
O.append(f"**{nA} palavras traduzidas · {nN} nomes destacados.** As demais seguem cruas (nomes desconhecidos / partículas sem glosa).\n")
path=os.path.join(ROOT,"docs","FOLHA1_LEITURA.md")
open(path,"w",encoding="utf-8").write("".join(O))
print("escrito:",path, "| traduzidas",nA,"nomes",nN)
