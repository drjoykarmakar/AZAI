"""General chemistry checks for AZAI."""

from azai.molecules.descriptors import calculate_descriptors, rule_of_five_flags
from azai.molecules.functional_groups import present_functional_groups


def molecule_quality_summary(smiles: str) -> dict[str, object]:
    """Return a conservative molecule-quality summary for early screening."""
    desc = calculate_descriptors(smiles)
    return {
        "canonical_smiles": desc["canonical_smiles"],
        "rule_of_five": rule_of_five_flags(smiles),
        "functional_groups": present_functional_groups(smiles),
        "notes": [
            "These checks are heuristic and do not replace experimental characterization.",
            "Use results for triage, not as validated safety or efficacy claims.",
        ],
    }
