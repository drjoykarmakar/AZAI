"""SMARTS-based functional group detection used for transparent alerts."""

from rdkit import Chem

from azai.molecules.standardize import mol_from_smiles

FUNCTIONAL_GROUP_SMARTS: dict[str, str] = {
    "aromatic_ring": "a1aaaaa1",
    "tertiary_amine": "[NX3;H0;!$(NC=O)]",
    "secondary_amine": "[NX3;H1;!$(NC=O)]",
    "basic_nitrogen": "[NX3,NX2;!$(NC=O)]",
    "amidine_or_guanidine_like": "[NX3][CX3](=[NX2,NX3])[NX3,NX2]",
    "amide": "[NX3][CX3](=[OX1])",
    "phenol": "c[OX2H]",
    "carboxylic_acid": "[CX3](=O)[OX2H1]",
    "sulfonamide": "S(=O)(=O)N",
    "halogenated_aromatic": "a[F,Cl,Br,I]",
}


def detect_functional_groups(smiles: str) -> dict[str, int]:
    """Return match counts for built-in functional group SMARTS patterns."""
    mol = mol_from_smiles(smiles)
    out: dict[str, int] = {}
    for name, smarts in FUNCTIONAL_GROUP_SMARTS.items():
        patt = Chem.MolFromSmarts(smarts)
        out[name] = len(mol.GetSubstructMatches(patt)) if patt is not None else 0
    return out


def present_functional_groups(smiles: str) -> list[str]:
    """Return detected functional-group names with nonzero matches."""
    return [name for name, count in detect_functional_groups(smiles).items() if count > 0]
