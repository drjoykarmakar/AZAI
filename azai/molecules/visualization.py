"""Molecular visualization helpers."""

from rdkit.Chem import Draw

from azai.molecules.standardize import mol_from_smiles


def mol_image(smiles: str, size: tuple[int, int] = (350, 250)):
    """Return a PIL image for a molecule."""
    return Draw.MolToImage(mol_from_smiles(smiles), size=size)
