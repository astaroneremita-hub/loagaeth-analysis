# Descobertas — Loagaeth (resumo consolidado)

Tudo medido contra modelo nulo (embaralhamento, surrogate Markov-3, anagrama). Marcado por força: **FORTE**
(vários controles, convergente), **MODERADO** (real, um controle), **LEAD** (pista), **REFUTADO** (caiu).

## 1. O que o Loagaeth É
- **FORTE — É uma língua**, não ruído nem cifra. Zipf inclinação −1,14 r² 0,98; entropia cai 4,01→2,52 bits/char
  (abaixo do aleatório 3,41); morfologia tipo semítica (raiz consonantal + padrão vocálico), 13 minimal pairs como
  o *pola/pala* de Dee. (a92)
- **FORTE — Cada linha é um inventário balanceado do alfabeto.** Toda letra espalhada por igual nas 49 linhas
  (consoantes 0,71× acaso, z −4,5, 36/42 folhas); nenhum nulo reproduz. (a75)
- O que o livro diz de si (diários): "every letter here bringeth furth the Names of God: but they are but one
  Name"; "49 voices, whereunto the so many powers shall be obedient". Casa com o medido.

## 2. O sistema de nomes
- **FORTE — Os nomes estão tecidos na grade.** A ordem exata de cada nome traça como caminho king-move muito
  acima das próprias letras embaralhadas (232/460 pares "tecidos"; CHASTOR 30/37 folhas). (a77)
- **FORTE — Gramática gerativa: raiz + afixo.** AD-NOCHA, NOCHA-P, I-CHASTOR, AL-GETH. Poder (repetição) cai com a
  profundidade de derivação. (a81)
- **FORTE — A gramática é preditiva.** Geradas combinações raiz×afixo, 32 nomes novos apareceram no livro acima do
  acaso. Espaço finito (~1320 combos depth-1). (a82)
- **FORTE — Super-nomes: cadeias de 2 raízes** até 14 letras (CHASTORACHANZA 3×; GETHALCHADAX 3×). Fusões de casas
  (GETH+NOCHA, NOCHA+ACLAX). ~5,5× acima do surrogate. (a99/a100)
- **MODERADO — Duas camadas:** substrato (raízes curtas, onipresentes) + camada deliberada (compostos longos,
  cravados acima do acaso). (a84)
- **LEAD — Sintaxe entre nomes:** GETHACLAX ordem fixa (17× vs 0 na ordem inversa, 26× acaso); GETH é raiz líder.
  Primeiro sinal de ordem de palavras. (a101)
- **LEAD — Palavras maximais:** 197 unidades livres por entropia de fronteira (OTHA, ANGE, ACHA…) — léxico/morfema
  candidato. (a102)

## 3. Mapa do livro
- **FORTE — Territórios.** CHADAX abre, casa NOCHA na frente, CHASTOR a espinha, casa GETH no fundo. Sai do tecido
  king-move E da leitura reta — dois métodos, o mesmo mapa. (a78)
- **FORTE — Hierarquia por repetição.** NOCHA (492×, rei) > ADNOCHA > NACHO > CHASTOR > ANZACH; singletons = anjos
  menores. (a80)
- **CONFIRMADO — Fluxo elemental ordenado** (17 transições vs 25 do acaso): Terra/Ar em regiões. (a91)
- **MODERADO — Segmento diagonal** (25-28) é a parte MAIS densa em nomes (44/1000 vs 29 na reta): valida a leitura
  diagonal; mesma língua. (a96)
- 7×7: vizinhos no plano mais parecidos (0,59 vs 0,37), mas vem da ordem suave do livro. (a103)

## 4. Atributos (pelo alfabeto enoquiano)
- Cada nome tem elemento (triplicidade do signo), planeta regente, forma, e um **perigo** (Fogo+Marte+Saturno+nodos).
  Elemento robusto em 55/89 nomes (3 fontes concordam). (a85/a90)

## 5. Pontes com as Chamadas
- **MODERADO — Loagaeth e Chamadas partilham vocabulário.** Lendo de todos os modos (reta/coluna/diagonal/traçado,
  reverso, sem acento), 489 palavras das Chamadas aparecem na grade; Call 1 = 68/86. Mesma língua. (a94/a98)
- **MODERADO — Padrão de tradução de Dee:** 96% 1:1 (ordem do inglês) + léxico próprio (0 relação morfológica com o
  inglês). Sintaxe inglesa, vocabulário alienígena. (a95)
- Sentido na grade: 39→ muitas palavras das Chamadas com tradução posta na posição; nossos nomes-raiz (NOCHA) têm
  0 âncora — sentido selado. (a97)

## 6. Refutados (reportados tão alto quanto os achados)
- **REFUTADO — Leitura omni-direcional** (o livro lê uma direção só). (a71)
- **REFUTADO — Famílias de rotação grudadas de propósito** (campo denso, acaso em 761 famílias). (a73)
- **REFUTADO — Chamada = caminho contíguo numa tabela** (não traça acima do acaso). (a93)
- **REFUTADO — Nomes do Loagaeth em outras vertentes** (0 matches em Shem/Goetia/planetários/governadores, mesmo
  afrouxando). Sui generis. (a88)
- **REFUTADO — Afixo prediz território; ponte vive na fronteira; servos ligados à força.** (a79/a83/a103)
- Refutados antigos: códigos longos, cópia, numerologia.

## 7. Onde isto chega
O Loagaeth é um **onomasticon gerativo** — um livro feito para gerar nomes de forças, com alfabeto fixo, morfologia
semítica (raiz+vogal+afixo), léxico em famílias e territórios, cadeias de raízes (super-nomes), um sinal de sintaxe
(ordem GETH→ACLAX), e vocabulário partilhado com as Chamadas. A medida entrega o **esqueleto da língua e um
dicionário parcial**; o sentido pleno de cada nome ou está nas poucas âncoras traduzidas das Chamadas, ou pertence à
prática. O que segue selado está marcado como selado.

Ferramentas no site (`viz/`, servir por HTTP): index, atlas, name_grammar, forge, tables (4 modos + busca),
language, call_map, call_translation, square_reading, call_grid_translation, repertoire, path_view, name_finder,
names_catalog, loagaeth_3d. Módulos a01–a103 em `src/` (`python src/run_all.py`). Figuras em `figures/`. Plano em
`docs/PLANO_33.md`. Log completo em `docs/RESEARCH_LOG.md`.
