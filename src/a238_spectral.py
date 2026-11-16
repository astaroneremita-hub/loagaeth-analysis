# -*- coding: utf-8 -*-
"""
238 - Geometria espectral: autocorrelação espacial 2D das faces 49x49.

Pergunta (sugerida pelo usuário): existe organização espacial GLOBAL — frequências/
periodicidade/direção privilegiada — que não se vê lendo em sequência?

Medida encoding-free: taxa de autocorrelação A(dy,dx) = fração de pares de células
(y,x),(y+dy,x+dx) com a MESMA letra, média sobre a grade e sobre as 42 faces densas.
Varre as 4 direções (horizontal, vertical, diagonal↘, diagonal↗), lags 1..20, mais
alguns períodos (7,14) para caçar periodicidade.

Três controles (o ponto é separar estrutura 2D real de "só existem linhas"):
  C1 shuffle          — embaralha cada face (destrói tudo).
  C2 row-order        — mantém cada LINHA intacta, embaralha a ORDEM das linhas
                        (destrói alinhamento vertical/diagonal, preserva o horizontal).
  C3 markov3-por-linha— gera cada linha por Markov-3 do próprio livro (preserva fluxo local).
O veredito de "é 2D de verdade" é vertical/diagonal REAL > C2.
stdlib only, seed 1583.
"""
import random, statistics
from collections import defaultdict
import load

SEED = 1583
N = 49


def faces():
    lv = load.leaves(); out = []
    for n in load.table_numbers():
        for side in ("a", "b"):
            key = f"{n}{side}"
            if key in lv:
                rows = [load.letters(r) for r in lv[key]]
                if len(rows) == N and all(len(r) == N for r in rows):
                    out.append(rows)
    return out


def acorr(face, dy, dx):
    m = t = 0
    for y in range(N):
        yy = y + dy
        if yy < 0 or yy >= N:
            continue
        rowy = face[y]; rowyy = face[yy]
        for x in range(N):
            xx = x + dx
            if 0 <= xx < N:
                t += 1
                if rowy[x] == rowyy[xx]:
                    m += 1
    return m / t if t else 0.0


def mean_acorr(stack, dy, dx):
    return statistics.mean(acorr(f, dy, dx) for f in stack)


# ---- controls ----
def c1_shuffle(stack, rng):
    out = []
    for f in stack:
        flat = [c for row in f for c in row]; rng.shuffle(flat)
        out.append(["".join(flat[i * N:(i + 1) * N]) for i in range(N)])
    return out


def c2_rowshuffle(stack, rng):
    out = []
    for f in stack:
        rows = list(f); rng.shuffle(rows); out.append(rows)
    return out


def _markov3_rows(stack, rng):
    # modelo order-3 sobre todas as linhas reais
    trans = defaultdict(list); starts = []
    for f in stack:
        for row in f:
            starts.append(row[:3])
            for i in range(len(row) - 3):
                trans[row[i:i + 3]].append(row[i + 3])
    def gen_row():
        s = list(rng.choice(starts))
        while len(s) < N:
            nxt = trans.get("".join(s[-3:]))
            s.append(rng.choice(nxt) if nxt else rng.choice("AEIOU"))
        return "".join(s[:N])
    return [[gen_row() for _ in range(N)] for _ in stack]


def zpair(real, nul):
    return round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 2)


def run():
    rng = random.Random(SEED)
    stack = faces()
    DIRS = {"horizontal": (0, 1), "vertical": (1, 0), "diag_desc": (1, 1), "diag_asc": (1, -1)}

    NREP = 5
    c1 = [c1_shuffle(stack, rng) for _ in range(NREP)]
    c2 = [c2_rowshuffle(stack, rng) for _ in range(NREP)]
    c3 = [_markov3_rows(stack, rng) for _ in range(NREP)]

    def dir_curve(dname):
        dy0, dx0 = DIRS[dname]
        lags = list(range(1, 21)) + [14] if dname in ("horizontal", "vertical") else list(range(1, 21))
        out = {}
        for k in range(1, 21):
            dy, dx = dy0 * k, dx0 * k
            real = mean_acorr(stack, dy, dx)
            n1 = [mean_acorr(s, dy, dx) for s in c1]
            n2 = [mean_acorr(s, dy, dx) for s in c2]
            n3 = [mean_acorr(s, dy, dx) for s in c3]
            out[k] = {"real": round(real, 4), "c1_shuffle": round(statistics.mean(n1), 4),
                      "c2_rowshuf": round(statistics.mean(n2), 4), "c3_markov3": round(statistics.mean(n3), 4),
                      "z_vs_c1": zpair(real, n1), "z_vs_c2": zpair(real, n2), "z_vs_c3": zpair(real, n3)}
        return out

    res = {"faces": len(stack), "dirs": {}}
    for d in DIRS:
        res["dirs"][d] = dir_curve(d)

    # resumo: periodicidade = maior |z_vs_c2| para lag>2 em cada direção
    summ = {}
    for d in DIRS:
        best_k, best_z = None, 0.0
        for k in range(3, 21):
            zc2 = res["dirs"][d][k]["z_vs_c2"]
            if abs(zc2) > abs(best_z):
                best_z, best_k = zc2, k
        summ[d] = {"lag1_z_vs_c2": res["dirs"][d][1]["z_vs_c2"],
                   "lag1_z_vs_c3": res["dirs"][d][1]["z_vs_c3"],
                   "best_periodic_lag(>2)": best_k, "best_periodic_z_vs_c2": best_z}
    res["summary"] = summ
    load.save_result("238_spectral", res)
    return res


if __name__ == "__main__":
    r = run()
    print("faces:", r["faces"])
    for d, s in r["summary"].items():
        print("  %-10s lag1: z_vs_rowshuf %7s  z_vs_markov3 %7s | pico periódico lag>2: lag %s z_vs_rowshuf %s"
              % (d, s["lag1_z_vs_c2"], s["lag1_z_vs_c3"], s["best_periodic_lag(>2)"], s["best_periodic_z_vs_c2"]))
    print("\n  (lag1 = vizinho imediato; z_vs_rowshuf alto em vertical/diag = alinhamento 2D real além das linhas)")
    v = r["dirs"]["vertical"]
    print("  vertical real por lag:", {k: v[k]["real"] for k in [1,2,3,7,14]})
    h = r["dirs"]["horizontal"]
    print("  horizontal real por lag:", {k: h[k]["real"] for k in [1,2,3,7,14]})
