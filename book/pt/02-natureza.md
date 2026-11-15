# PARTE I — A PESQUISA

# Capítulo 1 — O que o *Liber Loagaeth* é

## Não é ruído, não é cifra: é uma língua

A primeira pergunta é também a mais básica: o que são essas grades? Ruído? Uma cifra? Um texto numa língua? A medida responde com evidências convergentes de que é uma **língua** — construída, estranha, mas língua — e **não** ruído nem código escondido. Quatro medidas independentes o estabelecem.

### A lei de Zipf

Em toda língua natural, a frequência das palavras cai segundo uma lei de potência de inclinação próxima de −1 (a palavra mais comum aparece o dobro da segunda, o triplo da terceira...). Medido no Loagaeth — tomando como "palavras" os nomes recorrentes — a inclinação de Zipf é de **−1,31** com ajuste r² de **0,96** [128_zipf, a92]. É comportamento de língua, não de sequência aleatória (que daria inclinação próxima de zero). E mais: o livro real tem **88 nomes distintos** no inventário recorrente, contra **68,8** num surrogate de mesmo tamanho — o livro é **mais rico** em vocabulário que o seu próprio ruído fonotático.

![Figura 1.1 — A frequência dos nomes cai como numa língua (inclinação −1,31); o surrogate não acompanha. [128_zipf]](../figuras/fig_zipf.png)

### A entropia e a memória

A incerteza média por letra, medida como **compressibilidade**, separa o livro do acaso de forma decisiva. Comprimido, o texto real gasta **3,55 bits por letra** (zlib) ou **3,28** (bz2); o mesmo texto embaralhado gasta **4,58** e **4,32**. A diferença — cerca de um bit inteiro por letra — é **estrutura real**: há memória, há regra, as letras não são sorteadas [19_machine, seção C].

![Figura 1.2 — O texto real comprime muito abaixo do embaralhado: um bit por letra de ordem genuína. [19_machine]](../figuras/fig_compressao_bits.png)

De onde vem essa memória? De uma régua muito específica. Medindo a incerteza de uma letra dado o seu contexto: sozinha, uma letra carrega **3,95 bits**; sabendo a letra **de cima** (a coluna), cai para **3,94** — quase nada; sabendo a letra **à esquerda** (a linha), despenca para **3,09** [19_machine, seção B]. A memória do livro é **horizontal**. Guardaremos esse fato: ele é a chave de leitura de todo o Capítulo 3 e Capítulo 5.

### A morfologia

Os nomes exibem estrutura de tipo semítico: uma **raiz consonantal** vestida por um **padrão vocálico**. A prova mais limpa são os **pares mínimos** — nomes idênticos exceto por uma vogal — exatamente como o *pola/pala* que o próprio Dee registrou: **13 deles**, muito acima do acaso, enquanto pares que diferem por uma **consoante** são raríssimos (apenas 2) [a92, #358, #403]. A identidade está na consoante; a vogal é trocável. O Capítulo 2 disseca esse gerador.

### A linha como inventário

Um quarto sinal, independente e forte: **cada linha de 49 letras é um inventário balanceado do alfabeto**. As letras se espalham por igual pelas 49 linhas de uma face muito mais do que o acaso permite — as consoantes com densidade **0,71× a esperada** (z ≈ −4,5), e o efeito aparece em **36 de 42 folhas** testadas; nenhum nulo o reproduz [a75]. A linha não é uma frase: é uma distribuição deliberada, quase um verso construído para "conter um pouco de tudo".

O que o livro diz de si, nos diários, casa com a medida: *"every letter here bringeth furth the Names of God: but they are but one Name"* — toda letra traz os Nomes de Deus, mas são **um só Nome**. E ainda: *"49 voices, whereunto the so many powers shall be obedient."* Um livro **de nomes** e **de vozes**.

## Três camadas

A medida separa o livro em três estratos distintos, cada um com assinatura estatística própria:

**A folha 1 — a língua.** Única folha espaçada em palavras, é o **léxico**: recorrência real, boa-formação, famílias de palavras, prosódia marcada com acentos. A folha 1 **divide vocabulário fino com as Chamadas**: lendo a grade de todos os modos, 489 palavras das Chamadas reaparecem, e a Chamada 1 encontra 68 de 86 das suas palavras [a94, a98]. É a página-irmã das Claves, a camada de linguagem articulada [#331, #333].

**As folhas 2–48 — o campo de nomes.** As grades densas. Não são frases: a ordem das letras não carrega informação de sentença (nenhuma sintaxe de frase sobrevive ao nulo — a ordem ampla de palavras dá 19 pares ordenados contra 16,2 no surrogate, [a106]). São um **campo gerado de nomes** que recorrem em famílias. Entra-se pela folha 2 — a folha 1 é selada, sem Chave.

**A costura 26–28 — o limiar.** Uma faixa anômala onde a leitura reta falha e o conteúdo passa para a **diagonal**. É a zona de **maior entropia e menor compressibilidade** do livro todo (Cap. 5): o ponto de máxima desordem, o umbral. É também a região mais **densa em nomes** quando lida na diagonal (44 por mil letras contra 29 na reta), o que valida a leitura diagonal ali [a96].

## O arco do livro: densidade e dissolução

Mapeando a densidade de nomes folha a folha, o livro tem **forma**: abre, adensa no miolo, e **dissolve** no fundo. O "profundo" (folhas 41–48) é **dissolução**: os nomes somem, a repetição colapsa, a entropia sobe, a vogal escurece de A para U [#360, #382].

Esse arco não é um detalhe estético: é um dos achados mais robustos do livro, porque **três medidas independentes apontam a mesma zona de dissolução** no fundo — o desaparecimento dos nomes [#360], o escurecimento da vogal A→U [#382], e a fratura da identidade elemental [#397]. O fim do livro se desfaz em **toda** dimensão mensurável. É o Capítulo 6 inteiro.

## O que o livro NÃO reivindica ser

Antes de prosseguir, uma honestidade que orienta todo o resto: medimos um **esqueleto de língua e um dicionário parcial**. O **sentido pleno** de cada nome — o que NOCHA "quer dizer" — ou está nas poucas âncoras traduzidas das Chamadas, ou **pertence à prática, não à página**. As palavras das Chamadas têm tradução posta na posição por Dee; os nossos nomes-raiz (NOCHA e companhia) têm **zero** âncora de tradução [a97]. O próprio registro de Dee é explícito: *"Interpret not."* Não há uma tradução escondida a decifrar. Isto não é uma lacuna do estudo; é um **achado**, confirmado por dentro (nenhuma cifra interna sobrevive ao nulo — Parte II) e por fora (nenhuma fonte dá glosa).

O que **há** é a anatomia da língua. É o que os próximos capítulos dissecam.

\newpage
