# 20 ideias originais — novas descobertas e desmistificação

Baseadas no que já temos. Cada uma traz **o quê · por que · como testar (null)** e uma
etiqueta: **[D]** descoberta (achar estrutura nova) · **[M]** desmistificação (matar
falso-positivo / pareidolia) · **[V]** visual/estrutural.

> **O princípio que guia metade delas (o "Pi / Babel"):** num espaço grande o bastante,
> *qualquer* string aparece. O nosso gerador já tem **7.200** nomes bem-formados (ou ~**1
> milhão** com o inventário do livro). Então achar um nome-alvo lá dentro **não prova
> nada** — só conta se bater o **null** (a linha-base de Babel). Metade das ideias abaixo
> é exatamente para separar sinal de ruído.

---

## A — Descoberta (padrão novo)

1. **[D] Compressão do livro vs acaso.** Comprime o Loag inteiro (zlib) e compara com 1000
   embaralhamentos. Se o real comprime mais, há estrutura global não-aleatória. _Null:
   shuffle de letras._
2. **[D] Assinatura de "voz/escriba" por folha.** Matriz de transição de letras por folha
   → clusteriza as 48 em grupos (mãos/dialetos). _Null: shuffle de linhas dentro da folha._
3. **[D] Célula central (25,25) de cada quadrado.** Junta as 48 letras centrais → é
   nome/palavra? _Null: 48 posições aleatórias._
4. **[D] Texto da moldura.** Já achamos que os nomes grudam na borda (z=+42). Extrair o
   anel de borda de cada face como texto contínuo e ler o que diz.
5. **[D] Índice de rotação por folha.** Qual folha se lê em linha, qual na diagonal ↘?
   (26-28 giram; mapear TODAS.) Gera o "mapa de eixos" do livro.
6. **[D] A costura dos losangos.** Nos losangos, os nomes atravessam a linha larga (a dobra
   das duas pirâmides) ou a evitam? _Null: deslocar as linhas._
7. **[D] Grafo social das entidades.** Quais nomes dividem a mesma folha (co-ocorrem) →
   rede de "convivência"; detectar comunidades. _Null: nomes jogados em folhas aleatórias._
8. **[D] Migração de nome pelo livro.** A presença de um nome na folha N prevê N+k? Nomes
   que "costuram" a sequência. _Null: ordem de folhas embaralhada._

## B — Desmistificação (o princípio Babel)

9. **[M] Curva de Babel.** Plotar o falso-positivo vs o tamanho do inventário: a que
   tamanho o gerador passa a conter *qualquer* nome-alvo? Formaliza o "está no Pi".
10. **[M] Scanner de entidades reais.** Cola 200 nomes (deuses/anjos/demônios de várias
    tradições) e mede a taxa de acerto vs null — ferramenta para provar que "achei minha
    divindade" costuma ser ruído. (Primeira rodada já feita, #348: sem sinal limpo.)
11. **[M] Teste da megasena/data.** Procura números e datas (como posições de letra) no
    livro vs null. Mostra que aparecem no acaso — desmistifica a esperança estilo-Pi.
12. **[M] Palavra-escondida vs livro embaralhado.** Quantas palavras PT/EN/latim aparecem
    como substring no Loag vs no Loag embaralhado? Se igual, "achar palavra" é ruído.
13. **[M] Estabilidade por permutação.** Para cada achado nosso, quanto sobrevive ao
    embaralhar a grade? O que sobrevive ao shuffle é artefato, não descoberta.
14. **[M] Explosão de caminhos de leitura.** Quantos caminhos distintos (linha, coluna,
    diagonal, cavalo, espiral) existem por grade? Com tantos, calcular o nº esperado de
    "qualquer nome" por acaso — e comparar com o que realmente achamos.
15. **[M] Null-playground universal.** Em toda visualização, um botão "mostrar null ao
    lado" que roda a mesma análise em dados embaralhados. Sinal vs ruído, sempre juntos.
16. **[M] Reversível por semente.** Demonstrar que "prever" um nome específico é só escolher
    a semente certa do gerador — igual ao Pi. Desmonta a mística da previsão.

## C — Visual / estrutural

17. **[V] Cubo 3D das 48 faces.** Empilhar as grades e procurar colunas verticais
    (atravessando páginas) de nome vs null.
18. **[V] "A descida" animada.** O gradiente Terra→Água como jornada fluida pelo livro
    (semente → corpo → profundo), tocando folha a folha.
19. **[V] Mapa de calor de bigramas** do livro vs Chamadas — ver o "dialeto" (quais pares
    de letra o Loag usa a mais/menos).
20. **[V] Atlas unificado com camada de null.** Juntar tudo (nomes, famílias, esqueletos,
    elementos, mapa) e, em cada lente, o botão null — o projeto inteiro à prova de
    pareidolia.

---

## Minha recomendação (as 3 primeiras a fazer)

- **#9 Curva de Babel** + **#10 Scanner de entidades** — respondem de vez "dá pra achar
  qualquer entidade?" com números, e viram a ferramenta de desmistificação do projeto.
- **#2 Assinatura de escriba** — tem boa chance de achar estrutura nova real (várias mãos
  / regiões), e é independente dos nomes (sem circularidade).
- **#4 Texto da moldura** — leitura concreta que ainda não fizemos, com alvo claro.

As demais ficam de reserva. Diz qual atacar.
