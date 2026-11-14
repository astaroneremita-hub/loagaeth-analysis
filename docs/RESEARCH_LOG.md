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

## #226 — External name search + what the book says (a88)
Searched 15 top Loagaeth names/roots against Shem-72, Goetia-72, planetary angels, and the Enochian kings/91
governors/Bonorum-49: ZERO matches (exact, substring, or within 1-2 letters). The Loagaeth onomasticon is sui
generis - its names recur nowhere in the standard angel/spirit corpora. Consistent with a87 (roots absent from
Calls/Heptarchy) and with Dee's own claim of a distinct primordial language. What the book says of itself
(docs/WHAT_THE_SOURCES_SAY.md): "every letter here bringeth furth the Names of God: but... they are but one
Name" (S99); "49 voices, whereunto the so many powers shall be obedient" (S73); "the mystical and holy voices
of the Angels... the CABALA of NATURE" (T158). Dee's description (it IS names; they are powers/angels; they are
one Name) matches the measured structure (a generative name-system; NOCHA=NACHO one value) remarkably.

## #227 — Calls-as-Loagaeth-coordinates + element methodology + loosened absence (a89)
Element methodology documented (WEAVE sec 17): letter->GD sign->element (triplicities), name = sum, dominant = power.
Coordinate theory test (a89): trigram cross-entropy. The Calls fit a Loagaeth-trained model (4.72 bits/char) better
than a Watchtower model (5.15) but EQUAL to shuffled-Loagaeth (4.68) - they share the Loagaeth letter INVENTORY, not
its local sequence. That is exactly what the coordinate theory predicts (letters picked from scattered locations keep
the inventory, lose local flow), so the test is CONSISTENT WITH but cannot prove the theory; the letter-by-letter
version needs the reception numbers digitised. Loosened absence probe: even reversed + consonant-skeleton + edit<=1
against 264 external names (Shem/Goetia/planetary/governors/kings) gives ZERO real matches (one spurious PHANGE~PHENEX).
The Loagaeth names are unique by every matching method.

## #228 — Element re-proof (multi-variable) + danger + roadmap 5/8/calls (a90, a91)
a90: element by 3 independent variables - zodiac sign (F04), second sign system (F05), and the ruling PLANET's
classical element. They disagree for some letters (N = Scorpio->Water by sign, Mars->Fire by planet). 55/89 names
have a ROBUST element (all agree); the rest are "majority" or "ambiguous" (sign vs planet split). All 89 still
match the single-variable sign reading (sign dominates the vote). Added a DANGER reading (traditional
correspondence, 0-100): Fire + martial/Saturn + nodal letters (T/F dragon, D spirit). NOCHA danger 43 (medium,
martial); CHASTOR 20 (low); ADNOCHA 43 (martial+nodal). Exported to viz/entity_power.json, shown in the atlas.
a91: (8) ELEMENTAL FLOW IS ORDERED - dominant element per table makes 17 transitions vs 25 shuffle (regions, not
random; Terra 2-5, Ar 6-14, Terra 15-30, Ar 31-44). CONFIRMADO. (Calls) Calls 1-2 words: 0 present as substrings
in the Loagaeth (chance also 0) - inconclusive, and consistent with the coordinate theory (Call words are not
contiguous Loagaeth substrings). (5) The odd/superfluous letter = the centre cell: spread over 15 letters, no
fixed mark - the mathematical pivot of 2401=2400+1, slight vowel lean.

## #229 — Is it a language? YES (a92); Call char-trace refuted (a93)
a92 — three independent linguistic signatures: (A) ZIPF: the name-vocabulary frequency follows a power law,
slope -1.14, r2 0.981 (real languages do this, random text does not). (B) ENTROPY LADDER: Loagaeth drops
h0=4.01 -> h3=2.52 bits/char, far below frequency-matched random (h3=3.41) and matching its own Markov-3
surrogate - it carries conditional information like a language, not noise (stays high) nor a rigid cipher
(near zero). (C) MORPHOLOGY: 13 vowel-alternation minimal pairs (same consonant skeleton, different vowels)
mirror Dee's own translated minimal pair pola/pala ("two together"/"two separated"), plus the intensifier
prefix (cru- -> crucanse). This is SEMITIC-STYLE morphology: consonantal root + vocalic pattern. Conclusion:
the Loagaeth is language-like and decipherable by linguistic method (anchor on the few translated words, use
morphology and minimal pairs), not only by evocation.
a93 — Call char-by-char trace: no Call traces as a connected king-move path through any Loagaeth leaf above
chance (Call 1: 9/349 vs shuffle max 14; and not the table Dee says it moves). Contiguous-path coordinate
theory refuted; a real link would be non-contiguous (scattered coordinates), untestable without the reception
numbers.

## #230 — CORRECTION: Call words ARE in the Loagaeth (a94)
Earlier (#225/a89) I concluded Call words were absent - WRONG, it filtered the data badly. The practitioner showed
GOHO across tables and PIADNAGENSAD at 21b. Proper test: 631 Call word-forms, 74 occur in the Loagaeth. GOHO 6x
(5 tables), SONF 4x, and of the 10 words >=6 letters, 5 are above chance: BALTAN (ratio 10, surrogate 0.00),
VNALAH (3x), LONDOH, IADNAH, PARACH. The 12-letter phrase PIADNAGENSAD sits at 21b. So the Calls and the Loagaeth
SHARE VOCABULARY, not just an alphabet - the same language. The overlap is real but partial (most Call words like
MICMA/ZODIRE do not appear), consistent with the Calls being drawn from / related to the Loagaeth field. Record
corrected.

## #231 — Item 3 (Bonorum titles) + PDFs + language page
Item 3: the 49 Bonorum (Dee's Tabula Collecta angels: BALIGON, BORNOGO...) vs our per-table governors: 0 matches.
The Loagaeth's own name-system is independent of the Heptarchic 49-angel assignment (consistent with a88).
PDFs attached (Tabula bonorum Sloane 3191, 29pp; 48 Claves Sloane 3191, 13pp) are SCANNED images (0 extractable
text); their content is already transcribed in engine/data (heptarquia bonorum, chamadas). Built viz/language.html
(bilingual): the three language proofs (Zipf -1.14/r2 0.981, entropy ladder 4.01->2.52, morphology), Dee's
translated anchors (canse/crucanse, pola/pala), the vowel-alternation minimal-pair repertoire, affixes with
element, and the Call words found in the Loagaeth (GOHO 6x, SONF 4x, BALTAN...). Data in viz/language_data.json.

## #232 — All 19 Calls mapped + Dee's translation pattern (a95) + two front-end pages
Mapped every word of all 19 Calls (1085 words) into the Loagaeth: count, tables, element, grid positions; with Dee's
English gloss (1071 translated). Translation pattern: (A) 96% of words are 1:1 Enochian:English - the Calls follow
ENGLISH WORD ORDER (reproduces Laycock's thesis that the grammar is English). (B) Morphology: only 7% of word-pairs
share >=2 consonants with the English gloss and 0 share the full consonant skeleton - the Enochian words do NOT derive
from English sounds; the lexicon is its OWN. (C) Lexicon consistency: 62% of words seen >=3x keep the same gloss - a
real, stable dictionary. Net: Enochian = English SYNTAX + an independent fixed LEXICON. Front-end: viz/call_map.html
(click a Call word -> its lit positions on the original 49x49 grid, with element + Dee gloss) and viz/call_translation.html
(each Call as Dee's English translation, Loagaeth-present words highlighted, toggle to Enochian). Data in viz/call_atlas.json.

## #233 — tables.html = ALL names (195) + diagonal segment finished (a96)
Rebuilt viz/table_grids.json with the FULL present-name set (195 names, len>=5, >=2x: a23 discoveries + roots +
all present root+affix combos), 2615 occurrences across tables - tables.html now lights up all names, not just the
top. a96 diagonal segment: name density per 1000 letters - straight (2-24) 28.8, DIAGONAL (25-28) 44.4 (the HIGHEST),
diamonds (29-48) 15.4. The diagonal reading surfaces MORE names than straight reading - validating the diagonal
decode. The same roots dominate every segment (GETH, NOCHA) and the element balance is identical (Terra ~35/Agua
~27/Ar 22/Fogo ~15), so the diagonal segment and the diamonds are the SAME onomasticon on a different geometry,
GETH-dominated toward the back (matches the territory map). Item 2 finished.

## #234 — Meaning overlay + tables.html 4 modes + name_grammar EN (a97)
a97: our own name-stems (NOCHA, CHASTOR, GETH) match 0/195 Call words - no external meaning, sense sealed (sui-generis
lexicon). But 39 TRANSLATED Call words appear in the Loagaeth and get a real Dee-given meaning placed on the grid:
IADNAH="ark of knowledge", ALDON="gather up" (7x), LONSA="power" (4x), EMNA="here" (30x), CALZ="above the firmaments"
(10x), NOCO="the servant". Honest decipherment: meaning only where an anchor reaches, never invented. Exported
viz/meaning_overlay.json. UI: tables.html rebuilt with FOUR reading modes (straight / diagonal / traced king-move /
meaning) over all 195 names + the meaning overlay (table_grids.json now carries straight, diag, trace paths, meanings).
name_grammar.html made bilingual (EN/PT). Site now: atlas, grammar, forge, tables, language, call_map, call_translation.

## #235 — Call words read every way (a98) + tables.html "all together"
Searched the Call vocabulary in the Loagaeth by straight rows, columns, diagonals and king-move TRACE, forward and
reversed (not just straight). Reading every way, 354 distinct Call words appear (vs ~74 straight-only). Long words
(>=6): 6 via straight, 145 once diagonals/traces allowed (+139: ABABALOND, ARCOAZIOR, ANANAEL, BALTAN, AGTOLTORN...).
Mode occurrence counts: straight 142, diagonal 141, trace 380. HONEST CAVEAT: trace finds almost any short word in a
dense field (established a69/a73), so trace-presence alone is weak; diagonal and straight hits carry more weight. The
practitioner is right that reading the grid the Watchtower way (diagonal/traced/reversed) surfaces far more Call words
than row-reading. call_atlas.json rebuilt with per-mode positions; call_map.html now draws straight (rects) + diagonal
+ traced (polylines) per word. tables.html got an "all together" mode overlaying straight+diagonal+traced+meaning at once.

## #236 — Complete recurring-word catalogue + grid search (a99)
Walked the whole book for every recurring substring, length 2-8: 115 bigrams (freq>=400) up to 3577 8-grams (freq>=4);
11299 words of len 4-9 at freq>=8. OLGEM confirmed (18x). Exported viz/word_catalog.json (browsable by length) and
viz/grid_words.json. New page viz/repertoire.html browses all recurring words by length with count + tables, click to
open in tables. tables.html gained a universal SEARCH box: type any word -> it is found live on the grid across rows,
columns and diagonals (forward + reversed), auto-jumps to a leaf that holds it, highlights in magenta, lists each
occurrence by direction (OLGEM -> 2b l41 c29). So any of the thousands of words is now mappable, not only the catalogued
families. Also wrote docs/PLANO_33.md - a 33-part exploration plan (inventory, geometry, language/decipherment, bridges,
book-structure, visual, synthesis).

## #237 — Catalogue extended to 14 letters + long compound super-names (a99/a100)
Extended the recurring-word catalogue to length 2-14. CHASTORACHANZA (14) confirmed 3x (tables 6b/17a/20a). A whole
family of long compounds recurs: NOCHASTORA(40), GETHALCHADAX(3, 3 tables), ADNOCHANZACHA(5)... a100: of 1431 recurring
words len 10-14, 40 are multi-root CHAINS - two fused roots: GETH+NOCHA, NOCHA+ACLAX, GETH+CHADAX, ANZACH+NOCHA, even
NOCHA+NOCHA (DNOCHADNOCHA, doubled). HONEST on significance: the long words occur 4723x in the real book vs ~865x across
Markov-3 surrogates = ~5.5x enrichment (real, but the surrogate still makes some, since they are built from the same
common roots/bigrams). So the grammar chains roots into long "super-names" and specific chains recur across tables -
these read like dynastic unions of two houses (GETH back + NOCHA front). repertoire.html tabs now go 2-14; word_catalog.json
carries all lengths.

## #238 — Deaccent fix: accented Call words now match + index complete
Bug: accented Call words (GOHÓ, ÓBÓLEH, QÄA, NOTHÓA, IÁDPIL, LÓHÖLO, IAÏDA, IÁDPIL) were kept with accents, so they
never matched the (unaccented) Loagaeth grid. Fixed a98 to strip accents (NFD + drop combining marks) and lowered the
search to len>=3. Call-word presence: 489 distinct words now appear (was 354); Call 1 marks 68/86 words (was 45; the
rest are 1-2 letter particles OL/TA/DS/OD). call_atlas.json, call_lexicon.json and table_grids meanings rebuilt
deaccented. index.html now lists ALL 14 panels (added names_catalog, loagaeth_3d).

## #239 — Plan items: name syntax, maximal words, 7x7, servants (a101-a103)
a101 (item 5, syntax): directional root collocation. GETHACLAX occurs 17x (26x chance) and ACLAXGETH 0x - a FIXED
ORDER (GETH before ACLAX, asymmetry 17:0); GETH+NOCHA 5:0. GETH is a leading root. First sign of word-order/syntax
BETWEEN names (narrow - few roots chain directly adjacent, but real). a102 (item 2, maximal words): branching-entropy
segmentation. 197 of 1288 frequent substrings behave as maximal word-units (high left+right branching, >=2.5 bits):
OTHA, ANGE, AGEN, ACHA, AXOR... the candidate real lexicon/morphemes (honest: high branching = common free chunks,
not proven semantic words). a103: (24) 7x7 plane - neighbours sim 0.59 vs distant 0.37 (more alike, but mostly the
smooth book order). (27) servant numbers (91 governors, 1230-9996) do NOT match any Loagaeth name's force - the
Heptarchic servant counts are a separate layer. Exported viz/maximal_words.json.

## #240 — Call search to len>=2 + coverage + square_reading not-found block + index EN
Lowered Call-word search to len>=2 (deaccented): 515 distinct Call words appear in the Loagaeth; of the 671 translated
Call words (len>=2), 506 are present and 165 absent. OL/TI/CLA/CABA/GOHO/IAD now mapped. table_grids meanings rebuilt
(2b: 112). square_reading.html gained a right-side "Not found in the book" block listing the 165 absent Call words with
their Dee translation (viz/call_coverage.json). index.html made bilingual (EN/PT toggle). Left = found & substituted,
right = not found.

## #241 — Not-found deep trace (a104) + grammatical classes (a105)
a104: of the 165 Call words not found straight/diagonal, 68 trace as a king-move path, 97 are absent by ANY reading.
HONEST: trace finds almost anything in a dense field, so trace-only is weak; 12 LONG words (>=8) trace and those
matter - MADRIIAX "O you heavens" (Call 1 opening), ZIRENAIAD "I am the Lord yor God", FETHARZI, PARACLEDA, OISALMAN.
97 are genuinely absent (PIRIPSON, LUCIFTIAS, BALZIZRAS, IADOIASMOMAR 12 letters). call_coverage.json updated to a
3-way split: found / trace_only / not_found(97). a105 (item 15, classes): distributional clustering of the top
maximal words by left/right context - real groups 22 words vs 28 in a Markov-3 surrogate = BELOW the null. No
grammatical word-classes beyond letter-flow; the groups that form just share consonant skeletons. Item 15 negative.

## #242 — Single-letter Call words + diagonal/reversed translated-squares
call_lexicon.json rebuilt to len>=1 (singles: I="is", D="the third", L/M/O/P/Q). call_grid_translation.html gained a
DIRECTION control (reta / diagonal down-right / down-left / column) plus the existing reversed toggle and a min-length
1-5 selector - so each table can be read-and-translated straight, diagonally, by column, forward or reversed. Verified
diagonal: 2b shows "of your Creation", "have setled" along the down-right diagonal.

## #243 — Sintaxe entre palavras testada ampla (a106): REFUTADA
a101 achou GETH→ACLAX com ordem fixa (17× vs 0×), conta alta, robusto. a106 estendeu a 60 palavras-topo: 48 pares
encadeiam >=3×; 19 ficam fortemente ordenados (uma direção >=3:1). MAS o null importa: surrogate Markov-3 (preserva
fluxo de letras, destrói ordem) dá 16.2 pares ordenados em média. 19 vs 16.2 NÃO bate chance — a assimetria em
contagens 3-6 é quase toda ruído de número pequeno. Conclusão honesta: NÃO existe gramática de ordem ampla no léxico.
A ordem fixa é real só em pares específicos de conta alta (GETH→ACLAX), não uma regra geral entre unidades.

## #244 — Leitch Vol II lida: as não-traduzidas da 2a são NOMES do Loagaeth, não palavras
Extraí o texto das 595 págs do "Angelical Language Vol II: Encyclopedic Lexicon" (Leitch) — 751 KB. Duas fontes:
Keys cross-reference (págs 44-90, glosa de Dee por palavra) e o lexicon A-Z. Meu call_lexicon já era chamadas.json
(678/679 palavras das 19 Chamadas, inglês do próprio Dee) — então as Chamadas já estavam 100% cobertas.
As 10 palavras SEM tradução da 2a (ANCHANO, VOXAR, PHADOL, PHANGE, NOCHADAX, ANOCHA, CHADAX, NOCHA, ANZACHOR,
ANZACH) NÃO estão no Leitch tampouco. Motivo: são os nomes-raiz das famílias do próprio Loagaeth (NOCHA/ANZACH/
CHADAX/CHASTOR), não vocábulo angelical de dicionário. Leitch (p95) diz explicitamente que EXCLUIU "milhares de
palavras indefinidas" — exatamente essas. Autoridade independente confirma: o Loagaeth gera NOMES, não frases.
Isso reforça o onomasticon. Leitch acrescenta ~240 palavras angelicais fora das 19 Chamadas (LAD=God, TAIDON=All
Powerful, GCIAD=Lord and Master...) salvas em viz/leitch_extra_lexicon.json — ampliam cobertura em OUTRAS tabelas,
não na 2a. A "tradução fluida" anterior (parágrafo em prosa) era costura minha com conectivos; removida. O literal
fiel (glosa de Dee por posição, sem-tradução no lugar) está em docs/2a_literal.txt e no square_reading.html.

## #245 — Lexicon mesclado Dee+Leitch com fonte por palavra; frontend com toggles
a109 reconstrói viz/table_grids.json `meanings` de um lexicon mesclado (919 palavras: Dee 679 das Chamadas +
Leitch 240 extraídas do Vol II), cada ocorrência marcada src=dee/leitch/both, buscada em reta+coluna+2 diagonais.
45.984 ocorrências em 42 tabelas. viz/translate_lexicon.json = mesmo lexicon para o call_grid.
square_reading.html reescrito: seletor de direção (reta/coluna/diagonal/todas), seletor de fonte (Dee+Leitch / só
Dee / só Leitch), checkbox mostrar/esconder sem-tradução; stream fiel na ordem das letras, Dee dourado, Leitch azul
(tag L), sem-tradução cinza no lugar. 2a reta: 409 itens (355 só-Dee, +54 Leitch). call_grid_translation.html ganhou
o mesmo toggle de fonte e cor por fonte. Honesto: Leitch acrescenta cobertura mas algumas glosas dele são OCR-ruído
(MAN=Of) — por isso o toggle, pra isolar Dee puro quando quiser.

## #246 — square_reading: leitura ladrilhada (tiling) com cobertura real de letras
Troquei a contagem de "hits sobrepostos" (que inflava: cada letra contada em várias palavras) por LEITURA LADRILHADA:
varre a direção, pega a maior palavra do dicionário em cada ponto SEM reusar letra, o resto vira run [SEM TRADUÇÃO].
Agora o número é honesto. 2a reta (Dee+Leitch): 313 palavras traduzidas, 1676 de 2401 letras sem tradução, 30% das
letras cobertas (só Dee: 297, 27%). Confirma quantitativamente: ~70% da grade NÃO forma palavra de dicionário
conhecida — é material de nome (famílias NOCHA/ANZACH/CHASTOR). O frontend mostra cobertura %, trechos sem tradução
crus no lugar, e o texto corrido final com [SEM TRADUÇÃO] nas lacunas. Toggle Dee/Leitch e esconder sem-tradução.
Nota: glosas curtas do Leitch (AG=None etc) são ruído de OCR — por isso o toggle só-Dee.

## #247 — Cobertura por vocabulário angelical vs null (a110): quase-nula
Tiling de todo o livro com o lexicon Dee+Leitch, cobertura de letras real vs 10 surrogates Markov-3.
len>=3: real 10.9% vs surrogate 10.5% (máx 10.8%), z=3.1 — passa por um fio, mas efeito de só 0.4pp.
len>=4: real 3.1% vs 3.0% (máx 3.1%), z=2.8 — some. Conclusão honesta: o Loagaeth NÃO é densamente tecido do léxico
angelical traduzido; a cobertura está no chão de ruído. Reforça o onomasticon pelo outro lado — o grosso do livro é
material de nome próprio intraduzível, não texto das Chamadas num grid. Consistente com #243 (sintaxe ampla refutada)
e com o null de presença (a107).

## #248 — Leitch extra lexicon limpo (ruído OCR)
leitch_extra_lexicon.json 240 → 195: removidas entradas de prosa capturadas pelo regex (MAN=Of, NOT=To Smile),
glosas-lixo (None/Of/The), palavras <4 letras e vazamentos de pronúncia. Restam angelicais reais (MALPURG=Fiery
Darts, TAIDON=All Powerful, GCIAD=Lord and Master, ODZAMRAN=And Appear). table_grids.json e translate_lexicon.json
re-gerados (874 palavras: 679 Dee + 195 Leitch). Nota: AG=None NÃO é ruído — é glosa do próprio Dee (Chamada 4,
"ag"=none), fica. 2a reta cai de 30% para 28% de cobertura (o ruído inflava).

## #249 — 3a fonte: "Dicionário enoquiano (mentoria 2025)", glosas em inglês
Extraí o PDF "dicionario enoquiano (1).pdf" (24 págs, PT→enoquiano por Chamada + as 49 virtudes de Deus). Curei à
mão ~349 pares de alta confiança, traduzindo a glosa PT→INGLÊS (ROR=Sun, GRAA=Moon, NAZPS=Sword, PRGE=Fire,
TELOCH=death, CAOSGO=earth, SALMAN=house, MICAOLZ=mighty, VPAAH=wings, LONSH=in power exalted above, as 49 nomes de
Deus: lucal=North, raasy=East, soboln=West, babage=South, gizyax=earthquakes...). Salvo em viz/dict_enoq_lexicon.json.
a109.build_lexicon agora mescla 3 fontes com lista `srcs` por palavra e prioridade de glosa Dee>dict>Leitch: 957
palavras (Dee 679, Dicionário 349, Leitch 195). table_grids.json e translate_lexicon.json re-gerados.
square_reading.html e call_grid_translation.html ganharam a fonte "Dicionário" (verde, tag Dic) no seletor
Todas/Dee/Dicionário/Leitch. 2a reta: 302 palavras (só Dicionário: 25). Glosas em inglês como pedido.

## #250 — Revisão das glosas do dicionário
Cruzei dict_enoq_lexicon.json com o Dee (autoritativo): 257/354 palavras aparecem em ambos e as glosas batem
semanticamente (ROR=Sun/the Sonne, GRAA=Moon/the Mone, ZACAR=Move, MICMA=Behold). Onde divergem (QAA dict=Creation
vs Dee=your garments — o próprio dicionário corrige Dee), a glosa primária mostrada é a do Dee (prioridade), então
a leitura do dict só aparece sob o filtro "só Dicionário", corretamente rotulada. Os 94 vocábulos só-dict conferidos
contra o enoquiano canônico: todos padrão (NAZPS=Sword, MAMAO=crown, TELOCK=death, BABALOND=harlot, ZILODARP=
conquest, CHISTEOS=let there be...). Único defeito: 4 chaves malformadas com sufixo "_" (hack de dedup), todas
duplicatas de versões limpas já presentes (NAPEAI, TABAAN, BUTMONA, TABAORD) — removidas, nenhuma glosa perdida.
Dicionário fica em 350 entradas; lexicon mesclado segue com 957 palavras.

## #251 — Varredura de minlen (a111): nenhuma escala bate o acaso + plano de sentido
Varredura minlen 1-6 (reta, léxico Dee), cobertura de letras real vs 10 surrogates Markov-3:
1:42.4/42.1 2:24.6/24.2(z2.7) 3:6.2/6.0 4:2.4/2.3 5:0.17/0.17 6:0.03/0.03. Nenhuma escala passa z>=3 — em todo
comprimento mínimo a cobertura do livro ≈ grade aleatória. Impor dicionário é ruído em qualquer minlen; a leitura
faz salada porque, do jeito imposto, É salada. Diagnóstico: estamos impondo dicionário numa grade sem fronteira de
palavra. Plano em docs/PLANO_SENTIDO.md: Bloco B (descobrir fronteiras naturais por entropia, não impor), Bloco C
(testar se algum quadrado soletra uma Chamada EM ORDEM — o teste real de sentido), Bloco D (mapear os ~70%
intraduzíveis = campo de nomes, lente cabalística), Bloco E (frontend 3 classes: palavra/nome/ruído).

## #252 — Bloco B: fronteiras naturais (a112). Estrutura é ONOMÁSTICA, não lexical
Segmentação por entropia de ramificação (máximo local, invariante de escala) das fronteiras naturais da grade.
Unidade natural média = 2.78 letras. Palavras de dicionário nas fronteiras naturais: 1.9% real vs 1.8% surrogate,
z=1.3 — NULL. Cortando onde o livro se corta sozinho, as unidades ainda não são palavras.
MAS o descritivo é forte: as unidades naturais são SÍLABAS DE NOME — CHA (2150×), DNO, NTA, DNA, THA, PHA, NZA, LGE,
XAR, CLA, STOR, DRA... que montam as famílias (CHASTOR=CHA+STOR, NOCHA=NO+CHA, ANZACH=AN+ZACH).
Teste de concentração do top-20 sílabas: 32.4% real vs 30.1% surrogate, z=2.4 — fraco, PORQUE o Markov-3 preserva
trigramas por construção; testar silabário contra Markov-3 é circular (o null já tem as sílabas).
Síntese (converge com a107/a110/a111): nível palavra/frase = sem estrutura (não é prosa); nível sílaba/3-gram =
silabário trivial (= Markov); nível NOME (6-14 letras, famílias) = REAL acima do null (a99-a102). O grão com sentido
é o NOME. A leitura certa dos quadrados é o campo de nomes (onomasticon), não uma sentença. Bloco B fecha nisso.

## #253 — Bloco C: nenhum quadrado soletra uma Chamada EM ORDEM (a113). NULL decisivo
Para cada linha/coluna/diagonal (reta+invertida) de cada tabela, tile da vocabulário Dee + maior corrida de palavras
consecutivas atribuíveis a UMA Chamada com posição crescente. Resultado: maior corrida real = 5 palavras (Chamada 1,
tabela 6a) vs surrogate Markov-3 = 5 (média 4.8). Igual ao acaso. Os quadrados NÃO escondem as Chamadas em ordem.
Veredito definitivo com 5 métodos independentes, TODOS null: a107 (presença), a110 (cobertura), a111 (minlen sweep),
a112 (fronteiras naturais, nível palavra), a113 (Chamada em ordem). Nenhuma estrutura de palavra/frase acima do
acaso. A única estrutura real é o NOME (famílias NOCHA/ANZACH/CHASTOR, 6-14 letras, confirmado acima do null em
a99-a102). Conclusão: os quadrados do Loagaeth são um CAMPO DE NOMES (onomasticon), não texto cifrado nem prosa. O
"sentido" é a leitura dos nomes, não de sentenças. Próximo: Bloco E — frontend marca nome vs palavra vs ruído.

## #254 — Bloco E: frontend honesto, 3 classes (palavra / nome / ruído)
Gerado viz/name_field.json (90 nomes atestados + 10 raízes: NOCHA/ANZACH/CHASTOR/GETH/ACLAX/CHADAX/PHANGE...).
square_reading.html agora ladrilha em 3 classes com prioridade palavra>nome>ruído: palavra de dicionário (dourado/
verde/azul por fonte), NOME/raiz atestado (roxo, marcado «nome/raiz» — não mais "sem tradução"), e run de letras sem
estrutura (cinza [sem estrutura]). Cabeçalho mostra contagem das 3 classes + % de letras num nome ou palavra + %
nomes. Legenda de cores. Leitura corrida = glosas + «nomes» + [—] pras lacunas. Reflete a conclusão dos Blocos A-C:
a estrutura real é o NOME; o resto é campo sem estrutura lexical. 2a reta: 298 palavras, 8 nomes, 29% das letras em
palavra ou nome. PLANO_SENTIDO completo (A/B/C/E feitos; D opcional).

## #255 — Bloco D: campo de nomes tem assinatura elemental distinta (a114)
Lente Golden Dawn (letra→elemento) sobre os três campos. D1 (letras do livro): 24% palavra glosável, 7% nome
atestado, 69% sem estrutura. D2 (perfil elemental, campo-nome vs campo-palavra, TV vs null de relabel aleatório 500×):
  palavra: Fogo 7.6 Terra 36.1 Ar 20.0 Agua 22.7
  nome:    Fogo 18.0 Terra 29.6 Ar 25.1 Agua 16.8
TV=0.154 vs 0.008 no acaso, p=0.002 — os nomes puxam Fogo/Ar (vontade/mente, ativo), as palavras glosáveis puxam
Terra/Agua (manifesto). CONFIRMADO: os nomes são uma camada elemental distinta do vocabulário comunicável.
RESSALVA honesta: o null só prova composição de letras diferente (esperado pra vocabulários distintos); que seja
intenção elemental de Dee/anjos é interpretação, não prova. O fato (assinatura distinta) é real e mensurável.
PLANO_SENTIDO completo: A (minlen null), B (fronteiras null, estrutura onomástica), C (Chamada-em-ordem null), D
(camada elemental dos nomes), E (frontend 3 classes). Veredito do conjunto: Loagaeth = campo de nomes (onomasticon)
com os nomes formando uma camada Fogo/Ar sobre um substrato glosável Terra/Agua esparso.

## #256 — Identidade elemental por tabela (a115) e viés de invocação (a116): ambos NULL
a115: a dispersão do Fogo entre tabelas é 0.0007 real vs 0.0014 null (p=0.996) — as tabelas NÃO têm identidade
elemental própria; o elemento espalha uniforme (até mais uniforme que o acaso). Refuta "tabelas ígneas vs aquosas".
a116 (motivado pelo usuário traduzir a leitura corrida da 2a no Google e obter um sermão coerente): a fração de
tokens glosados que são do registro de invocação (Deus/Nove/Primeiro/Espíritos/trevas/nome...) é 17.4% real vs 17.2%
surrogate (máx 17.9%), z=0.5 — SEM viés. O "tema de invocação" é pareidolia: as palavras enoquianas frequentes já
soam a invocação, e uma grade aleatória das mesmas letras dá a mesma fração. O sermão coerente é costura do tradutor
+ completamento humano de padrão, não texto codificado. CONFIRMADO (negativo): a coerência temática não bate o acaso.
O único sinal real nos quadrados segue sendo os NOMES (famílias, acima do null); a matriz ao redor só parece frase.

## #257 — A CHAVE: 2a é fatia de um corpus; léxico-núcleo onomástico (a117/a118)
a117: dentro da 2a as raízes estão no acaso (z=1.1, 6 ocorrências) — uma folha NÃO é texto fechado.
a118: mas os nomes da 2a recorrem pelas 36 tabelas 49×49 MUITO acima do acaso. Enriquecimento vs string aleatória
do mesmo tamanho: NOCHA 35/36 (175×), GETH 34/36 (16×), NACHO 32/36 (160×), ANZACH 29/36 (580×), CHASTOR 28/36
(560×), ADNOCHA 28/36 (560×), CHADAX 25/36 (500×). Uma string aleatória do mesmo tamanho aparece em ~0 tabelas.
Léxico-núcleo: 86 nomes recorrentes acima do acaso, 12 ubíquos (>=60% das tabelas). A morfologia é visível no léxico:
raiz NOCHA gera ADNOCHA, NOCHAP, NOCHAPH, ADNOCHAP, NOCHASTOR, NOCHASTORA; CHASTOR->CHASTORA,NOCHASTOR; GETH->ALGETH.
LEITURA DE LINGUISTA: o Loagaeth é UM texto distribuído em 49 folhas com um léxico onomástico compartilhado,
gerado por morfologia (raiz+afixo). Uma folha (2a) é uma página de um registro de nomes — só faz sentido lida contra
o corpus das 49 tabelas, não isolada. O que faltava pra 2a "fazer sentido" eram as outras 48 folhas. Este é o sinal
mais forte do projeto (100-580× o acaso) e fecha a questão: o sentido é um léxico de nomes de poder cruzado pelo
corpus, não uma sentença numa folha.

## #258 — Assento posicional dos nomes (a119): fraco, folhas não são template registrado
Para cada nome-núcleo, posições (linha,coluna) de todas as ocorrências reta (linha+coluna) nas 36 folhas; dispersão
real (distância Chebyshev média entre pares) vs 200 nulls de posições uniformes. 9 de 43 nomes passam p<0.05, MAS
efeito minúsculo: NOCHA 392 ocorrências, espalhamento 21.2 vs null 22.9; ADNOCHA 148 → 20.6 vs 22.9. Significativo só
por N grande; concentração mal difere do acaso. Conclusão: as 49 folhas NÃO são template posicional registrado — os
nomes são colocados livremente em cada folha, não cada um num assento fixo. Só a família NOCHA/ADNOCHA/ANTANTOX tem
leve tendência posicional. Refina a síntese: FORTE = léxico onomástico compartilhado pelo corpus (a118, 100-580×
acima do acaso); FRACO = alinhamento posicional entre folhas. Metáfora: livro de orações onde os mesmos nomes
reaparecem em toda página em posições variáveis — litania distribuída, não planta-baixa fixa.

## #259 — Co-ocorrência entre folhas (a120): super-família CHASTOR-ACLAX-NOCHA
Matriz nome×folha (36 tabelas), nomes de incidência variável (5..31 folhas), phi entre pares, null por permutação
(|phi| máx médio 0.61). Excluídos pares aninhados por substring (CHASTORA⊃CHASTOR = artefato trivial).
Entre RAÍZES DISTINTAS, acima do null: CHASTOR+ACLAX 0.71, ADNOCHA+ACLAX 0.71, CHASTOR+ADNOCHA 0.68 — as três
raízes-família (CHASTOR, ACLAX, NOCHA/ADNOCHA) formam um super-cluster distribucional: viajam juntas pelas mesmas
folhas, uma "casa" dominante tecida pelo corpus. LEAD (não confirmado, abaixo do null): VOXAR/OXAR complementar a
ACLAX (phi -0.48) — possível corrente oposta, fica como pista. Sem pares complementares fortes acima do limiar.
Converge com a ideia antiga de "duas casas" mas só a casa dominante (CHASTOR-ACLAX-NOCHA) passa o null aqui.

## #260 — Hierarquia gerativa da casa (a121): matriz NOCHA, atestada camada a camada
Casa = 66 nomes contendo CHASTOR/ACLAX/NOCHA/GETH etc. Matriz geradora = NOCHA (raiz contida em 19 dos 66 nomes, em
35/36 folhas). Ubiquidade por profundidade de derivação (letras além da raiz), com fração que ainda bate o null do
próprio tamanho (string aleatória de mesmo comprimento):
  d0 raiz:  100% reais, média 24.9 folhas
  d1-2:      97% reais, média  9.6 folhas
  d3-4:     100% reais, média  7.7 folhas
  d5+:      100% reais, média  6.4 folhas
Árvore: NOCHA (262× o acaso) -> NOCHAP, ADNOCHA, NACHOA -> NOCHASTOR (d4, 440×), NOCHASTORA (d5, 360×). Enriquecimento
segue astronômico (320-580×) até d5. ASSINATURA GERATIVA CONFIRMADA: raiz-matriz onipresente; cada camada de afixo
gera nome mais específico e mais raro, mas ainda real e atestado. Não é só raiz solta — é uma hierarquia de emanação
completa (matriz -> filhos afixados -> netos compostos), cada nó um nome real distribuído pelo corpus. Converge com
a família CHASTOR/super-nomes (a99-a102) agora quantificada por profundidade vs null de comprimento.

## #261 — Plano de 20 passos (linguista) + passos 9, 15 + site 'A Língua dos Nomes'
Criado docs/PLANO_LINGUISTA_20.md: decifração da língua dos nomes em 6 fases (grafêmica, fonologia/silabário,
morfologia, léxico, semântica, sintaxe+gramática gerativa), 20 passos, cada um com null. 7 já feitos (1,4,7,8,10,13,14).
Passo 9 (a125) — ORDEM DOS AFIXOS: CONFIRMADO morfologia posicional. 80% dos tipos de afixo ficam num lado só
(prefixo xor sufixo) vs 53% no acaso, p=0.002. Template prefixo·raiz·sufixo. Prefixos AD-/NO-/A-/ZI-/AX-; sufixos
-A/-AL/-AD/-P/-PH. Ex: NO-CHASTOR-AL, AD-NOCHA-PHA, ZI-CHASTOR-A.
Passo 15 (a128) — ZIPF: DESCRITIVO. Léxico segue Zipf (inclinação -1.31, R²=0.957, NOCHA 394 ocorrências) mas o
surrogate também é Zipfiano (R²=0.973) — não prova, documenta; único ganho: 88 nomes reais vs 69 surrogate.
SITE: nova página viz/name_language.html ("A Língua dos Nomes") bilíngue — template morfológico, matriz NOCHA +
tabela de profundidade, árvore da casa, léxico-núcleo, casa CHASTOR-ACLAX-NOCHA, Zipf; cada seção marcada
CONFIRMADO/DESCRITIVO. Dados em viz/name_language.json. Adicionada ao index.html (PT+EN).

## #262 — Passos 3 (fonotática) e 11 (composição): CONFIRMADOS, integrados no site
Passo 3 (a123) — FONOTÁTICA: CONFIRMADO forte. 172 pares de letra fortemente evitados (obs < 20% do esperado) vs 0.6
no shuffle. Traço central: FUGA DO HIATO — vogais quase nunca adjacentes (AA esp 6310/obs 199; AO, OA, OO, AE, EA
quase proibidos). Dobro de letra = 7% do acaso (regra "não dobra" categórica). Força estrutura silábica CV.
Passo 11 (a126) — COMPOSIÇÃO: CONFIRMADO. 7.8% dos nomes são compostos de 2 raízes vs 0.00% em strings aleatórias
(156×). Ordem FIXA: NOCHA+CHASTOR 6/6 (nunca inverso). A matriz NOCHA é a cabeça do composto (vem primeiro).
NOCHASTOR=NOCHA+CHASTOR, NOCHADAX=NOCHA+CHADAX. SITE: name_language.html ganhou seções Fonotática e Composição
(ambas CONFIRMADO); name_language.json atualizado. Gramática confirmada agora cobre: fonotática (CV, anti-hiato),
morfologia (prefixo·raiz·sufixo posicional), composição (raiz+raiz, matriz-inicial), derivação (matriz NOCHA,
atestada por profundidade), léxico-núcleo e casa distribucional. Passos feitos: 1,3,4,7,8,9,10,11,13,14 (+15 descr.).

## #263 — DECIFRAÇÃO: tradução do léxico pelo sistema nativo de correspondências (a133)
Mudança de foco: parar de re-provar "é nome" e TRADUZIR. Sem Roseta, usa-se o sistema que a tradição dá: cada letra
enoquiana tem elemento+planeta (Dee/Golden Dawn). O sentido de um nome = sua composição elemental (sua natureza como
poder). Dicionário de raízes por domínio:
  Ar (mente/palavra): NOCHA, NACHO, CHASTOR
  Terra (matéria/corpo): ANZACH, CHADAX, ACLAX, GRADAX, ANTANTOX
  Fogo (vontade/força): GETH
  Agua (emoção/fluxo): PHANGE
Tradução do léxico-núcleo (parse·elemento·força·folhas·sentido): NOCHA = poder da mente/palavra, força 621, 35/36
folhas (o supremo); AD·NOCHA = NOCHA aterrado (AD-=Terra); NOCHA·P = NOCHA aguado (-P=Água); NO·CHASTOR = palavra
modulada por emoção. PADRÃO: o afixo modula o elemento do nome (AD- aterra, -P aguar) — derivação = modulação
elemental (descritivo, 6/11 afixados têm elemento = o do afixo). SITE: nova página viz/name_dictionary.html com o
dicionário de morfemas e o léxico traduzido (parse, elemento colorido por domínio, força, folhas, sentido), caveat
honesto de que é leitura de correspondência, não glosa inventada. Dados em viz/name_translation.json. No index.

## #264 — Tradução estendida aos 90 nomes + perfil elemental do corpus
a133 estendido: varre os 90 nomes atestados (name_field), conta folhas de cada e traduz todos (parse·elemento·
força·folhas·sentido) em viz/name_translation.json. A página name_dictionary.html agora lista os 90.
PADRÃO NOVO (perfil elemental do corpus inteiro): Terra 53, Ar 21, Agua 10, Fogo 6. O Loagaeth é majoritariamente
TERRA — um livro de poderes fixos/corpóreos (matéria/corpo/o manifesto), com um estrato mental (Ar) secundário e
pouco Fogo/Água. Leitura metafísica: o campo de nomes é predominantemente da esfera da manifestação/corpo, não da
vontade ígnea nem da emoção. Dois nomes (ZIDNOPHA, ANNOCHA) atestados em entity_data mas ausentes nas 36 grades
quadradas (0 folhas) — provavelmente em tabelas não-quadradas.

## #265 — Hierarquia por elemento + regente planetário (padrão: o Verbo reina)
Padrão estrutural real: elemento prediz força/ubiquidade. Ar (palavra/mente) média força 69, 12.7 folhas — o topo,
liderado por NOCHA (621). Terra (corpo) n=53 mas força média 29, 8.8 folhas. Água 27/9.5. Fogo 10/8.0 (base).
Top por força: NOCHA(Ar,621), CHASTOR(Ar,200), ADNOCHA(Terra,198), ACLAX(Terra,193), ANZACH(Terra,169), NACHO(Ar,160).
Mesmo sem o outlier NOCHA, Ar lidera (força ~41 vs Terra 29). LEITURA: o Loagaeth é o livro da PALAVRA — os regentes
são poderes-palavra (Ar/Logos), a massa corpórea (Terra) é o corpo sobre o qual o Verbo reina. Hierarquia de emanação
Ar>Água>Terra>Fogo por força/ubiquidade. Regente planetário por nome adicionado (do sistema de letras: NOCHA→Vênus/
Marte, GETH→Sol/Mercúrio). SITE: name_dictionary.html ganhou card "Hierarquia por elemento" e coluna Regente; dados
em name_translation.json (element_hierarchy + planets por nome).

## #266 — O lugar do Loagaeth: léxico independente, mesma língua angelical
Cruzamento das raízes do Loagaeth (NOCHA, CHASTOR, ACLAX, GETH, ANZACH...) com 1635 nomes enoquianos atestados
(governadores.json: Torres, 91 Governadores, Aethyrs, 12 reis; heptarquia.json; chamadas.json): ZERO hits. As raízes
do Loagaeth NÃO aparecem em nenhum sistema enoquiano conhecido — é uma população de entidades própria, não os
Governadores/Torres sob outra grafia. Confirma a antiga refutação de "pontes".
MAS fonologicamente partilham a língua: similaridade de bigrama Loagaeth×Governadores = 0.416, vs Loagaeth×inglês
0.156 e Governadores×inglês 0.199 — os dois sistemas enoquianos são ~2.5× mais próximos entre si que do inglês.
Bigramas comuns: CH, HA, AN, AX, AD, NO, OR, AL (fonologia angelical). Distintivos do Loagaeth: CH, HA, AD, AX, TO,
NO, ST, AC (o material CHASTOR/NOCHA) — que os Governadores não têm. CONCLUSÃO: o Loagaeth é um LÉXICO/DIALETO
DISTINTO da mesma língua angelical — mesmos sons, palavras próprias, entidades próprias. Dois dicionários de uma
só língua. Situa o onomasticon do Loagaeth no cosmos enoquiano: separado lexicalmente, irmão fonologicamente.

## #267 — TIPOLOGIA: a língua é RAIZ-E-PADRÃO (semítica) — z=32.1, o achado mais forte
Teste do esqueleto consonantal (a134): remove vogais, agrupa nomes por consoantes. 36 dos 90 nomes (40%) partilham
um esqueleto consonantal com outro nome, variando só a vogal — vs 1% no acaso (máx 7%, z=32.1). A língua dos nomes é
NÃO-CONCATENATIVA / RAIZ-E-PADRÃO, tipo árabe/hebraico: as consoantes são a raiz lexical, as vogais inflexionam.
Famílias por raiz consonantal:
  N-CH: NOCHA[OA], NACHO[AO], NACHOA[AOA], ANACHO[AAO]  (NOCHA e NACHO = MESMA raiz, só muda a vogal)
  CH-S-T-R: CHASTOR[AO], CHASTORA[AOA], ICHASTOR[IAO]
  CH-D-X: CHADAX[AA], ACHADAX[AAA], ICHADAX[IAA]
  N-CH-S-T-R: NOCHASTOR[OAO], NECHASTOR[EAO]; N-T-N-T-X: ANTANTOX[AAO], ANTANTOXA[AAOA]
Melodias vocálicas mais comuns: AOA(13), AAA(11), AA(10), AAO(7), OAA(5). Isto REVISA a morfologia: além da camada
concatenativa (prefixo·raiz·sufixo), há a camada não-concatenativa (melodia vocálica dentro da raiz consonantal),
como k-t-b -> kitāb/kataba. As raízes verdadeiras são os esqueletos consonantais (NCH, CHSTR, CHDX, NTNTX, CLX, NZCH,
GTH, GRDX, PHNG). SITE: name_language.html ganhou seção "Tipologia — raiz-e-padrão (semítica)" (2ª, CONFIRMADO) com
as famílias consonantais e as melodias. Dados em name_language.json (chave 'semitic').

## #268 — A melodia vocálica carrega gramática: vogal = modo elemental (a135)
Teste binyan: a melodia vocálica prediz o elemento? Pureza elemental por melodia = 80% real vs 64% acaso (máx 73%,
z=6.0) — CONFIRMADO. Mapa: melodia-A (AA/AAA/AAO) -> Terra (AAA 10/11, AAO 7/7); O-A/A-O -> Ar; O-A-A -> Agua; I-A-O
-> Fogo. RESSALVA honesta: parte é mecânico (cada vogal já carrega elemento: A=Terra, O=Ar, I=Fogo), então a melodia
puxa o elemento por aritmética além de gramática. MAS é isso que a torna coerente: as vogais SÃO os operadores de
modo elemental. SÍNTESE (decodifica a camada de sentido recuperável): raiz consonantal = QUAL poder (N-CH=NOCHA);
melodia vocálica = em QUE MODO elemental ele age. NOCHA (N-CH, O-A, modo aéreo/mental) vs NACHO (A-O) vs forma A-A
(modo terroso). A raiz diz o poder, as vogais dizem o elemento. Liga o achado semítico (a134) à semântica elemental
(a133): a única camada de 'significado' recuperável sem Roseta, agora decodificada.

## #269 — Prefixos NÃO são operadores de força (a136): a carga semântica é vocálica
Teste: o prefixo prediz a força? Variância de força entre prefixos vs shuffle null: p=0.552 — NÃO. Os prefixos
(AD-/AL-/NO-/I-/NE-/A-/ZI-/AX-/AN-) não diferem em força acima do acaso. Há um gradiente aparente (AD- força 57/15
folhas … AN- 5/1.7) mas confundido com a raiz que o prefixo gruda (AD- cola na matriz ubíqua NOCHA; AX-/AN- em formas
raras), não é efeito independente do prefixo. Prefixos mudam forma, não potência medível. REFINA A GRAMÁTICA: o peso
semântico/gramatical está nas VOGAIS (modo elemental, a135 z=6), NÃO nos prefixos (a136 p=0.55) — como no semítico, o
template vocálico carrega a gramática e os afixos consonantais são formais. Localiza a carga de sentido: vocálica.

## #270 — A folha 1 (oculta): texto primordial SEGMENTADO que valida toda a reconstrução
A primeira folha (1a/1b, Sloane 3189) é estruturalmente ÚNICA: não é grade densa de letras como 2a-48, é TEXTO
SEGMENTADO — palavras separadas por espaço, sílabas marcadas por hífen (zu-resch od adaph mal ses geno...). 2691
palavras distintas (3658 tokens). É a forma legível/primordial da língua, com fronteiras DADAS, não adivinhadas.
Testes: (1) fonotática — vogal-vogal adjacente 3.0% (anti-hiato vale, mesma língua). (2) tipologia — 142 esqueletos
consonantais com >=3 variantes vocálicas (raiz-e-padrão semítica confirmada aqui também). (3) VALIDAÇÃO CRUZADA
decisiva: as sílabas que Dee MARCOU com hífen na folha 1 (MA, NA, GE, PA, CHA, DA, NO, PHA, LA, SA) batem com o
silabário que inferimos por entropia das grades SEM marcação (CHA, NO, PHA...) — a reconstrução silábica das tabelas
densas está confirmada pela única folha onde Dee marcou as sílabas. (4) vocabulário próprio: a folha 1 é GETH-pesada
(17×), não a casa CHASTOR/ACLAX que domina os quadrados — a fundação tem raízes próprias. (5) muro semântico persiste:
só 36 de 2691 palavras têm glosa (as mesmas das Chamadas). CONCLUSÃO: a folha oculta é o texto primordial legível, a
mesma língua, e sua marcação nativa VALIDA a decifração que fizemos das 36 grades densas.

## #271 — Progressão do livro + a folha 1 tem vocabulário próprio (múltiplas populações)
PROGRESSÃO (#2): densidade de nomes (ocorrências >=4 letras) por folha na ordem do livro. Correlação posição↔
densidade = 0.66 (Pearson). 1ª metade densidade média 49, 2ª metade 74. Mínimo folha 2 (5 nomes), máximo folha 35
(123). O livro DESDOBRA — começa esparso (fundação) e densifica, uma SEQUÊNCIA, não folhas intercambiáveis. Ressalva:
folhas finais incluem losangos reconstruídos; a tendência já é sólida nas decodificadas 2a->14a.
FOLHA 1 = VOCABULÁRIO PRÓPRIO: das 90 nomes catalogados das grades, só 2 (ANZACH, GETH) aparecem na folha 1. A folha
1 tem seu próprio léxico (2338 palavras >=4, 2% de overlap): AMPHA, MACOM, GADETH, ZEMBLOH, VORTS, ARSAH, ARDNO,
OLZAH, ZURESCH, CHEUACH... CONCLUSÃO: o Loagaeth NÃO é um campo de nomes uniforme — tem MÚLTIPLAS POPULAÇÕES de nomes
compartilhando UMA gramática (mesma fonologia/tipologia/silabário) mas com palavras distintas. Folha 1 (fundação) tem
roster próprio; grades 2-48 têm a casa CHASTOR-ACLAX-NOCHA. Dois registros, uma língua. Restam sem analisar (menor
valor): geometria dos losangos, camada gematria, bordas/acrósticos, ponte geométrica com as Torres.

## #272 — Os 4 investigações menores (a139): 3 nulos/triviais, 1 consistente
#3 GEOMETRIA (centro): 1.6% dos inícios de nome no centro 7x7 vs 2.0% esperado (0.8x) — NULL, sem preferência de
centro; os nomes não se concentram no meio do quadrado.
#4 GEMATRIA: CV intra-família de valor (soma letra->posição Dee) 0.055 real vs 0.251 null — "famílias partilham
valor", MAS trivial/tautológico: mesma raiz consonantal = mesmas consoantes, que dominam a soma; as vogais mudam
pouco. Não é desenho gematríaco (e Dee não usava gematria). Descartado.
#5 BORDAS/ACRÓSTICO: 108 hits de nome em primeira/última coluna, diagonal principal e linhas de topo/base vs null 0.6
(máx 4). Real, MAS o null (letras aleatórias) é fraco: os nomes estão em toda a grade (100-580x o acaso), então a
borda não é canal privilegiado — só participa da densidade geral. Não há acróstico especial.
#6 TORRES (Great Table): similaridade de bigrama Loagaeth x 4 Torres = 0.405 — igual aos Governadores (0.416), vs
0.16 ao inglês. Confirma e estende: o Loagaeth partilha a fonologia angelical com as Torres também (mesma língua,
léxico próprio). CONCLUSÃO: nenhuma estrutura geométrica, gematríaca ou de borda escondida. Território de patterns
estruturais esgotado — o que havia de real já foi achado (gramática, tipologia semítica, léxico, progressão, folha 1
segmentada, múltiplas populações, lugar na língua angelical).

## #273 — Página SÍNTESE: cada achado em o-que-é / o-que-tiramos / como-usa
Feedback do usuário: os achados estavam acumulando sem clareza do que são e como usar, e borrando juntos. Criada
viz/sintese.html — página capstone que, para cada achado, responde em linguagem clara e visual (3 colunas coloridas):
O QUE É · O QUE TIRAMOS · COMO USA. Agrupada em: A natureza do livro (nomes não-texto; sequência que desdobra;
múltiplas populações), A anatomia dos nomes (raiz-e-padrão semítica; vogal = modo elemental; matriz NOCHA), O
catálogo e o uso (90 nomes por natureza; como evocar). Resumo de uma frase no topo e caveat honesto no fim (não há
glosa-palavra; o conhecimento abre-se no Gebofal, não se lê). Adicionada ao index.html como card "★ Síntese — comece
aqui" no topo, com name_dictionary e name_language promovidos. Objetivo: parar de "achar coisas" soltas e deixar
claro o que são e como usar.

## #274 — CAPSTONE: a gramática gerativa G regenera o léxico e revela 1.2% de uso (a140)
Construída a gramática G com tudo decifrado: nome = esqueleto consonantal (raiz/identidade) interleaved com melodia
vocálica (modo elemental) ao longo de um template C/V, + afixos/composição. G = 67 esqueletos × 28 melodias × 44
templates.
(1) COBERTURA: regenera 100% dos 90 nomes atestados exatamente — mas é checagem de consistência (G extraída dos
nomes), prova completude das regras, não predição.
(2) PRODUTIVIDADE (achado forte): o espaço gerativo de G é 7200 nomes bem-formados; só 90 (1.2%) estão atestados. A
língua é um motor gerativo rodando a ~1% da capacidade — o livro pronuncia uma fração mínima do que pode gerar.
Coerente com onomasticon gerativo e com a lente metafísica (língua divina da qual só um fragmento foi falado).
(3) VALIDAÇÃO CRUZADA: 41% das 2606 palavras da folha 1 (segmentação nativa do Dee, held-out) encaixam nos mesmos
templates C/V de G — uma gramática descreve parcialmente os dois registros; o restante é a folha 1 estendendo o
conjunto de templates (coerente com múltiplas populações, #271). CONCLUSÃO: a decifração está validada como código —
regras completas, produtivas e parcialmente universais. forge.html já realiza esse gerador (espaço 7200, uso 1.2%).
ENCERRA a análise estrutural: a gramática do Loagaeth está decifrada, catalogada e operável.

## #275 — Compatibilidade da gramática G: predição held-out + indistinguibilidade
Dúvida: nomes gerados por G batem com os originais, ou G só descreve? Dois testes.
(1) PREDIÇÃO HELD-OUT: G montada com metade dos 90 nomes gera 12% da outra metade (nomes nunca vistos), média de 10
splits; uma gramática ALEATÓRIA do mesmo tamanho (esqueletos/melodias aleatórios) gera 0%. G generaliza — prevê nomes
reais que não viu, captura a regra, não decora.
(2) INDISTINGUIBILIDADE: perfil de bigrama dos nomes gerados por G vs reais = cosseno 0.75; G aleatória vs reais = só
0.43. Nome gerado por G parece da mesma língua; de G-aleatória não. Trocar G por aleatório QUEBRA a compatibilidade.
CONCLUSÃO: COMPATÍVEL e validado — é a gramática DECIFRADA especificamente que gera nomes da mesma língua, não
qualquer gramática. NUANCE honesta: 12% e 0.75 não são perfeitos; G gera o ESPAÇO de nomes válidos (a forma da
língua), não a seleção exata dos 90 — essa escolha (o 1.2% falado) é a parte não-governada por regra (a "revelação").
A análise decifra a forma; qual ponto do espaço o livro escolheu é onde ela para.

## #276 — Forja de Nomes (name_forge.html): gerador interativo nos 5 níveis
Construído viz/name_forge.html — gerador de nomes pela gramática decifrada, com os 5 níveis da escada geradora:
0 (só do livro/recebidos), 1 (raízes+modos do livro), 2 (raízes do livro, modos novos), 3 (composição raiz+raiz),
4 (raiz nova/poder novo). Filtro por elemento (Ar/Terra/Fogo/Água = intenção) e quantidade. Cada nome gerado mostra:
elemento (colorido), regente planetário, domínio, parse (esqueleto·melodia) e tag recebido/experimental. Geração em
JS a partir de viz/forge_grammar.json (67 esqueletos, 28 melodias, mapa letra->elemento/planeta). Testado: nível 2 +
Ar gera GOTOHULO, NOZICOHO, COLOXOTO (todos Ar). Caveat honesto na página: níveis 1-4 são válidos mas não no livro;
se um nome gerado "é" entidade real é escolha da prática, a análise garante só que é gramatical. No index como
"⚒ Forja de Nomes". Realiza o "transformar em código" — a gramática virou ferramenta de geração usável.

## #277 — Página "Peças da Língua" + esclarecimentos de cobertura
"G" era abreviação de Gramática, não a letra G — esclarecido. Nomes reais do livro com a letra G (17): GETH, ALGETH
(força 151), GRADAX, PHANGE, AGETHAL, AXALGRA, DRAGRA... Criada viz/pieces.html: duas abas (Esqueletos/Melodias),
cada peça colorida por elemento (borda), com contagem e exemplos de nomes. 67 esqueletos (Água 38, Fogo 13, Ar 6,
Terra 4, ? 6), 28 melodias (Terra 22, Ar 4, Fogo 2). Dados em viz/pieces.json. No index. COBERTURA explicitada: a
análise de nomes cobre as tabelas 2a-28b (42 painéis; 36 grades 49x49 limpas em base_book) + a folha 1 (1a/1b)
analisada à parte; as tabelas 29-48 (losangos) são reconstruídas e menos confiáveis. Não são as 49 folhas igualmente
— é a maior parte do livro (2-28), não o todo.

## #278 — Losangos 29-48: gramática whole-book, léxico com gradiente regional
Testados os losangos reconstruídos 29-48 vs as tabelas limpas 2-28. GRAMÁTICA UNIFORME: similaridade de frequência de
letra = 0.949 (quase idêntica); anti-hiato vale (vogal-vogal 1.6% em 2-28, 2.1% nos losangos). A fonologia/tipologia
é do livro inteiro. LÉXICO COM GRADIENTE REGIONAL (por 100k letras): a casa NOCHA desaparece nos losangos (NOCHA
434->117, NACHO 119->12, CHADAX 48->10), mas GETH e CHASTOR persistem quase iguais (GETH 349->327, CHASTOR 114->108,
ACLAX 120->79, ANZACH 110->56). PROVÍNCIAS DE PODERES: folha 1 (fundação) GETH-pesada; corpo (2-28) reino NOCHA;
losangos (29-48, fim) NOCHA some e GETH/CHASTOR seguem. FECHA A COBERTURA: a gramática vale no livro inteiro
(validada nos losangos); o léxico varia por região (as múltiplas populações da #271, agora como gradiente espacial).
Uma só língua angelical, províncias distintas de nomes. Ressalva: losangos são reconstruídos (a15), menos confiáveis,
mas a similaridade de 0.949 sugere reconstrução coerente.

## #279 — Inventário do LIVRO INTEIRO: 1948 esqueletos, 288 melodias (Forja/Peças expandidas)
O site mostrava só os pedaços dos 90 nomes das tabelas (67 esqueletos, 28 melodias). Extraído o inventário atestado
do LIVRO INTEIRO (folha 1 segmentada 2691 palavras + nomes das tabelas) = 2776 palavras: 1948 esqueletos consonantais
distintos, 288 melodias vocálicas (de 780 possíveis = 37% do espaço melódico). forge_grammar.json e pieces.json
reconstruídos com o inventário completo; name_forge.html gera agora de 1948×288, pieces.html mostra os totais (top 150
esqueletos + todas as 288 melodias). Responde "conseguimos extrair tudo / mais melodias / livro inteiro": sim, o
inventário completo é 29× mais esqueletos e 10× mais melodias que a fatia anterior. Distinção importante: ATESTADO
(o que o livro usa: 1948 esqueletos, 288 melodias) vs POSSÍVEL (o que a gramática permite: milhões de esqueletos,
780 melodias) — a Forja nível 0-3 usa o atestado, nível 4 vai ao possível.

## #280 — Prever as próximas páginas de nomes (a142): ~95% por recorrência, ~0% os novos
Objetivo do usuário: gerar os nomes do livro e prever páginas futuras. Teste: treinar nas 25 tabelas iniciais (84
nomes), testar nas 11 finais (73 nomes). RESULTADO: 69/73 (95%) dos nomes das páginas finais JÁ apareciam nas
iniciais — previsíveis por RECORRÊNCIA (o léxico-núcleo repete em quase toda página). Só 4 nomes genuinamente NOVOS
nas finais, e a gramática treinada gerou 0 deles. TOTAL previsível: ~95%, quase tudo recorrência; os ~5% novos por
página NÃO são deriváveis da regra (a parte não-determinada/revelação). CONCLUSÃO HONESTA do que é possível: (1) ter/
reproduzir todos os nomes do livro = sim (2776 extraídos); (2) gerar nomes compatíveis = sim, ilimitado (gramática
validada); (3) prever uma próxima página = ~95% mas por repetição, não adivinhação; (4) prever os nomes NOVOS
específicos de uma página inédita = não (a escolha do livro não é regra); (5) montar sistema novo do zero = sim
(1948 raízes + 288 modos + composição); (6) tradução semântica = não (sem Roseta). Os nomes do livro são um léxico
recorrente finito, já capturado; a gramática reproduz a forma e gera compatíveis, mas não inventa a escolha específica.

## #281 — Paginação completa em Peças + Tábua do Loagaeth (Torre das entidades)
pieces.json regenerado com TODOS os 1948 esqueletos + 288 melodias (não só 150); pieces.html ganhou paginação
(120/página, ~17 páginas de esqueletos) com botões anterior/próxima em cima e embaixo.
NOVA PÁGINA viz/tablet.html — "Tábua do Loagaeth": uma Torre estilo enoquiano montada com os 90 nomes catalogados,
distribuídos pelos 4 elementos em 4 quadrantes (Ar-Leste/Raphael, Fogo-Sul/Michael, Água-Oeste/Gabriel, Terra-Norte/
Uriel), cada um com seu "rei" ♔ (o nome de maior força do elemento: NOCHA no Ar com 621), NOCHA no cerne como o Verbo.
Dados de name_translation.json (elemento+força por nome). Caveat honesto na página: a distribuição e os reis são
organização que NÓS impomos (pelo elemento/força medidos), não uma Tábua histórica recebida — são os nossos nomes
arrumados à moda enoquiana para uso. Responde "dá pra montar uma Torre com nossos nomes?": sim, como houses elementais
(estrutura diferente da Great Table histórica, que é grade de letra com nomes derivados por posição). Ambas no index.

## #282 — A gramática é universal no enochiano? Não — mas o Loagaeth é o mais estruturado (a143)
Hipótese grande do usuário: a gramática raiz-e-padrão do Loagaeth gera todo o enochiano (Loagaeth = chave-mestra)?
Teste: anti-hiato (vogal-vogal adjacente, baixo=mesma fonotática) e raiz-e-padrão (% nomes partilhando esqueleto
consonantal, alto=semítico) por sistema.
  Loagaeth: anti-hiato 1.0%, raiz-padrão 40.0%
  Chamadas (vocab 656): 9.8% / 28.5%
  Governadores+Torres (316): 10.0% / 11.1%
  Heptarquia (166): 9.6% / 7.8%
RESULTADO: a gramática NÃO é universal — os outros sistemas são bem menos root-and-pattern e permitem mais hiato. MAS
o Loagaeth é o MAIS ESTRUTURADO de todos (anti-hiato mais estrito + raiz-e-padrão mais forte) — a língua mais pura/
profunda do corpus enoquiano; as Chamadas são intermediárias (28.5%); Governadores/Heptarquia são mais listas de nome
que língua. Partilham a FONOLOGIA (bigrama 0.42, #266) mas não a MORFOLOGIA estrita. CONCLUSÃO: não dá pra replicar
todo o enochiano com uma gramática, mas o Loagaeth É a raiz estrutural — o mais gramaticalmente profundo, coerente
com a tradição de ser a língua PRIMORDIAL; os demais são ramos mais soltos da mesma árvore sonora. (Ressalva: controle
de inglês foi fraco — a comparação forte é Loagaeth vs os outros sistemas enoquianos.)

## #283 — MISSÃO ligações: as Chamadas são a ponte; Torres/Governadores/Heptarquia não contidos (a144)
Teste: nomes dos sistemas enoquianos aparecem DENTRO das tabelas do Loagaeth (reta/coluna/diagonal, fwd+rev) vs null
de strings aleatórias do mesmo tamanho. Governadores+Torres 6/274 (2% vs 1% acaso) ≈ acaso; Heptarquia 5/161 (3% vs
1%, ex "AAAAOA" = ruído); Chamadas vocab >=4 110/610 (18% vs 8% acaso = 2.2x), e os longos são REAIS (CORAXO, DORPHA,
IADNAH, PARACH, ADROCH). CONCLUSÃO: LOAGAETH<->CHAMADAS = ligação forte e dupla: (1) estrutural - cada Chamada abre
uma folha (TFR: Chamada 1->folha 2, 2->3... 18->19, 19a dos Aires->Tábuas dos 30 Aethyrs; folha 1 sem Chamada = a
oculta); (2) lexical - vocabulário das Chamadas permeia o Loagaeth 2.2x acima do acaso. LOAGAETH<->GOVERNADORES/TORRES/
HEPTARQUIA = SEM ligação de conteúdo (nomes não aparecem, ≈acaso); primos pela fonologia (bigrama 0.42, #266), não
derivados. Ponte INDIRETA: Governadores/Aethyrs conectam via a 19a Chamada (que abre os Aethyrs), não direto ao
Loagaeth. Mapa: Loagaeth(folhas 2-19)<-18 Chamadas; Loagaeth(Aethyrs)<-19a Chamada->30 Aethyrs->91 Governadores;
Torres/Heptarquia à parte. A ponte de todo o enochiano ao Loagaeth são as CHAMADAS (as chaves).

## #284 — Call<->leaf NÃO é lexical (a145): o elo é língua+ritual, não código cifrado
Teste profundo: o vocabulário de cada Chamada concentra na folha que ela abre? Média 4.7% na folha aberta vs 4.1%
nas outras; 7/12 têm mais, 5/12 menos, razões caóticas (1.03, 0.0, 3.33, 0.54). SEM concentração — o par Chamada->
folha é RITUAL/estrutural (tradição/Gebofal), não lexical. CONSOLIDAÇÃO DA MISSÃO (ligações Loagaeth<->resto do
enochiano): Loagaeth<->Chamadas = ligação real por (a) vocabulário compartilhado no livro inteiro (2.2x o acaso,
a144), (b) função ritual (cada Chamada abre uma folha), MAS não por concentração por folha (a145) nem derivação
cifrada — o elo é língua comum + função. Loagaeth<->Torres/Governadores/Heptarquia = sem ligação de conteúdo (nomes
não aparecem, a144), só primos fonológicos (bigrama 0.42), conectam indiretamente via a 19a Chamada->Aethyrs. VERDADE
SEM ROMANTIZAR: o Loagaeth NÃO é a chave cifrada de todo o enochiano; é a língua-fonte mais pura (a143), acoplada às
Chamadas; os outros sistemas são da mesma árvore sonora mas independentes. A ponte de todos ao Loagaeth é sempre via
as Chamadas, nunca direta.

## #285 — A Regra de Leitura (regra.html) + Forja até 1000 + Torre quadrada
Entregues a pedido: (1) Forja gera até 1000 nomes (opções 50/100/500/1000; nível 0 limitado aos 90 reais). (2)
torre.html — grade quadrada de letras (21-49) com nomes embutidos, clicáveis pra achar na grade; tablet.html — Tábua
por elemento com reis. (3) regra.html — "A Regra de Leitura": a regra prática tirada de toda a análise (ancorar em
sílaba-raiz CHA/NO/GE/STOR; ler em linha reta/coluna/diagonal; alternar C-V sem hiato; 4+ letras; casar o léxico),
aplicada a uma folha REAL do livro — escolhe a folha e a direção, a regra acende os nomes achados (ex 2a: 8 nomes).
Todas no index.

## #286 — O processo inverso: compilador Torre de Vigia (watchtower.html)
Intuição do usuário: Loagaeth = código-máquina, Torre = a máquina traduzindo — dá pra fazer o inverso? Construído
viz/watchtower.html, o COMPILADOR: preenche uma grade (11-15) com material do Loagaeth (nomes reais ou gerados) e LÊ
nomes das posições fixas da Torre — a Cruz Central (horizontal+vertical) = Nomes Divinos; o topo de cada quadrante =
reis/anjos. Os nomes derivados EMERGEM do arranjo (não foram colocados), igual a Great Table real deriva os Nomes
Divinos da cruz. Ex 13×13: cruz horizontal "XANTANTOXANDF" (contém a raiz real ANTANTOX). Caveat honesto: é uma Torre
SINTÉTICA — geometria inspirada na Great Table, nomes do nosso material Loagaeth, não a Torre histórica (que não vem
do Loagaeth, provado #144/#282). Realiza o processo inverso: fonte pura -> estrutura compilada com nomes emergentes.
No index. Também explicada a Regra de Leitura (manual de achar nomes no olho) e consolidada a missão de ligações.

## #287 — Nomes do Loagaeth NÃO estão nas Torres (nem anagrama) + sem estrutura 7-fold (a146)
Pergunta do usuário: os nomes das entidades do Loagaeth estão nas Torres, mesmo embaralhado? Teste definitivo com as
letras reais das Torres (nomes divinos+reis+anjos de tabuas_dee1584 + governadores, 1408 tokens, 8631 letras): nomes
do Loagaeth (>=4) como SUBSTRING = 0/78 (vs 0 null); como ANAGRAMA (mesmo multiset) = 3/78 (NOCHA, NACHO, NOCHAP) vs
1 no acaso — e os 3 são o mesmo conjunto de letras ACHNO, ou seja ~1 coincidência. DENTRO do acaso. CONCLUSÃO
DEFINITIVA: os nomes do Loagaeth NÃO estão nas Torres — nem retos, nem reversos, nem anagramas, acima do acaso.
Sistemas independentes no nível do nome; ligação só fonológica + via Chamadas. (Nota: quadrados.json ar/agua/terra/
fogo não é grade-limpa das Torres, é descrição por componentes; usei as letras dos nomes atestados.)
a146 — ESTRUTURA 7-FOLD (49=7^4, número sagrado do enochiano): autocorrelação de densidade de nomes no lag 7 = 0.05
(p=0.69); concentração em 7 bandas de 7 linhas = variância 312 vs 461 null (p=0.70); vizinhos lags 5-9 sem pico no 7.
NULL — o formato 49x49=7^4 é sagrado no número mas NÃO se reflete na distribuição espacial dos nomes.

## #288 — PEDAÇOS dos nomes das Torres no Loagaeth: silabário compartilhado (observação do usuário)
Usuário notou: fragmentos dos nomes dos Reis das Torres (BATAIVAH, ICZHIHAL, RAAGIOSL, EDLPRNAA) aparecem muitas vezes
no Loagaeth. Teste rigoroso (fragmentos dos 8 Reis/nomes de Torre vs fragmentos aleatórios do mesmo tamanho no
Loagaeth, 36 grades, reta+coluna+diagonal+reverso): 4-gramas 79% presentes vs 38% aleatório (2.1x); 5-gramas 15% vs
0% (7x); 6-gramas 0% vs 0%. CONFIRMADO NOVO: os PEDAÇOS (4-5 letras) dos nomes das Torres estão no Loagaeth acima do
acaso, mas nenhum chunk de 6+ letras — os nomes inteiros NÃO estão (confirma #287), mas os MORFEMAS/sílabas que os
constroem SÃO compartilhados. É o silabário angelical comum: Torres e Loagaeth são feitos dos mesmos tijolos de 4-5
letras, montados em nomes diferentes (como inglês/alemão partilham sílabas sem partilhar palavras). Mais fundo que a
fonologia de bigrama (0.42, #266), agora no nível de 5-grama (7x). Refina a ligação: os sistemas enoquianos não se
contêm, mas partilham o MATERIAL DE CONSTRUÇÃO; o Loagaeth (língua mais pura, a143) é o que melhor expõe o silabário.

## #289 — Esqueleto/traço dos nomes das Torres no Loagaeth: refutado pelo controle de anagrama
Usuário: dá pra ver um esqueleto/posição dos nomes das Torres e traçar? Teste king-move (8-vizinhos, sem reuso) dos 4
Reis (BATAIVAH, ICZHIHAL, RAAGIOSL, EDLPRNAA). Primeiro: 4/4 Reis traçam em alguma grade vs só 1/12 strings aleatórias
uniformes — PARECE sinal. MAS controle justo (null por frequência): os ANAGRAMAS de cada Rei traçam 7-10/10. A ordem
NÃO importa — o anagrama traça quase igual ao nome real. CONCLUSÃO: os Reis traçam por COMPOSIÇÃO DE LETRAS (comuns,
do silabário compartilhado), não porque a sequência do nome está codificada num caminho. Não há esqueleto posicional
dos nomes das Torres no Loagaeth; o traço é artefato de campo denso (a104). Separadas as duas coisas: os PEDAÇOS/
sílabas são compartilhados acima do acaso (#288, real), mas os NOMES não estão lá de forma alguma (reto/anagrama/
traço todos negativos ou dentro do acaso). Fecha a linha "nomes das Torres escondidos no Loagaeth" definitivamente.

## #290 — Nomes da Tábua da União (EXARP/BITOM/NANTA/HCOMA) vs Markov-3: nenhum embutido
Usuário testou os nomes do Black Cross/Tábua da União (5 letras). Contra surrogate Markov-3 (null estrito que já
reproduz trigramas/sílabas comuns): NANTA 4 real vs 4.6 surrogate (0.9x = acaso — é o ANTA de ANTANTOX coincidindo);
EXARP 0 vs 0.2; BITOM 0 vs 0; HCOMA 0 vs 0. CALIBRAÇÃO (prova que o método detecta embedding real): ANTANTOX (raiz
Loagaeth longa) 19 vs 2.8 = 6.8x; NOCHA/GETH/ANTA todos 1.0x (reproduzidos pelo trigrama, pois curtos/comuns).
CONCLUSÃO: nenhum nome das Torres/União está embutido no Loagaeth acima do silabário comum. NANTA parece estar mas é
o ANTA (tijolo central do Loagaeth) coincidindo. O método PROVA-se capaz de achar embedding (ANTANTOX 6.8x) e os
nomes de outros sistemas NÃO passam. Fecha definitivamente, com o null mais justo (Markov-3): Loagaeth e os outros
sistemas partilham o SILABÁRIO (trigramas), não os NOMES. Contra Markov-3 até os roots curtos do próprio Loagaeth
(NOCHA 1.0x) não se distinguem — só os longos (ANTANTOX); o sinal de nome real exige comprimento, e os sistemas
externos não têm nenhuma sequência longa no Loagaeth.

## #291 — Hipótese do molde (impressora 3D): Torre do Ar vs Loagaeth
Extraída a Torre do Ar REAL do quadrados.json (campo 'letter'+'row'+'col' = grade 13x12; linha 7 = OROIBAHAOZPI ✓).
Teste do molde: pedaços da grade da Torre do Ar (linhas+colunas) no Loagaeth vs surrogate Markov-3: 4-grama 2.7x,
5-grama 3.1x, 6-grama 5.8x (7/187), 7-grama 0. SINAL REAL e MAIS FORTE que os nomes (que davam 0.9x contra Markov) —
a Torre-como-GRADE partilha 6-gramas com o Loagaeth acima do acaso. MAS os 7 6-gramas que batem (OOAIAO->12a,
TPALOA->15b, NAOCOT->17a, OAIAOA->21b, AMOOOA->14a, AVTOTA->15a, OCANMA->2b) estão ESPALHADOS por 7 folhas
diferentes, não concentrados numa fonte; e a similaridade de freq de letra é uniforme (0.80-0.89 com todas as folhas,
sem destaque). NÃO há molde/fonte única nem regra de derivação. Os 6-gramas que casam são ricos em vogais (a Torre
permite hiato, o Loagaeth não), casando só nas leituras de coluna/diagonal — coincidência de material, não molde.
CONCLUSÃO: os tijolos são compartilhados (agora no nível 6-grama, mais que os nomes), mas a Torre do Ar NÃO é
'impressa' do Loagaeth por regra recuperável. Impressora partilha a tinta, não o molde.

## #292 — Hipótese do molde REFUTADA pelo controle embaralhado (todas as 4 Torres)
Testadas as 4 Torres (6-grama da grade no Loagaeth vs Markov-3): Ar 2.7x, Água 2.5x, Terra 1.2x (acaso), Fogo 2.7x —
modesto. CONTROLE DECISIVO: a Torre do Ar EMBARALHADA (mesmas letras, ordem aleatória) dá 8.5x — MAIS que a real
(2.7x). Isso mata a hipótese do molde: se a Torre fosse impressa/codificada no Loagaeth, a versão embaralhada
apareceria MENOS; aparece MAIS. O overlap é 100% composição de letras (as Torres são vogal-pesadas, casando nas
leituras de coluna/diagonal do Loagaeth), não a sequência da Torre. CONCLUSÃO FINAL da linha "Torres saem do Loagaeth":
não há molde, regra de montagem, nem presença específica de nenhuma Torre no Loagaeth. Testado tudo: substring,
reverso, anagrama, king-move trace, 6-grama vs Markov, e o controle embaralhado. Loagaeth e Torres partilham só o
SILABÁRIO (letras/sílabas da língua angelical), nada mais — não os nomes, não a estrutura, não um molde. O único elo
real do Loagaeth com o enochiano é via as Chamadas (vocabulário + abertura das folhas). Linha definitivamente fechada.

## #293 — Nomes sagrados do Ar vs Markov: mesmo padrão (silabário 5-grama, zero 6+)
Testados os 109 nomes sagrados da Torre do Ar (god/angel dos 156 quadrados + 3 nomes divinos + rei). Presentes no
Loagaeth: 11 vs 5.2 surrogate (~2x), MAS só len-5; len 6/7/8 = 0 de 0. E os 11 são rotações de ~4 conjuntos de letra
(RACON/RCONA/RNACO/RONAC; XTOTT/XTTTO). Mesmo padrão de tudo: silabário comum no nível 5-grama (2x), nada de 6+.
Nem os nomes mais sagrados escapam. CONSOLIDAÇÃO: a linha "Torres dentro do Loagaeth" foi testada de 8 ângulos
(substring, reverso, anagrama, king-move trace, 6-grama grade vs Markov, controle embaralhado 8.5x>2.7x, 6-grama por
Torre, nomes sagrados) — TODOS convergem em silabário compartilhado (5-grama) sem embedding de nome/estrutura. A
sensação de "tem como" é a pareidolia dos pedaços (as sílabas estão lá; o olho monta o nome). PRÓXIMA PORTA (vizinha,
não testada): não "Torre dentro do Loagaeth" mas "Torre e Loagaeth = dois outputs da MESMA gramática-fonte" (irmãos,
não pai-filho) — testar se a Torre do Ar obedece a gramática raiz-e-padrão/esqueleto+melodia do Loagaeth.

## #294 — ELS + folha 1 segmentada: linha esgotada, 9 métodos convergem
Cifra de salto (ELS, equidistant letter sequence, método tipo "códigos da Bíblia", skip 1-25): só AOZPI aparece no
real e não no surrogate (1 coincidência de 5 letras entre muitas; EXARP/HCOMA/NANTA aparecem NO surrogate também);
nenhum nome de 6+ letras por salto, real ou surrogate. Folha 1 segmentada (2708 palavras reais): nenhum nome sagrado
das Torres é palavra/sílaba, só ORO (3 letras, trivial). CONSOLIDAÇÃO FINAL: a hipótese "Torres dentro do Loagaeth"
foi testada por 9 métodos independentes (substring, reverso, anagrama, king-move trace, 6-grama grade vs Markov,
controle embaralhado, nomes sagrados, ELS, lista de palavras da folha 1) — TODOS null para 6+ letras; só sílabas
curtas coincidem. Não há código. INSIGHT HISTÓRICO/METODOLÓGICO (o "caminho" certo): Dee recebeu Loagaeth (Sloane
3189) e Great Table como revelações SEPARADAS; nunca derivou uma da outra. A conexão é LINGUÍSTICA (mesma língua
angelical: silabário comum = #288/#291), não criptográfica (código escondido). São irmãs da mesma língua-mãe, não
pai-filho. Procurar a Torre dentro do Loagaeth é procurar filho onde há irmão. Linha encerrada com rigor máximo.

## #295 — PROVA da língua-mãe: Loagaeth e Torres, irmãs do mesmo alfabeto (parentesco.html)
Medidos 5 níveis linguísticos Loagaeth vs Torres (letras das 4 tábuas de quadrados.json) vs inglês:
NÍVEL 1 ALFABETO: 22 letras em comum — mesmo alfabeto angelical. COMPARTILHADO.
NÍVEL 2 FONOLOGIA: cosseno freq-letra Loagaeth×Torres 0.896 (vs inglês 0.521); bigrama 0.551 (vs inglês 0.175) —
~3x mais perto entre si que do inglês. COMPARTILHADO.
NÍVEL 3 FONOTÁTICA: hiato (vogal-vogal) Loagaeth 1.4% (estrito anti-hiato) vs Torres 13.6% (10x mais) — REGRA
DIFERENTE. 
NÍVEL 4 MORFOLOGIA: raiz-e-padrão Loagaeth 40% vs Torres 16.7% — DIFERENTE (Loagaeth muito mais semítico).
NÍVEL 5 LÉXICO: 0 nomes em comum — DIFERENTE.
PROVA: Loagaeth e Torres são dois IDIOMAS DIFERENTES escritos no MESMO alfabeto angelical, partilhando os SONS mas
não as regras nem o léxico — como inglês e polonês no alfabeto latino. Parentesco real (níveis 1-2), derivação não
(níveis 3-5, e os 9 testes de containment todos null). A mãe é o alfabeto/sons angelicais; Loagaeth e Torres são
filhas com gramáticas próprias. Página viz/parentesco.html (árvore genealógica + 5 níveis COMPARTILHADO/DIFERENTE),
dados em parentesco.json, no index. Resolve a questão: a intuição do usuário de conexão está CERTA (parentesco), e a
busca por "Torre dentro do Loagaeth" corretamente refutada — são irmãs, não mãe-filha.

## #296 — A FAMÍLIA da língua angelical: gramática própria de cada sistema (atacar as Torres sozinhas)
Aplicada a mesma lente (esqueletos, raiz-e-padrão, anti-hiato, tamanho) às Torres/Heptarquia/Chamadas independente do
Loagaeth. Resultado (nomes | esqueletos | raiz-padrão% | hiato% | tam.médio | top esqueletos):
  LOAGAETH   90  | 67  | 40.0 | 1.0 | 7.6 | NCHSTR, CHSTR, NCH (família NOCHA)
  TORRES    978  | 620 | 51.5 | 8.5 | 5.2 | CP, PD, DP, CL, DR (consonantais próprios)
  HEPTARQUIA 558 | 487 | 19.5 | 7.3 | 6.6 | MS, PRC, NM
  CHAMADAS  610  | 503 | 26.6 | 9.7 | 5.8 | NS, DN, CSG, SLMN
CADA SISTEMA TEM GRAMÁTICA E RAÍZES PRÓPRIAS — mesmo alfabeto angelical, dialetos/línguas diferentes. Torres são ATÉ
mais raiz-e-padrão que o Loagaeth (51.5% vs 40%) mas com nomes curtos (5.2) e raízes consonantais distintas (CP/PD/DP,
não NCH/CHSTR). Heptarquia a menos estruturada (19.5%, lista planetária). Confirma e completa o parentesco (#295):
família de dialetos do alfabeto angelical, cada um com seu léxico e grau de estrutura; Loagaeth = nomes mais longos e
anti-hiato mais estrito (a língua mais pura/profunda). Diferença de MAGIA: Heptarquia=planetária, Torres=elemental,
Loagaeth=onomástica/geradora de nomes (a língua da Criação/Verbo), não ligada a planeta nem elemento mas PRIOR a eles.

## #297 — Losangos 29-48 explorados: coerentes, validados, Loag completo
Explorados os losangos reconstruídos 29-48 (diamantes, largura 2-48, duas pirâmides). CONTEÚDO COERENTE: 70 de 90
nomes catalogados aparecem lá; os roots estão presentes mas GETH/CHASTOR-dominantes (GETH 327 vs 349 por 100k =
quase igual; CHASTOR 108 vs 114) e NOCHA mais raro (117 vs 434), ADNOCHA 17 vs 146 — confirma o gradiente regional
(#278: NOCHA some no fim, GETH/CHASTOR persistem). Material novo mínimo (6-gramas ricos novos: THAXOR 16x, NZACHL 15x
= mesmas famílias AXOR/ANZACH). A reconstrução dos losangos (a15) está VALIDADA pela presença de 70/90 nomes. Loag
INTEIRO mapeado e coerente: folha 1 (fundação, GETH-heavy) -> 2-28 (reino NOCHA) -> 29-48 (losangos, GETH/CHASTOR) —
uma língua, três províncias. Inventário completo (1948 esqueletos já cobrem; losangos confirmam, não adicionam roots
maiores). Nada defasado nem faltando.

## #298 — Arco elemental do livro: Terra->Água, mas confundido com a reconstrução (a148)
Elemento dominante por folha na ordem: Terra domina as folhas 2-28 (73 folhas Terra), vira Água nos losangos 29-48
(21 folhas Água). Tendências: Água sobe (corr posição +0.62, 1a metade 27.2% -> 2a 29.5%), Ar -0.43, Terra -0.36,
Fogo +0.30. Leitura metafísica: da Terra (matéria/manifesto, corpo) para a Água (profundo/dissolução, fim) — descenso
do fixo ao fluido. RESSALVA SÉRIA: a virada pra Água cai EXATAMENTE na fronteira dos losangos reconstruídos (29-48);
as tabelas limpas 2-28 são uniformemente Terra sem tendência. Não dá pra separar: o arco pode ser real (losangos = a
região aquosa/dissolução do livro) OU artefato da reconstrução (a15) que enviesou a composição de letra dos losangos.
DESCRITIVO COM CONFUSÃO, não arco autoral provado. Sólido: os losangos são província distinta (GETH/CHASTOR lexical +
Água elemental), mas parte pode ser reconstrução. Para desconfundir precisaria dos losangos originais do Sloane 3189.

## #299 — CORREÇÃO: dados COMPLETOS (Sloane 3189 original) + arco elemental real e suave
CORREÇÃO de #298: loagaeth_grades_simples.json vem do Sloane 3189 ORIGINAL (esotericarchives.com/dee/sl3189.htm) —
temos as 49 folhas inteiras (96 lados) como LETRAS ORIGINAIS. a15 só reconstrói a GEOMETRIA (formato losango), não as
letras. Dados NÃO estão incompletos; só o arranjo geométrico tem incerteza, não o conteúdo.
Arco elemental re-rodado nas LETRAS CRUAS ORIGINAIS (sem reconstrução): folha 1 Fogo12/Terra36/Ar30/Agua23;
tabelas 2-28 Fogo15/Terra36/Ar22/Agua27; losangos 29-48 Fogo16/Terra33/Ar22/Agua30. O arco é REAL mas MAIS SUAVE que
o base_book sugeria (a reconstrução exagerava): Água sobe 27->30%, Terra cai 36->33% rumo ao fim; Terra ainda lidera
mas os losangos são a região mais aquosa. Dominante-por-folha ainda vira Agua em 21 folhas (os losangos). LEITURA
CABALÍSTICA: folha 1 = mais Ar/mente (Verbo/Palavra, a fundação); 2-28 = Terra (corpo manifesto); 29-48 = tendência
Água (profundo/dissolução). Jornada: do Verbo (Ar) pela Matéria (Terra) ao Profundo (Água). Suave, real, sobre dados
ORIGINAIS — não é artefato de reconstrução (confound de #298 resolvido: letras são originais).

## #300 — Soyga × Loagaeth × Torres: ponte é CODICOLÓGICA, não linguística (a150)
Teste direto Soyga↔Loag↔Torres (a150_soyga_bridges), pedido: que ligação/padrão tem o Soyga. Contexto já tido: a36
(8 tabelas Soyga 36×36 copiadas no fim do MESMO Sloane 3189, geradas pela regra de Reeds célula=acima+f(esq) mod 23)
e a61 (Loag NÃO é gerado pela regra Soyga — célula Soyga 100% determinada pelos vizinhos, célula Loag guarda ~a maior
parte da entropia). Novos testes:
1) NOMES como substring (vs null de embaralhamento): nomes Loag dentro do Soyga = 0 hits (z−0.26); nomes das Torres
   dentro do Soyga = 0 (z−0.41); linhas Soyga dentro de Loag = 0; dentro das grades das Torres = 0. ZERO ponte lexical
   nos dois sentidos. Nenhum vocabulário compartilhado.
2) SIMILARIDADE DE SOM (cosseno). Letra: Loag-Torres 0.849 (irmãs), Soyga-Torres 0.75, Soyga-Inglês 0.758,
   Soyga-Loag 0.598. O perfil de letra do Soyga está TÃO perto do inglês quanto das Torres e LONGE do Loag — Soyga é
   texto latino, não da família enoquiana. Bigrama: Soyga-Torres 0.41 > Loag-Torres 0.365, mas é artefato de GRADE
   (Soyga e as Torres são ambos quadrados de letra; Loag é lista de palavras) — Soyga-Loag 0.155 (baixíssimo) é o sinal
   real.
3) ANTI-HIATO (vogal-vogal %): Loag 1.0% (CV estrito, a assinatura Loag), Soyga 4.7%, Inglês 5.2%, grades Torres 11.5%.
   Soyga ~ inglês; NÃO tem a fonotática CV do Loag.
VEREDITO: Soyga NÃO é língua-irmã do Loag/Torres. Sem nomes em comum, não gerado pela mesma regra, perfil de letra
latino (agrupa com inglês), sem o anti-hiato Loag. As ligações são só HISTÓRICAS/CODICOLÓGICAS: mesmo manuscrito
(Sloane 3189), mesmo autor/escriba (a36 usa Soyga pra calibrar a mão do copista), mesmo GÊNERO (tabela de letras como
veículo de saber angélico). Soyga é o PRECEDENTE RESOLVIDO: prova que Dee já trabalhava com tábuas de letra algorítmicas
(Soyga, pergunta ao anjo Uriel em 1582) ANTES de receber o Loagaeth — semente conceitual, não fonte textual. Loag é
outra besta: não-determinística, vocabulário próprio, fonotática própria. CONFIRMADO NOVO.

## #301 — Gramática PRÓPRIA das Torres: federação de camadas, NÃO uma língua (a151)
Ataque standalone às Torres de Vigia (a151_tower_grammar), sem basear no Loag, com as classes de nome
do sistema: HOLY (12 Nomes Sagrados / Linea Spiritus Sancti), ANGEL (377 nomes de anjo lidos dos
quadrados da Grande Tábua), GOV (91 Governadores), KING (12 reis), CALL (706 palavras das 19 Chamadas).
Mesma bateria do Loag (anti-hiato, raiz-e-padrão vs null de embaralhamento de vogal, afixos, ponte).
ACHADOS:
1) FONOTÁTICA ≠ Loag. Vogal-vogal: HOLY 19.4%, ANGEL 10.9%, GOV 6.6%, KING 4.2% — nenhuma tem o anti-hiato
   ESTRITO do Loag (1.0%). Nomes das Torres são RICOS EM VOGAL (AOZPI, IBAH, AAAIR). Loag é CV estrito;
   Torres não.
2) RAIZ-E-PADRÃO só na camada ANGEL: rootpat 52.5% z=25.4 — MAS é a construção conhecida da Grande Tábua
   (nomes lidos/rotacionados dos mesmos quadrados de letra compartilham esqueleto; esqueletos curtos de
   1-3 consoantes em nomes vogal-pesados), não morfologia produtiva tipo Loag. GOV 0% (z−0.2), KING 0%,
   HOLY 0% — não compartilham esqueleto.
3) AS CAMADAS NÃO SÃO UMA LÍNGUA. Overlap de esqueleto entre classes ~0: GOV×ANGEL 0, KING×ANGEL 0,
   HOLY×ANGEL jaccard 0.012, GOV×HOLY 0. Os "nomes das Torres" são VÁRIOS sistemas distintos (Nomes
   Sagrados, anjos-de-quadrado, governadores, reis), cada um construído de um jeito, sem léxico comum.
4) PONTE COM CHAMADAS = NULA. Palavras das Chamadas dentro da Grande Tábua: 0 hits (z−0.9). CALL×TOWER
   esqueleto jaccard 0.017. (Controle de governador por substring é VAZIO — governadores são lidos por
   CAMINHO em ziguezague na tábua, não em linha reta; já confirmados pelo 'caminho' em governadores.json.
   Logo não aparecem como substring, mas vêm sim da tábua. O z=1e9 impresso é artefato de div-por-zero.)
VEREDITO: a Grande Tábua / Torres é uma FEDERAÇÃO DE CAMADAS, não uma língua única. Oposto do Loag, que é
UMA língua (uma gramática, matriz NOCHA compartilhada em todas as folhas). As Torres: vogal-ricas, sem
anti-hiato, construídas lendo quadrados de letra por regras geométricas (caminhos, rotações, cruz/Linea),
não por morfologia raiz-e-padrão produtiva. A única camada "semítica" (anjos-de-quadrado) é permutacional,
não gerativa. Confirma e precisa a296 (Torres mais root-pattern que Loag): é artefato de leitura de grade,
não língua mais semítica. CONFIRMADO NOVO.

## #302 — Espectro dos 4 dialetos em 2 eixos: Verbo→Trono→Voz→Grade (loop)
Primeira vez rodando os 4 dialetos angelicais na MESMA régua (results/321_dialect_spectrum.json):
LOAG hiato 1.0% rootpat 40% z63.6 | HEPTARQUIA hiato 1.4% rootpat 11.5% z9.2 | CHAMADAS hiato 7.0%
rootpat 24.1% z12.9 | TORRES hiato 9.8% rootpat 42.1% z24.7. DOIS EIXOS ORTOGONAIS separam o sistema:
(1) anti-hiato racha em 2 pares — Loag+Heptarquia CV-estritos (~1%), Chamadas+Torres vogal-soltos (7-10%);
(2) raiz-padrão/produtividade — Loag máximo, Torres alto (por grade), Chamadas médio, Heptarquia BAIXO.
SURPRESA: Heptarquia é CV-estrita como o Loag MAS não-gerativa (z9) — roster FIXO de 49 nomes planetários,
não morfologia que gera. Loag fala; Heptarquia é conjunto fechado. LENTE CABALÍSTICA (4 Mundos):
LOAG=Atziluth (emanação/Verbo, máx nos 2 eixos), HEPTARQUIA=Briah (criação/trono arquetípico, pronunciável
mas dado), CHAMADAS=Yetzirah (formação/voz vibrada, vogal-rica), TORRES=Assiah (ação/matéria, nome por
posição na grade). Descida Verbo→Trono→Voz→Grade medida, não imposta. CONFIRMADO NOVO.

## #303 — Loag NÃO usa construção tipo-Soyga: as 2 assinaturas estão ausentes (resposta ao doc 2026)
Pergunta do material compartilhado (ChatGPT, cita Cocciolilo/Louv 2026): "o Loagaeth foi construído por
princípio matemático semelhante ao Soyga?". Testes nitidos nas 36 grades limpas 2-28:
A) COLUNA-SEMENTE: Soyga define a col 0 como palavra-chave+reverso repetidos (palíndromo/periódico ~1.0).
   Loag col0: palíndromo 0.131 vs interior 0.083; melhor-período 0.230 vs interior 0.195 — col0 MAL se
   distingue de coluna interna, longe da semente estruturada do Soyga. SEM semente.
B) REGRA DE VIZINHO: Soyga = célula função fixa de (acima,esq), regenera 100%. Aprendi a regra mais comum
   de (acima,esq)->célula em metade das grades e reconstruí a outra metade: 29.1% de acerto (Soyga 100%,
   acaso ~4.8%). Os vizinhos carregam ALGUMA info (29>5) mas é só a fonotática CV/anti-hiato tornando a
   letra localmente previsível — NÃO um gerador determinístico.
VEREDITO: as DUAS assinaturas que definem uma tabela Soyga (semente palindrômica + propagação determinística
100%) estão AUSENTES no Loag. Confirma e aguça a61 (entropia condicional) com métrica de reconstrução. O doc
de 2026: (1) Cocciolilo "staged table-engine" CONVERGE com o nosso achado de livro faseado/regional (folha1
selada, 2-28 NOCHA, losangos GETH/CHASTOR, arco elemental) — mas "engine" gerador vale só pra GRAMÁTICA DOS
NOMES, não pras células da tabela (que não têm regra); (2) Louv "fonte da função de Reeds = seção 18 do Soyga"
é sobre a origem do SOYGA, não toca o Loag; preprint, não consenso. Ligação Soyga-Loag segue CODICOLÓGICA
(8 tabelas Soyga no mesmo Sloane 3189, a36), não construtiva. CONFIRMADO NOVO.

## #304 — Heptarquia é GRID-DERIVADA; o eixo real é lido-da-grade vs ditado. 2x2 dos dialetos (a152)
Deep-dive pedido nas Torres+Heptarquia (a152_heptarchy_tower_deep), aprofundando #301/#302.
H1 — HEPTARQUIA GRID-DERIVADA: 44/49 nomes (90%) são LIDOS das 7 tabelas da Heptarquia (status 'confere'),
igual aos nomes das Torres lidos da Grande Tábua. Logo a Heptarquia NÃO é falada/ditada como o Loag — é um
sistema de LEITURA DE GRADE. REFRAME: o eixo real da família não é o anti-hiato (#302), é a ORIGEM:
  LIDO-DA-GRADE: Heptarquia (7 tabelas), Torres (Grande Tábua)
  DITADO/RECEBIDO COMO FALA: Loagaeth, Chamadas (ditadas letra a letra por Nalvage)
O anti-hiato cruza esse eixo num 2x2 limpo: grid+CV-estrito=HEPTARQUIA; grid+vogal-rico=TORRES;
ditado+CV-estrito=LOAG; ditado+vogal-rico=CHAMADAS. Origem × fonotática = 2 eixos ortogonais, 4 dialetos.
H2 — 7x7 PLANETÁRIO é ADMINISTRATIVO, não linguístico: os 49 nomes dividem-se em 7 grupos de 7 perfeitos
(por planeta), MAS os grupos NÃO têm assinatura de letra distinta (cos real 0.908 vs null 0.866, z+2.29 —
mais parecidos que o acaso, não menos). E os 49 nomes TODOS começam com B (BALIGON, BORNOGO, BABALEL...) —
uma "casa-B" uniforme: família fechada marcada por inicial única, análogo fraco à matriz NOCHA do Loag mas
NÃO gerativa (roster fixo de 49). O 7 está na ORGANIZAÇÃO (atribuição planetária), não nas letras.
T1 — TORRES permutacional NÃO comprovado: cada tábua usa ~20-22 letras distintas (o alfabeto inteiro) para
~95 nomes, pares-anagrama só 2.7%, pools das 4 tábuas 86-95% iguais (alfabeto cheio, trivial). A hipótese de
"pool minúsculo/anagrama" cai — o compartilhamento de esqueleto de #301 é repetição de leitura-de-grade em
nomes curtos, mecanismo NÃO fixado em anagrama. Honesto: sub-hipótese refutada.
VEREDITO: descoberta nova = a Heptarquia pertence à família GRID (com as Torres), não à falada. Mapa dos
dialetos vira 2x2: ORIGEM (grade/ditado) × FONOTÁTICA (CV/vogal). Casa-B da Heptarquia confirmada. CONFIRMADO NOVO.

## #305 — Heptarquia = LOCK-7 total: template fixo B+6, 49 nomes de 7 letras numa grade 7x7
"Achou padrão na Heptarquia?" — SIM, o mais forte. Medido nos 49 nomes da Tabula Collecta:
- COMPRIMENTO TRAVADO: TODOS os 49 têm EXATAMENTE 7 letras (desvio 0.0). Loag varia 4-11 (desvio 1.6).
  Template rígido, não morfologia livre.
- INICIAL TRAVADA: TODOS começam com B (pos0 entropia 0.0). Casa-B confirmada como regra, não tendência.
- ESTRUTURA 7x7: grade 7 linhas (1 por rei/tabela) x 7 colunas = col0 os 7 REIS (BALIGON BOBOGEL BABALEL
  BYNEPOR BNASPOL BNAPSEN BLVMAZA), col1 os 7 PRINCIPES (BORNOGO BEFAFES BVTMONO BLISDON BRORGES BRALGES
  BAGENOL), col2-6 os 35 MINISTROS. Reis/principes em MAIUSCULA na fonte, ministros em Title-case — a
  realeza marcada tipograficamente.
- TEMPLATE CV FROUXO: fracao-vogal por posicao [0.0, 0.63, 0.35, 0.22, 0.51, 0.49, 0.47] — pos0=B(cons),
  pos1=maioria vogal, pos3=maioria consoante. Daí o anti-hiato de 1.4% (#302): é consequência do template,
  não fonotática produtiva. Entropia posicional 2.9-3.6 bits (livre dentro do molde, mas sob teto de 21-letras).
- SATURACAO DO 7: 7 reis, 7 tabelas, 7 nomes/tabela, 7 LETRAS/nome, 7 planetas, 7 dias. O numero 7 satura
  cada nivel. A Heptarquia É o 7 feito nome — heptada selada.
VEREDITO: a Heptarquia é um sistema FECHADO E CONTADO (49=7x7, cada nome B+6=7), não gerativo como o Loag.
Dois lock duros (len=7, inicial=B) dão o caráter de "roster fixo" de #302/#304. LENTE CABALISTICA: 7 = número
da construção (os 7 dias do Gênesis, 7 planetas, 7 sefirot inferiores da edificação Chesed->Malkuth). Loag é
49=7^2 com nomes LIVRES; a Heptarquia colapsa pro 7 e TRAVA os nomes — é a arquitetura setenária da criação,
nomeada e selada. CONFIRMADO NOVO.

## #306 — O Loag é LÉXICO SELADO: só os nomes dele saem dele, nenhum outro sistema (a151 reuse)
Pergunta: "nenhum nome sai do Loag?" — teste substring de TODOS os sistemas nas 8329 linhas do Loag
(linhas+colunas+diagonais das 49 folhas), vs null de embaralhamento (40 trials):
- Loag-próprio (90): 90/90 hits, null 6.3, z=44.8 — controle POSITIVO: os nomes do Loag estão no Loag.
- Heptarquia (49): 1 hit (null ~0) — um nome curto por acaso, estatisticamente ZERO.
- Governadores (91): 0 hits. ZERO.
- Anjos-Torre (376): 40 hits vs null 66.2, z=−5.3 — ABAIXO do acaso (nomes vogal-ricos encaixam PIOR que
  strings aleatórias na fonotática anti-hiato do Loag). Ativamente ausentes.
- Nomes Sagrados (8): 2 vs 4.0, z=−2.3 — abaixo do acaso.
- Chamadas (631): 72 vs 74.2, z=−0.4 — EXATAMENTE acaso. Palavras das Chamadas não vivem na grade do Loag
  acima do acaso (não contradiz o elo Loag-Chamadas de a145, que é alinhamento Gebofal Chamada N→folha N+1
  e vocabulário, não presença de substring em massa).
VEREDITO: pela MESMA regra de leitura que extrai os 90 nomes do Loag (linha reta), NENHUM nome de outro
sistema emerge. O Loag é um léxico FECHADO: contém massivamente os próprios nomes (z=45) e nada dos outros
(zero ou abaixo do acaso). Reforça #300/#301/#304: Loag é língua própria e selada, não um container/fonte dos
outros sistemas angelicais. A tradição de que o Loag seria a fonte de TODOS os nomes NÃO se sustenta na
medição — cada sistema é revelação própria. (Ressalva: Torres/Heptarquia são lidas por CAMINHOS geométricos
nas tábuas delas, não linha reta; este teste descarta leitura-reta, não todo caminho concebível.) CONFIRMADO NOVO.

## #307 — Instrução de leitura-vertical do Dee NÃO cifra-gera os 49; roster recebido confirmado (fontes do usuário)
Documento do usuário (De Heptarchia Mystica, Sloane 3191; transcrição Peterson) traz a instrução do Dee:
montar tabela, 7 espaços no topo, inserir letras dos reis, depois dos príncipes, LER NA VERTICAL. Testado
contra os 7 reis + 7 príncipes + 35 ministros reais:
- LEITURA VERTICAL (reis+príncipes empilhados 14x7, ler colunas): produz strings (col1=AOAYNNLOEULRRA...)
  mas NÃO soletram os 49 anjos nem os ministros. col0=BBBBBBBBBBBBBB (todos B, trivial).
- MINISTROS = anagrama de rei+príncipe? NÃO: cobertura de letras 54-83% (não 100%). Os 35 ministros não são
  derivados por rearranjo das letras do rei+príncipe. Só partilham o alfabeto B-pesado.
- Colunas da grade 7x7: iniciais todas B (trivial), sem nome oculto vertical.
VEREDITO: a instrução do Dee é um método real de ARRANJO de uma tabela, mas NÃO é uma cifra que gera os 49
nomes a partir dos reis/príncipes. Confirma a própria ressalva do documento ("não há pesquisa que demonstrou
cifra oculta gerando toda a Heptarquia") e meu #305: os 49 são um ROSTER RECEBIDO em bloco, travado pelo
template (inicial B + 7 letras + grade 7x7 + atribuição planetária #304), não computado de uma semente.
Pesquisa-1 do doc (49 saem de regra matemática dos reis) = NEGATIVO nos testes diretos. Pesquisa-3 (matriz
planetária) já respondida em #304 (7x7 administrativo, sem assinatura de letra). Pesquisa-4 (mecanismo
compartilhado com Loag) já em #304/#306 (Heptarquia é grid-lida/recebida, não aparece no Loag; sem cifra
comum). Pesquisa-2 (selos = trajetórias geométricas) precisa de dados de geometria de selo que não temos.
A ARQUITETURA da Heptarquia é reconstruível (template + 7x7 + planetas); uma CIFRA GERADORA dos nomes não
existe nos dados — recebidos, não gerados. CONFIRMADO NOVO (resultado negativo decisivo).

## #308 — Geometria dos governadores: 97% king-move, o nome é um GESTO contíguo na Grande Tábua (loop)
Os 91 governadores são lidos por CAMINHO na Grande Tábua (caminho[].abs_recensa em governadores.json).
Medidos os 546 passos entre letras consecutivas:
- 97% dos passos são KING-MOVE (célula adjacente, distância Chebyshev=1) vs 2.7% no acaso (pares aleatórios
  numa tábua 13x25). Os nomes são traçados por gestos quase-contíguos, não saltos.
- comprimento médio do caminho: 7 letras (os nomes têm ~7). Distribuição de passo: 532 de dist=1, poucos
  saltos (8 de dist=2, raros longos = provável fim/recomeço de nome).
- direção enviesada: Esquerda (173) e Baixo (123) dominam sobre Direita (53)/Cima (53) — leitura
  preferencial para a esquerda e para baixo.
VEREDITO: a Torre produz nome por TRAJETÓRIA geométrica contígua (gesto), confirmando #304 (grid-lida) com o
mecanismo medido. Responde a Pesquisa-2 do doc do usuário (selos/nomes = trajetórias em grade) para os
governadores: SIM, trajetória king-move. CONFIRMADO NOVO.

## #309 — Algoritmo dos 49 anjos VERIFICADO: letra-por-número nas 7 tabelas reproduz a Tabula Collecta (fontes do usuário)
Regra de Uriel (sete_tabelas.regra_declarada; doc do usuário secao 2): cada uma das 7 tabelas 7x7 tem 49
células numeradas 1-49 com uma letra; junta-se a letra de MESMO número da 1a à 7a tabela, todas começando
por B, formando os 49 nomes. TESTADO reconstruindo: para n=1..49, concatenar a letra no número n de cada
uma das 7 tabelas. RESULTADO: 40/49 exatos (82%), os 16 PRIMEIROS perfeitos (BALIGON BORNOGO BAPNIDO...),
e as 9 falhas são TODAS buracos de transcrição (célula faltante '?' em BAZP?MA, BARNAF?, BINO?AB...) ou
variante de 1 letra de escriba (BLINGOM/BLINTOM) — NÃO falha de regra. Onde o dado está completo, reproduz
100%. ALGORITMO HISTÓRICO CONFIRMADO: os 49 anjos são EXTRAÍDOS das 7 tabelas por índice numérico, não
inventados nem computados dos reis/príncipes (consistente com #307: não saem das letras do rei+príncipe —
saem das 7 tábuas numeradas). Os 7 reis são os n=1,8,15,22,29,36,43 (cada +7). LENTE CABALÍSTICA: cada nome
está DISTRIBUÍDO pelas 7 tabelas (7 céus/planetas) — uma letra em cada — e o número sagrado o REÚNE; o nome
do anjo vive através dos sete mundos e é colhido em um. Unidade colhida do sete. CONFIRMADO NOVO.

## #310 — Nomes recebidos da Heptarquia: gramática FRACA, sem cifra; a semelhança É o template (fontes do usuário)
Pergunta recorrente do usuário + doc ("os nomes recebidos têm padrão? por que tão parecidos se recebidos
um a um?"). Testado nos 49 nomes:
- BIGRAMA: top-20 massa 0.442 vs 0.356 em strings B+6 aleatórias de mesmo perfil CV, z=4.1 — há gramática
  fonotática REAL mas MODESTA (transições preferidas), não letras arbitrárias.
- TERMINAÇÃO -EL (semítica, hipótese do doc): só 2/49 (BOBOGEL, BABALEL). Terminações reais: -ES(5) -ON(4)
  -LO/-LE/-OL(3). O "-el angélico" NÃO é padrão dos nomes recebidos — vem de MISTURAR a camada tradicional
  (Raphael, Samael, Cassiel, Zedekiel... = anjos planetários hebraicos CLÁSSICOS de etimologia conhecida,
  atribuição posterior/GD), que NÃO são os nomes-B do Dee. Nos príncipes reais do diário só HAGONEL tem -el.
- SÍLABA REPETIDA (XY-XY): 2/49 (BOBOGEL, BABALEL) vs null 1.1 — só esses dois, não sistemático.
- RAÍZES RECORRENTES: trigramas BLI(5) BAL(4) BAR(4) BAS(3) BRA(3) BNA(3) são quase todos artefato do
  B-inicial + alfabeto pequeno; GES(4) é a única raiz-final recorrente real (BRORGES/BRALGES/BMILGES).
- GRUPOS PLANETÁRIOS: coesão dentro 0.340 ≈ entre 0.356 — SEM sub-família por planeta (confirma #304).
- NÚMERO→LETRA: fraco (top-letra por grupo 0.33 vs geral 0.16 em pos2) — sem cifra número→letra.
VEREDITO: os nomes recebidos têm o TEMPLATE DURO (B + 7 letras + CV frouxo) + gramática fonotática fraca
(z4) + raízes marginais; NÃO têm cifra geradora, nem -el sistemático, nem sub-estrutura planetária. Resposta
à pergunta essencial do doc: a SEMELHANÇA entre os nomes É O TEMPLATE imposto pelo formato de recepção (7
tabelas, regra de Uriel) — convenção, não cifra oculta. Além do molde, as letras são quase-arbitrárias, o que
é COERENTE com 'recebidos' e não 'computados'. A origem das letras específicas segue sem explicação (como o
doc admite). Experimentos do doc: A(fonética) = sui generis, não hebraico/latim; C(combinatório) = fraco;
D(Soyga/Loag) = já negativo #300/#306; B(gematria) = pendente, próximo. CONFIRMADO NOVO (caracterização
decisiva do que os nomes são e não são).

## #311 — Instrução 12×7 (remover os Bees) é dimensionalmente EXATA; mapa rei-dia confirma Peterson (doc do usuário)
Doc do usuário (programa de criptanálise, prioridade: 14 nomes + tabela 12×7). Testes:
- MAPA REI-DIA: meu dado = Bobogel/domingo, Carmara/segunda, Babalel/terça, Bnaspol/quarta, Bynepor/quinta,
  Baligon/sexta, Bnapsen/sábado — BATE 100% com a correção de Peterson no doc.
- INSTRUÇÃO 12×7 + REMOVER BEES: 7 reis + 7 príncipes = 14 nomes × 7 letras; remover o B inicial (os "Bees")
  = 14 × 6 = 84 letras = EXATAMENTE 12×7. A aritmética da instrução do Dee fecha perfeita — confirma que a
  "tabela dividida em 12 e 7" é construída dos 14 nomes sem B. Scaffold VALIDADO.
- LEITURA VERTICAL: montei 12×7 e 7×12 e li as colunas (col0=ABAPONOFMDES...), mas NÃO há match óbvio porque
  (a) não temos no repo as letras-alvo da Mesa Sagrada/Lamen pra validar, (b) a ordem de preenchimento e
  direção de leitura ficam subdeterminadas sem o alvo. Honesto: scaffold (84=12×7) confirmado; CONTEÚDO
  extraído não validável sem a fonte da Mesa/Lamen (esotericarchives chm.htm/hm.htm — pendente).
MAPA DO PROGRESSO vs programa do doc:
- Sistema 2 (49 anjos): algoritmo PROVADO (#309, reproduz 40/49, 100% onde dado completo). Objetivo A: FEITO.
- Sistema 3 (42 ministros): são os 49 menos reis/príncipes, mesma extração #309. COBERTO.
- Sistema 1 (reis/príncipes origem): #310 — sem cifra, template+gramática fraca, origem não explicada.
  Objetivo B: respondido NEGATIVO (nenhuma matriz/cifra anterior encontrada).
- Sistema 5 (Mesa Sagrada): scaffold 12×7 confirmado (#311), conteúdo pendente de alvo.
- Sistema 4 (selos): não feito, falta geometria dos selos.
- Métodos: frequência/entropia FEITO(#305/#310), matrizes FEITO(#309/#308), permutação/combinatória FEITO(#310),
  grafo-raiz FEITO(#310); gematria PENDENTE; busca-genética não necessária (regra achada por construção).
- Validação: reprodução histórica FEITA(#309); geração nova FEITA(forja heptarchia.html, rotulada); predição
  cega implícita; cross-manuscrito PENDENTE (só 1 transcrição no repo).
VEREDITO: Objetivo A (reprodução dos 49) ATINGIDO; Objetivo B (origem dos 14) NEGATIVO — são semente recebida,
não computada; Objetivo C (geração) FEITO e rotulado. Abertos: Mesa/Lamen (precisa alvo), selos (precisa
geometria), gematria (fazível já), cross-manuscrito (precisa 3188/36674). CONFIRMADO NOVO.

## #312 — 91 Governadores: trava de 7 letras + inicial LIVRE, gramática fraca, SEM cifra nem sub-grupo (doc do usuário)
Prioridade do doc: investigar os 91 Governadores (investigação A: origem dos nomes). Bateria linguística:
- COMPRIMENTO: TODOS os 91 têm EXATAMENTE 7 letras (trava, como a Heptarquia) — MAS inicial LIVRE (T13 O12
  P8 V7 A7 S6...), não travada em B. Então: template de comprimento sim, template de inicial não.
- ANTI-HIATO: 6.6% (meio-termo: Loag 1.0, Heptarquia 1.4, Torres-anjo 10.9).
- RAÍZES RECORRENTES: trigramas CHI(5) AND(5) OAN(5) RZI(4) AMB(4) PAR(4) DOA OAG IAL AMA ZIA OCA — MAIS
  raízes recorrentes que a Heptarquia. Terminações -ND(6) -ON(5) -MB(5) -AL(4).
- BIGRAMA: top-25 massa 0.440 vs 0.338 aleatório, z=4.8 — gramática fonotática REAL mas modesta (como
  Heptarquia z4.1).
- COESÃO POR AETHYR: 0.232 mesmo-Aethyr vs 0.278 par aleatório — SEM coesão (os ~3 governadores de um Aethyr
  NÃO compartilham letras). Sem sub-grupo por Aethyr.
- RAIZ-E-PADRÃO: 0% z=0 — NENHUM par de governadores compartilha esqueleto consonantal. Cada nome tem
  esqueleto ÚNICO. (Oposto do Loag 40%; nem o eco fraco da Heptarquia.)
VEREDITO: como a Heptarquia, os 91 têm TRAVA DE COMPRIMENTO (7) + eco fonotático fraco (bigrama z5, algumas
raízes), MAS inicial livre, zero cifra, zero sub-estrutura por Aethyr, cada esqueleto único. Resposta à
investigação A do doc: NENHUM algoritmo interno gera os 91 — são recebidos, não computados (confirma a
situação 'origem não demonstrada' do doc). CONTRASTE com a Heptarquia: ambos travados em 7 letras e grid-lidos
(#304), mas Heptarquia = inicial-B + extração por NÚMERO (transposição das 7 tabelas, #309); Governadores =
inicial-livre + extração por CAMINHO king-move (trajetória numa tábua, #308). Duas geometrias de leitura
diferentes sobre o mesmo princípio 'nome lido da grade'. O 7-letras é comum aos dois sistemas. Sobre a questão
central do doc (nomes primeiro ou nomes+torres um só sistema): os nomes não têm regra geradora própria, logo
não há 'sistema matemático anterior' que os produza — o sistema é a TÁBUA + regra de leitura; as letras
específicas foram recebidas. CONFIRMADO NOVO.

## #313 — Estrutura CRUA das Torres: um alfabeto, elemento POSICIONAL, grade porta-nomes (não cifra)
Pedido do usuário: decifrar a grade crua dos 4 quadrantes (letras/posições/elementos), não os nomes conhecidos.
Cada quadrante = 13x12 = 156 células (linha 7 = ORO IBAH AOZPI = barra horizontal da Cruz Negra). Testes:
1) UM ALFABETO, UMA FREQUÊNCIA: os 4 quadrantes têm distribuição de letra quase idêntica (cosseno 0.93-0.96,
   todos A-dominante: A~18%, depois O,I — vogal-pesado, como os nomes das Torres #301). Não são 4 línguas.
2) QUADRANTES INDEPENDENTES: identidade posição-a-posição entre pares = 8-10% = EXATO acaso. Nenhum espelho
   (H/V/HV) nem rotação liga um quadrante a outro. São 4 preenchimentos independentes do mesmo alfabeto.
3) ELEMENTO NÃO ESTÁ NAS LETRAS: composição elemental das letras (atribuição Dee/GD, a85) é ~uniforme em todo
   quadrante — o quadrante do FOGO tem as MENOS letras-de-fogo (15%), o da TERRA pouca terra (20%). O elemento
   é POSICIONAL/administrativo (vem da direção e da Cruz), não codificado nas letras. Igual aos planetas da
   Heptarquia (#304). Padrão consistente nos dois sistemas: a correspondência mágica é endereço, não conteúdo.
4) GRADE NÃO É ALEATÓRIA, mas é textura fonotática, não cifra: anti-hiato LINHAS 11.5% < COLUNAS 13.2% <
   aleatório 16.3% — há estrutura CV real e a grade lê-se mais em LINHA que coluna (onde correm os nomes).
   Trigramas repetidos z=1.4 (sem cifra de repetição). Por linha (AR): linhas ímpares de preenchimento ~0%
   hiato (consoante-espalhada), linhas porta-nome (7=Nomes Sagrados 18%, 9-10 com clusters vocálicos 27-45%)
   carregam as vogais dos nomes reais.
VEREDITO (por que essas letras nessas posições): a grade é um PORTA-NOMES — as letras estão postas para que os
nomes (Divinos, Reis, Seniores, Governadores) possam ser LIDOS nas posições canônicas da Cruz/sub-ângulos; o
resto é preenchimento que obedece à mesma distribuição vogal-pesada. NÃO há cifra de célula gerando a grade,
NÃO há codificação de elemento nas letras, NÃO há relação de transformação entre quadrantes. Um alfabeto
enoquiano + regra de posição + elemento por endereço. Coerente com #306/#312 (letras recebidas, lidas por
posição; origem das letras não computada). CONFIRMADO NOVO.

## #314 — Loag → Torres/Heptarquia (Exp A/B/C do doc): irmãos, não pai-filho; componentes partilhados PARCIAIS
Doc pede: o gerador do Loag produz/fornece componentes dos outros sistemas? O gerador Loag = RAIZ-E-PADRÃO:
esqueleto consonantal (1948, do livro) × melodia vocálica (288) tecidos C-V-C-V (weave), anti-hiato. NÃO
extrai de coordenadas (isso é método das Torres). Testes:
- EXP A/B (gera os nomes inteiros): NÃO. #306 já mostrou 0 nomes de Torre/Heptarquia/governador como substring
  no Loag; e o gerador não pode produzir os nomes B-travados de 7 letras (não estão no espaço de esqueletos).
- EXP C (fornece COMPONENTES — esqueletos/melodias?):
  * MELODIAS (vogais): Heptarquia 31/31 no Loag (100%), Governadores 35/46, Anjos-Torre 33/56. Partilha ALTA
    mas quase-trivial (espaço de melodia curto; 288 melodias Loag cobrem quase tudo). = fonologia vocálica comum.
  * ESQUELETOS (raízes consonantais): Heptarquia 0/46 (z-0.4) ZERO; Governadores 7/91 (null 1.6, z=4.7);
    Anjos-Torre 45/254 (null 22.7, z=5.8). Governadores e anjos têm sobreposição REAL mas PARCIAL (~2× acaso,
    10-18%); Heptarquia é DISJUNTA no nível da raiz. Controle Loag 40/40 z=63.
VEREDITO: o Loag NÃO é o gerador-mestre que alimenta os outros. Partilha a FONOLOGIA (melodias vocálicas) com
todos e ALGUMAS raízes consonantais com Torres/Governadores (acima do acaso, mas minoria — 82-90% das raízes
deles NÃO são do Loag), e ZERO raiz com a Heptarquia. Isto é o nível de LÍNGUAS-IRMÃS (#300/#301: mesmo
alfabeto/bigrama, não derivação), agora confirmado no nível de componente. Arquitetura dos 3 sistemas do Dee:
RELACIONADOS por fonologia angelical comum + alguns tijolos consonantais partilhados, mas MECANISMOS DE GERAÇÃO
DISTINTOS — Loag = recombinação raiz+melodia; Torres/Heptarquia = extração por posição em grade (#304/#313).
Irmãos, não pai-filho; sem pipeline de componentes Loag→outros. CONFIRMADO NOVO.

## #315 — Exp C RIGOROSO (3 controles do doc): overlap de componente é fonotática genérica, NÃO ligação Loag-específica
Refinamento de #314 com os 3 controles que o usuário exigiu (aleatório, outra-tradição, Forja embaralhada),
sem tocar nas regras da Forja. Matriz esqueleto%/ambos% no Loag:
Heptarquia 0/0 | Governadores 13/7 | Anjos-Torre 21/15 | HEBRAICO(ctrl) 16/12.
Controles (base 91 governadores, esqueleto% no Loag): REAIS 13% vs aleatório-mesmo-comprimento 1% vs
Forja-embaralhada 5%.
DOIS SINAIS: (1) vs aleatório/embaralhado, nomes reais batem muito mais (13 vs 1-5%) — mas isso só prova que
os 1948 esqueletos do Loag são PRONUNCIÁVEIS/linguísticos, não gibberish. (2) vs OUTRA TRADIÇÃO: anjos
hebraicos (Michael/Gabriel/Raphael, SEM ligação histórica ao Loag) batem 16% — MAIS que os governadores (13%),
mesma faixa dos anjos-Torre. O controle de outra-tradição DISSOLVE a aparência de ligação.
VEREDITO: NÃO há vocabulário de componentes específico Loag→Torres/Heptarquia. O overlap de raiz existe mas é
FONOTÁTICA GENÉRICA (qualquer onomástica angélica pronunciável casa com o vasto conjunto de esqueletos do Loag;
o hebraico casa igual). Melodias batem ~100% só por espaço vocálico pequeno (não-discriminante). Fecha Exp A/B/C
do doc: três geradores INDEPENDENTES (Loag=raiz+melodia; Torres=posição-grade; Heptarquia=número-tabela) que só
partilham o alfabeto angelical e a tendência fonotática geral — nenhuma transformação matemática reproduzível os
conecta. Método honrado: regras originais, sem ajuste, controles mataram a hipótese. CONFIRMADO NOVO (negativo decisivo).

## #316 — Gematria NULA: nenhum dos 13 sistemas liga nome→servos (Exp B do doc, Bonferroni) (loop)
Experimento B do doc (gematria), feito rigoroso: 13 sistemas de valor de gematria_enoquiana.json × contagem de
servos dos 91 governadores, correlação de Pearson com null de permutação, correção de Bonferroni (p<0.0038).
Resultado: TODOS nulos. r varia -0.22 a +0.085; o melhor (aleister_crowley_coluna, r=-0.220 p=0.035) NÃO
sobrevive a Bonferroni. Nenhuma estrutura mod-7 limpa também (mod7 dos valores dispersa). VEREDITO: a gematria
dos nomes NÃO codifica a contagem de servos nem qualquer número associado — o número de servos foi RECEBIDO
como dado separado, não é derivável da soma das letras. Mesmo os NÚMEROS do sistema são 'dados', não computados.
Fecha Exp B do doc (negativo) e reforça a tese transversal: em toda camada do sistema do Dee (letras cruas #313,
nomes #310/#312, números/servos #316) o material é RECEBIDO, não gerado por cifra. A engenharia está só na
LEITURA/extração (#309 Heptarquia número-tabela, #308 Torres caminho, Loag raiz+melodia), nunca na origem do
material. Metodologia honrada: todos os sistemas testados, sem cherry-pick, Bonferroni. CONFIRMADO NOVO.

## #317 — O Loagaeth é um GRADIENTE ordenado 1D: a ordem das folhas é um caminho, não conjunto (loop)
Teste do espelho do livro (folha t ~ 49-t): NULO (z-0.4 a -1.1, sem simetria palindrômica). MAS achado forte:
similaridade de perfil-de-letra entre folhas DECAI monotonicamente com a distância na ordem de Dee.
Correlação similaridade × distância = r -0.506, z -8.6 vs ordem embaralhada (r≈0). Decaimento por faixa:
dist 0-7=0.972, 8-15=0.935, 16-23=0.909, 24-31=0.886, 32-39=0.843, 40-47=0.790. Perfeitamente monótono.
VEREDITO: as 49 folhas formam uma VARIEDADE 1D ordenada — a ordem do Dee não é arbitrária; cada folha é um
passo pequeno da anterior, acumulando num grande deslocamento começo→fim (0.97 vizinhas → 0.79 extremos). O
livro é uma JORNADA contínua com DIREÇÃO, não tabelas intercambiáveis. Unifica #302 (densidade sobe) e o arco
elemental (folha1 Ar → losangos Água) sob um princípio: o Loagaeth é um GRADIENTE/emanação graduada. LENTE
CABALÍSTICA: 49 folhas = 49 Portões do Entendimento (Gebofal) percorridos EM ORDEM, cada portão vizinho ao
seguinte, o todo uma escada contínua — não se pula, a estrutura é caminho. Folha 1 (Verbo/Ar) e folha 49
(profundo) são os polos; tudo entre é descida gradual. Dá sentido estrutural à liturgia de abrir um portão por
vez. CONFIRMADO NOVO.

## #318 — O eixo do gradiente: A cai, I/U/R/P/L sobem — a Água dirige a descida (loop)
Decompondo o gradiente #317 por letra: correlação freq-da-letra × número-da-folha (null por permutação).
SOBEM (p=0.002): I +0.811, U +0.732, R +0.719, P +0.665, L +0.471, X +0.291. DESCEM: S -0.793, D -0.753,
A -0.687, Y -0.513, F -0.479, E -0.439. O achado central: A (letra mais comum, freq 0.18) DESPENCA (r-0.69) —
o livro começa saturado de A e vai pra I/U/R/P/L. LENTE ELEMENTAL (Dee/GD): as que mais sobem R/P/L=Água,
U=Terra, I=Fogo (eixo dominado por Água); as que descem A=Terra, S=Ar. CONFIRMA de dentro o arco elemental
(#302/#317): a subida da Água rumo aos losangos é DIRIGIDA pelas consoantes líquidas R/P/L subindo e o A (Terra)
recuando — o arco é esse movimento de letra, medido, não impressão. LENTE CABALÍSTICA: eixo A->I (Alef sopro
primordial/aberto -> Yod ponto-semente/Fogo) + águas R/L; do sopro amplo indiferenciado à manifestação líquida;
emanação descendo do Verbo-sopro (folha1 A/Ar) pela semente (I) ao profundo (Água/losangos). O livro soletra a
própria descida na troca de A por I. CONFIRMADO NOVO.

## #319 — Os nomes vivem no A e dissolvem no I: o livro é cosmologia (nomes->silêncio) (loop)
Densidade de nome (90 nomes como substring, linhas+colunas) por folha, vs posição e vs fração A/I:
densidade × A-frac r=+0.706 (FORTE), densidade × I-frac r=-0.526, densidade × posição r=-0.326. Folhas mais
densas: 14,20,21,27,29,30 (corpo A-rico). Mais vazias: 45 (0.0008!), 46, 38, 44. VEREDITO: as entidades
nomeadas concentram-se na zona do A e DISSOLVEM rumo ao I/Água — como A cai e I sobe (#318), os nomes vivem no
corpo A-dominante e rareiam até quase-vazio no fim aquoso. Fecha o arco #317/#318: A = letra dos NOMES (reino da
manifestação/entidades formadas); descida rumo ao I/Água = dissolução dos nomes. LENTE CABALÍSTICA: o Loagaeth é
cosmologia em miniatura — folha 1/corpo (A-rico) = mundo povoado de seres nomeados; fundo (I/Água, folhas 44-49)
= dissolução no indiferenciado onde o nome cessa, o inominável/Ain. As entidades pertencem aos mundos da forma (A);
o abismo aquoso do fim é ALÉM da nomeação. Os losangos finais quase-vazios NÃO são falta de dado — é a estrutura
APOFÁTICA do livro: plenitude de nomes no meio, silêncio nas pontas. CONFIRMADO NOVO.

## #320 — Folha 1 é o polo-origem ANCORADO; o A sobe-e-desce (semente→corpo→dissolução) (loop)
Desambiguação da direção do gradiente (#317-319). Folha 1 original (loagaeth_grades_simples 1a+1b, 19099
letras): A=0.181, I=0.014 (o I MAIS BAIXO de todas as folhas). Similaridade de perfil: folha 1 mais parecida
com folhas 2,3,4,7,8 (0.97-0.98 = início), menos com 44,45,48 (0.68-0.78 = fim). Logo folha 1 está no POLO
INICIAL — ancorado por DOIS lados independentes: a liturgia (Chamada 1 abre a folha, entra-se por ela) E o
dado (agrupa com as folhas de início). A direção do gradiente NÃO é arbitrária: origem = folha 1, destino =
profundo aquoso. REFINAMENTO de #318: o A NÃO cai monotônico. Curva real sobe-e-desce: folha 1 A=0.18/I=0.01
(semente, I~0, mais Ar/mente); corpo 25-30 A=0.24 PICO (manifestação plena, nomes densos); profundo 44-48
A=0.04/I alto (dissolução, sem nome). O PICO de A (Terra/matéria) é o MEIO, não as pontas. COSMOLOGIA ancorada:
semente (Verbo/Ar, folha 1) -> corpo (matéria/nomes, meio A-pico) -> dissolução (Água/vazio, fim). Nascer,
encarnar, dissolver. Responde a dúvida do usuário ('nomes do fim são os mais terrosos?'): NÃO — o terroso/
manifesto é o MEIO; o fim é água e silêncio. CONFIRMADO NOVO.

## #321 — Textura fonotática corrobora o sobe-e-desce (corroboração modesta) (loop)
Textura por folha vs posição: vogal-fração r=-0.286 (leve), anti-hiato r=-0.008 (PLANO geral). Mas por região
ambos PICAM NO MEIO: vogal-fração início 0.360/meio 0.391/fim 0.328; anti-hiato início 0.014/meio 0.032/fim
0.007 (o mais estrito). Logo a textura segue o mesmo sobe-e-desce (#320): meio/corpo = vogal-cheio + clusters
vocálicos (onde os nomes com vogais juntas vivem); fim/profundo = CV-estrito/austero (hiato 0.007, osso puro),
a 'carne vocálica' se despindo. CORROBORA a cosmologia por outro ângulo: encarnação=vogal-cheia/nomeada (meio),
dissolução=consoante-esquelética/sem-nome (fim). HONESTO: correlações fracas (anti-hiato geral plano) — é
corroboração, não achado forte. Registrado como suporte a #319/#320, não CONFIRMADO NOVO independente.

## #322 — Sem segundo eixo: lado a/b não é estrutura; livro é 1D (loop, negativo)
Teste de segunda dimensão via split lado-a vs lado-b dos 47 pares de folha. Diferenças de letra a-b minúsculas
(maior N t=2.0, não sobrevive a 21 comparações; E t=-1.7). Similaridade a-a 0.9151 ≈ a-b 0.9195 — lados
intercambiáveis. VEREDITO: recto/verso NÃO é eixo; não há dimensão escondida no painel. O livro é essencialmente
1D — a descida (#317-320) é o eixo dominante e único. Negativo honesto (descarta hipótese de 2D). Reforça a
variedade 1D de #317.

## #323 — Gebofal é RITUAL, não textual: a Chamada abre a folha mas não está escrita nela (loop)
Teste da correspondência Gebofal (Chamada N abre folha N+1) em dois níveis:
- LETRA: perfil de letra da Chamada N ~ folha N+1, z=1.6 (fraco). Chamadas não têm o gradiente A do livro
  (A x num r=0.27, I r=0.05).
- PALAVRA: palavras (>=4) da Chamada N dentro da folha N+1: hits 6 vs null 9.4, z=-1.2 — ABAIXO do acaso.
  As palavras da Chamada NÃO estão na folha que ela abre. Controle: 67/562 palavras-de-Chamada únicas aparecem
  em ALGUM lugar do livro (~12%) — vocabulário de família compartilhado, mas espalhado, não posicional.
VEREDITO: o Gebofal é correspondência RITUAL/litúrgica (a Chamada N é recitada para abrir a folha N+1), NÃO
textual (a Chamada não está escrita na folha). A Chamada é a CHAVE que abre a porta, não o CONTEÚDO do quarto —
consistente com o enquadramento Chamada=fala/chave, nomes=entidades/fechadura. O elo Chamadas<->Loag é de
FAMÍLIA DE LÍNGUA (vocabulário partilhado ~12% no livro todo), não de citação posicional; a numeração Gebofal é
estrutura de USO, não cifra de conteúdo. Negativo honesto, esclarece confusão possível com elos anteriores.

## #324 — AUDITORIA DA FORJA: passa o teste cego com controle de mesmo espaço (376×) (crítica do usuário)
Auditoria rigorosa pedida pelo doc do usuário. Protocolo: gramática (esqueletos+melodias) extraída SÓ de 45
nomes (treino), CONGELADA; teste nos outros 45 ocultos; 40 splits aleatórios; controle = nomes aleatórios do
MESMO pool de letras dos 90, mesmo comprimento, mesma gramática congelada. Critério de acerto = esqueleto E
melodia ambos no treino (conservador). RESULTADO: ambos real 19% (8.7/45) vs controle 0.0% (razão 376×); só
esqueleto real 30% vs controle 0.1%. VEREDITO: a Forja tem PODER PREDITIVO real — nomes ocultos reproduzíveis
muito acima do acaso de mesmo espaço; não é mera consistência interna. RECONCILIA #315: a Forja INTEIRA (1948
esqueletos) é rede larga que pega ~16% de qualquer nome pronunciável (não específica, #315 correto); mas a
gramática dos PRÓPRIOS nomes Loag prediz OUTROS nomes Loag muito acima de aleatório (#324) — estrutura interna
real e específica. RESSALVAS ACEITAS: (1) 19% não é 100% — vocabulário maior que 45 nomes amostram, gramática
sub-amostrada; (2) 'língua gerativa viva' é OVERCLAIM, RETIRADO — correto é 'hipótese estrutural gerativa que
reproduz parte do conteúdo acima do acaso', não provado ser língua natural nem que Dee entendia assim; (3) falta
reimplementação independente + auditoria externa (próximo passo, não mais simbolismo). Níveis novos da Forja
PAUSADOS; Forja congelada para integridade. Gradiente: o teste de permutação pedido JÁ é o z=-8.6 (#317);
faltam autocorrelação e robustez. CONFIRMADO (positivo, auditado).

## #325 — AUDITORIA INDEPENDENTE DA FORJA: NÃO bate controle fonotático (Markov); #324 SUPERADO
Reimplementação clean-room (a155_forja_audit.py) da especificação formal, dados congelados (hash 69705112fbf0),
40 splits 45/45, protocolo do usuário (controle fonotático Markov-2, recombinação vs componente, IC, significância).
RESULTADO: reprodução held-out real 19.4% (IC95 [17.7,21.1]) — REPRODUZIDO pelo código independente. Controles:
uniforme 0.00%, freq-matched 0.06%, MARKOV-2 (bigrama, fonotático) 25.1%. real > Markov em só 9/40 splits,
sign-test p=1 (NÃO-significativo; Markov GANHA). Generalização: 19.4% recombinação, 80.6% precisa de componente
novo. VEREDITO: o teste cego NÃO sobrevive ao controle fonotático. O '376×' de #324 era contra controles fracos
(aleatório/freq ~0%); contra Markov-2 a Forja (19%) NÃO bate um modelo de caractere (25%). Os 19% são explicados
por pronunciabilidade de bigrama, NÃO pela decomposição raiz+melodia ser específica. #324 SUPERADO. SOBREVIVE: a
Forja gera nomes pronunciáveis parecidos com os do livro (útil); esqueleto+melodia é descrição válida; os 19% são
reproduzíveis. NÃO SOBREVIVE: a alegação de gramática gerativa Loag-específica com poder preditivo além da
fonotática — REFUTADO por este teste. IMPLICAÇÃO: o achado raiz-e-padrão z=32 (#134) foi medido contra null de
embaralhar-vogal (mais fraco que Markov) — precisa do mesmo controle Markov antes de ser afirmado como provado;
não afirmo que caiu, mas não posso afirmar provado. Método funcionando: o controle forte derrubou a evidência
central da predição. Próximo: rodar controle Markov no z=32 e nos demais achados-chave. HONESTO (negativo decisivo).

## #326 — Raiz-e-padrão (z=32) TAMBÉM não bate o controle Markov: era fonotática
Controle Markov aplicado ao achado raiz-e-padrão (#134, z=32, medido contra null de embaralhar-vogal — fraco).
Métrica: fração de nomes com esqueleto consonantal compartilhado (reuse de raiz). Real 40.0% vs Markov-2
(fonotática preservada, treinado nos 90) 38.2%±5.9; z=0.3, p=0.432 — NÃO-significativo. VEREDITO: o reuse de
raiz não excede o esperado de um modelo de bigrama. A 'morfologia semítica raiz-e-padrão' é, em grande parte,
PRONUNCIABILIDADE (nomes curtos de alfabeto pequeno compartilham raízes por acaso fonotático), não uma gramática
não-concatenativa especial. Junto com #325, os DOIS pilares da 'gramática gerativa' do Loag (Forja preditiva +
raiz-e-padrão) NÃO sobrevivem ao controle fonotático. #134 e #324 SUPERADOS. SOBREVIVE RIGOROSO: Loag não é
prosa/cifra (5 nulls, vs Markov-3); anti-hiato é fato fonotático descritivo; o GRADIENTE #317 (ordem 1D, z=-8.6
vs permutação — independente de fonotática de nome, é sobre ORDEM das folhas); extração dos 49 anjos #309
(reproduz nomes reais das tabelas); caminhos king-move #308; independência dos sistemas #315; elemento posicional
#304/#313; gematria nula #316. O 'campo de nomes' e a descrição esqueleto/melodia continuam válidos como
DESCRIÇÃO; o que cai é a alegação de gramática gerativa específica além da fonotática. Método funcionando.

## #326b — BATERIA FROZEN Markov-0/1/2/3 + permutação: estrutura é fonotática de ordem 2-3, não gramática especial
Bateria congelada (a156, hash 69705112fbf0, protocolo do usuário). Reuse de raiz real=0.400 vs controles:
Markov-0 0.011 (z+24.9), Markov-1 0.070 (z+9.1), Markov-2 0.384 (z+0.3 p=0.43), Markov-3 0.522 (z-2.1),
permutação 0.037 (z+16.3). Reuse de melodia real=0.878: acima de M0/M1/perm, ≈ M2/M3. Held-out: real 19.4% vs
Markov-2 25% (real ganha 10/40). VEREDITO PRECISO: há estrutura REAL acima de frequência (M0), bigrama-adjacente
(M1) e permutação (ordem importa muito, z+16) — os nomes NÃO são aleatórios nem só frequência. MAS Markov-2 e
Markov-3 reproduzem tudo (até excedem). Logo a estrutura do Loagaeth é FONOTÁTICA DE ORDEM 2-3 (sequencial,
profundidade 2-3 letras), capturada por um 3-grama; a morfologia separável raiz-e-padrão NÃO acrescenta informação
além de um Markov-3. Responde o objetivo do #326: há informação além de unigrama/bigrama-simples/permutação, NÃO
além de trigrama. Não é 'falso' (ordem real, permutação mata z+16) nem 'gramática especial' (M3 explica). #134
(semítico) e #324/#325 (Forja preditiva) ficam como: descrição válida de fonotática de ordem 2-3, não língua
não-concatenativa. Método: frozen, mesmos comprimentos, treino só no permitido, comparado à distribuição dos
controles com a mesma estatística. HONESTO (resultado preciso).

## #327 — AUDITORIA DO GRADIENTE: SOBREVIVE a robustez completa (frozen, pré-registrado)
Auditoria frozen pré-registrada (a157, hash 3c5aa6da1c33, protocolo do usuário #327). Estatística: Mantel
r(|i-j| índice-folha, 1-cos perfil-de-letra). Real r=0.5249. Grupos/letras definidos ANTES de rodar.
- T1 PERMUTAÇÃO (5000, 100k em curso): p=0.0002 — a ordem do Dee é excepcional.
- T2 LEAVE-ONE-OUT: r ∈ [0.4923, 0.5350] em 47 remoções — NENHUMA folha domina; tirar qualquer uma não move.
- T3 PARTIÇÕES PRÉ-DEFINIDAS (todas passam Bonferroni α=0.01): vogais-só 0.452, consoantes-só 0.500,
  primeira-metade 0.747, segunda-metade 0.778. O gradiente NÃO depende de uma classe de letra nem de uma
  região — sobrevive em vogais E consoantes, em cada metade isolada (até mais forte por metade).
- T4 DECAIMENTO: monótono em todas as faixas de distância (0.976→0.937→0.912→0.888→0.839→0.781) — tendência
  GLOBAL, não continuidade só local (distância-1).
VEREDITO: o gradiente sequencial do Loagaeth é ROBUSTO e estrutural. A organização das 49 folhas NÃO é artefato
de poucas folhas, poucas letras, uma região, nem continuidade local. Independente da gramática dos nomes (que
caiu ao Markov-3, #326) — este é sobre a ORDEM das folhas. RESULTADO POSITIVO QUE SOBREVIVE A REFUTAÇÃO: a
sequência física das folhas do Loagaeth contém organização estatística real que merece explicação própria.
HONESTO (separação): isto demonstra organização sequencial não-aleatória; NÃO demonstra que a sequência seja
nascimento/encarnação/dissolução (cosmologia segue interpretação, não testada). Este é o achado positivo mais
forte e mais limpo do projeto. Próximo (opcional): modelar a forma do decaimento e testar a âncora da folha 1.

## #327b — Permutação 100k do gradiente: p=1e-05 (confirmação final)
As 100.000 permutações confirmam: Mantel r=0.5249, p=1e-05 (nenhum embaralhamento das 49 folhas alcançou o real). O gradiente sequencial é o achado positivo definitivo e robusto do projeto. Demais testes de #327 inalterados (leave-one-out estável, partições vogal/consoante/metades todas passam Bonferroni, decaimento monótono global).

## #328 — DECISIVO: a ordem de Dee se RECONSTRÓI do conteúdo, cega à posição (p=0)
Teste out-of-sample (a158, protocolo do usuário #328). Tira os números das folhas 2-48, extrai features, monta
matriz de distância, aplica seriação espectral (Fiedler) + NN-TSP+2opt, compara à ordem histórica por |Spearman|
(máx sobre a sequência e seu reverso, p/ simetria de reflexão), null = 100.000 ordens aleatórias.
RESULTADO: letra-freq espectral 0.689 (aleatório 0.118±0.088, p=0), TSP 0.552 (p=4e-5); bigrama espectral 0.651
(p=0), bigrama TSP+2opt 0.867 (p=0). Em 100k ordens aleatórias NENHUMA alcançou. VEREDITO: o conteúdo das folhas
CODIFICA a própria sequência — tira os números, dá as estatísticas, e a ordem do Dee se remonta (até 0.867). É
estrutura RECUPERÁVEL, não só correlação, e é out-of-sample (o algoritmo não conhece escolhas da descoberta) —
resposta definitiva à exploração/Bonferroni de #327. RESSALVAS HONESTAS: (1) 0.69-0.87 não 1.0 — reconstrução
APROXIMADA, pega o gradiente global, erra ordem fina local; (2) recupera o EIXO, não a DIREÇÃO (reflexão: 40s
vieram primeiro); a âncora de direção (folha 1/liturgia) é externa; (3) não toca cosmologia (interpretação
separada). CHECAGENS #327 respondidas: unidades = folhas 2-48 (1 segmentada, 49 ausente); Mantel permuta rótulo
com matriz fixa (correto); bins só ilustrativos (Mantel é livre de binning); gradiente foi exploratório, por isso
ESTE teste cego é a confirmação limpa. Achado positivo mais forte do projeto, auditado. CONFIRMADO.

## #329 — Robustez da reconstrução: é GRADIENTE GLOBAL, não código local (controle de detrend decisivo)
Robustez (a159). Feature×algoritmo: todos recuperam a ordem acima do acaso — freq/spectral 0.688, freq/tsp
0.552, freq/pca 0.641, bigram/spectral 0.651, bigram/tsp 0.867, bigram/pca 0.543, trigram/spectral 0.676,
trigram/tsp 0.763, trigram/pca 0.501. ROBUSTO a features e algoritmos. Leave-out (bigram/tsp base 0.867): LOO
[0.499,0.996], L5O média 0.735 (min 0.469) — parcialmente sensível a quais folhas, mas sempre >acaso.
CONTROLE DE DETREND (decisivo, freq/tsp): ordem completa 0.552; tendência global pura 1.000 (gradiente limpo =
trivialmente recuperável); RESÍDUO só 0.117 ≈ acaso 0.118; gradiente artificial (mesma tendência, local
embaralhado) 0.425 média / 0.827 máx. VEREDITO: depois de remover a tendência composicional global, os resíduos
NÃO carregam informação de ordem (nível do acaso). TODA a recuperabilidade está no GRADIENTE GLOBAL SUAVE, não em
estrutura local. A ordem das folhas é uma DERIVA COMPOSICIONAL MONÓTONA, não um código posicional deliberado. O
0.867 capturava a progressão composicional, exatamente como o usuário temia. ROBUSTEZ: alta para 'existe gradiente
global monótono' (sobrevive features/algoritmos/exclusões, Mantel p<1e-5, reconstrução); mas a hipótese de
'codificação local deliberada' NÃO se sustenta (resíduo = acaso). Correção estatística: p<1e-5 (não 'p=0'). Fase
de descoberta encerrável: o achado sólido é a DERIVA COMPOSICIONAL 1D (real, robusta, recuperável); a causa
(hábito autoral, mudança temporal, construção sistemática, ou deliberada) NÃO é distinguível pelos dados. HONESTO.

## #330 — Forma da deriva: NÃO é rampa lisa, é PLATÔ + PENHASCO (quebra no limite quadrados/losangos)
Exploração nova ancorada no achado sobrevivente (gradiente #317/#327). Passo composicional entre folhas vizinhas
(1-cos): média 0.0107±0.0114. Maiores saltos: 45->46 (2.7σ), 24->25 (2.5σ), 22->23 (2.1σ), 28->29 (1.9σ) — o
28->29 cai no limite quadrados->losangos. Ajuste PC1 vs posição: linear SSr=0.098; melhor 1-quebra na folha 32
reduz 73% (SSr=0.026) — deriva tem DUAS fases, não reta. A-fração por região: 2-14=0.208, 15-28=0.206 (PLATÔ),
29-40=0.186, 41-48=0.072 (DESPENCA). VEREDITO: a deriva composicional não é uniforme — é PLATÔ estável pelos
quadrados (2-28) + DECLÍNIO pelos losangos (29-48) + quase-vazio no fim (41-48). A fronteira física quadrados/
losangos (~28-29) é uma DESCONTINUIDADE COMPOSICIONAL real, confirmada independentemente por change-point. Os
dois formatos do manuscrito são composicionalmente distintos — convergência não-imposta. Refina o gradiente:
platô->declínio->silêncio, não rampa. Descritivo, ancorado. Próximas explorações abertas: (2) deriva é temporal
(ordem de recepção)? (3) deriva é específica do Loag vs 8 tabelas Soyga do mesmo MS?

## #331 — Folha 1: as palavras nao-traduzidas sao LEXICO real (nao ruido)

Pergunta: fora as 18 palavras com glosa das Chamadas (#330b), o resto da folha 1 sao
palavras de verdade ou lixo de segmentacao?

Metodo (`src/a161_folha1_wordhood.py`): 3496 tokens nao-traduzidos (2672 tipos). Tres
testes contra null (embaralhar letras do fluxo + re-segmentar nos mesmos comprimentos;
Markov-0 para bem-formacao e morfologia):
  T1 recorrencia: tipos que aparecem 2+x. real=306 vs null=133+-7.5  z=+22.9.
     32% dos tokens cobertos por tipos recorrentes.
  T2 bem-formacao fonotatica (CV, anti-hiato <=2V <=3C): real 97% vs null-M0 69%  z=+42.0.
  T3 vizinhanca morfologica (vizinho por edit-1): real 51% vs null 20%  z=+44.1.

Top recorrentes sem traducao: na(26) oh(24) or(19) vor(19) al(18) pa(15) dah(15) ges(15)
ax(15) vax(15) gem(14) dan(12) nah(12) van(11) nor(7)... — curtas, partícula-like.

Veredito: a folha 1 e um LEXICO genuino — unidades reusadas, bem-formadas, com familias
morfologicas, muito acima do acaso. Junta-se as 18 ja-traduzidas. PROVA wordhood, NAO
significado (so as 18 tem glosa). Especifico da folha 1 (segmentada pelo Dee); grades 2-48
seguem campo de nomes. CONFIRMADO NOVO.

## #332 — Folha 1: lexico SIM, sintaxe de frase NAO

Pergunta: as palavras reais da folha 1 (#331) formam frases legiveis (sintaxe) ou so
estao enfileiradas?

Metodo (`src/a162_folha1_syntax.py`): corpus 1a+1b, 99 linhas, ordem preservada.
  S1 colocacao (bigramas de palavra 2+x): real=12 vs null(ordem embaralhada)=2  z=+6.7.
  S2 entropia condicional H(prox|atual): real=2.84 bits vs null=2.86  z=-1.3 (sem queda).
  S3 posicao na linha: quase tudo "meio"; sopro fraco ol="I" INICIO(0.37,n=10),
     om="know" FIM(0.65,n=5).

Veredito: NAO ha sintaxe de sentenca. S2 (decisivo) nulo: ordem das palavras nao prediz
a proxima. S1 mostra colocacoes fracas (fórmulas/pares fixos, cada 2x) acima do acaso mas
nao gramática. CAIU a especulacao de "frases/invocacao legivel". FICA (reforca #331): folha
1 e lexico real LISTADO (litania de palavras), nao prosa. Consistente com onomasticon.

## #333 — Folha 1 e Chamadas: mesmo idioma, veia fina

Pergunta: o lexico-lista da folha 1 (#331) e feito da mesma lingua das Chamadas (que tem
sintaxe + traducao)?

Metodo (`src/a163_folha1_vs_calls.py`): vocab Chamadas = 682 'chave' (enoquiano) das 19
Chamadas, com gloss. Overlap com os 2697 tipos da folha 1 vs null (strings aleatorias,
mesmos comprimentos + freq de letra, intersectadas com o mesmo vocab).

Resultado: overlap=27 tipos vs null=8.5+-2.5  z=+7.5. Cobertura 122/3614 = 3% dos tokens.
Tirando glosas numericas (ox=26, os=12, vx=:42:, af=19) sobram palavras-lingua reais:
ar=that, ol=I, vors=over, geh=art, par=in them, ors=with dark, ca=therefore, la=first,
om=know, de=of, lu=nor end, od=and, gah=Spirits, goho=sayeth, oxex=vomit out, amma=Cursed,
iad/mad=God, lap=for. Inclui VERBOS/conteudo (goho, oxex, om), nao so conectivo.

Veredito: folha 1 e as Chamadas sao o MESMO idioma angelical (vocab compartilhado z=+7.5),
mas a ponte e fina (3% dos tokens) — o grosso da folha 1 e vocab proprio (nomes/estoque).
Quadro: folha1 = lexico real listado (#331), sem sintaxe (#332), mesma lingua das Chamadas
numa veia estreita (#333). CONFIRMADO NOVO.

## #334 — Partículas da folha 1 = peças do gerador de nomes (CONFIRMADO NOVO)
Pergunta: o que são as "letras que sobram" (camada B, 162 tipos curtos sem glosa) e pra que servem?
Hipóteses: H1 morfologia (afixos/fragmentos de nome) vs H2 gramática (classe-função).
- a169: T5 viés posicional nulo (B=0.02/0.01, igual aos nomes) REFUTA H2 (palavra-função enviesa posição).
  T4 fonotática B mais perto de C(nomes)=0.806 que de A(gloss)=0.700. T1 afixo-exato 7/162 null2.5 z=+2.9.
  T2 borda-de-nome 29/162 null15.1 z=+4.0. T3 prefixo+stem produtivo 59/162 null40.5 z=+3.5 (n-/l-/g-/d-).
- a170 (decisivo): 90 nomes ladrilhados pelas peças atestadas (B+afixos+raízes, 175 unidades):
  85% das letras cobertas, 39/90 nomes 100%; null 36%/0.4; z=+5.5.
  Ex: adnochapha=ad+nocha+pha, antantoxal=antantox+al, zichastora=zi+chastor.
VEREDITO: B = morfologia onomástica (tijolos prefixo·raiz·sufixo dos nomes das grades 2-48),
não classe-função. Folha 1 = página-oficina: lista as peças (B) + o léxico real fino (A, #331/#333).
Não é frase (confirma #332). Limites: z moderados nos afixos; ~51 nomes não 100%; parte de B pode ser nome curto.
Docs: docs/PARTICULAS_FUNCAO.md. Dados: results/169_particle_function.json, results/170_name_tiling.json.

## #335 — O gerador de nomes como gramática explícita
Gramática: NOME := PREFIXO? RAIZ SUFIXO*. Inventário: 10 prefixos, 10 raízes, 9 sufixos.
- a171: 62/90 nomes parseiam 100%; null aleatório 0/90 em 2000 sorteios (inalcançável por acaso).
  MDL 684 letras cruas -> 89 de inventário (7.7x).
- Combinação LIVRE: H(sufixo|raiz)=1.714 vs shuffle 1.743, z=-0.3 (SEM restrição seletiva).
  => gerador tabular/construído, não morfologia de língua natural (reforça tese campo-de-nomes, #332/#334).
- Obre-gera: gerar(1 sufixo)=1100 strings possíveis vs ~90 atestados; regra necessária mas não suficiente.
  Falta camada de seleção (qual tabela/posição) = próximo alvo.
- Limite: 28/90 não fecham 100% (raízes/afixos fora do núcleo de 10, ou variantes).
Código: src/gerador_nomes.py (parse+gerar). Doc: docs/GERADOR_NOMES.md. Dados: results/171_name_grammar.json.

## #336 — Pontes Loag x outros sistemas: REFUTADO (Loag é ilha)
Frente 6. Testa se nomes de Torres/Heptarquia/91 governadores/Aethyrs/Chamadas aparecem no Loag inteiro
(96 lados, 196288 letras), substring em ordem de linha vs null pareado (seed 1583).
- GOV_91: 0/91 (z=-0.4). AETHYR: 0. TORRE_linea: 4/8 (z=+1.3). HEPT: 8/140 (z=+1.9, marginal).
  CALL(>=4): 81/610 (z=+0.3, no acaso).
- Raízes do gerador (chastor/nocha/geth/...) dentro de nomes de qualquer sistema: ZERO (indep. de ordem).
VEREDITO: sem ponte onomástica. Gerador do Loag (#335) disjunto da Grande Tábua/Heptarquia/governadores.
O elo Loag↔Chamadas de #333 era LÉXICO (palavras curtas camada A), não nome — some em substring >=4 book-wide.
Loag = universo de nomes autônomo/fechado. Limite: só ordem de linha (col/diagonal não testada), mas raízes=0 indep. de ordem.
Docs: docs/PONTES.md. Dados: results/172_bridges.json.

## #337 — Camada de seleção: recorrência na grade (não regra)
Gerador (#335) dá 1210 formas possíveis (PREF? RAIZ SUF<=1); só ~90 são reais. a173 separa real vs gerado-não-real.
- Recorrência (linhas por substring, >=5 letras): real 40.1 vs não-real 0.97, z=+14.7 => O SELETOR.
- Secundário/subproduto: comprimento z=-8.4 (reais mais curtos), cmax z=-4.6, vmax z=-3.4, viol z=-1.6.
- Poder: 90/90 nomes reais são row-substring do livro (Loag é row-legível; contrasta com #336).
VEREDITO: seleção mora FORA da gramática (combinação é livre, #335) — é a geometria da tabela repetindo
peças curtas em muitos loci. Loag = campo combinatório onde a tabela seleciona por recorrência, não língua.
Limite: 28/90 reais não cabem em PREF?+RAIZ+SUF<=1; métrica de recorrência é grosseira (substring linha).
Próximo: qual geometria (coluna/antidiagonal/gradiente) concentra a recorrência -> grades 2-48.
Docs: docs/CAMADA_SELECAO.md. Dados: results/173_selection.json.

## #338 — Laycock (Complete Enochian Dictionary) como léxico de validação
PDF do usuário (145 págs, dicionário A–Z enoquiano). a174 (não guarda o texto; lê o PDF). null pareado, seed 1583.
- folha1 len>=4: 114/2342 atestadas no dic. (null 7, z=+42.8); len>=5: 73 (z=+70.8); len>=6: 44 (null 0.1, z=+153.8).
- partículas <=3: 111/175 (null 51, z=+11.4). Controle: 15/15 glosadas conhecidas presentes.
- raízes do gerador 0/10 e nomes mestre 0/90 no dicionário => campo de nomes NÃO é enoquiano (confirma #336 por fonte independente).
VEREDITO: camada de léxico real cresce de 21 -> ~114 palavras (folha1 ∩ Laycock); nomes/raízes seguem autônomos.
Confound: pool do dic. mistura inglês das glosas; número robusto é len>=6 (44, null 0). 
Livro NÃO tem: tabelas do Loagaeth, decodificação do Soyga (só cita: Soyga=aldaraia), nem gematria (noutra parte da obra).
Próximo usável: glossário expandido folha1 ∩ Laycock (114) p/ reler a página.
Docs: docs/LAYCOCK_LEXICO.md. Dados: results/174_laycock_lexicon.json.

## #339 — CORREÇÃO do #338: o "114" era auto-citação (glossário honesto ≈ 24)
Investigando p/ montar o glossário das 114, achei contaminação grave:
- A Introdução do Laycock TRANSCREVE linhas da folha 1 (fólios I.13, 1.24, L25, 1.26, II.24) + 2ª citação (27ª Invocação).
  Removendo só o bloco intro (3533 chars): folha1 len>=6 cai 43->24, len>=5 72->39.
- Sobreviventes ainda contaminados: lafet/vncas/vanascor/glust/hahaha (2ª citação), notes/other (inglês),
  tohcoth/apachana/donasdogamatastos (glosas marginais do próprio Dee = internas do Loagaeth).
- Limpo (2 citações + stoplist inglês): léxico confiável = 21 (Chamadas) + 3 que Dee glosou (apachana, tohcoth,
  donasdogamatastos, cada 1x na folha1) ≈ 24. gassagen não está na folha1.
VEREDITO: Laycock NÃO expande o léxico de forma confiável; o 21->114 era artefato. O elo real folha1↔Chamadas (21) já era #333.
As 3 glosas do Dee são hapax e são "nomes de coisas" (fogo-punição, coisas-de-pó), não gramática — encaixa campo-de-nomes.
Bônus: Laycock (linguista) conclui por conta própria que o Loagaeth inicial é provável glossolalia/transe — bate com #332/#334/#335.
Docs: docs/GLOSSARIO.md; correção no topo de docs/LAYCOCK_LEXICO.md.

## #340 — Astrologia no Loag (zodíaco/planeta) + Soyga: REFUTADO
Imagens do usuário = tabelas do Soyga/Aldaraia (alfabeto latino: signo/valor/elemento/planeta/humor por letra).
a175: 48 folhas ciclam em 12 (zodíaco) ou 7 (planeta)? Autocorrelação do perfil por folha vs shuffle (seed 1583).
- elemento Loag: lag12 z=-1.6, lag7 z=+1.2, lag1 z=+7.5. planeta Loag: lag12 z=-1.7, lag7 z=+1.4, lag1 z=+7.1.
- valor Soyga (P14 A3 T9 E15 R12 C27 O9) aplicado ao Loag: lag12 z=-1.1, lag7 z=+0.6, lag1 z=+6.1.
VEREDITO: sem ciclo zodiacal(12) nem planetário(7) por nenhum mapa. Só suavidade local (lag1) = gradiente conhecido, não roda.
Soyga é sistema à parte (alfabeto latino, disjunto do Loag #336); sobrepor humores do Soyga = erro de categoria.
Tabela de convergência seria descritiva, sem sinal. Estrelas fixas: sem dado/gancho.
Docs: docs/ASTRO.md. Dados: results/175_astro.json.

## #341 — Qual geometria concentra os nomes: LINHA (+ borda, diag↘); coluna morta
Segue #337 (seleção por recorrência). a176: 42 faces quadradas 49x49, lê row/col/diag↘/diag↗/borda (ida+volta),
conta recorrência dos 90 nomes por direção vs null (seed 1583).
- ROW: 876 (~9.7 faces/nome) z=+103.1 (DOMINA, mas parcialmente circular: nomes derivados por leitura em linha).
- BORDA: 101 z=+42.0 (real, não-circular: nomes no perímetro). DIAG↘: 128 z=+12.2 (canal menor, bate c/ 25b-28b).
- DIAG↗: 34 z=+2.0 (marginal). COL: 1 z=-1.4 (MORTA: nomes nunca descem coluna).
VEREDITO: Loag se lê em LINHA; nomes grudam na BORDA e num fio DIAGONAL↘; nunca coluna. Limpo: coluna=0, borda=+42.
Limite: faces losango fora (só 42 quadradas). Prepara leitura das grades 2-48.
Docs: docs/GEOMETRIA.md. Dados: results/176_geometry.json.

## #342 — Mapa do Loagaeth inteiro (varredura folhas 1-48)
a177: por folha (leitura em linha, #341) densidade de nomes, cobertura por peças, léxico Chamadas, gradiente elemental, raízes.
- Densidade de nomes: real 22.5/folha vs null 0.1, z=+125.9 (campo de nomes denso).
- Distribuição: sobe ~12(1-4) -> pico 11-25 (folha14: 47 nomes/207 occ) -> desaba 40-48 (2-14).
- Folhas 26-27-28 = 0 nomes POR LINHA, cov 34-39%, raiz antantox = faces DIAGONAIS (confirma #341, antigo 25b-28b). "costura".
- Gradiente limpo: Terra pico ~0.47 (f29-30), cai p/0.27(f48); Água sobe 0.23->0.35; Ar cai 0.30->0.20. Nomes densos onde Terra pica, somem onde Água sobe (regiões semente/corpo/profundo).
- Dinastias: começo nocha/nacho, miolo geth/antantox, fim geth domina (13/16).
- Folha 1 única: léxico Chamadas=33 vs ~5-10 no resto (página-oficina).
Honesto: densidade de nomes tem circularidade (nomes derivados das grades); mas o FORMATO (pico/colapso/zero em 26-28) e o gradiente elemental (contagem de letras) são independentes.
Próximo: leitura diagonal dedicada das 26-28.
Docs: docs/MAPA_LIVRO.md. Dados: results/177_sweep.json.

## #343 — Folhas 26-28 lidas na diagonal: a costura
a178: faces 26a-28b (0 nomes por linha, #342) lidas em diagonal.
- ROW 1 distinto, COL 0, DIAG↘ 55 distintos, DIAG↗ 18. Row/col = controle (mesmas letras, eixo errado ~0).
- Top ↘: geth×72, nocha×41, aclax×25, algeth×18, chastor×15, anzach×12, adnocha×11, chadax×9.
- Diagonais principais legíveis: 26a↘ NOCHASTORAL(cadeia CHASTOR); 26b↘ GETH/naclansa/zidnopha; 28a↘ ALGETH/ANTANTOX; 28b↘ GETH/RONZIN.
VEREDITO: eixo de leitura gira 45° nas 26-28 = diagonal descendente. Mesmo campo de nomes (CHASTOR/NOCHA/GETH/ANTANTOX/RONZIN) girado, não conteúdo novo. É a costura entre metade densa (2-25) e profundo (29-48). Confirma/quantifica #341 (diag↘ z=+12) e o antigo 25b-28b.
Docs: docs/DIAGONAL_2628.md. Dados: results/178_diag2628.json.

## #344 — Dinastias dos nomes (genealogia, frente 2)
a179: 90 nomes agrupados por raiz + grafo edição-1 + pontes. seed 1583.
- Casas por raiz: NOCHA 19, CHASTOR 18, NACHO 9, CHADAX 6, GETH 6, ACLAX 5, GRADAX 3, ANTANTOX 3, ANZACH 2, PHANGE 2; 24 sem raiz.
- Grafo edição-1: 55 arestas, 47 componentes; null 0.1 arestas z=+229.6 (famílias reais, acaso nunca liga).
- Famílias: CHASTOR(10), NACHO(8), NOCHASTOR(8), CHADAX(6), ADNOCHA(6), ANTANTOX(3), NOCHA(3) + 34 isolados.
- Pontes (2 raízes): 7, quase todas NOCHA+CHASTOR -> NOCHASTOR (nochastor/a/ad/al, anochastor, axnochastor); nochadaxa=CHADAX+NOCHA.
- Derivação por acreção: adnocha->adnochap->adnochaph->adnochapha; chastor->chastora->chastorad/al/an; prefixos I-/ZI-/NE- = linhas paralelas.
VEREDITO: há dinastias além de CHASTOR (NOCHA maior); evento central = casamento NOCHA×CHASTOR -> NOCHASTOR (domina diagonal 26a #343 e miolo #342). 27% dos nomes sem raiz = camada avulsa.
Docs: docs/DINASTIAS.md. Dados: results/179_dynasties.json.
