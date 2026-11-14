# -*- coding: utf-8 -*-
"""
a161 — As palavras QUE SOBRARAM da folha 1 (fora o vocabulario traduzido das Chamadas):
sao palavras de verdade ou lixo/segmentacao?

Testes honestos:
  T1. Recorrencia acima de null: um idioma reusa palavras. Tipos que aparecem 2+x
      devem exceder um surrogate Markov-3 do MESMO fluxo (mesmo tamanho de tokens).
  T2. Boa-formacao fonotatica: fracao de tokens que casa a fonotatica CV do livro
      (anti-hiato, consoantes/vogais do alfabeto) vs surrogate.
  T3. Estrutura morfologica: familias por edicao de 1 letra / prefixo-sufixo
      compartilhado — ha vizinhanca lexical acima do null?
  T4. Lista as top recorrentes nao-traduzidas para o olho humano julgar.
Null: embaralhar as LETRAS do fluxo concatenado e re-segmentar nos mesmos cortes
      (preserva n de tokens e comprimentos), + surrogate Markov-3 por token.
"""
import json, re, random, collections, math, os
random.seed(1583)

ROOT = r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"

# ---- vocabulario traduzido das Chamadas (para subtrair os ja-conhecidos) ----
cham = json.load(open(os.path.join(ROOT, "engine", "data", "chamadas.json"), encoding="utf-8"))
known = set()
def walk(o):
    if isinstance(o, dict):
        w = o.get("enoquiano") or o.get("enochian") or o.get("word")
        if isinstance(w, str): known.add(w.lower())
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(cham)

# ---- palavras da folha 1 ----
fw = json.load(open(os.path.join(ROOT, "viz", "folha1_palavras.json"), encoding="utf-8"))
raw = fw["words_all"]

def norm(w):
    w = w.lower()
    # tira marcas de acento/estresse e hifens de silaba, mantem letras base
    w = w.replace("-", "").replace(".", "").replace(":", "")
    w = (w.replace("á","a").replace("à","a").replace("ä","a").replace("â","a").replace("å","a")
          .replace("é","e").replace("è","e").replace("ê","e").replace("ë","e")
          .replace("í","i").replace("ì","i").replace("î","i").replace("ï","i")
          .replace("ó","o").replace("ò","o").replace("ö","o").replace("ô","o").replace("ø","o").replace("õ","o")
          .replace("ú","u").replace("ù","u").replace("û","u").replace("ü","u")
          .replace("ñ","n").replace("ç","c"))
    w = re.sub(r"[^a-z]", "", w)
    return w

toks = [norm(w) for w in raw]
toks = [t for t in toks if len(t) >= 2]          # descarta 1-letra/vazio
N = len(toks)
types = collections.Counter(toks)

# subtrai os traduzidos conhecidos
unknown = [t for t in toks if t not in known]
unk_types = collections.Counter(unknown)
print("tokens(>=2):", N, " tipos:", len(types), " tokens nao-traduzidos:", len(unknown), " tipos:", len(unk_types))

# ---------- T1: recorrencia real vs null ----------
def n_recurring(counter):
    return sum(1 for w,c in counter.items() if c >= 2)
real_recur = n_recurring(unk_types)

# null A: embaralhar letras do fluxo, re-segmentar nos mesmos comprimentos
lens = [len(t) for t in unknown]
pool = list("".join(unknown))
def shuffle_resegment():
    random.shuffle(pool)
    out=[]; i=0
    for L in lens:
        out.append("".join(pool[i:i+L])); i+=L
    return collections.Counter(out)
null_recur=[]
for _ in range(2000):
    null_recur.append(n_recurring(shuffle_resegment()))
mu=sum(null_recur)/len(null_recur)
sd=(sum((x-mu)**2 for x in null_recur)/len(null_recur))**0.5
z=(real_recur-mu)/sd if sd else 0
print(f"\nT1 recorrencia: tipos 2+x reais={real_recur}  null={mu:.1f}+-{sd:.1f}  z={z:+.1f}")

# quantos TOKENS cobertos por tipos recorrentes (massa do lexico reusado)
mass_real = sum(c for w,c in unk_types.items() if c>=2)
print(f"   tokens cobertos por tipos recorrentes: {mass_real}/{len(unknown)} = {mass_real/len(unknown)*100:.0f}%")

# ---------- T2: boa-formacao fonotatica (anti-hiato) ----------
V=set("aeiou")
def max_vowel_run(t):
    best=cur=0
    for ch in t:
        cur=cur+1 if ch in V else 0
        best=max(best,cur)
    return best
def max_cons_run(t):
    best=cur=0
    for ch in t:
        cur=cur+1 if ch not in V else 0
        best=max(best,cur)
    return best
wellformed = sum(1 for t in unknown if max_vowel_run(t)<=2 and max_cons_run(t)<=3)
# null: Markov-0 (freq de letra) gerando tokens de mesmo comprimento
letters=list("".join(unknown));
def m0_tok(L): return "".join(random.choice(letters) for _ in range(L))
null_wf=[]
for _ in range(500):
    g=[m0_tok(L) for L in lens]
    null_wf.append(sum(1 for t in g if max_vowel_run(t)<=2 and max_cons_run(t)<=3))
mu2=sum(null_wf)/len(null_wf); sd2=(sum((x-mu2)**2 for x in null_wf)/len(null_wf))**0.5
z2=(wellformed-mu2)/sd2 if sd2 else 0
print(f"\nT2 bem-formadas (CV, anti-hiato): reais={wellformed}/{len(unknown)} ({wellformed/len(unknown)*100:.0f}%)  null_M0={mu2:.0f} ({mu2/len(unknown)*100:.0f}%)  z={z2:+.1f}")

# ---------- T3: vizinhanca morfologica (familias edit-1) ----------
def edit1_neighbors(words):
    ws=set(words); cnt=0
    for w in ws:
        has=False
        # substituicao de 1 letra
        for i in range(len(w)):
            for c in "abcdefghilmnopqrstuvxz":
                if c!=w[i] and w[:i]+c+w[i+1:] in ws: has=True;break
            if has:break
        if not has:
            # prefixo/sufixo de 1 letra
            for c in "abcdefghilmnopqrstuvxz":
                if c+w in ws or w+c in ws or (len(w)>2 and (w[1:] in ws or w[:-1] in ws)): has=True;break
        cnt+= 1 if has else 0
    return cnt
distinct=list(unk_types.keys())
real_fam=edit1_neighbors(distinct)
# null: mesmo n de tipos distintos, strings Markov-0 comprimentos casados
tl=[len(w) for w in distinct]
null_fam=[]
for _ in range(300):
    g=[m0_tok(L) for L in tl]
    null_fam.append(edit1_neighbors(g))
mu3=sum(null_fam)/len(null_fam); sd3=(sum((x-mu3)**2 for x in null_fam)/len(null_fam))**0.5
z3=(real_fam-mu3)/sd3 if sd3 else 0
print(f"\nT3 tipos com vizinho edit-1: reais={real_fam}/{len(distinct)} ({real_fam/len(distinct)*100:.0f}%)  null={mu3:.0f}  z={z3:+.1f}")

# ---------- T4: top recorrentes nao-traduzidas ----------
print("\nT4 top 40 palavras nao-traduzidas recorrentes (candidatas a lexico):")
for w,c in unk_types.most_common(40):
    print(f"   {w:<14} {c}x")

# salva resultado
out={"tokens":N,"types":len(types),"unknown_tokens":len(unknown),"unknown_types":len(unk_types),
     "T1_recur_real":real_recur,"T1_null_mu":mu,"T1_z":z,"T1_mass_pct":mass_real/len(unknown)*100,
     "T2_wf_pct":wellformed/len(unknown)*100,"T2_z":z2,
     "T3_fam_pct":real_fam/len(distinct)*100,"T3_z":z3,
     "top40":unk_types.most_common(40)}
json.dump(out, open(os.path.join(ROOT,"results","161_folha1_wordhood.json"),"w"), ensure_ascii=False, indent=1)
print("\nsaved results/161_folha1_wordhood.json")
