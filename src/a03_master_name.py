"""
03 - The master stem CHASTOR and its coverage.

Counts occurrences (as substrings of the dense stream) of the master stem and its
main vowel variant, per table, and reports how much of the book each one touches.

Finding: CHASTOR is the dominant recurring name; NOCHASTOR is its main prefixed
form; CHUSTOR is an A->U vowel variant that tends to appear in the tables that
lack CHASTOR. "Coverage" = number of tables containing the form at least once.
"""
from collections import Counter

import load

FORMS = ["CHASTOR", "NOCHASTOR", "NOCHASTORAD", "CHUSTOR", "NOCHUSTOR"]


def run():
    tables = load.all_tables()
    ntab = len(tables)
    rows = {}
    for form in FORMS:
        total = 0
        tabs_with = 0
        for n, s in tables.items():
            c = s.count(form)
            total += c
            if c:
                tabs_with += 1
        rows[form] = {"occurrences": total, "tables": tabs_with,
                      "coverage_pct": round(100 * tabs_with / ntab, 1)}

    # tables with neither CHASTOR nor NOCHASTOR, and whether CHUSTOR fills them
    no_chastor = [n for n, s in tables.items()
                  if "CHASTOR" not in s]
    chustor_fills = [n for n in no_chastor if "CHUSTOR" in tables[n]]

    res = {
        "n_tables": ntab,
        "forms": rows,
        "tables_without_CHASTOR": sorted(no_chastor),
        "of_those_with_CHUSTOR": sorted(chustor_fills),
        "note": "CHASTOR+NOCHASTOR jointly touch the large majority of tables; "
                "CHUSTOR tends to occupy the CHASTOR-free ones.",
    }
    load.save_result("03_master_name", res)
    return res


if __name__ == "__main__":
    import json
    print(json.dumps(run(), ensure_ascii=False, indent=1))
