# É uma língua? As leis linguísticas aplicadas ao Loag
# Is it a language? Linguistic laws applied to the Loag

**#351 — NÃO (comporta-se como campo de nomes / alta entropia, não língua natural).**
Rodamos cinco leis quantitativas de língua no Loag, comparando com as Chamadas e com
latim, hebraico, grego, inglês e aleatório. O Loag **falha em quatro das cinco**.

---

## Resultados (`src/a187`)

| lei | língua natural | folha 1 | Chamadas | lê |
|---|---|---|---|---|
| **Zipf** (inclinação rank-freq) | ≈ −1 | **−0.36** | −0.43 | plana demais — sem a cauda de língua |
| **Heaps** (β do vocabulário) | 0.4–0.6 | **0.97** | 0.87 | vocabulário **nunca satura** = lista de nomes |
| **Menzerath** (corr. compr.×grupo) | negativa | +0.20 | +0.17 | sinal fraco, no sentido errado |

**Entropia condicional (bits/letra):**

| corpus | H0 | H1 | H2 |
|---|---|---|---|
| **LOAG** | 4.01 | **3.42** | 2.64 |
| Chamadas | 4.06 | 3.61 | 2.52 |
| latim | 3.91 | 2.78 | 1.05 |
| hebraico | 3.80 | 2.17 | 0.94 |
| inglês | 3.94 | 2.33 | 0.71 |

O Loag é **menos previsível letra-a-letra** (H1=3.42) que qualquer língua real (2.2–2.8) —
tem **menos redundância**, mais perto do aleatório.

**NCD (distância por compressão, 0=idêntico, 1=sem relação):** o Loag fica
~**equidistante de tudo** (0.81–0.84), inclusive do **aleatório** (0.818). **Não agrupa**
com as línguas (que se agrupam entre si, 0.76–0.77). As Chamadas ficam mais perto do
**aleatório** que de qualquer língua.

---

## Leitura honesta

- **As provas mais robustas** (Zipf e Heaps, calculadas nos dados reais do Loag/Chamadas,
  não em amostras pequenas) são **decisivas**: Zipf plano (−0.36) e Heaps β≈1 dizem que o
  Loag é uma **lista onde quase todo item é único** — comportamento de **campo de nomes**,
  não de texto corrido. Confirma #332 (sem sintaxe), #334/#335 (gerador de nomes).
- **A entropia** mostra o Loag menos estruturado que línguas reais — alta entropia, pouca
  redundância. As próprias **Chamadas** de Dee também são de alta entropia (perto do
  aleatório por NCD), coerente com o veredito de **glossolalia** de Laycock (#339).
- **Limites:** as amostras de comparação (latim/hebraico/grego/inglês) são pequenas e
  codificadas à mão; a entropia de ordem alta (H2+) e a NCD sofrem com tamanho desigual.
  Por isso os pesos estão em **Zipf, Heaps e H1**, que são robustos. (Menzerath teve bug
  no latim; o sinal Loag/Chamadas é fraco e fica de reserva.)

**Veredito:** o Loag **não é uma língua natural** no sentido estatístico — é um
**sistema de nomes de alta entropia**. Isso não o diminui: casa perfeitamente com tudo que
achamos (gerador de nomes, campo fechado, sem sintaxe). "Língua de Deus" aqui significa
**um onomástico construído**, não um idioma com gramática de sentença.

Dados: `src/a187_language_battery.py`.
