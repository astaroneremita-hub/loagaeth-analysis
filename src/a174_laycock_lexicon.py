# -*- coding: utf-8 -*-
"""
a174 — Laycock (Complete Enochian Dictionary) como lexico de validacao.
NAO guarda o texto do dicionario (copyright); so deriva: quantas palavras da folha 1
sao palavras enoquianas atestadas em Laycock, e quais. Confirma tambem que os nomes/
raizes do gerador NAO sao enoquianos (reforca #336). seed 1583.
Uso: python a174_laycock_lexicon.py "<caminho do PDF Laycock>"
"""
import sys, re, json, random, collections, os
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
PDF=sys.argv[1] if len(sys.argv)>1 else r"C:\Users\T-GAMER\Downloads\121880413-The-Complete-Enochian-Dictionary (1).pdf"
import fitz
doc=fitz.open(PDF)
LT="\n".join(doc[i].get_text() for i in range(len(doc))).lower()
LEX=set(re.findall(r"[a-z]{2,}",LT))

def norm(w):
    w=str(w).lower()
    for a,b in [("áàäâ","a"),("éèê","e"),("íìî","i"),("óòô","o"),("úùû","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)
grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
f1=[]
for k in ("1a","1b"):
    for ln in grd[k]: f1+=[norm(w) for w in ln.split()]
F=collections.Counter(t for t in f1 if len(t)>=2)
letpool="".join(t for t in f1 if len(t)>=2)
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
ROOTS=[r.lower() for r in fg["roots"]]; REAL=[norm(n) for n in fg["real_names"]]

def overlap(types,NT=1000):
    real=sum(1 for w in types if w in LEX)
    nul=[sum(1 for w in types if "".join(random.choice(letpool) for _ in w) in LEX) for _ in range(NT)]
    mu=sum(nul)/NT; sd=(sum((x-mu)**2 for x in nul)/NT)**.5
    return real,len(types),round(mu,1),round((real-mu)/sd,1) if sd else 0

res={"dic_tokens":len(LEX),"overlap":{}}
for L in (2,4,5,6):
    tp=[w for w in F if len(w)>=L]
    r,n,mu,z=overlap(tp); res["overlap"][f"len>={L}"]={"hits":r,"n":n,"null":mu,"z":z}
    print(f"folha1 len>={L}: {r}/{n} no Laycock | null {mu} z={z:+}")

# nomes/raizes NAO enoquianos (controle independente de #336)
res["roots_in_lex"]=sum(1 for r in ROOTS if r in LEX)
res["realnames_in_lex"]=sum(1 for n in REAL if n in LEX)
print(f"\nraizes do gerador no Laycock: {res['roots_in_lex']}/{len(ROOTS)}  | nomes reais: {res['realnames_in_lex']}/{len(REAL)}")

# lista usavel: palavras da folha1 (len>=5) atestadas, por freq
att=sorted([(w,F[w]) for w in F if len(w)>=5 and w in LEX], key=lambda x:-x[1])
res["attested_folha1_len5"]=[w for w,_ in att]
print(f"\n{len(att)} palavras folha1 (len>=5) atestadas no Laycock. Top 30:")
print(", ".join(f"{w}({c})" for w,c in att[:30]))
json.dump(res,open(os.path.join(ROOT,"results","174_laycock_lexicon.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/174_laycock_lexicon.json")
