from azai.release.model_cards import heuristic_probe_scorer_card


def test_model_card_renders_markdown():
    card = heuristic_probe_scorer_card()
    md = card.to_markdown()
    assert "Model Card" in md
    assert "Not experimentally validated" in md
    assert "Safety" in md or "safety" in md
