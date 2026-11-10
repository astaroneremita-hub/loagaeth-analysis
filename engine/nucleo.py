# -*- coding: utf-8 -*-
"""CORE of the pattern engine - shared layer of data, gematria, corpus and memory.

Reuses the audited primary infrastructure:
  - enoch.py      Great-Table derivations (hierarchy names, search, baseline)
  - fontes.py     Calls, governors, Sigillum, Heptarchia, tables, 13 gematria systems
  - corpus/*.txt  (OPTIONAL) extracted books as independent evidence (RAG) to cross-check
                  findings. Not shipped; if engine/corpus/ is absent, Corpus is a no-op.

Everything here is deterministic. The method is SKEPTICAL by construction: no pattern
becomes a finding without a baseline (null model) saying how often it would occur by
pure chance - that is what separates real structure from pareidolia.
"""
import hashlib
import json
import math
import os
import random
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = HERE
sys.path.insert(0, HERE)
import enoch   # noqa: E402
import fontes  # noqa: E402

ACHADOS = os.path.join(HERE, "results")
os.makedirs(ACHADOS, exist_ok=True)
TEXTO = os.path.join(HERE, "corpus")  # optional evidence corpus; absent by default -> Corpus is a no-op


# --------------------------------------------------------------------- text / normalization
def norm(s):
    """Uppercase A-Z, no accents; usual Enochian transliteration Y/J->I, V/W->U, K->C."""
    s = "".join(c for c in unicodedata.normalize("NFD", (s or "").upper()) if "A" <= c <= "Z")
    return s.translate(str.maketrans("YJVWK", "IIUUC"))


def raiz_digital(n):
    """Digital root 1-9 (0 only if n==0)."""
    if n == 0:
        return 0
    return 1 + (int(n) - 1) % 9


# --------------------------------------------------------------------- hierarchy names
def nomes_hierarquia():
    """List of dicts {name, kind, tower, sub?} - every name derived by the GD rule, with the
    normalized form in .norm and the letter multiset in .ms (to find non-trivial equivalences)."""
    out = []
    seen = set()
    for d in enoch.derive_names():
        nm = norm(d["name"])
        if not nm:
            continue
        key = (nm, d["kind"], d.get("tower"), d.get("sub"))
        if key in seen:
            continue
        seen.add(key)
        e = dict(d)
        e["norm"] = nm
        e["ms"] = "".join(sorted(nm))      # anagram signature (rotations collapse here)
        out.append(e)
    return out


def grades_dee():
    return {el: [[norm(x) or "?" for x in r] for r in g] for el, g in fontes.dee_1584().items()}


def grades_gd():
    return {el: [[norm(x) or "?" for x in r] for r in enoch.GRID[el]] for el in enoch.TOWERS}


# --------------------------------------------------------------------- own Enochian gematria
class Gematria:
    """Enochian gematria over the 13 value systems. Only sums names the system fully covers
    (a missing letter => name 'not covered', never a false value)."""

    def __init__(self):
        self.sist = fontes.gematria_value_tables()      # id -> {LETTER: value}
        self.ids = list(self.sist)

    def cobre(self, sid, nm):
        tab = self.sist[sid]
        return all(c in tab for c in nm)

    def valor(self, sid, nm):
        tab = self.sist[sid]
        if not all(c in tab for c in nm):
            return None
        return int(sum(tab[c] for c in nm))


# --------------------------------------------------------------------- corpus / evidence (light RAG, optional)
class Corpus:
    """Literal search over the extracted books (if present in engine/corpus/). Used to cross a
    structural finding with independent textual evidence. Absent by default -> empty, no-op."""

    def __init__(self):
        self.arquivos = sorted(f for f in os.listdir(TEXTO) if f.endswith(".txt")) if os.path.isdir(TEXTO) else []
        self._cache = {}

    def _texto(self, f):
        if f not in self._cache:
            try:
                self._cache[f] = open(os.path.join(TEXTO, f), encoding="utf-8", errors="ignore").read()
            except OSError:
                self._cache[f] = ""
        return self._cache[f]

    def buscar(self, termo, limite=6, janela=90):
        """Occurrences of `termo` (case-insensitive) with a short context excerpt."""
        if not termo or len(termo) < 3:
            return []
        rx = re.compile(re.escape(termo), re.IGNORECASE)
        hits = []
        for f in self.arquivos:
            for m in rx.finditer(self._texto(f)):
                a, b = max(0, m.start() - janela), m.end() + janela
                excerpt = re.sub(r"\s+", " ", self._texto(f)[a:b]).strip()
                hits.append({"book": f[:-4], "excerpt": excerpt})
                if len(hits) >= limite:
                    return hits
        return hits


# --------------------------------------------------------------------- statistics (baseline)
def p_empirico(obs, sims, cauda="maior"):
    """Empirical p-value of `obs` against the null distribution `sims`.
    cauda (tail): 'maior' (greater), 'menor' (lesser), 'dois' (two-sided)."""
    n = len(sims)
    if cauda == "maior":
        c = sum(1 for x in sims if x >= obs)
    elif cauda == "menor":
        c = sum(1 for x in sims if x <= obs)
    else:
        c = sum(1 for x in sims if abs(x) >= abs(obs))
    mean = sum(sims) / n if n else 0.0
    sd = (sum((x - mean) ** 2 for x in sims) / n) ** 0.5 if n else 0.0
    return {"obs": obs, "chance": round(mean, 3), "sd": round(sd, 3),
            "z": round((obs - mean) / sd, 2) if sd else None, "p": round((1 + c) / (1 + n), 4)}


def spearman(a, b):
    def rank(v):
        o = sorted(range(len(v)), key=lambda i: v[i])
        r = [0] * len(v)
        for k, i in enumerate(o):
            r[i] = k
        return r
    ra, rb = rank(a), rank(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    num = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    den = math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
    return num / den if den else 0.0


def js_div(p, q):
    keys = set(p) | set(q)
    m = {k: (p.get(k, 0) + q.get(k, 0)) / 2 for k in keys}
    kl = lambda a: sum(a.get(k, 0) * math.log2(a.get(k, 0) / m[k]) for k in keys if a.get(k, 0) > 0)
    return (kl(p) + kl(q)) / 2


def dist_letras(txt):
    c = Counter(ch for ch in txt if "A" <= ch <= "Z")
    n = sum(c.values()) or 1
    return {k: v / n for k, v in c.items()}


def alfabeto_torres():
    """Letter frequency of the 4 Towers (Dee 1584) - the 'urn' for realistic null names."""
    letras = [x for g in grades_dee().values() for r in g for x in r if x != "?"]
    return letras


# --------------------------------------------------------------------- verdict
def veredito(p, limiar=0.01):
    if p <= limiar:
        return "CONFIRMED"
    if p <= 0.05:
        return "indication"
    return "coincidence"


# --------------------------------------------------------------------- memory / findings store
class Armazem:
    """Persistent memory: achados.jsonl (append-only) + seen.json (hashes already seen) + estado.json.
    Ensures the same finding is not recounted round after round (dedupe by canonical key)."""

    def __init__(self):
        self.f_jsonl = os.path.join(ACHADOS, "achados.jsonl")
        self.f_seen = os.path.join(ACHADOS, "seen.json")
        self.f_estado = os.path.join(ACHADOS, "estado.json")
        self.seen = set(json.load(open(self.f_seen, encoding="utf-8"))) if os.path.exists(self.f_seen) else set()

    @staticmethod
    def chave(probe, canonical):
        return hashlib.sha1((probe + "|" + canonical).encode("utf-8")).hexdigest()[:16]

    def ja_visto(self, h):
        return h in self.seen

    def registrar(self, finding):
        """Store a new finding. Returns True if new, False if already in memory."""
        h = finding["id"]
        if h in self.seen:
            return False
        self.seen.add(h)
        with open(self.f_jsonl, "a", encoding="utf-8") as fp:
            fp.write(json.dumps(finding, ensure_ascii=False) + "\n")
        json.dump(sorted(self.seen), open(self.f_seen, "w", encoding="utf-8"))
        return True

    def todos(self):
        if not os.path.exists(self.f_jsonl):
            return []
        return [json.loads(l) for l in open(self.f_jsonl, encoding="utf-8") if l.strip()]

    def estado(self):
        if os.path.exists(self.f_estado):
            return json.load(open(self.f_estado, encoding="utf-8"))
        return {"round": 0, "total": 0, "new_last": 0, "running": False, "ts": None, "probe": None}

    def salvar_estado(self, est):
        json.dump(est, open(self.f_estado, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    g = Gematria()
    nh = nomes_hierarquia()
    c = Corpus()
    print("hierarchy names:", len(nh), "| gematria systems:", len(g.ids), "| books:", len(c.arquivos))
