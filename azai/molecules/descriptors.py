"""RDKit-based molecular descriptor calculation for AZAI."""

from dataclasses import asdict, dataclass
from typing import Any

from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors

from azai.molecules.standardize import mol_from_smiles


@dataclass(frozen=True)
class MolecularDescriptors:
    """Transparent descriptor set used by AZAI baseline chemistry modules."""

    smiles: str
    canonical_smiles: str
    molecular_formula: str
    molecular_weight: float
    exact_mol_weight: float
    logp: float
    molar_refractivity: float
    tpsa: float
    hbond_donors: int
    hbond_acceptors: int
    rotatable_bonds: int
    formal_charge: int
    aromatic_rings: int
    aliphatic_rings: int
    saturated_rings: int
    total_rings: int
    heteroatoms: int
    heavy_atoms: int
    fraction_csp3: float
    qed: float


def calculate_descriptors(smiles: str) -> dict[str, float | int | str]:
    """Calculate a transparent set of medicinal chemistry descriptors."""
    mol = mol_from_smiles(smiles)
    desc = MolecularDescriptors(
        smiles=smiles,
        canonical_smiles=Chem.MolToSmiles(mol, isomericSmiles=True),
        molecular_formula=rdMolDescriptors.CalcMolFormula(mol),
        molecular_weight=round(Descriptors.MolWt(mol), 3),
        exact_mol_weight=round(Descriptors.ExactMolWt(mol), 5),
        logp=round(Crippen.MolLogP(mol), 3),
        molar_refractivity=round(Crippen.MolMR(mol), 3),
        tpsa=round(rdMolDescriptors.CalcTPSA(mol), 3),
        hbond_donors=Lipinski.NumHDonors(mol),
        hbond_acceptors=Lipinski.NumHAcceptors(mol),
        rotatable_bonds=Lipinski.NumRotatableBonds(mol),
        formal_charge=sum(atom.GetFormalCharge() for atom in mol.GetAtoms()),
        aromatic_rings=rdMolDescriptors.CalcNumAromaticRings(mol),
        aliphatic_rings=rdMolDescriptors.CalcNumAliphaticRings(mol),
        saturated_rings=rdMolDescriptors.CalcNumSaturatedRings(mol),
        total_rings=rdMolDescriptors.CalcNumRings(mol),
        heteroatoms=Lipinski.NumHeteroatoms(mol),
        heavy_atoms=mol.GetNumHeavyAtoms(),
        fraction_csp3=round(rdMolDescriptors.CalcFractionCSP3(mol), 3),
        qed=round(Descriptors.qed(mol), 3),
    )
    return asdict(desc)


def descriptor_vector(smiles: str, keys: list[str] | None = None) -> list[float]:
    """Return numeric descriptor vector for similarity and baseline modeling."""
    desc = calculate_descriptors(smiles)
    selected = keys or [
        "molecular_weight",
        "logp",
        "tpsa",
        "hbond_donors",
        "hbond_acceptors",
        "rotatable_bonds",
        "formal_charge",
        "aromatic_rings",
        "heteroatoms",
        "fraction_csp3",
    ]
    return [float(desc[k]) for k in selected]


def rule_of_five_flags(smiles: str) -> dict[str, Any]:
    """Compute Lipinski-style rule-of-five flags without treating them as pass/fail truth."""
    d = calculate_descriptors(smiles)
    flags = {
        "mw_le_500": float(d["molecular_weight"]) <= 500,
        "logp_le_5": float(d["logp"]) <= 5,
        "hbd_le_5": int(d["hbond_donors"]) <= 5,
        "hba_le_10": int(d["hbond_acceptors"]) <= 10,
    }
    return {"flags": flags, "violations": [name for name, ok in flags.items() if not ok]}


def medicinal_interpretation(descriptors: dict[str, float | int | str]) -> list[str]:
    """Generate conservative descriptor-based interpretation statements."""
    notes: list[str] = []
    logp = float(descriptors["logp"])
    tpsa = float(descriptors["tpsa"])
    hba = int(descriptors["hbond_acceptors"])
    charge = int(descriptors["formal_charge"])

    if logp > 3:
        notes.append("Moderately lipophilic; aqueous assay design may require solubility checks.")
    else:
        notes.append("Lipophilicity is not extreme by simple descriptor screening.")
    if tpsa < 60:
        notes.append("Low-to-moderate TPSA suggests limited polarity and possible membrane permeability.")
    if hba > 0:
        notes.append("H-bond acceptors and basic heteroatoms may support recognition by acidic or H-bond donor motifs.")
    if charge == 0:
        notes.append("Neutral formal charge does not exclude protonation under assay-relevant pH conditions.")
    notes.append("Interpretation is descriptor-based and should be validated experimentally.")
    return notes
