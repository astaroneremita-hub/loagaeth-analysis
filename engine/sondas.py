# -*- coding: utf-8 -*-
"""PROBE BATTERY - each pattern-search technique, ALWAYS with a skeptical baseline.

Golden rule: no probe returns a finding without a null model saying how much of the
effect would be expected by chance. The probe classifies the verdict by p-value
(CONFIRMED <=0.01, indication <=0.05, otherwise coincidence). The loop only announces
the CONFIRMED and NEW ones.

Each probe(ctx, params, rng) -> list of findings (partial dict; the loop fills in
id/round/ts/evidence). Function names keep an sN_ prefix for the loop's schedule.
"""
from collections import defaultdict

import nucleo as N


# ----------------------------------------------------------------- null-model utilities
def urna_nomes(rng, lengths, urn):
    """Random names with the same lengths, drawing letters from the Towers' urn."""
    return ["".join(rng.choice(urn) for _ in range(c)) for c in lengths]


def pares_valor_iguais(valores_por_ms):
    """valores_por_ms: dict multiset->value. Counts pairs of DISTINCT multisets with equal value."""
    byval = defaultdict(list)
    for ms, v in valores_por_ms.items():
        byval[v].append(ms)
    return sum(len(g) * (len(g) - 1) // 2 for g in byval.values() if len(g) > 1), byval


# ================================================================= S1 gematria: equivalences
def s1_gematria_equivalencias(ctx, params, rng):
    sid = params["sid"]
    trials = params.get("trials", 400)
    reps = {}
    tow = {}
    for e in ctx.nh:
        if ctx.G.cobre(sid, e["norm"]):
            v = ctx.G.valor(sid, e["norm"])
            reps[e["ms"]] = v
            tow.setdefault(e["ms"], set()).add(e["tower"])
    if len(reps) < 8:
        return []
    obs, byval = pares_valor_iguais(reps)
    comp = [len(ms) for ms in reps]
    sims = []
    for _ in range(trials):
        rn = urna_nomes(rng, comp, ctx.urna)
        vm = {}
        for nm in rn:
            if ctx.G.cobre(sid, nm):
                vm["".join(sorted(nm)) + str(rng.random())] = ctx.G.valor(sid, nm)
        sims.append(pares_valor_iguais(vm)[0])
    stat = N.p_empirico(obs, sims)
    groups = []
    for v, mss in sorted(byval.items(), key=lambda kv: -len(kv[1])):
        if len(mss) > 1:
            towers = {t for ms in mss for t in tow.get(ms, ())}
            if len(towers) >= 2:
                groups.append({"value": v, "names": sorted(mss)[:6], "towers": sorted(towers)})
        if len(groups) >= 5:
            break
    return [{
        "probe": "s1_gematria_equivalencias", "lens": "gematria",
        "title": f"Gematria equivalences in system {sid}",
        "technique": f"Pairs of names (distinct multisets) with equal value in system '{sid}', vs random names of the same shape (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"system": sid, "names_covered": len(reps), "equal_value_groups": groups},
        "canonical": f"s1:{sid}",
        "class": "candidate",
        "caveat": "A gematria equivalence is not forced by construction; surviving chance makes it a genuine clue. Check whether the equal names carry related meaning.",
        "evidence_terms": ["gematria", "numeric value", sid.split("__")[0].replace("_", " ")],
    }]


# ================================================================= S2 gematria: multi-system consensus
def s2_gematria_consenso(ctx, params, rng):
    K = params.get("K", 3)
    trials = params.get("trials", 300)
    names = [(e["ms"], e["norm"], e["tower"]) for e in ctx.nh]
    mss = {}
    for ms, nm, tw in names:
        mss.setdefault(ms, (nm, set()))[1].add(tw)
    reps = list(mss.items())

    def consensus(valfun):
        vals = {}
        for ms, (nm, _) in reps:
            vals[ms] = [valfun(sid, nm) for sid in ctx.G.ids]
        keys = list(vals)
        c = 0
        examples = []
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = vals[keys[i]], vals[keys[j]]
                k = sum(1 for x, y in zip(a, b) if x is not None and x == y)
                if k >= K:
                    c += 1
                    if len(examples) < 6:
                        examples.append({"names": [mss[keys[i]][0], mss[keys[j]][0]], "systems_equal": k})
        return c, examples

    obs, examples = consensus(lambda sid, nm: ctx.G.valor(sid, nm))
    comp = [len(ms) for ms, _ in reps]
    sims = []
    for _ in range(trials):
        rn = urna_nomes(rng, comp, ctx.urna)
        vals = [[ctx.G.valor(sid, nm) for sid in ctx.G.ids] for nm in rn]
        c = 0
        for i in range(len(vals)):
            for j in range(i + 1, len(vals)):
                if sum(1 for x, y in zip(vals[i], vals[j]) if x is not None and x == y) >= K:
                    c += 1
        sims.append(c)
    stat = N.p_empirico(obs, sims)
    return [{
        "probe": "s2_gematria_consenso", "lens": "gematria",
        "title": f"Equivalences confirmed by {K}+ gematria systems at once",
        "technique": f"Pairs of names with equal value in at least {K} of the 13 systems simultaneously, vs random (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"K": K, "examples": examples},
        "canonical": f"s2:K{K}",
        "class": "candidate",
        "caveat": "Equal value across several independent systems at once is harder to explain by chance - a stronger clue than S1.",
        "evidence_terms": ["gematria", "same value", "equivalence"],
    }]


# ================================================================= S3 value vs Call numbers
def s3_valor_x_chamadas(ctx, params, rng):
    sid = params.get("sid", "golden_dawn_coluna__F08")
    trials = params.get("trials", 400)
    nums = set()
    for item in (fontes_call_numbers() or []):
        for v in item.values() if isinstance(item, dict) else []:
            if isinstance(v, int):
                nums.add(v)
    if not nums:
        return []
    covered = [(e["ms"], ctx.G.valor(sid, e["norm"])) for e in ctx.nh if ctx.G.cobre(sid, e["norm"])]
    reps = {ms: v for ms, v in covered}
    obs = sum(1 for v in reps.values() if v in nums)
    comp = [len(ms) for ms in reps]
    sims = []
    for _ in range(trials):
        rn = urna_nomes(rng, comp, ctx.urna)
        sims.append(sum(1 for nm in rn if ctx.G.cobre(sid, nm) and ctx.G.valor(sid, nm) in nums))
    stat = N.p_empirico(obs, sims)
    cases = sorted({v for v in reps.values() if v in nums})[:12]
    return [{
        "probe": "s3_valor_x_chamadas", "lens": "gematria",
        "title": "Name values that land exactly on numbers cited in the Calls",
        "technique": f"Names whose value ({sid}) matches a cardinal number Dee cites in the 19 Calls, vs random (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"system": sid, "call_numbers": sorted(nums)[:20], "coincident_values": cases},
        "canonical": f"s3:{sid}",
        "class": "candidate",
        "caveat": "Call numbers and name values come from different systems; coincidence above chance would be a real bridge between them.",
        "evidence_terms": ["number", "Call", "key"],
    }]


def fontes_call_numbers():
    try:
        return N.fontes.call_numbers()
    except Exception:
        return []


# ================================================================= S4 frequency kinship (JS)
def s4_parentesco_frequencia(ctx, params, rng):
    trials = params.get("trials", 200)
    D84 = ctx.grades_dee
    towers_txt = "".join(x for g in D84.values() for r in g for x in r if x != "?")
    source_txt = ctx.corpora_freq
    dt = N.dist_letras(towers_txt)
    distances = {k: round(N.js_div(dt, N.dist_letras(v)), 4) for k, v in source_txt.items()}
    if not distances:
        return []
    kin = min(distances, key=distances.get)
    import string
    sims = []
    nchars = len(towers_txt)
    for _ in range(trials):
        rt = "".join(rng.choice(string.ascii_uppercase) for _ in range(min(nchars, 400)))
        sims.append(N.js_div(dt, N.dist_letras(rt)))
    stat = N.p_empirico(distances[kin], sims, cauda="menor")
    return [{
        "probe": "s4_parentesco_frequencia", "lens": "frequency",
        "title": f"The Towers' letter-print is kin to: {kin}",
        "technique": f"Jensen-Shannon distance between the Towers' letter frequency and each Enochian corpus; null = random text (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"closest_kin": kin, "distances": distances},
        "canonical": "s4:kinship",
        "class": "known" if kin == "Governors" else "candidate",
        "caveat": ("Governors are extracted from the Tables themselves in GD tradition - kinship is expected, not a mystery." if kin == "Governors"
                   else f"Letter-print kinship with {kin} (a separate system) would hint at common origin."),
        "evidence_terms": [kin, "frequency", "letters"],
    }]


# ================================================================= S5 geometry: sets as straight lines
def s5_geometria_conjuntos(ctx, params, rng):
    conj = params["conjunto"]  # 'heptarquia' | 'governadores' | 'sigillum'
    trials = params.get("trials", 300)
    words = ctx.conjuntos.get(conj, [])
    words = [p for p in words if len(p) >= 4]
    if len(words) < 5:
        return []
    grids = list(ctx.grades_dee.values())
    obs, mean, sd, p = N.enoch.baseline(words, grids, trials=trials, seed=rng.randint(1, 10 ** 6))
    stat = {"obs": obs, "chance": round(mean, 3), "sd": round(sd, 3),
            "z": round((obs - mean) / sd, 2) if sd else None, "p": round(p, 4)}
    lines = []
    for w in words:
        hits = [(el, N.enoch.search(g, w)) for el, g in ctx.grades_dee.items()]
        for el, hh in hits:
            if hh:
                lines.append({"name": w, "tower": el, "occurrences": len(hh)})
    return [{
        "probe": "s5_geometria_conjuntos", "lens": "geometry",
        "title": f"Names of '{conj}' appear as straight lines in the Towers",
        "technique": f"How many {conj} names occur as a straight line (8 directions) in the 4 Towers, vs shuffled grids (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"set": conj, "n_words": len(words), "lines_found": lines[:12]},
        "canonical": f"s5:{conj}",
        "class": "known" if conj == "governadores" else "candidate",
        "caveat": ("Governors are derived from the Tables by rule - finding them there is expected, not a new finding." if conj == "governadores"
                   else f"'{conj}' is a separate system from the Great Table; appearing as a straight line in it above chance would be a genuine link."),
        "evidence_terms": [conj, "Great Table", "hidden"],
    }]


# ================================================================= S6 symmetry: palindromes
def s6_simetria_palindromos(ctx, params, rng):
    trials = params.get("trials", 500)
    names = {e["norm"] for e in ctx.nh if len(e["norm"]) >= 3}
    obs = sum(1 for nm in names if nm == nm[::-1])
    comp = [len(nm) for nm in names]
    sims = []
    for _ in range(trials):
        rn = urna_nomes(rng, comp, ctx.urna)
        sims.append(sum(1 for nm in rn if nm == nm[::-1]))
    stat = N.p_empirico(obs, sims)
    pal = sorted(nm for nm in names if nm == nm[::-1])
    mirrors = sorted({tuple(sorted((nm, nm[::-1]))) for nm in names if nm[::-1] in names and nm != nm[::-1]})
    return [{
        "probe": "s6_simetria_palindromos", "lens": "symmetry",
        "title": "Palindrome names and mirror pairs in the hierarchy",
        "technique": f"Palindromic names (read the same backwards) vs random names of the same shape (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"palindromes": pal[:20], "mirror_pairs": [list(e) for e in mirrors[:12]]},
        "canonical": "s6:palindromes",
        "class": "candidate",
        "caveat": "Excess palindromes would suggest intent in the name design; check whether they are whole names or line fragments.",
        "evidence_terms": ["palindrome", "mirror", "symmetry"],
    }]


# ================================================================= S7 numerology 3-6-9
def s7_numeros_369(ctx, params, rng):
    sid = params.get("sid", "golden_dawn_coluna__F08")
    trials = params.get("trials", 500)
    roots = [N.raiz_digital(ctx.G.valor(sid, e["norm"])) for e in ctx.nh if ctx.G.cobre(sid, e["norm"])]
    roots = [r for r in roots if r]
    if len(roots) < 20:
        return []
    obs = sum(1 for r in roots if r in (3, 6, 9))
    n = len(roots)
    # HARDENED null: shuffle the letter->value assignment, keeping the real names. This isolates
    # whether the NAMES concentrate 3/6/9, controlling for the system's own value distribution.
    names = [e["norm"] for e in ctx.nh if ctx.G.cobre(sid, e["norm"])]
    tab = ctx.G.sist[sid]
    letters, vals = list(tab), list(tab.values())

    def count369(m):
        rz = [N.raiz_digital(sum(m[c] for c in nm)) for nm in names]
        return sum(1 for r in rz if r in (3, 6, 9))
    sims = []
    for _ in range(trials):
        rng.shuffle(vals)
        sims.append(count369(dict(zip(letters, vals))))
    stat = N.p_empirico(obs, sims, cauda="dois")
    from collections import Counter
    return [{
        "probe": "s7_numeros_369", "lens": "numerology",
        "title": "Concentration of 3-6-9 digital roots in name values",
        "technique": f"Number of names whose digital root ({sid}) is 3/6/9, vs shuffling the system's letter->value assignment (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"system": sid, "n": n, "in_369": obs, "distribution": dict(Counter(roots))},
        "canonical": f"s7:{sid}",
        "class": "candidate",
        "caveat": "Hardened null (shuffle letter->value): if it falls, the concentration belongs to the gematria system, not the names. Prior investigation: falls for GD.",
        "evidence_terms": ["369", "digital root", "number"],
    }]


# ================================================================= S8 kabbalah: root->sefira per Tower
def s8_cabala_sefira(ctx, params, rng):
    sid = params.get("sid", "golden_dawn_coluna__F08")
    trials = params.get("trials", 400)
    per_tower = defaultdict(list)
    for e in ctx.nh:
        if ctx.G.cobre(sid, e["norm"]):
            r = N.raiz_digital(ctx.G.valor(sid, e["norm"]))
            if r:
                per_tower[e["tower"]].append(r)
    towers = [t for t in per_tower if len(per_tower[t]) >= 10]
    if len(towers) < 3:
        return []

    def separation(signatures):
        profiles = []
        for t in towers:
            c = [0] * 10
            for r in signatures[t]:
                c[r] += 1
            s = sum(c) or 1
            profiles.append([x / s for x in c])
        tot = 0.0
        for i in range(len(profiles)):
            for j in range(i + 1, len(profiles)):
                tot += sum(abs(a - b) for a, b in zip(profiles[i], profiles[j]))
        return tot

    obs = separation(per_tower)
    allr = [r for t in towers for r in per_tower[t]]
    sizes = {t: len(per_tower[t]) for t in towers}
    sims = []
    for _ in range(trials):
        emb = allr[:]
        rng.shuffle(emb)
        ass = {}
        i = 0
        for t in towers:
            ass[t] = emb[i:i + sizes[t]]
            i += sizes[t]
        sims.append(separation(ass))
    stat = N.p_empirico(obs, sims)
    modal = {t: max(set(per_tower[t]), key=per_tower[t].count) for t in towers}
    return [{
        "probe": "s8_cabala_sefira", "lens": "metaphysics",
        "title": "Each Tower prefers its own digital roots (sefirot) - a kabbalistic signature per element",
        "technique": f"Separation of the digital-root profiles ({sid}) across the 4 Towers vs shuffled Tower labels (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"system": sid, "modal_root_per_tower": modal},
        "canonical": f"s8:{sid}",
        "class": "known",
        "caveat": "Investigation: DOWNGRADED. The separation comes only from letter composition (4 distinct tables, a known fact); the modal roots do NOT match the element's traditional number. Not a sefirotic code.",
        "evidence_terms": ["sefira", "sefirot", "element", "tree of life"],
    }]


# ================================================================= S9 governors: servants vs name value
def s9_governadores_servos(ctx, params, rng):
    sid = params.get("sid", "golden_dawn_coluna__F08")
    trials = params.get("trials", 2000)
    pairs = []
    for g in N.fontes.governors()["governadores"]:
        nm = N.norm(g.get("nome", ""))
        try:
            sv = int(g.get("servos"))
        except (TypeError, ValueError):
            continue
        if nm and ctx.G.cobre(sid, nm):
            pairs.append((sv, ctx.G.valor(sid, nm)))
    if len(pairs) < 20:
        return []
    a = [p[0] for p in pairs]
    b = [p[1] for p in pairs]
    rho = N.spearman(a, b)
    bb = b[:]
    sims = []
    for _ in range(trials):
        rng.shuffle(bb)
        sims.append(N.spearman(a, bb))
    stat = N.p_empirico(rho, sims, cauda="dois")
    stat["obs"] = round(rho, 3)
    return [{
        "probe": "s9_governadores_servos", "lens": "numerology",
        "title": "Does a Governor's number of servants track its name's gematria?",
        "technique": f"Spearman correlation between servants Dee declares and the name value ({sid}) of each Governor, vs shuffled (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"system": sid, "n_governors": len(pairs), "rho": round(rho, 3)},
        "canonical": f"s9:{sid}",
        "class": "candidate",
        "caveat": "Servants and name come from the same source (Dee); correlation above chance would suggest a construction rule, not proven meaning.",
        "evidence_terms": ["governor", "servants", "ministers"],
    }]


# ================================================================= S10 Loagaeth k-grams vs Towers
def _linhas_grade(grid):
    H, W = len(grid), len(grid[0])
    out = ["".join(r) for r in grid] + ["".join(grid[r][c] for r in range(H)) for c in range(W)]
    for d in range(-H + 1, W):
        out.append("".join(grid[r][r + d] for r in range(H) if 0 <= r + d < W))
    return out


def _kgrams(strs, L):
    s = set()
    for w in strs:
        w = w.replace("?", "")
        for i in range(len(w) - L + 1):
            s.add(w[i:i + L])
    return s


def s10_kgramas_loagaeth(ctx, params, rng):
    L = params.get("L", 4)
    trials = params.get("trials", 150)
    loa = ctx.corpora_freq.get("Loagaeth", "")
    if len(loa) < 400:
        return []
    kt = set().union(*[_kgrams(_linhas_grade(g), L) for g in ctx.grades_dee.values()])
    obs = len(kt & _kgrams([loa], L))
    # HARDENED null: pseudo-Loagaeth by order-1 Markov (same letter-transition statistics).
    # It only survives if the REAL Loagaeth shares more with the Towers than a text of equal
    # statistics - otherwise it is just the common Enochian alphabet.
    from collections import Counter
    pairs = Counter(zip(loa, loa[1:]))
    trans = {}
    for (a, b), c in pairs.items():
        trans.setdefault(a, []).append((b, c))

    def pseudo(nn):
        if not trans:
            return ""
        cur = rng.choice(list(trans))
        out = [cur]
        for _ in range(nn - 1):
            opc = trans.get(cur) or [(rng.choice(list(trans)), 1)]
            tot = sum(c for _, c in opc)
            x = rng.randint(1, tot)
            ac = 0
            for b, c in opc:
                ac += c
                if x <= ac:
                    cur = b
                    break
            out.append(cur)
        return "".join(out)
    sims = [len(kt & _kgrams([pseudo(len(loa))], L)) for _ in range(trials)]
    stat = N.p_empirico(obs, sims)
    shared = sorted(kt & _kgrams([loa], L))
    return [{
        "probe": "s10_kgramas_loagaeth", "lens": "frequency",
        "title": f"{L}-letter chunks shared between the Loagaeth and the Towers",
        "technique": f"Number of {L}-grams Towers n Loagaeth, vs a pseudo-Loagaeth Markov of equal statistics (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"L": L, "shared": shared[:30]},
        "canonical": f"s10:L{L}",
        "class": "candidate",
        "caveat": "Markov null: survives only if the REAL Loagaeth shares more than a text of equal letter statistics. Prior investigation: falls (it is the common alphabet).",
        "evidence_terms": ["Loagaeth", "Great Table", "angelical language"],
    }]


# ================================================================= S11 skip cipher (ELS)
def s11_saltos_els(ctx, params, rng):
    trials = params.get("trials", 200)
    skips = params.get("saltos", (2, 3, 4, 5))
    names = sorted({e["norm"] for e in ctx.nh if 4 <= len(e["norm"]) <= 5})[:140]
    if len(names) < 10:
        return []

    def haystack(grids):
        hay = set()
        for g in grids:
            flat = "".join("".join(r) for r in g).replace("?", "")
            for d in skips:
                for off in range(d):
                    hay.add(flat[off::d])
        return "#".join(hay)
    grids = list(ctx.grades_dee.values())
    hay = haystack(grids)
    obs = sum(1 for w in names if w in hay)
    comp = [len(w) for w in names]
    sims = []
    for _ in range(trials):
        rnames = ["".join(rng.choice(ctx.urna) for _ in range(c)) for c in comp]
        sims.append(sum(1 for w in rnames if w in hay))
    stat = N.p_empirico(obs, sims)
    found_els = [w for w in names if w in hay]
    return [{
        "probe": "s11_saltos_els", "lens": "geometry",
        "title": "Names hidden at regular skips (ELS) in the Towers - Bible-code style test",
        "technique": f"Names that appear reading the Towers at a fixed step (skips {skips}), vs random names in the same haystack (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"skips": list(skips), "names_tested": len(names), "els_found": found_els[:20]},
        "canonical": f"s11:{'-'.join(map(str, skips))}",
        "class": "candidate",
        "caveat": "ELS finds ANYTHING in long text - that is why the null is everything. It only counts if the real names beat random names in the SAME haystack.",
        "evidence_terms": ["hidden", "cipher", "key"],
    }]


# ================================================================= S13 gematria links different classes
def s13_gematria_entre_classes(ctx, params, rng):
    sid = params.get("sid", "golden_dawn_coluna__F08")
    trials = params.get("trials", 1000)
    reps = {}
    kinds = {}
    for e in ctx.nh:
        if ctx.G.cobre(sid, e["norm"]):
            reps[e["ms"]] = ctx.G.valor(sid, e["norm"])
            kinds.setdefault(e["ms"], set()).add(e["kind"].split(" ")[0])
    if len(reps) < 10:
        return []
    byval = defaultdict(list)
    for ms, v in reps.items():
        byval[v].append(ms)
    edges = [(a, b) for g in byval.values() if len(g) > 1 for i, a in enumerate(g) for b in g[i + 1:]]
    if not edges:
        return []

    def cross(labels):
        return sum(1 for a, b in edges if labels[a].isdisjoint(labels[b]))
    obs = cross(kinds)
    keys = list(kinds)
    labels = [kinds[k] for k in keys]
    sims = []
    for _ in range(trials):
        rng.shuffle(labels)
        lab = dict(zip(keys, labels))
        sims.append(cross(lab))
    stat = N.p_empirico(obs, sims, cauda="dois")
    bridges = []
    for a, b in edges:
        if kinds[a].isdisjoint(kinds[b]):
            bridges.append({"a": a, "b": b, "classes": sorted(kinds[a] | kinds[b]), "value": reps[a]})
        if len(bridges) >= 8:
            break
    return [{
        "probe": "s13_gematria_entre_classes", "lens": "gematria",
        "title": "Do gematria equivalences link different ranks of the hierarchy?",
        "technique": f"Number of equal-value pairs ({sid}) that link distinct classes (e.g. lesser angel <-> king), vs shuffled class labels (n={trials}).",
        "stat": stat, "verdict": N.veredito(stat["p"]),
        "detail": {"system": sid, "equal_pairs": len(edges), "cross_class_bridges": bridges},
        "canonical": f"s13:{sid}",
        "class": "candidate",
        "caveat": "If equalities prefer to link different ranks, it would suggest a hidden bridge in the hierarchy; if not, it is numeric chance.",
        "evidence_terms": ["hierarchy", "same value", "king"],
    }]


SONDAS = [
    s1_gematria_equivalencias, s2_gematria_consenso, s3_valor_x_chamadas,
    s4_parentesco_frequencia, s5_geometria_conjuntos, s6_simetria_palindromos,
    s7_numeros_369, s8_cabala_sefira,
    s9_governadores_servos, s10_kgramas_loagaeth, s11_saltos_els, s13_gematria_entre_classes,
]
