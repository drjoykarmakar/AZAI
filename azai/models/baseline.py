"""Transparent baseline models for descriptor-based prioritization.

These utilities are intentionally simple. They are designed for small, user-supplied
example datasets and should not be presented as validated QSAR models without
external validation.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from azai.molecules.descriptors import descriptor_vector

DEFAULT_DESCRIPTOR_KEYS = [
    "molecular_weight",
    "logp",
    "tpsa",
    "hbond_donors",
    "hbond_acceptors",
    "rotatable_bonds",
    "formal_charge",
    "aromatic_rings",
    "heteroatoms",
    "fraction_csp3",
]


@dataclass(frozen=True)
class BaselineModelResult:
    """Container for a fitted baseline model and lightweight metadata."""

    model_type: str
    descriptor_keys: list[str]
    cross_validation_r2_mean: float | None
    cross_validation_r2_std: float | None
    warning: str


def smiles_to_descriptor_frame(smiles: Iterable[str], keys: list[str] | None = None) -> pd.DataFrame:
    """Convert SMILES strings to a numeric descriptor matrix."""
    selected = keys or DEFAULT_DESCRIPTOR_KEYS
    rows = [descriptor_vector(smi, selected) for smi in smiles]
    return pd.DataFrame(rows, columns=selected)


def train_baseline_regressor(
    data: pd.DataFrame,
    smiles_column: str = "smiles",
    target_column: str = "target",
    model_type: str = "ridge",
) -> tuple[Pipeline | RandomForestRegressor, BaselineModelResult]:
    """Train a transparent baseline regression model from SMILES and a numeric target.

    Parameters
    ----------
    data:
        DataFrame containing at least SMILES and target columns.
    smiles_column:
        Column containing SMILES strings.
    target_column:
        Column containing measured target values.
    model_type:
        Either ``ridge`` or ``random_forest``.
    """
    if smiles_column not in data.columns or target_column not in data.columns:
        raise ValueError("Input data must contain SMILES and target columns.")

    clean = data[[smiles_column, target_column]].dropna().copy()
    clean[target_column] = pd.to_numeric(clean[target_column], errors="coerce")
    clean = clean.dropna()
    if len(clean) < 3:
        raise ValueError("At least three valid rows are required for a baseline model.")

    x = smiles_to_descriptor_frame(clean[smiles_column].astype(str))
    y = clean[target_column].astype(float).to_numpy()

    if model_type == "ridge":
        model: Pipeline | RandomForestRegressor = Pipeline(
            [("scale", StandardScaler()), ("model", Ridge(alpha=1.0))]
        )
    elif model_type == "random_forest":
        model = RandomForestRegressor(n_estimators=100, random_state=42, min_samples_leaf=1)
    else:
        raise ValueError("model_type must be 'ridge' or 'random_forest'.")

    cv_mean = None
    cv_std = None
    if len(clean) >= 10:
        # R2 is undefined for one-sample test folds, so require enough rows
        # for meaningful lightweight cross-validation.
        cv = min(5, len(clean) // 2)
        scores = cross_val_score(model, x, y, cv=cv, scoring="r2")
        cv_mean = float(np.mean(scores))
        cv_std = float(np.std(scores))

    model.fit(x, y)
    warning = (
        "Baseline model fitted for exploratory analysis only. Do not claim predictive performance "
        "without held-out validation, applicability-domain checks, and experimental context."
    )
    result = BaselineModelResult(
        model_type=model_type,
        descriptor_keys=list(x.columns),
        cross_validation_r2_mean=cv_mean,
        cross_validation_r2_std=cv_std,
        warning=warning,
    )
    return model, result


def predict_from_smiles(
    model: Pipeline | RandomForestRegressor,
    smiles: Iterable[str],
    keys: list[str] | None = None,
) -> pd.DataFrame:
    """Predict target values for SMILES using a fitted baseline model."""
    descriptor_df = smiles_to_descriptor_frame(smiles, keys)
    predictions = model.predict(descriptor_df)
    output = descriptor_df.copy()
    output.insert(0, "smiles", list(smiles))
    output["prediction"] = predictions
    return output
