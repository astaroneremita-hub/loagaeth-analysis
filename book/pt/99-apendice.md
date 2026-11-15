# Apêndice A — Como refazer cada medida

Todo achado deste livro é **reproduzível bit a bit**. A disciplina (Cap. 0):

- **Python de biblioteca padrão**, sem dependências externas na análise.
- **Semente fixa: 1583** (o ano da primeira recepção do Livro). Toda aleatoriedade parte dela.
- **Modelos nulos** em cada afirmação: embaralhamento, surrogate de Markov-3, permutação/anagrama controlado.
- **Veredito explícito**: REAL / REFUTADO / DESCRITIVO / LEAD.
- Rodar tudo: `python src/run_all.py`. Cada módulo grava um `results/*.json` com a sua estatística e escore-z.

## Os módulos de análise (203 resultados)

As medidas vivem em `src/aNNN_*.py`, numerados na ordem em que foram feitos. Grupos principais:

- **a01–a22 — fundação.** Gramática posicional, regra de não-dobrar, bordas de linha, quatro segmentos, famílias (CHASTOR), as duas casas, leitura diagonal da costura, caminho único nos losangos, registro vocálico, memória 4–12 letras, regra 2-D (horizontal manda).
- **a71–a106 — territórios e gerador.** Estratificação de linha (inventário balanceado), nomes tecidos na grade (king-move), mapa de territórios por dois métodos, gramática gerativa raiz+afixo, 32 nomes novos preditos, super-nomes (cadeias de raízes), duas camadas de léxico, sintaxe GETH→ACLAX, gematria e cross-system (refutados), perfis de entidade.
- **a190+ — nomes externos e som.** Traços das Torres (refutado), anjos por subângulo (refutado), eixo-som (pronunciável #386, assonância #387, acento latino #388, vogal-final #391, melodia-A #392, pulso-A #398), Menzerath (artefato), dois registros de voz #401, identidade consonantal #402, fonologia balanceada #403, sem template posicional #404, classes gramaticais por casa #405, Ars Paulina ausente #406, salto-7 e Laycock refutados #407.

## Os dados

- **Fonte primária:** transcrição das 48 folhas do *Liber Loagaeth* (Sloane MS 3189), dois lados por folha; folha 1 espaçada em palavras (léxico); a 49ª só por relato. Transcrição de Holden/Peterson; conferida contra kondor.de (cópia, 1 letra em 23.712 de diferença).
- **Alfabeto:** 21 letras enoquianas — A B C D E F G H I L M N O P Q R S T U X Z.
- **Corpus de comparação:** Chamadas (Claves Angelicae, Sloane 3191), Tábuas de Vigia, 91 governadores, Heptarquia, gematria (Liber Scientiae, *A True and Faithful Relation*).

## As telas interativas

As visualizações (em `viz/`, servidas localmente) acompanham a análise: catálogo bilíngue, voz do Loagaeth, mapa de ocorrências, estrutura/tear, dialetos, nomes recorrentes, guia prático, Chamadas↔tabelas, ritual, atlas 3D.

\newpage

# Apêndice B — Glossário

- **Modelo nulo.** Versão do livro sem a estrutura testada (embaralhada, surrogate ou permutada), contra a qual se mede o real.
- **Escore-z.** Quantos desvios-padrão o real está acima/abaixo do nulo. |z|>3 real; |z|>6 decisivo; z negativo = anti-estrutura.
- **Surrogate de Markov-3.** Texto gerado respeitando as probabilidades de transição de 3 letras do livro real; preserva a fonotática local. O nulo mais severo.
- **Princípio de Babel.** Um inventário grande o bastante aceita qualquer coisa por acaso; só conta o que supera o nulo.
- **Casa.** Classe gramatical de nomes (casa NOCHA D-/AD-; casa GETH L-/X-), distinguida por afixos e registro vocálico.
- **Família.** Conjunto de nomes com raiz consonantal aparentada (NOCHA, GETH, CHASTOR, ANZACH, DAXVAR, ACLAXT, ALGETHA).
- **Par mínimo.** Dois nomes idênticos exceto por uma vogal (*pola/pala*); prova de que a consoante é identidade, a vogal é registro. 13 vocálicos vs 2 consonantais.
- **King-move.** O traçado (passo de rei no xadrez) por onde um nome está tecido na grade; mede se o nome está costurado ou só pousado.
- **Template.** Gabarito vertical (coluna) que sustenta a forma sem carregar sentido (MI vertical 0,007 bits).
- **Anti-repetição.** Tendência da linha a evitar repetir letras (z ≈ −4,5); a linha "avança".
- **Costura (26–28).** Faixa-umbral de máximo caos onde a leitura migra para a diagonal.
- **Arco de dissolução.** O profundo (folhas ~41–48), onde nomes somem, vogal escurece A→U e a identidade elemental se fratura.
- **Eixo-som.** Conjunto de propriedades que fazem o livro cantável (pronunciável, assonante, acento latino, vogal-final, melodia-A, pulso-A).
- **Dois registros.** A mesma língua em fala (Chamadas) e em invocação (nomes das tabelas).
- **Onomasticon gerativo.** O que o Loagaeth é: um livro feito para gerar nomes de forças.

\newpage

# Apêndice C — Nota final e crédito de pesquisa

Este livro é o registro honesto de um estudo que mediu o *Liber Loagaeth* com disciplina estatística e separou dois planos: o que a medida pode afirmar (Partes I–II) e o que a prática faz com o que sobrou (Parte III). O método é o argumento: **nada conta sem superar o nulo**, e o que falhou está relatado tão alto quanto o que passou — mais de cem refutações, cada uma com o seu número.

Qualquer uso dos achados, métodos, termos ou dados desta obra exige a referência da página de licença:

> Astaron Eremita. *Liber Loagaeth — Anatomia de uma Língua Selada.* 1ª ed., 2026.

*"Every letter here bringeth furth the Names of God: but they are but one Name."*

\newpage
