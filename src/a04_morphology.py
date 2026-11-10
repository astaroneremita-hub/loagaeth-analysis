"""
04 - Productive morphology: affixes on a small set of stems.

Reproducible from the raw stream without any external segmentation. For each stem
we scan every occurrence in the dense stream and tabulate the letters immediately
BEFORE (candidate prefix) and AFTER (candidate suffix). A stem that takes a small,
repeating inventory of prefixes/suffixes is behaving like a word root.

We also count, as substrings, a hand-built list of CHASTOR-family forms, to show
the paradigm concretely.

Caveat: before/after letters in a dense grid can cross a true word boundary. Treat
this as a strong hypothesis of word-formation, not proof. Cross-check needs a
boundary-aware transcription.
"""
from collections import Counter

import load

STEMS = ["CHAST", "CHA", "GETH", "DAX", "DRAX", "ZAD", "LAX"]
PRE_LEN = 2
SUF_LEN = 2

FAMILY = ["CHASTOR", "NOCHASTOR", "NECHASTOR", "NACHASTOR", "ZICHASTOR",
          "ZUCHASTOR", "UOLCHASTOR", "PLICHASTOR", "PRICHASTOR", "UOCASTOR",
          "NOCHASTER", "NOCHASTORA", "NOCHASTORAD", "CHUSTOR"]


def affixes_for(stem, s):
    pre, suf = Counter(), Counter()
    start = 0
    while True:
        i = s.find(stem, start)
        if i < 0:
            break
        if i >= PRE_LEN:
            pre[s[i - PRE_LEN:i]] += 1
        j = i + len(stem)
        if j + SUF_LEN <= len(s):
            suf[s[j:j + SUF_LEN]] += 1
        start = i + 1
    return pre, suf


def run():
    s = load.dense_stream()
    stems = {}
    for stem in STEMS:
        pre, suf = affixes_for(stem, s)
        stems[stem] = {
            "occurrences": s.count(stem),
            "top_prefixes": pre.most_common(8),
            "top_suffixes": suf.most_common(8),
        }

    family = {}
    for form in FAMILY:
        c = sum(t.count(form) for t in load.all_tables().values())
        if c:
            family[form] = c

    res = {
        "stems": stems,
        "chastor_family_counts": dict(sorted(family.items(),
                                             key=lambda kv: kv[1], reverse=True)),
        "note": "A closed inventory of prefixes (NO-, NE-, NA-, ZI-, ZU-, UOL-, AD-, "
                "AL-, OR-) recurs across several stems; the CHASTOR paradigm is the "
                "clearest case.",
    }
    load.save_result("04_morphology", res)
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=1))
