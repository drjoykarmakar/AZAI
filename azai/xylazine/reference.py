"""Xylazine reference molecule and profile generation."""

from dataclasses import dataclass

from azai.molecules.descriptors import calculate_descriptors, medicinal_interpretation, rule_of_five_flags
from azai.molecules.functional_groups import present_functional_groups
from azai.molecules.scaffolds import generic_scaffold_smiles, murcko_scaffold_smiles


@dataclass(frozen=True)
class ReferenceMolecule:
    """Curated reference molecule record."""

    name: str
    smiles: str
    description: str
    category: str = "reference"


XYLAZINE = ReferenceMolecule(
    name="xylazine",
    smiles="Cc1cccc(C)c1NC(=N)N2CCCCC2",
    description=(
        "Alpha-2 adrenergic agonist used in veterinary medicine; analyzed here for "
        "detection-oriented chemistry and molecular characterization."
    ),
)

COMMON_INTERFERENTS: list[ReferenceMolecule] = [
    ReferenceMolecule("fentanyl", "CCC(=O)N(C1CCN(CC1)CCc2ccccc2)c3ccccc3", "Synthetic opioid; example interferent", "interferent"),
    ReferenceMolecule("ketamine", "CN1CCCCC1C(=O)c2ccccc2Cl", "Dissociative anesthetic; example interferent", "interferent"),
    ReferenceMolecule("lidocaine", "CCN(CC)CC(=O)Nc1c(C)cccc1C", "Local anesthetic; tertiary amine-like interferent", "interferent"),
    ReferenceMolecule("cocaine", "COC(=O)C1C(OC(=O)c2ccccc2)CC2CCC1N2C", "Tropane alkaloid; example interferent", "interferent"),
    ReferenceMolecule("morphine", "CN1CCC23c4c5ccc(O)c4OC2C(O)=CC3C1C5", "Opioid alkaloid; example interferent", "interferent"),
    ReferenceMolecule("naloxone", "C=CCN1CCC23c4c5ccc(O)c4OC2C(=O)CC3C1C5O", "Opioid antagonist; example interferent", "interferent"),
    ReferenceMolecule("clonidine", "Clc1cccc(Cl)c1NC1=NCCN1", "Alpha-2 agonist; pharmacophore-related interferent", "interferent"),
    ReferenceMolecule("dexmedetomidine", "CC1=CC=C(C=C1)C2=C(N=C(C)N2)C", "Alpha-2 agonist; pharmacophore-related interferent", "interferent"),
]


def xylazine_profile() -> dict[str, object]:
    """Return descriptor profile and conservative interpretation for xylazine."""
    descriptors = calculate_descriptors(XYLAZINE.smiles)
    return {
        "name": XYLAZINE.name,
        "smiles": XYLAZINE.smiles,
        "description": XYLAZINE.description,
        "descriptors": descriptors,
        "murcko_scaffold": murcko_scaffold_smiles(XYLAZINE.smiles),
        "generic_scaffold": generic_scaffold_smiles(XYLAZINE.smiles),
        "functional_group_alerts": present_functional_groups(XYLAZINE.smiles),
        "rule_of_five": rule_of_five_flags(XYLAZINE.smiles),
        "protonation_relevant_features": [
            "basic nitrogen-containing recognition features may be pH-sensitive",
            "neutral formal charge does not rule out protonated microspecies",
            "aqueous detection assays should define pH and ionic strength",
        ],
        "interpretation": medicinal_interpretation(descriptors),
    }
