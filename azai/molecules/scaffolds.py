"""Scaffold utilities for analog exploration."""

from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold

from azai.molecules.standardize import mol_from_smiles


def murcko_scaffold_smiles(smiles: str) -> str:
    """Return the Bemis-Murcko scaffold SMILES for a molecule."""
    mol = mol_from_smiles(smiles)
    scaffold = MurckoScaffold.GetScaffoldForMol(mol)
    return Chem.MolToSmiles(scaffold, isomericSmiles=True) if scaffold.GetNumAtoms() else ""


def generic_scaffold_smiles(smiles: str) -> str:
    """Return generic Murcko scaffold with atom and bond types generalized."""
    mol = mol_from_smiles(smiles)
    scaffold = MurckoScaffold.GetScaffoldForMol(mol)
    generic = MurckoScaffold.MakeScaffoldGeneric(scaffold)
    return Chem.MolToSmiles(generic, isomericSmiles=True) if generic.GetNumAtoms() else ""


def same_murcko_scaffold(smiles_a: str, smiles_b: str) -> bool:
    """Return True when two molecules share the same exact Murcko scaffold."""
    return murcko_scaffold_smiles(smiles_a) == murcko_scaffold_smiles(smiles_b)
