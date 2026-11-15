# -*- coding: utf-8 -*-
"""a226 - pronunciation table (Dee letter-names + phonetic) and the book's FUNCTION map by
element, plus the functional arc (new): does the book progress through the elements?

Writes viz/pronuncia.json. stdlib only.
"""
import os
import sys
import json
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "engine"))
import load

# Dee letter-names (for vibration) + phonetic hint
LETTERS = [
    ("A", "Un", "ah (longo, o tom)"), ("B", "Pa", "b"), ("C", "Veh", "k / s"),
    ("D", "Gal", "d"), ("E", "Graph", "é"), ("F", "Or", "f"), ("G", "Ged", "g (gutural)"),
    ("H", "Na", "h aspirado (sopro)"), ("I", "Gon", "i (ou y)"), ("L", "Ur", "l"),
    ("M", "Tal", "m"), ("N", "Drux", "n"), ("O", "Med", "ô (longo)"), ("P", "Mals", "p"),
    ("Q", "Ger", "k (qu)"), ("R", "Don", "r vibrado"), ("S", "Fam", "s"), ("T", "Gisg", "t"),
    ("U", "Van", "u / v"), ("X", "Pal", "ks"), ("Z", "Ceph", "z / ts"),
]

ELEM_FUNC = {
    "Ar": {"dominio": "Mente · Palavra · Conhecimento",
           "faz": "abre entendimento, comunicação, revelação; o trabalho do intelecto e da fala",
           "cor": "#5bb3e0"},
    "Agua": {"dominio": "Emoção · Intuição · Dissolução",
             "faz": "move o sentimento, a intuição, a cura; dissolve formas, leva ao profundo",
             "cor": "#3d6bd6"},
    "Fogo": {"dominio": "Vontade · Energia · Transformação",
             "faz": "acende a vontade, a força, a transmutação; queima e refina",
             "cor": "#e0573b"},
    "Terra": {"dominio": "Matéria · Corpo · Manifestação",
              "faz": "fixa, manifesta, estabiliza; o trabalho do corpo e do mundo concreto",
              "cor": "#c9a24b"},
}


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    # HONESTO: há dois sistemas GD que discordam (a90). Computo elemento por folha nos DOIS:
    #  - por SIGNO (triplicidade, a85)   - por PLANETA (regente, a90; Venus=Terra)
    import importlib
    a85 = importlib.import_module("a85_entity_attributes")
    LET = a85.load_letters()
    PLANET_EL = {"Sol": "Fogo", "Marte": "Fogo", "Jupiter": "Fogo", "Venus": "Terra",
                 "Saturno": "Terra", "Mercurio": "Ar", "Lua": "Agua"}

    def sign_el(L):
        i = LET.get(L, {})
        return a85.SIGN_ELEMENT.get(i.get("sign") or i.get("signo"))

    def planet_el(L):
        i = LET.get(L, {})
        return PLANET_EL.get(i.get("planet") or i.get("planeta"))

    def dom_el(rng, fn):
        c = Counter()
        for f in rng:
            for ch in load.table_text(f):
                e = fn(ch)
                if e in ELEM_FUNC:
                    c[e] += 1
        return (c.most_common(1)[0][0], dict(c)) if c else ("?", {})

    regions = [
        ("Abertura", range(1, 13), "a porta — entra-se pela folha 2 (Chamada 1)"),
        ("Corpo", range(13, 26), "o adensamento — o campo de nomes mais cheio"),
        ("Costura", range(26, 29), "o limiar — a leitura vira diagonal, maior desordem"),
        ("Descida", range(29, 41), "o aprofundamento"),
        ("Profundo", range(41, 49), "a dissolução — nomes somem, a vogal escurece (A→U)"),
    ]
    region_rows = []
    for name, rng, desc in regions:
        ds, cs = dom_el(rng, sign_el)
        dp, cp = dom_el(rng, planet_el)
        agree = ds == dp
        prim = ds  # usa signo como primário (= pilha), mas mostra planeta e o conflito
        region_rows.append({"regiao": name, "folhas": f"{rng.start}-{rng.stop-1}",
                            "elemento": prim, "elemento_signo": ds, "elemento_planeta": dp,
                            "concordam": agree, "desc": desc,
                            "dominio": ELEM_FUNC[prim]["dominio"], "faz": ELEM_FUNC[prim]["faz"]})
        flag = "CONCORDAM" if agree else f"CONFLITO (signo {ds} vs planeta {dp})"
        print(f"{name:10s} {rng.start}-{rng.stop-1}: signo={ds} planeta={dp}  [{flag}]", flush=True)

    arc = [dom_el(range(f, f+1), sign_el)[0] for f in load.table_numbers()]
    print("ARCO (por signo):", Counter(arc), flush=True)

    out = {"letters": [{"letra": a, "nome_dee": b, "som": c} for a, b, c in LETTERS],
           "elem_func": ELEM_FUNC,
           "regions": region_rows,
           "arc": arc,
           "chant_rules": {"tom": "A", "acento": "penúltima (latina)", "final": "vogal sustentada ou H (sopro)",
                           "vibracao": "soletre pelos nomes das letras (ex. NOCHA = Drux-Med-Veh-Na-Un)"}}
    with open(os.path.join(os.path.dirname(HERE), "viz", "pronuncia.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False)
    print("done", flush=True)


if __name__ == "__main__":
    main()
