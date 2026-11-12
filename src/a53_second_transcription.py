"""
53 - A second transcription on line: kondor.de. Independent witness, or a copy of the first?

The site kondor.de publishes the 96 sides of the book, one page each. If it were an independent
reading of the manuscript it would let us separate the text from the transcriber (the n/u problem,
which Dee himself complains of in Kelley's hand). Row by row, letters only, against the
transcription used in this study (Peterson):

  - share of rows that are identical, share of letters that agree in rows of equal length;
  - which letters differ (an independent reading of this hand must differ in n/u and z/x, the
    confusions measured on the Soyga tables in a36);
  - whether the two share accidents that no two readers would make alike: the points between
    words on the same sides only, and rows of irregular length in the same places.

Pages are fetched to data/raw/kondor/ and not redistributed.
"""
import html
import os
import re
import unicodedata
from collections import Counter

import load

DIR = os.path.join(load.DATA, "raw", "kondor")
URL = "https://www.kondor.de/enoch/loagaeth/%s.html"


def page(k):
    p = os.path.join(DIR, k + ".html")
    if not os.path.exists(p):
        import time
        import urllib.request
        os.makedirs(DIR, exist_ok=True)
        req = urllib.request.Request(URL % k, headers={"User-Agent": "Mozilla/5.0 (research script)"})
        with urllib.request.urlopen(req, timeout=40) as r, open(p, "wb") as fh:
            fh.write(r.read())
        time.sleep(0.3)
    return open(p, encoding="latin-1").read()


def rows_of(k):
    h = re.sub(r"(?s)<(script|style).*?</\1>", " ", page(k))
    t = html.unescape(re.sub(r"<br\s*/?>|</tr>|</p>|</div>", "\n", h))
    t = re.sub(r"<[^>]+>", "", t)
    out = {}
    for l in t.split("\n"):
        m = re.match(r"^(.*?[A-Za-z].*?)\s+(\d{1,2})\s*$", l.strip())
        if not m:
            continue
        body = unicodedata.normalize("NFD", m.group(1))
        L = re.sub(r"[^A-Z]", "", body.upper())
        if len(L) >= 1 and len(L) / max(1, len(re.sub(r"\s", "", body))) > 0.6:
            out.setdefault(int(m.group(2)), (L, "." in m.group(1)))
    return out


def run():
    lv = load.leaves()
    keys = [k for k in sorted(lv, key=lambda k: (int(k[:-1]), k)) if int(k[:-1]) >= 2]
    same_rows = rows = letters = agree = 0
    diff = Counter()
    per = {}
    pts_p, pts_k, irregular_both = set(), set(), 0
    irregular_p = 0
    missing = []
    for k in keys:
        K = rows_of(k)
        P = [load.letters(r) for r in lv[k]]
        if len(K) < 5:
            missing.append(k)
            continue
        s = n = 0
        for i, a in enumerate(P, 1):
            if not a or i not in K:
                continue
            b = K[i][0]
            rows += 1
            n += 1
            same_rows += a == b
            s += a == b
            if K[i][1]:
                pts_k.add(k)
            if len(a) not in (49,) and int(k[:-1]) <= 24:
                irregular_p += 1
                irregular_both += len(b) == len(a)
            if len(a) == len(b):
                letters += len(a)
                for x, y in zip(a, b):
                    if x == y:
                        agree += 1
                    else:
                        diff[tuple(sorted((x, y)))] += 1
        per[k] = round(s / max(1, n), 3)
    import a51_word_points
    pts_p = set(a51_word_points.parse())
    nd = sum(diff.values())
    res = {"sides_compared": len(per), "sides_not_parsed": missing, "rows_compared": rows,
           "rows_identical": same_rows, "share": round(same_rows / max(1, rows), 4),
           "letters_compared_in_rows_of_equal_length": letters, "letters_that_differ": nd,
           "letter_agreement": round(agree / max(1, letters), 5),
           "commonest_differences": [{"pair": a + "/" + b, "count": c} for (a, b), c in diff.most_common(12)],
           "n_u_differences": diff.get(("N", "U"), 0) + diff.get(("N", "V"), 0), "z_x_differences": diff.get(("X", "Z"), 0),
           "expected_n_u_if_independent_reading": "about 6.5% of the n's (a36): several hundred",
           "sides_with_word_points": {"peterson": sorted(pts_p), "kondor": sorted(pts_k)},
           "irregular_rows_in_tables_2_24": {"in_peterson": irregular_p, "same_length_in_kondor": irregular_both},
           "least_alike_sides": sorted(per.items(), key=lambda x: x[1])[:8]}
    load.save_result("53_second_transcription", res)
    return res


if __name__ == "__main__":
    for k, v in run().items():
        print(k, v)
