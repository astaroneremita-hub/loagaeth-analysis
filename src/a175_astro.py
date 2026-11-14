# -*- coding: utf-8 -*-
"""
a175 — O Loag tem estrutura astrologica PROPRIA? Usa a atribuicao do proprio Loag
(forge_grammar.letters: elemento + planeta por letra). Testa se as 48 folhas CICLAM
em 12 (zodiaco) ou 7 (planetas), via autocorrelacao do perfil por folha vs null
(shuffle da ordem das folhas). Exploratorio e sujeito a pareidolia -> null rigoroso. seed 1583.
"""
import json, re, os, random, collections, math
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
LET=fg["letters"]  # {A:{e:Terra,p:Venus},...}
def norm(w):
    return re.sub(r"[^a-z]","",str(w).lower())

grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))
# por folha (1..48) junta os dois lados, conta elemento e planeta das letras
ELEM=["Fogo","Terra","Ar","Agua"];
PLAN=sorted(set(v["p"] for v in LET.values() if v["p"] not in ("-","?")))
folhas=sorted(set(int(re.match(r"(\d+)",k).group(1)) for k in grd if k and k[0].isdigit()))
def profile(folha,kind):
    cnt=collections.Counter()
    for side in ("a","b"):
        key=f"{folha}{side}"
        if key in grd:
            for ln in grd[key]:
                for ch in norm(ln).upper():
                    if ch in LET:
                        val=LET[ch][kind]
                        if val not in ("-","?","?"): cnt[val]+=1
    return cnt
def vec(folha,kind,cats):
    c=profile(folha,kind); t=sum(c.values()) or 1
    return [c.get(x,0)/t for x in cats]

def cos(a,b):
    d=sum(x*y for x,y in zip(a,b)); na=math.sqrt(sum(x*x for x in a)); nb=math.sqrt(sum(y*y for y in b))
    return d/(na*nb) if na and nb else 0

def autocorr(series,lag):
    n=len(series); vals=[cos(series[i],series[(i+lag)%n]) for i in range(n)]
    return sum(vals)/len(vals)

print(f"folhas={len(folhas)}  elementos={ELEM}  planetas={len(PLAN)}\n")
res={}
for kind,cats,name in (("e",ELEM,"ELEMENTO"),("p",PLAN,"PLANETA")):
    series=[vec(f,kind,cats) for f in folhas]
    for lag,label in ((12,"zodiaco-12"),(7,"planeta-7"),(4,"ctrl-4"),(1,"vizinho-1")):
        real=autocorr(series,lag)
        nul=[]
        for _ in range(2000):
            idx=list(range(len(series))); random.shuffle(idx)
            sh=[series[i] for i in idx]
            nul.append(autocorr(sh,lag))
        mu=sum(nul)/len(nul); sd=(sum((x-mu)**2 for x in nul)/len(nul))**.5
        z=(real-mu)/sd if sd else 0
        print(f"{name:<9} lag {lag:>2} ({label:<11}): autocorr={real:.3f} null={mu:.3f} z={z:+.1f}")
        res[f"{name}_lag{lag}"]={"real":round(real,3),"null":round(mu,3),"z":round(z,1)}
    print()

# gradiente conhecido (sanity): proporcao de A-element (Terra) por folha, tendencia
terra=[vec(f,"e",ELEM)[ELEM.index("Terra")] for f in folhas]
# correlacao com indice (tendencia linear)
n=len(terra); mx=(n-1)/2; my=sum(terra)/n
sxy=sum((i-mx)*(terra[i]-my) for i in range(n)); sxx=sum((i-mx)**2 for i in range(n))
slope=sxy/sxx if sxx else 0
print(f"SANITY gradiente Terra por folha: slope={slope:+.5f}/folha (so descritivo)")

json.dump(res,open(os.path.join(ROOT,"results","175_astro.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/175_astro.json")
