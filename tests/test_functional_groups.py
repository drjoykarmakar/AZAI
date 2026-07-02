from azai.molecules.functional_groups import detect_functional_groups, present_functional_groups
from azai.xylazine.reference import XYLAZINE


def test_xylazine_functional_group_detection():
    groups = detect_functional_groups(XYLAZINE.smiles)
    assert groups["aromatic_ring"] >= 1
    assert "basic_nitrogen" in present_functional_groups(XYLAZINE.smiles)
