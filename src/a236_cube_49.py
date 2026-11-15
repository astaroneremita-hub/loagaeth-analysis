# -*- coding: utf-8 -*-
"""
236 - The 49x49x49 cube, revisited and extended (sugestão de Rev. JBG).

a62 já testou o cubo básico (eixo de profundidade MI + nomes descendo z) e REFUTOU.
Aqui estendemos, para dar à hipótese o teste mais completo possível:
  - empilha TODAS as faces densas 49x49 (os DOIS lados a/b, não um só) na ordem do livro;
  - A) eixo z: informação mútua da mesma célula entre faces adjacentes;
  - B) nomes lidos DESCENDO as colunas de profundidade (r,c) na pilha;
  - C) nomes lidos ao longo das 4 DIAGONAIS ESPACIAIS do cubo (a leitura 3D real);
  - D) colunas de profundidade são mais ordenadas (entropia menor) que o acaso? (hipótese "lista/índice").
Nulo: embaralhar cada face (preserva a composição de cada página, testa só o arranjo espacial).
stdlib only, seed 1583.
"""
import math, random, statistics
from collections import Counter
import load

SEED = 1583
NAMES = ["NOCHA", "ADNOCHA", "DNOCHA", "NACHO", "GETH", "ALGETH", "ACLAX", "ACLAXT",
         "CHASTOR", "ANZACH", "HANZACH", "DAXVAR", "CHIDNO", "GETHACLAX"]


def faces():
    """Toda face densa 49x49 sem nulos, ambos os lados, na ordem do livro."""
    lv = load.leaves()
    out = []
    for n in load.table_numbers():
        for side in ("a", "b"):
            key = f"{n}{side}"
            if key not in lv:
                continue
            rows = [load.letters(r) for r in lv[key]]
            if len(rows) == 49 and all(len(r) == 49 for r in rows):
                out.append([list(r) for r in rows])
    return out


def shuffled(stack, rng):
    out = []
    for g in stack:
        flat = [x for row in g for x in row]
        rng.shuffle(flat)
        out.append([flat[i * 49:(i + 1) * 49] for i in range(49)])
    return out


def depth_mi(stack):
    c, a, b = Counter(), Counter(), Counter()
    for d in range(len(stack) - 1):
        for r in range(49):
            for col in range(49):
                x, y = stack[d][r][col], stack[d + 1][r][col]
                c[(x, y)] += 1; a[x] += 1; b[y] += 1
    n = sum(c.values())
    return sum(v / n * math.log2(v * n / (a[x] * b[y])) for (x, y), v in c.items())


def count_names(text):
    return sum(text.count(nm) for nm in NAMES)


def down_z(stack):
    D = len(stack)
    cols = ["".join(stack[d][r][c] for d in range(D)) for r in range(49) for c in range(49)]
    return "|".join(cols)


def diagonals_3d(stack):
    """Lê as 4 direções diagonais espaciais (dz=1, dy=±1, dx=±1); junta todas as linhas>=4."""
    D = len(stack)
    lines = []
    for dy in (1, -1):
        for dx in (1, -1):
            # cada linha começa numa borda de onde a direção aponta para dentro
            for r0 in range(49):
                for c0 in range(49):
                    # anda a partir de (0, r0, c0)
                    s = []
                    z, y, x = 0, r0, c0
                    while 0 <= z < D and 0 <= y < 49 and 0 <= x < 49:
                        s.append(stack[z][y][x]); z += 1; y += dy; x += dx
                    if len(s) >= 4:
                        lines.append("".join(s))
    return "|".join(lines)


def depth_col_entropy(stack):
    """Entropia média das colunas de profundidade (baixa = colunas repetitivas/ordenadas)."""
    D = len(stack)
    ents = []
    for r in range(49):
        for c in range(49):
            col = [stack[d][r][c] for d in range(D)]
            cnt = Counter(col); tot = len(col)
            ents.append(-sum(v / tot * math.log2(v / tot) for v in cnt.values()))
    return statistics.mean(ents)


def z(real, nul):
    return round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 2)


def run():
    rng = random.Random(SEED)
    stack = faces()
    D = len(stack)

    real_mi = depth_mi(stack)
    nul_mi = [depth_mi(shuffled(stack, rng)) for _ in range(12)]

    real_dz = count_names(down_z(stack))
    nul_dz = [count_names(down_z(shuffled(stack, rng))) for _ in range(12)]

    real_diag = count_names(diagonals_3d(stack))
    nul_diag = [count_names(diagonals_3d(shuffled(stack, rng))) for _ in range(12)]

    real_ent = depth_col_entropy(stack)
    nul_ent = [depth_col_entropy(shuffled(stack, rng)) for _ in range(12)]

    res = {
        "faces_in_cube": D,
        "A_depth_axis_MI": {"real_bits": round(real_mi, 4), "null_bits": round(statistics.mean(nul_mi), 4),
                            "z": z(real_mi, nul_mi)},
        "B_names_down_z": {"real": real_dz, "null_mean": round(statistics.mean(nul_dz), 1), "z": z(real_dz, nul_dz)},
        "C_names_on_3d_diagonals": {"real": real_diag, "null_mean": round(statistics.mean(nul_diag), 1),
                                    "z": z(real_diag, nul_diag)},
        "D_depth_col_entropy": {"real_bits": round(real_ent, 3), "null_bits": round(statistics.mean(nul_ent), 3),
                                "z": z(real_ent, nul_ent)},
    }
    load.save_result("236_cube_49", res)
    return res


if __name__ == "__main__":
    r = run()
    print("faces empilhadas no cubo:", r["faces_in_cube"])
    a = r["A_depth_axis_MI"]; print("A eixo-z MI: real %.4f vs nulo %.4f bits (z %.2f)" % (a["real_bits"], a["null_bits"], a["z"]))
    b = r["B_names_down_z"]; print("B nomes descendo z: %d vs nulo %.1f (z %.2f)" % (b["real"], b["null_mean"], b["z"]))
    c = r["C_names_on_3d_diagonals"]; print("C nomes nas diagonais 3D: %d vs nulo %.1f (z %.2f)" % (c["real"], c["null_mean"], c["z"]))
    d = r["D_depth_col_entropy"]; print("D entropia das colunas de profundidade: real %.3f vs nulo %.3f (z %.2f)" % (d["real_bits"], d["null_bits"], d["z"]))
