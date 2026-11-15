# -*- coding: utf-8 -*-
"""a221 - the remaining clean Dee hypotheses (IDEIAS_DEE.md lote 2).

#8  radial decay: name-density falls off with distance from page centre (Propaedeumata rays)?
#11 alchemical sequence: per-folha dominant element runs Earth->Water/Air->Fire (nigredo->rubedo)?
#17 Call first-word predicts the heaviest name of the folha it opens?
#18 concentric rings: a radial gradient of letter-entropy by ring index?
#20 does a folha's dominant element predict its dominant vowel?
stdlib only. seed 1583.
"""
import os
import sys
import json
import math
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load
from a190_tower_traces import side_grids

DATA = os.path.join(os.path.dirname(HERE), "engine", "data")
DIRS8 = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
NAMES = ['NACHO','NOCHAP','NOCHASTOR','ICHASTOR','ANZACH','ALGETH','GETH','ACLAX','DAXVAR',
 'CHARDAX','VOXAR','GRAPHA','ACHEPH','NTAGNA','PHANGE','NADAB','ANTANTOX','AOXARD']
GD_EL = {"A":"Ar","E":"Ar","T":"Ar","I":"Agua","L":"Agua","M":"Agua","O":"Fogo","P":"Fogo",
         "R":"Fogo","F":"Fogo","G":"Terra","N":"Terra","S":"Terra","C":"Terra"}
VOW = "AEIOU"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    rng = random.Random(1583)
    sides = side_grids()
    grids = list(sides.values())
    nums = load.table_numbers()
    result = {}

    # ---- #18 concentric rings: letter entropy by ring ----
    ring_counts = {}
    for g in grids:
        H = len(g); W = len(g[0])
        for r in range(H):
            for c in range(W):
                ch = g[r][c]
                if ch == "?": continue
                ri = min(r, c, H-1-r, W-1-c)
                ring_counts.setdefault(ri, Counter())[ch] += 1
    def H_(cnt):
        n = sum(cnt.values());
        return -sum((v/n)*math.log2(v/n) for v in cnt.values() if v) if n else 0
    ring_ent = {ri: round(H_(ring_counts[ri]),3) for ri in sorted(ring_counts)}
    result["18_rings"] = {"entropy_by_ring_0to24": ring_ent}
    vals = [ring_ent[ri] for ri in sorted(ring_ent)]
    print(f"[#18 anéis] entropia ring0(borda)={vals[0]} ... ring12={vals[12]} ... ring24(centro)={vals[-1]}", flush=True)

    # ---- #8 radial decay of name density ----
    # name cells per ring / cells per ring
    name_cells = Counter()
    for g in grids:
        H=len(g); W=len(g[0])
        for nm in NAMES:
            L=len(nm)
            for r in range(H):
                for c in range(W):
                    if g[r][c]!=nm[0]: continue
                    for dr,dc in DIRS8:
                        er,ec=r+dr*(L-1),c+dc*(L-1)
                        if 0<=er<H and 0<=ec<W and all(g[r+dr*i][c+dc*i]==nm[i] for i in range(L)):
                            for i in range(L):
                                name_cells[min(r+dr*i,c+dc*i,H-1-(r+dr*i),W-1-(c+dc*i))]+=1
    tot_cells = {ri: sum(ring_counts[ri].values()) for ri in ring_counts}
    dens = {ri: round(name_cells[ri]/tot_cells[ri],4) for ri in sorted(tot_cells)}
    result["8_radial"] = {"name_density_by_ring": dens}
    dv=[dens[ri] for ri in sorted(dens)]
    print(f"[#8 radial] densidade de nome ring0={dv[0]} ring12={dv[12]} ring24={dv[-1]} (decai do centro p/ borda?)", flush=True)

    # ---- #11 alchemical sequence ----
    pil = json.load(open(os.path.join(os.path.dirname(HERE),"viz","pilha_data.json"),encoding="utf-8"))
    dom = {row["f"]: max(row["elem"], key=row["elem"].get) for row in pil if row.get("elem")}
    seq = [dom[f] for f in sorted(dom)]
    order = {"Terra":0,"Agua":1,"Ar":2,"Fogo":3}  # nigredo->...->rubedo
    ranks = [order.get(e, -1) for e in seq if e in order]
    # monotonic rising correlation with folha index
    idx = list(range(len(ranks)))
    n=len(ranks); mi=sum(idx)/n; mr=sum(ranks)/n
    cov=sum((idx[i]-mi)*(ranks[i]-mr) for i in range(n))
    vi=sum((x-mi)**2 for x in idx); vr=sum((x-mr)**2 for x in ranks)
    corr = cov/math.sqrt(vi*vr) if vi and vr else 0
    result["11_alchemy"] = {"dominant_element_seq": seq, "corr_with_folha_index": round(corr,3)}
    print(f"[#11 alquimia] corr(ordem Terra→Fogo, índice da folha) = {corr:+.3f} (sequência {Counter(seq)})", flush=True)

    # ---- #20 element -> dominant vowel ----
    rows=[]
    for row in pil:
        f=row["f"];
        if not row.get("elem"): continue
        de=max(row["elem"],key=row["elem"].get)
        txt=load.table_text(f)
        vc=Counter(ch for ch in txt if ch in VOW)
        dv_=max(VOW,key=lambda v:vc[v]) if sum(vc.values()) else "?"
        rows.append((de,dv_))
    pair=Counter(rows)
    result["20_elem_vowel"] = {"elem_vowel_pairs": {f"{a}|{b}":c for (a,b),c in pair.items()}}
    print(f"[#20 elem→vogal] pares (elemento,vogal dominante): {dict(pair)}", flush=True)

    # ---- #17 Call first word vs folha top name ----
    ch=json.load(open(os.path.join(DATA,"chamadas.json"),encoding="utf-8"))["chamadas"]
    def topname(f):
        t=load.table_text(f); c=[(nm,t.count(nm)) for nm in NAMES]; c=[x for x in c if x[1]>0]
        return max(c,key=lambda x:x[1])[0] if c else None
    hits=0; tot=0; overlaps=[]
    for c in ch:
        tab=c.get("tabua_que_move_segundo_o_tfr")
        if not isinstance(tab,int): continue
        pal=c.get("palavras") or []
        fw=load.letters(pal[0]["enoquiano"]) if pal and pal[0].get("enoquiano") else ""
        tn=topname(tab)
        if not fw or not tn: continue
        tot+=1
        ov=len(set(fw)&set(tn))/len(set(fw)|set(tn))
        overlaps.append(round(ov,2))
    obs=sum(overlaps)/len(overlaps) if overlaps else 0
    # null: random pairing
    allfw=[load.letters(c["palavras"][0]["enoquiano"]) for c in ch if c.get("palavras") and c["palavras"][0].get("enoquiano")]
    alltn=[topname(c.get("tabua_que_move_segundo_o_tfr")) for c in ch if isinstance(c.get("tabua_que_move_segundo_o_tfr"),int)]
    alltn=[t for t in alltn if t]
    sims=[]
    for _ in range(500):
        s=0;k=0
        for fw in allfw:
            tn=rng.choice(alltn)
            s+=len(set(fw)&set(tn))/len(set(fw)|set(tn)); k+=1
        sims.append(s/k)
    m=sum(sims)/len(sims); sd=(sum((x-m)**2 for x in sims)/len(sims))**0.5
    z=(obs-m)/sd if sd else 0
    result["17_call_word"] = {"obs_overlap":round(obs,3),"null":round(m,3),"sd":round(sd,3),"z":round(z,2)}
    print(f"[#17 Chamada→nome] overlap 1ª palavra × top-nome: obs {obs:.3f} vs null {m:.3f}±{sd:.3f} z={z:+.2f}", flush=True)

    rdir=os.path.join(HERE,"..","results"); os.makedirs(rdir,exist_ok=True)
    with open(os.path.join(rdir,"221_dee_batch2.json"),"w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=1)
    print("done", flush=True)


if __name__ == "__main__":
    main()
