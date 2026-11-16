# -*- coding: utf-8 -*-
"""
240 - O Sigillum Dei Aemeth esconde LOAGAETH? (pedido/desafio do usuário)

Usa engine/data/sigillum.json (SDA completo: anel de 40 casas, tabela 7x7 central,
tabela dos cestos 7x7, os 7 ângulos GALETHOG, os nomes do anel, as 4 famílias).

Busca honesta, em todos os caminhos de leitura, por:
  (A) LOAGAETH exato + variantes (reverso, folding u/v i/j, ω->O/W, <=1 edição);
  (B) distância de anagrama entre os NOMES reais do SDA e LOAGAETH (o GALETHOG dos
      ângulos é quase-anagrama: {A,E,G,H,L,O,T}, difere num A<->G);
  (C) nomes-família do Loagaeth (GETH/ALGETH/NOCHA/CHASTOR...) dentro do SDA.
Null: embaralhar o multiconjunto de letras do SDA e repetir a busca; e nomes aleatórios
da distribuição de letras do SDA para (B). stdlib only, seed 1583.
"""
import json, os, random, statistics
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583


def up(s):
    return "".join(ch for ch in s.upper() if ch.isalpha())


def load_sda():
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        return json.load(f)


def build(sda):
    # anel (40 casas; 'og' = 2 letras; ω -> O)
    ring = ""
    for c in sda["anel_externo_40"]["casas"]:
        ltr = c["letra"].replace("ω", "O")
        ring += up(ltr)
    # tabela central 7x7 (base letters; null -> '.')
    cel = sda["tabela_7x7"]["celulas"]
    grid_c = [["".join(ch for ch in (cell["letra"] or ".") if ch.isalpha() or ch == ".") or "."
               for cell in row] for row in cel]
    # tabela dos cestos 7x7
    bask = sda["tabela_dos_cestos_49"]["linhas"]
    grid_b = [[up(x) if x != "+" else "." for x in row["letras"]] for row in bask]
    # ângulos (a leitura é uma frase; o nome é o 1º token)
    angle = up(sda["angulos_7"]["leitura"].split()[0])  # GALETHOG
    # nomes do anel
    ring_names = [up(n.replace("ω", "O")) for n in sda["anel_externo_40"]["regra_de_leitura_declarada"]["ordem_final_dos_nomes"]]
    # anjos, nomes de deus, famílias
    angels = [up(a["leitura_da_tabela"]) for a in sda["anjos_7"]["anjos"]]
    gods = [up("".join(ch for ch in r["com_anotacoes"] if ch.isalpha())) for r in sda["nomes_de_deus_7"]["nomes"]]
    fams = []
    for fam in sda["familias_4"].values():
        for nm in fam["nomes"]:
            fams.append(up(nm["nome"]))
    return dict(ring=ring, grid_c=grid_c, grid_b=grid_b, angle=angle,
                ring_names=ring_names, angels=angels, gods=gods, fams=fams)


def grid_streams(g):
    n = len(g); m = len(g[0])
    out = []
    out += ["".join(g[r][c] for c in range(m)) for r in range(n)]          # rows
    out += ["".join(g[r][c] for r in range(n)) for c in range(m)]          # cols
    # diagonais ↘ e ↗ (todas)
    for s in range(-(n - 1), m):
        d = "".join(g[r][r - s] for r in range(n) if 0 <= r - s < m)
        if len(d) >= 2: out.append(d)
    for s in range(0, n + m - 1):
        d = "".join(g[r][s - r] for r in range(n) if 0 <= s - r < m)
        if len(d) >= 2: out.append(d)
    return out


def all_streams(S):
    streams = [S["ring"], S["angle"], "".join(S["ring_names"]),
               "".join(S["angels"]), "".join(S["gods"]), "".join(S["fams"])]
    streams += grid_streams(S["grid_c"])
    streams += grid_streams(S["grid_b"])
    # inclui reversos
    streams += [s[::-1] for s in streams]
    return [s for s in streams if s]


def fold(s):
    return s.replace("U", "V").replace("J", "I").replace("W", "O").replace("Y", "I")


def edits_le1(a, b):
    if a == b: return True
    if abs(len(a) - len(b)) > 1: return False
    # substituição
    if len(a) == len(b):
        return sum(x != y for x, y in zip(a, b)) == 1
    # inserção/remoção
    short, long = (a, b) if len(a) < len(b) else (b, a)
    for i in range(len(long)):
        if short == long[:i] + long[i + 1:]:
            return True
    return False


def find_target(streams, target):
    T = target; hits = []
    for s in streams:
        sf = fold(s)
        for i in range(len(sf) - len(T) + 1):
            w = sf[i:i + len(T)]
            if w == T:
                hits.append((w, "exato"))
            elif edits_le1(w, T):
                hits.append((w, "<=1 edit"))
    return hits


def multiset_dist(a, b):
    ca, cb = Counter(a), Counter(b)
    return sum((ca - cb).values()) + sum((cb - ca).values())


def run():
    rng = random.Random(SEED)
    sda = load_sda()
    S = build(sda)
    streams = all_streams(S)
    allletters = "".join(streams[:len(streams) // 2])  # sem duplicar reversos
    target = "LOAGAETH"; tf = fold(target)

    # (A) busca direta
    real_hits = find_target(streams, tf)
    real_exact = sum(1 for _, k in real_hits if k == "exato")
    real_near = sum(1 for _, k in real_hits if k != "exato")

    # null: embaralha o multiconjunto, mesma quantidade de streams/tamanhos
    sizes = [len(s) for s in streams[:len(streams) // 2]]
    pool = list(allletters)
    def null_once():
        rng.shuffle(pool)
        ss = []; i = 0
        for z in sizes:
            ss.append("".join(pool[i:i + z])); i += z
        ss += [s[::-1] for s in ss]
        h = find_target(ss, tf)
        return sum(1 for _, k in h if k == "exato"), sum(1 for _, k in h if k != "exato")
    nn = [null_once() for _ in range(300)]
    null_exact = [a for a, b in nn]; null_near = [b for a, b in nn]

    # (B) anagrama: distância dos nomes reais do SDA a LOAGAETH
    sda_names = S["ring_names"] + [S["angle"]] + S["angels"] + S["gods"] + S["fams"]
    dists = sorted(((multiset_dist(fold(nm), tf), nm) for nm in set(sda_names) if len(nm) == 8))
    near_anagrams = [(d, nm) for d, nm in dists if d <= 2]
    # null do anagrama: nomes de 8 letras aleatórios da distribuição do SDA
    letter_pool = list(fold(allletters))
    def rand_name():
        return "".join(rng.choice(letter_pool) for _ in range(8))
    nnames = 1000
    null_dists = [multiset_dist(rand_name(), tf) for _ in range(nnames)]
    frac_null_le1 = round(sum(1 for d in null_dists if d <= 1) / nnames, 4)
    frac_null_le2 = round(sum(1 for d in null_dists if d <= 2) / nnames, 4)

    # (C) nomes-família do Loag no SDA
    loag_fams = ["GETH", "ALGETH", "GETHOG", "GALETH", "NOCHA", "CHASTOR", "ANZACH", "ACLAX", "DAXVAR", "LOAG"]
    fam_hits = {}
    joined = "|".join(streams)
    for nm in loag_fams:
        c = joined.count(fold(nm))
        if c: fam_hits[nm] = c

    res = {
        "A_LOAGAETH_search": {
            "real_exact": real_exact, "real_near(<=1edit)": real_near,
            "null_exact_mean": round(statistics.mean(null_exact), 3),
            "null_near_mean": round(statistics.mean(null_near), 3),
            "null_exact_max": max(null_exact), "null_near_max": max(null_near),
            "p_exact": round(sum(1 for a in null_exact if a >= max(real_exact, 1)) / len(null_exact), 4) if real_exact else None,
        },
        "B_anagram_to_LOAGAETH": {
            "GALETHOG_distance": multiset_dist(fold(S["angle"]), tf),
            "nearest_sda_names(<=2)": [{"dist": d, "name": nm} for d, nm in near_anagrams],
            "null_frac_8letter_names_dist<=1": frac_null_le1,
            "null_frac_dist<=2": frac_null_le2,
        },
        "C_loag_families_in_sda": fam_hits,
        "counts": {"streams": len(streams), "sda_letters": len(allletters)},
    }
    # salva em results/
    os.makedirs(os.path.join(ROOT, "results"), exist_ok=True)
    with open(os.path.join(ROOT, "results", "240_sigillum.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = run()
    a = r["A_LOAGAETH_search"]
    print("=== (A) LOAGAETH em todos os caminhos do SDA ===")
    print("  exato real %d (null média %.2f, máx %d) | near<=1edit real %d (null média %.2f, máx %d)"
          % (a["real_exact"], a["null_exact_mean"], a["null_exact_max"], a["real_near(<=1edit)"], a["null_near_mean"], a["null_near_max"]))
    b = r["B_anagram_to_LOAGAETH"]
    print("=== (B) anagrama para LOAGAETH ===")
    print("  GALETHOG distância = %d (0=anagrama perfeito; 1=difere 1 letra)" % b["GALETHOG_distance"])
    print("  nomes do SDA mais perto:", b["nearest_sda_names(<=2)"])
    print("  null: %% de nomes-8 aleatórios com dist<=1 = %s ; dist<=2 = %s" % (b["null_frac_8letter_names_dist<=1"], b["null_frac_dist<=2"]))
    print("=== (C) famílias do Loag dentro do SDA ===", r["C_loag_families_in_sda"])
    print("streams:", r["counts"]["streams"], "| letras SDA:", r["counts"]["sda_letters"])
