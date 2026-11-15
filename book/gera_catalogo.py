# -*- coding: utf-8 -*-
"""Gera o catálogo numerado (book/<lang>/10-catalogo.md) a partir das entradas
## #NNN do docs/RESEARCH_LOG.md, localizando o veredito. Uso: python gera_catalogo.py [pt|en]"""
import os, re, sys

LANG = (sys.argv[1] if len(sys.argv) > 1 else "pt").lower()
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
LOG = os.path.join(ROOT, "docs", "RESEARCH_LOG.md")
OUT = os.path.join(HERE, LANG, "10-catalogo.md")

def verdict(text):
    t = text.upper()
    if "REFUT" in t: return ("REFUTADO", "R")
    if "CONFIRMADO NOVO" in t or "CONFIRMED" in t: return ("REAL", "V")
    if "REAL" in t and "REFUT" not in t: return ("REAL", "V")
    if "DESCRIPTIVE" in t or "DESCRIT" in t: return ("DESCRITIVO", "D")
    if "LEAD" in t: return ("LEAD", "L")
    return ("—", "")

# quebra o log em blocos por heading, guardando corpo p/ varredura de veredito
with open(LOG, encoding="utf-8") as f:
    text = f.read()
blocks = re.split(r"(?m)^(?=##\s+#\d+)", text)

def body_verdict(body):
    # procura linha de veredito explícita primeiro
    for ln in body.splitlines():
        u = ln.upper()
        if ("VEREDITO" in u or "VERDICT" in u) and verdict(ln)[0] != "—":
            return verdict(ln)[0]
    # senão, primeira ocorrência forte de token no corpo
    for tok, lab in [("REFUT", "REFUTADO"), ("CONFIRMADO NOVO", "REAL"),
                     ("DESCRIPTIVE", "DESCRITIVO"), ("DESCRIT", "DESCRITIVO")]:
        if tok in body.upper():
            return lab
    return "—"

rows = []
for blk in blocks:
    m = re.match(r"^##\s+#(\d+)\s*[—-]\s*(.+?)\s*$", blk.splitlines()[0] if blk.strip() else "")
    if not m:
        continue
    num = int(m.group(1))
    rest = m.group(2)
    v, _ = verdict(rest)
    if v == "—":
        v = body_verdict(blk)
    title = rest
    for sep in [" — ", " - "]:
        parts = rest.rsplit(sep, 1)
        if len(parts) == 2 and verdict(parts[1])[0] != "—" and len(parts[1]) < 60:
            title = parts[0]
            break
    title = title.replace("|", "/").strip()
    rows.append((num, title, v))

rows.sort(key=lambda r: r[0])

# contagem
from collections import Counter
cnt = Counter(v for _, _, v in rows)

# rótulo de veredito por idioma
DISP = {
    "pt": {"REAL": "REAL", "REFUTADO": "REFUTADO", "DESCRITIVO": "DESCRITIVO", "LEAD": "LEAD", "—": "—"},
    "en": {"REAL": "REAL", "REFUTADO": "REFUTED", "DESCRITIVO": "DESCRIPTIVE", "LEAD": "LEAD", "—": "—"},
}[LANG]

lines = []
if LANG == "pt":
    lines += [
        "# APARATO", "",
        "# Catálogo numerado dos achados", "",
        "Este catálogo lista, em ordem, as entradas do registro cronológico de "
        "pesquisa (`docs/RESEARCH_LOG.md`) desta fase do estudo. Cada entrada é "
        "um teste datado e reproduzível; os números **[#NNN]** citados ao longo "
        "do livro remetem a esta tabela e ao registro. Os títulos preservam o "
        "nome canônico do teste no registro (para rastreabilidade bit a bit); o "
        "**veredito** está localizado: **REAL** (superou o nulo), **REFUTADO** "
        "(caiu), **DESCRITIVO** (fato por construção/inspeção), **LEAD** (indício "
        "frágil, não confirmado), **—** (entrada de registro, sem veredito único).", "",
        f"**Balanço desta fase:** {cnt.get('REAL',0)} REAL · "
        f"{cnt.get('REFUTADO',0)} REFUTADO · {cnt.get('DESCRITIVO',0)} DESCRITIVO · "
        f"{cnt.get('LEAD',0)} LEAD · {cnt.get('—',0)} registro. "
        f"Total: {len(rows)} entradas (#{rows[0][0]}–#{rows[-1][0]}).", "",
        "| # | Teste | Veredito |", "|---:|---|:---|",
    ]
else:
    lines += [
        "# APPARATUS", "",
        "# Numbered catalog of findings", "",
        "This catalog lists, in order, the entries of the chronological research log "
        "(`docs/RESEARCH_LOG.md`) for this phase of the study. Each entry is a dated, "
        "reproducible test; the **[#NNN]** numbers cited throughout the book refer to "
        "this table and to the log. The titles preserve the test's canonical name in "
        "the log (for bit-by-bit traceability); the **verdict** is localized: **REAL** "
        "(beat the null), **REFUTED** (fell), **DESCRIPTIVE** (fact by "
        "construction/inspection), **LEAD** (fragile, unconfirmed), **—** (log entry, "
        "no single verdict).", "",
        f"**Balance of this phase:** {cnt.get('REAL',0)} REAL · "
        f"{cnt.get('REFUTADO',0)} REFUTED · {cnt.get('DESCRITIVO',0)} DESCRIPTIVE · "
        f"{cnt.get('LEAD',0)} LEAD · {cnt.get('—',0)} log. "
        f"Total: {len(rows)} entries (#{rows[0][0]}–#{rows[-1][0]}).", "",
        "| # | Test | Verdict |", "|---:|---|:---|",
    ]
for num, title, v in rows:
    lines.append(f"| {num} | {title} | {DISP[v]} |")
lines += ["", "\\newpage", ""]

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))

print(f"[{LANG}] catálogo: {len(rows)} entradas, #{rows[0][0]}–#{rows[-1][0]}", dict(cnt))
