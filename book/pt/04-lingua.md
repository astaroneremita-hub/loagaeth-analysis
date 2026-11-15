# Capítulo 3 — A língua: consoante, registro, fonologia

O Capítulo 1 mostrou **que** o Loagaeth é uma língua; o Capítulo 2, **como** ela monta nomes. Este capítulo disseca a língua por dentro: onde mora a identidade, o que faz a vogal, por que o sistema de consoantes é o de uma língua natural, e por que tudo se lê em linha.

## A identidade é consonantal

A descoberta estrutural central: **a consoante carrega a identidade; a vogal carrega o registro**. É o princípio das línguas semíticas, onde a raiz é um esqueleto de consoantes e as vogais que a vestem dão a palavra concreta.

A prova é a **entropia por classe** [#402]. A consoante é quase imprevisível (carrega quase toda a informação); a vogal é previsível, de um conjunto pequeno, e **nos nomes colapsa em A**:

| Registro | Entropia da vogal | Entropia da consoante |
|---|---:|---:|
| **Nomes** (invocação) | **1,25 bits** | **3,48 bits** (de 3,81 máx.) |
| **Chamadas** (fala) | 1,96 bits | 3,91 bits (de 4,17) |
| **Livro** (todo) | 1,80 bits | 3,81 bits |

Nos nomes, a vogal tem só 1,25 bits — quase sem informação lexical — enquanto a consoante satura perto do máximo. A consoante **é** a palavra; a vogal é a melodia que a carrega.

![Figura 3.1 — A consoante carrega a identidade; a vogal colapsa em A nos nomes. [#402]](../figuras/fig_consoante.png)

Os pares mínimos (Cap. 2) confirmam caso a caso: trocar a vogal não cria outra identidade — cria outra forma do mesmo nome. A implicação operativa, guardada para a Parte III: **o nome se reconhece pelas consoantes**; a vogal é liberdade de registro.

## O sistema de consoantes é uma fonologia natural

As consoantes do Loagaeth não são um amontoado: formam um **inventário fonológico balanceado**, como o de uma língua natural [#403].

- **Ponto de articulação:** coronal 53%, velar 21%, labial 15%, glotal 11%. O domínio coronal é o ponto **não-marcado**, típico de línguas naturais.
- **Modo de articulação:** oclusiva 35%, fricativa 29%, líquida 18%, nasal 17% — entropia 1,93 de 2,0 máximo, os quatro modos bem representados. Um inventário equilibrado, não um ruído enviesado.

Essa coerência fonológica **eleva a confiança** de que é língua desenhada, não aleatória: o acaso não produz um sistema de consoantes equilibrado em ponto e modo.

## A vogal é registro

Se a vogal não é identidade, o que ela é? **Registro** — o "tom" em que o nome é dito. A distribuição vocálica **muda de região para região**, escurecendo de A (aberta, clara) para U (fechada, escura) à medida que se desce para o profundo (Cap. 6). A vogal é o parâmetro que o livro **modula** mantendo as consoantes como âncora. É a camada melódica — o que, no Cap. 4, se mostra literalmente **cantável**.

## As leis fonotáticas

Uma língua tem **fonotática** — regras do que pode seguir o quê. As do Loagaeth são de uma língua **balanceada e pronunciável**:

- **Regra de não-dobrar.** Letras iguais evitam-se em sequência: a repetição imediata é muito mais rara que no acaso (anti-estrutura, z ≈ −4,5). Uma língua feita para ser dita evita o tropeço da geminação.
- **Bordas de linha marcadas.** O início da linha prefere consoante; o fim, vogal. As palavras não vazam de qualquer jeito pelas bordas; há um gabarito [#42, #391].
- **Sílaba C(C)-V.** As vogais quase sempre aparecem sozinhas no núcleo (run = 1); as consoantes em grupos de média 1,94. A batida silábica é consoante(s)-vogal [#400].

## A gramática é só horizontal

O teste decisivo de direção mede a **informação mútua** (quanto uma letra prediz a vizinha) em cada eixo [#400]:

| Direção | Informação mútua |
|---|---:|
| **Horizontal** (→) | **0,60 bits** |
| Vertical (↓) | 0,007 bits |
| Diagonal (↘) | 0,016 bits |
| Anti-diagonal (↙) | 0,008 bits |

A gramática é **~90× mais forte na horizontal**. As colunas e diagonais não têm sintaxe — o que há nelas é **template** (um molde de forma, não de sentido; Cap. 5). Isso resolve a questão da leitura: **o Loagaeth lê-se em linha, da esquerda para a direita** — exceto a costura 26–28, onde o conteúdo migra localmente para a diagonal, um truque local, não uma direção gramatical.

![Figura 3.2 — A gramática é ~90× mais forte na horizontal: lê-se em linha. [#400]](../figuras/fig_direcao.png)

A mesma conclusão vem da régua 2-D (Cap. 1): saber a letra de cima (vertical) quase não reduz a incerteza (3,95 → 3,94 bits), mas saber a da esquerda (horizontal) reduz muito (3,95 → 3,09) [19_machine].

![Figura 3.3 — A letra à esquerda tira ~0,9 bit de incerteza; a de cima, quase nada. [19_machine]](../figuras/fig_2d_rule.png)

## O horizonte da gramática: curto

Até onde a regra alcança? A memória excede o acaso apenas em distâncias de **4 a 12 letras**; além disso, é só mistura lado a lado [a22, #74]. A gramática do Loagaeth é de **alcance curto** — regras locais de montagem de sílaba e de nome, não períodos longos de sintaxe de frase. É mais uma prova de que são **nomes**, não sentenças: um nome é uma unidade curta e fechada; uma frase encadeia dependências longas. O Loagaeth não as tem.

## Uma só direção

Prova final de que a língua tem **uma** direção: lida ao contrário (espelhada), ela se desfaz — CHASTOR, que aparece 179 vezes na leitura direta, aparece **zero** vezes invertido; o modelo de letra direto gasta 3,5 bits, o invertido 6,1 [a21, #67]. O texto tem frente e verso; só a frente carrega nomes.

## Síntese

A língua do Loagaeth é: **consonantal** na identidade, **vocálica** no registro, **fonologicamente equilibrada**, **horizontal**, **de alcance curto** e **de direção única**. É uma língua desenhada para **nomear** e para **ser dita** — não para narrar e não para esconder. O próximo capítulo leva isso à sua consequência: o livro foi feito para ser **cantado**.

\newpage
