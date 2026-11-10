# -*- coding: utf-8 -*-
"""LOOP - the self-feeding runner. Each round runs the probe battery varying the technique
(gematria system, set, parameter K...), classifies by p-value against the baseline, dedupes
against memory (seen) and writes only what is NEW. For CONFIRMED findings, it cross-checks the
optional book corpus.

Run:   python loop.py                   (forever, no pause between rounds)
       python loop.py --rodadas 13       (one full sweep of the 13 systems)
       python loop.py --intervalo 20      (20s pause between rounds)
       python loop.py --limiar 0.01        (p-value cutoff for CONFIRMED)
Output: results/achados.jsonl . seen.json . estado.json . registro.md

LLM self-improvement (optional): see llm_agent.py and the engine README. With an API key set,
the agent reads the findings and proposes new hypotheses to add to the schedule.
"""
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import nucleo as N          # noqa: E402
import sondas as S          # noqa: E402


# ----------------------------------------------------------------- shared context
class Ctx:
    def __init__(self):
        self.nh = N.nomes_hierarquia()
        self.G = N.Gematria()
        self.urna = N.alfabeto_torres()
        self.grades_dee = N.grades_dee()
        self.grades_gd = N.grades_gd()
        self.corpus = N.Corpus()
        self.corpora_freq = self._corpora_freq()
        self.conjuntos = self._conjuntos()

    def _corpora_freq(self):
        f = N.fontes
        hept = self._hept()
        govs = "".join(N.norm(g["nome"]) for g in f.governors()["governadores"])
        calls = "".join(N.norm(p.get("enoquiano", "")) for c in f.calls() for p in c.get("palavras", []))
        loa = self._loagaeth()
        return {k: v for k, v in {"Heptarchy": "".join(hept), "Governors": govs,
                                  "Calls": calls, "Loagaeth": loa}.items() if v}

    def _conjuntos(self):
        return {"heptarquia": self._hept(),
                "governadores": [N.norm(g["nome"]) for g in N.fontes.governors()["governadores"]],
                "sigillum": self._sigillum()}

    def _hept(self):
        try:
            H = N.json.load(open(os.path.join(N.ROOT, "data", "heptarquia.json"), encoding="utf-8"))
            return [N.norm(x["tabula_collecta"]) for x in H.get("nomes_derivados_das_tabelas", []) if x.get("tabula_collecta")]
        except Exception:
            return []

    def _sigillum(self):
        try:
            cells = N.fontes.sigillum()["tabela_7x7"]["celulas"]
            M = [[N.norm(cells[r][c]["letra"]) or "?" for c in range(7)] for r in range(7)]
            return ["".join(r) for r in M] + ["".join(M[r][c] for r in range(7)) for c in range(7)]
        except Exception:
            return []

    def _loagaeth(self):
        try:
            L = N.json.load(open(os.path.join(N.ROOT, "data", "loagaeth_grades_simples.json"), encoding="utf-8"))
            return "".join(N.norm(r if isinstance(r, str) else "".join(x or "" for x in r))
                           for s, rr in L.items() if not s.startswith("_") and isinstance(rr, list) for r in rr)
        except Exception:
            return ""


# ----------------------------------------------------------------- schedule (varies each round)
def plano(ctx, rodada):
    ids = ctx.G.ids
    nid = len(ids)
    return [
        (S.s1_gematria_equivalencias, {"sid": ids[rodada % nid]}),
        (S.s2_gematria_consenso, {"K": [2, 3, 4][rodada % 3]}),
        (S.s3_valor_x_chamadas, {"sid": ids[(rodada * 2) % nid]}),
        (S.s4_parentesco_frequencia, {}),
        (S.s5_geometria_conjuntos, {"conjunto": ["heptarquia", "governadores", "sigillum"][rodada % 3]}),
        (S.s6_simetria_palindromos, {}),
        (S.s7_numeros_369, {"sid": ids[(rodada * 3) % nid]}),
        (S.s8_cabala_sefira, {"sid": ids[(rodada * 5) % nid]}),
        (S.s9_governadores_servos, {"sid": ids[(rodada * 7) % nid]}),
        (S.s10_kgramas_loagaeth, {"L": [4, 5, 6][rodada % 3]}),
        (S.s11_saltos_els, {"saltos": [(2, 3, 4, 5), (2, 3), (3, 5, 7), (6, 7, 8)][rodada % 4]}),
        (S.s13_gematria_entre_classes, {"sid": ids[(rodada * 11) % nid]}),
    ]


def anexar_evidencia(ctx, ach):
    ev = []
    for term in ach.get("evidence_terms", [])[:2]:
        for h in ctx.corpus.buscar(term, limite=2):
            ev.append({"term": term, **h})
        if len(ev) >= 3:
            break
    return ev[:3]


def registrar_md(ach):
    cam = os.path.join(N.ACHADOS, "registro.md")
    novo = not os.path.exists(cam)
    with open(cam, "a", encoding="utf-8") as fp:
        if novo:
            fp.write("# Findings log - Enochian pattern engine\n\n")
        st = ach["stat"]
        fp.write(f"## [{ach['verdict']}] {ach['title']}\n")
        fp.write(f"- probe `{ach['probe']}` . lens *{ach['lens']}* . round {ach['round']}\n")
        fp.write(f"- {ach['technique']}\n")
        fp.write(f"- obs={st['obs']} chance={st['chance']} z={st['z']} **p={st['p']}**\n")
        if ach.get("evidence"):
            for e in ach["evidence"]:
                fp.write(f"  - book *{e['book']}* (`{e['term']}`): ...{e['excerpt']}...\n")
        fp.write("\n")


def rodar(rodadas=0, intervalo=0.0, limiar=0.01, verbose=True):
    ctx = Ctx()
    arm = N.Armazem()
    est = arm.estado()
    r0 = est.get("round", 0)
    r = 0
    if verbose:
        print(f"engine started . {len(ctx.nh)} names . {len(ctx.G.ids)} systems . {len(ctx.corpus.arquivos)} books", flush=True)
    while rodadas == 0 or r < rodadas:
        rodada = r0 + r + 1
        rng = N.random.Random(1584 + rodada)
        new = 0
        by_verdict = {"CONFIRMED": 0, "indication": 0, "coincidence": 0}
        for func, params in plano(ctx, rodada):
            est.update({"round": rodada, "running": True, "probe": func.__name__,
                        "ts": time.strftime("%Y-%m-%d %H:%M:%S")})
            arm.salvar_estado({**est, "total": len(arm.seen), "new_last": new})
            try:
                out = func(ctx, params, rng) or []
            except Exception as ex:
                if verbose:
                    print(f"  ! {func.__name__}: {ex}", flush=True)
                continue
            for ach in out:
                ach["id"] = arm.chave(ach["probe"], ach["canonical"])
                ach["round"] = rodada
                ach["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
                by_verdict[ach["verdict"]] = by_verdict.get(ach["verdict"], 0) + 1
                if arm.ja_visto(ach["id"]):
                    continue
                if ach["verdict"] == "CONFIRMED":
                    ach["evidence"] = anexar_evidencia(ctx, ach)
                if arm.registrar(ach):
                    new += 1
                    registrar_md(ach)
                    if verbose and ach["verdict"] in ("CONFIRMED", "indication"):
                        tag = "CONFIRMED NEW" if ach["verdict"] == "CONFIRMED" else "indication new"
                        print(f"  >> {tag}: {ach['title']} (p={ach['stat']['p']})", flush=True)
        est.update({"round": rodada, "running": False, "probe": None,
                    "total": len(arm.seen), "new_last": new,
                    "ts": time.strftime("%Y-%m-%d %H:%M:%S"), "limiar": limiar,
                    "by_verdict": by_verdict})
        arm.salvar_estado(est)
        if verbose:
            print(f"round {rodada} . new {new} . total {len(arm.seen)} . {by_verdict}", flush=True)
        r += 1
        if intervalo and (rodadas == 0 or r < rodadas):
            time.sleep(intervalo)
    est["running"] = False
    arm.salvar_estado(est)
    return est


if __name__ == "__main__":
    a = sys.argv[1:]

    def opt(nome, dflt, tipo):
        if nome in a:
            return tipo(a[a.index(nome) + 1])
        return dflt
    sys.stdout.reconfigure(encoding="utf-8")
    rodar(rodadas=opt("--rodadas", 0, int),
          intervalo=opt("--intervalo", 0.0, float),
          limiar=opt("--limiar", 0.01, float))
