import pandas as pd

from azai.data.validation import issues_to_frame, validate_smiles_table


def test_validate_smiles_table_counts_invalid_rows():
    df = pd.DataFrame({"name": ["ethanol", "bad"], "smiles": ["CCO", "not_a_smiles"]})
    result = validate_smiles_table(df, label_column="name")
    assert result["is_valid"] is False
    assert result["valid_rows"] == 1
    assert result["invalid_rows"] == 1
    issues = issues_to_frame(result["issues"])
    assert "Invalid SMILES" in issues.loc[0, "message"]


def test_validate_missing_smiles_column():
    result = validate_smiles_table(pd.DataFrame({"name": ["x"]}))
    assert result["is_valid"] is False
    assert result["invalid_rows"] == 1
