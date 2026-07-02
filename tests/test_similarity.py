from azai.molecules.similarity import tanimoto_to_reference
from azai.xylazine.reference import XYLAZINE


def test_self_similarity_is_one():
    sim = tanimoto_to_reference(XYLAZINE.smiles, XYLAZINE.smiles)
    assert sim["morgan_tanimoto"] == 1.0
    assert sim["maccs_tanimoto"] == 1.0
