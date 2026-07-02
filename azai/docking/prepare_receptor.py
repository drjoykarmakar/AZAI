"""Receptor preparation guidance for AZAI.

AZAI does not automatically prepare receptors in the MVP because receptor preparation
requires project-specific choices about biological target, protonation, waters, cofactors,
and docking protocol validation.
"""


def receptor_preparation_checklist() -> list[str]:
    """Return a transparent receptor preparation checklist."""
    return [
        "Choose a biologically justified receptor target and cite the structure source.",
        "Inspect missing residues, cofactors, metals, and crystallographic waters.",
        "Assign protonation states using a documented pH assumption.",
        "Remove or retain waters based on an explicit protocol.",
        "Validate docking protocol with a known ligand when possible.",
        "Record grid center, grid size, exhaustiveness, and software versions.",
    ]
