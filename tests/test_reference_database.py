from azai.xylazine.database import reference_table, reference_smiles_by_category


def test_reference_table_contains_xylazine_and_interferents():
    table = reference_table()
    assert "xylazine" in table["name"].tolist()
    assert "interferent" in table["category"].tolist()


def test_reference_filter():
    filtered = reference_smiles_by_category("target")
    assert len(filtered) == 1
    assert filtered.iloc[0]["name"] == "xylazine"
