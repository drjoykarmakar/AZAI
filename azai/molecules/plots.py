"""Plotly visualization helpers for molecular descriptor dashboards."""

from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def descriptor_radar(descriptors: dict[str, float]) -> go.Figure:
    """Create a simple radar chart for selected molecular descriptors."""

    keys = ["molecular_weight", "logp", "tpsa", "hbd", "hba", "rotatable_bonds"]
    scales = {
        "molecular_weight": 500.0,
        "logp": 7.0,
        "tpsa": 160.0,
        "hbd": 5.0,
        "hba": 10.0,
        "rotatable_bonds": 12.0,
    }
    values = [min(float(descriptors.get(key, 0.0)) / scales[key], 1.0) for key in keys]
    fig = go.Figure(data=go.Scatterpolar(r=values + [values[0]], theta=keys + [keys[0]], fill="toself"))
    fig.update_layout(height=420, polar={"radialaxis": {"visible": True, "range": [0, 1]}}, showlegend=False)
    return fig


def similarity_bar_chart(df: pd.DataFrame, score_column: str = "morgan_tanimoto") -> go.Figure:
    """Create a bar chart for similarity ranking output.

    The similarity API has used a few column names across AZAI releases.
    This helper accepts the current canonical name and gracefully falls back
    to older or aggregate score columns so the Streamlit app does not crash
    when loaded with saved/example outputs from another version.
    """

    plot_df = df.copy().head(20)
    if "label" not in plot_df.columns:
        plot_df["label"] = [f"Mol {idx + 1}" for idx in range(len(plot_df))]

    fallback_columns = [
        score_column,
        "morgan_tanimoto",
        "azai_similarity_score",
        "tanimoto_morgan",
        "maccs_tanimoto",
        "descriptor_similarity",
    ]
    y_column = next((column for column in fallback_columns if column in plot_df.columns), None)
    if y_column is None:
        raise ValueError(
            "No similarity score column found. Expected one of: "
            + ", ".join(dict.fromkeys(fallback_columns))
        )

    return px.bar(plot_df, x="label", y=y_column, hover_data=[col for col in ["smiles"] if col in plot_df.columns])
