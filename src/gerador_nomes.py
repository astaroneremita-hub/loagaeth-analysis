# -*- coding: utf-8 -*-
"""
O gerador de nomes do Loagaeth, como codigo (frente 10).
Gramatica derivada empiricamente (a171): NOME := PREFIXO? RAIZ SUFIXO*
- cobre 62/90 nomes reais 100% (null aleatorio: 0/90).
- combinacao LIVRE: nenhuma restricao raiz x afixo (H(suf|raiz) z=-0.3).
  => gerador tabular/artificial, nao morfologia de lingua natural.
- OBRE-gera: o conjunto de regras e necessario (nomes cabem) mas nao suficiente
  (produz muito mais strings que as atestadas); falta a camada de selecao
  (qual tabela / qual posicao) que decide QUAIS combinacoes aparecem.
"""
import re, itertools

PREFIXOS = ["ad","no","a","al","an","ax","i","zi","ne","axno"]   # + vazio
RAIZES   = ["chastor","nocha","nacho","chadax","aclax","geth","gradax","antantox","anzach","phange"]
SUFIXOS  = ["a","al","p","ad","to","ph","tor","pha","an"]          # 0 ou mais

_P=sorted(PREFIXOS,key=len,reverse=True)
_S=sorted(SUFIXOS,key=len,reverse=True)
_R=sorted(RAIZES,key=len,reverse=True)

def parse(nome):
    """Decompoe nome em (prefixo, raiz, [sufixos], sobra). sobra=0 => parse completo."""
    n=re.sub(r"[^a-z]","",nome.lower()); best=None
    for p in [""]+_P:
        if not n.startswith(p): continue
        i=len(p)
        for r in _R:
            if n[i:].startswith(r):
                j=i+len(r); sufs=[]
                while j<len(n):
                    hit=next((s for s in _S if n[j:].startswith(s)),None)
                    if not hit: break
                    sufs.append(hit); j+=len(hit)
                cand=(p,r,sufs,len(n)-j)
                if best is None or (cand[3],len(cand[2]))<(best[3],len(best[2])): best=cand
    return best

def gerar(max_sufixos=1):
    """Gera todos os nomes PREFIXO? RAIZ SUFIXO{0..max_sufixos}."""
    out=set()
    for p in [""]+PREFIXOS:
        for r in RAIZES:
            for k in range(max_sufixos+1):
                for combo in itertools.product(SUFIXOS,repeat=k):
                    out.add(p+r+"".join(combo))
    return out

if __name__=="__main__":
    for ex in ["ADNOCHAPHA","ANTANTOXAL","ZICHASTORA","NOCHASTOR","PHANGE"]:
        p,r,s,sob=parse(ex)
        print(f"{ex:<12} = {('['+p+'] ' if p else '')}{r}{' '+ ' '.join(s) if s else ''}  (sobra {sob})")
    g=gerar(1)
    print(f"\ngerar(max_sufixos=1): {len(g)} nomes possiveis  (reais atestados ~90 => gerador obre-gera)")
