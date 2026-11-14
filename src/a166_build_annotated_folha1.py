# -*- coding: utf-8 -*-
"""
a166 — Monta o TEXTO INTEIRO da folha 1 anotado, palavra a palavra:
  **palavra** = significado   -> grupo A (tem glosa nas Chamadas)
  _palavra_                   -> grupo B (particula curta recorrente, sem glosa)
  palavra                     -> nome / palavra longa (campo de nomes)
Gera docs/FOLHA1_TEXTO_ANOTADO.md
"""
import json, re, collections, os
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=w.lower().replace("-","").replace(".","").replace(":","")
    for a,b in [("áàäâå","a"),("éèêë","e"),("íìîï","i"),("óòöôøõ","o"),("úùûü","u"),("ñ","n"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)

PT={"that":"que","I":"eu","over":"sobre","over you":"sobre vós","art":"és","are":"sois",
    "in them.":"neles","the first":"o primeiro","therefore,":"portanto","with darknes.":"com trevas",
    "know":"saber","of":"de","nor ende":"nem fim","and":"e","The Spirits":"os Espíritos",
    "the God":"o Deus","None":"nenhum","Cursed":"Maldito","vomit out":"vomitar",
    "of the same yor God,":"do mesmo vosso Deus","a half:":"metade","sayeth":"diz","for":"para"}

d=json.load(open(os.path.join(ROOT,"engine","data","chamadas.json"),encoding="utf-8"))
gloss={}
for c in d["chamadas"]:
    for p in c["palavras"]:
        k=norm(p.get("chave") or "")
        gl=(p.get("ingles_sl3191") or "").strip()
        if len(k)>=2 and gl and not re.fullmatch(r"[\d:.\- ]+", gl):
            gloss.setdefault(k, gl)

g=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
# freq global folha1 para decidir grupo B
alltok=[]
for key in ("1a","1b"):
    for ln in g[key]: alltok+=[norm(w) for w in ln.split()]
F=collections.Counter(t for t in alltok if len(t)>=2)
def is_particle(n): return (n not in gloss) and len(n)<=3 and F.get(n,0)>=2

nA=nB=nC=0
out=[]
out.append("# Folha 1 do Loagaeth — texto inteiro anotado\n")
out.append("# Folha 1 of the Loagaeth — full annotated text\n")
out.append("Transcricao Sloane MS 3189, folha 1 (lados 1a e 1b), segmentada em palavras pelo proprio Dee.\n")
out.append("**Legenda / Legend:**\n")
out.append("- **palavra** = significado — palavra-lingua com glosa atestada nas Chamadas (grupo A). _word with attested meaning._\n")
out.append("- _palavra_ — particula curta recorrente, sem traducao conhecida (grupo B). _short recurrent particle, meaning unknown._\n")
out.append("- palavra — nome / palavra do campo de nomes (grupo C). _name / onomasticon word._\n")
out.append("\n---\n")

for key,title in (("1a","Lado 1a"),("1b","Lado 1b")):
    out.append(f"\n## {key.upper()} — {title}\n")
    for i,ln in enumerate(g[key]):
        pieces=[]
        for w in ln.split():
            n=norm(w)
            if len(n)<2:
                pieces.append(w); continue
            if n in gloss:
                gl=gloss[n]; pt=PT.get(gl, gl)
                pieces.append(f"**{w}**={pt}"); nA+=1
            elif is_particle(n):
                pieces.append(f"_{w}_"); nB+=1
            else:
                pieces.append(w); nC+=1
        out.append(f"**{i+1:>2}.** " + " ".join(pieces) + "\n")

out.append("\n---\n")
out.append(f"\n**Contagem:** {nA} palavras-com-significado (A) · {nB} particulas sem glosa (B) · {nC} nomes/longas (C).\n")
out.append("\n> Honesto: a ordem das palavras NAO forma frase (teste de entropia nulo, #332). ")
out.append("A folha 1 LISTA palavras de uma lingua real (as mesmas das Chamadas numa veia fina, #333), ")
out.append("nao as encadeia em sentenca. Grupo A = fato traduzido; B = provavel gramatica, sentido aberto; ")
out.append("C = campo de nomes.\n")

path=os.path.join(ROOT,"docs","FOLHA1_TEXTO_ANOTADO.md")
open(path,"w",encoding="utf-8").write("".join(out))
print("escrito:",path)
print(f"A={nA} B={nB} C={nC}  total={nA+nB+nC}")
