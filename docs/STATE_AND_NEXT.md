# Where the study stands, and what is worth doing next

Written after reading the primary record (`WHAT_THE_SOURCES_SAY.md`). Fifty-five analysis modules
(`src/a01`–`a55`) and the diaries now agree on one picture. This page states the picture, then ranks
the analyses that are genuinely possible with the data in hand.

## 1. The settled picture

**What the book is, by the record and the measurements together.** The Loagaeth is 48 leaves (49
with the one that "is not, was not, shall be known"), each a 49 × 49 grid. On the first leaf a square
holds a word; on the rest a single letter. It is not a discourse to be translated — "there is no
other reading of the Book, but the appearing of the Ministers"; "Interpret not". The measurements
reach the same place from the other side: no sentence structure survives a test that finds sentences
in the Bible cut the same way (a44); words of the pointed tables are written once and never again
(a51); the text is a five-letter process (a47, a48) built of recurring names in families that vary
by one letter (a23, a28, a40). "Every letter here bringeth furth the Names of God: but they are but
one Name."

**The forms we have described (real, null-tested):**

- *Names.* 49 recurring strings in 5 families, two houses (GETH·ACLAX, NOCHA), with territory by
  leaf; CHASTOR the largest; GETH+ACLAX a real fixed-order compound (a23, a28, a42). Catalogued in
  `viz/names_catalog.html`.
- *The language.* A positional grammar; the no-doubled-letter rule (11× below chance); consonants
  that interchange share manner of articulation; long repeats real against Markov-3 but bounded to
  about six letters of memory; one leaf's vocabulary writes its own region (a19, a31, a40, a46).
- *The page.* Four segments with measured borders (a27) that match the diary's writing dates; the
  lines of a side are one stream read downward, names straddle the line break (a49); leaves 25b–28b
  carry two series on alternate squares turned half round from one another — **seen on the
  manuscript** (images; a50); leaves 29–48 split the two chessboard colours one per side (a15); the
  irregular rows are drawn figures on the page (images).
- *The scribe.* The Soyga tables at the back give the hand's error rate (3.3%); the U register is in
  the manuscript, not a misreading — but n and u are mostly indistinguishable in this hand, so any
  n/u result is provisional (a36; images).
- *The 49th leaf.* Its 21 words, recovered from the diary, are a third register: short table
  fragments plus long cluster-words found nowhere — the "hotchpot without order" (a55).

**Refuted, with a null:** sentences; a cipher of meaning in the letters; long codes; copying between
sides; numerology/gematria; a rule in Nalvage's position numbers; sound-classes as a rule of their
own; the "diamond" as a figure; OXAD+NOCHA as a compound; kondor.de as an independent transcription.

**The one thing the record forbids and we should stop doing:** searching the table letters for a
translation or a hidden message. The sources say plainly there is none to find that way.

## 2. What the sources changed

- They reframed everything above from "failed decipherment" to "description of an instrument". The
  null results are not dead ends; they are the measured confirmation of what Galvah and Gabriel say.
- They supplied data we did not have: the 21 words of leaf 49 (now a55), the writing dates that
  match our borders, the fact that leaf-1 squares hold words (confirmed, a54), the chessboard
  orientation (confirmed on the page).
- They set caution flags: n/u unreliable; leaf-1 side 1 comes from the diary, not the book; "read
  backward, the first leaf is the last" — a reading order we have never applied.

## 3. Analyses worth doing, ranked

Each is possible with data already on disk (or one short fetch), has a null, and answers a question
the record or the measurements left open.

### A. The book in Dee's intended order (new; high value)
**Question.** The diary: "Write the Book backward … the first leaf is the last." We have always read
leaf 1 → 48 in transcription order. Does the book read as one continuous stream when taken 48 → 1,
and does leaf 1 (words) sit naturally at the end after the nine transitional letter-rows?
**Method.** Junction model (a49) across leaf boundaries in both orders; name-territory gradient in
both orders; where the "transitional" nine letter-rows of leaf-1 side 2 (a54, 3.84 bits) fall
relative to the tables. **Null.** Leaves in random order. **Meaning.** If 48 → 1 flows and 1 → 48
does not, the book's direction is fixed and the transition word-language ↔ table-language is located.

### B. One generative seed for all the names (new; high value)
**Question.** "Every letter bringeth furth the Names of God, but they are but one Name." Is there a
single root from which the family-variation rules (prefix NO-/AD-/ZI-, A↔O, suffix -A/-AL) generate
the 49 names, or are there several independent seeds? **Method.** Build the edit-graph of the names
(already have families, a23/a28); find the minimum generating set under the measured rules; test
whether one root covers more than a null graph of surrogate names allows. **Meaning.** A direct,
testable reading of the diary's "one Name".

### C. Calls ↔ tables as a use artifact (new; delivery, not a test)
**Question.** The record: Call n opens table n+1; the first table has no Call. We tested text
similarity (null) but never laid them side by side for use. **Method.** Extend `names_catalog.html`
with a second view: each of the 48 Calls (from `engine/data/chamadas.json`) beside its table, the
table's heaviest names shown. **Meaning.** Turns the finding into something usable in practice,
which is the only use the record allows.

### D. Mine the nine transitional rows (new; medium)
**Question.** The nine single-letter rows that close leaf-1 side 2 read between word-language and
table-language (a55/a54). Are they the seed of the table lexicon — do the names first appear there,
in order? **Method.** Which catalogue names occur in the nine rows; branching-entropy name
discovery on them alone; compare their 3-gram profile to table 2 vs leaf 1. **Meaning.** Finds where
the two languages meet.

### E. Re-examine the U register without trusting n/u (correction; medium)
**Question.** The images say n and u are mostly indistinguishable in this hand. Our U-register
finding for tables 41–48 (a16) and the a36 calibration both lean on n/u. **Method.** Redo those
counts folding n and u together; see which results survive and which were artefacts of the
transcriber's choice. **Meaning.** Honest correction; some findings may weaken.

### F. Rebuild the loader to keep points and accents (infrastructure)
**Why.** Every module before a51 dropped the points and accents. Keeping them lets the pointed
tables (2a–5a) be read as words everywhere, and lets a reading-aid for speaking leaf 1 and leaves
2–5 be built from the stress marks the diary ordered. **Meaning.** Not an analysis; the groundwork
for using the book as the record intends (spoken, in order).

### G. Books I–IV of Sloane 3188, and the rest of TFR, read in full (source work)
So far surveyed or keyword-searched. Reading them in full may locate: a table-by-table statement of
contents beyond leaf 18; any rule for the position numbers; the relation of the 30 Aires to the
tables. **Meaning.** The record may still hold the one instruction we most lack.

## 4. What I would not do again

- Any further sentence / syntax / long-memory test on the table letters. Closed (a44–a48).
- Numerology, gematria, cross-system bridges by letter statistics. Refuted with nulls (a25, a21C).
- Trusting a single transcription for a fine n/u result. The images show why.

## 5. Recommended order

B and A first (both close a specific sentence of the record, both use data on disk, both have clean
nulls). Then D and E (shorter, sharpen what we have). C and F are delivery and infrastructure, worth
doing before any publication. G is open-ended source work, best done against a specific question
raised by A–E.
