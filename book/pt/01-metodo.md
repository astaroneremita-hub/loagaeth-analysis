# Capítulo 0 — Método: a disciplina do modelo nulo

## O problema de olhar para o caos

Uma grade de 49×49 letras — 2.401 casas — repetida por quase cinquenta folhas é um terreno fértil para a **pareidolia**. Em quase meio milhão de letras, qualquer nome, qualquer palavra, qualquer "código" que se procure será encontrado, exatamente como se encontram rostos em nuvens. O problema central de qualquer estudo honesto do *Liber Loagaeth* não é **achar** padrões — é distinguir os padrões **reais** dos que o acaso fabrica. Chamamos a isso o **princípio de Babel**: um inventário grande o bastante aceita qualquer coisa. Os dígitos de π contêm o seu nome, o meu, e todos os nomes de anjos já escritos — isso não os torna um grimório.

Por isso, a regra única e inflexível deste estudo:

> **Nenhum padrão conta como real até superar um modelo nulo.**

Esta não é uma formalidade. Ao longo da pesquisa, a maioria esmagadora das hipóteses **caiu** neste crivo — mais de cem refutações estão catalogadas na Parte II e no aparato. A medida existe para derrubar ideias bonitas, não para confirmá-las. Quando uma sobrevive, sobrevive porque não teve como cair.

## Os três modelos nulos

Para cada afirmação, construímos uma versão do livro **sem** a estrutura testada, medimos o mesmo fenômeno nela, e comparamos. Três nulos, do mais fraco ao mais severo:

1. **Embaralhamento (shuffle).** As mesmas letras, nas mesmas quantidades, em ordem aleatória. Preserva a **frequência** de cada letra, destrói toda ordem. É o nulo-base: se o fenômeno real não supera o embaralhado, ele é puro efeito da composição de letras.

2. **Surrogate de Markov-3.** Um texto gerado letra a letra respeitando as probabilidades de transição de três letras do livro real. Preserva os **hábitos locais** de escrita (os pares e trios de letras comuns). Um padrão que supera o shuffle mas **não** o Markov-3 é apenas um subproduto da fonotática — não um sinal independente. Este nulo é o mais duro, e vários achados "do som" (Cap. 4) encolhem diante dele; nós o dizemos, em vez de escondê-lo.

3. **Permutação controlada / anagrama.** Para testes posicionais e de direção, embaralham-se apenas as unidades relevantes (as linhas de uma face, a ordem das folhas, os dígitos de um número) preservando o resto. Isola o efeito específico.

## A régua: o escore-z

A força de um achado é o **escore-z**: quantos desvios-padrão o valor real está acima (ou abaixo) da distribuição do nulo.

| escore-z | leitura |
|---|---|
| \|z\| < 2 | dentro do acaso. **Não conta.** |
| \|z\| ≈ 2–3 | sugestivo, frágil. Relatado como *lead*, não achado. |
| \|z\| > 3 | **real.** Sobrevive ao nulo. |
| \|z\| > 6 | **decisivo.** |

Um z **negativo** forte também é informação: significa que o real está **abaixo** do acaso — uma anti-estrutura. (Exemplo real: na linha, letras iguais se **evitam**; a repetição imediata tem z ≈ −4,5, [a75].)

## Convenções e honestidade

- **Semente fixa (1583).** Toda aleatoriedade usa a mesma semente — o ano da primeira recepção do Livro por Dee — para que cada teste seja **reproduzível** bit a bit.
- **Python de biblioteca padrão.** Sem dependências externas na análise: qualquer pessoa pode rodar os módulos (`src/aNNN_*.py`, `python src/run_all.py`) e obter os mesmos números. Cada módulo grava um `results/*.json` com a sua estatística.
- **Veredito explícito.** Cada achado é marcado **REAL** (bateu o nulo), **REFUTADO** (caiu), **LEAD** (indício frágil) ou **DESCRITIVO** (um fato verdadeiro por construção ou inspeção, sem alegar sinal oculto).
- **O que falhou é relatado tão alto quanto o que passou.** Uma hipótese querida que cai é um resultado, não um embaraço. A Parte II deste livro existe para isso.
- **Separação de planos.** A medida responde "existe estrutura objetiva?". Ela **não** responde "funciona como magia?" — pergunta de outro plano, operativa, que a Parte III trata na sua própria lógica. Confundir os dois é o erro que este livro evita de ponta a ponta. Um veredito **REFUTADO** significa "não há cifra objetiva aqui", **não** "não funciona como prática".

## Os dados

A fonte é a transcrição das 48 folhas do *Liber Loagaeth* (Sloane MS 3189), cada folha com dois lados ("a" e "b"), a maioria grades densas de 49×49 letras; a folha 1 é espaçada em palavras (é a página de **léxico**); a 49ª folha "que não é, não foi, não será conhecida" existe só por relato. A transcrição de referência é a de Clay Holden / Joseph Peterson; conferimos uma transcrição independente (kondor.de) e ela é **cópia** da de Peterson — difere em 1 letra em 23.712 [a53], o que fecha a porta para erros de fonte.

O alfabeto é o enoquiano de 21 letras: **A B C D E F G H I L M N O P Q R S T U X Z** (sem J, K, V, W, Y). O corpus de comparação — Chamadas (Claves Angelicae), Tábuas de Vigia, 91 governadores, Heptarquia, gematria — vem das edições de referência (Sloane 3191, *A True and Faithful Relation*, *Liber Scientiae*).

Com o método posto, passemos ao que a medida revelou.

\newpage
