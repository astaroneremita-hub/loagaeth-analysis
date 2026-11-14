# The Complete Enochian Dictionary (Laycock) — o que dá pra usar
# What is usable from Laycock's dictionary

> ⚠️ **CORREÇÃO (#339).** O número "114 palavras / z=+42.8" abaixo estava **inflado por
> auto-citação**: a Introdução do Laycock **transcreve linhas da folha 1** (fólios I.13,
> 1.24, L25, 1.26, II.24…) e há uma 2ª citação (27ª Invocação), além de inglês das glosas.
> Removendo as citações + inglês, a folha 1 len≥6 cai de 43 → 24 e o ganho real some.
> **Léxico confiável = 21 (Chamadas) + 3 que Dee glosou (margem) ≈ 24, não 114.**
> Ver `docs/GLOSSARIO.md` e #339. O resto desta página fica como registro do erro.

**#338.** O livro é o **dicionário A–Z da língua enoquiana** (145 págs): léxico das
Chamadas + nomes de Aethyrs/governadores/seniores + gramática. **Não** traz as tabelas do
Loagaeth, **não** decodifica o Liber Soyga (só o cita: "Book of Soyga = _aldaraia_, um dos
livros sagrados de Dee"), e **não** tem a gematria neste extrato.

O que ele faz por nós: **valida e cresce a camada de léxico real do Loag**, e **confirma,
por fonte independente, que o campo de nomes do Loag não é enoquiano** (reforça #336).

---

## Achados (`src/a174`, folha 1 × léxico Laycock, null pareado, seed 1583)

| conjunto | atestado no dicionário | null | z |
|---|---|---|---|
| folha1 palavras len≥4 | **114** / 2342 | 7 | **+42.8** |
| folha1 len≥5 | 73 / 1948 | 1 | +70.8 |
| folha1 len≥6 | **44** / 1361 | 0.1 | **+153.8** |
| partículas ≤3 | 111 / 175 | 51 | +11.4 |
| **raízes do gerador** (chastor, nocha, geth…) | **0 / 10** | — | — |
| **nomes mestre** (nochastor, anzach…) | **0 / 90** | — | — |
| controle: as 21 glosadas já conhecidas | 15/15 presentes | — | — |

Palavras longas da folha 1 atestadas (amostra len≥5): `zimah zonze zambuges laphet danfa
arphe duxma gohed cruscanse ampri chramsa peleh pamphicas gascampho umascala umphagam
zemah zumacah`…

---

## Leitura honesta

- **A camada de léxico real é bem maior que os 21 das Chamadas.** ~**114 palavras** da
  folha 1 (len≥4) são palavras enoquianas atestadas em Laycock — 5× o que tínhamos. Dá pra
  traduzir muito mais da página. Usável de verdade.
- **O campo de nomes NÃO é enoquiano.** Zero das 10 raízes e zero dos 90 nomes do gerador
  estão no dicionário completo da língua, enquanto 15/15 das palavras-função estão. Fonte
  independente batendo no mesmo veredito do #336: léxico = enoquiano real; nomes = sistema
  próprio, autônomo.
- **Confound honesto:** o pool do dicionário mistura o inglês das glosas, então um ou outro
  hit curto pode ser palavra inglesa coincidente (ex. `notes`). Por isso o número forte é
  **len≥6 = 44, null 0.1** (string enoquiana de 6+ letras coincidir com inglês é
  desprezível). Um wordlist só-enoquiano apertaria o 114; o sinal não depende disso.

## O que NÃO dá pra usar
- **Loagaeth estrutural:** nada. Laycock trata `loagaeth/logah` só como verbete ("fala/
  livro"); não há tabelas nem leitura das grades.
- **Liber Soyga:** não decodifica. Só nomeia (Soyga = aldaraia). Soyga é outro sistema
  (tabelas 36×36 + Aldaraia) — projeto à parte se você quiser.
- **Gematria:** 0 neste PDF (fica noutra parte da obra). Já temos `gematria_enoquiana.json`.

**Próximo usável:** montar o glossário expandido folha 1 ∩ Laycock (as 114) com os
significados, pra reler a página com muito mais palavra traduzida.

Dados: `results/174_laycock_lexicon.json`. (O texto do dicionário não é guardado no repo —
copyright; `src/a174` lê o PDF que você baixou.)
