# As folhas 26-28 lidas na diagonal — a costura do livro
# Folios 26-28 read on the diagonal — the book's seam

**#343.** As folhas 26-28 davam **0 nomes por linha** (#342). Lidas na **diagonal
descendente (↘)** elas acendem: **55 nomes distintos**, enquanto linha=1 e coluna=0 nas
mesmas faces. O eixo de leitura dessas faces **gira 45°**. É a "costura" do Loag.

---

## O teste (`src/a178`, faces 26a-28b 49×49)

| face | ROW | COL | **DIAG↘** | DIAG↗ |
|---|---|---|---|---|
| 26a | 0 | 0 | **25** | 2 |
| 26b | 0 | 0 | **10** | 11 |
| 27a | 1 | 0 | **13** | 16 |
| 27b | 0 | 0 | **32** | 0 |
| 28a | 0 | 0 | **20** | 0 |
| 28b | 0 | 0 | **23** | 0 |

Nomes distintos (26-28 juntas): **ROW 1 · COL 0 · DIAG↘ 55 · DIAG↗ 18.**
Linha e coluna servem de controle (mesmas letras, eixo errado → ~0). A diagonal↘ é o eixo.

Mais frequentes no ↘: `geth×72, nocha×41, aclax×25, algeth×18, chastor×15, anzach×12,
adnocha×11, chadax×9, nochap×8, chastora×7, axalgra×5, nochastor×4`.

---

## As diagonais principais, legíveis

```
26a ↘  …tachad·NOCHASTORAL·ged·no·dant        → família CHASTOR (NOCHASTORAL, NOCHASTOR)
26b ↘  AN·GETH·adox·aclansa·gu…·zidnoprax      → GETH, NACLANSA, ZIDNOPHA
28a ↘  viot·ALGETH·ax…·aneron·ANTANTOX·antax   → GETH, ANTANTOX
28b ↘  vor·GETH·az…·zad·no·ateron·RONZIN       → GETH, RONZIN
```

---

## Leitura honesta

- **O eixo roda nas faces 26-28.** Row=1, Col=0, Diag↘=55 na mesma pilha de letras: a
  leitura correta dessas faces é a **diagonal descendente**, não a linha. Confirma e
  quantifica o antigo achado "leitura diagonal 25b-28b" e a geometria #341.
- **O que a diagonal diz:** as mesmas dinastias do resto do livro — **CHASTOR / NOCHA /
  GETH / ANTANTOX / RONZIN** — correm aqui na diagonal. A folha 26a chega a soletrar a
  cadeia `NOCHASTORAL` inteira na diagonal principal. Não é conteúdo novo de linguagem; é
  o **mesmo campo de nomes girado 45°**.
- **Por que "costura":** no mapa (#342) as 26-28 são a dobra entre a metade densa (2-25) e
  o profundo (29-48); o giro do eixo marca essa junta.
- **Honesto:** sem null novo aqui — o próprio ROW=1 nas mesmas faces é o controle, e a
  diagonal↘ já passou null global em #341 (z=+12). A ascendente (↗, 18) é um eco fraco.

Dados: `results/178_diag2628.json`.
