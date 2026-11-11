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
  a16_letters.py              letter counts + gematria, hidden-name test, positions, segments, U register
  a17_kingdom.py              sides/heights, mirrors, the 7x7 plan, the two houses
  a18_markup_decoding.py      Peterson's marks, leaf titles, decoding tables 25b-28b (two currents)
  a19_machine.py              Soyga vs Loagaeth, 2-D rule, compression, language model, generator
  a20_energy_fibonacci_gd.py  letter energy by realm, Fibonacci, 7x7 division, GD rearrangement
  a21_index_heptarchy_numbers.py  Peterson's index checked, dense-line gold standard, Heptarchy numbers, gematria
  a22_robustness_and_depth.py     findings under other readings, diamond roads, memory, repeats, Zipf
  a23_name_discovery.py           unsupervised name discovery, families, grammar
  a24_book_architecture.py        acrostics, pyramid cross, dialects, book order, two currents, verses
  a25_bridges.py                  other systems inside the Loagaeth, name constellation
  a26_letter_names.py             Dee's letter names as a reading layer (construction), letter profiles per side
  make_figures.py             draws every figure in figures/ from the results
  make_viz_data.py            builds viz/loagaeth_viz_data.js for the 3D viewer
viz/                          loagaeth_3d.html - interactive three.js viewer
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
  SESSION_FINDINGS.md         every finding with its numbers and method
  RESEARCH_LOG.md             the process, question by question, each result tagged
```

---

## Everything we discovered

Run `src/run_all.py` for the live numbers. Every claim below beat a null model or is true
by direct inspection; the module that reproduces it is named in brackets. The full write-up
with method is in [`docs/SESSION_FINDINGS.md`](docs/SESSION_FINDINGS.md); what we ruled out
is in [`docs/EXPLORED.md`](docs/EXPLORED.md); the whole process, question by question, with each
result tagged REAL / REFUTED / INCONCLUSIVE / DESCRIPTIVE, is in
[`docs/RESEARCH_LOG.md`](docs/RESEARCH_LOG.md).

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

- **Tables 2–25a are full 49×49 grids written in rows.** From side 25b on, the text runs on
  diagonals — see the decoding of 25b–28b below.
- **Tables 29–48 are diamonds.** One side of each leaf has rows of 1, 3, 5 … 49 … 3, 1 letters
  (1201 cells), the other 2, 4 … 48, 48 … 4, 2 (1200 cells): 1201 + 1200 = 2401 = 49². These are
  exactly the **two colours of a chessboard** on a 49×49 grid, each written along the diagonals
  (the paper turned 45°). Both sides of a leaf together are **one** 49×49 table.
- **The language runs along those diagonals.** Rebuilding the square from the two diamonds and
  reading its rows or columns gives pure noise (recurring-name share 0.001, conditional entropy
  4.0 bits), while the diagonals as written carry the names (0.15, 3.24 bits). This is the
  geometric form of Peterson's remark that Kelley "skipped every other letter" and that the
  paper was reoriented.
- **Tables 25b–28b are squares written on the diagonals** (decoded below). Read by rows they look
  like noise — an earlier version of this analysis called them noise; that was a reading-direction
  error, corrected by module `a18`.
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
  **about 11× below chance**. The Calls avoid doubles more loosely (1.85%). Tables 26–28 read by
  rows sit at chance (9.6%) only because that is the wrong direction; read on their diagonals they
  drop to 1.5% (0.2–0.4% in the cleanest currents).

### Tables 25b–28b decoded: two currents on the diagonals `[a18]`

![The two currents](figures/fig_two_currents.svg)

- **Peterson's transcription marks every letter of leaves 25b–28b** with one of two signs (`~`, `/`,
  `` ` `` or a space). Aligned to the 49×49 grid (2,401 letters = 2,401 cells), **each sign falls on
  exactly one chessboard colour** — about 1,200 / 1,201 cells, the same two colours that tables
  29–48 write as separate diamonds.
- **Read colour by colour along the diagonals, these tables are ordinary Loagaeth.** One colour
  runs **down-right** (↘) on the main diagonals; the other runs **leftward** (↖ on the same
  diagonals, or ↙ on the anti-diagonals — one binary choice per face). Recurring-name share: rows
  0.001 → decoded **0.27** (best currents 0.37–0.40, as high as row-written tables); conditional
  entropy 3.82 → 3.05 bits. **Control:** 35 ordinary row-written tables read by exactly the same
  procedure reach at most **0.005**.
- Example decoded line (27b ↘): `YSCHINER·OXAD·LOZAD·ALZACH·CHANTOX·AGETH·CHADAX·TAPHERO` — familiar
  names. In the decoded text: CHASTOR 16×, ANZACH 12×, GETH 85×, NOCHA 51×, ADNOCHA 15×. **CHASTOR's
  realm is continuous from table 6 to 43**; the earlier "void" at 26–28 was a reading artefact.
- **The turn falls at the exact middle of the book:** sides 1a–25a are written in rows; from 25b
  the text runs on diagonals. In a 49-leaf (98-side) book, 25a is side 49 — 49 sides in rows, 49 on
  diagonals. (Descriptive, noticed after seeing the data.)
- The decoded text is published in `data/loagaeth_diagonal_decoded.json`.

### Leaf titles `[a18]`

- Each leaf carries a heading (e.g. 26b *Draxph intayfalg*, 27b *Vincal leorna rvh*, 28b *Larvh
  gohonp babbabor*); all are extracted to `data/loagaeth_leaf_titles.json`. The heading of **5b,
  *Zvchastors plohodmax argednon***, names **ZUCHASTOR(S)** — the master name in its U form — on the
  leaf just before CHASTOR's realm begins (table 6). Headings of 3b, 4a, 7a, 8a carry ALGE/ALGETH.
- Titles are **not** drawn from their own leaf: 15% of a title's 4-grams occur in its leaf vs 16%
  in other leaves.

### Every letter, mapped `[a16]`

![Every letter counted](figures/fig_letter_counts.svg)

- **A is 19% of the text**, twice the next letter (O 9.2%, N 9.0%, H 6.8%, L 6.3%, D 5.8%, R 5.5%…);
  Q, W, K are practically absent. The figure gives each letter's value in the Golden Dawn Enochian
  gematria for reference; the full set of values in all 13 systems is in `results/16_letters.json`.
- **The top letters spell no name.** For the top 3 to 8 letters (AON, AONH, AONHL…), no attested
  Call word or recurring Loagaeth word is an exact anagram (the chance of a hit for a random
  frequent set is shown alongside). English coincidences such as AONH → "NOAH" are exactly what
  this null is there to discount.
- **Letter values do not track frequency** in any gematria system after correction for 13 tests.

![Rows start and end on word boundaries](figures/fig_row_edges.svg)

- **Rows of the 49×49 grids follow word boundaries.** The first letter of a row is an onset far
  more often than mid-row (V 5.3×, P 3.0×, Z 2.4×, G 1.9×); the last is a terminator (S 3.4×,
  H 2.0×, O 1.7×, X 1.6×). This edge effect is the whole of the left/right difference: away from
  the three outer columns, left and right halves have the same letter mix.

![Letters by segment](figures/fig_letters_by_segment.svg)

- **Each realm has its own letter mix** — far beyond chance (χ² ≈ 11,100 vs ≤ 3,800 when tables
  are shuffled between segments). The opening favours S and M; the diagonal squares 26–28 T and X;
  the diamonds R and U.

### The U register `[a16]`

![The U register](figures/fig_u_register.svg)

- **The end of the book (44–48) speaks the heartland's names with A turned into U.** Its recurring
  5-grams overlap the heartland's 228 times as written, **387 times after A→U** — and every other
  vowel swap lowers the overlap (A→E 146, A→I 166, A→O 169). CHAST→CHUST, HASTO→HUSTO,
  RANCH→RUNCH, RAPHA→RUPHU, APHAR→UPHUR. In the end segment A falls to 6% and U rises to 10%.
- This revives, in a sharper form, an earlier A↔U idea that failed when tested across the wrong
  grouping of tables. Caveat: with a single transcription we cannot rule out a scribal habit in
  those leaves rather than a deliberate register.

### The kingdom: plan, houses, sides `[a17]`

![The 7x7 plan of the book](figures/fig_plan_7x7.svg)

- **On the 7×7 plan of the 49 tables**, table 25 is the exact centre (week 4, position 4), and the
  writing turns from rows to diagonals **between its two sides** (25a | 25b); the diamond format
  begins with **week 5** (table 29); the U-register end starts at 44. Descriptive: these positions
  were noticed after seeing the data and cannot carry a p-value.

![Two houses](figures/fig_two_houses.svg)

- **Two houses exclude each other table by table.** With overall name density removed, the NOCHA
  house (ADNOCHA, NOCHAPH, NODAX) and the GETH/ACLAX house (ALGETH, ACLAX) are anti-correlated,
  and it holds **inside** each realm, so it is not just "they live in different places":
  ADNOCHA × ACLAX r = −0.58 in the heartland (p = 0.004) and −0.66 in the diamonds (p = 0.007);
  NODAX × ALGETH −0.60 in the heartland (p = 0.001); NOCHAPH × ACLAX −0.73 in the diamonds
  (p = 0.002). The NOCHA house leads the first half; the GETH/ACLAX house holds or grows in the second.
- **Sides and heights:** against an exact baseline (a k-letter name can only start in the first
  49−k columns), **no great name prefers the left or the right**. **ALGETH sits in the lower half**
  of the full grids (29% in the upper half vs 49% expected, z = −3.1, passes correction for 14
  tests); GETH leans low and the NOCHA family leans high without passing it.
- **No mirror symmetry** ("as above, so below" taken literally): a diamond row is *less* like its
  mirror row than like a random row of the same length (0.029 vs 0.047), and in the full grids a
  row matches its mirror no more than any other row of the same table (0.071 vs 0.073).

### Machine or language? The Book of Soyga as a yardstick `[a19]`

![Machine or language](figures/fig_machine_vs_language.svg)

- Dee also owned *Aldaraia sive Soyga*, whose letter tables are **generated by an algorithm** (Jim
  Reeds). Its Aries table's columns are periodic (best self-match 0.97, 0.88, 0.84 at period 4).
  The Loagaeth is not (0.20, barely above shuffled 0.17). (Soyga columns were extracted locally from
  J. Kupin's 2014 edition for comparison only; they are not redistributed.)
- **No 2-D generation rule:** the letter above adds nothing to predicting a cell (H 3.95 → 3.94 bits);
  the letter to the left does (3.09). It is a 1-D language written line by line.
- **A language model reads it like a language.** Trained on tables 2–24 (4-fold held-out:
  3.01 bits/letter), it reads the diagonal-decoded tables at 3.44, the same tables by rows at 7.62
  (≈ shuffled 7.51), the end at 5.05 — and **4.25 once U is turned back into A**, an independent,
  machine-learning confirmation of the U register.
- **A machine can write Loagaeth-like text:** an order-5 model trained on the heartland produces
  lines such as `ARCHINADOXT·ANZACH·ADATHNOLZANTAGEM…` with the right doubled-letter rate. Simple
  local rules are enough to produce the surface of the language — consistent with a constructed or
  inspired tongue, not with a cipher.

### Is the end "denser"? Letter energy by realm `[a20]`

![Energy by realm](figures/fig_energy_by_realm.svg)

- Treating each letter's gematria value (13 systems) or its information content (surprisal) as an
  "energy", the end segment is **denser than the heartland in 10 of 14 measures** after correction.
  In the Golden Dawn table the mean value rises steadily: opening 38.8 → heartland 45.6 → diamonds
  60.0 → end 83.2.
- **But the rise is carried by the A→U shift** (U = 400, A = 1 in that table): with U turned back
  into A it vanishes in all but 3 measures. What survives is information: the end uses rarer letters
  (+0.17 bit per letter even without the U shift, p < 0.001). Gematria tables are later conventions;
  read this as a property of the letter mix, not as proof of power.

### Fibonacci, gradual division, Golden-Dawn rearrangement — all negative `[a20]`

- **Fibonacci:** gaps between successive CHASTORs are Fibonacci numbers 1.0% of the time vs 1.5% at
  random; CHASTOR starts on Fibonacci columns 17.7% vs 18.6% expected; segment borders are neither
  Fibonacci numbers nor at the golden section (30.3 of 49).
- **Gradual division:** 7×7 sub-blocks differ beyond chance only through the row-edge effect; the
  central row (the Watchtowers' "Great Cross" position) is not special (names 0.264 vs 0.280).
- **Golden Dawn style:** cutting each row-written table into four quadrants around the central
  cross and trying all 24 arrangements, **the original order wins in 35 of 35 tables** — the
  quadrants are not misplaced.
- **Pyramid arithmetic** (true by construction): each odd diamond is two stepped pyramids,
  1+3+…+49 = 625 = 25² above and 576 = 24² below (1201 = 25² + 24²); the even diamond holds
  2·24·25 = 1200.

### Peterson's Index Verborum, and a gold standard for dense text `[a21]`

![Index check](figures/fig_index_check.svg)

Joseph Peterson's *Index Verborum of the "Angelic Language" from Liber Logaeth* (1986, Esoteric
Archives `angelix.htm`) lists 2,779 word forms as `word t<side> line[*count]`. Checked against our
transcription:

- **It covers leaf 1 only.** `t1` = leaf 1a, `t2` = leaf 1b (98% / 96% of their words are found
  there, ≤ 11% on any other leaf). There is no `t3`. It is a **concordance, not a dictionary** — it
  carries no meanings, so it cannot unseal CHASTOR or any other name.
- **97.5% of its 3,589 references land on the stated line.** 2.0% are variant readings that differ
  by one or two letters — the classic confusions of Dee's hand (Z/X, U/B, N/U, R/X); 0.5% are not
  found.
- **The line map exposed a split line.** In leaf 1b, the index's line 20 is our rows 20 + 21 and
  every later line sits one row lower: the transcription breaks manuscript line 20 in two. Leaf 1b
  therefore has 49 lines, like 1a and like every table.
- **Only 164 of our 3,672 leaf-1 tokens are not indexed as such**, mostly one- to three-letter
  particles (A, NA, GEM, AX…).

![Dense division](figures/fig_dense_division.svg)

**Completing what was missing.** Leaf 1b ends with nine lines of 49 letters written without spaces.
The index still divides them into words — an editor's reading, but one our methods never saw. That
makes it a **gold standard for segmenting dense Loagaeth text**. A simple word model trained only on
the spaced lines of leaf 1 recovers Peterson's breaks with F1 **0.33**, against **0.16** for the same
number of random breaks (95th percentile 0.22, p < 0.0005). The model over-cuts (precision 0.25,
recall 0.49): the dense lines are made of longer words than the spaced ones. **REAL** — the dense
text carries word structure that agrees with an independent reader.

**Letter counts and the Heptarchy (7 kings, 7 princes, 42 ministers, 49 good angels).** Of the 21
letter counts, 3 are divisible by 7 (3.6 expected), 1 by 42 (0.6), 1 by 49 (0.5) — chance. The
total, 177,226, is a multiple of 7, which mostly follows from the book being built of 49 × 49
squares (2,401 = 7⁴ letters per table). The clear contrast is **B**: it opens every one of the 49
Heptarchic names (16% of their letters) but is 1.2% of the Loagaeth. **REFUTED** as numerology.

**The top letters as a string (AONHLDRC…).** Frequency order is a property of the count, not a text.
As contiguous strings: AON 66× (97 expected from letter pairs), AONH 1×, ONHL 1×, nothing of length
5+; DRC is strongly avoided (1 vs 56). No Watchtower name, Call word or index word contains AON.
**REFUTED.**

**Gematria of the counts.** The true counts are A 33,441, O 16,361, N 15,892, H 12,099 (digit roots
6, 8, 7, 3). The "6 and 5" in a pasted calculation came from mistyped numbers with an extra digit
(334,441, 166,361, 158,892). The Golden Dawn values of all 21 letters sum to **1,486** (the pasted
1,446 gave Q = 50 instead of 90), and that sum is the same in every order, so it says nothing about
frequency. "A = 6, B = 5" is real — it is Crowley's column (and two GD-derived columns) in our
bundled tables. Digit roots of large counts fall on each of 1–9 about 1/9 of the time.

### Are we looking wrong? Every core result under other readings `[a22]`

We were wrong once (tables 26–28 read by rows instead of diagonals). So the main results were
recomputed on altered versions of the book: Z = X, U = V, U read as A, only sides whose rows are
exactly 49 letters, and ten copies with 2% of letters swapped for their look-alikes in Dee's hand.

![Robustness](figures/fig_robustness.svg)

- **Holds everywhere:** the no-doubled-letter rule (0.08–0.22 of chance), the row edges (z ≈ 40),
  the different letter mix of the four segments (χ² far above its null in every version), and the
  names themselves (2% noise loses only ~5% of CHASTORs).
- **Weaker than we said:** the CHASTOR **territory**. Counted per table it is strong (lag-1 0.49,
  p < 0.001); measured per 1,000 letters it is moderate (0.26, z ≈ 2, p ≈ 0.02), and if U is read as
  A it fades (z 1.1), because CHUSTOR at the end merges into it. The realm is real but partly the
  boundary of the U register. **REVISED.**
- **Segmentation, calibrated:** tuned on Peterson's division of eight dense lines and scored on the
  ninth, our segmenter rises from F1 0.33 to **0.36** (random 0.16). It still over-cuts; results that
  rest on substring counts (most of ours) do not depend on it.
- **Table 49 is missing:** no test assumes 49 present tables; the 7×7 plan results use 48.

![Diamond roads](figures/fig_diamond_roads.svg)

**Another road through the diamonds?** Each diamond pair rebuilt as its square and read ten ways:
only the stored anti-diagonals read as language (3.71 bits, 9.9 names per 1,000 letters); rows,
columns, main diagonals, boustrophedon and spiral are all noise (≈ 7.8 bits, 0 names). Backwards the
same road keeps the information (6.1 bits for a forward model) but loses every name. **REAL — there
is exactly one way to read them.**

### Deeper mathematics `[a22]`

![Memory](figures/fig_mi_decay.svg)

- **Memory of the text (mutual information by distance).** From 4 to about 12 letters the Loagaeth
  remembers more than a 3-letter Markov model (d = 8: 0.012 vs 0.006 bits) — the span of its words
  and names. Beyond ~12 letters every bit of memory equals that of letters shuffled inside each side:
  it is the change of letter mix from side to side, not a long-range code. **REAL (short range) /
  REFUTED (long-range code).**
- **Copying between tables:** the longest string shared by two tables is 16 letters
  (ADNOCHANTANTOXAL), shorter than in a Markov surrogate (18). No block was copied; 12-letter
  formulas shared between tables are 358 vs 206 (the names). **REFUTED (copying).**
- **Compression:** LZMA 3.22 bits/letter vs 3.26 for the Markov-3 surrogate — almost nothing beyond
  local letter habits for an algorithm to exploit.
- **Zipf and Heaps on Dee's own word divisions (leaf 1):** slope −0.61, Heaps β 0.91, 85% hapax at
  the size of the Calls — the same profile as the Calls themselves (−0.69, 0.87, 85%). By its word
  statistics leaf 1 behaves like the Calls. **DESCRIPTIVE.**
- **Vertical structure in the squares:** letters above/below each other share 0.0085 bits vs 0.0079
  with rows shuffled (z 1.7): the squares are written row by row, not as a 2-D design.

### New names, found by the text itself `[a23]`

![New names](figures/fig_new_names.svg)

Without telling the program any name, we kept every string of 4–14 letters that recurs (≥ 6×, in
≥ 3 tables), is followed and preceded by varied letters (a word boundary on both sides — Harris's
criterion), and occurs far more than a Markov-3 model of the same book predicts (z ≥ 4.5, Bonferroni
over 3,562 candidates).

- **47 strings survive. The same procedure on a Markov-3 copy of the book finds 0.** **REAL.**
- **Positive control:** it rediscovers NOCHASTOR/ICHASTOR/NECHASTOR, NOCHA/ADNOCHAP, ACLAX, CHADAX
  by itself. It misses the most frequent ones (CHASTOR alone, GETH, ANZACH) because a 3-letter model
  fitted on this book already "knows" them — the test is conservative.
- **New recurring names outside the known families** (count, tables): **NACHO** 157×/31 (and NACHOA,
  NACHOAD, NACHOAL), **AXALGRA** 39/19, **GRADAX** 38/13, **PHANGE** 32/20, **ANTANTOX** 27/16,
  **VOXAR** 25/15, **TAXALGRA** 19/11 (z 9.3), **DRAGRA**, **RONZIN**, **ANCHANO**, **NADAB**,
  **CHARDAX**, **AXACHAR**, **ZIDNOPHA** (mostly in the diamonds), **PHADOL** (tables 2–47),
  **ONDANVAGE** (z 12.2, only tables 3–10), **UCHER** (tables 23–48, the U register).
- **NACHO is the vowel mirror of NOCHA** (N·A·CH·O / N·O·CH·A), both strong, both widespread.
- **Families:** 5 families of three or more members (0 in the surrogate) — NACHO·A·AD·AL;
  NOCHAP·H·ADNOCHAP·ADNOCHAPHA; ACLAXTO·ACLAXTOR·AXACLAXTO; ICHASTOR·ICHASTORA·ZICHASTOR;
  NECHASTOR·NOCHASTOR·NOCHASTORA. Each family is a **core with a few prefixes and suffixes**: written
  as a grammar it takes ~40% of the letters of the list (e.g. core NACHO + endings {–, A, AD, AL}).
- **Limits:** these names barely help segment Peterson's dense lines (F1 unchanged, 0.33), and only
  4% occur inside Dee's spaced words of leaf 1 (2% for random strings) — they belong to the tables'
  own vocabulary.

### The architecture of the book `[a24]`

![Two currents](figures/fig_currents_vocab.svg)

- **The two currents of 25b–28b have two vocabularies.** Their recurring 5-letter formulas overlap
  (Jaccard) 0.221, while every random split of the same lines gives 0.29–0.34 (mean 0.315). ANZACH
  (10 vs 2), ACLAX (25 vs 11) and OXAD (37 vs 14) lean to the ↘ current; NOCHAP (5 vs 13) and
  CHASTOR (6 vs 10) to the ← current. The interleaved currents are **two texts, not one cut in two** —
  echoing the two houses. **REAL (new).**

![Dialects](figures/fig_dialects.svg)

- **A dialect chain.** A letter model of each realm reads its neighbours best: opening → heartland →
  26–28 → diamonds → end. The end is closest to the diamonds (4.00 bits) and farthest from the
  opening (6.36). The language drifts gradually along the book. **REAL.**

![Book order](figures/fig_book_order.svg)

- **Dee's order is nearly the smoothest possible.** Summed similarity of neighbouring sides: 91.2,
  against 84.3 for random orders (best of 500: 85.9) and 91.5 for a greedy "smoothest" ordering.
  Sides a and b of one table are about as alike as b and the next table's a (0.982 vs 0.979): the
  drift is continuous across leaves. **REAL.** Mirror pairs (t ↔ 49 − t) and tables in the same
  column of the 7×7 plan are no closer than random pairs. **REFUTED.**
- **Rows as verses:** a segmenter that never sees row breaks puts a word break at 34% of row breaks
  vs 19% of random positions (≈ 11 standard errors): rows end on word boundaries. **REAL** (the row
  edges again, measured a new way).
- **Acrostics and centres:** no name in the first- or last-letter columns of 36 squares, nor in the
  string of their centre cells (AHAROTNLDOVCHCOA…). **REFUTED.**
- **The pyramid's cross:** in the rebuilt diamonds, name cells are not drawn to the diagonals or the
  centre (z 1.9, 1.8 — slightly away, not toward). **REFUTED.**

### Bridges to the other systems, and the constellation `[a25]`

- **No other system "lives" in the Loagaeth.** Watchtower names occur 749× (Markov-3 expects 814),
  words of the Calls 1,008× (1,087), Aethyr names 1,999× (2,117) — all at chance; the 91 governors 0×
  (1.2 expected); the 49 Heptarchic angels once (BORNOGO, in the heartland; 0.2 expected — not
  significant alone). The frequent shared strings are short (ADNA 501×, RAPH 134×, TOR, TAN, ARN).
  Watchtower strings are rarer in the end (0.26× its share) — the U register again. **REFUTED.**
- **Constellation:** stacking the 36 squares, the busiest 3×3 window of each master name (CHASTOR 5,
  GETH 6, NOCHA 8 …) is inside both nulls (random row; random column). Names have no favourite cell.
  **REFUTED.**

**In the 3D viewer:** "Name set → discovered" overlays these names by family; **Constellation**
shows a name's start cells across the stacked squares beside its null; the **two-currents
vocabulary** toggle colours names on each current of 25b–28b; **Order** shows the 94×94 similarity
terrain with the dialect table.

| Discovered names on 12a | Constellation (NOCHA) vs null | Currents on 26a | Similarity terrain |
|---|---|---|---|
| ![disc](figures/viz_discovered_names_12a.jpg) | ![const](figures/viz_constellation_nocha.jpg) | ![cur](figures/viz_currents_vocab_26a.jpg) | ![order](figures/viz_order_terrain.jpg) |

### Dee's letter names as a reading layer `[a26]` — construction

Every letter of the Angelic alphabet has a name in Dee's table (A Un, B Pa, C Veh, D Gal, E Graph,
F Or, G Ged, H Na, I Gon, L Ur, M Tal, N Drux, O Med, P Mals, Q Ger, R Don, S Fam, T Gisg, U Van,
X Pal, Z Ceph). The meanings used here (A "indomitable, pulsing force", H "life", O "insight"…) are a
modern attribution supplied by the practitioner — a lens for reading, not evidence about the text.

- **Readings:** CHASTOR = Veh · Na · Un · Fam · Gisg · Med · Don — *crowned conquest → life →
  pulsing force → cosmic vessel → cosmic nourishment → insight → growth*. CHUSTOR differs only in
  the third letter: Van, *true law*, instead of Un. Every master and discovered name is spelled out
  in `results/26_letter_names.json`.
- **The measured grammar in this lens:** rows open with Van (U, ×4.2), Mals (P, ×3.0), Ceph (Z),
  Ged (G), Veh (C); they close with Fam (S, ×3.6), Ger (Q), Na (H), Med (O), Pal (X). Graph, Na,
  Don and Pal (E, H, R, X) almost never open a row.
- **Each realm's signature letters** (share vs the whole book): opening Tal, Fam, Or (M, S, F ×2);
  heartland Gal, Drux, Un; 26–28 Gisg, Pal; diamonds and end Van, Don, Mals (U ×2.7 at the end).
- **Names vs random strings of the book:** the recurring names are rich in Fam, Veh, Na, Un (S, C, H,
  A — the CHASTOR letters) and poor in Van, Pa, Or, Tal, Ger (U, B, F, M, Q). This restates letter
  frequencies, read through the names.

In the 3D viewer the **Letters** view draws a 21-letter chart for every square (share or
enrichment), with a picker to follow one letter through the book, and the name panel shows each
name's reading.

| Letters, book mode (Van/U picked) | One square (12a) | Reading of CHASTOR |
|---|---|---|
| ![letters](figures/viz_letters_book_U.jpg) | ![single](figures/viz_letters_single_12a.jpg) | ![reading](figures/viz_name_reading_chastor.jpg) |

Followed through the book: **Van (U)** rises from 3–5% to 14.2% at the end while **Un (A)** falls from
~20% to 5.8% (the U register); **Don (R)** rises toward the end; **Gisg (T)** and **Pal (X)** peak in
26–28; **Tal (M)** and **Fam (S)** are highest in the opening and Fam fades after it; **Na (H)** and
**Med (O)** stay flat (≈ 7% and 9%) in every realm.

### The machine question: can an algorithm turn the data into code?

What the machine side has given, honestly:

- **It recognises the language** (a character model): it confirmed the diagonal decoding of 25b–28b,
  the one road through the diamonds, the U register, and that the text has a single direction.
- **It can write more of it** (an order-5 generator produces convincing pseudo-Loagaeth), and it
  can **segment** the dense lines twice as well as chance against an independent editor.
- **It finds no generating program.** No periodicity (unlike the Soyga), no 2-D rule, no copying, no
  long-range memory, and compression gains almost nothing over a 3-letter model. The text is not
  the output of a short algorithm that could be reversed.
- **It cannot translate.** Translation needs anchors — words with known meanings. The Loagaeth has
  23 shared with the Calls, and no gloss for CHASTOR or its family (Peterson's index has none). A
  model can map structure; it cannot invent meaning without such anchors.

### 3D viewer — the tables as squares, diamonds and pyramids

![3D pyramid view](figures/viz_pyramid.jpg)

An interactive three.js viewer of every table (`viz/loagaeth_3d.html`, data from
`src/make_viz_data.py`). Open it through a local server (some browsers block scripts on
double-click):

```bash
python -m http.server 8860
```

then visit `http://localhost:8860/viz/loagaeth_3d.html`. Views:

- **Square** — any 49×49 side as tiles in the two chessboard colours; master-name cells raised and
  coloured (CHASTOR gold, ANZACH coral, GETH/ALGETH teal, NOCHA/ADNOCHA violet, ACLAX green,
  CHUSTOR blue). On 25b–28b, a toggle animates **the two currents** on the diagonals.
- **Diamond** — one diamond side as a stepped rhombus split into its two stepped pyramids, or both
  sides combined back into the 49×49 square, with a slider turning it through 45°.
- **Pyramid / Octahedron** — *the hypothesis "squares are bases, diamonds are faces", made
  visible*: a square table as base, the triangles of two diamond sides as the four faces (unfoldable
  into a flat net); or two pyramids base to base. This is a construction for exploring, not a
  finding: what is established is only that each diamond side is two stepped pyramids joined at
  its widest row.
- **Book** — the 49 tables on the 7×7 plan, coloured by territory; click a plate to open it.
- **Heatmap** — the 36 sides of 2a–25a that are exact 49×49 grids stacked into one: per cell, how
  many sides put a master name there, or observed/expected for any letter. A **Null** toggle swaps
  in the same sides with letters shuffled inside each side (seed 1583).
- **Trail** — the top letters' hotspots joined in order (A O N H L D R C X E G T, or true frequency
  order) by a gold tube, with the shuffled null's trail in cyan; on the stack or any single side.
- **Closed pyramid** — the base carries the stacked name heat; the 1,802 master-name cells of all
  diamond sides 29–48 glow on the four faces.
- **Tesseract** — a hypercube (24 square faces) turning in 4D, wearing 24 consecutive square sides.
- **Icosahedron** — 20 triangular faces carrying the upper and lower halves of ten diamond sides.

Every view links by URL hash (e.g. `#view=heat&hMode=letter&hLetter=X&hNull=1`).

| Heat map (letter X) | Trail, observed vs null | Closed pyramid |
|---|---|---|
| ![heat](figures/viz_heatmap.jpg) | ![trail](figures/viz_trail.jpg) | ![closed](figures/viz_closed_pyramid.jpg) |
| **Tesseract** | **Icosahedron** | |
| ![tesseract](figures/viz_tesseract.jpg) | ![ico](figures/viz_icosahedron.jpg) | |

**What the overlays show — no symbol.** Inside the grid, the hottest cells of every letter (ratio
2.2–5.5) are matched by the shuffled null (2.3–4.8): noise. The one real structure is the **row
edges** already found in `[a16]`: X sits at column 1 only 0.01× its average and at column 49 1.62×;
H 0.10× → 2.03×; G 1.89× → 0.52×; C 1.67× → 0.58× (null: 0.82–1.12× for every letter). So the trail
is pulled to the edges (O, H at the end of the row; L, C at the start) and otherwise zig-zags like
the null's. Master names hit any one cell in at most 9 of 36 sides, with no figure; on the closed
pyramid they are short horizontal streaks on all four faces, nothing at the apex or along the edges.
The tesseract and icosahedron are ways to look, not results.

**Second round of views.**
- **Inverse** (Pyramid / Closed pyramid): every face mirrored, side by side with the original, and
  reversed master names marked in magenta.
- **Elements** (Heatmap / Closed pyramid): heat split into quartiles and coloured, hottest to
  coldest, Fire (red), Air (yellow), Earth (brown), Water (blue) — the practitioner's lens, applied
  the same way to the null. Plus a **view from above**.
- **Tesseract by signature**: only the outer cube is textured; faces can be filled with sides that
  share the same top-three letters instead of consecutive sides.
- **Signatures**: the 94 sides as tiles in columns by their top-three letters.

| Inverse (ALGETH reads HTEGLA) | Elements, from above | Signature map |
|---|---|---|
| ![inverse](figures/viz_pyramid_inverse.jpg) | ![elements](figures/viz_elements_heat_top.jpg) | ![signatures](figures/viz_signature_map.jpg) |

What they show `[a21 F]`:
- **The text has one direction.** Read backwards, the names vanish: CHASTOR 179 forward / 0
  reversed, ANZACH 150 / 0, GETH 504 / 0, ADNOCHA 172 / 0 (only DAXO, OXAD reversed, appears — it
  is the DAX stem + O). A letter model trained forward reads reversed text at 6.1 bits vs 3.5.
  On the diamonds, reversed hits are DAXO only (19 vs 6.6 expected), forward names 426 vs 80.
- **Signatures sort the book by itself.** A dominates 83 of 94 sides; U 7 (43b–48b), R 3, N 1, all
  at the end. Top-three signatures follow the segments: AON opening, ANO heartland, AOX/AOL/AOR
  diamonds, ARO/RAO late, URN/URO/UON end — the segment difference of `[a16]` made visible.
- **Seen from above, the pyramid's four triangles are not separate realms.** Mean name heat per
  triangle: top 2.41, bottom 2.44, right 2.05, left 1.77 (null ≈ 0). Left and right are cooler only
  because they hold the row-start and row-end columns, where names rarely sit (edges 0.58 vs 2.31
  inside). With Elements, the edge columns are 87% Water; the interior splits evenly. For letters
  (where the null is usable) every triangle sits within ±4 points of the null, except X, whose
  absence from row starts makes the left side "Water".

**Majority by sub-quadrant.** A button paints each block in the element that holds most of its
cells: halves (four 24×24 quadrants plus the central cross as its own strip), 4×4, or the 7×7 blocks
of the book's plan. A "Display" select swaps the heat bars for the flat 49×49 letters in their
element colours.

| Letter H, halves, from above | Name heat, 7×7 | Side 12a as flat letters |
|---|---|---|
| ![2x2](figures/viz_majority_2x2.jpg) | ![7x7](figures/viz_majority_7x7.jpg) | ![flat](figures/viz_majority_flat_letters.jpg) |

What it shows: the first and last block columns are Water (cold) — up to 73% for the name heat —
and for H the last column turns Fire/Earth while the first stays Water; the null shows no such
columns. That is again the row edges (H closes rows, X never opens one). The interior blocks mix
Earth, Fire and Air with no figure. Note: quartile cut-offs fall on tied values, so Water's band
often holds the most cells and wins blocks for that reason alone.

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

## What is left — the roadmap

See [docs/ROADMAP.md](docs/ROADMAP.md): the ledger in one screen and every open question with its
test, null and stop rule (closing doubts, names, architecture, anchors for meaning, the machine
side, practitioner constructions, publication).

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
