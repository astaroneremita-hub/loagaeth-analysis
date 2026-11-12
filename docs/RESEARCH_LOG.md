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
| 131 | Do long strings repeat beyond chance? | 12 letters: 549 vs 116 (Markov-3); 14: 94 vs 11; 16: 5 vs 1 | REAL | a39 |
| 132 | Do long repeats need units longer than formulas? (held-out halves) | 259 shared; model of the other half: 120 (order 3), 521 (order 5) | BOUNDED — about six letters | a40 |
| 133 | Syntax between names? | adjacent 91 pairs p 0.81; successive 693 pairs p 0.86 | NOT SHOWN | a39, a40 |
| 134 | Compounds with a fixed order | OXAD+NOCHA 16 vs 1.7; GETH+ACLAX 9 vs 0.9; never reversed | SUPERSEDED by #141 (shuffle misled by overlapping names) | a40 |
| 135 | Long repeats copied in place? | same columns no more than shuffles (p 0.88) | REFUTED | a40 |
| 136 | Passages recurring with one letter changed | 179 vs 21–30; A/O 31, A/E 10, H/L 7, P/T 7, L/R 7 | REAL | a40 |
| 137 | Is that variation the copyist's? | Soyga confusions explain 2 of 179 | REAL — variation is in the text | a40 |
| 138 | Consonant changes stay inside sound classes? | 50% vs 21% by frequency; surrogates 37%; classes post hoc | SUGGESTIVE | a40 |
| 139 | Same, classes fixed beforehand (manner, place), 12 surrogates, fresh 10-letter variants | manner 41% vs 36% surrogate (p 0.18); fresh set 38.5% vs 35.5%; place nothing | REFUTED as a rule of its own — the slot grammar gives it | a41 |
| 140 | Do interchangeable consonants share manner of articulation? (incl. leaf-1 words) | variants 41% vs 21% by frequency; leaf 1 25.7% vs 20.9% (p < 0.001); place at chance | REAL (property of the grammar) | a41 |
| 141 | Compounds, strings searched in Markov-3 surrogates | GETHACLAX 17 vs 3.8, GETHACLAXTO 6 vs 0.25: REAL; OXADNOCHA 23 vs 16.4 (= OX + ADNOCHA): REFUTED | CORRECTS #134 | a42 |
| 142 | Where do long repeats fall? | inside one part 51% vs 20%; inside parts 7.2 vs 8.1 tables apart (p < 0.001); same leaf not favoured | REAL (local reuse) | a42 |
| 143 | Spelling drifts along the book? | 8 pairs tested, best p 0.125 | NOT SHOWN | a42 |
| 144 | Does the text reuse what it has just written (cache model, echo by lines)? | cache 2.920 → 2.906 bits, same with lines shuffled; 8-letter echo flat over 30 lines | NOT SHOWN — lines of a side are near exchangeable | a43 |
| 145 | Faint echo of 5-letter strings 1–4 lines below | 16.3 vs 15.0 per 1000 (z 5.4); 5–16 lines z 1.0; near same column p 0.02; window chosen post hoc | REAL but weak | a43 |
| 146 | Likeness of sides by distance | 15.6 per 1000 (adjacent) → 9.3 (20 apart); random 7.4 | REAL | a43 |
| 147 | Do our tests detect sentences where they exist? (Bible as the tables reach us) | English: z 15.7 / 10.0 / 37.8; no-syntax controls ≈ 0 | REAL — the tests have power | a44 |
| 148 | The tables on the same tests | next unit z 1.9; order of lines 0.0023 bits (z 4.5), a tenth of English; echo +8% (z 5.3) | REAL — no prose-like sentences along the rows; small order signal | a44 |
| 149 | The Calls on the same tests | 4,700 letters: the test misses the Bible's own syntax at that size | NO POWER | a44 |
| 150 | What decides the variant of a formula? | part z 8.5; table z 3.7; vowel 4–9 letters before z 3.1; side, row, column, previous choice: nothing | REFUTED as a positional channel | a45 |
| 151 | Can a machine write the book? | order 5 per side + neighbours reproduces repeats of 12, names, GETHACLAX, the gradient between sides | REAL (sufficiency) | a46 |
| 152 | What no machine reproduces | echo over 4 lines (1.08 vs 1.0); one-letter variants 110 vs 74–85; repeats of 14: 70 vs 53–55 | RESIDUE — templates with a slot | a46 |
| 153 | Templates with one free slot beyond the machine? | 9 letters: 566 vs 582 (G5L); 11: 59 vs 52 (max 70); 13: 5 vs 1 | EXPLAINED by the machine | a47 |
| 154 | Any memory beyond five letters of context, inside a side? | letter 6–14 back given the 5 before: z 1.3, 1.3, −0.8, 0.4, 0.7; Bible z 7.3–21.6; false book ≈ 0 | REAL — none detectable | a47 |
| 155 | Memory beyond five letters on chessboard leaves and diamonds? (Bible cut to the same shape as control) | z between −1.2 and 1.1 in every group; Bible 2.6–10.2 | REAL — none in any format (diamonds: few contexts) | a48 |
| 156 | Echo over four lines by format, corrected for line length | rows 1.085 vs 1.01 (z 7.0); chessboard 1.73 vs 1.41 (z 3.9); diamonds z 1.1, 1.4 | REAL in rows and chessboard; NOT SHOWN in diamonds | a48 |
| 157 | Method: shuffling lines of unequal length fakes an echo (ratio 1.4 in memoryless text) | compare with same-shape surrogates | ARTEFACT REMOVED | a48 |
| 158 | Does the text run on from one row to the next? | start of a row given the end of the row above: 12.47 vs 13.91 bits (z 15.9), 44 of 46 sides; upwards z 1.0; boustrophedon z 1.4; across the leaf z 1.1; side to next side z −0.8 | REAL — one stream per side, downwards | a49 |
| 159 | Rule against doubled letters across the line break | 85 vs 161 (z −7.0); inside rows 643 vs 9,250 | REAL — half strength across the break | a49 |
| 160 | Names split between two rows | 32 vs 16.7 (z 3.0) | REAL | a49 |
| 161 | Side b related to side a cell by cell (same, mirrored, upside down, transposed)? | all p ≥ 0.15 | REFUTED | a49 |
| 162 | Side b as side a half-turned | 8.94% vs 8.40%, p 0.002 (0.01 corrected), 10 of 13 leaves | SUGGESTIVE | a49 |
| 163 | Do the diagonals of the diamonds run on, in the stored order? | 29–40: 13.86 vs 15.26 bits (z 10.6); 41–48: z 6.2; opposite order nothing | REAL — order of the diagonals confirmed | a49 |
| 164 | Order of the diagonals on the chessboard leaves 25b–28b | forwards z 2.4, backwards z 3.7; differs colour by colour | OPEN — part of the decoding still to settle | a49 |
| 165 | Names counted along the joined stream (catalogue) | 51 of 3,968 occurrences split between two lines | DESCRIPTIVE | make_catalog |
| 166 | Order of the diagonals, colour by colour (25b–28b) | 25b colour 0 and 27b colour 1 (↘): stored order z 3.2, 3.5; same letter across junction 1 vs 6.2; split names 4 vs 0.3 (z 6.6) | REAL for these two | a50 |
| 167 | Order by road, pooled | ↘ stored order z 3.0; ↖ opposite order z 3.2; ↙ opposite order z 3.0; check on other blocks: same letter 21 vs 36 (z −2.9), rule reversed z −0.6 | PROBABLE — ↖ current = ↘ stream on a half-turned page | a50 |
| 168 | Word points of tables 2a–5a recovered from the source (232 rows, 1,425 words) | gold word boundaries; HZEMBL and DAHOXI were read across boundaries | CORRECTION — both withdrawn | a51 |
| 169 | How often is a word repeated? | 95.2% of words written once (leaf 1 67.5%, Calls 56.9%, Bible 8.8%); mean length 8.0 | REAL — no lexicon | a51 |
| 170 | Catalogue names against the points | whole word 3, start 13, end 11, inside 20, cut 10 (24.6 at random, z −4.2) | REAL — names are parts of words | a51 |
| 171 | Do rows end where words end? | edge words 7.4 and 8.9 letters, inner 7.9, blind cut 5.1 | REAL — whole words per row (refines #158, #160) | a51 |
| 172 | Our segmenters against the points | F1 0.335 and 0.223; random 0.114 | WEAK | a51 |
| 173 | Stress marks | next-to-last 391, earlier 443, last 64 | DESCRIPTIVE | a51 |
| 174 | English or Latin behind the letters? | tables 5.57 vs 6.32 bits; leaf 1 and Calls also lean English; far from both | Own pattern, mild English lean | a52 |
| 175 | Signs of a hand making letters at will | doubles 0.07, ABA 0.57, alternation 1.50, vowel pairs 0.24: beyond English, Latin, the Calls; Soyga ≈ 1 | REAL — more regular than speech | a52 |
| 176 | kondor.de an independent transcription? | 1 letter differs in 23,712; no n/u; same points, same irregular rows | REFUTED — copy of Peterson | a53 |
| 177 | Borders of the book against the diaries | "24 leaves being written" on 18 Apr 1583 = end of the row-written tables (border 25a/25b); no dated record for the other borders | DESCRIPTIVE (secondary notes) | docs |
| 178 | The primary record read (Sloane 3188, True and Faithful Relation) | see docs/WHAT_THE_SOURCES_SAY.md | CONTEXT — reframes the study | docs |
| 179 | Leaf 1 a table of words, 49 to a row? (diary) | 25 of the first 30 rows have exactly 49 words | CONFIRMED | a54 |
| 180 | Leaf 1 a key to the other leaves square for square? | 336 tests, mean z −0.1, one above 3 | REFUTED | a54 |
| 181 | The nine letter rows of leaf 1 side 2 | 3.84 bits (tables 2.80, leaf-1 words 4.79); hold NACHO, OXAD | DESCRIPTIVE | a54 |
| 182 | Is leaf 18 ("spirites of the earth") set apart? | ranks 14 and 23 of 24; nothing | NOT SHOWN | a54 |
| 183 | Images of Sloane 3189: are the two series of 25b–28b written in opposite orientations? | yes: alternate squares, tilted, turned half round from one another | CONFIRMED on the page (supports #167) | images |
| 184 | What are the "diamond" leaves 29–48 on the page? | the same 49 × 49 chessboard ruling with one series written, the other squares empty; note on 43a: "every empty square is to be filled as these are" | CONFIRMS a15 (two chessboard colours, 1201+1200); "diamond" names the transcription's print, not a page figure | images |
| 185 | Irregular rows of 8b–9a (a27) | figures on the page: capitals, a ring, boxed corners | EXPLAINED | images |
| 186 | n against u in Kelley's hand | mostly indistinguishable on the microfilm; z and x distinct | CAUTION for every n/u result (#96, #126) | images |
| 187 | Leaf 1 side 1 and the 49th table in Sloane 3189 | side 1 is not in the book (taken from the diary); f.57 is empty grids with two lines of angelic characters | DESCRIPTIVE | images |
| 188 | The 21 words of the 49th leaf (from the diary) against the rest | short words (DOX, NER, VORS, NOR, ADNOR, DONCHA) common in the tables; the long ones (BRTNC, HABZILB, HIROBRA, ZEDNIP, CHIMVANE, CHERMACH, ZANDOX, LOAGAETH) occur nowhere; read at 4.23 bits (table rows 2.51); DONCHA = DONCHAL−1 | REAL — a third register, the "hotchpot" the diary calls it | a55 |
| 189 | "They are but one Name" (Il): how few roots generate the names? | 58 names → 45 roots under the measured affix/vowel rules; surrogate name-sets of the same lengths → 57.9 (p 0.002); biggest root (CHAS) covers 5; 5 biggest cover 26% | REAL compression, but NO single seed — the literal "one Name" is not supported; the family structure is | a56 |
| 190 | Is the angel name DAHAHOXOM in the book? (reader's evocation of "dahahoxom"; DAHOXI said to resemble it) | DAHAHOXOM, DAHOXOM, DAHAHOX, AHOXOM, HOXOM occur nowhere (forward or backward); DAHOX 6× (3 are DAHOXI = "dah.oxi" across a point) | NOT IN THE TEXT (experience not contradicted; name absent) | a57 |
| 191 | Are the Calls assembled from letters scattered across the whole book? (reader) | Call words (≥4) occur contiguous 144× vs 136.9 random (z 0.8); first two Calls 21/89 vs 21.7 random; diary indexes Call letters to tables 21, 41, 46; a35 found no number rule | CONFIRMED — Calls are not localized chunks, unlike Watchtower names | a57 |
| 192 | Is there a textual reading direction? ("write backward, first leaf is last") | leaf read from preceding 6 leaves 3.282, from following 6 leaves 3.272; difficulty flat along the book | NO textual direction — binding order, not textual | a58 |
| 193 | Are the nine transitional letter-rows the seed of the table lexicon? | 3 names in them; names first appear in table 2, not leaf 1; 4-gram overlap table 0.056 vs leaf-1 words 0.028 | NO — the table language begins at table 2 | a58 |
| 194 | DAHAHOXOM — the wide search (all 8 paths, scribe-folding V/U/Z/X/I/Y, fuzzy ≤2 edits) | the whole name never occurs; AHOXOM/HAXOM/HAHOXOM never; DAHA common, OXOM rare, never adjacent; the one ≤2-edit near-match, DABAHOXIM on 2b, is "APRINDABAH.OXIMAGEN" across two word points | NOT A WORD in the book; its letters are present but scattered | a57+ |
| 195 | Are the Call words hidden along some reading path? (diagonals, backward, columns) | 8 paths × words forward/reversed; anti-diagonal reaches z 3.6 under a Markov-3 stream null but only z 1.5 under a word-scramble null; leaf-1 placebo words behave the same or stronger on every path | NOT FOUND — no path hides the Calls; the row signal is just real words beating letter-scrambles in a Loagaeth stream | a59 |
| 196 | Could the tables have been altered/scrambled after Dee? (seam scan) | bits per leaf flat, no outlier; geometry exactly 1201+1200=2401 on 13 of 20 leaves (the rest off by 1-2 cells or in the known irregular end); biggest jumps = the known format border 25a|25b (matches the diary's dates); 43-48 profile = known 4th segment | NO trace of rule-breaking alteration; coherent whole. LIMIT: statistics-preserving alteration needs an independent copy to detect | a60 |
| 197 | Nalvage's navigation numbers, checked against the required letter (exact TFR data, not blind) | best decoding 5/25 vs 2.6 chance, within multiple-test noise; numbers up to 312004 >> 2401 cells | RULE NOT RECOVERABLE — sharpest test, confirms a35 | a61 |
| 198 | Is the Loagaeth generated by a Soyga-style neighbour rule (cell = f(above, left))? | a cell keeps 3.02 of 3.95 bits given above+left; neighbours remove only 0.94 bits (Soyga removes ~all) | REFUTED — not neighbour-generated, far less determined than Soyga | a61 |
| 199 | Are the lines tuned to a syllable beat (metre)? | rows ~17.65 syllables, sd 1.05 vs 1.70 for the same letters shuffled (z -24); stress penultimate (452) then antepenultimate (301), rarely final (72) | REAL — the lines carry metre, as an intoned text would | a62 |
| 200 | Is the book a 49x49x49 cube with a readable depth axis? | same-cell MI across adjacent leaves 0.0066 vs 0.0048 (z 6, but 0.0016 bits, negligible); names down the stack 7 vs 5.9 (z 0.4) | REFUTED — no third reading axis | a62 |
| 201 | Is the syllable beat constant across the book, and is there a stress rhythm? | ~17.6 syllables/line in segments I-III (V drops to 16); stress intervals mostly 3-4 (mean 3.75), sd 1.79 vs 2.64 random-placed (z about -9) | REAL — book-wide metre with a recurring stress foot | a63 |
| 202 | Finer chant structure: rhyme, closed syllabary, vowel melody? | rhyme weak (z ~2); ~441 syllables cover 90% vs ~505 surrogate (barely tighter); order structure in consonants (0.71 bits) not vowels (0.13) | NOT FOUND — lines are metrical but not rhymed; structure is consonantal, no vowel melody | a64 |
| 203 | Bridges to other systems, refrains, acrostics? | governors 1/91, Heptarchy 1/53 (Poisson noise); 0 repeated whole lines, 0 repeated 20-letter openings; 0 names down the margins (vs 0.3) | ALL NULL — systems separate, no refrain, no acrostic | a65 |
| 204 | A 7-fold substructure (49=7x7)? And a column template? | word points at mult-7 11.6% (below 12.5% chance); names flat mod 7; vowel autocorr peaks at lag 3 not 7; column vowel-share swings only in the first 5 columns, flat after (z 25 but it is a line-onset signature) | 7x7 is the frame not a rhythm; column effect = line-onset shape only | a66 |
| 205 | Does each table have a presiding (over-represented) name? | most leaves have one at p < 0.01 (NOCHA on 12-14, ANZACH 6.1x on 25a, ACLAX ~7x on 29); the map follows the houses and territories | REAL — a per-table working list of names | a67 |
| 206 | If DAHAHOXOM is gathered from scattered letters, where does its material concentrate? | whole name 28% of its fragment-density in the opening tables 2-6 (z 3.0); the distinctive core AHOXOM 37% (z 4.5); peak leaf 2a; tables 2-6 are 12% of the book | REAL and specific (no other name tested concentrates so) — the text holds the name at its opening; not a claim about the entity | a68 |
| 207 | Is a name "walkable" as a king-move path on a leaf a real signal or the dense field? | real names walk far above their own anagrams (NOCHASTOR 292, CHASTOR 160, z >100) and above random strings (160 vs 22 best paths); BUT the walk-leaf matches the leaf where the name is actually written only 7/56 (12%) | REAL as a language property (names are Loagaeth-shaped and walkable), NOT a locator — a walk on a given leaf is not "meant" | a69 |

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

## #208 — Omni-directional reading (a71) — REFUTED
Image 4 (Vincent Bridges) claims Enochian squares read from 4 directions × 4 corners. Test: 8 dihedral
orientations of each 49×49 leaf, catalogue-name hits per orientation, vs Markov-3 surrogate. Written rows
52.4 hits; other 7 directions 0.7 each (77× fewer); real-other 0.7 ≈ surrogate 0.7 (z −0.51). The Loagaeth
reads ONE way; no omni-directional design like the Watchtowers'. Confirms "direção única."

## #209 — Rotation-family clustering (a72) — DESCRIPTIVE, one real hit
Murilo's reading: rotations/branches of a name = same entity, so they sit "glued together." Test: NN-distance
among positions of a name + its cyclic rotations (both writings) on its busiest leaf, vs 8 Markov-3 surrogates
of that leaf. Mean z −0.87 (threshold −1). Branches ARE near each other on the page (NN 1.7–3), but a same-flow
surrogate glues them about as tight — the gluing is the shared letters, not placement beyond flow. OXAD itself
z +0.48 (not glued beyond flow). Exception: CHADAX z −5.40 (real NN 3.0 vs surrogate 8.4) — a genuinely tight
family, worth a follow-up.

## #210 — Massive family-clustering sweep (a73) — REFUTED (CHADAX was a tail event)
Seeds: 761 recurring 4/5-gram rotation-families across the whole book. NN-distance on busiest leaf vs 24
Markov-3 surrogates (cached per leaf). z<-2: 1 observed vs 17 expected by chance; z<-3: 0 vs 1; mean z −0.30;
scattered (z>+2): 1. No excess of glued families — the opposite. CHADAX's earlier z−5.4 came from only 8
surrogates (noisy sd) and regressed. No deliberately-placed glued sub-population; the gluing is letter-flow
everywhere. Visual (ACHNZ 25a, OXAD 15b): real and surrogate scatter look equally clustered.

## #211 — Row stratification: every line is a balanced inventory (a74→a75) — CONFIRMADO NOVO
Chased from a gematria probe (a74): under a small ordinal value-map, row-sums are far more uniform than any
shuffle (DEE_ORD row-cv z −2.8, 35/42 leaves) while ISO (wild values) is flat and columns go the opposite way.
Not arithmetic. Traced (a75) to the cause: each LETTER is spread across the 49 rows more evenly than chance —
index of dispersion var/mean of per-row counts is sub-Poisson. All letters ratio 0.72 (z −5.2), VOWELS 0.68
(z −2.8), CONSONANTS 0.71 (z −4.5), 36/42 leaves z<−3. Holds for consonants, so it is NOT the known
~constant-syllables-per-line metre. Neither a full shuffle (0.92) nor a column-preserving shuffle (0.93)
reproduces the real value (~0.57) — so it is a genuine 2D placement rule, not letter frequency and not per-column
grammar. Every row carries a near-equal share of every letter. New global compositional rule. Visual: letter A on
2b sits at 9–11 every row (var 1.4) vs 4–16 shuffled (var 8.3).

## #212 — Letter column-position map (a76) — no fixed column, only edges
Follow-up to a75: within a row, where does each letter sit? Column concentration 0.07 (0=no preference).
Odd-vs-even row column-profiles agree at cosine 0.59 real vs 0.58 shuffle (gain 0.013) — column position is
not predictable. Each letter roams the whole row. Only edge preferences (known rule): I/E to the start, V/P/Z/G
col 0, S/H/X col 48; weak (6-10% peak share). So the book lets you predict HOW MANY of a letter per line
(stratification), not WHERE in the line. book_column_profile saved for mapping.

## #213 — Names are woven into the grid (a77) — CONFIRMADO NOVO (strong)
Fair control = the name's OWN letters scrambled. Core family names trace as connected king-move paths far
above their scrambles, book-wide: 232/460 name-leaf pairs (50%) are "woven" (real traces >=3 paths AND 0 of 80
scrambles reach it). CHASTOR woven on 30/37 leaves (15b ratio 271x), ADNOCHA 28/42 (14b 619 paths vs 0),
ALGETH 26/39. Longer names (ICHASTOR, NECHASTOR) trace while every scramble traces zero. Each family has a home
region: CHASTOR 15b/18b/22b, DAHAHOXOM 2b (43x), NOCHA 14b, GETH 23b. The specific letter-ORDER of these names
is built into the grid; permutations are not. Reading: the book is woven from this name-vocabulary. (Interpretive
limit stated once: "beats own scramble" = the order follows the book's own letter-weave, which is why the names —
the book's own words — thread it; it is the weave and the names being the same fabric, not a separate hidden cipher.)

## #214 — Territory map from the weave (a78) — CONFIRMADO NOVO (convergent)
Per-family z-normalised weave-ratio assigns each leaf a home family. Mean book position: CHADAX 13.2 (opening),
NOCHA 17.8 (front-middle), CHASTOR 18.2, GETH 28.3 (back). GETH rules the back (16a-27b almost solid), NOCHA the
12a-14b block, CHADAX the opening. Built only from king-move tracing vs letter-scrambles, this reproduces the
two-house geography (NOCHA early / GETH late) found independently by the straight-reading analysis (a67) — two
unrelated methods agree on the same map. Families are placed in regions, like governors over territories.

## #215 — Hierarchy and elemental powers (a79) — DESCRIPTIVE (clean for 2 houses)
Each Enochian letter carries a GD element (sign->element). Name's dominant element = its power. By family:
CHADAX = Terra/Earth (3/3 members, opening territory), CHASTOR = Ar/Air (3/3, spine), NOCHA = Ar/Água mixed,
GETH = Fogo/Terra mixed, DAHAHOXOM = Ar. Honest limit: family agreement is largely driven by the shared root
letters, so it is not independent proof of a house-element, and a clean 4-element division does not hold — only
CHADAX=Earth and CHASTOR=Air are clean. Next: test whether a family's HOME territory leaves carry that element's
letters above chance (would tie power to territory beyond the stem).

## #216 — Complete hierarchy map (a80) — DESCRIPTIVE (Murilo's model realized)
Rank validated catalogue names (len>=5, forward+reversed) by repetition per square and book-wide, Watchtower-style.
SUPREME: NOCHA=Rei (492 total, king of 34 squares), ADNOCHA=Nome de Deus (168), NACHO=Espirito (148), CHASTOR=
Arcanjo (132), ANZACH=Senior (127); singletons = anjos menores. NOCHA is king nearly everywhere because it nests
inside its whole family (ADNOCHA/NOCHAP/NOCHASTOR). The "independent ruler" layer (top name not a substring of a
longer present name) gives each square its local governor: ANZACH mid-book, ALGETH late, GRADAX 14-15, CHADAX
opening — consistent with the a78 territory map. Two-tier structure: NOCHA over-king + per-square governors + court
+ lesser spirits. Honest limit: raw counts include letter-flow; ranks use len>=5 names to stay meaningful.

## #217 — Generative name-grammar (a81) — CONFIRMADO NOVO
The repetition hierarchy (a80) is a root + affix grammar. Each validated name decomposes as a ROOT (NOCHA, NACHO,
CHASTOR, ACLAX, GETH, ANZACH...) with a prefix and/or suffix: AD-NOCHA, NOCHA-P, NOCHA-STOR, I-CHASTOR, AL-GETH,
ACLAX-TO. Power (book-wide repetition) falls with derivation depth: depth-0 roots mean 127 vs depth-2+ derived 29.
NOCHA 492 -> NOCHAP 100 -> NOCHAPH 41 -> ADNOCHAPHA 12; ACLAX 118 -> ACLAXTO 37 -> ACLAXTOR 13 -> AXACLAXTO 6. The
root repeats most; each added layer repeats less, like a source and its weaker emanations. Non-monotonic note: the
AD- prefix is itself productive (ADNOCHA 168 > NOCHAP 100). This is the generative system behind the names.

## #218 — Affix meaning (a81 follow-up) — LEAD
Grouping derived names by affix: prefix AD-/AL- -> all Terra (AD-NOCHA flips the Ar root NOCHA to Terra;
mean power 74); prefix I- weak (power 14, demotes); suffix -A diminutive (mean power ~20, the smallest
emanations); suffix -P marks high rank (NOCHAP/ADNOCHAP ~70). Honest: partly mechanical (element = letter
composition, and the affix adds its own letters' elements) and confounded by shared roots, so it is a
coherent lead, not an independent rank-morpheme proof. Affix = elemental charge + rank marker.

## #219 — Grammar discovers new names (a82) — CONFIRMADO NOVO (strong)
Generate every prefix x root x suffix (1319 candidates), count in the FULL book (tables 2-48, diamonds 29-48
included via base_book), compare to 6 Markov-3 surrogates. 253 candidates occur; 54 beat the surrogate across
>=3 tables; 32 were NOT in the prior catalogue - new branches the grammar generated and the text confirms.
Top: NECHASTORA (23x surrogate, 6 tables), NOCHASTORAL (15x), NOCHASTORAD (10x, 12 tables), ZICHASTORA (7x),
ANOCHASTOR = NOCHA+STOR cross-family fusion (6x, 13 tables), ADNOCHAPH (25x in 20 tables), ANTANTOXA, ALGRADAX,
ANZACHAL, ALGETHAD, ICHADAX. Productive prefixes NO-/A-/AD-/AX-, suffixes -A/-AL/-P/-AD. The generative grammar
is predictive: unseen root+affix combos are really present above letter-flow. 32 names added to viz/grammar_data.json.

## #220 — Bridge names (a83) — border hypothesis REFUTED, bridge class REAL
Names carrying two roots are a real class (7 fusions >=4x). Border hypothesis (a bridge sits where its two parent
houses meet) FAILED: 0/7 sit between parents. Instead the NOCHA+CHASTOR fusions cluster in the back of the book
(mean pos 34-44, GETH region), later than both parents. The standout: NOCHASTOR (NOCHA+CHASTOR) appears in 42/47
tables, 65x - a near-universal connector of the two great houses, not localized. The grammar is recursive: affixes
stack on derived names (NOCHASTOR -> NOCHASTORAD -> AXNOCHASTOR; ADNOCHA -> ADNOCHAPHA depth 5). So bridges exist
and the tree grows deep, but bridges do not mark territorial borders.

## #221 — Entity profiles + interactive atlas (a84)
Dropped the borrowed Watchtower ranks (Rei/Arcanjo/Anjo) - they did not hold. Each name (89 entities) is now
profiled by MEASURED attributes over the full book: forca (total occurrences), alcance (tables, 0-74), potencia
(occurrences / Markov-3 surrogate = how far above letter-flow), elemento (GD element of its letters), natureza
(the element's temperament, a labelled correspondence), classe (raiz/derivado/ponte, from the grammar), profundidade.
Two axes emerge: forca (ubiquity) and potencia (deliberate placement) are DIFFERENT - NOCHA force 621 but potencia
1.1x (common, not placed), while NOCHASTORA potencia 4.8x, NOCHAPH 2.8x (rarer, pointedly woven). Interactive atlas
at viz/atlas.html (scatter forca x potencia, size=alcance, colour=elemento, click for profile + family). Data in
viz/entity_data.json.

## #222 — Two layers: common substrate vs deliberate compounds (a84 follow-up)
High-potencia entities (>=2.5, n=56) are mostly long DERIVED names (49/56 derivado, median len 8, median forca 11,
alcance 10). Low-potencia (<1.5, n=11) are short ROOTS (5 raiz, median len 6, forca 151, alcance 45). So the book has
a common substrate (short roots, ubiquitous, textura) and a deliberate layer (long compound/derived names placed far
above chance). Partly a length effect (long strings have low surrogate expectation), but the long compounds recur well
beyond chance, so they are the genuinely-placed entities; the roots are the shared alphabet of the name-system.

## #223 — Coverage + attribute algorithm (a85)
Coverage: the name-system appears in ALL 47 tables (2-48, diamonds included). Dense in 2-38 (median 25 names/table,
up to 190 occurrences); thin in the deep diamonds 43-48 (1-6 names - also the least-reconstructed). So it spans the
whole book, strongly for most, faintly at the deepest diamonds.
Attribute algorithm (a85): each Enochian letter carries a GD sign + planetary condition + element; a name is read as
the sum -> element balance (4 elements %), ruling planet, signs, and a traditional "forma do ser". Deterministic,
reproducible. Generated for all 89 entities, exported to viz/entity_astro.json and rendered in the atlas detail (clic
a name -> full ficha). Honest scope: this DEFINES the attributes the alphabet assigns a name; it does not prove the
name denotes a literal spirit - that remains the practitioner's reading, which the measured structure supports but
cannot establish.

## #224 — Name space + two tools (a86)
Name space is FINITE and numerable, bounded by the grammar: 10 roots x (1+11 prefixes) x (1+12 suffixes) = 1320
combos at depth 1, ~15840 with a second affix layer; 89 attested (>=3x), 253 present at any count. Not infinite.
Affix element pushes measured: AD-/AL- -> Terra (force ~57/48), I-/ZI- -> Fogo, NO-/NE- -> Agua, Ar comes from the
roots. Two tools built in the repo site: viz/forge.html (pick element + force -> the roots/prefixes/suffixes that
build such a name, marking attested ones) and viz/tables.html (every 49x49 straight leaf with its system-names lit
on the original grid, coloured by element, click to isolate). Data: viz/forge_data.json, viz/table_grids.json.

## #225 — Gematria + cross-system (a87)
A) Gematria of top names across 12 systems: NOCHA and NACHO carry the SAME value in every system (149 isopsefia,
387 Crowley-astro, 141 primes...) - they are anagrams, so gematrically identical. The two top-ranked names of the
hierarchy are one being by number, an independent confirmation of the rotation=same-entity reading. Also CHASTOR=ANZACH
(24, digital), NOCHA/NACHO/ALGETH share 23. Notable: CHASTOR=30 (Aethyrs), GRADAX=12 (tribes) in Hildebrandt (one
system each, weak). B) Cross-system: the grammar roots (NOCHA, CHASTOR, GETH...) appear ZERO times in the Heptarchy's
49 angels, the 91 Governors, the kings, or the Call words. The Loagaeth name-system is its own layer, not shared with
or copied from the other Enochian systems.
