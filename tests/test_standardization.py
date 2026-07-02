import pytest

from azai.molecules.standardize import canonical_smiles, mol_from_smiles


def test_valid_smiles_loads():
    assert mol_from_smiles("CCO") is not None
    assert canonical_smiles("OCC") == "CCO"


def test_invalid_smiles_raises():
    with pytest.raises(ValueError):
        mol_from_smiles("not-a-smiles")
