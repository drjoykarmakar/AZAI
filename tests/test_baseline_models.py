import pandas as pd

from azai.models.baseline import predict_from_smiles, smiles_to_descriptor_frame, train_baseline_regressor
from azai.models.explainability import descriptor_contribution_table, feature_importance_table
from azai.molecules.descriptors import calculate_descriptors


def test_smiles_to_descriptor_frame():
    frame = smiles_to_descriptor_frame(["CCO", "CCN"])
    assert len(frame) == 2
    assert "logp" in frame.columns


def test_train_baseline_regressor_and_predict():
    data = pd.DataFrame(
        {
            "smiles": ["CCO", "CCN", "CCC", "c1ccccc1", "CC(=O)O"],
            "target": [1.0, 1.2, 0.8, 2.0, 0.5],
        }
    )
    model, result = train_baseline_regressor(data, model_type="ridge")
    preds = predict_from_smiles(model, ["CCO"])
    assert result.model_type == "ridge"
    assert "prediction" in preds.columns


def test_descriptor_contribution_table():
    desc = calculate_descriptors("CCO")
    table = descriptor_contribution_table(desc)
    assert "interpretation" in table.columns
    assert len(table) >= 3


def test_feature_importance_table_with_ridge():
    data = pd.DataFrame(
        {
            "smiles": ["CCO", "CCN", "CCC", "c1ccccc1", "CC(=O)O"],
            "target": [1.0, 1.2, 0.8, 2.0, 0.5],
        }
    )
    model, result = train_baseline_regressor(data, model_type="ridge")
    table = feature_importance_table(model, result.descriptor_keys)
    assert "importance" in table.columns
