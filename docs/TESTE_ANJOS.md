# Nomes de anjos são geráveis pela gramática do Loag?
# Are angel names generable by the Loag grammar?

**#348 — NÃO (sem confirmação limpa).** Testamos se nomes de anjos — venusianos
(Hanael, Anael, Hagiel, Noguel…), os Filhos da Luz (Filii Lucis), reis da Heptarquia, e
`BAAL`/`IHRLAA` — saem da gramática do Loag. A resposta honesta é **não**: a gramática que
descreve o Loag de verdade gera **zero**; a versão permissiva aceita 8% de **qualquer
coisa** (inclusive ruído aleatório), então seus acertos são falso-positivos.

---

## O teste (`src/a184`, contra null, seed 1583)

| grupo | n | gramática apertada (dos 90) | gramática ampla (do livro) |
|---|---|---|---|
| anjos venusianos | 8 | **0** | 3 (anael, asmodel, noguel) |
| Filhos da Luz (Filii Lucis) | 14 | **0** | 0 |
| reis da Heptarquia | 16 | **0** | 0 |
| controle (outros sistemas) | 15 | **0** | 1 (michael) |
| **null** (strings aleatórias, mesmos tamanhos) | — | **0%** | **8%** |

- **Apertada** = esqueleto·melodia·template dos 90 nomes (67×28×44). Gera **0/53** anjos; o
  null também é 0% → é **restritiva e disciplinada** (não inventa).
- **Ampla** = os 1948 esqueletos × 288 melodias do livro inteiro. Aceita **8% de tudo** —
  e o **null é 8%** (z=−0.1). Logo os acertos (michael, anael…) são **falso-positivo**, não
  descoberta.

### O bump venusiano é confound, não prova
Os venusianos passam um pouco mais na gramática ampla (3/8 vs null 0.9, z=+2.3). **Mas** é
o mesmo **confound A/O**: anjos venusianos são A/O-pesados (an**a**el, n**o**gu**e**l), e o
inventário do Loag é A/O-pesado — porque as letras "de Vênus" (A, O) **são** as vogais mais
comuns. É exatamente o que pôs 81/90 nomes em Vênus (#340, correspondências). Não é um elo
independente; é a mesma frequência de letras se repetindo. `michael` (controle) também
passou.

---

## Leitura honesta

- **Nomes curtos** (baal, el, me) falham porque seus esqueletos/melodias **não estão** no
  inventário do Loag — a rede rica não os "acha" por mágica; o Loag simplesmente não tem
  aquelas estruturas.
- **Seria lindo** achar os anjos venusianos saindo da forja — mas não acham. E isso é
  **bom para a integridade**: o teste tinha poder (null apertado = 0%), então um acerto
  real apareceria; não apareceu.
- **Reconfirma a ilha (#336):** a gramática do Loag não produz o onomástico angélico dos
  outros sistemas. O Loag é fechado.
- A gramática **ampla** do livro não serve para "provar" nada: ela casa com qualquer coisa
  (8% de ruído). Usá-la para dizer "achamos anjo X" seria falso-positivo — o mesmo erro de
  auto-replicação que já evitamos.

**Veredito:** o sistema planetário é **internamente consistente** (Vênus = frequência de
A/O), mas essa consistência é **circular**; não há prova independente de que o Loag gere
nomes de anjos venusianos.

Dados: `src/a184_angel_test.py`.
