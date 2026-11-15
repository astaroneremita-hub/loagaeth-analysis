# Chapter 0 — Method: the discipline of the null model

## The problem of staring into chaos

A 49×49 grid of letters — 2,401 cells — repeated across nearly fifty leaves is fertile ground for **pareidolia**. In half a million letters, any name, any word, any "code" one looks for will be found, exactly as faces are found in clouds. The central problem of any honest study of the *Liber Loagaeth* is not to **find** patterns — it is to tell the **real** patterns from the ones chance manufactures. We call this the **Babel principle**: a large enough inventory accepts anything. The digits of π contain your name, mine, and every angel name ever written — that does not make them a grimoire.

Hence the single, inflexible rule of this study:

> **No pattern counts as real until it beats a null model.**

## The null models

For each claim, we build a version of the book **without** the structure being tested, measure the same phenomenon on it, and compare. Three nulls, from weakest to strongest:

1. **Shuffle.** The same letters, in the same quantities, in random order. Preserves each letter's **frequency**, destroys all order. It is the base null for almost everything: if the real phenomenon does not beat the shuffle, it is pure effect of the letter composition.

2. **Markov-3 surrogate.** A text generated letter by letter respecting the three-letter transition probabilities of the real book. Preserves the **local habits** of writing (the common pairs and triples). A pattern that beats the shuffle but **not** the Markov-3 is merely a by-product of the phonotactics — not an independent signal.

3. **Controlled permutation.** For positional and directional tests, only the relevant units are shuffled (the rows of a face, the order of the leaves), preserving the rest. Isolates the specific effect.

## The ruler: the z-score

A finding's strength is the **z-score**: how many standard deviations the real value lies above (or below) the null distribution.

- **|z| < 2** — within chance. Does not count.
- **|z| ≈ 2–3** — suggestive, fragile. Reported as a *lead*, not a finding.
- **|z| > 3** — real. Survives the null.
- **|z| > 6** — decisive.

A strong **negative** z is also information: it means the real value is **below** chance — an anti-structure (for example, letters that avoid each other).

## Conventions and honesty

- **Fixed seed (1583).** All randomness uses the same seed — the year of Dee's first reception of the Book — so that every test is **reproducible** bit by bit.
- **Standard-library Python.** No external dependencies in the analysis: anyone can run the modules (`src/aNNN_*.py`) and get the same numbers.
- **Explicit verdict.** Each finding is marked **REAL** (beat the null), **REFUTED** (fell) or **DESCRIPTIVE** (a fact true by construction or inspection, with no claim of hidden signal).
- **What failed is reported as loudly as what passed.** A cherished hypothesis that falls is a result, not an embarrassment. Part II of this book exists for that.
- **Separation of planes.** The measurement answers "is there objective structure?". It does **not** answer "does it work as magic?" — a question of another plane, the operative one, which Part III treats in its own logic. Conflating the two is the error this book avoids end to end.

## The data

The source is the transcription of the 48 leaves of the *Liber Loagaeth* (Sloane MS 3189), each leaf with two sides ("a" and "b"), most of them dense 49×49 grids; leaf 1 is spaced into words (it is the **lexicon** page); the 49th leaf "that is not, was not, and shall not be known" exists only by report. The alphabet is the 21-letter Enochian (A, B, C, D, E, F, G, H, I, L, M, N, O, P, Q, R, S, T, U, X, Z). The comparison corpus — Calls (Claves Angelicae), Watchtowers, 91 governors, Heptarchy, gematria — comes from the reference editions (Sloane 3191, *True and Faithful Relation*, Liber Scientiae).

With the method in place, let us turn to what the measurement revealed.

\newpage
