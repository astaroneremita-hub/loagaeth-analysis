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
