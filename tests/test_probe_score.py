from azai.fluorescence.fluorophores import FLUOROPHORES
from azai.scoring.probe_score import ProbeConcept, score_probe_concept


def test_probe_score_range():
    concept = ProbeConcept("coumarin", "amine recognition motif", "amide", "PET", "test hypothesis")
    score = score_probe_concept(concept, FLUOROPHORES["coumarin"])
    assert 0 <= score["total_score"] <= 100
    assert "component_scores" in score
