"""Validation helpers for user-provided AZAI tables."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
from rdkit import Chem


@dataclass(frozen=True)
class ValidationIssue:
    """One validation issue found in an input table."""

    row: int
    column: str
    message: str
    severity: str = "error"


def validate_smiles_table(
    df: pd.DataFrame,
    smiles_column: str = "smiles",
    label_column: str | None = None,
) -> dict[str, object]:
    """Validate a table containing SMILES strings.

    Returns a dictionary with a clean copy of the table, summary counts, and
    row-level issues. Invalid rows are not dropped automatically; downstream
    batch analysis can keep them visible to the user.
    """
    issues: list[ValidationIssue] = []
    if smiles_column not in df.columns:
        return {
            "is_valid": False,
            "valid_rows": 0,
            "invalid_rows": len(df),
            "issues": [ValidationIssue(-1, smiles_column, f"Missing required column '{smiles_column}'")],
            "clean_table": df.copy(),
        }

    clean = df.copy()
    clean[smiles_column] = clean[smiles_column].astype(str).str.strip()
    if label_column and label_column in clean.columns:
        clean[label_column] = clean[label_column].astype(str).str.strip()

    valid_count = 0
    for row_number, value in clean[smiles_column].items():
        if not value or value.lower() in {"nan", "none"}:
            issues.append(ValidationIssue(int(row_number), smiles_column, "Empty SMILES string"))
            continue
        mol = Chem.MolFromSmiles(value)
        if mol is None:
            issues.append(ValidationIssue(int(row_number), smiles_column, "Invalid SMILES string"))
            continue
        valid_count += 1

    return {
        "is_valid": len(issues) == 0,
        "valid_rows": valid_count,
        "invalid_rows": len(clean) - valid_count,
        "issues": issues,
        "clean_table": clean,
    }


def issues_to_frame(issues: list[ValidationIssue]) -> pd.DataFrame:
    """Convert validation issues to a display-friendly DataFrame."""
    return pd.DataFrame([issue.__dict__ for issue in issues], columns=["row", "column", "message", "severity"])
