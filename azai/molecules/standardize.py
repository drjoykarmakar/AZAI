"""Molecule loading and standardization helpers."""

from rdkit import Chem


def mol_from_smiles(smiles: str) -> Chem.Mol:
    """Parse a SMILES string into an RDKit molecule.

    Raises:
        ValueError: If the SMILES cannot be parsed.
    """
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"Invalid SMILES: {smiles}")
    return mol


def canonical_smiles(smiles: str) -> str:
    """Return canonical isomeric SMILES."""
    return Chem.MolToSmiles(mol_from_smiles(smiles), isomericSmiles=True)
