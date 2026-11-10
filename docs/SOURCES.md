# Sources & provenance

Where every dataset comes from. All underlying texts are public-domain manuscripts of
John Dee and the derived tables of the later Golden Dawn tradition. Nothing here is
personal data. The "book" behind the Loagaeth is not a printed book but a 16th-century
manuscript; we ship the extracted JSON, not the facsimile images.

## The Loagaeth (primary object)

- **Manuscript:** John Dee, *Liber Mysteriorum Sextus et Sanctus* / *Liber Loagaeth*,
  British Library **Sloane MS 3189** (the holograph of the 49 tables).
- **Transcription used:** the public-domain transcription hosted at
  `http://www.esotericarchives.com/dee/sl3189.htm` (Joseph H. Peterson, Esoteric
  Archives), captured 2026-10-21.
- **Shipped as:** `data/loagaeth_tables.json` - 49 tables, each with up to two sides
  (`Na`/`Nb`). Leaves `1a`/`1b` are word-spaced; all other sides are dense 49x49 grids
  of 2401 letters. `?` = an illegible/null cell.
- **Caveat:** one transcription only. Hubs and counts should be re-checked against a
  second transcription; transcription error can inflate or hide a recurring name.
- **Markup and leaf titles:** module `a18` downloads the same page
  (`https://www.esotericarchives.com/dee/sl3189.htm`, revision of 12/12/2022) into
  `data/raw/` (git-ignored, not redistributed) and derives from it only: the leaf headings
  (`data/loagaeth_leaf_titles.json`), which chessboard colour each of Peterson's marks falls on in
  leaves 25b–28b, and the diagonal reading of those tables
  (`data/loagaeth_diagonal_decoded.json`).
- **Comparison only — the Book of Soyga:** *Aldaraia sive Soyga vocor*, edited and translated by
  Jane L. Kupin (2014, all rights reserved; from BL MS Sloane 8 and Bodleian MS Bodley 908). Module
  `a19` reads five columns of its *Tabula prima Aries* from a local copy
  (`data/raw/soyga_aries_columns.json`, git-ignored) to compare periodicity. Nothing from that
  edition is shipped in this repository.

- **Index Verborum:** Joseph H. Peterson, *Index Verborum of the "Angelic Language" from Liber
  Logaeth* (© 1986, all rights reserved), `https://www.esotericarchives.com/dee/angelix.htm`.
  Module `a21` downloads it into `data/raw/` (git-ignored, not redistributed) and writes only
  aggregate checks to `results/21_index_heptarchy_numbers.json` (verification counts, the line map,
  and the cut positions of the nine dense lines of leaf 1b used as a segmentation gold standard).

## Derived Loagaeth datasets (produced by this project)

- `data/loagaeth_vocabulary.json` - word list obtained by segmenting the dense tables;
  per-word occurrence and leaf counts. Segmentation is **ours**, not Dee's.
- `data/loagaeth_segmentation.json` - the segmentation model and its measured
  precision/recall on held-out leaves.
- `data/loagaeth_crossing.json` - cross-check of the recurrent word types against the
  Call lexicon, with a pseudo-word null baseline.
- `data/hive_graph.json` - the recurring-string adjacency network (the "hive").
- `data/call_lexicon.json` - attested Angelical vocabulary from the 48 Calls, with the
  few leaf-1 glosses used in the bridge test.

## The Great Table and the hierarchy (engine layer)

- `engine/data/quadrados.json` - the 4 Watchtowers / Great Table as 624 squares + the
  20 of the Table of Union, in the **Golden Dawn** arrangement (letters, faces, zones,
  attributions), compiled from Golden Dawn line works. This is what `enoch.py` derives
  the hierarchy names from (kings, seniors, kerubic archangels, lesser angels) by rule.
- `engine/data/tabuas_dee1584.json` - the Watchtowers in Dee's **original 1584**
  dictation order (Sloane 3191 / Cotton reference grids).
- `engine/data/tabuas_raphael1587.json` - the **1587** reformed/recension table.

## The other Enochian systems (engine layer)

- `engine/data/governadores.json` - the **91 governors / Parts of the Earth** from the
  *Liber Scientiae Auxilii et Victoriae Terrestris* (names, servant counts, coordinates).
- `engine/data/chamadas.json` - the **19 Calls / Keys** (Enochian text and word lists).
- `engine/data/numeros_nas_chamadas.json` - the numeric words (cardinals) Dee gives in
  the Calls.
- `engine/data/heptarquia.json` - the **Heptarchia Mystica** names and the Tabula
  Collecta.
- `engine/data/sigillum.json` - the **Sigillum Dei Aemeth** 7x7 letter table.
- `engine/data/gematria_enoquiana.json` - the **13 Enochian gematria value systems**
  (per-letter values with their evidence grade), collected from the Golden Dawn /
  Crowley line and later commentators.

## A note on keys and language

The study datasets under `data/` use English field names. The raw Enochian source JSON
under `engine/data/` keeps the original Portuguese/Latin field names it was compiled with
(e.g. `nome`, `servos`, `tabula_collecta`), because the engine's loaders read those keys
by name; `docs/DATA.md` glosses them in English. The data *values* (letters, names,
numbers) are language-neutral.

## Not included (and why)

- The facsimile images of Sloane 3189 - large and available at the Esoteric Archives
  link above.
- The private evidence corpus (a library of books the engine can optionally search to
  cross-check a confirmed finding). It is not redistributable; `engine/nucleo.py` runs
  fine without it (`Corpus` degrades to a no-op).
