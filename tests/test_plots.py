import pandas as pd

from azai.molecules.plots import similarity_bar_chart


def test_similarity_bar_chart_uses_current_similarity_column():
    df = pd.DataFrame(
        {
            "label": ["xylazine", "candidate"],
            "smiles": ["Cc1cccc(C)c1NC(=N)N1CCCCC1", "CCN"],
            "morgan_tanimoto": [1.0, 0.25],
        }
    )

    fig = similarity_bar_chart(df)

    assert fig.data[0].y[0] == 1.0


def test_similarity_bar_chart_falls_back_to_aggregate_score():
    df = pd.DataFrame(
        {
            "label": ["candidate"],
            "smiles": ["CCN"],
            "azai_similarity_score": [0.42],
        }
    )

    fig = similarity_bar_chart(df, score_column="missing_column")

    assert fig.data[0].y[0] == 0.42
