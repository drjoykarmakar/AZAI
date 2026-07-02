"""RDKit-based molecular descriptor calculation."""

from dataclasses import asdict, dataclass

from rdkit import Chem
from rdkit.Chem import Crippen, Descriptors, Lipinski, rdMolDescriptors

from azai.molecules.standardize import mol_from_smiles


@dataclass(frozen=True)
class MolecularDescriptors:
    smiles: str
    canonical_smiles: str
    molecular_weight: float
    logp: float
    tpsa: float
    hbond_donors: int
    hbond_acceptors: int
    rotatable_bonds: int
    formal_charge: int
    aromatic_rings: int
    heteroatoms: int
    heavy_atoms: int


def calculate_descriptors(smiles: str) -> dict[str, float | int | str]:
    """Calculate a transparent set of medicinal chemistry descriptors."""
    mol = mol_from_smiles(smiles)
    desc = MolecularDescriptors(
        smiles=smiles,
        canonical_smiles=Chem.MolToSmiles(mol, isomericSmiles=True),
        molecular_weight=round(Descriptors.MolWt(mol), 3),
        logp=round(Crippen.MolLogP(mol), 3),
        tpsa=round(rdMolDescriptors.CalcTPSA(mol), 3),
        hbond_donors=Lipinski.NumHDonors(mol),
        hbond_acceptors=Lipinski.NumHAcceptors(mol),
        rotatable_bonds=Lipinski.NumRotatableBonds(mol),
        formal_charge=sum(atom.GetFormalCharge() for atom in mol.GetAtoms()),
        aromatic_rings=rdMolDescriptors.CalcNumAromaticRings(mol),
        heteroatoms=Lipinski.NumHeteroatoms(mol),
        heavy_atoms=mol.GetNumHeavyAtoms(),
    )
    return asdict(desc)


def medicinal_interpretation(descriptors: dict[str, float | int | str]) -> list[str]:
    """Generate conservative descriptor-based interpretation statements."""
    notes: list[str] = []
    logp = float(descriptors["logp"])
    tpsa = float(descriptors["tpsa"])
    hba = int(descriptors["hbond_acceptors"])

    if logp > 3:
        notes.append("Moderately lipophilic; aqueous assay design may require solubility checks.")
    else:
        notes.append("Lipophilicity is not extreme by simple descriptor screening.")
    if tpsa < 60:
        notes.append("Low-to-moderate TPSA suggests limited polarity and possible membrane permeability.")
    if hba > 0:
        notes.append("H-bond acceptors and basic heteroatoms may support recognition by acidic or H-bond donor motifs.")
    notes.append("Interpretation is descriptor-based and should be validated experimentally.")
    return notes
