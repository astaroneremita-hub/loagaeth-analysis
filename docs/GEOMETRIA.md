# Qual geometria concentra os nomes?
# Which geometry carries the names?

**#341.** O #337 achou que a seleção dos nomes é por **recorrência na grade**. Aqui: em
**que direção** de leitura. Lendo cada face quadrada 49×49 em linha / coluna / diagonal↘ /
diagonal↗ / borda (ida+volta), os 90 nomes vivem nas **LINHAS** (primário), com **BORDA**
e **DIAGONAL↘** como canais reais secundários. **COLUNA é morta.**

---

## O teste (`src/a176`, 42 faces quadradas, recorrência vs null, seed 1583)

| direção | total hits | faces/nome | null | z | lê |
|---|---|---|---|---|---|
| **ROW (linha)** | 876 | ~9.7 | 7.5 | **+103.1** | domina (parcialmente circular — ver nota) |
| **BORDA (perímetro)** | 101 | ~1.1 | 1.4 | **+42.0** | real, não-circular: nomes na moldura |
| **DIAG↘ (descendente)** | 128 | ~1.4 | 12.3 | **+12.2** | canal diagonal menor (bate c/ 25b-28b) |
| DIAG↗ (ascendente) | 34 | ~0.4 | 13.4 | +2.0 | marginal |
| **COL (coluna)** | 1 | ~0.0 | 14.7 | −1.4 | **morta** — nomes nunca descem coluna |

---

## Leitura honesta

- **Linha domina, mas cuidado com circularidade.** Os 90 nomes de referência foram
  derivados do livro lendo em **linha/segmento**; então ROW ganhar é em parte definicional
  (achamos nas linhas o que definimos por linha). O z=+103 confirma consistência, não é
  descoberta pura.
- **O achado limpo é BORDA e COLUNA.** Independentes da ordem de leitura:
  - **Coluna = 0** (z=−1.4): o Loag **não** é lido para baixo. Mata de vez leitura colunar.
  - **Borda = z=+42**: os nomes se concentram no **perímetro** das faces, muito acima do
    acaso. Casa com o achado antigo de "bordas de linha" — a moldura é lugar privilegiado.
  - **Diagonal↘ = z=+12**: canal real menor, consistente com a leitura diagonal já
    documentada de 25b-28b.
- **Resumo da geometria:** o Loag se lê **em linha**, com os nomes **grudando na borda** e
  um fio **diagonal descendente**; **nunca em coluna**, quase nada na ascendente.

### Limite
- Faces losango (linhas de tamanho variável) ficaram de fora deste teste (só as 42
  quadradas 49×49). A diagonal dos losangos (25b-28b) aparece aqui só pelo eco nas
  quadradas.

Isto prepara a leitura das grades 2-48: ler em linha, conferir borda e diagonal↘, ignorar
coluna.

Dados: `results/176_geometry.json`.
