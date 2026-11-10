"""
Shared loader and helpers for the Loagaeth analysis.

Pure Python standard library only. No third-party dependencies.

Data model
----------
data/loagaeth_tables.json holds {"meta": {...}, "leaves": {"1a": [rows...], ...}}.
Each table number N has up to two sides, "Na" and "Nb". Leaves "1a"/"1b" are
word-spaced (the only ones with explicit word boundaries); every other side is a
dense 49x49 grid of 2401 letters. '?' marks a null/illegible cell.

Conventions used across all modules
-----------------------------------
- letters(s)     -> uppercase A-Z only, everything else stripped.
- table_text(N)  -> all letters of table N (both sides concatenated), dense stream.
- spaced_words() -> word tokens from the two word-spaced leaves (1a, 1b).
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DATA = os.path.join(ROOT, "data")
RESULTS = os.path.join(ROOT, "results")

_cache = {}


def _load_json(name):
    if name not in _cache:
        with open(os.path.join(DATA, name), encoding="utf-8") as f:
            _cache[name] = json.load(f)
    return _cache[name]


def leaves():
    """Raw {sideKey: [row strings]} mapping, e.g. '1a', '12b'."""
    return _load_json("loagaeth_tables.json")["leaves"]


def lexicon():
    """The attested-Call vocabulary bundle (known_glosses, attested_wordforms)."""
    return _load_json("call_lexicon.json")


def letters(s):
    """Uppercase A-Z only."""
    return re.sub(r"[^A-Z]", "", s.upper())


def table_numbers():
    """Sorted list of integer table numbers present in the data."""
    nums = set()
    for k in leaves():
        m = re.match(r"(\d+)[ab]?", k)
        if m:
            nums.add(int(m.group(1)))
    return sorted(nums)


def table_text(n):
    """All letters of table n (both sides), as one dense string."""
    out = []
    for side in ("a", "b"):
        key = f"{n}{side}"
        if key in leaves():
            for row in leaves()[key]:
                out.append(letters(row))
    return "".join(out)


def all_tables():
    """Dict {n: dense letter string} for every table."""
    return {n: table_text(n) for n in table_numbers()}


def dense_stream():
    """Every table concatenated in order: the whole book as one letter stream."""
    return "".join(table_text(n) for n in table_numbers())


def spaced_words(min_len=3):
    """Word tokens (>= min_len letters) from the two word-spaced leaves 1a, 1b."""
    words = []
    for key in ("1a", "1b"):
        for row in leaves().get(key, []):
            for tok in row.split():
                w = letters(tok)
                if len(w) >= min_len:
                    words.append(w)
    return words


def ngrams(s, k):
    """Iterator of length-k substrings of s."""
    return (s[i:i + k] for i in range(len(s) - k + 1))


def save_result(name, obj):
    """Write a result dict to results/<name>.json and return the path."""
    os.makedirs(RESULTS, exist_ok=True)
    path = os.path.join(RESULTS, name + ".json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=1)
    return path


if __name__ == "__main__":
    print("tables:", len(table_numbers()))
    print("total letters:", len(dense_stream()))
    print("spaced words (leaves 1a/1b):", len(spaced_words()))
