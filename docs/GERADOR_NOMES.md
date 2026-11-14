# O gerador de nomes do Loagaeth, como código
# The Loagaeth name generator, as code

**#335.** Os 90 nomes das grades saem de uma gramática pequena e explícita.
Código roda em [`src/gerador_nomes.py`](../src/gerador_nomes.py).

_The 90 grid names come from a small explicit grammar. Runnable code in `src/gerador_nomes.py`._

---

## A regra

```
NOME  :=  PREFIXO?  RAIZ  SUFIXO*
```

| slot | inventário | nº |
|---|---|---|
| **PREFIXO** (0 ou 1) | `ad no a al an ax i zi ne axno` | 10 |
| **RAIZ** (1) | `chastor nocha nacho chadax aclax geth gradax antantox anzach phange` | 10 |
| **SUFIXO** (0+) | `a al p ad to ph tor pha an` | 9 |

Exemplos (parse real):

```
ADNOCHAPHA = [ad] nocha pha
ANTANTOXAL =      antantox al
ZICHASTORA = [zi] chastor a
NOCHASTOR  = [no] chastor
PHANGE     =      phange
```

---

## Provas (`src/a171`, contra null, seed 1583)

| medida | real | null | lê |
|---|---|---|---|
| nomes 100% parseados | **62/90** | **0/90** em 2000 sorteios | gramática real; acaso nunca monta |
| compressão (MDL) | 684 letras → **89** de inventário | — | **7.7×**: as peças descrevem os nomes |
| raízes / prefixos / sufixos usados | 10 / 10 / 9 | — | núcleo pequeno fechado |
| `H(sufixo\|raiz)` | 1.714 bits | 1.743 (shuffle) z=−0.3 | **combinação LIVRE, sem restrição** |

Frequência das raízes: `chastor` 17 · `nocha` 11 · `nacho` 8 · `chadax` 6 · `aclax` 5 ·
`geth` 5 · `gradax` 3 · `antantox` 3 · `anzach` 2 · `phange` 2.

---

## Leitura honesta

- **A gramática é real.** 62 dos 90 nomes caem exatos em `PREFIXO? RAIZ SUFIXO*`;
  null aleatório do mesmo tamanho nunca monta um sequer (0/90 em 2000). Compressão 7.7×.
- **A combinação é LIVRE.** Nenhuma raiz prefere ou recusa um sufixo (`H(suf|raiz)` igual
  ao shuffle). Língua natural tem seleção morfológica; isto não tem — é **gerador
  tabular/construído**, casa com a tese de que o Loag é campo de nomes combinatório, não
  idioma com sintaxe (reforça #332, #334).
- **A gramática OBRE-gera.** Com 1 sufixo já são **1100** nomes possíveis; só ~90 estão
  atestados. Logo a regra é **necessária** (os nomes cabem) mas **não suficiente**: falta
  a camada de seleção — qual tabela, qual posição na grade — que decide QUAIS das 1100
  combinações viram nome de verdade. Esse é o próximo alvo.
- **Limite:** 28/90 não fecham 100% (sobra material) — faltam raízes/afixos fora do núcleo
  de 10, ou são variantes/compostos. O inventário atual é o miolo, não o total.

Dados: `results/171_name_grammar.json`. Peças vêm de `viz/forge_grammar.json`.
