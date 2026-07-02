from azai.xylazine.selectivity import descriptor_overlap_risk, interferent_risk_table


def test_descriptor_overlap_risk_range():
    risk = descriptor_overlap_risk("CCN(CC)CC")
    assert 0 <= risk <= 100


def test_interferent_risk_table_columns():
    df = interferent_risk_table()
    assert not df.empty
    assert "combined_selectivity_risk" in df.columns
    assert df["combined_selectivity_risk"].iloc[0] >= df["combined_selectivity_risk"].iloc[-1]
