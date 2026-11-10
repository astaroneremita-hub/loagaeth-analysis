# The recursive pattern engine

A self-feeding loop that searches for **real structure** in the Enochian Great
Table and the systems tied to it (Heptarchia, governors, Sigillum, Loagaeth),
separating genuine design from coincidence. One rule governs everything:

> **No pattern becomes a finding without passing a skeptical baseline (null model)**
> that says how often it would appear by pure chance. That is what keeps the search
> out of pareidolia.

This is the engine referred to in the main README as "the recursive system." It is
the real code, made standalone: it needs only its bundled `data/`, Python stdlib,
and nothing else. The evidence-corpus layer (a private library of books used to
cross-check confirmed findings) is **not shipped** — `Corpus` degrades to a no-op
when `engine/corpus/` is absent, and the engine runs fine without it.

## Run it

```bash
cd engine
python loop.py --rodadas 13     # one full sweep of the 13 gematria systems
python loop.py                  # run forever (self-feeding)
python loop.py --intervalo 20   # 20s pause between rounds
python loop.py --limiar 0.01    # p-value cutoff for CONFIRMADO
```

Output lands in `engine/results/`:
`achados.jsonl` (append-only findings) · `seen.json` (dedupe hashes) ·
`estado.json` (loop state) · `registro.md` (human-readable log).

Standalone sanity check of the data layer:

```bash
python nucleo.py     # prints: names in hierarchy, gematria systems, books (0 by default)
python enoch.py      # prints the derived Great-Table names
python fontes.py     # prints the 1584 tables and gematria systems
```

## Architecture

| file | role |
|---|---|
| `enoch.py` | Great Table (Golden Dawn): derives the hierarchy names by rule, straight-line search, and the shuffle **baseline**. Data: `data/quadrados.json`. |
| `fontes.py` | Dee's primary sources: the 1584/1587 tables, the 19 Calls, the 91 governors, the Sigillum, and the 13 gematria value systems. Data: `data/*.json`. |
| `nucleo.py` | shared layer: normalization, own gematria, empirical p-value / Spearman / Jensen-Shannon statistics, and the persistent **memory** (`Armazem`: jsonl + dedupe + state). Optional `Corpus` evidence search. |
| `sondas.py` | the **probe battery** (S1–S13), each with its own null model and a p-value verdict. |
| `loop.py` | the self-feeding runner: each round varies the technique/system, dedupes against memory, writes only what is NEW, and (if a corpus is present) cross-checks confirmed findings against the books. |

## The probes (lenses), each with its own null

- **S1 gematria** — pairs of names with the same value (non-trivial equivalences) in one system.
- **S2 gematria** — equivalence confirmed by **K+ systems at once** (a stronger clue).
- **S3 gematria** — a name's value landing on a **number cited in the Calls**.
- **S4 frequency** — whose letter-frequency the Towers resemble (Jensen-Shannon).
- **S5 geometry** — Heptarchy / governor / Sigillum names as **straight lines** in the Towers.
- **S6 symmetry** — palindromes and mirror pairs.
- **S7 numerology** — concentration of digital roots **3-6-9** (hardened null: shuffles letter→value, so it tests the NAMES, not the system's bias).
- **S8 metaphysics / kabbalah** — does each Tower prefer its own digital-root "sefirot"?
- **S9 governors** — does a governor's declared number of servants track its name's gematria (Spearman)?
- **S10 frequency** — k-grams shared between the Loagaeth and the Towers (hardened null: order-1 Markov pseudo-Loagaeth).
- **S11 geometry** — names hidden at regular skips (ELS / "Bible-code" style) — the null is everything here, because ELS finds anything in long text.
- **S13 gematria** — do equal-value pairs preferentially bridge DIFFERENT ranks of the hierarchy?

## Verdict and honesty

- `CONFIRMED` p ≤ 0.01 · `indication` p ≤ 0.05 · `coincidence` above that.
- `class`: **candidate** (a genuine clue if real) vs **known** (structure already
  expected or circular — e.g. governors are *derived from* the Tables, so finding
  them in the Tables is **not** a discovery).
- Every finding carries a `caveat`: a low p means the pattern is **real**
  (not chance), **not** that the symbolic *interpretation* is proven. Structural
  correlation is not hidden meaning.

## What the first sweeps actually produced

Run it yourself, but for orientation: most `CONFIRMED` results are `known`
(expected construction, e.g. governors as straight lines, letter-frequency kinship
with the governors — both circular because the governors come from the Tables). The
two candidate clues that resisted hardening:

1. **3-6-9 digital roots** concentrated in name values — but S7's hardened null shows
   this largely reflects the Golden Dawn value system, not the names. Downgraded.
2. **Per-Tower kabbalistic signature** (S8) — the separation turned out to come from
   the four Tables having different letter compositions (a known fact), and the modal
   roots do **not** match the traditional element numbers. Downgraded in the caveat.

The honest headline from the broader 72-hypothesis audit (see
`../docs/EXPERIMENTS_72_hypotheses.md`): **no hidden code appeared that the naked eye
could not already see.** What the engine does well is tell structure apart from
coincidence — including its own.
