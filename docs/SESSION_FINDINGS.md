# What we found, where we got, and how

A consolidated, honest record of the structural analysis of the Loagaeth. Every claim
here beat a null model or is true by direct inspection; the refuted ideas are listed too,
because that is what makes the rest trustworthy. Reproduce any number with the module
named beside it.

## The one-paragraph picture

The Loagaeth is **not a cipher to translate — it is the name-book of the Angelical
language.** It is written in the *same tongue* as the 48 Calls (shared sound-grammar),
but its content is that language's **names**, organized as a scale-free network with one
dominant stem, **CHASTOR**, that behaves like a real word (takes a closed set of prefixes)
and governs a **contiguous territory** of the tables. The letters are not placed at random
— they carry measurable positional roles. The names are **sealed** (no attested meaning)
except for ~20 shared sacred particles in the prophetic first leaf. Structure is known;
the referents are not.

## Findings (with method and module)

### 1. It is a catalog of names, not prose — module `a01`, `a03`
- 195,548 letters. Unigram entropy 4.03 bits, conditional 3.44 (strong local/syllable
  structure). Type/token 0.81 on the word-spaced leaves. No prose-like long-range grammar.
- **CHASTOR**: 184 occurrences across 35 of 48 tables (72.9%); with NOCHASTOR, 61 more
  across 27. **CHUSTOR** is its A→U vowel twin.
- *How:* substring counts per table + entropy/IC over the dense stream.

### 2. Productive morphology — a few roots, a closed affix set — module `a04`
- CHASTOR takes a closed prefix inventory: **NO- (77), NE- (24), ZI- (18), NA- (12),
  OL- (11)**, giving a clean paradigm (NOCHASTOR, NECHASTOR, ZICHASTOR, NOCHASTORAD…).
- The **family forest**: three roots take ≥3 distinct prefixes — **CHASTOR** (8 prefixes),
  **DAX** (4), **CHADAX** (3). CHASTOR is the trunk; DAX/CHADAX are minor branches.
- *How:* scan the stream for each stem, tabulate the letters before/after.

### 3. The alphabet has real positional grammar — module `a09`
- Mutual information MI(letter; position) = **0.181 bits** vs a within-word shuffle null
  of 0.003 — **z ≈ 331**. Letters are assigned to positions far beyond chance.
- **G, V are onsets** (word-initial); **H is a terminator** (word-final). Names parse as a
  tendency `[onset][root][terminator]`: ZURAH = ZU·RA·H, NOGAH = NO·GA·H, UORGET·H.
- *How:* MI(letter; initial/medial/final), null = shuffle letters within each word.

### 4. Same Angelical tongue as the Calls, different lexicon — module `a09`
- Correlation of each letter's P(final) profile: **Loagaeth ↔ Calls r = 0.71**, vs
  **Loagaeth ↔ English r = 0.22** (control), Calls ↔ English r = 0.56. The shared
  word-ending grammar is Angelical-specific, not universal phonotactics.
- Corollary: the Loagaeth is *less* English-like than the Calls — the deeper/older layer.
- *How:* positional profiles + Pearson correlation, English as control.

### 5. A territorial map — name-dynasties — module `a10`, dataset `data/loagaeth_territories.json`
- Per table, the dominant recurring name ("local ruler"). The book is partitioned:
  - **CHASTOR** rules the heartland (tables 6–25) and a second realm (29–43); the local
    rulers there (DNOCHA, ADNACH, CHANZA) are its own kin.
  - **CHUSTOR** rules the end (44–48).
  - A **-MACH** dynasty (ADMACH, DMACHE, CAPNAG) holds the opening (2–5) — a different family.
  - Table 1 = prophecy (and the *last* leaf in reading order); 26–28, 41, 47 are void/border.
- The zonation is real: per-table CHASTOR counts have lag-1 autocorrelation **0.51** vs a
  shuffle null (95th percentile 0.20). CHASTOR holds a contiguous territory, not scatter.
- *How:* most-frequent recurring 6-gram per table + autocorrelation vs shuffle null.

### 6. Each table also has its own signature name — module `a05`
- All 48 tables have a distinctive local string; none are CHASTOR-family. (The two examples first given here, HZEMBL and DAHOXI, were read across word boundaries and are withdrawn: see section 56.)

### 7. The readable layer: ~20 glossed particles in leaf 1 — module `a06`
- Leaf 1 (the word-spaced *prophecy*) carries attested Angelical words with known meanings:
  MAD (of god), IAD (the god), GAH (spirits), ORS (with darkness), ZIR (I am), ODO (open),
  GOHO (sayeth), plus VORS ("now the seas appear", which recurs 47× across 12 tables).
- These are the Loagaeth's **grammatical/sacred particles**, shared with the Calls. The
  **proper names (CHASTOR etc.) remain unglossed.**
- *How:* whole-word matches in leaf 1 (boundaries exist) against the attested lexicon.
- Honest caveat: counting these as dense-table *substrings* is misleading (ADNA appears
  474× but embedded inside ADNOCHA etc.) — a chance artifact. Only the whole-word leaf-1
  matches are trustworthy anchors.

## Three deep dives (numeric layer, dynasties, the anchor)

### 8. The numeric layer — the one strong unexplained anomaly — CONFIRMED
- The numbers Dee attached to the 91 governors are dominated by the digits 2, 3, 6:
  **2 appears 71×, 3 appears 75×, 6 appears 69×**, against 12–40 for every other digit.
  Together 2/3/6 make **59% of all digits** (chance ≈ 30%). **62 of 91** numbers contain a 6.
- Null (random numbers of the same range): **z = 11.4**. This is the single strongest
  pattern in the whole corpus with no known construction rule. A Reeds-style generative
  rule behind Dee's numbers is the open lead.

### 9. The dynasties, refined — one empire, a lone twin, scattered realms
- Only **CHASTOR** is a true productive dynasty (8 prefixes, a contiguous heartland).
- **CHUSTOR** is a lone vowel-twin ruling the end tables (44–48) but spawns essentially no
  prefix-family — a sovereign variant, not a dynasty.
- The **-MACH** opening (tables 2–5) is weak: the MACH morphological family is tiny
  (5 forms, 8 occurrences). Those tables have their own dominant local names but no shared
  dynasty.
- Honest correction to the territory map: it is **one empire (CHASTOR) + a lone twin
  (CHUSTOR) + small independent realms**, not three equal dynasties.

### 10. The CHASTOR anchor — confirmed sealed; the Rosetta seed
- Exhaustive search of the unified lexicon: **zero** glossed entries contain CHAST or CHUST.
  The master name is unglossed in every source we hold — **sealed**.
- The only usable anchors are the ~12 glossed particles in leaf 1 (GEH, PAR, ORS, ADNA,
  GAH, URAN, MAD, LAP, OXEX "vomit out", POLA…) — the **Rosetta seed**. These are shared
  Angelical function/sacred words, not the proper names. Meaning for CHASTOR, if it comes,
  comes from outside the text (attestation or evocation), then to the bench.

### 11. The queen and the "rival house": CHAST vs GETH — module `a11`
- **CHAST is a head-stem.** Its right side is almost fixed (followed by -OR in 80% of 231
  cases; right-context entropy 1.49 bits) while its left side varies (9 prefix types: NO 77,
  NE 24, ZI 18, NA 12, PLI, PRI…). It is the paradigm-maker.
- **GETH is the most pervasive element.** 504 occurrences across 43 tables (more than CHAST's
  36), high-entropy contexts on both sides (preceded mostly by AL/AR/OL/AN, followed by the
  start of a new name). It ends in H, the measured terminator.
- **They are not rivals.** Per-table counts correlate r = 0.64 — exactly what any string of
  that frequency shows (null 0.66 ± 0.04, z = −0.8). Every table with CHAST also has GETH. No
  local attraction (mean distance z = −1.9) and no phrase syntax (GETH is never immediately
  followed by NOCHAST: 0/60 vs a 2.2% base rate).
- Two kinds of "power": **ubiquity** (GETH) vs **depth of rank** (CHASTOR).

### 12. The empire up close: stems + a stackable title-chain — module `a12`
- The wider project's **"seven Lords"** (CHASTOR, HANZACH, ALGETHA, ADNOCHA, ADNACHA, ACHEPHA,
  ANTANTO) were the seven most recurrent 7-letter strings. They are real, but they **overlap
  and nest** (ADNOCHA·STOR, NOC·HANZACH, ADN·ACHEPHA) rather than being seven independent beings.
- Underneath: **a few stem-names + a shared title-chain that stacks.**
  CHASTOR 184 ⊃ NOCHASTOR 61 ⊃ ADNOCHASTOR 10 · CHAPH 100 ⊃ NOCHAPH 47 ⊃ ADNOCHAPH 20 ·
  ANZACH 153 ⊃ NOCHANZACH 11 ⊃ ADNOCHANZACH 5 · CHEPHA 70 ⊃ ACHEPHA 49 ⊃ ADNACHEPHA 10.
  The title itself (NOCHA 544; AD-/ED-/ID-/AG-NOCHA) recurs with a free vowel. **Each added
  title cuts frequency about threefold** — rank-like compounding.
- **ANZACH** (153 occurrences, 39 tables) is a second great stem, nearly as large as CHASTOR.
- **"Queen of the hive", tested:** yes structurally — the stem is carried inside every titled
  form. But shorter forms are more frequent (length vs occurrences ρ = −0.39), and gematria
  does not track power (ρ = +0.11).
- Refuted here: **CHA as a closed core** (2,811×, tail entropy 9.4 bits — a generic syllable);
  **vowel twins as a noble mark** (100% of the Lords have one, but so do 99% of any frequent
  7-gram — vowel alternation is language-wide).
- **Literature check:** zero mentions of CHASTOR, NOCHASTOR, ALGETH or CHUSTOR in the 81
  reference books held by the project.

### 13. The governors' numbers: a generative architecture — module `a13`
Beyond "2, 3, 6 dominate" (z ≈ 11): every test below uses a null that **shuffles all digits
across the 91 numbers, keeping lengths** — so the global 2/3/6 excess is already priced in.
- 2, 3, 6 appear **together in one number**: 34 vs 11.8 (z = 7.6).
- As a **contiguous block** (632, 362, 236…): 30 vs 7.6 (z = 9.0).
- **The block sits at the end** (last three digits a 236-permutation): 20 vs 4.2 (z = 8.3).
- **Zero padding** (number ends in 0: 2360, 3620, 6320…): 28 vs 10.1 (z = 6.7).
- **Exact duplicates**: 13 pairs vs 1.7 (z = 8.5). **Anagram pairs** (same digit multiset):
  92 vs 20.6 (z = 13.7).
- **Architecture:** *number = [head digit] + [the 2-3-6 block, permuted, sometimes zero-padded]*
  (7|632, 9|236, 5|362, 2|360).
- **The head digit belongs to the Aethyr** — and only in the second half. Governors of the same
  Aethyr share their first digit: Aethyrs 1–14, 2 pairs vs 5.0 (z = −1.4, no rule); **Aethyrs
  15–30, 25 vs 6.1 (z = 8.2)**. Aethyrs 15, 16, 21, 22, 23, 24, 27 have all heads identical
  (1, 9, 5, 2, 7, 8, 7). The construction **changes regime at the midpoint** of the 30.
- Nothing else sets the head: part in Aethyr (p = 0.78), tribe 1–12 (p = 0.74), name initial
  (p = 0.14). The exact rule choosing each head digit and permutation is still unknown.
- Textual note: Dee's declared sum for Aethyr 2 (6660) disagrees with its parts (14960); it
  would fit exactly if DIALIVA were 662, but every source gives 8962 — so the declared sum is
  the likelier slip. Hypothesis only.

### 14. ANZACH, the sibling stem — module `a14`
- **153 occurrences across 39 tables** (wider reach than CHASTOR's 35), present already in the
  opening tables 2–5 where CHASTOR is absent.
- **Built like CHASTOR:** preceded by OCH/ACH → **NO·CHA·NZACH** in parallel to **NO·CHA·STOR**.
  Title nesting: ANZACH 153 ⊃ HANZACH 76 ⊃ NOCHANZACH 11 ⊃ ADNOCHANZACH 5. Variants ONZACH 77,
  ANZACHA 67.
- **A real word:** ANZACH stands alone as a word in the prophetic leaf 1 (which has word
  boundaries), alongside HANZAH, ORANZA, ANZAZED.
- **No rivalry, no precedence:** territory correlation with CHASTOR r = 0.58 vs a density null
  of 0.62 ± 0.06 (z = −0.5); in the 34 tables holding both, each comes first 17 times.
- **NOCHA as a closed title — refuted.** NOCHA (544×) is followed by an open range of
  continuations (7.7 bits; top five cover 18%). What is solid: it is preceded by vowel+D (AD 176,
  ED 72, ID 35, YD 16 → the unit DNOCHA, the heartland's dominant name), and its most common
  continuations are STOR (61), PH (47), NZACH (11).

### 15. The book's physical geometry — module `a15`
- **Four segments.** Table 1: word-spaced prophecy. Tables 2–28: full 49×49 grids written in
  rows. Tables 29–48: each side is a **diamond** — row lengths 1,3,5…49…3,1 (1201 cells) on one
  side and 2,4…48,48…4,2 (1200 cells) on the other; 1201 + 1200 = 2401 = 49². Tables 44–48 use an
  irregular diamond pairing and carry almost no recurring names. Table 49 is not in the data.
- **The diamonds are the two colours of a chessboard.** Placing one side on the even
  anti-diagonals (r+c = 2u) and the other on the odd ones rebuilds one complete 49×49 grid; each
  diamond row is one diagonal of that grid (the paper turned 45°).
- **The language runs along the diagonals.** In the 13 cleanly paired tables, reading the
  diamond rows as written gives recurring-name share 0.150, conditional entropy 3.24 bits,
  doubled letters 0.43%. Reading the rebuilt square by rows or columns gives 0.001 / 0.000, 4.02
  bits, 8.3–8.5% — noise. This is the geometric form of Peterson's note that Kelley skipped every
  other letter and that the paper was reoriented. (A naive "every-other-letter along the row"
  version of that idea is refuted: the diamond rows match ordinary adjacent-letter statistics,
  JS 0.09, not skip-one statistics, JS 0.35.)
- ~~Tables 26–28 are statistical noise.~~ **SUPERSEDED by section 22.** Read by rows they are
  indistinguishable from noise (conditional entropy equals a shuffled copy, no recurring names,
  doubled letters at chance), but that is the wrong reading direction: they are written on the
  diagonals in two colour currents and decode into ordinary text.
- **Method correction.** Because the diamond tables hold half the letters per side, raw
  per-table counts (module `a10`, `a11`, `a14`) are not comparable across the two formats. Length-
  normalised, CHASTOR's density is steady from table 6 to 43; the real breaks are at table 6
  (CHASTOR appears) and table 44 (recurring names collapse).

### 16. The no-doubled-letter rule — module `a15`
- Adjacent identical letters: full tables 0.76%, diamond tables 0.43%, leaf 1 0.61% — against
  8.6% expected from the letter frequencies: **about 11× below chance**. The Calls 1.85%
  (avoided, but less strictly). Tables 26–28: 9.6%, at chance.

### 17. The numbers, further — module `a13`
- **The 2-3-6 block prefers its natural order:** "236" in 13 of the 30 numbers that contain the
  block contiguously, vs 5 expected if all six orders were equal (binomial p = 0.0005).
- **No known rule sets the head digit.** 30 candidate rules (gematria of the Aethyr name in all 13
  systems, index transforms, sums of the parts) were tried; the null re-runs the entire search on
  shuffled heads. Best 4/16 vs 4.3 expected by chance (p = 0.83). Honest negative.

### 18. Every letter, mapped — module `a16`
- Counts over tables 2–48: A 33,441 (18.9%), O 9.2%, N 9.0%, H 6.8%, L 6.3%, D 5.8%, R 5.5%,
  C 4.8%, X 4.7%, E 4.0%, G 4.0%, T 3.9%, V 3.2%, P 3.0%, Z 2.4%, U 2.0%, I 1.8%, M 1.5%, S 1.2%,
  B 1.2%, Y 0.6%, F 0.3%, Q 0.09%; W and K virtually absent. Each letter's value in all 13
  gematria systems is stored with the counts (reference only — those systems are later
  conventions, and raw counts depend on the transcription's size, so they carry no meaning of
  their own).
- **No hidden name in the top letters** (k = 3…8, exact anagram against the attested lexicon and
  the Loagaeth vocabulary; nulls give the chance of a hit).
- **Frequency vs letter value:** no relation in any system after Bonferroni (13 tests; the lowest
  p = 0.02 for an unspecified "English Qabalah" table does not survive).
- **Position in the full grids:** the letter × region table (four quadrants + central cross)
  departs from a within-grid shuffle (χ² 161.5 vs 95th percentile ≈ 108–115). The cause is the row
  edges: rows open with onsets (V 5.3×, P 3.0×, Z 2.4×, G 1.9×) and close with terminators
  (S 3.4×, H 2.0×, O 1.7×, X 1.6×) — the 49-letter lines follow word boundaries. Without the three
  outer columns, left and right halves are alike (ratios 0.95–1.12). The centre cell (25,25) has
  no special letter (O 7 of 36 grids, p ≈ 0.06).
- **Segments have distinct letter mixes** (χ² ≈ 11,100 vs ≤ 3,800 with tables shuffled between
  segments).

### 19. The U register — module `a16`
- End segment (44–48) vs heartland (6–25), recurring 5-grams in common: 228 as written; 387 with
  A→U; 146 / 166 / 169 with A→E / A→I / A→O. Only A→U brings them together; 28% of the end's
  recurring 5-grams are heartland 5-grams with A turned into U (36% counting both ways).
  Examples: CHAST→CHUST, HASTO→HUSTO, ASTOR→USTOR, RANCH→RUNCH, VANCH→VUNCH, RAPHA→RUPHU,
  APHAR→UPHUR, ANCHA→UNCHU. In the end segment A drops to 5.8% and U rises to 10.1%.
- This sharpens an earlier A↔U hypothesis that had failed across a different grouping (tables
  with vs without CHASTOR). Caveat: one transcription cannot separate a deliberate register from a
  reading habit in those leaves.

### 20. Sides, mirrors and the 7×7 plan — module `a17`
- **Sides:** exact baseline (centre of a k-letter name falls left with known probability; rows
  uniform). Left/right: all |z| ≤ 1.7 — no preference. Top/bottom: **ALGETH z = −3.1** (lower half,
  passes Bonferroni for 14 tests); GETH −2.3 and NOCHA +1.8 only lean.
- **Mirrors:** diamond row vs its mirror 0.029 vs random same-length row 0.047 (trigram Jaccard);
  full-grid row vs mirror 0.071 vs random row of the same table 0.073. No mirror symmetry.
- **The 7×7 plan:** CHASTOR appears at table 6 (week 1, pos 6); the heartland ends at table 25 —
  the exact centre of the plan (week 4, pos 4) and of 1..49; noise 26–28 completes week 4; the 45°
  format begins at table 29 (week 5, pos 1); the U register at 44 (week 7, pos 2). Descriptive,
  post hoc, no p-value claimed.

### 21. The implicit correlation zone: two houses — module `a17`
- Per-table densities of 15 names, regressed on the table's overall name density; residual
  correlations; family-wise 95% threshold from shuffled series (|r| > 0.53). Pairs where one name
  contains the other (GETH⊂ALGETH, NOCHAPH/ADNOCHA via ADNOCHAPH) are trivial and set aside.
- The non-trivial strong pairs are all **antagonisms**: NODAX × ALGETH −0.65, ADNOCHA × ACLAX
  −0.60, ADNOCHA × ALGETH −0.57.
- **Re-tested inside each realm** (so living in different realms cannot explain it):
  ADNOCHA × ACLAX −0.58 heartland (p = 0.004), −0.66 diamonds (p = 0.007); NODAX × ALGETH −0.60
  heartland (p = 0.001), +0.13 diamonds (n.s.); NOCHAPH × ACLAX −0.24 heartland (n.s.), −0.73
  diamonds (p = 0.002); ADNOCHA × ALGETH marginal (p ≈ 0.05 / 0.12).
- Densities per 1000 letters (opening / heartland / diamonds / end): ADNOCHA 0 / 1.75 / 0.22 / 0;
  ALGETH 0.10 / 0.78 / 1.03 / 0; ACLAX 0 / 1.23 / 1.06 / 0. **Two houses alternate table by
  table; the NOCHA house leads the first half, the GETH/ACLAX house holds or grows in the second.**

### 22. Tables 25b–28b decoded: two currents on the diagonals — module `a18`
- Source: Peterson's page (https://www.esotericarchives.com/dee/sl3189.htm), parsed with its
  markup. In leaves 25b–28b every letter is followed by one of two signs (`~` / `` ` `` / space).
  Aligned to the grid (2,401 letters = 2,401 cells in 26a–28b), each sign falls on one chessboard
  colour: 26a/27a `~` on colour 0 (1,200); 26b `~` colour 0, `/` colour 1; 27b `/` colour 0,
  `` ` `` colour 1; 28a/28b `/` colour 1, `` ` `` colour 0.
- Reading each colour along the diagonals (one binary choice per face for the leftward current):

  | face | rows | ↘ current | leftward current |
  |---|---|---|---|
  | 26a | 0.001 | 0.220 | 0.259 (↖) |
  | 26b | 0.001 | 0.367 | 0.246 (↙) |
  | 27a | 0.000 | 0.150 | 0.227 (↙) |
  | 27b | 0.001 | 0.381 | 0.284 (↖) |
  | 28a | 0.001 | 0.403 | 0.126 (↖) |
  | 28b | 0.000 | 0.403 | 0.175 (↖) |

  (recurring-name share against the inventory of tables 2–24). Overall 0.001 → 0.27; conditional
  entropy 3.82 → 3.05 bits; doubled letters 9.6% → 1.5%. Control: 35 row-written tables read by the
  same procedure, maximum 0.005. 25b follows the same rule (colour 0 ↘ 0.307, colour 1 ↖ 0.181).
- Master names appear once decoded (rows → decoded): CHASTOR 0 → 16, ANZACH 0 → 12, GETH 0 → 85,
  NOCHA 0 → 51, ADNOCHA 0 → 15, ALGETH 0 → 26, ACLAX 0 → 27. With the decoded text, tables 26–28
  fall inside CHASTOR's territory (module `a10` now uses it): **the realm is continuous 6–43**.
- **Midpoint (descriptive):** sides 1a–25a are written in rows, 25b onwards on diagonals; 25a is
  side 49 of a 98-side book.

### 23. Leaf titles — module `a18`
- 94 leaf headings extracted (`data/loagaeth_leaf_titles.json`). 5b *Zvchastors plohodmax argednon*
  contains ZUCHASTOR(S) — the U form of the master name — immediately before CHASTOR's realm begins
  at table 6; ALGE/ALGETH appear in the headings of 3b, 4a, 7a, 8a.
- Headings are not summaries of their leaf: 15% of title 4-grams occur in their own leaf vs 16% in
  other leaves (53 titles).

### 24. Machine or language — module `a19`
- Soyga Aries table (extracted locally from Kupin 2014, not redistributed): columns periodic, best
  self-match 0.969 / 0.875 / 0.844 at period 4, 0.458 at period 12. Loagaeth rows 0.197 vs shuffled
  0.168; decoded diagonals 0.227. **The Soyga table is generated; the Loagaeth is not.**
- 2-D rule: H(x) 3.951, H(x|above) 3.943, H(x|left) 3.093, H(x|left, above) 3.016.
- Compression (bits/letter, zlib / bz2 / lzma): real 3.55 / 3.28 / 3.38, Markov-3 surrogate
  3.52 / 3.16 / 3.34, shuffled 4.58 / 4.32 / 4.10 — no long-range regularity beyond local syllables.
- Character model (order 4, trained on 2–24): held-out 3.012; decoded 25b–28 3.437; same tables by
  rows 7.620; diamonds 3.745; end as written 5.051; end with U→A 4.246; shuffled 7.508.
- Order-5 generator: produces plausible Loagaeth surface text with a similar doubled-letter rate
  (0.6% vs 0.9%); it over-produces the most frequent names.

### 25. Letter energy by realm — module `a20`
- Mean letter value per segment in 13 gematria systems + surprisal: end > heartland in 10 of 14 after
  Bonferroni. Golden Dawn: 38.8 / 45.6 / 60.0 / 83.2 (opening / heartland / diamonds / end).
- With U turned back into A, only 3 of 14 remain (Golden Dawn difference −0.75, p = 0.65). Surprisal
  stays higher at the end (+0.17 bit/letter, p < 0.001).

### 26. Fibonacci, gradual division, Golden-Dawn rearrangement — module `a20` (negative)
- Fibonacci gaps between CHASTORs 1.04% vs 1.47% random (95th 3.1%); Fibonacci start columns 17.7%
  vs 18.6% expected; borders not Fibonacci, not at the golden section (30.3).
- 7×7 blocks χ² 1473 vs shuffled 95th 1063 — explained by the row-edge effect; central row names
  0.264 vs 0.280 elsewhere.
- Golden-Dawn-style quadrant rearrangement: original best in 35/35 tables (mean best gain −0.014).

### 27. Peterson's Index Verborum, Heptarchy numbers, gematria — module `a21`
- The index (angelix, © 1986) is a concordance of leaf 1 only: t1 = 1a, t2 = 1b; no glosses.
  97.5% of 3,589 references on the stated line; 2.0% variant readings (Z/X, U/B, N/U, R/X).
- Line map: 1b line 20 is split over two transcription rows; 1b has 49 lines.
- Gold standard: Peterson's division of the nine unspaced lines of 1b vs our word model trained on
  the spaced lines — F1 0.33 vs 0.16 random (p < 0.0005). REAL.
- Letter counts vs 7/42/49: chance. Total 177,226 ≡ 0 mod 7 (49×49 build). B opens all 49
  Heptarchic names (16% of their letters) but is 1.2% of the Loagaeth.
- AONHLDRC… as a string: AONH 1×, ONHL 1×, nothing longer. Gematria 6/5 came from mistyped counts;
  GD sum is 1,486 and order-independent.

### 28. 3D overlays: heat map, trail, closed pyramid, tesseract, icosahedron (viewer)
- Stack of the 36 exact 49×49 sides of 2a–25a with a within-side shuffle null.
- Interior hotspots match the null (ratios 2.2–5.5 vs 2.3–4.8). Only the row edges stand out
  (X col 1 0.01× / col 49 1.62×; H 0.10× / 2.03×; G 1.89× / 0.52×; null 0.82–1.12×).
- The letter trail and the master-name overlay form no symbol; names are short row streaks.

### 29. Inverse reading, signatures, elements — `a21 F` + viewer
- Reversed reading: names vanish (CHASTOR 179/0, GETH 504/0…); forward model 3.5 vs 6.1 bits on
  reversed text. Only DAXO (= DAX + O) appears reversed. The text has one direction.
- Dominant letter A in 83/94 sides; U 7, R 3, N 1 (end). Top-3 signatures track the segments.
- Pyramid from above: triangles top 2.41, bottom 2.44, right 2.05, left 1.77 name-heat; difference
  = row-edge effect. Elements (quartiles): edges 87% Water; letter maps within ±4 pts of null except X.

### 30. Robustness and deeper mathematics — module `a22`
- Under Z=X, U=V, U→A, clean 49×49 sides only, and 2% look-alike noise: doubled-letter rule,
  row edges (z ≈ 40), segment χ² and name counts all hold.
- Territory revised: count lag-1 0.49 (p<0.001), per-1000 0.26 (z≈2), U→A z 1.1 — moderate, partly
  the U-register boundary.
- Segmentation tuned leave-one-line-out on Peterson: F1 0.36 (default 0.33, random 0.16).
- Diamonds: only the stored anti-diagonals read (3.71 bits, 9.9 names/1000); nine other paths ≈7.8, 0.
- Mutual information: excess over Markov-3 only at 4–12 letters; beyond = within-side letter mix.
- No block copying (16 vs 18 surrogate); LZMA 3.22 vs 3.26; leaf 1 Zipf/Heaps ≈ Calls; no 2-D structure.
- Viewer: majority-by-sub-quadrant shows only the edge columns (row edges).

### 31. Names, architecture, bridges — modules `a23`, `a24`, `a25`
- Unsupervised discovery: 47 word-like recurring strings beyond Markov-3 (surrogate 0). New: NACHO
  (157×, vowel mirror of NOCHA), AXALGRA, GRADAX, PHANGE, ANTANTOX, VOXAR, TAXALGRA, ONDANVAGE, UCHER.
  Five families (core + affixes), none in the surrogate.
- The two currents of 25b–28b carry different vocabularies (Jaccard 0.221 vs 0.315 random).
- Dialect chain along the book; Dee's order nearly maximally smooth (91.2 vs ≤ 85.9 random).
- Refuted: mirror pairs, plan columns, acrostics, centre string, names on the pyramid cross, other
  systems' names (all at chance), constellation of names.

### 32. Letter names as a lens — `a26` (construction)
- Dee's letter names (Un, Pa, Veh… Gisg, Van) + practitioner meanings; every name read through them.
- Rows open with Van/Mals/Ceph/Ged/Veh, close with Fam/Ger/Na/Med/Pal; realm signatures: opening
  Tal/Fam/Or, end Van/Don/Mals. Roadmap of open questions in docs/ROADMAP.md.

### 33. Track A — borders, irregular rows — `a27`
- Optimal contiguous blocks: 5 suffice; borders 12b|13a, 25a|25b, 33a|33b, 40b|41a. Opening 2–5 is
  not separate; U register starts at 41; new break at 12|13 (T, X double; U appears).
- Dialect chain and U register hold on the new parts (U→A 436 vs 242).
- Irregular rows: 7 isolated ±1; 8b a dropped column (−37); 9a −376 in rows 1–7; 12b −4. U/A check
  of the manuscript open (no table images).

### 34. Track B — names deeper — `a28`
- 12 names with Bonferroni-surviving territories; NOCHA house peaks ~11–21, GETH/ACLAX ~25–31.
- Refuted: genealogy (core first z 0.19), vowel-mirror law (same ratio as surrogate), variants by current.
- Hidden names after masking: MACHO 51×, DNACHAP, NOPHAR, ANZANO, NACHAPA, DRAXVL, RONTANTOXA.

### 35. Track C — architecture deeper — `a29`
- Language drifts in small steps (1.07 vs 1.72 bits); biggest jumps in tables 40–48.
- Diamond a/b halves are one text (Jaccard = random split); the currents of 25b–28b are the special case.
- Leaf-1 words at chance in the tables; no particle system between names.

### 36. Track D — anchors — `a30`
- Glossed Call words occur in the Loagaeth exactly at letter-habit rates (TAGE 139 vs 147, EMNA 94 vs
  100…): no anchor. Titles not in their leaf's dialect (rank 0.49). Diaries' text unavailable — open.

### 37. Track E — grammar — `a31`
- Names + letters grammar: 3.000 bits/letter vs 2.985 for a 3-letter memory: no shorter code.
- Only part V (41–48) gains from its own grammar (3.55 vs 3.68).

### 38. One language? — `a32`
- Loagaeth model reads Call words (z 23.9), governors (13.4), Heptarchic names (8.5) as its own
  sound-pattern; rule-read Watchtower names are not word-like (1.9). Great Table not rule-generated.

### 39. Dee's record tested — `a33`
- Diaries read in full: ~30 glossed words, all in leaf 1; no gloss for any table name.
- Glossed words absent from the tables; direction confirmed by leaf 1; leaf 1 heads the dialect chain;
  Call n ↔ table n+1 has no textual trace; table 18 = NECHASTOR's home.

### 40. Vowel paradigms — `a34`
- Leaf 1: 222 one-vowel word pairs vs 33 by chance; 17 full vowel series (DATH/DETH/DOTH/DUTH,
  GATH/GETH/GOTH/GUTH…) vs 0.8. Master stems are the dominant grades of such series in the tables.

### 41. Nalvage's coordinates and the scribe's ruler — `a35`, `a36`
- Nalvage's 61 table/number references: no plain indexing finds the letters (p 0.79); numbers are
  composed (rise with table, thousands + small tail).
- Soyga tables regenerated by Reeds's rule: 3.3% errors; z→x 8.5%, n→u 6.5%; a→u 0.3%, a↔o never —
  the U register and the vowel series are not reading artefacts.

### 42. Re-decoding 25b–28b and three leads — `a37`, `a38`
- 27a first colour: rows 1–28 by rows then diagonals (5.52 → 2.74 bits); 26a: rows 1–8 + triangles
  (5.01 → 2.92; 90 letters still unclear); 25b: rows 1–5 (Peterson's third series). ~1,500 letters recovered.
- Refuted: every k-th letter; 43–48 as replication; rule in Heptarchic number layouts.

### Provenance warning: the grimoire's "powers"
The wider project generated a grimoire that assigns each Lord a sefira, planet, talisman,
how-to-call and danger grade. Its own generator states these layers were *"constructed
(Golden Dawn method), not deciphered"*, and its provenance file marks "7 Lords = 7 lower
sefirot" and "gematria → sefira/planet" as **convention**. The same name received two
incompatible assignments (CHASTOR as Tiferet/Sun and as Chesed/Jupiter) depending on the
mapping. Treat those powers as a ritual design choice, not as properties of the names.

## What we tested and threw out (this is the discipline)

All refuted against a strong (Markov / frequency-controlled / within-word-shuffle) null:
- **Mirror / reversal of names** — a syllable-pool artifact (and 0 reverse pairs among the
  686 attested forms).
- **Decimation by 2** (the theory that Kelley wrote every-other letter) — splitting the
  stream destroys structure (2220 recurring 6-grams → ~20); the names are contiguous.
- **Prefix = region/rank** — NOCHASTOR vs NECHASTOR table-overlap matches a frequency null.
- **Numeric signature of the CHASTOR family** (2/3/6 digits) — spread, no concentration.
- **Acrostic of the prologue** — gibberish, and a paraphrased translation kills any cipher.
- **Semitic triliteral roots** — words/skeleton ratio ~1.3, English-like, not root-and-pattern.
- Earlier: Call-vocabulary-as-key, Gebofal reordering, four geometric models, divine-name
  ciphers.

## Where we are, and what is still needed

We have the **form** of the names (network, morphology, letter-grammar, territory) and the
fact that it is one language with the Calls. We do **not** have the **referents** of the
proper names. The only path to meaning is an **external anchor**: the attested sense of a
single Loagaeth proper name (CHASTOR is the highest-value target, since it governs most of
the book). One real meaning could be tested as a key across its 35 tables — a real meaning
leaves a trace in the neighboring names; an imagined one does not. Per Dee's own source,
the highest names were "honored but not to be pronounced," so this layer may be sealed by
design, not merely undiscovered.

---

## On evocation: are these "kings" names to call? (an honest answer)

A natural question: the Watchtower system gives **kings, seniors, angels to evoke**, derived
by a documented algorithm. Do the Loagaeth "rulers" work the same way? Three honest points:

1. **"Ruler" here is a statistic, not an attested king.** In module `a10` a table's ruler
   is simply its most frequent recurring name. The Watchtower kings (BATAIVAH, RAAGIOSL…)
   are different: they are **derived by a known rule** (the spiral from the Great Cross) and
   **attested** as entities to evoke. The engine reproduces all 456 Watchtower names
   deterministically (`engine/enoch.py`). The Loagaeth rulers have **no attested derivation
   rule and no attested evocation role.**

2. **Dee's own source says the Loagaeth names are NOT for pronouncing.** Galvah: the high
   names are "honored, but of me are not to be pronounced." The Loagaeth is called "a Book of
   Secrets and Key of this World," and historically its tables are the **matrix from which
   the 48 Calls were extracted** — the evocation roster (kings, governors, Aethyrs) comes
   from the **Great Table + the Calls**, not from reciting Loagaeth names. So these names
   plausibly serve a **different purpose** (the knowledge/"Key of this World" layer), not a
   call-list.

3. **Can we still BUILD a name-mapping system over the 49×49 grids, like the Towers?** Yes —
   mechanically. One can apply Watchtower-style geometric extraction (spiral from a centre,
   straight-line reads, cross/arm reads) to each 49×49 table to surface **candidate** names,
   and tabulate a per-table name-table. But be clear about status: it would be **our
   construction**, not attested. The 49×49 grid has no attested Great-Cross/centre, so the
   geometry is a hypothesis; any names it produces are **candidates to null-test**, with no
   guaranteed meaning or evocation validity — and our track record says most such
   constructions fail the null. It is worth building as an **exploration tool** (and clearly
   labeled as such), not as a revealed evocation system.

**Practical bottom line:** if the goal is an evocation table, build it from the **attested**
Watchtower system (we already reproduce it). If the goal is to *explore* whether the
Loagaeth grids hide an extractable name-system, that is a buildable, honest experiment —
candidates in, null model as judge, no claims until something survives.

## 43. Long repeats and phrases (module a39)

Raised by a reader: repeats longer than 10 letters suggest phrases.

- **Long repeats are real against Markov-3.** Distinct strings occurring twice or more inside a line:
  length 12: 549 (surrogate 116); length 14: 94 (surrogate 11); length 16: 5 (surrogate 1). REAL.
- **An order-5 letter model reproduces them** (521, 66 and 7). The repeats need no unit longer than
  about six letters of context: chained formulas are enough.
- **Longest:** ADNACHEPHALZEDNOC (17, twice on 19b); ADNOCHANTANTOXAL (19a, 22a), ACHEDNOCHALZINTO
  (21b, 23b), CHASTORANTANTOXA (21b, 24b), all 16. One repeat of 16 is expected by chance under
  Markov-3, so a single one is not proof by itself; the count at 12-14 is.
- **Phrases, tested directly:** where one name is followed at once by another (91 cases), the second
  is not tied to the first more than in shuffles (1.84 bits vs 1.99, p 0.81). NOT SHOWN.
- **Descriptive:** GETH+ACLAX written together, never reversed (tested in section 46; OXAD+NOCHA, first listed here, did not survive).

## 44. Formulas: memory, compounds and controlled variation (module a40)

- **Memory of the text (held-out).** Half the sides against the other half: strings of 12 letters
  shared, 259; a letter model trained on the first half only gives 120 at order 3 and 521 at order 5.
  The book repeats more than three letters of context explain and no more than five do. No unit
  longer than about six letters is needed. BOUNDED.
- **Names in sequence.** 693 successive names inside lines: the next name is not tied to the
  previous one (1.007 bits vs 1.051 shuffled, p 0.86). No syntax between names. NOT SHOWN.
- **Compounds with a fixed order.** First result (shuffle of names): OXAD+NOCHA and GETH+ACLAX.
  Corrected in section 46: only GETH+ACLAX is real.
- **Long repeats are not copied in place.** Start columns of the two occurrences agree no more than
  in shuffles (10% within two columns vs 14%).
- **Controlled variation.** 179 passages of 14 letters recur with exactly one letter changed
  (Markov-3: 21-30). REAL. The changes: A/O 31 (ADNOCHA / ADNACHA), A/E 10, A/I 8, E/O 8, H/L 7
  (NOCHANT / NOCLANT), P/T 7 (CHAPHAL / CHATHAL), L/R 7, L/N 7, M/N 6, G/Z 5, S/Z 4.
- **Not the copyist.** The confusions measured on the Soyga tables (Z/X, N/U, I/Y, I/L, C/E) account
  for 2 of the 179 changes. The variation belongs to the text.
- **Sound classes (suggestive).** Half of the 98 consonant changes stay inside one class (stops,
  liquids and nasals, sibilants) against 21% by letter frequency; Markov-3 surrogates give 37% on
  few cases, and the classes were drawn after seeing the pairs. Needs an independent check.

## 45. Do the letter changes follow sounds? (module a41)

Classes fixed beforehand: manner (stops PBTDCGKQ, fricatives FVSZXH, nasals MN, liquids LR) and
place (lips PBFMV, tongue tip TDSZNLR, back CGKQXH).

- 14-letter variants, 98 consonant changes: inside a manner class 40.8%; by letter frequency 20.8%;
  12 pooled Markov-3 surrogates 35.8% (p 0.18). Place: 34.7% vs 41.0% surrogate.
- Fresh evidence, 10-letter passages at other positions (3,457 changes): manner 38.5% vs 35.5%
  surrogate; place 45.7% vs 46.2%. Surrogates give the same commonest pairs (L/N, L/R, H/L).
- Verdict: the sound-likeness of the changes is what the positional grammar already produces.
  REFUTED as a separate rule.
- Kept: interchangeable consonants share manner, not place, well above letter frequency; also in
  Dee's spaced words of leaf 1 (1,932 pairs: manner 25.7% vs 20.9%, p < 0.001; place p 0.28). REAL,
  as a property of the grammar.

## 46. The map of repeats, and a correction (module a42)

- **Correction.** OXAD+NOCHA is also OX+ADNOCHA (overlapping names); shuffling names counted it as a
  rare meeting. The string itself: 23 in the book, 16.4 in Markov-3 surrogates (p 0.07). REFUTED.
- **GETH+ACLAX holds.** GETHACLAX 17 vs 3.8; GETHACLAXTO 6 vs 0.25; never reversed. REAL.
- **Repeats are neighbours.** 387 pairs of sides share 12 letters: 51% inside one part (20% at
  random); inside parts 7.2 tables apart vs 8.1 (p < 0.001). Same leaf not favoured (p 0.19).
  Sisters: 20a-22a, 21b-24b, 21b-25a.
- **No drift of spelling** between earlier and later sides (best p 0.125 of 8).

## 47. Recency (module a43)

- **Cache model.** Order-3 letter model trained on half the sides: 2.920 bits per letter on the
  rest; with a cache of the same side 2.906; identical with the side's lines shuffled. No use of
  the recent past beyond the side's own vocabulary.
- **Echo by lines.** 8-letter strings: flat from 1 to 30 lines. 5-letter strings: +9% at 1-4 lines
  (z 5.4), nothing at 5-16; slightly column-aligned (p 0.02). Window chosen after the profile.
- **Echo by sides.** 15.6 per 1000 for neighbours, 9.3 at twenty sides, 7.4 at random.
- Reading: the unit of memory is the leaf and its neighbourhood; inside a side the lines are almost
  exchangeable, with a faint trace over four lines.

## 48. Positive control (module a44)

The King James Bible, cut like the tables, is seen by all three blind tests (next unit z 15.7;
order of lines 0.025 bits, z 10.0; echo over four lines +68%, z 37.8). Word-shuffled Bible and
Markov-3 surrogates: nothing. Tables 2-24: next unit z 1.9; order of lines 0.0023 bits (z 4.5);
echo +8% (z 5.3). Prose-like sentences along the rows would have been detected. The Calls (4,700
letters) are too short for these tests. Source of the control: Project Gutenberg #10, kept in
data/raw/ (not redistributed).

## 49. What decides the variant (module a45)

129 frames, 3,420 occurrences. Filler depends on part (z 8.5), table inside the part (z 3.7),
nearest vowel before the frame (z 3.1). Not on side a/b, row, column, or the previous choice
(z 0.3). No positional channel.

## 50. The false book (module a46)

G5L (five letters of context, model per side with three neighbours each way) reproduces repeats of
12 (378 vs 365), master names (1866 vs 1861), GETHACLAX (9 vs 10), the gradient between sides.
Residue: echo over four lines; one-letter variants of long passages (110 vs 74); repeats of 14
(70 vs 53).

## 51. Templates and the limit of five letters (module a47)

- Templates with one free slot: 566 of 9 letters (G5L 582), 59 of 11 (G5L 52, up to 70), 5 of 13
  (G5L 1). The machine produces them. Examples: AHN_CHASTOR (O 10, E 5), DNO_HANZACH (C 7, T 2).
- Memory beyond five letters, permuting inside (context, side): tables z 1.3 / 1.3 / -0.8 / 0.4 /
  0.7 at 6, 7, 8, 10, 14 letters back; false book about 0; Bible 16.6 / 17.5 / 21.6 / 13.0 / 7.3.
- Two-slot templates six letters apart: only 2 with enough occurrences; no test possible.
- Reading: inside a side the row-written tables behave as a five-letter process with the leaf's
  vocabulary. No word order, no long-range agreement.

## 52. The limit of five letters in the other formats (module a48)

- Beyond five letters: chessboard 25b-28b z -0.8 / 0.3 / 1.1 / -0.4 (Bible same shape 7.8 / 8.2 /
  9.0 / 5.5); diamonds 29-40 about 0 (Bible 4.7-10.2); diamonds 41-48 about 0 (Bible 2.6-8.9).
  Few testable contexts in the diamonds (236 and 46).
- Echo over four lines, against same-shape surrogates: rows z 7.0; chessboard z 3.9; diamonds z 1.1
  and 1.4. Naive shuffling fakes an echo of 1.4 where lines differ in length.
- Leaf 1 is not in the decoded book used here; not tested.

## 53. Junctions and the leaf (module a49)

- Start of a row given the end of the row above: 12.47 bits against 13.91 for rows in random order
  (z 15.9); 44 of 46 sides positive. Upwards z 1.0, boustrophedon z 1.4, across the leaf z 1.1, last
  row of a side to first row of the next z -0.8. Inside a row the same three letters cost 7.05.
- Same letter on both sides of the break: 85 against 161 (z -7.0). Inside rows: 643 against 9,250.
- Names split between rows: 32 against 16.7 (z 3.0). Examples: 13b rows 45-46 NOCHASTORA; 7a rows
  39-40 CHASTOR; 12b rows 48-49 ANZACH.
- Two sides of a leaf (13 leaves): same cell, mirrored, upside down, transposed: nothing. Half turn
  8.94% against 8.40% (p 0.002; 0.01 corrected): suggestive only.
- Reading: a side is one stream written downwards; the row end is a favoured pause, not a wall.

## 54. Junctions in the other formats; the catalogue recounted

- Diamonds 29-40: next diagonal 13.86 bits against 15.26 (z 10.6); 41-48: 13.64 against 14.56
  (z 6.2); opposite order nothing. The stored order of the diagonals is the order of the stream.
- Chessboard leaves 25b-28b: z 2.4 forwards, 3.7 backwards; by colour, forwards on 25b colour 0 and
  27b colour 1, backwards on 25b colour 1, 26b, 27a colour 1, 27b colour 0; others nothing. Open.
- Catalogue: names counted along the whole side on rows and diamonds; 51 of 3,968 occurrences are
  split between two lines (CHASTOR 5, NOCHA 8, OXAD 9, ACLAX 6, ADNOCHA 4, ANZACH 3).

## 55. Order of the diagonals on leaves 25b-28b (module a50)

- Settled alone: 25b colour 0 and 27b colour 1 (both down-right), stored order, z 3.2 and 3.5.
  Independent signs: same letter across a junction 1 against 6.2; names split 4 against 0.3 (z 6.6).
- Pooled by road: down-right stored order z 3.0 (the two above carry it); up-left opposite order
  z 3.2 (5 blocks); down-left opposite order z 3.0 (2 blocks). On the blocks not settled alone the
  rule gives same-letter 21 against 36 (z -2.9); reversed rule z -0.6.
- Geometry: an up-left colour in opposite order is a down-right stream on a page turned half round.
- Unsettled: row blocks of 26a and 27a, zones of 26a colour 0, down-right colours of 26b, 27a,
  28a, 28b alone.

## 56. The word points (module a51)

- Source: Peterson's rows keep the points and accents on 2a, 2b, 3a, 3b (full), 4a, 4b, 5a (part):
  232 rows, 1,425 words, 1,193 points inside rows. Our loader had dropped them.
- HZEMBL (leaf 1: "...h zembl...") and DAHOXI ("dah.oxi...") cross word boundaries. Withdrawn.
- 1,383 different words; 95.2% written once. Leaf 1 67.5%, Calls 56.9%, Bible 8.8%. Mean length 8.0.
- Names: whole word 3, start 13, end 11, inside 20, cut by a point 10 (24.6 at random; z -4.2).
- Row edges: last word 7.4 letters, first 8.9, inner 7.9; blind cutting would give 5.1.
- Segmenters: F1 0.335 (word model), 0.223 (surprise), 0.114 (random).
- Accents: 59% of words; next-to-last vowel 391, earlier 443, last 64.

## 57. Two imprints (module a52)

- Read as English / Latin (bits per letter): tables 5.57 / 6.32; leaf 1 5.58 / 6.19; Calls 5.83 /
  6.30; English 2.93 / 5.23; Latin 4.98 / 3.06; Soyga 8.13 / 8.52.
- Observed / expected: doubles 0.07 (English 0.44, Latin 0.39, Calls 0.37, leaf 1 0.15, Soyga
  0.90); ABA 0.57; alternation 1.50; three consonants 0.14; two vowels 0.24.

## 58. kondor.de (module a53) and the diaries

- 846 rows aligned; 23,712 letters in rows of equal length; 1 differs; no n/u; same pointed sides;
  same 13 irregular rows. A copy of Peterson.
- Diaries (secondary notes in data/raw): leaf 1 dictated 29 March - 6 April 1583; leaf 18 read on
  15 April; "24 leaves being written" on 18 April; tables finished 6 May. The end of the
  row-written tables (25a/25b) coincides with the 18 April count. On 20 June the words were still
  to be "distinguished" and accented: the points stop at leaf 5.

## 59. The diaries read, and four tests taken from them (module a54)

- The record: docs/WHAT_THE_SOURCES_SAY.md. The tables are an instrument opened by the Calls, not a
  discourse; "Interpret not"; "every letter ... bringeth furth the Names of God".
- Leaf 1 side 1: 25 of the first 30 rows have exactly 49 words: a table of words, as the diary says.
- Leaf 1 as a key square for square: 336 tests, mean z -0.1. Refuted.
- Nine letter rows of leaf 1 side 2: 3.84 bits under the tables' model (tables 2.80; leaf-1 words
  4.79; shuffled 6.76); NACHO and OXAD already present.
- Leaf 18: not set apart from tables 13-24.

## 60. The manuscript seen (images of Sloane 3189)

- 25b-28b: every square filled; two series on alternate squares, tilted, turned half round from one
  another. Confirms on the page what a50 found from the junctions.
- 29-48: the same square ruling, letters on alternate squares only. One series of a chessboard, not
  a lozenge. Note on 43a: "every empty square is to be filled as these are".
- 8a, 9a, 10b, 11a carry figures (capitals, ring, boxed corners, inset blocks): the irregular rows.
- Leaf 1 side 1 is not in the book; f.57 is empty grids with two lines of angelic characters.
- n and u mostly cannot be told apart; z and x can.
- Two views were checked directly for this note (f.34 and f.42 regions); the rest is the reading
  recorded in data/raw/notes_sloane3189_images.md.

## 61. The 21 words of the 49th leaf (module a55)

From the diary (18 June 1583): Loagaeth seg lovi brtnc / Larzed dox ner habzilb adnor / doncha Larb
vors hirobra / exi vr zednip taiip chimvane / chermach lendix nor zandox (22 tokens printed, 21
words; one division doubtful). Never in our data before.

- Short words occur freely in the tables: DOX 545, VR 482, NOR 144, NER 56, VORS 27, ADNOR 17,
  DONCHA 17, SEG 13, LARB 3, EXI 2, LOVI/LARZED/ZANDOX 1.
- The long words occur nowhere: LOAGAETH, BRTNC, HABZILB, HIROBRA, ZEDNIP, TAIIP, CHIMVANE,
  CHERMACH, LENDIX. They carry consonant clusters (BRTNC, HABZILB, ZEDNIP) absent from the tables.
- Read under a letter model of the tables they cost 4.23 bits (leaf-1 model 4.58, Calls 4.42); a
  real table row costs 2.51. They are neither table language nor leaf-1 language: a third register.
- Only catalogue link: DONCHA is DONCHAL without its last letter.
- Fits the diary: Galvah calls the first leaf "a hotchpot without order", unlike the ordered tables.

## 62. "One Name", measured (module a56)

Reading the diary's "they are but one Name" as "few roots": under the affix rules (prefixes AD-,
NO-, NE-, NI-, ZI-, A-, AX-, AL-; suffixes -A, -AL, -AD, -H, -HA, -R, -TO, -TOR, -P) and an interior
A/O/E fold, the 58 recurring names collapse to 45 roots. Surrogate name-sets (Markov-3 strings of
the same lengths) collapse to only 57.9 (p 0.002): the rules compress the real names far more than
random strings. But 45 roots is not one: the largest (CHAS: CHASTOR, ICHASTOR, NECHASTOR,
NOCHASTOR, ZICHASTOR) covers 5; the five biggest cover 26%. The literal "one Name" is not supported;
the family structure (a23, a28) is confirmed by a second method. (Root-stripping is approximate, so
a few roots that should merge stay apart; the headline is robust to that.)

## 63. Two reader claims checked (module a57)

- **DAHAHOXOM.** A practitioner was addressed by an angel "DAHAHOXOM" and thought DAHOXI resembled
  it. DAHAHOXOM and its near forms (DAHOXOM, DAHAHOX, AHOXOM, HOXOM) occur nowhere in the book,
  forward or backward, whole or by leaf. DAHOX occurs 6×; 3 are DAHOXI, which in the pointed tables
  is "dah.oxi" across a word point (two words, a51). The angel name is not in the text, so the
  resemblance cannot be tested against the book; the experience is respected, not contradicted.
- **Calls assembled from scattered letters.** The reader notes the first two Calls look built from
  letters spread through the whole book, unlike Watchtower names. Confirmed three ways: (1) the
  diary indexes each Call letter to a table and number, and the tables are scattered (21st, 41st,
  46th; 13 April 1584); (2) a35 could not recover the number→place rule; (3) fresh test: Call words
  (≥4 letters) occur as whole strings in the tables only 144× against 136.9 for random strings of
  the same lengths (z 0.8) — first two Calls 21/89 vs 21.7 — so they are not localized chunks.

## 64. DAHAHOXOM, the wide search

A reader was addressed in evocation by an angel DAHAHOXOM and asked whether it, or its halves
(DAHA + HOXOM, DAH + AHOXOM, DAH + AHOX + OM), is in the book. Searched exhaustively: eight reading
paths (rows both ways, columns both ways, the two diagonals, the two anti-diagonals), scribe
letters folded (V/U, Z/X, I/Y, J/I), and approximate matching up to two edits.

- The whole name DAHAHOXOM never occurs, in any path or direction.
- The distinctive parts AHOXOM, HAXOM, HAHOXOM never occur. DAHA is a common fragment; OXOM occurs
  a few times; DAHAH, AHOXO, AHAHOX occur once or twice. The two ends never sit together.
- The single nearest form in the whole book within two edits is DABAHOXIM on leaf 2b — and in the
  pointed transcription it is "…APRINDABAH.OXIMAGEN…", i.e. the words APRINDABAH and OXIMAGEN run
  together across two word points. Like DAHOXI = "dah.oxi" (a51), it is a word-boundary artefact,
  not a word.
- Reading: the LETTERS of DAHAHOXOM are all in the book, but scattered and never adjacent. By the
  book's own method — each name's letters gathered from numbered places in different tables (a57) —
  the name could be assembled letter by letter; it is simply not written anywhere as a unit. The
  resemblance the reader felt (DAHOXI ~ DAHAHOXOM) is a real surface pattern, but every form close
  to it that the book produces comes from reading across the word-separating points.

## 65. The Call words along every reading path (module a59)

The reader's idea: search the tables for the Call words read other ways — diagonals, backward,
columns. Eight paths tested (rows both ways, columns both ways, two diagonals, two anti-diagonals),
Call words forward and reversed, against two nulls and a placebo wordlist (Dee's leaf-1 words).

- Under a Markov-3 surrogate of each path's stream, the anti-diagonal reaches z 3.6 — looked like a
  signal. It does NOT survive the stronger word-scramble null (each word's own letters shuffled):
  anti-diagonal z 1.5, and the leaf-1 placebo z −0.6 there. One of eight paths; not robust.
- On the rows both Calls (z 8.9) and leaf-1 words (z 23.3) beat letter-scrambles — but that is what
  any real Loagaeth-structured word does in a Loagaeth stream; the placebo beats the Calls, so it is
  a property of the language, not hidden placement of the Calls.
- Conclusion: no reading path hides the Calls. Matches a57 and the diary: the Call letters are
  gathered from scattered numbered places (different tables), not laid along one path.

## 66. Any trace of later tampering? (module a60)

Two kinds of alteration: one that breaks the text's rules (detectable), one that preserves the local
statistics (invisible from one copy).

- Bits per leaf: flat (mean 2.16, sd 0.08), no outlier. A replaced or scrambled leaf would show.
- Doubled-letter rate: two mild high leaves (3a, 7b), the extra doubles spread across many rows, not
  a localized corruption.
- Letter profile: 43-48 distinct = the known fourth segment (a15), not a seam.
- Largest bits jumps: 24b|25a and 25a|25b (the rows→chessboard format border), which matches the
  diary's "24 leaves written by 18 April 1583". Structural, not tampering.
- Geometry: 13 of the 20 leaves 29-48 are exactly 1201+1200=2401; the other seven are off by one or
  two cells (~0.1%, ordinary copying slips) or in the known irregular end 44-48 (leaf 36 is off by 25,
  the largest). None is scrambled; a shuffle would not leave near-complete grids.
- Conclusion: no trace of alteration that broke the text's rules; the book is a coherent whole whose
  seams the record explains. LIMIT: alteration preserving the local statistics (a same-dialect leaf
  swap, letter substitution keeping the letter-flow) cannot be caught from one transcription; only an
  independent copy could. The one ground-truth check (Soyga tables, Reeds' generator, a36) shows 3.3%
  copying error, no systematic tampering.

## 67. Navigation numbers and the Soyga-rule hypothesis (module a61)

- **Nalvage's numbers.** Using the exact letter-by-letter instructions from the diary (TFR 173-174)
  and checking each decoded cell against the letter it must hold, the best decoding (row-major, or
  column-major with a one-table offset) lands right only 4-5 of ~24, against 2.2-2.6 expected by
  chance - within the noise of twelve combinations. The numbers run to 312004, far past a table's
  2401 cells, so they encode a path whose traversal Dee never wrote down. Not recoverable. Sharpest
  test yet; confirms a35.
- **Soyga-style rule.** A Soyga cell is fixed by the cell above plus a function of the cell to the
  left (Reeds). A Loagaeth cell keeps 3.02 bits of entropy of 3.95 given its above and left
  neighbours - they remove only 0.94 bits (the ordinary row-flow), not the ~all that a deterministic
  rule removes. The Loagaeth is not generated by a Soyga neighbour rule.

## 68. The book as a chant, and as a cube (module a62)

- **Chant (REAL).** The rows are tuned to a syllable count: ~17.65 syllables per 49-letter row, spread
  sd 1.05 - well below the sd 1.70 the same rows give with their letters shuffled (z -24). So the beat
  is not just the fixed line width; the vowel/consonant arrangement holds it (the strict alternation
  of a52 is the mechanism). Stress falls on the penultimate syllable far more than any other (452),
  then the antepenultimate (301), rarely the last (72). The lines carry metre - consistent with a
  text the record says is intoned ("sounded Logah", the accents of a51). This is the first structural
  trace of the book's spoken use.
- **Cube (REFUTED).** 49 leaves x 49 x 49: no readable third axis. The same cell on adjacent leaves
  shares 0.0016 bits above chance (z ~6 but negligible - the dialect of neighbouring leaves, a43), and
  no names read down the depth axis (z 0.4). "Every element hath 49 understandings" is not a literal
  third dimension.

## 69. The metre, developed (module a63)

- The ~17.6-syllable beat is a constant of the main body: segment I 17.58, II 17.71, III 17.89; it
  loosens only in the end segment V (16.0, the U-register tail).
- Stress rhythm on the accented tables 2a-5a: stresses fall mostly three or four syllables apart
  (mean interval 3.75), more regularly than the same number of stresses placed at random (sd 1.79 vs
  2.64, z about -9 to -11 across samples).
- So each line has a fixed length in syllables and a recurring stress - metre, not just a count. The
  first measurable structure of the book's spoken use.

## 70. Finer chant structure — rhyme, syllabary, melody (module a64)

Beyond the metre (a63): no further poetic structure.
- Rhyme: consecutive lines share their last two letters only a little above shuffled (z ~2). No rhyme scheme.
- Syllabary: ~441 syllables cover 90% of the text, against ~505 for a Markov-3 surrogate — barely more closed.
- Vowel vs consonant: the order structure lives in the consonants (~0.71 bits saved against shuffle),
  not the vowels (~0.13). No vowel melody; the pattern is the consonant skeleton of the names.
- So the lines are metrical (syllable beat + stress) but not rhymed, and carry their structure in the
  consonants — consistent with a book of consonant-framed names set to a beat.

## 71. Bridges, refrains, acrostics — all null (module a65)

- Bridges: the 91 governors appear in the tables 1 time (random 0.1), the Heptarchy names 1 time —
  Poisson noise on long rare strings. The systems stay separate (confirms a25; matches the record,
  which makes the Loagaeth a different language from the Calls and the Great Table).
- Refrains: no whole line and no 20-letter line-opening ever repeats. No chant refrain.
- Acrostics: no recurring name reads down the left or right margin (0 vs ~0.3 expected). (Reading a
  whole top/bottom row finds names, but that is ordinary row text, not an acrostic.)
- So the book's structure is the names set in metrical rows (a62-a64); nothing hides in other
  systems, refrains, or margins.
