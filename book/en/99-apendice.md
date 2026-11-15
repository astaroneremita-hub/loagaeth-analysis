# Appendix A — How to redo each measure

Every finding in this book is **reproducible bit by bit**. The discipline (Ch. 0):

- **Standard-library Python**, no external dependencies in the analysis.
- **Fixed seed: 1583** (the year of the Book's first reception). All randomness starts from it.
- **Null models** behind every claim: shuffle, Markov-3 surrogate, controlled permutation/anagram.
- **Explicit verdict**: REAL / REFUTED / DESCRIPTIVE / LEAD.
- Run everything: `python src/run_all.py`. Each module writes a `results/*.json` with its statistic and z-score.

## The analysis modules (203 results)

The measures live in `src/aNNN_*.py`, numbered in the order they were made. Main groups:

- **a01–a22 — foundation.** Positional grammar, no-doubling rule, line edges, four segments, families (CHASTOR), the two houses, the seam's diagonal reading, single path in the diamonds, vocalic register, 4–12 letter memory, 2-D rule (horizontal rules).
- **a71–a106 — territories and generator.** Line stratification (balanced inventory), names woven into the grid (king-move), territory map by two methods, generative root+affix grammar, 32 predicted new names, super-names (root chains), two lexicon layers, GETH→ACLAX syntax, gematria and cross-system (refuted), entity profiles.
- **a190+ — external names and sound.** Watchtower traces (refuted), angels by sub-angle (refuted), the sound axis (pronounceable #386, assonance #387, Latin stress #388, final vowel #391, melody-A #392, A-pulse #398), Menzerath (artifact), two voice registers #401, consonantal identity #402, balanced phonology #403, no positional template #404, grammatical classes by house #405, Ars Paulina absent #406, skip-7 and Laycock refuted #407.

## The data

- **Primary source:** transcription of the 48 leaves of the *Liber Loagaeth* (Sloane MS 3189), two sides per leaf; leaf 1 spaced into words (lexicon); the 49th only by report. Holden/Peterson transcription; checked against kondor.de (a copy, 1 letter in 23,712 difference).
- **Alphabet:** 21 Enochian letters — A B C D E F G H I L M N O P Q R S T U X Z.
- **Comparison corpus:** Calls (Claves Angelicae, Sloane 3191), Watchtowers, 91 governors, Heptarchy, gematria (Liber Scientiae, *A True and Faithful Relation*).

## The interactive screens

The visualizations (in `viz/`, served locally) accompany the analysis: bilingual catalog, voice of the Loagaeth, occurrence map, structure/loom, dialects, recurrent names, practical guide, Calls↔tables, ritual, 3D atlas.

\newpage

# Appendix B — Glossary

- **Null model.** A version of the book without the tested structure (shuffled, surrogate or permuted), against which the real is measured.
- **z-score.** How many standard deviations the real value lies above/below the null. |z|>3 real; |z|>6 decisive; negative z = anti-structure.
- **Markov-3 surrogate.** A text generated respecting the real book's 3-letter transition probabilities; preserves local phonotactics. The strongest null.
- **Babel principle.** A large enough inventory accepts anything by chance; only what beats the null counts.
- **House.** A grammatical class of names (house NOCHA D-/AD-; house GETH L-/X-), distinguished by affixes and vocalic register.
- **Family.** A set of names with a related consonantal root (NOCHA, GETH, CHASTOR, ANZACH, DAXVAR, ACLAXT, ALGETHA).
- **Minimal pair.** Two names identical except for one vowel (*pola/pala*); proof that the consonant is identity, the vowel is register. 13 vocalic vs 2 consonantal.
- **King-move.** The trace (chess king's step) by which a name is woven into the grid; measures whether the name is stitched or merely resting.
- **Template.** The vertical (column) pattern that sustains form without carrying meaning (vertical MI 0.007 bits).
- **Anti-repetition.** The line's tendency to avoid repeating letters (z ≈ −4.5); the line "advances".
- **Seam (26–28).** The threshold band of maximum chaos where the reading migrates to the diagonal.
- **Dissolution arc.** The deep (leaves ~41–48), where names vanish, the vowel darkens A→U and elemental identity fractures.
- **Sound axis.** The set of properties that make the book singable (pronounceable, assonant, Latin stress, final vowel, melody-A, A-pulse).
- **Two registers.** The same language in speech (Calls) and in invocation (table-names).
- **Generative onomasticon.** What the Loagaeth is: a book made to generate names of forces.

\newpage

# Appendix C — Closing note and research credit

This book is the honest record of a study that measured the *Liber Loagaeth* with statistical discipline and kept two planes apart: what the measurement can assert (Parts I–II) and what the practice does with what remained (Part III). The method is the argument: **nothing counts without beating the null**, and what failed is reported as loudly as what passed — more than a hundred refutations, each with its number.

Any use of the findings, methods, terms or data of this work requires the attribution of the license page:

> Astaron Eremita. *Liber Loagaeth — Anatomy of a Sealed Language.* 1st ed., 2026.

*"Every letter here bringeth furth the Names of God: but they are but one Name."*

\newpage
