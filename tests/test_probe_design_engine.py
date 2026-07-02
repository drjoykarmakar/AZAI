from azai.fluorescence.experiment_plan import recommended_experiment_plan
from azai.fluorescence.linkers import linker_table
from azai.fluorescence.probe_builder import generate_probe_concepts
from azai.fluorescence.recognition import recognition_motif_table
from azai.fluorescence.selectivity_matrix import probe_interferent_matrix
from azai.fluorescence.spectra import fluorophore_spectral_window, optical_priority_label


def test_recognition_and_linker_libraries_are_available():
    motifs = recognition_motif_table()
    linkers = linker_table()
    assert len(motifs) >= 4
    assert len(linkers) >= 4
    assert "target_features" in motifs[0]
    assert "synthetic_accessibility" in linkers[0]


def test_generate_probe_concepts_has_v07_fields():
    concepts = generate_probe_concepts(limit=5)
    assert len(concepts) == 5
    top = concepts[0]
    assert top["total_score"] > 0
    assert "spectral_window" in top
    assert "next_experiment" in top


def test_spectra_helpers():
    window = fluorophore_spectral_window("coumarin")
    assert window["typical_excitation_nm"]
    assert optical_priority_label("fluorescein") in {
        "high-priority optical screen",
        "medium-priority optical screen",
        "specialized or formulation-dependent optical screen",
    }


def test_experiment_plan_and_selectivity_matrix():
    plan = recommended_experiment_plan(71.0, "PET", "common amines")
    assert len(plan) >= 5
    matrix = probe_interferent_matrix(62.0)
    assert "probe_adjusted_risk" in matrix.columns
    assert "recommended_control_priority" in matrix.columns
