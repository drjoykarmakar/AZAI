"""Xylazine reference molecule and profile generation."""

from dataclasses import dataclass

from azai.molecules.descriptors import calculate_descriptors, medicinal_interpretation


@dataclass(frozen=True)
class ReferenceMolecule:
    name: str
    smiles: str
    description: str


XYLAZINE = ReferenceMolecule(
    name="xylazine",
    smiles="Cc1cccc(C)c1NC(=N)N2CCCCC2",
    description="Alpha-2 adrenergic agonist used in veterinary medicine; analyzed here for detection-oriented chemistry.",
)


def xylazine_profile() -> dict[str, object]:
    """Return descriptor profile and conservative interpretation for xylazine."""
    descriptors = calculate_descriptors(XYLAZINE.smiles)
    return {
        "name": XYLAZINE.name,
        "smiles": XYLAZINE.smiles,
        "description": XYLAZINE.description,
        "descriptors": descriptors,
        "functional_group_alerts": [
            "basic amidine/guanidine-like motif",
            "tertiary cyclic amine character",
            "substituted aromatic ring",
            "protonation-state-sensitive recognition likely",
        ],
        "interpretation": medicinal_interpretation(descriptors),
    }
