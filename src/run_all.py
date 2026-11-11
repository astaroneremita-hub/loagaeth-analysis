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
import a11_lineages
import a12_empire
import a13_numbers
import a14_anzach
import a15_book_geometry
import a16_letters
import a17_kingdom
import a18_markup_decoding
import a19_machine
import a20_energy_fibonacci_gd
import a21_index_heptarchy_numbers
import a22_robustness_and_depth
import a23_name_discovery
import a24_book_architecture
import a25_bridges
import a26_letter_names
import make_figures
import make_viz_data

MODULES = [
    # a18 runs first: it downloads Peterson's page (if missing) and writes the diagonal-decoded
    # text of tables 25b-28b, which later modules (territory, geometry) read.
    ("18_markup_decoding", a18_markup_decoding),
    ("01_basic_stats", a01_basic_stats),
    ("02_network", a02_network),
    ("03_master_name", a03_master_name),
    ("04_morphology", a04_morphology),
    ("05_signature_names", a05_signature_names),
    ("06_call_bridge", a06_call_bridge),
    ("08_refutations", a08_refutations),
    ("09_letter_grammar", a09_letter_grammar),
    ("10_territory", a10_territory),
    ("11_lineages", a11_lineages),
    ("12_empire", a12_empire),
    ("13_numbers", a13_numbers),
    ("14_anzach", a14_anzach),
    ("15_book_geometry", a15_book_geometry),
    ("16_letters", a16_letters),
    ("17_kingdom", a17_kingdom),
    ("19_machine", a19_machine),
    ("20_energy_fibonacci_gd", a20_energy_fibonacci_gd),
    ("21_index_heptarchy_numbers", a21_index_heptarchy_numbers),
    ("22_robustness_and_depth", a22_robustness_and_depth),
    ("23_name_discovery", a23_name_discovery),
    ("24_book_architecture", a24_book_architecture),
    ("25_bridges", a25_bridges),
    ("26_letter_names", a26_letter_names),
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
    print("\n[figures]")
    for f in make_figures.run():
        print("  " + f)
    print("\n[3D viewer data]")
    make_viz_data.main()


if __name__ == "__main__":
    main()
