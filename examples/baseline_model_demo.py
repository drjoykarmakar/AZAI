"""Train a tiny transparent baseline model on example values.

The target column is toy data for software demonstration only.
"""

import pandas as pd

from azai.models.baseline import predict_from_smiles, train_baseline_regressor

example = pd.DataFrame(
    {
        "smiles": ["CCO", "CCN", "CCC", "c1ccccc1", "CC(=O)O"],
        "target": [1.0, 1.2, 0.8, 2.0, 0.5],
    }
)
model, meta = train_baseline_regressor(example, model_type="ridge")
print(meta)
print(predict_from_smiles(model, ["CCO", "CCN"]))
