# O que são as "letras que sobram" da folha 1 — e pra que servem
# What the leftover non-name tokens of folha 1 are — and what they do

**CONFIRMADO NOVO (#334).** As ~162 "partículas" curtas da folha 1 (as letras que
não são nome e não têm tradução) **não são uma classe-função gramatical** (artigos,
preposições). São **as peças do gerador de nomes** — prefixos, sufixos e fragmentos
de raiz — aparecendo soltas e espalhadas na página.

_The short "particles" of folha 1 are not a grammatical function-word class. They are
the building blocks of the name generator (prefixes, suffixes, root fragments) standing
alone._

---

## As três camadas da folha 1

| camada | o que é | nº tipos | tokens | % corpus |
|---|---|---|---|---|
| **A — léxico** | palavras com sentido, glosadas nas Chamadas (`ar`=that, `ol`=I, `od`=and…) | 21 | 97 | 3% |
| **B — partículas** | curtas, recorrentes, sem glosa | 162 | 809 | 22% |
| **C — nomes** | nomes/palavras longas do campo onomástico | 2514 | 2708 | 75% |

A pergunta era: **o que é a camada B e pra que serve?** Duas hipóteses:
- **H1 (morfologia):** B = peças do gerador de nomes (afixos/fragmentos).
- **H2 (gramática):** B = classe-função independente, como artigos/preposições.

Os testes (todos contra null, seed 1583) **confirmam H1 e refutam H2**.

---

## Provas (`src/a169`, `src/a170`)

| teste | medida | real | null | z | lê |
|---|---|---|---|---|---|
| **T5 viés posicional** | B prende em início/fim de linha? | 0.02/0.01 | 0.03 | — | **refuta H2** — palavra-função sempre enviesa posição; B não. Idêntico aos nomes |
| **T4 fonotática** | B parece A (gloss) ou C (nomes)? | cos(B,C)=0.806 | cos(B,A)=0.700 | — | B agrupa com **nomes**, não com as palavras-função |
| **T1 afixo-exato** | B é prefixo/sufixo da Forja? | 7/162 | 2.5 | +2.9 | `ad al an ax ne no pa` já são afixos |
| **T2 borda-de-nome** | B é início/fim de algum nome real? | 29/162 (18%) | 15.1 | +4.0 | sim, acima do acaso |
| **T3 prefixo produtivo** | B = inicial + stem atestado? | 59/162 | 40.5 | +3.5 | prefixos `n- l- g- d-` produtivos |
| **T6 ladrilho dos nomes** | os 90 nomes se montam com as peças B+afixos+raízes? | **85%** letras · **39/90** nomes 100% | 36% · 0.4/90 | **+5.5** | **decisivo** |

### O teste decisivo (T6): os nomes se desmontam nas peças

Pegando o vocabulário de peças atestadas (B + prefixos + sufixos + raízes = 175 unidades)
e ladrilhando os 90 nomes das grades da esquerda pra direita (casamento mais longo):

```
adnochapha  = ad + nocha + pha      [100%]   prefixo + raiz + sufixo
antantoxal  = antantox + al         [100%]   raiz + sufixo
nochastor   = nocha + tor           [89%]
zichastora  = zi + chastor          [90%]    prefixo + raiz
achadax     = chadax                [86%]
```

**85% das letras** dos nomes são cobertas por peças atestadas; **39 de 90** nomes
ladrilham 100%. Vocabulário aleatório do mesmo tamanho cobre só **36%** e ladrilha
**0.4** nome. z = **+5.5**.

---

## Resposta honesta

**O que são:** a camada B é a **morfologia onomástica** — os tijolos
(prefixo · raiz · sufixo) com que os 90 nomes das grades 2-48 são montados, deitados
soltos e repetidos na folha 1. Não é frase, não é gramática de sentença (já sabíamos,
#332); é a **lista de peças** do gerador de nomes, lado a lado com o fino léxico real
(camada A, as 21 palavras que batem com as Chamadas, #333).

**Pra que servem:** são o material de construção dos nomes. A folha 1 é a página-oficina:
expõe as peças (B) e o pouco de língua de verdade (A) de onde o resto do livro tira os
nomes (C).

### Limites (honesto)
- z moderados (2.9–4.0) nos testes de afixo; só o ladrilho (T6, z=+5.5) é forte.
- ~51/90 nomes não ladrilham 100% — peças faltam ou o casamento guloso erra; parte do B
  que não é afixo pode ser **nome curto** (ainda onomástico, não gramática).
- Não mexe na camada A: o léxico real continua real (#331, #333). Isto explica só o B.

Dados: `results/169_particle_function.json`, `results/170_name_tiling.json`.
