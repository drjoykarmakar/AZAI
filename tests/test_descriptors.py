from azai.molecules.descriptors import calculate_descriptors
from azai.xylazine.reference import XYLAZINE


def test_xylazine_descriptors_are_reasonable():
    desc = calculate_descriptors(XYLAZINE.smiles)
    assert desc["molecular_weight"] > 200
    assert desc["hbond_acceptors"] >= 1
    assert desc["aromatic_rings"] >= 1
