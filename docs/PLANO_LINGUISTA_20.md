# Plano de 20 passos — decifrar a língua dos nomes do Loagaeth (método de linguista de campo)

Premissa estabelecida (a107-a121): o Loagaeth NÃO é prosa nem Chamada cifrada (5 nulls). É um **onomasticon** — um
léxico de NOMES distribuído pelas 36 folhas 49×49, gerado por morfologia (raiz+afixo), com matriz NOCHA. Este plano
decifra a GRAMÁTICA desse léxico como um linguista decifra uma língua desconhecida: grafêmica → fonologia →
morfologia → léxico → semântica → sintaxe → gramática gerativa validada.

Regras: todo passo tem null model; marca REAL/REFUTADO/DESCRITIVO; glosas em inglês; nada commitado; cada passo vira
módulo a### + registro no RESEARCH_LOG; tudo CONFIRMADO vai pro site (`viz/`).

## Fase I — Corpus e grafêmica
1. **Corpus** — 36 quadrados 49×49 normalizados (25b-28b decodificados, losangos reconstruídos). ✅ base_book (a22)
2. **Inventário de grafemas** — os 21 símbolos, frequência e distribuição por folha. Null: uniforme. [a122]
3. **Fonotática** — pares de letra legais/ilegais; a regra "não dobra letra"; onsets e codas possíveis. Null: shuffle. [a123]

## Fase II — Fonologia / silabário
4. **Silabário** — inventário de sílabas (CHA, STOR, NZA, PHA...). ✅ a112
5. **Gramática silábica** — como as sílabas se encadeiam (transições sílaba→sílaba), vogais vs consoantes estruturais. [a124]
6. **Núcleo vocálico** — quais letras funcionam como vogal (A, E, O, I como centros de sílaba). Null. [a124]

## Fase III — Morfologia
7. **Inventário de raízes** — NOCHA, CHASTOR, ACLAX, GETH, NACHO, ANZACH, CHADAX, ANTANTOX, GRADAX, PHANGE. ✅ a86
8. **Inventário de afixos** — prefixos (AD-, AN-, A-, NO-, ZI-, AX-), sufixos (-AX, -OR, -A, -AL, -TO). ✅ parcial a86
9. **Ordem dos afixos** — template fixo prefixo·raiz·sufixo? qual prefixo precede qual? Null de ordem. [a125] ⭐
10. **Hierarquia de derivação** — ubiquidade cai com profundidade, cada camada atestada. ✅ a121 (matriz NOCHA)
11. **Composição (super-nomes)** — raiz+raiz (NOCHASTOR=NOCHA+CHASTOR); quais raízes se compõem, em que ordem. [a126]
12. **Produtividade** — nomes possíveis pela gramática vs atestados (espaço gerativo). [a127]

## Fase IV — Léxico e distribuição
13. **Léxico-núcleo** — nomes por ubiquidade entre folhas (NOCHA 35/36...). ✅ a118
14. **Famílias distribucionais** — co-ocorrência (casa CHASTOR-ACLAX-NOCHA). ✅ a120
15. **Lei de Zipf** — a distribuição de frequência dos nomes segue lei de potência linguística? Null: Markov. [a128] ⭐

## Fase V — Semântica (o limite duro)
16. **Âncoras de sentido** — quais nomes/raízes tocam glosa de Chamada/dicionário (os poucos traduzíveis). [a129]
17. **Perfil elemental por família** — assinatura Fogo/Terra/Ar/Água de cada casa (lente cabalística). ✅ a114 estende
18. **Contexto recorrente** — um nome aparece perto das mesmas palavras/raízes em folhas diferentes? (colocação). [a130]

## Fase VI — Sintaxe e validação
19. **Sintaxe supra-nome** — há ordem entre nomes numa linha/folha? (majoritariamente refutado — formalizar limite). [a131]
20. **Gramática gerativa G + validação MDL** — escrever as regras (raiz × prefixo × sufixo × composição) e testar: G
    regenera o léxico atestado? quantas regras descrevem a casa inteira? É a resposta final a "transformar em código". [a132] ⭐

## Saída no site
- Página nova `viz/name_language.html` — "A Língua dos Nomes": inventário de raízes/afixos, a árvore da matriz NOCHA
  com ubiquidade, o léxico-núcleo, a casa CHASTOR-ACLAX-NOCHA, e a gramática G quando fechada.
- Cada passo CONFIRMADO alimenta essa página (e os dados em `viz/*.json`).

## Ordem de execução
Passos já feitos: 1,4,7,8,10,13,14 (+17 parcial). Novos, em ordem: 2,3 (grafêmica) → 5,6 (silábico) → 9,11,12
(morfologia) → 15 (Zipf) → 16,18 (semântica) → 19,20 (sintaxe+gramática). Site atualizado a cada confirmação.
