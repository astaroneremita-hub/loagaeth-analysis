# 40 hipóteses profundas — padrão oculto no caos (célula a célula)

Busca de estrutura escondida ALÉM dos nomes e do já explorado (autocorrelação 1D lag 1-120,
viés posicional coluna/linha, MI entre colunas dist 1-10, motivos 2x2, Markov, runs verticais,
dialetos, segmentação — #369-371, #377). Cada uma: método + null. Rodadas em `src/a228`.
Sobrevive só se z>3 contra o null. Expectativa honesta: a maioria falha (alta entropia); caça-se a exceção.

## Família A — lattice modular (letra prefere posição r/c mod m?)
1. Letra × (r mod 2) — tabuleiro par/ímpar por linha.
2. Letra × (c mod 2) — par/ímpar por coluna.
3. Letra × ((r+c) mod 2) — cor de tabuleiro (xadrez).
4. Letra × (r mod 3), 5. (c mod 3), 6. ((r+c) mod 3), 7. ((r−c) mod 3).
8. Letra × (r mod 5), 9. (c mod 5), 10. ((r+c) mod 5).
11. Letra × (r mod 7), 12. (c mod 7), 13. ((r+c) mod 7), 14. ((r−c) mod 7) — o 7 é o número de Dee (7×7).

## Família B — periodicidade por letra (letra a cada N?)
15. Para cada letra, autocorrelação do seu indicador no fluxo (aparece a cada N?).
16. Gap entre ocorrências consecutivas de cada letra — distribuição periódica?
17. A letra mais rara (U/Q/Z) é espaçada regularmente (marcador)?

## Família C — co-ocorrência por vetor (par de letras a distância d)
18. Skip-bigrama no fluxo a distância d=2..12: par de letras sobre-representado?
19. Co-ocorrência 2D por vetor (dr,dc) pequeno: par A→B a offset fixo?
20. Letra X sempre seguida de Y após k células na linha?
21. Letra que precede/segue a vogal tônica tem padrão?

## Família D — geometria oculta
22. Autocorrelação na DIAGONAL ↘ (lag diagonal) vs anti-diagonal ↙.
23. Listras diagonais — periodicidade ao longo das diagonais.
24. Estrutura 7×7: tratar 49×49 como 7×7 blocos de 7×7; viés de letra por posição-no-bloco.
25. Viés por posição-no-bloco 7 (cada letra prefere um canto do bloco 7×7?).
26. Salto de cavalo: letra em (r,c) prediz letra em (r±1,c±2)?
27. Simetria rotacional 90°/180° da grade (célula vs célula girada).
28. Centro (24,24) e a cruz central têm distribuição própria (já: coluna morta; agora a CRUZ inteira).

## Família E — sequência e ordem fina
29. Trigrama mais provável após cada bigrama muda por região? (gramática local deriva)
30. Entropia condicional por COLUNA vs por LINHA (anisotropia de memória, além de #370).
31. A primeira letra de cada linha prediz a última da mesma linha?
32. Soma/paridade de letras (valor) por linha forma sequência?
33. Comprimento de "run" de vogais vs consoantes — distribuição periódica?
34. Posição das vogais na linha (toda n-ésima é vogal?).

## Família F — campo e textura
35. Densidade de uma letra forma gradiente 2D suave (mapa de calor com estrutura)?
36. Correlação coluna×coluna (quais colunas são gêmeas) além de linha.
37. Mutual information por DISTÂNCIA DIAGONAL (não só horizontal #371).
38. "Buracos": células '?' (nulos) têm padrão posicional?
39. Transição entre folhas: a última linha de uma prediz a primeira da próxima (junção fina, por letra)?
40. Compressibilidade por BLOCO (quais regiões comprimem mais — ilhas de ordem no caos).

---
Rodar: `src/a228_deep_battery.py` (as automatizáveis). Cada achado z>3 vira entrada no RESEARCH_LOG.
