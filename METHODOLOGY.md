# Methodology

The whole project rests on one rule: **an apparent pattern is not a finding until it
beats a null model that preserves the text's own local texture.** Most "discoveries"
in historical-cipher work die here. Shipping the dead ones is the point.

## The two null models (src/a07_null_models.py)

**1. Letter shuffle (weak null).** Same multiset of letters, order randomized. This
destroys *all* structure, including the ordinary syllable statistics any constructed
text has. Beating it proves almost nothing, because the real text obviously has
local letter structure and the shuffle does not. A pattern that beats only this null
is, in practice, measuring "the text has syllables," not "the text has a hidden
device."

**2. Order-k Markov surrogate (strong null).** Learn the order-k letter-transition
table from the real stream, then generate a new stream of the same length from it.
This reproduces the local syllable texture (bigrams, trigrams, the AD-AX / AX-AD
kind of repetition) while destroying any long-range or intentional design. If a
pattern does **not** beat the Markov surrogate, the pattern is a by-product of local
letter statistics — an artifact — not evidence of structure the author put there on
purpose.

We use **k = 3** (order-3 Markov) as the default strong null. It is strict enough to
kill syllable-pool artifacts and loose enough that genuine long-range design would
still stand out.

### Worked example: why reversal died

Dee received some Angelical backwards off the scrying stone, so "names and their
reverses co-occur" is a reasonable hypothesis. Measured co-occurrence of recurring
6-grams with their reverses: **102**.

- vs letter shuffle: 3.3 → looks like a massive 30-sigma signal.
- vs Markov-3 surrogate: 92.8 (sd 9.7), z ≈ 0.95 → **ordinary**.

The Loagaeth is full of AD-AX and AX-AD type syllables; reversing one lands you on
another that already exists, purely from the syllable inventory. The "mirror
structure" is what any text with this syllable pool produces. Verdict: refuted. An
independent check on the attested Enochian lexicon agrees (0 reverse pairs among the
~686 known word-forms).

This is the template for every test: **report observed, weak-null, and strong-null
side by side, and trust only the strong null.**

## Significance reporting

Where a null distribution is generated, we report its mean and standard deviation
and a z-score, not just a yes/no. A pattern is called real only when it clears
roughly mean + 3·sd of the strong null. Counts of exact matches (e.g. the Call
bridge) are compared to a same-length random-string null. We deliberately avoid
post-hoc target selection: thresholds (frequency ≥ 5, k = 6, etc.) are fixed in the
code, not tuned to produce a result.

## Descriptive vs inferential modules

- Modules 01, 03, 04, 05 are mostly **descriptive**: they report counts, ratios and
  paradigms that are true by inspection of the data. They characterize the text.
- Modules 06 and 08 are **inferential**: they pit an observation against a null and
  report a verdict.
- Module 02 is descriptive about the graph (hubs, degree, alpha); the question
  "is the hubbiness beyond chance" is left to the null-model machinery and to the
  reader's own extension, because the honest answer depends on which graph you build.

## Known limitations

1. **Segmentation.** The dense tables have no word boundaries. The morphology in
   module 04 is derived by scanning for stems and tabulating adjacent letters, which
   can cross a true boundary. It is a strong hypothesis, not a proof. A
   boundary-aware transcription would settle it.
2. **Transcription.** One source. Hubs should be re-checked against a second
   transcription of Sloane 3189.
3. **Power-law exponent.** The Hill alpha depends on the graph construction and
   xmin. We report it for transparency, not as a load-bearing claim; the robust
   statement is "heavy-tailed with a few dominant hubs."
4. **The numeric layer is not analyzed here.** The strongest unexplained signal in
   the wider corpus (digits 2/3/6 in the 91 governors' numbers) lives outside this
   package and is flagged as future work.
