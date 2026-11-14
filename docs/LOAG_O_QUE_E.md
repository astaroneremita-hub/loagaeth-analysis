# O Loagaeth — o que descobrimos (só dele) e como usar

Inventário honesto, **apenas do Liber Loagaeth** (não Heptarquia, não Torres). Três camadas:
**PROVADO** (sobreviveu a controle forte), **DESCRITIVO** (fato medido), **CAIU** (não resistiu — não confie).
Depois: **uso ritual** e **uso de estudo**. Nada aqui é tradução nem intenção declarada de Dee.

---

## A. O que é o Loagaeth — PROVADO

1. **É um campo de nomes (onomasticon), não prosa nem cifra.** Cinco testes de null (vs Markov-3) refutam
   estrutura de texto/sentença/código. O livro é um **catálogo de nomes**, não uma mensagem a ler.
2. **As 49 folhas são uma sequência ordenada com estrutura composicional real.** A composição das folhas muda
   de forma sistemática ao longo da ordem do Dee: similaridade cai com a distância (Mantel r=0.52, permutação
   **p<1e-5**), e a ordem **se reconstrói só do conteúdo** (Spearman 0.87, cega à posição). Robusto a exclusões,
   features e algoritmos.
3. **A forma da deriva: platô → penhasco.** Estável pelos **quadrados (folhas 2-28)**, declina pelos **losangos
   (29-48)**, quase-vazio no fim. A fronteira **quadrados/losangos é uma descontinuidade composicional real**
   (change-point confirma). Os dois formatos físicos do manuscrito são composicionalmente distintos.

## B. Fatos do Loagaeth — DESCRITIVO (medido, real)

4. **~90 nomes recorrentes** existem no livro (aparecem em 2+ tabelas). São reais, estão no Sloane 3189.
5. **Eixo de letra da deriva:** A (letra mais comum) fica alta/estável nos quadrados e **despenca** nos losangos;
   I e as consoantes R·P·L **sobem** (cada uma p=0.002).
6. **Os nomes vivem na zona do A** (quadrados, densos) e **dissolvem** rumo ao fim (losango 45 ≈ 0.0008, quase
   sem nome). Densidade de nome correlaciona +0.71 com A, −0.53 com I.
7. **Folha 1 é distinta** — a fundação selada: o **I mais baixo de todas**, agrupa com as folhas de início. É o
   polo de entrada (entra-se por ela com a Chamada 1).
8. **Anti-hiato:** os nomes evitam vogais adjacentes (fonotática CV). Fato real.
9. **Decomposição esqueleto (consoantes) + melodia (vogais):** descrição válida de qualquer nome. (Não é uma
   gramática especial — ver C.)
10. **Raiz recorrente NOCHA** marca a "casa" dominante, presente na maioria das folhas dos quadrados.

## C. O que CAIU — não confie nisto

- **"Gramática gerativa semítica especial" (raiz-e-padrão como idioma não-concatenativo).** Testada contra
  Markov-0/1/2/3: a estrutura dos nomes é **fonotática de ordem 2-3** — um 3-grama reproduz tudo. A decomposição
  descreve, mas não acrescenta informação além da fonotática.
- **Forja com poder preditivo "mágico".** Não bate um modelo de caractere (Markov-2) ao prever nomes ocultos.
- **Código local deliberado na ordem das folhas.** Removida a tendência global, o resíduo = acaso. A ordem é uma
  **deriva global**, não uma cifra posicional.
- **Loag como fonte dos nomes das Torres/Heptarquia.** Não há vínculo específico (controle de outra tradição mata).
- **Tradução palavra-a-palavra dos nomes.** Nunca foi possível (sem Pedra de Roseta). Não é perda recente.

---

## D. Como usar — RITUAL

O que funciona de fato, com o rótulo honesto (construção fiel ao estilo, prática experimental; não entidade
revelada comprovada):

1. **Trabalhar os 90 nomes reais do livro.** Estão no manuscrito. Use por **invocação/vibração**. Escolha pela
   natureza elemental/planetária (convenção Golden Dawn — `viz/name_dictionary.html`).
2. **Gerar nomes novos no estilo real (a Forja — `viz/name_forge.html`).** Produz nomes pronunciáveis com a
   fonotática do livro. Para vibrar/invocar como experimento. São construções fiéis ao som real, não revelações.
3. **A regra de leitura (`viz/regra.html`):** achar nomes numa tabela no olho — ancora numa sílaba-raiz (CHA, NO,
   GE, STOR…), lê em linha, alterna consoante-vogal, 4+ letras, casa o léxico.
4. **A folha 1 como entrada** (selada; abre-se com a Chamada 1 "Ol sonf vorsg"), e **percorrer as folhas em
   ordem** — ancorado na sequência real do livro (a deriva confirma que a ordem importa).
5. **A casa NOCHA** como raiz dominante para trabalho amplo; os derivados para foco específico.
6. **Correspondências elementais** (`viz/name_language.html`, `tablet.html`): convenção usável para montar o
   ritual (cor, incenso, direção) — é tradição Golden Dawn, não propriedade medida das letras.

## E. Como usar — ESTUDO

1. **O objeto de pesquisa real é a ordem.** A deriva composicional (platô→penhasco, p<1e-5, reconstruível) é um
   achado não-trivial sobre um manuscrito de 1583. Perguntas abertas honestas: a deriva é **temporal** (acompanha
   a ordem de recepção das sessões)? É **específica do Loag** ou do escriba (comparar com as 8 tabelas Soyga do
   mesmo MS)?
2. **A descontinuidade quadrados/losangos** (folha ~29) é estrutural, não arbitrária — merece estudo próprio.
3. **Reframe metodológico:** o Loag é um **onomasticon**. Não procure uma mensagem escondida; estude a
   **distribuição dos nomes** e a **progressão da composição**. É assim que faz sentido analisá-lo.
4. **Reprodutível:** todos os testes em `src/a1xx_*.py`, figuras em `figures/audit_*.png`, relatório em
   `docs/RELATORIO_AUDITORIA.md`, log em `docs/RESEARCH_LOG.md`.

---

## F. A frase única

O Loagaeth **é** um catálogo de nomes com uma **ordem composicional real e estruturada** (platô nos quadrados,
declínio nos losangos). **Não é** um idioma secreto com gramática gerativa — isso é fonotática. Para a prática:
os 90 nomes reais e a Forja (nomes-no-estilo) são usáveis por invocação/vibração, com honestidade sobre o que
são. Para o estudo: a ordem do livro é o achado que vale, auditado e reproduzível.
