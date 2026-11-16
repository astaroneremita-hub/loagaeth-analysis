# -*- coding: utf-8 -*-
"""
246 - Fora da caixa: o Sigillum como CHAVE do Loagaeth (não como recipiente).

O selo (1582) veio ANTES do Livro (1583); o Loagaeth é selado, sem ordem de leitura.
Hipótese: os NÚMEROS do SDA dizem ONDE ler no Loagaeth.
  (A) índice direto: número n -> a n-ésima letra de uma folha (1 ou 2), em ordem do anel.
  (B) salto cumulativo: andar pelo fluxo do Loagaeth pulando os números do anel (a própria
      regra do selo aplicada ao Livro), lendo as letras onde cai.
  (C) coordenadas: números (acima/abaixo) como (linha/coluna) na grade 49x49 da folha.
Busca Loag-nomes / palavras das Chamadas no resultado, vs null (números embaralhados /
aleatórios). stdlib only, seed 1583.
"""
import json, os, random, statistics
import load

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SEED = 1583
LOAG = ["NOCHA", "GETH", "ALGETH", "CHASTOR", "ANZACH", "ACLAX", "NACHO", "DAXVAR", "CHIDNO",
        "ADNOCHA", "NACHO", "CHA", "NOC", "ETH", "LOAG", "LOAGAETH", "GALETHOG"]


def sda_numbers():
    with open(os.path.join(ROOT, "engine", "data", "sigillum.json"), encoding="utf-8") as f:
        sda = json.load(f)
    casas = sda["anel_externo_40"]["casas"]
    nums, above = [], []
    for c in casas:
        if c["numero"] is not None:
            nums.append(c["numero"]); above.append(c["posicao_numero"] == "acima")
    return nums, above


def score(s):
    return sum(s.count(nm) for nm in LOAG if len(nm) >= 4)


def direct_read(stream, nums):
    return "".join(stream[(n - 1) % len(stream)] for n in nums)


def jump_read(stream, nums, above, start=0):
    pos = start; out = []
    for n, up_ in zip(nums, above):
        pos = (pos + (n if up_ else -n)) % len(stream)
        out.append(stream[pos])
    return "".join(out)


def grid49(n):
    lv = load.leaves()
    for k in (f"{n}a", f"{n}b"):
        g = [load.letters(r) for r in lv.get(k, [])]
        if len(g) == 49 and all(len(r) == 49 for r in g):
            return g
    return None


def coord_read(grid, nums, above):
    # pares consecutivos (num_i, num_{i+1}) como (linha, coluna)
    out = []
    for i in range(0, len(nums) - 1, 2):
        r = (nums[i] - 1) % 49; c = (nums[i + 1] - 1) % 49
        out.append(grid[r][c])
    return "".join(out)


def run():
    rng = random.Random(SEED)
    nums, above = sda_numbers()
    f1 = load.table_text(1)
    f2 = load.table_text(2)
    book = load.dense_stream()
    g2 = grid49(2)

    def test(label, fn):
        real = fn(nums, above)
        sc = score(real)
        # null A: ordem embaralhada dos números
        na = []
        for _ in range(300):
            idx = list(range(len(nums))); rng.shuffle(idx)
            na.append(score(fn([nums[i] for i in idx], [above[i] for i in idx])))
        # null B: números aleatórios na mesma faixa
        nb = []
        mx = max(nums)
        for _ in range(300):
            na2 = [rng.randint(1, mx) for _ in nums]
            nb.append(score(fn(na2, above)))
        z_shuf = (sc - statistics.mean(na)) / (statistics.pstdev(na) or 1e-9)
        z_rand = (sc - statistics.mean(nb)) / (statistics.pstdev(nb) or 1e-9)
        return {"label": label, "string": real[:60], "score": sc,
                "null_shuffle_mean": round(statistics.mean(na), 2), "z_vs_shuffle": round(z_shuf, 2),
                "null_random_mean": round(statistics.mean(nb), 2), "z_vs_random": round(z_rand, 2)}

    results = []
    results.append(test("A_indice_direto_folha1", lambda nm, ab: direct_read(f1, nm)))
    results.append(test("A_indice_direto_folha2", lambda nm, ab: direct_read(f2, nm)))
    results.append(test("B_salto_cumulativo_folha2", lambda nm, ab: jump_read(f2, nm, ab)))
    results.append(test("B_salto_cumulativo_livro", lambda nm, ab: jump_read(book, nm, ab)))
    if g2:
        results.append(test("C_coordenadas_folha2", lambda nm, ab: coord_read(g2, nm, ab)))

    res = {"nums": nums, "results": results}
    with open(os.path.join(ROOT, "results", "246_sda_key.json"), "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    return res


if __name__ == "__main__":
    r = run()
    print("números do SDA (34):", r["nums"])
    print("\nmétodo                        score  z_vs_shuffle  z_vs_random   string")
    for d in r["results"]:
        flag = "  <== !!" if max(d["z_vs_shuffle"], d["z_vs_random"]) >= 3 else ""
        print("  %-28s %4d   %10s  %10s   %s%s" %
              (d["label"], d["score"], d["z_vs_shuffle"], d["z_vs_random"], d["string"], flag))
