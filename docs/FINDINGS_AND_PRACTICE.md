# Liber Loagaeth — what we found, and what to do with it

This is the summary of the whole study (67 analysis modules, `src/a01`–`a67`, plus the primary
record). Every claim below was measured against a null model and is reproducible from the code; the
exact figures and the diary citations are in `RESEARCH_LOG.md`, `SESSION_FINDINGS.md` and
`WHAT_THE_SOURCES_SAY.md`. This page says, in plain terms, what the book is, what is really in it,
what is not, and how a practitioner can use it.

---

## 1. What the book is

The Loagaeth (Sloane MS 3189) is 48 leaves, 49 with the one "that is not, was not, shall be known",
each a 49 × 49 grid. On the first leaf a square holds a word; on the rest a single letter. The diary
says plainly what it is for: **"There is no other reading of the Book, but the appearing of the
Ministers and Creatures of God"**, and **"Interpret not."** The 49 tables answer to 49 voices or
Calls, the Keys that open 48 of them; the first has none, "it is of the Godhead."

Our measurements reach the same place from the other side. The tables are **not a message to
translate**: no sentence structure survives a test that finds sentences in ordinary prose; the
words of the pointed tables are each written once and never again; the text is a short-memory process
(about six letters) built of **recurring names in families**. "Every letter here bringeth furth the
Names of God: but they are but one Name." So the book is an **instrument of names**, as the record
says — and what we can study is its form.

---

## 2. What is really in it (measured, with a null)

- **Names.** 49 recurring strings (plus the 13 master names), in **5 families** and **two houses** —
  GETH · ACLAX, and NOCHA. CHASTOR is the largest. GETH + ACLAX is a real fixed-order compound. Each
  name has a **territory** — the region of the book where it concentrates. Catalogued, with its
  sides, family, house and passages, in `viz/names_catalog.html`.
- **The names are built by rule.** Prefixes (AD-, NO-, NE-, ZI-, A-, AX-), suffixes (-A, -AL, -AD,
  -H, -HA, -R, -TO, -TOR), and a single interior vowel swap (A ↔ O ↔ E) generate the family. Under
  these rules the 58 names collapse to 45 roots — far more than random strings, but **not to a single
  seed**: the literal "one Name" is the family structure, not one root.
- **A presiding name per table** (see §3): most leaves have one name significantly over-represented.
- **The language.** A positional grammar; the **no-doubled-letter rule** (a letter follows itself
  about 11× below chance); consonants that interchange share manner of articulation; long repeats
  real but bounded to ~6 letters of memory. A per-leaf "vocabulary": neighbouring leaves share
  formulas, the likeness fading with distance.
- **The page.** Four segments with measured borders that match the diary's writing dates. The lines
  of a side are **one stream read downward**; names straddle the line break. Leaves 25b–28b carry
  **two currents** on alternate squares, the second written turned half round — confirmed on the
  manuscript images. Leaves 29–48 split the two chessboard colours one per side (the "diamonds").
- **The book is a chant.** The lines carry **metre**: ~17–18 syllables per 49-letter line, far more
  regular than chance, constant across the main body; the **stress falls on the penultimate
  syllable**, and stresses recur every **three to four syllables** (a foot). The structure lives in
  the **consonants** (the name-skeletons); the vowels carry the beat. The accents that survive on
  leaves 2a–5a are a guide to intoning it.
- **Not tampered.** The book is internally homogeneous: no leaf stands out as replaced or scrambled,
  the chessboard geometry adds up (1201 + 1200 = 2401), and the only sharp seams are the known format
  borders, which match the diary's dates. The one place with a known ground truth (the Soyga tables
  at the back) shows ordinary ~3% copying error, no systematic alteration.

---

## 3. The presiding name of each table (a working list)

For each table, the recurring name most over-represented there (Poisson p; from `a67`). This is the
name most **at home** on that leaf — a starting point for a practitioner opening it, not a claim that
it is the table's "true" minister (the record names a minister for no leaf except leaf 18, "of the
spirites of the earth").

| Table | Presiding name | over chance | Table | Presiding name | over chance |
|---|---|---|---|---|---|
| 6 | OXAD | 2.3× | 22 | ANZACH | 4.4× |
| 7 | NACHOA | 5.7× | 23 | ACLAX | 2.7× |
| 8 | PHANGE | 6.9× | 24 | GETH | 2.3× |
| 10 | ALGETH | 2.9× | 25 | ANZACH | 6.1× |
| 11 | NACHO | 4.2× | 26 | ALGETH | 3.9× |
| 12 | NOCHA | 2.8× | 27 | ALGETH | 3.9× |
| 13 | ADNOCHA | 4.5× | 28 | ACLAX | 3.4× |
| 14 | NOCHA | 2.9× | 29 | ACLAX | 6.9× |
| 15 | GRADAX | 9.0× | 30 | ACLAX | 6.1× |
| 16 | NOCHA | 2.2× | 31 | GETH | 3.2× |
| 17 | ACLAX | 3.4× | 32 | CHASTOR | 4.4× |
| 19 | NOCHA | 2.5× | 33–48 | GETH house (GETH, ALGETH) | — |
| 20 | ADNOCHA | 4.1× | 21 | ACLAX | 5.0× |

The map is coherent: the **NOCHA house** (NACHO, NOCHA, ADNOCHA) rules the early–middle leaves
(7–22), the **GETH house** (ACLAX, GETH, ALGETH) the later ones (17–48), with CHASTOR around leaf 32.
The full per-table list, with significance, is in `results/67_presiding_names.json`.

---

## 4. What is NOT in it (each refuted with a null)

Sentences or a translation in the letters · a cipher of hidden meaning · long codes · copying or
mirroring between sides · numerology or gematria of the names · a recoverable rule behind Nalvage's
position numbers · the Calls hidden along any reading path (rows, columns, diagonals, backward) ·
sound-classes as a rule of their own · rhyme · a vowel melody · a closed syllabary · refrains
(repeated lines) · acrostics down the margins · bridges to the Heptarchy, the governors or the Great
Table · a 49×49×49 cube with a readable depth · a Soyga-style neighbour-generation rule · a 7-fold
rhythm (49 = 7×7 is the frame, not a beat) · the angel name DAHAHOXOM as a word (its letters are in
the book but scattered) · alteration that broke the text's rules.

This long list of honest "no"s is not failure. Most are exactly what the record predicts, and
together they are the proof that the book is what §1 says: an instrument of names, not a coded
message.

---

## 5. The limits

- **One transcription.** All of this is Peterson's reading. We can detect alteration that broke the
  statistics; we **cannot** detect alteration that preserved them (a same-dialect leaf swap, a
  letter substitution keeping the letter-flow). Only an **independent copy** (Klein's forthcoming
  edition, or the 17th-century copies) could. kondor.de is a copy of Peterson, not independent.
- **n and u** are mostly indistinguishable in Kelley's hand; any finding that leans on telling them
  apart (the U register of 41–48) is provisional.
- **Meaning is sealed.** No word of the tables has a gloss in any source. What the names mean is not
  in the record; the letter-sense layer (Un = force, etc.) is a practitioner's attribution, labelled
  as such, not evidence.

---

## 6. Using the names, and testing them

The record permits exactly one use — opening a table by its Call, to the appearing of its ministers —
and forbids reading the letters for a message. Everything below stays inside that frame.

**A. The names as a working set.** The 49 + 13 names, with their families, houses, territories and
presiding leaves, are a concrete set of names the book itself repeats and sets apart. They are the
best-grounded candidates in the book for the "Names of God / ministers" the diary speaks of. Open
`viz/names_catalog.html`; to work a name, go to its heaviest leaves.

**B. Which name with which table.** Use §3: open table N, and the presiding name is the one most at
home there. Call n opens table n + 1 (the record's rule); the first table has no Call.

**C. How to intone a line.** The lines are metrical. To speak a row of a table: take it in ~17–18
syllables, with a light beat every three to four, and the **stress on the next-to-last syllable** of
each word. On leaves 2a–5a the manuscript's own points and accents give the word breaks and the
stressed vowels directly (`data/loagaeth_word_points.json`).

**D. The names are pieces of longer words.** In the pointed tables the recurring names are roots and
endings inside longer, once-written words. So a name like NOCHA or ADNOCHA is a **building block**,
not necessarily a whole utterance; the full "word" it sits in is unique to its place.

**E. How to test, honestly.** The study cannot test the practice — the manuscript is not that kind of
evidence, and we never pretend otherwise. But the practitioner can, and the book's own frame says
how: open a table by its Call, intone it as in C, hold the presiding name of §3, and **record the
result** — which ministers/impressions appear, with the table, the name, the date. Over many
workings a diary of (table, name, result) is itself data: if certain tables or names reliably
produce certain effects for you, that is the book doing what the record says it does, measured in the
only place it can be — the practice. (This is what the `diario-ritual` skill is for.)

**F. What would change the research picture.** An independent transcription (to catch hidden
alteration), or the full text of Sloane 3188's earlier books (which might hold the number rule or the
contents of other leaves). Everything else in the letters has been measured.

---

*Nothing in this study is evidence for or against the reality of the entities a practitioner may meet.
It describes the text. The practice is the practitioner's, and the record places the meaning of the
book there — in the appearing, not on the page.*
