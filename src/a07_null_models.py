"""
07 - Null models.

Two surrogate generators used to decide whether an observed pattern is real or an
artifact of the text's own texture:

  shuffle(s)            -> same letters, order destroyed (weak null; kills all
                           local structure, so it inflates the apparent signal of
                           anything syllable-driven).
  markov_surrogate(s,k) -> order-k Markov surrogate: reproduces the local syllable
                           texture while destroying any long-range / intentional
                           design. This is the STRONG null. A pattern that does not
                           beat the Markov surrogate is a by-product of local
                           letter statistics, not a hidden device.

Lesson baked into this project: a pattern that only beats shuffle but not Markov is
not a finding. Several candidate "discoveries" died exactly here.
"""
import random


def shuffle(s, rng):
    lst = list(s)
    rng.shuffle(lst)
    return "".join(lst)


def build_markov(s, k):
    table = {}
    for i in range(len(s) - k):
        table.setdefault(s[i:i + k], []).append(s[i + k])
    return table


def markov_surrogate(s, k, rng):
    table = build_markov(s, k)
    keys = list(table)
    cur = rng.choice(keys)
    out = list(cur)
    for _ in range(len(s) - k):
        nxt = table.get("".join(out[-k:]))
        if not nxt:
            cur = rng.choice(keys)
            out.extend(cur)
            continue
        out.append(rng.choice(nxt))
    return "".join(out[:len(s)])


def make_rng(seed=0):
    return random.Random(seed)


if __name__ == "__main__":
    import load
    r = make_rng(7)
    s = load.dense_stream()[:5000]
    print("orig   :", s[:60])
    print("shuffle:", shuffle(s, r)[:60])
    print("markov3:", markov_surrogate(s, 3, r)[:60])
