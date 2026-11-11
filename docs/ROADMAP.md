# Roadmap — what is left to investigate, to the end

Written after modules a01–a26. Every item is a question with a test, its null, and a stop rule.
Tags in the ledger follow RESEARCH_LOG.md (REAL / REFUTED / DESCRIPTIVE / REVISED).

## 1. Where we stand (ledger in one screen)

**Real and robust:**
- **The writing:**
  - The text is language-like, written in one direction.
  - Positional grammar: G/V open, H closes, rows end on word boundaries.
  - Letters are almost never doubled.
- **The names:**
  - Master stem CHASTOR, with titles nested about ÷3 per level.
  - ANZACH, the sibling stem.
  - Two houses (NOCHA vs GETH/ACLAX).
  - 47 recurring names found by the text itself, in five families (NACHO is the vowel mirror of NOCHA).
- **The book's form:**
  - Four formats; the writing turns from rows to diagonals at side 49 of 98.
  - Tables 25b–28b are two decoded currents, which carry two vocabularies.
  - The diamonds have exactly one reading road.
- **Change along the book:**
  - Four segments with different letter mixes.
  - A dialect chain, with a near-maximally smooth book order.
  - The U register at the end.
- **Outside sources:**
  - The governors' numbers: head digit + a 2·3·6 block.
  - Peterson's index checked; its divisions of the dense lines serve as a segmentation gold standard.

**Revised:** the CHASTOR territory (moderate; partly the U-register boundary).

**Refuted:**
- **Ciphers and number keys:** mirrors, Semitic roots, Fibonacci, Golden Dawn rearrangement, numerology 7/42/49, gematria of power.
- **Hidden figures and patterns:** acrostics, centres, symbols in the heat maps, constellations, pyramid-cross gathering.
- **Copying and code:** block copying, long-range code.
- **Outside names:** other systems' names inside the book.

**Sealed:** the meaning of CHASTOR and its family. No gloss exists in any source we hold.

## 2. Priority tracks

### Track A — Close the remaining doubts (do first)

**Status (a27):** A3 done — borders 12b|13a, 25a|25b, 33a|33b, 40b|41a; segments revised (opening not
separate, U register from 41). A2 diagnosed (8b dropped column, 9a damaged block, 7 isolated ±1); the
corrections need the manuscript. A1 open — no table images available; next step is consulting
Sloane 3189 images (British Library) when accessible.

| # | Question | Test | Null | Stop rule |
|---|---|---|---|---|
| A1 | Is the U register Dee's or the transcriber's? | Check 200 random U/A and Z/X cells of tables 43–48 against the facsimile images of Sloane 3189 (manual sample, logged) | — (error rate) | If >10% of U are A in the image, rerun a16/a22 with corrected letters |
| A2 | Rows of 48/50 letters (11 sides) | Locate each irregular row; compare with the facsimile; record omissions | — | Corrected grid file `data/loagaeth_corrections.json` (sourced, never silent) |
| A3 | Are the segment borders where we put them? | Change-point detection on the per-side profile (letters + trigrams), no prior borders | permutations of side order | If borders differ from 5/25/28/43, update SEGMENTS everywhere |

### Track B — Names (largest chance of new real findings)

**Status (a28):** done. B1 real (12 territories), B2 real (houses territorial), B3 refuted, B4
refuted as a rule, B5 seven hidden names, B6 refuted.

| # | Question | Test | Null | Stop rule |
|---|---|---|---|---|
| B1 | Do the new names have territories? | a10-style zonation for NACHO, AXALGRA, GRADAX, PHANGE, ZIDNOPHA, ONDANVAGE, UCHER | shuffled table order | report z per name, Bonferroni |
| B2 | Do new names belong to the two houses? | co-occurrence per table with NOCHA vs GETH/ACLAX; partial correlations within segments (a17 method) | table-label permutation | each name assigned to a house or "neither" |
| B3 | A genealogy along the book | first appearance and spread of each family member; does an affixed form (ADNOCHAP) appear only after its core (NOCHAP)? | random first-appearance order | test "core before title" across all families |
| B4 | Is NACHO↔NOCHA vowel mirroring a rule? | count all name pairs related by swapping two vowels; compare with pairs related by any other single permutation | surrogate candidate lists | REAL if mirror pairs exceed other permutations |
| B5 | Lower the detector's blind spot | rerun a23 with a Markov-2 baseline and with each known name masked, to see what CHASTOR-like names hide behind the dominant ones | surrogate as now | stop when no new survivors appear |
| B6 | Do the names of the two currents form complete pairs? | for every name on ↘, look for its counterpart on ← in the same face (same core, different affix or vowel) | random line split | REAL if pairing beats split |

### Track C — Architecture

**Status (a29):** done. C1 refuted (diamond halves are one text), C2 real (small steps; jumps at
40–48), C3 refuted, C4 descriptive (no particles).

| # | Question | Test | Null | Stop rule |
|---|---|---|---|---|
| C1 | Are the a/b diamond sides (the two chessboard colours of one square) also two vocabularies, like the currents? | 5-gram Jaccard a vs b per table 29–43 | random split of the table's lines | REAL if below split range |
| C2 | Where exactly does the dialect change fastest? | cross-entropy between consecutive sides (a24 models) along the book | shuffled order | list the sharpest steps; compare with leaf titles and dates |
| C3 | Leaf 1 ↔ tables | which leaf-1 words (Dee's spaced text) occur in the grids, where, and in which current | Markov-3 expectation | map leaf-1 vocabulary onto the book |
| C4 | Is there a grammar beyond names (particles, function strings)? | short high-frequency strings between names (2–3 letters) and their positions relative to names | shuffle within rows | candidate "particles" list |

### Track D — Anchors for meaning

**Status (a30):** D1 refuted (Call words at letter-habit rates), D2 open (needs the printed Five
Books of Mystery or the BL photos of Sloane 3188), D3 refuted.

| # | Question | Test | Null | Stop rule |
|---|---|---|---|---|
| D1 | Words shared with the Calls (ADNA 501×, TAGE, EMNA, HARG…) | where they occur, what precedes/follows them; do they keep Call morphology? | Markov-3 | a short list of probable shared words with contexts |
| D2 | Dee's diaries around the Loagaeth sessions (Sloane 3188, 1583) | read the passages where the angels name or comment on the tables; any gloss of a table word | — | any gloss becomes an anchor; none = stays sealed |
| D3 | Leaf titles | titles decoded by the dialect models; are titles in the same dialect as their leaf? | other leaves' titles | REAL if own-leaf fit beats others |

### Track E — The machine side

**Status (a31):** done. E1 refuted (no code shorter than a 3-letter memory), E2 real (only the end
needs its own grammar). Remaining tracks: F (constructions, on request) and G (publication).

| # | Question | Test | Null | Stop rule |
|---|---|---|---|---|
| E1 | Small generative grammar of the whole book | probabilistic grammar = names (a23 families) + particles (C4) + letter model for the rest; compare its compression with Markov-3 | Markov-3 | if it compresses better, the grammar is the best "code" of the text |
| E2 | Can the grammar reproduce the drift? | one grammar per segment vs one for the book | — | report bits saved |

### Track F — Practitioner constructions (kept separate from findings)
Labelled "construction" in the repo, no claims of discovery:
- **Letter-name readings:** readings of every name (a26), and a tablet of the discovered names in Dee's letter names.
- **Elements and letter charts:** element maps and per-square letter charts in the 3D viewer.
- **Name tablets:** if wanted, invocation tables built from the discovered families. They use the same conventions as the Watchtower system and are marked as built, not found.

### Track G — Publication
- **Reproducibility:** freeze a release with `run_all.py` reproducible from a clean clone. Record the data sources and what is git-ignored.
- **Paper-style report:** "Liber Loagaeth: what the text shows" — findings, refutations, method, limits.
- **Commit and release:** a CITATION file and a tag, only on the user's word.

## 3. Order
1. **Doubts:** Track A (A3 first; A1/A2 need the facsimile).
2. **Names and architecture:** B1, B2, B4, C1, B6, C2 — the most promising for new real findings.
3. **Anchors and machine:** D1, D3, C3, C4, then E1/E2.
4. **Close:** F on request; G at the end.

Each finished item: module + figure + README section + log entry + SESSION_FINDINGS line, and a
3D view where a picture helps.

## 4. After the web research (a32–a36)

Done: one phonology across the systems (a32); Dee's diaries read and tested (a33); vowel paradigms
(a34); Nalvage's coordinates (a35); scribe calibrated on the Soyga tables — A1 closed (a36).

Still open, from the literature survey (`data/raw/research_hypotheses.md`, git-ignored):
- Leaf 25b has a third series (Peterson) — re-decode 25b with three currents.
- Note on leaf 43a: tables 43–48 are a pattern "to be filled" — test repetition structure of 43–48.
- Table 49: the 21 words as five tables of 21 letters (112 vs 105 letters).
- Laycock's "every tenth letter": do decimated tables look like Calls?
- Heptarchy: structure of the six number layouts of the seven 7×7 tables (restores 8 lost cells if a rule exists).
- Images of Sloane 3189 (phergoph mirror, fols 02r–57v) for spot checks of Z/X and N/U.
- Robustness set of a22 extended with the measured confusions (z→x 8.5%, n→u 6.5%).

**Update (a37, a38):** 25b third series done and extended (27a, 26a re-decoded); 43–48 replication,
every k-th letter and Heptarchic layouts refuted. Left: the unclear corner of 26a (90 letters); table 49's 21 words; spot checks on the manuscript images; a22 with the measured confusions;
update the 3D viewer's currents for 26a/27a to the mixed layout.
