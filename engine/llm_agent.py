# -*- coding: utf-8 -*-
"""Optional LLM agent that keeps the engine LEARNING.

What it does (and does NOT do):
  - It READS the findings the engine has produced (results/achados.jsonl) and the list of
    already-refuted ideas, then asks a language model to PROPOSE new, testable hypotheses.
  - Each suggestion must name the data needed and a concrete null model, so it can be coded
    as a new probe in sondas.py.
  - The LLM NEVER decides what is true. It only proposes. The engine's null models remain the
    sole judge. This keeps the skeptical contract intact while letting the search self-improve.

Two backends, pick whichever you have:
  1. Anthropic API (cloud, needs a key):
       pip install anthropic
       set ANTHROPIC_API_KEY=sk-...        (Windows)   /   export ANTHROPIC_API_KEY=sk-...
       python llm_agent.py --n 5
  2. Ollama (local, free, no key) - stdlib only:
       run Ollama, then
       set LLM_BACKEND=ollama
       set OLLAMA_HOST=http://localhost:11434
       set OLLAMA_MODEL=qwen2.5:7b
       python llm_agent.py --n 5

Continuous self-improvement:
       python llm_agent.py --watch --rounds 13 --every 3
  runs the engine, every few rounds asks the model for fresh hypotheses, logs them to
  results/llm_suggestions.jsonl, and repeats. Implement the good ones as probes; the null
  models will then confirm or kill them.
"""
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
SUGGESTIONS = os.path.join(RESULTS, "llm_suggestions.jsonl")

SYSTEM = (
    "You are a skeptical research assistant for a statistical analysis of John Dee's "
    "Enochian system (the Great Table, the 91 governors, the Calls and the Loagaeth). "
    "You propose NEW, falsifiable hypotheses that can be tested against a NULL MODEL "
    "(letter-shuffle or order-k Markov surrogate). You never claim anything is true; the "
    "engine's null models decide. Avoid ideas already refuted. Prefer hypotheses that, if "
    "real, would leave a statistical trace a surrogate text would not."
)

PROMPT = """Current confirmed/known findings (compressed):
{findings}

Already refuted or downgraded (do NOT re-propose):
{refuted}

Propose {n} NEW hypotheses. Return ONLY a JSON array; each item:
{{"id": "short-slug",
  "hypothesis": "one sentence, falsifiable",
  "data_needed": "which bundled data (tables, governors, calls, loagaeth, gematria)",
  "null_model": "exact surrogate to compare against",
  "why_promising": "one sentence"}}
"""

REFUTED = [
    "mirror/reversal of names (syllable-pool artifact under Markov-3)",
    "Semitic triliteral-root morphology (ratio ~1.3, English-like)",
    "Call-vocabulary as a Loagaeth decode key (~3.4%, chance)",
    "Gebofal weekly reordering as a reading key",
    "geometric models: pentagonal solid, honeycomb, tesseract, CHASTOR-cube",
    "YHVH/MAD/Tetragrammaton as a grid cipher",
    "3-6-9 digital roots as a name property (belongs to the GD value system, not the names)",
    "per-Tower sefirotic signature (comes from letter composition, not a code)",
]


def _findings_digest(limit=40):
    path = os.path.join(RESULTS, "achados.jsonl")
    if not os.path.exists(path):
        return "(no findings yet - run loop.py first)"
    rows = [json.loads(l) for l in open(path, encoding="utf-8") if l.strip()]
    rows = [r for r in rows if r.get("verdict") in ("CONFIRMED", "indication")][:limit]
    return "\n".join(f"- [{r['verdict']}] {r['title']} (p={r['stat']['p']}, class={r.get('class')})"
                     for r in rows) or "(no confirmed findings yet)"


# ----------------------------------------------------------------- backends
def _ask_anthropic(prompt, model=None):
    try:
        import anthropic
    except ImportError:
        raise RuntimeError("pip install anthropic, or use LLM_BACKEND=ollama")
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY
    model = model or os.environ.get("ANTHROPIC_MODEL", "claude-opus-4-8")
    msg = client.messages.create(
        model=model,
        max_tokens=2000,
        system=SYSTEM,
        messages=[{"role": "user", "content": prompt}],
    )
    return "".join(b.text for b in msg.content if getattr(b, "type", None) == "text")


def _ask_ollama(prompt, model=None):
    host = os.environ.get("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    model = model or os.environ.get("OLLAMA_MODEL", "qwen2.5:7b")
    body = json.dumps({
        "model": model,
        "system": SYSTEM,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.7},
    }).encode("utf-8")
    req = urllib.request.Request(host + "/api/generate", data=body,
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read().decode("utf-8")).get("response", "")


def ask_llm(prompt):
    backend = os.environ.get("LLM_BACKEND", "anthropic" if os.environ.get("ANTHROPIC_API_KEY") else "ollama")
    return _ask_anthropic(prompt) if backend == "anthropic" else _ask_ollama(prompt)


# ----------------------------------------------------------------- parse + store
def _extract_json_array(text):
    i, j = text.find("["), text.rfind("]")
    if i < 0 or j < 0:
        return []
    try:
        return json.loads(text[i:j + 1])
    except json.JSONDecodeError:
        return []


def propose(n=5):
    prompt = PROMPT.format(findings=_findings_digest(), refuted="\n".join("- " + r for r in REFUTED), n=n)
    raw = ask_llm(prompt)
    ideas = _extract_json_array(raw)
    os.makedirs(RESULTS, exist_ok=True)
    with open(SUGGESTIONS, "a", encoding="utf-8") as fp:
        for idea in ideas:
            idea["ts"] = time.strftime("%Y-%m-%d %H:%M:%S")
            fp.write(json.dumps(idea, ensure_ascii=False) + "\n")
    return ideas


def watch(rounds=13, every=3, n=5):
    import loop as L
    r = 0
    while True:
        L.rodar(rodadas=every, verbose=True)
        r += every
        print(f"\n[llm] asking for {n} new hypotheses after {r} rounds ...", flush=True)
        try:
            ideas = propose(n)
            for it in ideas:
                print(f"  + {it.get('id')}: {it.get('hypothesis')}", flush=True)
            print(f"[llm] {len(ideas)} suggestions appended to {SUGGESTIONS}", flush=True)
        except Exception as ex:
            print(f"[llm] skipped ({ex})", flush=True)
        if rounds and r >= rounds:
            break


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    a = sys.argv[1:]

    def opt(name, dflt, cast):
        return cast(a[a.index(name) + 1]) if name in a else dflt
    if "--watch" in a:
        watch(rounds=opt("--rounds", 13, int), every=opt("--every", 3, int), n=opt("--n", 5, int))
    else:
        for it in propose(opt("--n", 5, int)):
            print(json.dumps(it, ensure_ascii=False, indent=1))
