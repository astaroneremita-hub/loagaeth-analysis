# Decifração estrutural do Liber Loagaeth — documento de pesquisa

**O que é, como foi achado, e como qualquer pessoa reproduz.**
Transcrição-base: John Dee & Edward Kelley, *Liber Loagaeth*, Sloane MS 3189 (British Library),
via esotericarchives.com. Análise: repositório `loagaeth-analysis`. Linguagem: Python stdlib.
Semente de aleatoriedade fixa em todos os testes: **1583**.

> **Tese em uma frase.** O Loagaeth não é um texto com sentido: é um **campo de nomes**
> gerado por um **autômato combinatório pequeno** (prefixo·raiz·sufixo), lido **em linha**,
> com uma **arquitetura** (os nomes picam no miolo do livro e somem no fim) e uma
> **genealogia** (os nomes formam famílias que se casam). Ele é **autônomo** (não se liga
> às Torres / Heptarquia / governadores) e carrega só uma **camada fina de língua real**
> (~24 palavras atestadas). O que **não** existe é uma tradução palavra-a-palavra dos nomes.

---

## 0. Como ler este documento

Cada achado segue o mesmo molde:
- **Pergunta** — o que se queria saber.
- **Método** — como se mediu.
- **Null** — o modelo de acaso contra o qual se comparou (sem isto, nada conta).
- **Resultado** — os números (z = desvios-padrão acima do acaso; z>3 ≈ forte; z>6 ≈ decisivo).
- **Interpretação** — o que significa, com os limites.
- **Reproduzir** — o script que roda e o arquivo de resultado.

Regra de honestidade do projeto: **nenhum padrão conta até bater um null**; pareidolia
(ver figura onde não há) é o inimigo. Achados refutados são marcados REFUTADO e ficam no
registro. Tudo está em `docs/RESEARCH_LOG.md` (entradas numeradas #NNN).

---

## 1. Material e dados

| arquivo | o que é |
|---|---|
| `engine/data/loagaeth_grades_simples.json` | as 96 faces (48 folhas × 2 lados) em minúsculas; `?` = célula nula. Folha 1 segmentada em palavras pelo próprio Dee; grades 2-48 em letra corrida 49×49 (e losangos no fim) |
| `engine/data/chamadas.json` | as 19 Chamadas (Claves Angelicae) com a tradução inglesa de Dee (Sloane 3191) |
| `engine/data/governadores.json` | 91 governadores, 30 Aethyrs, 12 reis, as 4 Torres |
| `engine/data/heptarquia.json` | Tabula Collecta, 7 tabelas, reis e príncipes |
| `viz/forge_grammar.json` | inventário derivado: 90 nomes reais, 10 raízes, prefixos, sufixos, esqueletos, melodias, mapa letra→elemento (Golden Dawn) |
| `src/a161`…`a181` | os scripts de análise desta fase |
| `results/1NN_*.json` | os números brutos de cada teste |

**Os 90 "nomes reais"** foram derivados em fase anterior lendo as grades (linha/segmento);
são o conjunto de referência. Onde um achado depende deles, a circularidade é apontada.

---

## 2. Os achados

### Parte I — A natureza do livro

#### Achado 1 — É um campo de nomes, não prosa (#332)
- **Pergunta:** a folha 1 encadeia palavras em frase?
- **Método:** entropia condicional H(próxima|atual) do corpus 1a+1b (99 linhas).
- **Null:** embaralhar a ordem das palavras (word-order shuffle).
- **Resultado:** H real = 2.84 vs null 2.86, **z = −1.3**. Bigramas recorrentes 12 vs 2
  (z=+6.7), mas sem queda de entropia: a ordem **não carrega informação**.
- **Interpretação:** há léxico (palavras que se repetem), mas **não há sintaxe de sentença**.
  O livro lista; não sentencia.
- **Reproduzir:** `python src/a162_folha1_syntax.py` → `results/162_folha1_syntax.json`.

#### Achado 2 — As palavras da folha 1 são léxico real (#331)
- **Pergunta:** as palavras que sobram (fora os nomes) são palavras de verdade ou lixo?
- **Método:** recorrência acima do acaso, boa-formação fonotática (anti-hiato), famílias
  por edição-1.
- **Null:** shuffle-resegment (reembaralhar letras e re-segmentar).
- **Resultado:** 306 tipos recorrentes vs null 133 (**z=+22.9**); boa-formação 97% vs 69%
  (z=+42.0); famílias edição-1 51% vs 20% (z=+44.1).
- **Interpretação:** a folha 1 é um **léxico real**, não ruído.
- **Reproduzir:** `python src/a161_folha1_wordhood.py`.

#### Achado 3 — As "partículas" são peças do gerador, não gramática (#334)
- **Pergunta:** as ~162 palavras curtas da folha 1 (sem tradução) são uma classe-função
  (artigos/preposições) ou peças dos nomes?
- **Método:** viés posicional (início/fim de linha), fonotática (bigrama) comparando as
  partículas B com as palavras glosadas A e com os nomes C, e **ladrilho**: tentar cobrir
  os 90 nomes com o inventário de peças atestadas (partículas + afixos + raízes).
- **Null:** strings aleatórias do mesmo tamanho/letras; para o ladrilho, vocabulário
  aleatório do mesmo porte.
- **Resultado:** viés posicional **nulo** (B = 0.02/0.01, igual aos nomes — refuta
  classe-função); B agrupa fonotaticamente com os nomes (cos 0.806) e não com as glosadas
  (0.700); os 90 nomes **ladrilham 85%** das letras com as peças, 39/90 a 100%, vs null
  36% / 0.4 nome (**z=+5.5**).
- **Interpretação:** as partículas são a **morfologia onomástica** — prefixos, sufixos e
  fragmentos de raiz soltos. A folha 1 é a **página-oficina**: lista as peças.
- **Reproduzir:** `python src/a169_particle_function.py` e `python src/a170_name_tiling.py`.

### Parte II — O gerador de nomes

#### Achado 4 — NOME := PREFIXO? RAIZ SUFIXO*, combinação livre (#335)
- **Pergunta:** há uma gramática que gere os nomes?
- **Método:** parsear os 90 nomes em slots prefixo·raiz·sufixo; medir compressão (MDL) e a
  restrição de combinação (entropia condicional sufixo dado raiz).
- **Null:** nomes aleatórios do mesmo tamanho/letras; shuffle dos rótulos de raiz.
- **Resultado:** **62/90** parseiam 100%; null **0/90** em 2000 sorteios. Inventário: 10
  prefixos, 10 raízes, 9 sufixos; compressão 684→89 letras (**7.7×**). H(sufixo|raiz) real
  1.714 vs shuffle 1.743, **z=−0.3** → **combinação livre** (nenhuma raiz prefere um sufixo).
- **Interpretação:** gerador **tabular/construído**, não morfologia de língua natural
  (língua natural tem seleção; esta não tem). **Obre-gera**: só com 1 sufixo são 1210
  strings possíveis, ~90 atestadas → a regra é necessária, não suficiente.
- **Reproduzir:** `python src/a171_name_grammar.py`; o gerador roda em
  `python src/gerador_nomes.py` (funções `parse` e `gerar`).

#### Achado 5 — A seleção é por recorrência na grade (#337)
- **Pergunta:** por que só ~90 dos 1210 possíveis viram nome?
- **Método:** separar os reais dos gerados-não-reais e procurar o discriminador
  (recorrência no livro, comprimento, fonotática).
- **Null:** permutação de rótulos (2000×).
- **Resultado:** recorrência real 40.1 linhas vs não-real 0.97 (**z=+14.7**) — domina.
  Comprimento (z=−8.4) e lisura (cmax z=−4.6) são secundários/subproduto.
- **Interpretação:** o filtro mora **fora da gramática** (que é livre, Achado 4): é a
  **geometria da tabela** repetindo as peças em muitos lugares. O que vira nome é o que a
  grade produz de novo e de novo.
- **Reproduzir:** `python src/a173_selection.py`.

### Parte III — Geometria e mapa

#### Achado 6 — Lê-se em linha; coluna é morta; borda e diagonal↘ são canais (#341)
- **Pergunta:** em que direção de leitura os nomes recorrem?
- **Método:** ler cada face quadrada 49×49 em linha / coluna / diagonal↘ / diagonal↗ /
  borda (ida+volta), contar recorrência dos 90 nomes por direção.
- **Null:** nomes aleatórios do mesmo tamanho/letras, por direção.
- **Resultado:** LINHA z=+103 (parcialmente circular — os nomes foram derivados por
  linha); **BORDA z=+42** e **DIAGONAL↘ z=+12** (não-circulares, reais); **COLUNA z=−1.4,
  total 1** (morta); diagonal↗ marginal.
- **Interpretação:** o Loag se lê **em linha**, com os nomes grudando na **borda** e num
  fio **diagonal descendente**; **nunca** em coluna.
- **Reproduzir:** `python src/a176_geometry.py`.

#### Achado 7 — O mapa do livro inteiro (#342)
- **Pergunta:** o livro é uniforme ou tem forma?
- **Método:** por folha (leitura em linha), densidade dos 90 nomes, cobertura pelas peças,
  léxico das Chamadas, perfil elemental (contagem de letras), raiz dominante.
- **Null:** nomes aleatórios para a densidade.
- **Resultado:** densidade real 22.5 nomes/folha vs null 0.1 (**z=+126**). Distribuição:
  sobe ~12 (folhas 1-4) → pico 11-25 (folha 14: 47 nomes, 207 ocorrências) → desaba 40-48
  (2-14). Gradiente elemental **limpo** (independe dos nomes): Terra(corpo) pica ~0.47 no
  meio e cai a ~0.27 no fim; Água(profundo) sobe 0.23→0.35. Raízes: começo nocha/nacho,
  miolo geth/antantox, fim geth domina (13/16).
- **Interpretação:** arquitetura **abertura → corpo → costura → profundo**. A folha 1 é
  única (léxico das Chamadas = 33 vs ~5-10 no resto): a página-oficina.
- **Reproduzir:** `python src/a177_sweep.py` → `results/177_sweep.json`.

#### Achado 8 — As folhas 26-28 são a costura diagonal (#343)
- **Pergunta:** por que 26-28 dão 0 nomes por linha (Achado 7)?
- **Método:** ler 26a-28b também na diagonal ↘ e ↗; contar nomes por direção; ler as
  diagonais principais.
- **Controle:** a própria linha (=1 nome) e coluna (=0) nas mesmas faces.
- **Resultado:** ROW 1, COL 0, **DIAG↘ 55 nomes distintos** (geth×72, nocha×41, chastor×15…),
  DIAG↗ 18. A diagonal principal de 26a soletra `…chad·NOCHASTORAL·ged·no·dant`; 28a/b dão
  ALGETH/ANTANTOX/RONZIN.
- **Interpretação:** nessas faces o **eixo de leitura gira 45°**. É a **costura** entre a
  metade densa (2-25) e o profundo (29-48). Mesmo campo de nomes girado, não conteúdo novo.
- **Reproduzir:** `python src/a178_diag2628.py`.

### Parte IV — A genealogia

#### Achado 9 — Os nomes são dinastias que se casam (#344)
- **Pergunta:** há famílias além de CHASTOR?
- **Método:** agrupar os 90 nomes por raiz; grafo de edição-1 (nomes a 1 letra de
  distância); achar pontes (nomes com 2 raízes).
- **Null:** o mesmo grafo sobre nomes aleatórios do mesmo tamanho/letras.
- **Resultado:** grafo edição-1 com **55 arestas**, null 0.1 (**z=+229.6** — o acaso nunca
  liga dois). Dez casas: NOCHA 19, CHASTOR 18, NACHO 9, CHADAX/GETH 6, ACLAX 5, etc.; 24
  nomes sem raiz. Sete pontes, quase todas **NOCHA+CHASTOR → NOCHASTOR**.
- **Interpretação:** o campo de nomes é uma **genealogia** — tudo deriva por acreção de
  afixo (`adnocha→adnochap→adnochaph→adnochapha`), e as duas casas grandes se casam.
- **Reproduzir:** `python src/a179_dynasties.py`; visual em `viz/dinastias.html` e
  `viz/genealogia.html`.

### Parte V — As fronteiras (o que o Loag NÃO é)

#### Achado 10 — O Loag é uma ilha (#336)
- **Pergunta:** o Loag se liga às Torres / Heptarquia / 91 governadores / Chamadas?
- **Método:** cada nome desses sistemas como substring no livro inteiro (96 lados); e as 10
  raízes do gerador dentro dos nomes desses sistemas (teste independente de ordem).
- **Null:** strings aleatórias pareadas por tamanho/letras.
- **Resultado:** governadores 0/91 (z=−0.4); Torres, Heptarquia, Chamadas-longas todos no
  acaso; **raízes do gerador em 0 nomes de qualquer sistema**.
- **Interpretação:** sem ponte onomástica. O gerador do Loag é **disjunto** dos outros
  sistemas enoquianos. (O elo folha1↔Chamadas do #333 era **léxico** — palavras curtas —,
  não nome.)
- **Reproduzir:** `python src/a172_bridges.py`.

#### Achado 11 — O léxico real é fino; Laycock não o expande (#338, #339)
- **Pergunta:** o *Complete Enochian Dictionary* (Laycock) dá mais palavras traduzíveis?
- **Método:** overlap da folha 1 com o léxico do dicionário, por tamanho, contra null; e
  controle de contaminação.
- **Resultado bruto:** folha1 len≥4 bate 114/2342 no dicionário (z=+42.8). **Mas** a
  Introdução do Laycock **transcreve a própria folha 1** (fólios I.13, 1.24, L25, II.24) —
  auto-citação. Removido o bloco de citação + o inglês das glosas, sobra ~**24** palavras
  confiáveis: 21 das Chamadas + 3 que **Dee** glosou (apachana, tohcoth, donasdogamatastos).
  Controle: raízes 0/10 e nomes 0/90 no dicionário → o campo de nomes **não é enoquiano**.
- **Interpretação:** a camada de língua real é fina; o "114" era artefato. Bônus: Laycock
  (linguista) julga o Loag inicial **glossolalia**, batendo com o Achado 1.
- **Reproduzir:** `python src/a174_laycock_lexicon.py "<caminho do PDF>"`. Glossário honesto
  em `docs/GLOSSARIO.md`.

#### Achado 12 — Não há astrologia (zodíaco/planeta) no Loag (#340)
- **Pergunta:** as 48 folhas ciclam como zodíaco (12) ou planetas (7)?
- **Método:** autocorrelação do perfil por folha (elemento e planeta das letras, pelo mapa
  Golden Dawn; e pelo valor do Soyga) nos lags 12, 7, 4, 1.
- **Null:** shuffle da ordem das folhas.
- **Resultado:** lag 12 z=−1.6/−1.7; lag 7 z=+1.2/+1.4 (acaso); só lag 1 forte (z=+7.5) =
  suavidade local (o gradiente). O valor do Soyga dá o mesmo padrão.
- **Interpretação:** **sem roda** zodiacal nem planetária. O único padrão astro-adjacente é
  o gradiente **elemental**, que é deriva, não ciclo. O Soyga é outro sistema (alfabeto
  latino), não serve de chave.
- **Reproduzir:** `python src/a175_astro.py`.

---

## 3. O que NÃO achamos (limites honestos)

- **A glosa-palavra de cada nome** ("NOCHA = X"). Não há Pedra de Roseta; Dee nunca
  traduziu as tabelas. A análise descreve a estrutura; não decifra um dicionário dos nomes.
- **Gramática semítica especial / poder preditivo da "Forja"** — REFUTADOS por controles
  fortes anteriores (é fonotática de ordem 2-3; um Markov-3 reproduz). A decomposição é
  descrição válida; a geração é construção fiel ao estilo, não língua decifrada. Ver
  `docs/RELATORIO_AUDITORIA.md`.
- **Circularidade residual:** a densidade de nomes (Achado 7) e a leitura em linha (Achado
  6) herdam que os nomes foram derivados por linha. Os achados **independentes** disso — o
  gradiente elemental, a coluna morta, a borda, a diagonal 26-28, a genealogia, as pontes,
  a astrologia — são os mais sólidos.
- **Losangos (faces de linha variável)** ficaram fora dos testes de geometria quadrada.

---

## 4. Guia passo-a-passo (reproduzir do zero)

Pré-requisito: Python 3 (stdlib). No Windows, prefixe os comandos com
`set PYTHONIOENCODING=utf-8` (ou `PYTHONIOENCODING=utf-8` no bash) por causa dos acentos.

1. **Obter a transcrição.** Já incluída em `engine/data/loagaeth_grades_simples.json`
   (fonte: esotericarchives.com/dee/sl3189.htm). As Chamadas em `chamadas.json`.
2. **Confirmar que não é frase (Achado 1):**
   ```bash
   python src/a162_folha1_syntax.py
   ```
   Esperado: H(próxima|atual) z≈−1.3 (sem sintaxe).
3. **Confirmar o léxico real (Achado 2):** `python src/a161_folha1_wordhood.py` → z até +44.
4. **Mostrar que as partículas são peças (Achado 3):**
   ```bash
   python src/a169_particle_function.py
   python src/a170_name_tiling.py
   ```
   Esperado: ladrilho 85% / 39-de-90, z≈+5.5.
5. **Extrair o gerador (Achado 4):** `python src/a171_name_grammar.py` → 62/90, null 0/90.
   Rodar o gerador: `python src/gerador_nomes.py`.
6. **A camada de seleção (Achado 5):** `python src/a173_selection.py` → recorrência z≈+14.7.
7. **A geometria (Achado 6):** `python src/a176_geometry.py` → linha domina, coluna morta,
   borda z≈+42, diagonal↘ z≈+12.
8. **O mapa do livro (Achado 7):** `python src/a177_sweep.py` → densidade z≈+126, gradiente.
9. **A costura diagonal (Achado 8):** `python src/a178_diag2628.py` → 55 nomes na diagonal.
10. **As dinastias (Achado 9):** `python src/a179_dynasties.py` → z≈+229.6, NOCHASTOR.
11. **As fronteiras:** `python src/a172_bridges.py` (ilha), `python src/a175_astro.py`
    (sem zodíaco), `python src/a174_laycock_lexicon.py "<PDF>"` (léxico honesto).
12. **Ver tudo visual:** `cd viz && python -m http.server 8860`, abrir
    `http://localhost:8860/` e navegar: Síntese, Atlas dos Nomes, Mapa do livro, Dinastias,
    Genealogia viva.

Cada script grava um `results/1NN_*.json` com os números exatos para conferência.

---

## 5. Índice

**Scripts** (`src/`): a161 wordhood · a162 sintaxe · a163 folha1×Chamadas · a164 densidade
de glosa · a165 não-nomes · a166-a168 anotações da folha 1 · a169 função das partículas ·
a170 ladrilho · a171 gramática · a172 pontes · a173 seleção · a174 Laycock · a175 astro ·
a176 geometria · a177 varredura · a178 diagonal 26-28 · a179 dinastias · a180 viz dinastias
· a181 dados do atlas · `gerador_nomes.py`.

**Documentos** (`docs/`): PARTICULAS_FUNCAO · GERADOR_NOMES · CAMADA_SELECAO · PONTES ·
LAYCOCK_LEXICO · GLOSSARIO · ASTRO · GEOMETRIA · MAPA_LIVRO · DIAGONAL_2628 · DINASTIAS ·
RELATORIO_AUDITORIA · RESEARCH_LOG (registro cronológico #NNN).

**Visual** (`viz/`, servir em :8860): index (painel) · sintese · atlas_nomes · genealogia ·
mapa_livro · dinastias, e as páginas da fase anterior.

---

*Honestidade acima de resultado: cada número aqui tem um null que o sustenta, e cada limite
está dito. O que o Loag é — campo de nomes gerado e arquitetado — a análise mostra. O que
ele guarda além disso, se guarda, não está nesta página.*
