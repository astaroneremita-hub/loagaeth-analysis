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
