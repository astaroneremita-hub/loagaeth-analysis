"""
Run every analysis in order and write a combined results/summary.json.

Usage:
    python src/run_all.py

Pure standard library. Deterministic (fixed seeds). Writes one JSON per module in
results/ plus a combined summary.
"""
import json
import time

import load
import a01_basic_stats
import a02_network
import a03_master_name
import a04_morphology
import a05_signature_names
import a06_call_bridge
import a08_refutations
import a09_letter_grammar
import a10_territory

MODULES = [
    ("01_basic_stats", a01_basic_stats),
    ("02_network", a02_network),
    ("03_master_name", a03_master_name),
    ("04_morphology", a04_morphology),
    ("05_signature_names", a05_signature_names),
    ("06_call_bridge", a06_call_bridge),
    ("08_refutations", a08_refutations),
    ("09_letter_grammar", a09_letter_grammar),
    ("10_territory", a10_territory),
]


def main():
    summary = {"generated": time.strftime("%Y-%m-%d %H:%M:%S"), "modules": {}}
    for name, mod in MODULES:
        t = time.time()
        print(f"[run] {name} ...", end=" ", flush=True)
        res = mod.run()
        summary["modules"][name] = res
        print(f"ok ({time.time()-t:.1f}s)")
    load.save_result("summary", summary)
    print("\nWrote results/summary.json and per-module files.")


if __name__ == "__main__":
    main()
