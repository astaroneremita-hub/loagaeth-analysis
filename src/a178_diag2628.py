# -*- coding: utf-8 -*-
"""
a178 — Folhas 26-28 (0 nomes por LINHA, #342) lidas na DIAGONAL. Reconstroi as faces
49x49, le diagonais ↘ (r-c) e ↙ (r+c), ida+volta, conta nomes vs linha e EXTRAI quais
nomes aparecem e onde. seed 1583.
"""
import json, re, os, random, collections
random.seed(1583)
ROOT=r"C:\Users\T-GAMER\Documents\GitHub\loagaeth-analysis"
def norm(w):
    w=str(w).lower()
    for a,b in [("áàäâ","a"),("éèê","e"),("íìî","i"),("óòô","o"),("úùû","u"),("ç","c")]:
        for ch in a: w=w.replace(ch,b)
    return re.sub(r"[^a-z]","",w)
fg=json.load(open(os.path.join(ROOT,"viz","forge_grammar.json"),encoding="utf-8"))
NAMES=sorted((norm(n) for n in fg["real_names"]),key=len,reverse=True)
ROOTS=[r.lower() for r in fg["roots"]]
grd=json.load(open(os.path.join(ROOT,"engine","data","loagaeth_grades_simples.json"),encoding="utf-8"))

def face(key):
    if key not in grd: return None
    rows=[norm(r) for r in grd[key]]
    if len(rows)==49 and all(len(r)==49 for r in rows): return rows
    return None

def read_dirs(rows):
    N=len(rows)
    ROW=rows[:]
    COL=["".join(rows[r][c] for r in range(N)) for c in range(N)]
    DR=[]
    for d in range(-N+1,N):
        s="".join(rows[r][r-d] for r in range(N) if 0<=r-d<N)
        if len(s)>=2: DR.append(s)
    DL=[]
    for d in range(2*N-1):
        s="".join(rows[r][d-r] for r in range(N) if 0<=d-r<N)
        if len(s)>=2: DL.append(s)
    return {"ROW":ROW,"COL":COL,"DIAG_desc":DR,"DIAG_asc":DL}

def namehits(strs):
    found=collections.Counter()
    for s in strs:
        for n in NAMES:
            if n in s: found[n]+=s.count(n)
            r=s[::-1]
            if n in r: found[n]+=r.count(n)
    return found

keys=[f"{f}{s}" for f in (26,27,28) for s in "ab"]
print("face | ROW | COL | DIAG↘ | DIAG↗   (nomes distintos achados)")
allfound={d:collections.Counter() for d in ("ROW","COL","DIAG_desc","DIAG_asc")}
for k in keys:
    rows=face(k)
    if not rows: print(f"{k}: (nao-quadrada)"); continue
    dd=read_dirs(rows)
    line=[]
    for d in ("ROW","COL","DIAG_desc","DIAG_asc"):
        fh=namehits(dd[d]); allfound[d]+=fh
        line.append(f"{len(fh)}")
    print(f"{k:>4} | {line[0]:>3} | {line[1]:>3} | {line[2]:>5} | {line[3]:>5}")

print("\nNomes achados por direcao (26-28 juntas):")
for d in ("ROW","COL","DIAG_desc","DIAG_asc"):
    top=allfound[d].most_common(12)
    print(f"  {d:<10} {len(allfound[d])} distintos: {', '.join(f'{n}×{c}' for n,c in top)}")

# a diagonal principal longa (49) de cada face ↘ e ↗
print("\nDiagonal principal (49 letras) de cada face:")
for k in keys:
    rows=face(k)
    if not rows: continue
    N=len(rows)
    main_dr="".join(rows[i][i] for i in range(N))
    main_dl="".join(rows[i][N-1-i] for i in range(N))
    def tag(s):
        hits=[n for n in NAMES if n in s or n in s[::-1]]
        return (", ".join(hits[:6]) or "—")
    print(f"  {k} ↘: {main_dr}")
    print(f"       nomes: {tag(main_dr)}")
    print(f"  {k} ↗: {main_dl}")
    print(f"       nomes: {tag(main_dl)}")

json.dump({d:dict(allfound[d]) for d in allfound},
          open(os.path.join(ROOT,"results","178_diag2628.json"),"w"),ensure_ascii=False,indent=1)
print("\nsaved results/178_diag2628.json")
