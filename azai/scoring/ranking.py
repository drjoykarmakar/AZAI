"""Ranking helpers for AZAI scoring outputs."""

import pandas as pd


def rank_records(records: list[dict[str, object]], score_key: str = "total_score") -> pd.DataFrame:
    """Rank dictionaries by a numeric score key."""
    df = pd.DataFrame(records)
    if score_key not in df.columns:
        raise ValueError(f"score key not found: {score_key}")
    return df.sort_values(score_key, ascending=False).reset_index(drop=True)
