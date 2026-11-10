# Datasets: fields and how to load

Every file is plain UTF-8 JSON. Study data is under `data/` (English keys); the Enochian
source data the engine reads is under `engine/data/` (original keys, glossed here).

## data/ (study layer)

### loagaeth_tables.json
The Loagaeth itself.
```
{
  "meta": { source, description, leaf_count, encoding, provenance },
  "leaves": { "1a": ["row", ...], "1b": [...], "2a": [...], ... }   // '?' = null cell
}
```
Leaves `1a`/`1b` are word-spaced (spaces separate words); every other side is a dense
49x49 grid (2401 letters, no boundaries).
```python
import json
leaves = json.load(open("data/loagaeth_tables.json", encoding="utf-8"))["leaves"]
whole_table_2 = "".join(leaves["2a"]) + "".join(leaves["2b"])
```

### loagaeth_vocabulary.json
```
{ "types": int, "tokens": int,
  "vocabulary": [ { "word": "NOCHASTOR", "occurrences": 24, "leaves": 18, "in_leaf1": false }, ... ] }
```
`leaves` = number of distinct tables the word appears in. Note: words come from **our**
segmentation of the dense tables, not from explicit boundaries in the manuscript.

### loagaeth_segmentation.json
The segmentation model and its quality.
```
{ "evaluation": { precision/recall-style fields },
  "test_leaves": [...], "train_words": [...], "leaf1": [...] }
```

### loagaeth_crossing.json
Recurrent word types vs the Call lexicon, with a null.
```
{ "types_3plus": int, "match_lexicon": [...],
  "pseudowords_mean": float, "pseudowords_max": int, "words": [...] }
```

### call_lexicon.json
```
{ "meta": {...},
  "known_glosses": { "IAD": "the god", "GAH": "the spirits", ... },
  "attested_wordforms": [ "...", ... ] }     // ~892 attested Angelical forms
```

### hive_graph.json
The name-network as data: node degrees (`deg`), edges, and per-table membership (`tabs`).

## engine/data/ (Enochian sources read by the engine)

These keep their original field names; the engine's loaders (`enoch.py`, `fontes.py`)
read specific keys. Glosses:

| file | key (original) | meaning |
|---|---|---|
| `quadrados.json` | `row`, `col`, `letter` | Great-Table square position + letter (GD arrangement) |
| `governadores.json` | `nome`, `servos`, coords | governor name, servant count, Earth coordinates |
| `chamadas.json` | `chamadas[].enoquiano`, `palavras` | Call text and word list |
| `numeros_nas_chamadas.json` | cardinal -> value | numeric words Dee gives in the Calls |
| `heptarquia.json` | `nomes_derivados_das_tabelas[].tabula_collecta` | Heptarchia Tabula Collecta names |
| `sigillum.json` | `tabela_7x7.celulas[][].letra` | Sigillum Dei Aemeth 7x7 letters |
| `gematria_enoquiana.json` | `c_sistemas_de_valores[].valores` | per-letter value tables (13 systems) |
| `tabuas_dee1584.json` | `grades_de_referencia.ditado_cotton_1584.grades` | 1584 Watchtowers |

Load any of them directly, or through the engine helpers:
```python
import sys; sys.path.insert(0, "engine")
import fontes, enoch
fontes.governors()["governadores"][0]        # first governor record
enoch.derive_names()[:5]                      # hierarchy names derived by rule
enoch.GRID["ar"]                              # the Air Watchtower as a 13x12 grid
```

## Helpers (`src/load.py`)

```python
import sys; sys.path.insert(0, "src")
import load
load.table_numbers()      # [1..49]
load.table_text(1)        # dense letter stream of table 1 (both sides)
load.dense_stream()       # the whole book as one stream
load.spaced_words(3)      # word tokens (>=3 letters) from leaves 1a/1b
load.ngrams(s, 6)         # 6-gram iterator
load.lexicon()            # the Call lexicon bundle
```
