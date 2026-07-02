"""Reference interferent panel for xylazine detection studies.

The structures are provided for analytical selectivity triage and cheminformatics
comparison only. They are not intended for synthesis or pharmacological
optimization.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Interferent:
    """A molecular interferent that may complicate analytical detection."""

    name: str
    smiles: str
    category: str
    rationale: str


INTERFERENTS: tuple[Interferent, ...] = (
    Interferent("fentanyl", "CCC(=O)N(C1CCN(CC1)CCC2=CC=CC=C2)C3=CC=CC=C3", "opioid", "Basic tertiary amine and aromatic groups may overlap with broad amine-recognition probes."),
    Interferent("ketamine", "CNC1(CCCCC1=O)C2=CC=CC=C2Cl", "arylcyclohexylamine", "Secondary amine and aromatic chlorophenyl group may create descriptor overlap."),
    Interferent("lidocaine", "CCN(CC)CC(=O)NC1=C(C=CC=C1C)C", "local anesthetic", "Tertiary amine plus dimethyl anilide motif can mimic basic amphiphilic analytes."),
    Interferent("cocaine", "CN1C2CCC1CC(C2)OC(=O)C(C3=CC=CC=C3)OC(=O)C", "alkaloid", "Tertiary amine and ester-rich structure can interfere with charge-based sensors."),
    Interferent("morphine", "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O", "opioid alkaloid", "Basic amine and phenolic H-bonding may contribute to nonspecific binding."),
    Interferent("naloxone", "C=CCN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(=O)CC4O", "opioid antagonist", "Polyfunctional basic scaffold may challenge selectivity assays."),
    Interferent("clonidine", "C1=CC(=C(C(=C1)Cl)NC2=NCCN2)Cl", "alpha-2 agonist", "Imidazoline-like alpha-2 agonist with aromatic chlorides; pharmacophore overlap concern."),
    Interferent("dexmedetomidine", "CC1=C(C(=CC=C1)C)C(C)N2C=NC=C2", "alpha-2 agonist", "Basic imidazole-containing alpha-2 agonist; relevant selectivity comparator."),
    Interferent("triethylamine", "CCN(CC)CC", "common amine", "Small tertiary amine control for pH and nonspecific amine response."),
)


def interferent_smiles() -> list[str]:
    """Return interferent SMILES strings."""

    return [item.smiles for item in INTERFERENTS]


def interferent_names() -> list[str]:
    """Return interferent names in reference order."""

    return [item.name for item in INTERFERENTS]
