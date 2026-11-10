# Loagaeth Analysis

A reproducible, dependency-free statistical analysis of John Dee's *Liber Loagaeth*
(the 49 tables of the Angelical / Enochian system, British Library Sloane MS 3189).

It treats the tables as data and asks one question with discipline: **which apparent
patterns survive a proper null model, and which are artifacts of the text's own
texture?** Everything here runs on the Python standard library alone. Fixed random
seeds, so every number below is reproducible by running the code.

> **Honest framing.** This does not decipher the Loagaeth. It maps its structure,
> shows what looks like real word-formation, and rules out a stack of popular
> "keys." The meaning is still sealed and probably opens only from an external
> anchor (the attested sense of a single Loagaeth name). Negative results are
> shipped as first-class findings (see module 08).

## Quick start

```bash
python src/run_all.py
```

No install step. Requires Python 3.8+. Outputs land in `results/` as JSON, plus a
combined `results/summary.json`. Each module also runs standalone, e.g.
`python src/a04_morphology.py`.

## Layout

```
data/
  loagaeth_tables.json   49 tables, Sloane MS 3189. Leaves 1a/1b are word-spaced;
                         the rest are dense 49x49 grids. '?' = null cell.
  call_lexicon.json      attested Angelical vocabulary from the 48 Calls, with the
                         handful of known glosses, used only for the bridge test.
src/
  load.py                shared loader + helpers (letters, tables, n-grams, nulls)
  a01_basic_stats.py     entropy, index of coincidence, type/token, Zipf
  a02_network.py         name-network: hubs, degree distribution, power-law alpha
  a03_master_name.py     CHASTOR / NOCHASTOR / CHUSTOR coverage across tables
  a04_morphology.py      affix paradigm on a small set of stems (the strongest find)
  a05_signature_names.py per-table distinctive names
  a06_call_bridge.py     whole-word matches between leaf-1 and the Calls
  a07_null_models.py     shuffle + order-k Markov surrogate generators
  a08_refutations.py     patterns that FAILED the strong null (reversal, Semitic root)
  run_all.py             runs everything, writes results/summary.json
results/                 generated JSON outputs
METHODOLOGY.md           how the null models work and why Markov is the real bar
```

## What the code finds (reproduced numbers)

All figures below are emitted by `run_all.py` on the bundled data.

### Structure
- **195,548 letters.** Unigram entropy **4.03 bits/letter**; conditional (bigram)
  entropy drops to **3.44 bits** — strong local predictability (syllable structure).
- **Index of coincidence 0.079**, about twice the uniform reference (0.038): the
  letter distribution is far from random.
- **Type/token ratio 0.81** over the word-spaced leaves: lots of distinct forms,
  consistent with a list of names rather than repetitive prose.

### It's a name-network ("hive")
- 6-grams recurring 5+ times form a graph of **4,291 nodes / 13,779 edges**.
- The degree distribution is heavy-tailed: mean degree 6.4, a few dominant hubs.
  Hill power-law exponent **alpha ~1.4 on this 6-gram adjacency graph** (the exact
  value is construction-dependent; the point is the heavy tail, not a magic number).

### The master stem CHASTOR
- **CHASTOR: 184 occurrences across 35 of 48 tables (72.9%).**
- **NOCHASTOR: 61 across 27 tables (56.2%).**
- **CHUSTOR** (A→U vowel variant): 19 across 8 tables. Of the 13 tables with no
  CHASTOR, CHUSTOR appears in **4** of them (a partial, not total, filler — stated
  precisely here because the raw counts matter).

### Productive morphology (the strongest result)
The CHAST stem takes a small, repeating prefix inventory:
`NO- (77), NE- (24), ZI- (18), NA- (12), OL- (11)`, yielding a clear paradigm:

```
NOCHASTOR 61   NOCHASTORA 37   NECHASTOR 19   ZICHASTOR 13
NOCHASTORAD 11 NACHASTOR 9     PLICHASTOR 5   PRICHASTOR 4
```

The same affix set recurs on other stems (-GETH, -DAX families, AD- compounds).
This is concatenative word-formation on a closed root set — the most language-like
behavior in the manuscript.

### Per-table signature names
Every one of the 48 tables has a distinctive name of its own (table 1 HZEMBL,
table 2 DAHOXI, table 3 DOMNAG, ...). **0 of 48** belong to the CHASTOR family. One
shared master stem + a unique local name per table.

### Bridge to the Calls
Of 2,619 word-spaced tokens, **23 exactly match** attested Angelical word-forms
(0.88%, vs a chance null of ~2.5). Four carry known meanings: **IAD** (god),
**GAH** (spirits), **ORS** (darkness), **URAN** (elders). Small but real.

## What FAILED (module 08 — read this one)

- **Mirror / reversal.** Observed 6-gram↔reverse co-occurrences: 102. Against a
  letter-shuffle null (3.3) it looks huge; against the **Markov-3 null (92.8,
  z≈0.95) it is dead.** It's a syllable-pool artifact, not intentional reversal.
- **Semitic triliteral roots.** Words-per-consonant-skeleton ratio is **1.38**,
  English-like, nowhere near the >2 that root-and-pattern languages produce. The
  morphology in module 04 is concatenative (prefix/suffix), not Semitic.

Other ideas tested and discarded in the broader project (not all re-run here):
Call-vocabulary as a decode key, Gebofal reordering, several geometric models
(pentagonal solid, honeycomb, tesseract, "CHASTOR cube"), and divine-name ciphers
(YHVH/MAD). None beat their null.

## How to help / extend

- Cross-check `data/loagaeth_tables.json` against a second transcription of Sloane
  3189. Transcription error could inflate or hide hubs.
- Work the **numeric layer** (the numbers Dee attached to the leaves). In the wider
  Enochian corpus the digits 2, 3, 6 dominate the 91 governors' numbers at
  p < 3e-4 with no known construction reason — the most promising unexplained thread.
- Supply an attested gloss for any single Loagaeth name (CHASTOR first). One real
  anchor lets the neighbors be tested as a key.

## Provenance & caveats

Word boundaries on the dense tables are the analysis's own segmentation, not Dee's;
treat the morphology as a strong hypothesis. The data is compiled from public-domain
facsimiles. See `METHODOLOGY.md` for the null-model details and `LICENSE`.
