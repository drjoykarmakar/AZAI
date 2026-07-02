"""Explainability helpers for AZAI baseline models."""

from __future__ import annotations

import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline


def descriptor_contribution_table(descriptors: dict[str, float | int | str]) -> pd.DataFrame:
    """Create a conservative descriptor contribution table for a molecule.

    Contributions are heuristic directions for interpretation, not causal model attributions.
    """
    rules = [
        ("molecular_weight", "Size and mass influence diffusion, solubility, and assay matrix behavior."),
        ("logp", "Lipophilicity can affect aqueous compatibility and nonspecific binding."),
        ("tpsa", "Polar surface area influences H-bonding and polarity-driven recognition."),
        ("hbond_acceptors", "Acceptors/basic heteroatoms may support H-bond or ion-pair recognition."),
        ("hbond_donors", "Donors can contribute to recognition and solubility."),
        ("rotatable_bonds", "Flexibility may affect binding entropy and probe response geometry."),
        ("aromatic_rings", "Aromaticity may support pi-stacking or hydrophobic recognition."),
        ("heteroatoms", "Heteroatoms shape protonation, polarity, and recognition options."),
    ]
    rows = []
    for key, interpretation in rules:
        if key in descriptors:
            rows.append({"descriptor": key, "value": descriptors[key], "interpretation": interpretation})
    return pd.DataFrame(rows)


def feature_importance_table(model: object, feature_names: list[str]) -> pd.DataFrame:
    """Return feature importance or coefficient magnitudes for supported baseline models."""
    estimator = model
    if isinstance(model, Pipeline):
        estimator = model.named_steps.get("model")

    if hasattr(estimator, "feature_importances_"):
        values = getattr(estimator, "feature_importances_")
    elif hasattr(estimator, "coef_"):
        values = abs(getattr(estimator, "coef_"))
    else:
        raise ValueError("Model does not expose feature importances or coefficients.")

    table = pd.DataFrame({"feature": feature_names, "importance": values})
    return table.sort_values("importance", ascending=False).reset_index(drop=True)
