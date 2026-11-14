# Tem astrologia (signo/planeta) dentro do Loag? E o Soyga serve?
# Is there astrology (zodiac/planet) inside the Loag? Does Soyga apply?

**#340 — REFUTADO.** Testamos se as 48 folhas do Loag **ciclam** como zodíaco (12) ou
planetas (7), por três mapas de letra→atributo. **Nenhum ciclo.** A única estrutura é
**suavidade local** (folha vizinha parecida) — o gradiente que já conhecíamos, não uma
roda astrológica. E o Soyga é **outro sistema** (alfabeto latino próprio); sobrepô-lo ao
Loag seria impor uma grade de fora, não decifrar.

---

## O teste (`src/a175`, autocorrelação do perfil por folha vs shuffle, seed 1583)

| mapa | lag 12 (zodíaco) | lag 7 (planeta) | lag 1 (vizinho) |
|---|---|---|---|
| **elemento** do Loag (GD) | z=−1.6 | z=+1.2 | z=+7.5 |
| **planeta** do Loag (GD) | z=−1.7 | z=+1.4 | z=+7.1 |
| **valor do Soyga** (imagem) | z=−1.1 | z=+0.6 | z=+6.1 |

Leitura: ciclo apareceria como PICO no lag 12 ou 7. Não há — ambos no acaso ou negativos.
O que há é lag 1 forte (vizinho): folhas adjacentes se parecem = **drift suave** (o
gradiente), não periodicidade astrológica.

---

## Respostas diretas

- **Já testamos signo/zodíaco/planeta no Loag?** Agora sim: **não ciclam.** (Antes:
  numerologia já refutada; o gradiente elemental é real, mas é um _drift_ monótono, não
  uma roda de 12 ou 7.)
- **As tabelas das imagens são Soyga, né?** Sim — são as correspondências do **Liber
  Soyga / Aldaraia**: alfabeto **latino** (P A T E R C O… "PATER"), com signo, valor,
  elemento, planeta e humor por letra. Sistema diferente, alfabeto diferente.
- **Dá pra montar tabela de convergência Loag × signo/planeta/humor?** Dá pra montar uma
  tabela **descritiva** (elemento/planeta dominante por folha), mas ela **não carrega
  sinal** — testamos, não há ciclo. Seria decorativo, não decifração. Bolar os **humores
  do Soyga** no Loag é erro de categoria: já provamos que o Loag é sistema **autônomo**,
  disjunto dos outros enoquianos (#336), e o Soyga nem compartilha o alfabeto.
- **Estrelas fixas:** sem dado de catálogo estelar e sem gancho no Loag — não aplicável.

## Honesto
- Isto é terreno de **pareidolia alta** (astrologia casa com qualquer coisa se você deixar).
  Por isso o null estrito: ele mata o ciclo. O gradiente elemental continua o único padrão
  "astro-adjacente" real, e ele é **elemental**, não zodiacal.
- O Soyga em si é um sistema de tabelas 36×36 — se você quiser, é um **projeto à parte**
  (decifrar o Soyga), não uma chave do Loag.

Dados: `results/175_astro.json`.
