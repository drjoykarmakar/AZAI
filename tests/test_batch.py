
import pandas as pd

from azai.molecules.batch import analyze_smiles_list, xylazine_similarity_workup


def test_analyze_smiles_list_keeps_invalid_rows():
    result = analyze_smiles_list(["CCO", "not_a_smiles"], labels=["ethanol", "bad"])
    assert len(result) == 2
    assert result.loc[0, "error"] == ""
    assert result.loc[1, "error"] != ""


def test_xylazine_similarity_workup_adds_similarity_columns():
    df = pd.DataFrame({"name": ["xylazine"], "smiles": ["Cc1cccc(C)c1NC(=N)N1CCCCC1"]})
    result = xylazine_similarity_workup(df, label_column="name")
    assert "morgan_tanimoto" in result.columns
    assert result.loc[0, "morgan_tanimoto"] > 0.99
