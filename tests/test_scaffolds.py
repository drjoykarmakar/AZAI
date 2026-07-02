from azai.molecules.scaffolds import generic_scaffold_smiles, murcko_scaffold_smiles
from azai.xylazine.reference import XYLAZINE


def test_scaffold_generation_returns_string():
    assert isinstance(murcko_scaffold_smiles(XYLAZINE.smiles), str)
    assert isinstance(generic_scaffold_smiles(XYLAZINE.smiles), str)
