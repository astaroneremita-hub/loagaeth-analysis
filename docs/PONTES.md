# O Loag faz ponte com os outros sistemas enoquianos?
# Does the Loag bridge into the other enochian systems?

**#336 — REFUTADO (honesto).** Testamos se os nomes das Torres, da Heptarquia, dos
91 governadores, dos Aethyrs e as palavras das Chamadas aparecem dentro do Loagaeth
inteiro (48 folhas, 196 288 letras). **Não aparecem acima do acaso, e as raízes do
gerador de nomes do Loag não estão em nenhum desses sistemas.** O Loag é um universo de
nomes **autônomo e fechado**.

_No system bridges into the Loag above chance; the Loag's generator roots appear in none
of them. The Loag is a self-contained name universe._

---

## O teste (`src/a172`, substring no livro inteiro vs null pareado, seed 1583)

| sistema | nomes testados | batem no Loag | null | z | lê |
|---|---|---|---|---|---|
| **GOV_91** (governadores) | 91 | **0** | 0.2 | −0.4 | nenhum governador no Loag |
| **AETHYR** | 1 (≥4 letras) | 0 | 0.5 | −1.0 | — (nomes curtos, sem poder) |
| **TORRE_linea** (nomes santos) | 8 | 4 | 2.4 | +1.3 | no acaso |
| **HEPT** (reis/príncipes/derivados) | 140 | 8 | 4.9 | +1.9 | marginal, não decisivo |
| **CALL** (palavras ≥4) | 610 | 81 | 78.5 | **+0.3** | **no acaso** |

**Raízes do gerador** (`chastor nocha nacho chadax aclax geth gradax antantox anzach phange`)
dentro dos nomes de qualquer sistema: **ZERO**. Teste independente de ordem — e é a prova
mais forte: os dois conjuntos de nomes não compartilham morfologia.

---

## Leitura honesta

- **Sem ponte onomástica.** Governadores (0/91), Torres, Heptarquia e Chamadas-longas
  todos no nível do acaso. As 10 raízes do Loag não tocam nenhum nome dos outros sistemas.
  O gerador do Loag (#335) é **disjunto** da Grande Tábua / Heptarquia / governadores.
- **A exceção já conhecida é LÉXICO, não nome.** O elo Loag↔Chamadas que achamos antes
  (#333, z=+7.5) vinha das **palavras curtas** com sentido (a camada A: `ar`, `ol`, `od`…),
  não dos nomes. Aqui, testando só substrings ≥4 letras no livro todo, o sinal some
  (z=+0.3). Confirma: o Loag divide **língua fina** com as Chamadas, **não o campo de nomes**.
- **O Loag é uma ilha.** Responde direto à pergunta "algum sistema mora no Loag?": **não**.
  Ele tem o próprio gerador e o próprio inventário de nomes.

### Limites
- Substring em **ordem de linha** só. Nomes nas grades podem ser lidos por coluna/diagonal;
  este teste não pega esses. **Mas** o teste de raízes (raiz dentro do NOME do outro
  sistema) independe de ordem e deu zero — então, mesmo com leitura por coluna, os dois
  geradores não casam.
- Nomes longos têm pouco poder no substring (null ≈ 0). Os sistemas de nome curto/médio
  (TORRE, HEPT, CALL) é que carregam o teste — e todos ficaram no acaso.

Dados: `results/172_bridges.json`.
