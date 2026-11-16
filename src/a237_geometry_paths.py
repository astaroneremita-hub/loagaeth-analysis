# -*- coding: utf-8 -*-
"""
237 - Caminhos geométricos de leitura ainda não testados (pedido do usuário).

Quatro ordens de leitura que não estavam no log, mais um CONTROLE positivo (linha):
  - ROW (controle): leitura em linha — tem de disparar (nomes foram achados em linha).
  - ESPIRAL: espiral quadrada de fora para dentro.
  - CAVALO: tour do cavalo (Warnsdorff) — passos de cavalo, diferente do king-move.
  - TOROIDAL: diagonais que dão a volta (r, (r+k) mod 49) — leitura no toro.
  - HILBERT: curva de Hilbert (preenche o espaço preservando vizinhança local).

Cada ordem depende só de n=49 (não das letras), então é calculada UMA vez e reusada.
Lê as 42 faces densas 49x49 naquela ordem, conta nomes recorrentes, vs null (embaralhar
cada face). stdlib only, seed 1583.
"""
import random, statistics
import load

SEED = 1583
N = 49
NAMES = ["NOCHA", "ADNOCHA", "DNOCHA", "NACHO", "NOCHASTOR", "GETH", "ALGETH", "ACLAX",
         "ACLAXT", "CHASTOR", "ANZACH", "HANZACH", "DAXVAR", "CHIDNO", "GETHACLAX", "CHADAX"]


def faces():
    lv = load.leaves(); out = []
    for n in load.table_numbers():
        for side in ("a", "b"):
            key = f"{n}{side}"
            if key in lv:
                rows = [load.letters(r) for r in lv[key]]
                if len(rows) == N and all(len(r) == N for r in rows):
                    out.append([list(r) for r in rows])
    return out


def order_row():
    return [(r, c) for r in range(N) for c in range(N)]


def order_spiral():
    seen = [[False] * N for _ in range(N)]
    out = []
    top, bot, lft, rgt = 0, N - 1, 0, N - 1
    while top <= bot and lft <= rgt:
        for c in range(lft, rgt + 1): out.append((top, c))
        top += 1
        for r in range(top, bot + 1): out.append((r, rgt))
        rgt -= 1
        if top <= bot:
            for c in range(rgt, lft - 1, -1): out.append((bot, c))
            bot -= 1
        if lft <= rgt:
            for r in range(bot, top - 1, -1): out.append((r, lft))
            lft += 1
    return out


def order_knight():
    moves = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]
    def deg(r, c, vis):
        d = 0
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and not vis[nr][nc]: d += 1
        return d
    vis = [[False] * N for _ in range(N)]
    r, c = 0, 0; vis[r][c] = True; out = [(r, c)]
    for _ in range(N * N - 1):
        best, bc = None, 999
        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            if 0 <= nr < N and 0 <= nc < N and not vis[nr][nc]:
                d = deg(nr, nc, vis)
                if d < bc: bc, best = d, (nr, nc)
        if best is None: break
        r, c = best; vis[r][c] = True; out.append((r, c))
    return out  # pode ser parcial se travar


def order_toroidal():
    # 49 diagonais que dão a volta; retorna lista de segmentos (cada diagonal separada)
    segs = []
    for k in range(N):
        segs.append([(r, (r + k) % N) for r in range(N)])
    return segs


def _hilbert_d2xy(order, d):
    x = y = 0; t = d; s = 1
    while s < (1 << order):
        rx = 1 & (t // 2); ry = 1 & (t ^ rx)
        if ry == 0:
            if rx == 1:
                x = s - 1 - x; y = s - 1 - y
            x, y = y, x
        x += s * rx; y += s * ry; t //= 4; s <<= 1
    return x, y


def order_hilbert():
    out = []
    for d in range(1 << (2 * 6)):  # 64x64
        x, y = _hilbert_d2xy(6, d)
        if x < N and y < N: out.append((y, x))
    return out


def read_single(face, order):
    return "".join(face[r][c] for (r, c) in order)


def read_segmented(face, segs):
    return "|".join("".join(face[r][c] for (r, c) in seg) for seg in segs)


def count(text):
    return sum(text.count(nm) for nm in NAMES)


def shuffled(stack, rng):
    out = []
    for g in stack:
        flat = [x for row in g for x in row]; rng.shuffle(flat)
        out.append([flat[i * N:(i + 1) * N] for i in range(N)])
    return out


def z(real, nul):
    return round((real - statistics.mean(nul)) / (statistics.pstdev(nul) or 1e-9), 2)


def run():
    rng = random.Random(SEED)
    stack = faces()
    single_orders = {"ROW (controle)": order_row(), "ESPIRAL": order_spiral(),
                     "CAVALO": order_knight(), "HILBERT": order_hilbert()}
    toro = order_toroidal()

    def total_single(st, order):
        return count("|".join(read_single(f, order) for f in st))
    def total_toro(st):
        return count("|".join(read_segmented(f, toro) for f in st))

    nulls = [shuffled(stack, rng) for _ in range(12)]
    res = {"faces": len(stack), "knight_cells_covered": len(single_orders["CAVALO"]), "paths": {}}
    for name, order in single_orders.items():
        real = total_single(stack, order)
        nul = [total_single(s, order) for s in nulls]
        res["paths"][name] = {"real": real, "null_mean": round(statistics.mean(nul), 1), "z": z(real, nul)}
    real = total_toro(stack); nul = [total_toro(s) for s in nulls]
    res["paths"]["TOROIDAL"] = {"real": real, "null_mean": round(statistics.mean(nul), 1), "z": z(real, nul)}

    load.save_result("237_geometry_paths", res)
    return res


if __name__ == "__main__":
    r = run()
    print("faces:", r["faces"], "| cavalo cobriu", r["knight_cells_covered"], "de", N * N, "células")
    for k in ["ROW (controle)", "ESPIRAL", "CAVALO", "TOROIDAL", "HILBERT"]:
        p = r["paths"][k]
        print("  %-14s real %-4d vs null %-6s z %s" % (k, p["real"], p["null_mean"], p["z"]))
