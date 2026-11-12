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
import a27_doubts
import a28_names_deep
import a29_architecture_deep
import a30_anchors
import a31_grammar
import a32_one_language
import a33_diary_anchors
import a34_vowel_paradigms
import a35_nalvage_coordinates
import a36_soyga_calibration
import a37_mixed_decoding
import a38_open_leads
import a39_long_repeats
import a40_formulas
import a41_sound_classes
import a42_repeat_map
import a43_recency
import a44_positive_control
import a45_variation_channel
import a46_generator
import a47_templates
import a48_beyond_five_elsewhere
import a49_leaf_and_junctions
import a50_chessboard_order
import a51_word_points
import a52_origin_of_formulas
import a53_second_transcription
import a54_source_checks
import a55_leaf49_words
import a56_one_name
import a57_forum_checks
import a58_direction_and_transition
import a59_calls_every_path
import a60_tampering
import a61_navigation_and_soyga_rule
import a62_chant_and_cube
import a63_metre
import a64_finer_chant
import a65_bridges_refrains_acrostics
import a66_seven_and_columns
import a67_presiding_names
import a68_dahahoxom_home
import a69_path_tracing
import a70_packing_meaning
import a71_omnidirectional
import a72_rotation_family
import a73_family_sweep
import a74_gematria_lines
import a75_row_stratification
import a76_letter_position_map
import a77_names_woven
import a78_territory_map
import a79_hierarchy_powers
import a80_full_hierarchy
import a81_name_derivation
import a82_grammar_discovery
import a83_bridge_names
import a84_entity_profiles
import a85_entity_attributes
import a86_forge_and_grids
import a87_gematria_crosssystem
import a88_external_names
import a89_calls_source
import a90_element_proof_danger
import a91_flow_calls_oddletter
import a92_is_it_a_language
import a93_call_char_trace
import a94_call_words_in_loagaeth
import a95_call_atlas
import a96_diagonal_segment
import make_figures
import make_viz_data

MODULES = [
    # a18 runs first: it downloads Peterson's page (if missing) and writes the diagonal-decoded
    # text of tables 25b-28b, which later modules (territory, geometry) read.
    ("18_markup_decoding", a18_markup_decoding),
    # a37 refines that decoding (row blocks and zones); later modules read it through a22.base_book
    ("37_mixed_decoding", a37_mixed_decoding),
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
    ("27_doubts", a27_doubts),
    ("28_names_deep", a28_names_deep),
    ("29_architecture_deep", a29_architecture_deep),
    ("30_anchors", a30_anchors),
    ("31_grammar", a31_grammar),
    ("32_one_language", a32_one_language),
    ("33_diary_anchors", a33_diary_anchors),
    ("34_vowel_paradigms", a34_vowel_paradigms),
    ("35_nalvage_coordinates", a35_nalvage_coordinates),
    ("36_soyga_calibration", a36_soyga_calibration),
    ("38_open_leads", a38_open_leads),
    ("39_long_repeats", a39_long_repeats),
    ("40_formulas", a40_formulas),
    ("41_sound_classes", a41_sound_classes),
    ("42_repeat_map", a42_repeat_map),
    ("43_recency", a43_recency),
    ("44_positive_control", a44_positive_control),
    ("45_variation_channel", a45_variation_channel),
    ("46_generator", a46_generator),
    ("47_templates", a47_templates),
    ("48_beyond_five_elsewhere", a48_beyond_five_elsewhere),
    ("49_leaf_and_junctions", a49_leaf_and_junctions),
    ("50_chessboard_order", a50_chessboard_order),
    ("51_word_points", a51_word_points),
    ("52_origin_of_formulas", a52_origin_of_formulas),
    ("53_second_transcription", a53_second_transcription),
    ("54_source_checks", a54_source_checks),
    ("55_leaf49_words", a55_leaf49_words),
    ("56_one_name", a56_one_name),
    ("57_forum_checks", a57_forum_checks),
    ("58_direction_and_transition", a58_direction_and_transition),
    ("59_calls_every_path", a59_calls_every_path),
    ("60_tampering", a60_tampering),
    ("61_navigation_and_soyga_rule", a61_navigation_and_soyga_rule),
    ("62_chant_and_cube", a62_chant_and_cube),
    ("63_metre", a63_metre),
    ("64_finer_chant", a64_finer_chant),
    ("65_bridges_refrains_acrostics", a65_bridges_refrains_acrostics),
    ("66_seven_and_columns", a66_seven_and_columns),
    ("67_presiding_names", a67_presiding_names),
    ("68_dahahoxom_home", a68_dahahoxom_home),
    ("69_path_tracing", a69_path_tracing),
    ("70_packing_meaning", a70_packing_meaning),
    ("71_omnidirectional", a71_omnidirectional),
    ("72_rotation_family", a72_rotation_family),
    ("73_family_sweep", a73_family_sweep),
    ("74_gematria_lines", a74_gematria_lines),
    ("75_row_stratification", a75_row_stratification),
    ("76_letter_position_map", a76_letter_position_map),
    ("77_names_woven", a77_names_woven),
    ("78_territory_map", a78_territory_map),
    ("79_hierarchy_powers", a79_hierarchy_powers),
    ("80_full_hierarchy", a80_full_hierarchy),
    ("81_name_derivation", a81_name_derivation),
    ("82_grammar_discovery", a82_grammar_discovery),
    ("83_bridge_names", a83_bridge_names),
    ("84_entity_profiles", a84_entity_profiles),
    ("85_entity_attributes", a85_entity_attributes),
    ("86_forge_and_grids", a86_forge_and_grids),
    ("87_gematria_crosssystem", a87_gematria_crosssystem),
    ("88_external_names", a88_external_names),
    ("89_calls_source", a89_calls_source),
    ("90_element_proof_danger", a90_element_proof_danger),
    ("91_flow_calls_oddletter", a91_flow_calls_oddletter),
    ("92_is_it_a_language", a92_is_it_a_language),
    ("93_call_char_trace", a93_call_char_trace),
    ("94_call_words_in_loagaeth", a94_call_words_in_loagaeth),
    ("95_call_atlas", a95_call_atlas),
    ("96_diagonal_segment", a96_diagonal_segment),
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
    import make_catalog
    make_catalog.run()


if __name__ == "__main__":
    main()
