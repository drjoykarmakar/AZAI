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


def similarity_bar_chart(df: pd.DataFrame, score_column: str = "tanimoto_morgan") -> go.Figure:
    """Create a bar chart for similarity ranking output."""

    plot_df = df.copy().head(20)
    if "label" not in plot_df.columns:
        plot_df["label"] = [f"Mol {idx + 1}" for idx in range(len(plot_df))]
    return px.bar(plot_df, x="label", y=score_column, hover_data=[col for col in ["smiles"] if col in plot_df.columns])
