# O tecido e a hierarquia do Loagaeth

Fase de busca a71–a80. Toda afirmação é medida contra um modelo nulo (letras embaralhadas, surrogate
Markov-3 que preserva o fluxo local, ou embaralhamento por coluna). Documentação e imagens ficam no
repositório.

---

## 1. Cada linha é um inventário balanceado do alfabeto (a75) — CONFIRMADO NOVO

Conte quantas vezes uma letra aparece em cada linha de um quadrado. No livro, cada letra aparece quase o
mesmo número de vezes em **toda** linha. Embaralhe as mesmas letras na mesma grade e a contagem passa a
oscilar muito. O livro distribui cada letra por igual entre as 49 linhas — toda linha é uma amostra
equilibrada do alfabeto inteiro.

![Estratificação por linha](../figures/fig_row_stratification.png)

Números (índice de dispersão = variância/média da contagem por linha; <1 = regular/anti-aglomerado):

| conjunto | real / acaso | z |
|---|---|---|
| todas as letras | 0,72 | −5,2 |
| vogais | 0,68 | −2,8 |
| **consoantes** | **0,71** | **−4,5** (36/42 folhas) |

Controles: embaralhamento total dá 0,92 (quase Poisson); embaralhamento por coluna dá ~0,93. Nenhum
reproduz o valor real (~0,57). Vale para consoantes, então não é a métrica de sílabas já conhecida. É um
arranjo 2D proposital: cada linha é uma unidade fechada (um verso/nome), não texto corrido.

## 2. Posição da letra na linha (a76)

Dentro da linha, **não** há coluna fixa por letra (concentração 0,07; previsibilidade ímpar-vs-par 0,59 ≈
acaso 0,58). Cada letra vagueia pela linha inteira. Só as bordas têm dono (regra já conhecida): V/I/P/Z no
começo, S/H/X no fim. Prevê-se *quantas* vezes a letra vem por linha, não *onde*.

## 3. Os nomes estão tecidos na grade (a77) — CONFIRMADO NOVO (forte)

Controle justo = as próprias letras do nome, embaralhadas. Os nomes das famílias traçam como caminho
king-move (saltando entre células vizinhas, sem reusar célula) muito acima dos seus embaralhamentos:
**232 de 460 pares nome-folha (50%) são "tecidos"** — o nome real traça ≥3 caminhos e nenhum dos 80
embaralhamentos alcança isso. CHASTOR tece em 30/37 folhas (15b: 271× o acaso); ADNOCHA em 14b traça 619
caminhos contra zero dos embaralhamentos. Nomes longos (ICHASTOR, NECHASTOR) traçam enquanto todo
embaralhamento traça zero.

![Nomes tecidos](../figures/fig_names_woven.png)

A *ordem* específica de cada nome está construída na grade; permutações não estão. O livro é tecido deste
vocabulário de nomes.

## 4. Mapa de territórios (a78) — CONFIRMADO NOVO (convergente)

Normalizando o tecido por família (z dentro de cada uma), cada folha ganha uma família-casa:

![Mapa de territórios](../figures/fig_territory_map.png)

- **CHADAX** abre o livro (posição média 13 de 42).
- **casa NOCHA** segura a frente-meio (bloco 12a–14b).
- **CHASTOR** é a espinha, com picos (15b, 18b).
- **casa GETH** domina o fundo (16a–27b).

Construído só do traço king-move vs letras embaralhadas, reproduz a geografia das duas casas (NOCHA cedo /
GETH tarde) que a leitura reta achou por outro método (a67). Dois métodos independentes, o mesmo mapa.

## 5. Poderes elementais (a79) — DESCRITIVO

Cada letra enoquiana carrega um elemento (correspondência Golden Dawn: signo → elemento). O elemento
dominante de um nome é seu poder: **CHADAX = Terra** (3/3 membros), **CHASTOR = Ar** (3/3), NOCHA = Ar/Água
misto, GETH = Fogo/Terra misto, DAHAHOXOM = Ar. Limites testados: a concordância vem do radical
compartilhado; e o elemento é do nome, não do território (as folhas-casa não carregam mais letras do seu
elemento que a média, z entre −1,1 e +0,9).

## 6. Mapa completo de entidades: Rei, corte e anjos menores (a80)

Modelo (igual às Torres): o nome que mais repete é o **Rei**; os seguintes são a corte; os que aparecem uma
vez são **anjos menores**. Só nomes validados (≥5 letras), contados nos dois sentidos.

![Hierarquia](../figures/fig_hierarchy_pyramid.png)

Hierarquia suprema do livro (repetição total): **Rei NOCHA** (492×, reina em 34 quadrados), **Nome de Deus
ADNOCHA** (168×), **Nome do Espírito NACHO** (148×), **Arcanjo CHASTOR** (132×), **Senior ANZACH** (127×);
anjos da corte ACLAX/NOCHAP/ALGETH; anjos menores = os nomes que aparecem 1×.

NOCHA reina quase sempre porque está dentro de toda a sua família (ADNOCHA, NOCHAP, NOCHASTOR). O
*governador local* de cada quadrado (tirando esse aninhamento) varia por região — ANZACH no meio, ALGETH no
fim, GRADAX no bloco 14–15, CHADAX na abertura — batendo com o mapa de territórios. A hierarquia completa de
cada quadrado, tier a tier, está em `results/80_full_hierarchy.json`. As folhas 25b–28b leem na diagonal e
precisam do fluxo decodificado (ficam fora desta contagem reta).

## 7. O que foi negado nesta leva (honestidade)

- **Leitura omni-direcional** (a71): o livro lê uma direção só; as outras 7 orientações não carregam nomes
  acima do acaso. Não é como as Torres.
- **Famílias de rotação grudadas de propósito** (a72/a73): varri 761 famílias; o clustering saiu no acaso. As
  ramificações estão coladas na página porque compartilham letras, não por posição intencional.

## Módulos

`a71_omnidirectional`, `a72_rotation_family`, `a73_family_sweep`, `a74_gematria_lines`,
`a75_row_stratification`, `a76_letter_position_map`, `a77_names_woven`, `a78_territory_map`,
`a79_hierarchy_powers`, `a80_full_hierarchy`. Figuras em `figures/`, geradas por `make_hierarchy_figures.py`.
Log em `docs/RESEARCH_LOG.md` #208–#216.

## 8. Lendo todas as tabelas como um todo — matriz nomes × tabelas

Começo da leitura unificada: cada nome principal em cada quadrado, de uma vez.

![Matriz nomes x tabelas](../figures/fig_names_tables_matrix.png)

Lê-se: a abertura (1a–5b) é esparsa — o livro "aquece", poucos nomes. De ~6a em diante o vocabulário
compartilhado adensa, e NOCHA/ADNOCHA/NACHO/CHASTOR/ANZACH formam a espinha presente em quase toda tabela.
O que achamos numa tabela aparece nas outras — é um sistema único, não quadrados isolados. Próximo passo:
para cada tabela, aplicar o conjunto completo de padrões (hierarquia, território, tecido) e marcar onde cada
achado reaparece.
