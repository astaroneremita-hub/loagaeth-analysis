# Appendix A — How to redo each measure

Every finding in this book is **reproducible bit by bit**. The discipline (Ch. 0):

- **Standard-library Python**, no external dependencies in the analysis.
- **Fixed seed: 1583** (the year of the Book's first reception). All randomness — shuffles, surrogates, permutations — starts from it, so each run returns the same numbers.
- **Null models** behind every claim: shuffle, Markov-3 surrogate, controlled permutation (Ch. 0).
- **Explicit verdict**: REAL / REFUTED / DESCRIPTIVE / LEAD.

## The analysis modules

The measures live in `src/aNNN_*.py`, numbered in the order they were made. Main groups:

- **a01–a22** — foundation: positional grammar, no-doubling rule, line edges, four segments, families (CHASTOR), the two houses, the seam's diagonal reading, single path in the diamonds, vocalic register.
- **a71–a106** — the territory and generator phase: line stratification, names woven into the grid (high z), territory map, generative grammar, grammar-discovered names, gematria and cross-system (refuted), entity profiles.
- **a190+** — the external-names and sound phase: Watchtower traces (refuted), angels by sub-angle (refuted), the sound axis (pronounceability, assonance, final vowel, melody-A, A-pulse), the two voice registers, the sign×planet elemental conflict, the dissolution arc.

Each module writes a `results/*.json` with its test's statistic and z-score.

## The data

- **Primary source:** transcription of the 48 leaves of the *Liber Loagaeth* (Sloane MS 3189), two sides per leaf; leaf 1 spaced into words (lexicon); the 49th only by report.
- **Alphabet:** 21 Enochian letters — A B C D E F G H I L M N O P Q R S T U X Z.
- **Comparison corpus:** Calls (Claves Angelicae, Sloane 3191), Watchtowers, 91 governors, Heptarchy, gematria (Liber Scientiae, *True and Faithful Relation*).

## The interactive screens

The visualizations (in `viz/`, served locally) accompany the analysis: bilingual catalog, voice of the Loagaeth, occurrence map, structure/loom, dialects, recurrent names, practical guide, Calls↔tables, ritual.

\newpage

# Appendix B — Glossary

- **Null model.** A version of the book without the tested structure (shuffled, surrogate or permuted), against which the real is measured.
- **z-score.** How many standard deviations the real value lies above/below the null. |z|>3 real; |z|>6 decisive; negative z = anti-structure.
- **Markov-3 surrogate.** A text generated respecting the real book's 3-letter transition probabilities; preserves local phonotactics.
- **Babel principle.** A large enough inventory accepts anything by chance; hence only what beats the null counts.
- **House.** A grammatical class of names (house NOCHA D-/AD-; house GETH L-/X-), distinguished by affixes and vocalic register.
- **Family.** A set of names with a related consonantal root (CHASTOR, NOCHA, GETH, ANZACH, DAXVAR, ACLAX, CHIDNO, ALGETH).
- **Minimal pair.** Two names identical except for one vowel (e.g. *pola/pala*); proof that the consonant is identity and the vowel is register.
- **Template.** The vertical (column) pattern that sustains form without carrying meaning (z=+173).
- **Anti-repetition.** The line's tendency to avoid repeating letters/patterns (z=−77); the line "advances".
- **Seam (26–28).** The threshold band of maximum chaos where the reading migrates to the diagonal.
- **Dissolution arc.** The deep (leaves ~41–48), where names vanish, the vowel darkens and elemental identity fractures.
- **Sound axis.** The set of properties that make the book singable (pronounceability, assonance, final vowel, melody-A, A-pulse).
- **Two registers.** The same language in speech (Calls) and in invocation (table-names).

\newpage

# Appendix C — Closing note and research credit

This book is the honest record of a study that measured the *Liber Loagaeth* with statistical discipline and kept two planes apart: what the measurement can assert (Parts I–II) and what the practice does with what remained (Part III). The method is the argument: **nothing counts without beating the null**, and what failed is reported as loudly as what passed.

Any use of the findings, methods, terms or data of this work requires the attribution of the license page:

> Astaron Eremita. *Liber Loagaeth — Anatomy of a Sealed Language.* 1st ed., 2026.

*"Every letter here bringeth furth the Names of God: but they are but one Name."*

\newpage
