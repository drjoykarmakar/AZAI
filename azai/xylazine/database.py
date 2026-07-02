"""Small curated reference records for xylazine-focused analytical chemistry.

The MVP database is intentionally compact and transparent. Entries are provided as
starting points for cheminformatics demos, not as a validated forensic database.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd


@dataclass(frozen=True)
class ReferenceMolecule:
    """A lightweight reference molecule record."""

    name: str
    smiles: str
    category: str
    role: str
    note: str


REFERENCE_MOLECULES: tuple[ReferenceMolecule, ...] = (
    ReferenceMolecule(
        "xylazine",
        "Cc1cccc(C)c1NC(=N)N1CCCCC1",
        "target",
        "xylazine reference",
        "Primary target molecule for detection-oriented AZAI workflows.",
    ),
    ReferenceMolecule(
        "lidocaine",
        "CCN(CC)CC(=O)NC1=C(C=CC=C1C)C",
        "interferent",
        "local anesthetic",
        "Basic amide-containing interferent relevant to analytical selectivity screens.",
    ),
    ReferenceMolecule(
        "ketamine",
        "CNC1(CCCCC1=O)c1ccccc1Cl",
        "interferent",
        "dissociative anesthetic",
        "Contains a basic amine and hydrophobic aromatic features.",
    ),
    ReferenceMolecule(
        "clonidine",
        "C1=CC(=C(C(=C1)Cl)NC2=NCCN2)Cl",
        "analog_or_interferent",
        "alpha-2 agonist comparator",
        "Pharmacology-adjacent comparator with imidazoline-like recognition concerns.",
    ),
    ReferenceMolecule(
        "dexmedetomidine",
        "CC1=CC(=C(C=C1)C(C)C2=CN=CN2)C",
        "analog_or_interferent",
        "alpha-2 agonist comparator",
        "Useful comparator for selectivity risk and alpha-2 agonist chemical space.",
    ),
    ReferenceMolecule(
        "naloxone",
        "C=CCN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O",
        "interferent",
        "opioid antagonist",
        "Public-health relevant comparator for mixture analysis contexts.",
    ),
    ReferenceMolecule(
        "morphine",
        "CN1CCC23C4C1CC5=C2C(=C(C=C5)O)OC3C(C=C4)O",
        "interferent",
        "opioid alkaloid",
        "Polycyclic phenolic amine comparator; included for descriptor-space contrast.",
    ),
)


def reference_table() -> pd.DataFrame:
    """Return the AZAI reference molecule table."""
    return pd.DataFrame([record.__dict__ for record in REFERENCE_MOLECULES])


def reference_smiles_by_category(category: str) -> pd.DataFrame:
    """Filter reference molecules by exact category."""
    table = reference_table()
    return table[table["category"].eq(category)].reset_index(drop=True)
