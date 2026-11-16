# -*- coding: utf-8 -*-
"""
247 - Gematria (Golden Dawn / hebraico qabalístico) + elemento dos nomes top do Loagaeth.
Correspondência por letra de engine/data/gematria_enoquiana.json (valor hebraico GD
tradicional) + elemento pela triplicidade do signo. Descritivo/correspondência (plano
simbólico), não teste estatístico. stdlib only.
"""
import json, os
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# letra -> (nome Dee, hebraico, valor GD tradicional, signo/elem, ELEMENTO)
# valores GD tradicional (Áries=Heh=5, Aquário=Tzaddi=90); nós do dragão F/T = Gimel(3), marcado.
LET = {
 "A": ("Un",   "ו Vav",   6,   "Touro",          "Terra"),
 "B": ("Pa",   "ה Heh",   5,   "Áries",          "Fogo"),
 "C": ("Veh",  "ש Shin",  300, "Fogo",           "Fogo"),
 "D": ("Gal",  "ש Shin",  300, "Espírito",       "Espírito"),
 "E": ("Graph","י Yod",   10,  "Virgem",         "Terra"),
 "F": ("Or",   "ג Gimel*",3,   "Cauda Draconis", "Nodo"),
 "G": ("Ged",  "ט Teth",  9,   "Leão",           "Fogo"),
 "H": ("Na",   "א Aleph", 1,   "Ar",             "Ar"),
 "I": ("Gon",  "ס Samekh",60,  "Sagitário",      "Fogo"),
 "L": ("Ur",   "ח Cheth", 8,   "Câncer",         "Água"),
 "M": ("Tal",  "צ Tzaddi",90,  "Aquário",        "Ar"),
 "N": ("Drux", "נ Nun",   50,  "Escorpião",      "Água"),
 "O": ("Med",  "ל Lamed", 30,  "Libra",          "Ar"),
 "P": ("Mals", "ח Cheth", 8,   "Câncer",         "Água"),
 "Q": ("Ger",  "מ Mem",   40,  "Água",           "Água"),
 "R": ("Don",  "ק Qoph",  100, "Peixes",         "Água"),
 "S": ("Fam",  "ז Zayin", 7,   "Gêmeos",         "Ar"),
 "T": ("Gisg", "ג Gimel*",3,   "Caput Draconis", "Nodo"),
 "U": ("Van",  "ע Ayin",  70,  "Capricórnio",    "Terra"),
 "X": ("Pal",  "ת Tav",   400, "Terra",          "Terra"),
 "Z": ("Ceph", "ט Teth",  9,   "Leão",           "Fogo"),
}

TOP = ["NOCHA", "GETH", "CHASTOR", "ANZACH", "NOCHASTOR", "ADNOCHA", "NACHO",
       "ALGETH", "ACLAX", "DAXVAR", "CHIDNO", "HANZACH", "GETHACLAX", "GALETHOG", "LOAGAETH"]


def reduce9(n):
    while n > 9:
        n = sum(int(d) for d in str(n))
    return n


def analyze(name):
    total = 0; per = []; elems = Counter()
    for ch in name:
        if ch not in LET:
            continue
        nm, heb, val, signo, el = LET[ch]
        total += val; per.append((ch, heb, val, el)); elems[el] += 1
    dom = elems.most_common(1)[0] if elems else ("—", 0)
    return total, per, elems, dom


if __name__ == "__main__":
    print("TABELA DAS 21 LETRAS (gematria GD + elemento)")
    print("letra | nome Dee | hebraico | valor | signo/elem | ELEMENTO")
    for k, (nm, heb, val, signo, el) in LET.items():
        print("  %s | %-5s | %-8s | %4d | %-14s | %s" % (k, nm, heb, val, signo, el))
    print("\n(* F e T = Cauda/Caput Draconis, nós do dragão; sem letra hebraica GD padrão — usei Gimel=3)\n")

    out = {}
    print("NOMES TOP DO LOAGAETH — gematria e elemento")
    for name in TOP:
        total, per, elems, dom = analyze(name)
        letras = " + ".join("%s(%d)" % (c, v) for c, _, v, _ in per)
        elperfil = " ".join("%s:%d" % (e, n) for e, n in elems.most_common())
        print("\n%s = %s = %d (reduz %d)" % (name, letras, total, reduce9(total)))
        print("   elementos: %s  -> dominante %s" % (elperfil, dom[0]))
        out[name] = {"total": total, "reduzido": reduce9(total),
                     "letras": [{"letra": c, "hebraico": h, "valor": v, "elemento": e} for c, h, v, e in per],
                     "elementos": dict(elems), "dominante": dom[0]}
    with open(os.path.join(ROOT, "results", "247_gematria_nomes.json"), "w", encoding="utf-8") as f:
        json.dump({"tabela_letras": {k: {"nome": v[0], "hebraico": v[1], "valor": v[2], "signo": v[3], "elemento": v[4]} for k, v in LET.items()},
                   "nomes": out}, f, ensure_ascii=False, indent=1)
