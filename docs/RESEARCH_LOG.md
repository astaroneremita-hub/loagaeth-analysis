# Research log — how we got here

A chronological record of the questions asked, how each was tested, and what came back.
Every entry is tagged **REAL** (beat its null or is true by inspection), **REFUTED** (failed its
null), **INCONCLUSIVE**, or **DESCRIPTIVE** (a true observation that cannot carry a p-value,
usually because it was noticed after looking). The module that reproduces each result is named.

The rule throughout: an idea is welcome from anywhere — statistics, Kabbalah, a tarot spread, a
dream — but it only enters the findings after a test against a null model that preserves the
text's own texture.

---

## Phase 1 — What kind of text is it?

| # | Question | Method | Result | Tag | Module |
|---|---|---|---|---|---|
| 1 | Is the Loagaeth language-like or noise? | Entropy, conditional entropy, index of coincidence | H₁ 4.03 → H(next\|current) 3.44 bits; IC 0.079 ≈ 2× uniform | REAL | a01 |
| 2 | Prose or list? | Type/token, repetition, network of recurring strings | Catalog of names; scale-free hub structure | REAL | a01, a02 |
| 3 | Is there a master name? | Substring counts per table | CHASTOR 184× in 35/48 tables; NOCHASTOR 61×; CHUSTOR its A/U twin | REAL | a03 |
| 4 | Do names inflect? | Prefix/suffix inventory around stems | Closed prefix set NO-/NE-/ZI-/NA-/OL- on CHAST; forest CHASTOR, DAX, CHADAX | REAL | a04 |
| 5 | Does each table have its own name? | Most distinctive 6-gram per table | 48 distinct, none CHASTOR-family | REAL | a05 |
| 6 | Shared words with the Calls? | Whole-word matches in word-spaced leaf 1 | 23 matches (~10× chance), IAD, GAH, ORS, URAN, ZIR, MAD… | REAL (small) | a06 |

## Phase 2 — Keys that did not open it

| # | Idea | Result | Tag | Module |
|---|---|---|---|---|
| 7 | Mirror/reversed names | 102 pairs vs 93 under a Markov-3 null | REFUTED | a08 |
| 8 | Semitic triliteral roots | words/skeleton ≈ 1.3, English-like | REFUTED | a08 |
| 9 | Call vocabulary as decode key | ~3.4% substring overlap ≈ chance | REFUTED | — |
| 10 | Gebofal reordering, 4 geometric models, YHVH/MAD ciphers | none beat null | REFUTED | — |
| 11 | Acrostic of the prologue | gibberish; translation kills any cipher | REFUTED | — |
| 12 | Decimation by 2 along rows | structure collapses (2220 → ~20 recurring 6-grams) | REFUTED | — |
| 13 | Watchtower-style extraction from the grid centre | centre ≈ random positions (z ≤ 1.7) | REFUTED | engine/extract_names.py |

## Phase 3 — The grammar and the language

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 14 | Do letters have positions? | MI(letter; position) 0.181 vs 0.003, z ≈ 331; G/V onsets, H terminator | REAL | a09 |
| 15 | Same tongue as the Calls? | Word-ending profile r = 0.71 vs English 0.22 | REAL | a09 |
| 16 | Is the Loagaeth "older" than the Calls? | Loagaeth less English-like (0.22) than the Calls (0.56) | REAL (descriptive reading) | a09 |

## Phase 4 — The empire

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 17 | Does CHASTOR govern a territory? | Contiguous zone, lag-1 autocorrelation 0.51 vs null 0.20 | REAL | a10 |
| 18 | Is GETH a rival house of CHAST? | Morphology complementary; territory only at density null; no syntax | REAL (not rivals) | a11 |
| 19 | Are the "seven Lords" seven beings? | They overlap and nest inside compounds | REAL (refines earlier list) | a12 |
| 20 | Title nesting | CHASTOR 184 ⊃ NOCHASTOR 61 ⊃ ADNOCHASTOR 10 (≈ ÷3 per title), same for CHAPH, ANZACH | REAL | a12 |
| 21 | Bigger name = bigger realm? | length vs frequency ρ = −0.39 (opposite) | REFUTED | a12 |
| 22 | Does gematria encode power? | ρ = +0.11 | REFUTED | a12 |
| 23 | Is CHA a closed core? | 2,811×, open continuation | REFUTED | a12 |
| 24 | Vowel twins as a noble mark | 99% of any frequent 7-gram has one | REFUTED | a12 |
| 25 | ANZACH, second stem | 153×, 39 tables, NO·CHA·NZACH parallels NO·CHA·STOR; a standalone word in leaf 1 | REAL | a14 |
| 26 | NOCHA as a closed title slot | open continuation (7.7 bits) | REFUTED | a14 |
| 27 | Grimoire "powers" (sefira, planet…) | the project's own provenance marks them convention; CHASTOR got two incompatible assignments | provenance warning | a12 |

## Phase 5 — The numbers

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 28 | Why 2/3/6? | Number = head digit + permuted 2·3·6 block; block z 7.6–9.0; anagram pairs z 13.7 (digit-preserving null) | REAL | a13 |
| 29 | What sets the head digit? | Shared within an Aethyr — only in Aethyrs 15–30 (z 8.2), free in 1–14 (z −1.4) | REAL | a13 |
| 30 | Tribe, part, name as head drivers | p 0.14–0.78 | REFUTED | a13 |
| 31 | Any rule in 30 candidates (gematria of Aethyr names in 13 systems…) | best 4/16 vs 4.3 by chance (p 0.83) | REFUTED | a13 |
| 32 | Order of the block | "236" in 13/30 vs 5 expected (p 0.0005) | REAL | a13 |
| 33 | Dee's declared sum for Aethyr 2 | 6660 fits only if DIALIVA = 662; all sources give 8962 | INCONCLUSIVE (likely a slip) | a13 |

## Phase 6 — The physical book

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 34 | Why do tables 29+ hold half the letters? | Each side is a diamond (1201 / 1200 cells) = the two chessboard colours of one 49×49 grid, written on the diagonals | REAL | a15 |
| 35 | Which way does the language run there? | Along the diagonals (names 0.15); rebuilt rows/columns are noise | REAL | a15 |
| 36 | "Kelley skipped every other letter" along rows | adjacent stats match, skip-one do not (JS 0.09 vs 0.35) | REFUTED (as row-skipping); REAL in its chessboard form | a15 |
| 37 | Tables 26–28 | Read by rows: no sequential structure, no names, doubled letters at chance | **SUPERSEDED by #49** (wrong reading direction) | a15 |
| 38 | Doubled letters | Loagaeth ≈ 11× below chance; Calls looser; 26–28 at chance | REAL | a15 |
| 39 | Method check | Raw per-table counts confounded by format; length-normalised CHASTOR density steady 6–43 | correction | a15 |

## Phase 7 — The kingdom, read as a government

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 40 | Do the top letters spell a name? | No, k = 3…8 | REFUTED | a16 |
| 41 | Do letter values follow frequency? | No, 13 systems with correction | REFUTED | a16 |
| 42 | Left/right "pillars" | Only the row edges: onsets open rows, terminators close them; inside, left = right | REAL (edges) / REFUTED (pillars) | a16 |
| 43 | Distinct letter mix per realm | χ² ≈ 11,100 vs ≤ 3,800 | REAL | a16 |
| 44 | The end in a U register | A→U overlap 387 vs 228 as is; other swaps lower | REAL (transcription caveat) | a16 |
| 45 | Names preferring a side or height | No side; ALGETH low (z −3.1) | REAL (ALGETH only) | a17 |
| 46 | "As above, so below" as mirror symmetry | none | REFUTED | a17 |
| 47 | Borders on the 7×7 plan | ~~heartland ends at the centre~~ — revised: writing turns rows→diagonals between 25a and 25b (centre of the plan); diamond format starts week 5 | DESCRIPTIVE (revised by #49) | a17 |
| 48 | Implicit correlation zone | Two houses (NOCHA vs GETH/ACLAX) exclude each other inside each realm | REAL | a17 |

## Phase 8 — The source page, the machine, the energy

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 49 | Peterson marks `~ / \`` in 25b–28b — what are they? | Each mark falls on one chessboard colour; each colour read on the diagonals is ordinary text (rows 0.001 → 0.27; control 0.005). Tables 26–28 are not noise | REAL (corrects #37) | a18 |
| 50 | Where does diagonal writing begin? | Side 25b — after side 49 of 98 | DESCRIPTIVE | a18 |
| 51 | Is CHASTOR absent from 26–28? | No: 16× once decoded; the realm is continuous 6–43 | REAL (corrects territory) | a18, a10 |
| 52 | Do leaf titles summarise their leaf? | No (15% vs 16%); 5b's title holds ZUCHASTORS | REFUTED / DESCRIPTIVE | a18 |
| 53 | Is the Loagaeth machine-generated like the Soyga? | No periodicity, no 2-D rule; Soyga columns periodic | REAL | a19 |
| 54 | Does a language model read it as a language? | Decoded 26–28 3.44 bits vs rows 7.62; end improves with U→A (5.05 → 4.25) | REAL | a19 |
| 55 | Can a machine write it? | Yes, at the surface (order-5 generator) | REAL | a19 |
| 56 | Is the end "denser" in letter energy? | Yes in 10/14 measures, mostly via A→U; information stays higher | REAL (with caveat) | a20 |
| 57 | Fibonacci structure | none | REFUTED | a20 |
| 58 | 7×7 gradual division / central cross | edge effect only / not special | REFUTED | a20 |
| 59 | Golden-Dawn quadrant rearrangement | original best 35/35 | REFUTED | a20 |

## Phase 9 — Peterson's index, the Heptarchy, the numbers

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 60 | What is the angelix index? | Concordance of leaf 1 only (t1 = 1a, t2 = 1b), no glosses; 97.5% of 3,589 references on the stated line | REAL | a21 |
| 61 | Does the index line up with our rows? | Leaf 1b line 20 is split over two rows in the transcription; later lines +1; 1b has 49 lines | REAL (data correction) | a21 |
| 62 | Variant readings | 71 refs differ by 1–2 letters: Z/X, U/B, N/U, R/X | DESCRIPTIVE | a21 |
| 63 | Do the dense lines of 1b have word structure an outside reader agrees with? | Model vs Peterson's breaks F1 0.33 vs 0.16 random (p < 0.0005) | REAL | a21 |
| 64 | Letter counts vs 7 / 42 / 49 | at chance; total ≡ 0 mod 7 from the 49×49 build; B 16% in Heptarchic names vs 1.2% in Loagaeth | REFUTED (numerology) | a21 |
| 65 | AONHLDRC… as a string | AONH 1×, ONHL 1×, nothing longer; in no name pool | REFUTED | a21 |
| 66 | Gematria 6 and 5 of the counts | came from mistyped counts; GD sum 1,486 (not 1,446), order-independent | REFUTED | a21 |
| 67 | Does the inverse (mirror) reading hold names? | Names vanish (CHASTOR 179 → 0); only DAXO; forward model 3.5 vs 6.1 bits | REFUTED (text has one direction) | a21 |
| 68 | Group squares by dominant letter | A 83/94; U/R/N only at the end; top-3 signatures track the segments | REAL (restates a16) | a21 |
| 69 | Pyramid from above / four elements | triangles differ only by the row-edge effect; letter maps ≈ null except X | REFUTED (no figure) | viewer |
| 70 | Do core findings survive other readings (Z=X, U=V, U→A, clean sides, 2% noise)? | grammar, row edges, segments, names hold everywhere | REAL (robust) | a22 |
| 71 | CHASTOR territory, re-measured | count lag-1 0.49 (p<0.001); per-1000 0.26 (z≈2); U→A z 1.1 | REVISED (moderate; partly the U-register boundary) | a22 |
| 72 | Segmentation tuned on Peterson (leave-one-line-out) | F1 0.33 → 0.36 (random 0.16) | REAL (modest) | a22 |
| 73 | Other roads through the diamonds | only stored anti-diagonals read (3.71 bits vs ≈7.8 for 9 other paths) | REAL | a22 |
| 74 | Long-range memory / hidden code | excess memory only at 4–12 letters; beyond = side-to-side letter mix | REFUTED (long range) | a22 |
| 75 | Copying of blocks between tables | longest shared 16 vs surrogate 18 | REFUTED | a22 |
| 76 | Zipf / Heaps on leaf 1 | same profile as the Calls at equal size | DESCRIPTIVE | a22 |
| 77 | Vertical (2-D) structure in squares | z 1.7 | REFUTED | a22 |
| 78 | Sub-quadrant majority of elements | only edge block columns differ (row edges) | REFUTED (no figure) | viewer |

## Phase 10 — Names, architecture, bridges

| # | Question | Result | Tag | Module |
|---|---|---|---|---|
| 79 | Can the text reveal its own names (no supervision)? | 47 word-like strings beyond Markov-3 (Bonferroni); surrogate 0; rediscovers the known families | REAL | a23 |
| 80 | New names outside the known families | NACHO 157×/31 tables, AXALGRA, GRADAX, PHANGE, ANTANTOX, VOXAR, TAXALGRA, ONDANVAGE, UCHER… | REAL | a23 |
| 81 | Name families | 5 families of 3+ (surrogate 0); core + prefixes/suffixes (~40% of list length) | REAL | a23 |
| 82 | NACHO vs NOCHA | vowel mirror, both strong | DESCRIPTIVE | a23 |
| 83 | Two currents of 25b–28b | 5-gram Jaccard 0.221 vs random split 0.29–0.34; names lean to one current | REAL (new) | a24 |
| 84 | Dialects | each realm reads its neighbours best; chain opening→…→end | REAL | a24 |
| 85 | Book order | neighbour similarity 91.2 vs random ≤ 85.9, greedy 91.5 | REAL | a24 |
| 86 | Mirror t↔49−t, 7×7 plan columns | no closer than random | REFUTED | a24 |
| 87 | Rows as verses | row breaks are word breaks 34% vs 19% | REAL (row edges) | a24 |
| 88 | Acrostics / centre cells | no names | REFUTED | a24 |
| 89 | Names gather on the pyramid's diagonals or centre | z 1.9 / 1.8 away | REFUTED | a24 |
| 90 | Other systems' names inside the Loagaeth | all at Markov-3 expectation; BORNOGO once | REFUTED | a25 |
| 91 | Constellation of names across stacked squares | within both nulls | REFUTED | a25 |
| 92 | Dee's letter names + practitioner meanings as a reading layer | readings of all names; grammar and realm signatures re-expressed | CONSTRUCTION (lens) | a26 |
| 93 | Segment borders without assumptions | 5 blocks: 12b|13a, 25a|25b, 33a|33b, 40b|41a; opening not separate; U register from 41 | REAL / REVISED | a27 |
| 94 | Do dialect chain and U register hold on the new parts? | yes (U→A 436 vs as-is 242, other vowels ≤ 300) | REAL | a27 |
| 95 | Irregular rows | 7 isolated ±1; 8b one column dropped (−37); 9a −376 (rows 1–7); 12b −4 | DESCRIPTIVE (needs manuscript) | a27 |
| 96 | U/A in the manuscript | no table images available | OPEN | a27 |
| 97 | Territories of each name | 12 survive Bonferroni (NOCHA family, GETH/ACLAX family, NACHO, GRADAX, OXAD); CHASTOR alone p 0.027 | REAL | a28 |
| 98 | Houses beyond part effects | NOCHA house peaks ~11–21, GETH/ACLAX house ~25–31 | REAL | a28 |
| 99 | Core born before its titles? | 23/27 vs 22.7 expected (z 0.19) | REFUTED | a28 |
| 100 | Vowel mirroring as a rule | 304 vowel vs 342 consonant swaps; surrogate same ratio | REFUTED | a28 |
| 101 | Names hidden behind the dominant ones | MACHO, DNACHAP, NOPHAR, ANZANO, NACHAPA, DRAXVL, RONTANTOXA | REAL (candidates) | a28 |
| 102 | Variants split by current | χ² 14.5 vs 9.5, p 0.09 | REFUTED | a28 |
| 103 | Diamond a/b sides as two vocabularies | Jaccard 0.279 vs split 0.277 | REFUTED (currents are special) | a29 |
| 104 | Where the language changes fastest | neighbours 1.07 vs random 1.72 bits; largest jumps in 40–48 | REAL | a29 |
| 105 | Leaf-1 words inside the tables | 2,780 vs 3,081 expected | REFUTED | a29 |
| 106 | Particles between names | flat gap lengths 0–11; few short gaps | DESCRIPTIVE | a29 |
| 107 | Glossed Call words inside the Loagaeth | all 26 at Markov-3 expectation; none word-like and in excess | REFUTED | a30 |
| 108 | Dee's diaries for glosses | text not available online | OPEN | a30 |
| 109 | Leaf titles in their leaf's dialect | mean own rank 0.49 (chance 0.5) | REFUTED | a30 |
| 110 | Does a names+letters grammar code the text better than letter habits? | 3.000 vs 2.985 bits/letter (3.027 with lexicon) | REFUTED | a31 |
| 111 | One grammar or one per part? | book grammar better except part V (3.55 vs 3.68) | REAL (end is distinct) | a31 |
| 112 | Do the other systems share the Loagaeth's letter order? | Calls z 23.9, governors 13.4, Heptarchy 8.5 | REAL | a32 |
| 113 | Are rule-read Watchtower names words of the tongue? | z 1.9 (0.8 by Calls model) vs governors 13.4 | REAL (new): governors are the word layer of the Great Table | a32 |
| 114 | Is the Great Table rule-generated (Soyga-type)? | cell not predictable from left/above | REFUTED | a32 |
| 115 | Dee's diaries for glosses (closes #108) | ~30 glossed words, all leaf 1; none for tables 2–48 or the master names | DESCRIPTIVE | a33 |
| 116 | Do Dee's glossed words occur in the tables? | 21 of 25 never; rest at chance (53 vs 57) | REFUTED | a33 |
| 117 | Reading direction vs leaf 1 | as transcribed 3.57 bits, reversed 4.97 | REAL | a33 |
| 118 | "The first leaf is the last" | leaf 1 nearest the opening tables (3.45 → 4.55) | DESCRIPTIVE | a33 |
| 119 | Call n ↔ table n+1 | p 0.63 | REFUTED (textual link) | a33 |
| 120 | Table 18 "spirits of the earth" | home of NECHASTOR; Y ×2.9 | DESCRIPTIVE | a33 |
| 121 | Is vowel change a mechanism (POLA/PALA)? | leaf 1: 222 one-vowel pairs vs 33; 17 vowel series vs 0.8 (z 18.6); ratio to consonant pairs z 3.6 | REAL (new) | a34 |
| 122 | Master stems as vowel grades | GETH/GATH/GOTH/GUTH, NOCHA/NACHA/NECHA, ANZACH/ONZACH/UNZACH/ENZACH | DESCRIPTIVE | a34 |
| 123 | Nalvage's table/number references locate the Call's letters? | best of 48 indexings 9/61, family-wise p 0.79 | REFUTED | a35 |
| 124 | Structure of Nalvage's numbers | rise with table (ρ 0.79); 33/38 = thousands + small tail | DESCRIPTIVE | a35 |
| 125 | How reliable is the hand + transcription? (Soyga tables regenerated) | 3.3% errors; z→x 8.5%, n→u 6.5% | REAL | a36 |
| 126 | Is the U register a misreading? (closes #96) | a→u 1/329, u→a 0/332; U→N recovers nothing | REAL — register is in the manuscript | a36 |
| 127 | Are 25b–28b fully decoded? | 27a: rows 1–28 by rows then ↘ (5.52 → 2.74 bits); 26a: rows 1–8 + zones (5.01 → 2.92); 25b: rows 1–5 (matches Peterson); names 349 → 384 | REAL (corrects a18) | a37 |
| 128 | Every k-th letter gives Call-like text (Laycock) | k = 2…12 ≈ shuffled | REFUTED | a38 |
| 129 | Tables 43–48 as a replicated pattern | not copies; less internal repetition | REFUTED | a38 |
| 130 | Rule in the Heptarchic number layouts | no affine fit, no drift | REFUTED | a38 |

Note: from #127 on, tables 25b–28b are read with the refined decoding of a37; counts quoted in entries
79–122 moved by a few units (current values are in the README and in results/*.json).

## Side tracks (recorded, not findings)

- **Tarot dialogue.** Questions to the cards were turned into tests: "the Wheel" → CHASTOR's
  distribution (found the territory, REAL); "the King of Pentacles / numbers" → CHASTOR-family
  gematria (REFUTED). The cards are a source of hypotheses, never evidence.
- **Felt experience.** Practitioner reports (chills during the work) are part of the practice and
  are respected as such; they are not used as evidence about the manuscript.
- **External anchor.** No source we hold glosses CHASTOR or its family (lexicon search, 81-book
  corpus). The meaning of the proper names remains sealed.
