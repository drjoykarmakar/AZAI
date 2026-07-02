"""Probe selectivity matrix helpers for common xylazine interferents."""

from __future__ import annotations

import pandas as pd

from azai.xylazine.selectivity import interferent_risk_table


def probe_interferent_matrix(probe_selectivity_score: float = 62.0) -> pd.DataFrame:
    """Combine probe-level selectivity score with molecule-level interferent risks.

    The returned risk index is a triage heuristic for planning analytical controls,
    not a validated selectivity model.
    """

    table = interferent_risk_table().copy()
    vulnerability = max(0.0, min(1.0, (100.0 - probe_selectivity_score) / 100.0))
    table["probe_vulnerability"] = round(vulnerability, 3)
    table["probe_adjusted_risk"] = (table["combined_selectivity_risk"] * (0.65 + vulnerability)).round(1)
    table["recommended_control_priority"] = pd.cut(
        table["probe_adjusted_risk"],
        bins=[-1, 35, 55, 10_000],
        labels=["routine", "important", "critical"],
    ).astype(str)
    return table.sort_values("probe_adjusted_risk", ascending=False).reset_index(drop=True)
