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
- **Letters carry positional roles** `[a09]` — mutual information MI(letter; position) =
  0.181 bits vs a within-word-shuffle null of 0.003, **z ≈ 331**. **G, V are onsets; H is a
  terminator.** Names parse as `[onset][root][terminator]` (ZURAH = ZU·RA·H, NOGAH = NO·GA·H).
- **Same Angelical tongue as the Calls** `[a09]` — the per-letter word-ending profile
  correlates **Loagaeth↔Calls r = 0.71** vs Loagaeth↔English r = 0.22 (control). Same
  sound-grammar, different lexicon. The Loagaeth is the *more alien / older* layer.

### A political geography of names
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
- **The 2/3/6 anomaly** — the numbers Dee attached to the 91 governors are dominated by the
  digits 2 (71×), 3 (75×), 6 (69×): 59% of all digits vs a chance ≈ 30%, **z = 11.4**. 62 of
  91 numbers contain a 6. The single strongest pattern with no known construction rule — the
  open lead for a Reeds-style generative rule.

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
