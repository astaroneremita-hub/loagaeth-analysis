"""
a142 - Can we PREDICT the book's next pages of names? Train on early tables, test on later ones.

The goal: generate the book's own names and predict unseen pages. We order the 36 clean tables by position, train on
the first 70% and hold out the last 30% (the 'next pages'). Two honest questions:
  (A) RECURRENCE: how many names on the later pages ALREADY appeared on the earlier pages? Those are predictable by
      memory alone (the names recur across the book).
  (B) NOVEL PREDICTION: of the genuinely NEW names on the later pages (never seen in training), how many does the
      grammar G (learned from training) generate? That is the real 'predict the unseen' power, beyond recurrence.
Together they bound what 'predicting the next pages' can achieve.
"""
import json
import unicodedata
from collections import defaultdict

import load
from a22_robustness_and_depth import base_book

VOW = set("AEIOU")


def da(s):
    return "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn").upper()


def parse(w):
    return ("".join(c for c in w if c not in VOW),
            "".join(c for c in w if c in VOW),
            "".join("C" if c not in VOW else "V" for c in w))


def interleave(skel, mel, tmpl):
    out, si, mi = [], 0, 0
    for t in tmpl:
        if t == "C":
            if si >= len(skel):
                return None
            out.append(skel[si]); si += 1
        else:
            if mi >= len(mel):
                return None
            out.append(mel[mi]); mi += 1
    return "".join(out) if si == len(skel) and mi == len(mel) else None


def leaf_lines(g):
    R = 49
    o = [g[r] for r in range(R)]
    o += ["".join(g[r][c] for r in range(R)) for c in range(R)]
    for s in range(R):
        o.append("".join(g[s + k][k] for k in range(R - s)))
    return o


def run():
    book = base_book()
    order = [k for k in book if len([r for r in book[k] if r]) == 49
             and all(len("".join(r)) == 49 for r in book[k] if r)]
    order.sort(key=lambda k: (int("".join(c for c in k if c.isdigit())), k[-1]))
    names = [da(w) for w in json.load(open(load.ROOT + "/viz/name_field.json", encoding="utf-8"))]

    def names_in(k):
        g = ["".join(r) for r in book[k] if r]
        t = "\n".join(leaf_lines(g)); rt = t[::-1]
        return set(w for w in names if len(w) >= 4 and (w in t or w in rt))

    split = int(len(order) * 0.7)
    train_tabs, test_tabs = order[:split], order[split:]
    train_names = set()
    for k in train_tabs:
        train_names |= names_in(k)
    test_names = set()
    for k in test_tabs:
        test_names |= names_in(k)

    # (A) recurrence
    recur = test_names & train_names
    novel = test_names - train_names

    # (B) novel prediction: grammar from train generates which novel names?
    SK, ML, TM = set(), set(), set()
    for w in train_names:
        s, m, t = parse(w)
        SK.add(s); ML.add(m); TM.add(t)
    tmpl_by = defaultdict(list)
    for t in TM:
        tmpl_by[(t.count("C"), t.count("V"))].append(t)
    gen = set()
    for s in SK:
        for m in ML:
            for t in tmpl_by.get((len(s), len(m)), []):
                w = interleave(s, m, t)
                if w:
                    gen.add(w)
    novel_pred = novel & gen

    res = {
        "tables_total": len(order), "train_tables": len(train_tabs), "test_tables": len(test_tabs),
        "train_names": len(train_names), "test_names": len(test_names),
        "recur_predictable": len(recur), "recur_frac": round(len(recur) / len(test_names), 3) if test_names else 0,
        "novel": len(novel), "novel_generated_by_G": len(novel_pred),
        "novel_pred_frac": round(len(novel_pred) / len(novel), 3) if novel else 0,
        "total_predictable_frac": round((len(recur) + len(novel_pred)) / len(test_names), 3) if test_names else 0,
        "finding": (
            "Prevendo as páginas finais a partir das iniciais: das %d nomes nas páginas de teste, %d (%.0f%%) já "
            "tinham aparecido nas páginas de treino (previsíveis por recorrência). Dos %d genuinamente NOVOS, a "
            "gramática treinada gera %d (%.0f%%). TOTAL previsível: %.0f%% das páginas finais. O resto (%.0f%%) são "
            "nomes novos que a gramática não gerou - a parte não-determinada (a 'escolha' do livro)." % (
                len(test_names), len(recur), 100 * len(recur) / max(1, len(test_names)), len(novel),
                len(novel_pred), 100 * len(novel_pred) / max(1, len(novel)),
                100 * (len(recur) + len(novel_pred)) / max(1, len(test_names)),
                100 * (len(novel) - len(novel_pred)) / max(1, len(test_names)))),
    }
    load.save_result("142_predict_pages", res)
    return res


if __name__ == "__main__":
    r = run()
    print(r["finding"] + "\n")
    print("treino %d tabelas (%d nomes) -> teste %d tabelas (%d nomes)" % (
        r["train_tables"], r["train_names"], r["test_tables"], r["test_names"]))
    print("recorrência: %d (%.0f%%) | novos: %d, gerados por G: %d (%.0f%%)" % (
        r["recur_predictable"], r["recur_frac"] * 100, r["novel"], r["novel_generated_by_G"], r["novel_pred_frac"] * 100))
    print("TOTAL previsível das páginas finais: %.0f%%" % (r["total_predictable_frac"] * 100))
