# Plano — fazer a leitura dos quadrados FAZER SENTIDO (ou provar que não é frase)

## Diagnóstico (o que descobrimos até aqui)
- A leitura atual ladrilha a grade impondo um dicionário (Dee + Dicionário + Leitch). Isso dá salada.
- **a111 (varredura de minlen 1→6):** em TODA escala a cobertura do livro real ≈ surrogate aleatório das mesmas
  letras (melhor z=2.7 em minlen=2, abaixo do limiar). Nenhum comprimento mínimo transforma em frase.
- **a107 / a110:** presença e cobertura de vocabulário angelical NÃO batem o acaso. ~70% da grade é material
  intraduzível (famílias de nome NOCHA/ANZACH/CHASTOR/GETH).
- Conclusão honesta provisória: os quadrados **não são prosa**. São um CAMPO DE NOMES com fragmentos de palavra das
  Chamadas. "Fazer sentido" pode significar ler os NOMES (o onomasticon), não decifrar uma sentença.

O plano abaixo ou acha uma leitura real escondida (Bloco C), ou estabelece formalmente o modelo campo-de-nomes
(Blocos B e D) — e ajusta o frontend pra não confundir (Bloco E).

## Regras
- Todo bloco com null model (Markov-3, shuffle de linha, surrogate da própria grade).
- Resultado REAL / REFUTADO / DESCRITIVO. Glosas em inglês.
- Nada commitado sem pedido. Docs atualizados, módulo a### + registro no RESEARCH_LOG.

## Bloco A — Escala de leitura ✅ FEITO (a111)
Varredura minlen 1-6, cobertura real vs null. Resultado: nenhuma escala bate o acaso. Guardado.
Próximo refinamento: repetir por DIREÇÃO (reta/coluna/diagonal) e por FONTE (só Dee) — ver se alguma combinação
específica destaca, mesmo que o geral não destaque.

## Bloco B — Descobrir as palavras DA PRÓPRIA GRADE (não impor dicionário) ⭐ chave
- **B1** Segmentação por entropia de ramificação (reaproveitar a102): achar onde as unidades naturalmente começam/
  terminam em cada linha/coluna/diagonal, sem dicionário.
- **B2** Dessas unidades naturais, quantas são: (a) palavra de dicionário, (b) raiz de família de nome, (c)
  desconhecida? Comparar com surrogate. Se as fronteiras naturais coincidirem com palavras de dicionário ACIMA do
  acaso, existe leitura real nas fronteiras certas (não nas que eu impus).
- **B3** Medir "taxa de palavra real por unidade descoberta" real vs surrogate.

## Bloco C — Algum quadrado soletra uma CHAMADA em ordem? ⭐ teste real de sentido
- **C1** Para cada Chamada (ordem de palavra conhecida, chamadas.json), deslizar a sequência enoquiana dela contra
  cada linha/coluna/diagonal de cada tabela; pontuar a maior corrida de palavras consecutivas NA ORDEM certa.
  Comparar com surrogate. Um acerto = um quadrado codifica literalmente um trecho de Chamada.
- **C2** Testar também a Chamada de TRÁS PRA FRENTE (Dee recebeu invertido) e começando em qualquer offset.
- Se C der positivo forte: achamos o sentido literal. Se der nulo: confirma que não é a Chamada escondida.

## Bloco D — Mapear os ~70% intraduzíveis (o campo de nomes) — lente cabalística
- **D1** Que fração das letras sem-tradução pertence às famílias de nome atestadas (NOCHA/ANZACH/CHASTOR/GETH e
  derivados)? Quantificar.
- **D2** Perfil elemental/gematria (Golden Dawn) do campo-de-nomes vs o campo de palavras-de-Chamada — assinaturas
  diferentes? Isso testa se os nomes são uma camada distinta (a "língua dos nomes") sobre o texto glosável.

## Bloco E — Frontend honesto (não confundir palavra com ruído)
- **E1** Controle de minlen ao vivo no square_reading + mostrar cobertura% e z por ajuste (o usuário vê a escala
  mudando o que aparece).
- **E2** Colorir os tokens em 3 classes, não 2: palavra-de-dicionário (glosa), raiz-de-nome (nome, intraduzível por
  natureza), run-de-ruído (cinza). Assim fica claro o que é palavra de verdade ali dentro.
- **E3** "Medidor de sentido" por quadrado: cobertura% e se bate o null, pra não achar que salada é frase.

## Ordem sugerida
1. **C** primeiro (teste real de sentido — se algum quadrado é uma Chamada em ordem, muda tudo).
2. **B** (fronteiras naturais — a leitura certa pode estar em outras fronteiras).
3. **D** (caracterizar o campo de nomes com a lente cabalística).
4. **E** (frontend reflete o modelo honesto: palavra vs nome vs ruído).

## Verificação
- Cada bloco grava results/2x_*.json e passa pelo seu null.
- Positivo em C só conta se bate surrogate com folga (z>=4) e aparece em leitura reta/coluna/diagonal (não só traço).
- Frontend confere no navegador (http.server 8860), sem quebrar.
