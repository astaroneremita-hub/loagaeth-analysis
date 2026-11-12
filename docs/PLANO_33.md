# Plano de 33 partes — explorar o que falta e aonde chega

Estado atual (resumo): confirmados a estratificação por linha, os nomes tecidos, o mapa de territórios, a
gramática gerativa (raiz+afixo), a hierarquia por repetição, as duas camadas (substrato/compostos), a língua
(Zipf/entropia/morfologia semítica), o vocabulário partilhado com as Chamadas, e o catálogo completo de palavras
recorrentes (2–8 letras, ~11k). Falta ligar tudo numa leitura e empurrar a decifração. Cada parte tem um teste e
um nulo; nada vira achado sem bater o nulo.

## Bloco A — Completar o inventário e a leitura
1. **Catálogo total 2–8** (feito, a99): toda palavra recorrente, por comprimento. Próximo: marcar cada uma como
   raiz, derivado, ponte ou livre.
2. **Palavras maximais**: extrair o léxico "real" (substrings recorrentes que não são só pedaço de uma maior) por
   MDL/BPE, para separar palavra de fragmento.
3. **Fronteiras de palavra**: onde uma palavra acaba e outra começa (entropia de fronteira) — segmentar o livro
   em "tokens" de verdade.
4. **Linhas como versos**: cada linha contém um número inteiro de palavras? (fronteiras alinhadas nas pontas).
5. **Sintaxe entre nomes**: numa tabela, há ordem/regra entre palavras (rei primeiro, corte em volta)? a camada
   de frase.

## Bloco B — Geometria e leitura
6. **Diagonais e diamantes** (parcial): ler 25–28 e 29–48 na ordem correta e catalogar (densidade já medida:
   diagonal é a mais rica).
7. **Costura das pirâmides**: os nomes atravessam ou evitam a linha larga do losango?
8. **Omni-direcional por palavra**: cada palavra lida em reta/coluna/diagonal/traçado — quais preferem qual modo?
9. **Acrósticos e centros**: primeira/última letra de cada linha, célula central, vértices — lidas ao longo e
   através das tabelas.
10. **A letra supérflua** (feito): a central é o pivô, sem marca — fechar com teste de borda.

## Bloco C — A língua e a decifração
11. **Reconstrução interna do sentido**: ancorar nas palavras que Dee traduziu (canse/crucanse, pola/pala, os=12)
    e propagar por morfologia (vogal = modulação, afixo = papel).
12. **Morfologia semítica**: mapear raiz consonantal × padrão vocálico — que vogal muda que sentido (como
    pola/pala).
13. **Afixos com função**: o que cada prefixo/sufixo faz (AD-, AL-, I-, -P, -STOR…) — carga elemental + posto +
    (talvez) sentido.
14. **Minimal pairs em massa**: todos os pares que diferem por 1 letra/vogal — o mapa de oposições da língua.
15. **Classes gramaticais**: as palavras se agrupam em "tipos" (nomes, verbos, partículas) por distribuição?
16. **A acentuação**: Dee acentuou as palavras nos últimos 7 dias — a tônica marca posto/classe?

## Bloco D — Pontes com os outros sistemas
17. **Chamadas na Loagaeth** (feito, todos os modos): vocabulário partilhado; aprofundar quais palavras e onde.
18. **Teoria das coordenadas**: digitalizar os números da recepção da 1ª Chamada e testar o elo letra-a-letra.
19. **Padrão de tradução de Dee** (feito): sintaxe inglesa + léxico próprio; aprofundar de onde vem cada glosa.
20. **Torres e Heptarquia**: já medido que os nomes do Loagaeth não aparecem lá; testar o inverso (nomes das
    Torres na Loagaeth) em todos os modos.
21. **Aethyrs e governadores**: os 91 governadores / 30 Aethyrs aparecem em região específica do livro?
22. **Gematria interna**: NOCHA≡NACHO (um só valor); varrer todos os pares anagrama/rotação com mesmo valor.

## Bloco E — Estrutura do livro inteiro
23. **Ordem do livro**: a ordem de Dee é um caminho suave (seriação) ou tem saltos? espelho t↔49−t?
24. **Plano 7×7**: as 49 partes num plano 7×7 — vizinhos se parecem? blocos de 7?
25. **Fluxo elemental** (feito): ordenado em regiões; ligar à hierarquia e aos territórios.
26. **Mapa de dialetos**: perplexidade cruzada segmento×segmento — o livro tem "sotaques" por região?
27. **Números dos servos**: os números (7209 etc.) dos governadores relacionam-se com repetição/força de algum
    nome?

## Bloco F — O visual e o repertório próprio
28. **Repertório navegável** (feito): todas as palavras por comprimento; adicionar filtro por elemento/tabela.
29. **Busca universal na grade** (feito): qualquer palavra, em qualquer modo, em qualquer folha.
30. **Sigilo tradicional vs traçado**: desenhar o sigilo de um nome (ligar letras na ordem) e comparar ao nosso
    king-move.
31. **Mapa-livro**: uma visão única do livro inteiro (49 tabelas) com densidade/elemento/território por folha.
32. **Dicionário vivo**: cada palavra com tudo que sabemos (posições, modos, elemento, perigo, sentido se houver,
    família) — a ficha completa, exportável.

## Onde isto chega (parte 33)
33. **A síntese**: um modelo único do Loagaeth como língua-onomasticon — alfabeto → morfologia (raiz+vogal+afixo)
    → léxico (famílias e territórios) → sintaxe (ordem entre palavras) → semântica parcial (âncoras das Chamadas).
    O que a medida pode entregar é o **esqueleto completo da língua e um dicionário parcial**; o sentido pleno de
    cada nome ou fica nas poucas âncoras traduzidas, ou exige a prática. A meta final é: dado qualquer nome do
    livro, devolver sua ficha completa e, onde houver âncora, seu sentido — e marcar honestamente onde o
    significado continua selado.
