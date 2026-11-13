"""
153 - Stellar Heptarchy: scale the decoded Heptarchy template to any number of celestial bodies.

The historical Heptarchy encodes the 7 classical planets. a305 decoded its hard template:
  - every name starts with a fixed initial (B),
  - every name is a fixed length (7 letters),
  - 49 = 7x7 names in a grid: col0 = kings, col1 = princes, cols 2.. = ministers, one row per body,
  - a positional CV template (vowel fraction per slot) with strict hiatus avoidance.

So the Heptarchy is a RULE, not just a list. This module applies that rule to K bodies: K groups of K
names, each name = fixed initial + (L-1) letters, built from the measured positional vowel profile,
hiatus-avoiding. For K=7 it reproduces a Heptarchy-shaped system; for K=8 (the real solar system), K=12
(a zodiacal order), K=anything, it CONSTRUCTS a well-formed analogue.

HONEST: this is structured CONSTRUCTION in the Heptarchy's grammar, not a received tradition or a
"discovery" of real names for other stars. It is the Forge idea applied to the planetary system.
"""
import json
import random

VOW = "AEIOU"
CONS = "BCDFGHKLMNPQRSTXZ"  # Enochian-ish consonant pool (no J/V/W/Y to stay period)

# positional vowel fraction measured on the real 49 (a305): slot0 is the fixed initial (consonant)
HEPT_VPROFILE = [0.0, 0.63, 0.35, 0.22, 0.51, 0.49, 0.47]


def vprofile(length):
    """stretch the 7-slot Heptarchy vowel profile to an arbitrary name length."""
    if length == len(HEPT_VPROFILE):
        return HEPT_VPROFILE[:]
    out = []
    for i in range(length):
        # map slot i onto the reference profile
        src = i * (len(HEPT_VPROFILE) - 1) / max(1, length - 1)
        lo = int(src); hi = min(lo + 1, len(HEPT_VPROFILE) - 1)
        frac = src - lo
        out.append(HEPT_VPROFILE[lo] * (1 - frac) + HEPT_VPROFILE[hi] * frac)
    out[0] = 0.0  # initial always consonant (the fixed letter)
    return out


def gen_name(initial, length, prof, rng):
    name = initial
    run_cons = 1  # the initial consonant
    for i in range(1, length):
        want_vowel = rng.random() < prof[i]
        if want_vowel and name[-1] in VOW:      # strict anti-hiatus: never two vowels
            want_vowel = False
        if not want_vowel and run_cons >= 2:     # no 3 consonants in a row -> keeps it pronounceable
            want_vowel = True
        ch = rng.choice(VOW) if want_vowel else rng.choice(CONS)
        name += ch
        run_cons = 0 if ch in VOW else run_cons + 1
    return name


def build_system(k_bodies, bodies=None, initial="B", length=None, seed=153):
    """K bodies -> K groups of K names (K x K grid), locked template."""
    rng = random.Random(seed)
    length = length or k_bodies  # the saturating number: name length = body count (7 for the classic)
    prof = vprofile(length)
    if bodies is None:
        bodies = ["Body %d" % (i + 1) for i in range(k_bodies)]
    grid = []
    seen = set()
    for b in range(k_bodies):
        row = []
        while len(row) < k_bodies:
            nm = gen_name(initial, length, prof, rng)
            if nm in seen:
                continue
            seen.add(nm)
            row.append(nm)
        grid.append({"body": bodies[b], "king": row[0], "prince": row[1] if k_bodies > 1 else None,
                     "ministers": row[2:], "all": row})
    return {"k_bodies": k_bodies, "name_length": length, "initial": initial,
            "total_names": k_bodies * k_bodies, "grid": grid,
            "rules": {"fixed_initial": initial, "fixed_length": length,
                      "grid": "%dx%d" % (k_bodies, k_bodies), "anti_hiatus": True,
                      "vowel_profile": [round(x, 2) for x in prof]},
            "honest": "Structured construction in the decoded Heptarchy template, NOT a received tradition."}


# some ready systems
SOLAR8 = ["Mercurio", "Venus", "Terra", "Marte", "Jupiter", "Saturno", "Urano", "Netuno"]
CLASSIC7 = ["Saturno", "Jupiter", "Marte", "Sol", "Venus", "Mercurio", "Lua"]
ZODIAC12 = ["Aries", "Touro", "Gemeos", "Cancer", "Leao", "Virgem", "Libra", "Escorpiao",
            "Sagitario", "Capricornio", "Aquario", "Peixes"]


def run():
    out = {
        "classic_7": build_system(7, CLASSIC7),
        "solar_8_real": build_system(8, SOLAR8),
        "zodiac_12": build_system(12, ZODIAC12),
    }
    try:
        import load
        load.save_result("153_stellar_heptarchy", out)
    except Exception:
        pass
    return out


if __name__ == "__main__":
    r = run()
    for key in ("classic_7", "solar_8_real", "zodiac_12"):
        s = r[key]
        print("\n=== %s : %d bodies, names of %d letters, %d total (all start '%s') ===" % (
            key, s["k_bodies"], s["name_length"], s["total_names"], s["initial"]))
        for row in s["grid"]:
            print("  %-12s rei %-10s principe %-10s ministros %s" % (
                row["body"], row["king"], row["prince"] or "-", " ".join(row["ministers"])))
    print("\n", r["classic_7"]["honest"])
