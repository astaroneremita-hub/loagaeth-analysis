# Loagaeth Analysis

A reproducible, dependency-free toolkit for studying John Dee's Enochian / Angelical
system as **data** - above all the *Liber Loagaeth* (the 49 tables of letters,
British Library Sloane MS 3189), plus the Great Table, the 91 governors, the 19 Calls,
the Heptarchia and the Sigillum.

It has one discipline and one promise. The discipline: **no apparent pattern counts as
a finding until it beats a null model** that preserves the text's own texture, so we
report what fails as loudly as what survives. The promise: everything runs on the
Python standard library alone, with fixed seeds, so every number in these docs is one
command away from being reproduced or refuted.

> This does **not** decipher the Loagaeth. It maps the structure, shows what looks like
> real word-formation, rules out a stack of popular "keys," and ships the recursive
> engine we used to tell structure from coincidence. The meaning is still sealed and
> probably opens only from an external anchor (the attested sense of one name).

---

## What you need

- Python 3.8+ . Nothing else. No pip install for the core.
- Optional: an LLM backend (an Anthropic API key, **or** a local Ollama) only if you
  want the engine to propose new hypotheses on its own - see [Self-improving loop](#self-improving-loop).

## What you get when you run it

Two layers you can run independently:

**A. The Loagaeth analysis** (`src/`) - characterizes the 49 tables and prints:
the entropy/structure profile, the scale-free name-network and its hubs, the master
stem **CHASTOR** and its coverage, the **productive morphology** (a stem + a closed set
of prefixes/suffixes), the per-table signature names, the bridge to the Calls, and the
**refutation tests** (what died against the strong null).

**B. The recursive pattern engine** (`engine/`) - the self-feeding loop that sweeps 12
probes (gematria, geometry, symmetry, numerology, kabbalah, frequency, skip-ciphers...)
across the whole Enochian corpus, each probe with its own null model, dedupes against a
persistent memory, writes only what is new, and labels every finding `candidate` vs
`known` (circular/by-construction) with a p-value verdict.

```bash
# A - the Loagaeth analysis (writes results/*.json)
python src/run_all.py

# B - the recursive engine, one full sweep (writes engine/results/*)
cd engine && python loop.py --rodadas 13
```

---

## How to load the data yourself

Every dataset is plain JSON under `data/` (study data) and `engine/data/` (the Enochian
sources the engine reads). Load any of them directly:

```python
import json

# the Loagaeth itself: {"meta": {...}, "leaves": {"1a": [rows...], "1b": [...], "2a": [...]}}
loa = json.load(open("data/loagaeth_tables.json", encoding="utf-8"))
leaves = loa["leaves"]
dense_1a = "".join(leaves["2a"])          # a dense 49x49 table as one letter stream

# the derived word list (segmented): [{"word","occurrences","leaves","in_leaf1"}, ...]
vocab = json.load(open("data/loagaeth_vocabulary.json", encoding="utf-8"))["vocabulary"]
```

Or use the shared helpers in `src/load.py`, which handle letters, tables, n-grams and
null models for you:

```python
import sys; sys.path.insert(0, "src")
import load
load.table_text(1)         # all letters of table 1 (both sides)
load.dense_stream()        # the whole book as one stream
load.spaced_words()        # word tokens from the two word-spaced leaves (1a, 1b)
```

See [`docs/DATA.md`](docs/DATA.md) for every file, its fields, and what it contains, and
[`docs/SOURCES.md`](docs/SOURCES.md) for where each dataset comes from (the Loagaeth
transcription, the Great Table, the governors, the gematria systems).

---

## Layout

```
data/                         study data (impersonal, English keys)
  loagaeth_tables.json        the 49 tables (Sloane MS 3189). '?' = null cell
  loagaeth_vocabulary.json    segmented word list with per-leaf counts
  loagaeth_segmentation.json  the segmentation model + its precision/recall
  loagaeth_crossing.json      cross-check of recurrent words vs the Call lexicon
  call_lexicon.json           attested Angelical vocabulary (for the bridge test)
  hive_graph.json             the name-network (nodes/edges) as data
src/                          LAYER A - the Loagaeth analysis
  load.py                     shared loader + helpers (letters, tables, n-grams, nulls)
  a01..a06_*.py               the six analyses
  a07_null_models.py          shuffle + order-k Markov surrogate generators
  a08_refutations.py          the patterns that FAILED the strong null
  a09_letter_grammar.py       letter positional roles (z~331) + same tongue as the Calls
  a10_territory.py            per-table territory map of the master names
  a11_lineages.py             CHAST vs GETH: morphology, territory, co-location, syntax
  a12_empire.py               the "seven Lords", title-nesting, vowel twins, CHA-core test
  a13_numbers.py              governors' numbers: head digit + 2-3-6 block, midpoint regime change
  a14_anzach.py               ANZACH profiled and compared with CHASTOR
  a15_book_geometry.py        full grids vs chessboard diamonds, text direction, noise tables
  make_figures.py             draws every figure in figures/ from the results
figures/                      all figures as SVG (regenerated by run_all.py)
  run_all.py                  runs everything -> results/summary.json
engine/                       LAYER B - the recursive pattern engine
  enoch.py  fontes.py         Great-Table derivation + Dee's primary sources
  nucleo.py                   data, gematria, statistics, persistent memory
  sondas.py                   the 12 probes, each with its own null model
  loop.py                     the self-feeding runner
  llm_agent.py                optional: an LLM proposes new hypotheses (API key or Ollama)
  data/                       the Enochian source JSON the engine reads
  README.md                   how the engine works, probe by probe
docs/
  SOURCES.md                  provenance of every dataset (the "where did this come from")
  DATA.md                     every dataset's fields + how to load it
  EXPLORED.md                 everything we tried: what held up, what we threw out
  EXPERIMENTS_72_hypotheses.md the full 72-hypothesis audit across the whole system
  METHODOLOGY.md              the null models and why Markov is the real bar
```

---

## Everything we discovered

Run `src/run_all.py` for the live numbers. Every claim below beat a null model or is true
by direct inspection; the module that reproduces it is named in brackets. The full write-up
with method is in [`docs/SESSION_FINDINGS.md`](docs/SESSION_FINDINGS.md); what we ruled out
is in [`docs/EXPLORED.md`](docs/EXPLORED.md).

**The one-line picture:** the Loagaeth is not a cipher to translate — it is the **name-book
of the Angelical language**. It is written in the *same tongue* as the 48 Calls, but its
content is that language's **names**, with a real grammar and a political geography, and
with the meanings of the proper names still sealed.

### Structure
- **It is a catalog of names, not prose** `[a01,a03]` — 195,548 letters; entropy 4.03 bits,
  conditional 3.44 (strong syllable structure); type/token 0.81; no prose-like grammar.
- **A scale-free name-network** `[a02]` — ~4,300 recurring-string nodes, a heavy tail of a
  few dominant hubs (the "hive").

### The master stem CHASTOR
- **CHASTOR rules the book** `[a03]` — 184 occurrences across 35 of 48 tables (72.9%); with
  NOCHASTOR, 61 more across 27. **CHUSTOR** is its A→U vowel twin.
- **Productive morphology** `[a04]` — CHASTOR takes a closed prefix set (NO- 77, NE- 24,
  ZI- 18, NA- 12, OL- 11): NOCHASTOR, NECHASTOR, ZICHASTOR, NOCHASTORAD… The **family
  forest**: three roots take ≥3 prefixes — CHASTOR (8), DAX (4), CHADAX (3). CHASTOR is the
  trunk.

### The alphabet is a real grammar

![Letter positional roles](figures/fig_letter_grammar.svg)

- **Letters carry positional roles** `[a09]` — mutual information MI(letter; position) =
  0.181 bits vs a within-word-shuffle null of 0.003, **z ≈ 331**. **G, V are onsets; H is a
  terminator.** Names parse as `[onset][root][terminator]` (ZURAH = ZU·RA·H, NOGAH = NO·GA·H).
- **Same Angelical tongue as the Calls** `[a09]` — the per-letter word-ending profile
  correlates **Loagaeth↔Calls r = 0.71** vs Loagaeth↔English r = 0.22 (control). Same
  sound-grammar, different lexicon. The Loagaeth is the *more alien / older* layer.

### A political geography of names

![Territory of the master names](figures/fig_territory.svg)

![Three great stems across the tables](figures/fig_stems_across_tables.svg)

- **Territorial map** `[a10]`, dataset `data/loagaeth_territories.json` — the book is
  partitioned. **CHASTOR** rules the heartland (tables 6–25) and a second realm (29–43);
  **CHUSTOR** rules the end (44–48); the opening (2–5) holds small independent realms;
  table 1 is the prophecy (and the *last* leaf in reading order). The zonation is real:
  per-table CHASTOR counts have lag-1 autocorrelation 0.51 vs a shuffle null of 0.20.
- **Refined honestly** — only CHASTOR is a true dynasty; CHUSTOR is a lone twin (no
  prefix-family); the opening realms share no large family. One empire + a twin + small realms.
- **Per-table signature names** `[a05]` — all 48 tables have a distinct local name; none are
  CHASTOR-family.

### The readable layer, and the sealed one
- **A small real bridge to the Calls** `[a06]` — ~20 whole words in the prophetic leaf 1 are
  attested Angelical with known meanings: MAD (of god), IAD (the god), GAH (spirits), ORS
  (with darkness), ZIR (I am), GOHO (sayeth), VORS ("now the seas appear", recurs 47×). These
  are the shared sacred **particles**.
- **The proper names are sealed** — an exhaustive lexicon search finds **zero** glosses for
  CHASTOR or its family. The master names have no attested meaning in any source we hold.

### The one unexplained number

![Digits in the governors' numbers](figures/fig_governor_digits.svg)

- **The 2/3/6 anomaly** — the numbers Dee attached to the 91 governors are dominated by the
  digits 2 (71×), 3 (75×), 6 (69×): 59% of all digits vs a chance ≈ 30%, **z = 11.4**. 62 of
  91 numbers contain a 6. Its architecture is now partly decoded (head digit + permuted 2·3·6
  block, head shared per Aethyr in the second half) — see the section on the governors'
  numbers below; the exact choice of each head and permutation is still open.

### The empire, examined closely

![Title nesting in the name-empire](figures/fig_empire_nesting.svg)

![The CHASTOR hive](figures/fig_chastor_hive.svg)

- **The queen is a stem, carried inside her titled forms** `[a12]` — a few stem-names plus a
  shared, stackable title-chain: CHASTOR 184 ⊃ NOCHASTOR 61 ⊃ ADNOCHASTOR 10; CHAPH 100 ⊃
  NOCHAPH 47 ⊃ ADNOCHAPH 20; ANZACH 153 ⊃ NOCHANZACH 11 ⊃ ADNOCHANZACH 5. Each added title
  cuts frequency about threefold — rank-like compounding. ANZACH is a second great stem.
- **The "seven Lords"** listed elsewhere in the project (CHASTOR, HANZACH, ALGETHA, ADNOCHA,
  ADNACHA, ACHEPHA, ANTANTO) are real frequent strings, but they overlap and nest inside this
  compounding system rather than being seven independent beings.
- **CHAST vs GETH** `[a11]` — CHAST is a head-stem (fixed -OR ending, variable prefixes); GETH is
  the most pervasive element (504×, 43 tables) and ends in the terminator H. They are not rivals
  (territory correlation exactly at the frequency null) and form no phrase together.
- **Shorter is stronger; numbers don't encode power** — name length vs frequency ρ = −0.39;
  gematria vs frequency ρ = +0.11.
- **Provenance warning** — the sefira/planet/talisman "powers" attached to these names in the
  wider project's grimoire are convention (its own generator says "constructed, not
  deciphered"); one name even received two incompatible assignments.
- **Literature check** — none of these names appear in the 81 reference books held by the project.

### The governors' numbers — decoded architecture

![Head digit per Aethyr](figures/fig_head_digit_regime.svg)

- **Number = [head digit] + [a permuted 2·3·6 block, sometimes zero-padded]** `[a13]` — e.g.
  7|632, 9|236, 5|362, 2|360. Against a null that shuffles every digit (so the 2/3/6 excess is
  already priced in): the block co-occurs in one number z = 7.6, is contiguous z = 9.0, sits at
  the end z = 8.3; exact duplicates z = 8.5; anagram pairs 92 vs 20.6, z = 13.7.
- **The head digit belongs to the Aethyr — only in the second half.** Aethyrs 1–14: no rule
  (z = −1.4). Aethyrs 15–30: governors share their first digit (z = 8.2); seven Aethyrs have all
  three identical. The construction changes regime at the midpoint of the 30.
- Head digit is unrelated to part, tribe or name. A search over 30 candidate rules (Aethyr-name
  gematria in all 13 systems, index transforms, sums), with a null that re-runs the whole search
  on shuffled heads, finds nothing (best 4/16 vs 4.3 by chance, p = 0.83).
- **The block prefers its natural order**: "236" ascending in 13 of 30 numbers vs 5 expected if
  all six orders were equal (p = 0.0005).

### ANZACH, the sibling stem
- **153 occurrences, 39 tables** `[a14]` — wider than CHASTOR, and present in tables 2–5 where
  CHASTOR is absent. Built the same way: **NO·CHA·NZACH** parallels **NO·CHA·STOR**, with the
  same title nesting (ANZACH ⊃ HANZACH ⊃ NOCHANZACH ⊃ ADNOCHANZACH).
- It stands alone as a **word in the prophetic leaf 1**. No rivalry or precedence with CHASTOR
  (territory at the density null; each comes first 17 of 34 times).

### The book's physical geometry — four segments `[a15]`

![The book's formats](figures/fig_book_formats.svg)

- **Tables 2–28 are full 49×49 grids written in rows.**
- **Tables 29–48 are diamonds.** One side of each leaf has rows of 1, 3, 5 … 49 … 3, 1 letters
  (1201 cells), the other 2, 4 … 48, 48 … 4, 2 (1200 cells): 1201 + 1200 = 2401 = 49². These are
  exactly the **two colours of a chessboard** on a 49×49 grid, each written along the diagonals
  (the paper turned 45°). Both sides of a leaf together are **one** 49×49 table.
- **The language runs along those diagonals.** Rebuilding the square from the two diamonds and
  reading its rows or columns gives pure noise (recurring-name share 0.001, conditional entropy
  4.0 bits), while the diagonals as written carry the names (0.15, 3.24 bits). This is the
  geometric form of Peterson's remark that Kelley "skipped every other letter" and that the
  paper was reoriented.
- **Tables 26–28 are statistical noise** — full grids, but letters are independent of each other
  (conditional entropy equals a shuffled copy), no recurring names, and they break the rule below.
  They are the last three full tables before the format changes.
- **Tables 44–48** use an irregular diamond pairing and almost no recurring names — the end of
  the book is a distinct fourth segment.
- **Method note:** the diamond tables hold half the letters per side, so raw per-table counts
  (as in the territory map) are not comparable across the two formats. Normalised by length,
  CHASTOR's density is steady from table 6 to 43.

![Diamond geometry](figures/fig_diamond_geometry.svg)

### The no-doubled-letter rule

![No doubled letters](figures/fig_doubled_letters.svg)

- The Loagaeth almost never writes the same letter twice in a row: 0.76% in the full tables,
  0.43% in the diamonds, 0.61% in leaf 1, against 8.6% expected from its letter frequencies —
  **about 11× below chance**. The Calls avoid doubles more loosely (1.85%). Tables 26–28 sit at
  chance (9.6%), another sign they were produced differently.

### What we tested and threw out (the discipline)
Mirror/reversal (syllable-pool artifact), decimation-by-2 (names are contiguous), Semitic
roots (ratio ~1.3, English-like), prefix-as-region (matches a frequency null), the
CHASTOR-family numeric signature (spread, not 2/3/6), the prologue acrostic (gibberish),
Call-vocabulary-as-key, Gebofal reordering, four geometric models, divine-name ciphers, and —
from the engine's broader 72-hypothesis sweep — most gematria and the 3-6-9 / sefirotic
claims (they belong to the value system or grid geometry, not a hidden code). Watchtower-style
geometric name-extraction from the 49×49 grids also fails its null (`engine/extract_names.py`):
the names live in the linear reading, not a Great-Cross geometry.

### Where this leaves us
We have the **form** of the names — network, morphology, letter-grammar, territory — and the
fact that it is one language with the Calls. We do not have the **referents** of the proper
names. The only path to meaning is an **external anchor**: the attested sense of a single
name (CHASTOR first). Per Dee's own source the highest names were "not to be pronounced," so
this layer may be sealed by design. Honest bottom line: we have not deciphered the Loagaeth —
we have mapped its skeleton, proved it is a real name-language, and ruled out a stack of
popular keys, further than any published treatment we could find.

---

## Self-improving loop

The engine can keep searching on its own: an LLM reads the findings and proposes new
testable hypotheses, which you then code as probes - but the **null models stay the only
judge of truth**. Set one backend:

```bash
# cloud (Anthropic)
pip install anthropic
set ANTHROPIC_API_KEY=sk-...
cd engine && python llm_agent.py --watch --rounds 13 --every 3

# local (Ollama, no key, stdlib only)
set LLM_BACKEND=ollama
set OLLAMA_MODEL=qwen2.5:7b
cd engine && python llm_agent.py --n 5
```

Suggestions are appended to `engine/results/llm_suggestions.jsonl`. The LLM never
decides what is real; it only widens the search. See `engine/README.md`.

---

## How to simulate and test

- Change the data: drop in a second transcription of Sloane 3189 as
  `data/loagaeth_tables.json` and re-run - does CHASTOR survive the new source?
- Add a hypothesis: write a probe in `engine/sondas.py` returning a finding dict with its
  own null model (copy the shape of `s6`), add it to `SONDAS` and the loop's `plano`.
- Break a claim: every result ships its null; if you think a finding is an artifact,
  harden its surrogate in `src/a07_null_models.py` and show it falls. That is exactly how
  we killed the reversal idea (see `docs/METHODOLOGY.md`).

## Provenance & honesty

Word boundaries on the dense tables are our own segmentation, not Dee's - treat the
morphology as a strong hypothesis. The Loagaeth text is transcribed from a public-domain
facsimile of Sloane MS 3189; the Great-Table and gematria layers come from the Golden
Dawn line and Dee's diaries. Nothing here is personal data. Full provenance in
[`docs/SOURCES.md`](docs/SOURCES.md). License: MIT (code and compiled data; the historical
sources are public domain).
