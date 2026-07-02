"""Batch molecule analysis utilities for AZAI."""

from __future__ import annotations

from collections.abc import Iterable

import pandas as pd

from azai.molecules.descriptors import calculate_descriptors
from azai.molecules.functional_groups import present_functional_groups
from azai.molecules.similarity import rank_by_similarity
from azai.xylazine.reference import XYLAZINE


def analyze_smiles_list(smiles_list: Iterable[str], labels: Iterable[str] | None = None) -> pd.DataFrame:
    """Analyze a list of SMILES strings and return descriptor rows.

    Invalid molecules are retained with an ``error`` column so user CSV uploads can be
    reviewed without silently dropping entries.
    """
    label_values = list(labels) if labels is not None else None
    rows: list[dict[str, object]] = []
    for index, smiles in enumerate(smiles_list):
        label = label_values[index] if label_values and index < len(label_values) else f"molecule_{index + 1}"
        try:
            desc = calculate_descriptors(str(smiles))
            alerts = present_functional_groups(str(smiles))
            row: dict[str, object] = {"label": label, "input_smiles": str(smiles), **desc}
            row["present_functional_groups"] = "; ".join(alerts)
            row["error"] = ""
        except Exception as exc:  # noqa: BLE001 - preserve user-facing batch errors
            row = {"label": label, "input_smiles": str(smiles), "error": str(exc)}
        rows.append(row)
    return pd.DataFrame(rows)


def analyze_uploaded_table(df: pd.DataFrame, smiles_column: str = "smiles", label_column: str | None = None) -> pd.DataFrame:
    """Analyze a CSV-like table with a SMILES column."""
    if smiles_column not in df.columns:
        raise ValueError(f"Input table must contain a '{smiles_column}' column.")
    labels = df[label_column].astype(str).tolist() if label_column and label_column in df.columns else None
    return analyze_smiles_list(df[smiles_column].astype(str).tolist(), labels=labels)


def xylazine_similarity_workup(df: pd.DataFrame, smiles_column: str = "smiles", label_column: str | None = None) -> pd.DataFrame:
    """Return descriptor and xylazine-similarity information for an input table."""
    analyzed = analyze_uploaded_table(df, smiles_column=smiles_column, label_column=label_column)
    valid = analyzed[analyzed["error"].fillna("").eq("")]
    if valid.empty:
        return analyzed
    ranked = rank_by_similarity(valid["input_smiles"].astype(str).tolist(), XYLAZINE.smiles)
    ranked.insert(0, "label", valid["label"].astype(str).tolist())
    return analyzed.merge(ranked, on="label", how="left", suffixes=("", "_similarity"))
