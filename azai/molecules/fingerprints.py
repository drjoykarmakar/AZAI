"""Molecular fingerprint generation."""

from rdkit import DataStructs
from rdkit.Chem import MACCSkeys, rdFingerprintGenerator

from azai.molecules.standardize import mol_from_smiles


def morgan_fingerprint(smiles: str, radius: int = 2, n_bits: int = 2048):
    """Return an RDKit Morgan fingerprint bit vector."""
    generator = rdFingerprintGenerator.GetMorganGenerator(radius=radius, fpSize=n_bits)
    return generator.GetFingerprint(mol_from_smiles(smiles))


def maccs_fingerprint(smiles: str):
    """Return an RDKit MACCS keys fingerprint."""
    return MACCSkeys.GenMACCSKeys(mol_from_smiles(smiles))


def tanimoto(fp_a, fp_b) -> float:
    """Calculate Tanimoto similarity between two RDKit fingerprints."""
    return float(DataStructs.TanimotoSimilarity(fp_a, fp_b))
