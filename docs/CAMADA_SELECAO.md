# A camada de seleção: por que só ~90 dos 1210 nomes possíveis?
# The selection layer: why only ~90 of 1210 possible names?

**#337 — CONFIRMADO.** O gerador (#335) descreve a FORMA de ~1210 nomes possíveis
(`PREFIXO? RAIZ SUFIXO≤1`), mas só ~90 viram nome de verdade. O que seleciona é a
**recorrência na grade**: um nome real aparece em ~40 linhas do livro; uma forma gerada
que não virou nome aparece em ~1 (acaso). **z = +14.7.** A seleção **não** é regra
morfológica nem fonotática — é a geometria das tabelas repetindo as mesmas peças.

_The generator gives the shape; the grid selects by sheer recurrence (~40 lines vs ~1,
z=+14.7). Not a linguistic filter — table geometry._

---

## O teste (`src/a173`, real vs gerado-não-real, permutação 2000, seed 1583)

Candidatos `PREFIXO? RAIZ SUFIXO≤1` = **1210**; reais entre eles = **62**; não-reais = **1148**.
Poder: **90/90** nomes reais são substring de linha no livro (os nomes do Loag são
row-legíveis — ao contrário dos outros sistemas, #336).

| discriminador | real | não-real | z | peso |
|---|---|---|---|---|
| **recorrência** (linhas, ≥5 letras) | **40.1** | **0.97** | **+14.7** | **o seletor** |
| comprimento | 7.73 | 9.53 | −8.4 | secundário |
| run de consoante (cmax) | 2.05 | 2.38 | −4.6 | subproduto |
| run de vogal (vmax) | 1.08 | 1.28 | −3.4 | subproduto |
| violação anti-hiato | 0.00 | 0.04 | −1.6 | fraco |

---

## Leitura honesta

- **O seletor é recorrência, não regra.** Uma forma vira "nome" porque a grade a produz
  de novo e de novo (~40 loci), não porque passa num filtro de gramática ou de som. O
  z=+14.7 da recorrência engole os outros efeitos.
- **Curto/liso é subproduto.** Nomes reais são mais curtos e mais lisos (z −8.4, −4.6,
  −3.4), mas unidade curta recorre mais por definição; mesmo controlando (≥5 letras) a
  recorrência fica 40 vs 1. O filtro primário é a repetição, não a fonotática.
- **Fecha a história do gerador.** #335: a forma é `PREFIXO? RAIZ SUFIXO*`, combinação
  LIVRE (sem seleção na gramática). #337: a seleção mora FORA da gramática — na geometria
  da tabela, que lança as mesmas peças curtas em muitos lugares. Juntos: o Loag é um
  **campo combinatório de nomes** onde a tabela escolhe por recorrência, não uma língua.

### Limites
- 28/90 nomes reais **não** cabem em `PREF?+RAIZ+SUF≤1` (precisam de 2+ sufixos ou peças
  fora do núcleo de 10). O quadro de 1210 cobre 62; o retrato completo pede o inventário
  estendido.
- "Recorrência" aqui é contagem de linhas por substring em ordem de linha; não separa
  recorrência real de sobreposição de janelas. O sinal é grande demais (z=+14.7) pra ser
  só isso, mas a métrica é grosseira.

Próximo natural: **qual geometria** (coluna? antidiagonal? gradiente semente/corpo/
profundo?) concentra a recorrência — aí liga na leitura das grades 2-48.

Dados: `results/173_selection.json`.
