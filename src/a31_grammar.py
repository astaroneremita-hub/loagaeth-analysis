"""
31 - Track E of the roadmap: the machine side - a small generative grammar of the book.

  E1) A two-level code: a line is a sequence of names (from the lexicon found in a23/a28 plus the
      known stems) and single letters (from a 3-letter-context model). Trained on the even tables,
      scored on the odd ones (bits per letter, best parse). Compared with letter models of order 3
      and 4 trained on the same tables. The lexicon's own cost (MDL) is reported too. If the grammar
      codes the text in fewer bits, the names are a real "code" of the text, beyond letter habits.
  E2) Drift: one grammar per data-driven part (a27) vs one grammar for the whole book.
"""
import json
import math
import os
from collections import Counter

import load
from a19_machine import CharLM
from a22_robustness_and_depth import base_book, tnum

KNOWN = ["CHASTOR", "CHUSTOR", "NOCHASTOR", "ANZACH", "GETH", "ALGETH", "NOCHA", "ADNOCHA", "ACLAX",
         "OXAD", "CHADAX", "CHAPH"]
PARTS = {"I": range(2, 13), "II": range(13, 26), "III": range(26, 34), "IV": range(34, 41), "V": range(41, 49)}


def lexicon():
    names = list(KNOWN)
    for f, key in (("23_name_discovery.json", None), ("28_names_deep.json", "B5")):
        p = os.path.join(load.RESULTS, f)
        if not os.path.exists(p):
            continue
        d = json.load(open(p, encoding="utf-8"))
        if key is None:
            names += [c["name"] for c in d["A_candidates"]["top"]]
        else:
            names += [x[0] for x in d["B5_hidden_names"]["not_seen_before"]]
    return sorted({n for n in names if len(n) >= 4}, key=len, reverse=True)


class Grammar:
    def __init__(self, lex, order=3):
        self.lex = lex
        self.order = order

    def parse(self, line):
        toks, i = [], 0
        while i < len(line):
            for w in self.lex:
                if line.startswith(w, i):
                    toks.append(w)
                    i += len(w)
                    break
            else:
                toks.append(line[i])
                i += 1
        return toks

    def fit(self, lines):
        self.char = CharLM(self.order).fit(lines)
        tc = Counter()
        for l in lines:
            tc.update(t for t in self.parse(l) if len(t) > 1)
        nl = sum(len(l) for l in lines)
        nn = sum(tc.values())
        letters = nl - sum(len(w) * c for w, c in tc.items())
        self.lam = nn / (nn + letters)
        tot = sum(tc.values())
        V = len(self.lex)
        self.pw = {w: (tc[w] + 0.5) / (tot + 0.5 * V) for w in self.lex}
        self.used = sum(1 for w in self.lex if tc[w])
        return self

    def bits_line(self, line):
        n = len(line)
        dp = [math.inf] * (n + 1)
        dp[0] = 0.0
        lnl = -math.log2(1 - self.lam)
        pad = "^" * self.order
        s = pad + line
        for i in range(n):
            if dp[i] == math.inf:
                continue
            c = dp[i] + lnl - math.log2(self.char.prob(s[i:i + self.order], line[i]))
            if c < dp[i + 1]:
                dp[i + 1] = c
            for w in self.lex:
                if line.startswith(w, i):
                    v = dp[i] - math.log2(self.lam * self.pw[w])
                    if v < dp[i + len(w)]:
                        dp[i + len(w)] = v
        return dp[n]

    def bits(self, lines):
        return sum(self.bits_line(l) for l in lines) / sum(len(l) for l in lines)


def split(book, rg=None):
    tr, te = [], []
    for k, v in book.items():
        t = tnum(k)
        if rg is not None and t not in rg:
            continue
        (tr if t % 2 == 0 else te).extend(v)
    return tr, te


def run():
    book = base_book()
    lex = lexicon()
    tr, te = split(book)
    N = sum(len(l) for l in te)
    g = Grammar(lex).fit(tr)
    gb = g.bits(te)
    c3 = CharLM(3).fit(tr).bits(te)
    c4 = CharLM(4).fit(tr).bits(te)
    lex_bits = sum(len(w) + 1 for w in lex) * math.log2(22)
    E1 = {"lexicon_names": len(lex), "names_used_in_training": g.used, "share_of_tokens_that_are_names": round(g.lam, 3),
          "test_letters": N,
          "grammar_bits_per_letter": round(gb, 4), "letter_model_order3": round(c3, 4),
          "letter_model_order4": round(c4, 4),
          "lexicon_cost_bits": round(lex_bits), "grammar_incl_lexicon_per_letter": round(gb + lex_bits / N, 4),
          "saving_vs_order3_percent": round((c3 - gb) / c3 * 100, 2)}
    # E2 drift: per-part grammars vs the one book grammar, on each part's test tables
    per = {}
    tot_book = tot_part = tot_n = 0
    for p, rg in PARTS.items():
        trp, tep = split(book, rg)
        n = sum(len(l) for l in tep)
        if not trp or not tep:
            continue
        gp = Grammar(lex).fit(trp)
        bb, bp = g.bits(tep), gp.bits(tep)
        per[p] = {"test_letters": n, "book_grammar": round(bb, 3), "own_part_grammar": round(bp, 3)}
        tot_book += bb * n
        tot_part += bp * n
        tot_n += n
    E2 = {"by_part": per, "book_grammar_mean": round(tot_book / tot_n, 4),
          "part_grammars_mean": round(tot_part / tot_n, 4)}
    res = {"E1_grammar_vs_letters": E1, "E2_one_or_five_grammars": E2,
           "note": "Best-parse code length (an upper bound for the grammar); training = even tables, test = odd tables."}
    load.save_result("31_grammar", res)
    return res


if __name__ == "__main__":
    print(json.dumps(run(), ensure_ascii=False, indent=1))
