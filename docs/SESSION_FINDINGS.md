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
- All 48 tables have a distinctive local name (HZEMBL, DAHOXI…); none are CHASTOR-family.

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
