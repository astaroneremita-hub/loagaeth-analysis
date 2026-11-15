# Apêndice A — Como refazer cada medida

Todo achado deste livro é **reproduzível bit a bit**. A disciplina (Cap. 0):

- **Python de biblioteca padrão**, sem dependências externas na análise.
- **Semente fixa: 1583** (o ano da primeira recepção do Livro). Toda aleatoriedade — embaralhamentos, surrogates, permutações — parte dela, de modo que cada execução devolve os mesmos números.
- **Modelos nulos** em cada afirmação: embaralhamento (shuffle), surrogate de Markov-3, permutação controlada (Cap. 0).
- **Veredito explícito**: REAL / REFUTADO / DESCRITIVO / LEAD.

## Os módulos de análise

As medidas vivem em `src/aNNN_*.py`, numerados na ordem em que foram feitos. Grupos principais:

- **a01–a22** — fundação: gramática posicional, regra de não-dobrar, bordas de linha, quatro segmentos, famílias (CHASTOR), as duas casas, leitura diagonal da costura, caminho único nos losangos, registro vocálico.
- **a71–a106** — a fase de territórios e gerador: estratificação de linha, nomes tecidos na grade (z alto), mapa de território, gramática gerativa, descoberta de nomes pela gramática, gematria e cross-system (refutados), perfis de entidade.
- **a190+** — a fase de nomes externos e som: traços das Torres (refutado), anjos por subângulo (refutado), eixo-som (pronunciabilidade, assonância, vogal-final, melodia-A, pulso-A), os dois registros de voz, o conflito elemental signo×planeta, o arco de dissolução.

Cada módulo grava um `results/*.json` com a estatística e o escore-z do seu teste.

## Os dados

- **Fonte primária:** transcrição das 48 folhas do *Liber Loagaeth* (Sloane MS 3189), dois lados por folha; a folha 1 espaçada em palavras (léxico); a 49ª só por relato.
- **Alfabeto:** 21 letras enoquianas — A B C D E F G H I L M N O P Q R S T U X Z.
- **Corpus de comparação:** Chamadas (Claves Angelicae, Sloane 3191), Tábuas de Vigia, 91 governadores, Heptarquia, gematria (Liber Scientiae, *True and Faithful Relation*).

## As telas interativas

As visualizações (em `viz/`, servidas localmente) acompanham a análise: catálogo bilíngue, voz do Loagaeth, mapa de ocorrências, estrutura/tear, dialetos, nomes recorrentes, guia prático, Chamadas↔tabelas, ritual. Todas em português (o catálogo com alternância PT/EN).

\newpage

# Apêndice B — Glossário

- **Modelo nulo.** Versão do livro sem a estrutura testada (embaralhada, surrogate ou permutada), contra a qual se mede o real.
- **Escore-z.** Quantos desvios-padrão o valor real está acima/abaixo do nulo. |z|>3 real; |z|>6 decisivo; z negativo = anti-estrutura.
- **Surrogate de Markov-3.** Texto gerado respeitando as probabilidades de transição de 3 letras do livro real; preserva a fonotática local.
- **Princípio de Babel.** Um inventário grande o bastante aceita qualquer coisa por acaso; por isso só conta o que supera o nulo.
- **Casa.** Classe gramatical de nomes (casa NOCHA D-/AD-; casa GETH L-/X-), distinguida por afixos e registro vocálico.
- **Família.** Conjunto de nomes com raiz consonantal aparentada (CHASTOR, NOCHA, GETH, ANZACH, DAXVAR, ACLAX, CHIDNO, ALGETH).
- **Par mínimo.** Dois nomes idênticos exceto por uma vogal (ex. *pola/pala*); prova de que a consoante é identidade e a vogal é registro.
- **Template.** Gabarito vertical (coluna) que sustenta a forma sem carregar sentido (z=+173).
- **Anti-repetição.** Tendência da linha a evitar repetir letras/padrões (z=−77); a linha "avança".
- **Costura (26–28).** Faixa-umbral de máximo caos onde a leitura migra para a diagonal.
- **Arco de dissolução.** O profundo (folhas ~41–48), onde nomes somem, vogal escurece e a identidade elemental se fratura.
- **Eixo-som.** Conjunto de propriedades que fazem o livro cantável (pronunciabilidade, assonância, vogal-final, melodia-A, pulso-A).
- **Dois registros.** A mesma língua em fala (Chamadas) e em invocação (nomes das tabelas).

\newpage

# Apêndice C — Nota final e crédito de pesquisa

Este livro é o registro honesto de um estudo que mediu o *Liber Loagaeth* com disciplina estatística e separou dois planos: o que a medida pode afirmar (Partes I–II) e o que a prática faz com o que sobrou (Parte III). O método é o argumento: **nada conta sem superar o nulo**, e o que falhou está relatado tão alto quanto o que passou.

Qualquer uso dos achados, métodos, termos ou dados desta obra exige a referência da página de licença:

> Astaron Eremita. *Liber Loagaeth — Anatomia de uma Língua Selada.* 1ª ed., 2026.

*"Every letter here bringeth furth the Names of God: but they are but one Name."*

\newpage
