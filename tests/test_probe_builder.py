from azai.fluorescence.probe_builder import generate_probe_concepts


def test_generate_probe_concepts_ranked():
    concepts = generate_probe_concepts(limit=5)
    assert len(concepts) == 5
    assert concepts[0]["total_score"] >= concepts[-1]["total_score"]
    assert "fluorophore" in concepts[0]
    assert "selectivity_concern" in concepts[0]
