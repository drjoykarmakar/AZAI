"""Similarity search utilities."""

import math

import pandas as pd

from azai.molecules.descriptors import calculate_descriptors, descriptor_vector
from azai.molecules.fingerprints import maccs_fingerprint, morgan_fingerprint, tanimoto
from azai.molecules.functional_groups import present_functional_groups
from azai.molecules.scaffolds import generic_scaffold_smiles, murcko_scaffold_smiles


def tanimoto_to_reference(smiles: str, reference_smiles: str) -> dict[str, float]:
    """Calculate Morgan and MACCS Tanimoto similarity to a reference molecule."""
    return {
        "morgan_tanimoto": round(
            tanimoto(morgan_fingerprint(smiles), morgan_fingerprint(reference_smiles)), 4
        ),
        "maccs_tanimoto": round(tanimoto(maccs_fingerprint(smiles), maccs_fingerprint(reference_smiles)), 4),
    }


def descriptor_similarity(smiles: str, reference_smiles: str) -> float:
    """Return a bounded descriptor-overlap score using a scaled Euclidean distance."""
    a = descriptor_vector(smiles)
    b = descriptor_vector(reference_smiles)
    scales = [300.0, 5.0, 120.0, 5.0, 10.0, 10.0, 3.0, 5.0, 10.0, 1.0]
    dist = math.sqrt(sum(((x - y) / s) ** 2 for x, y, s in zip(a, b, scales, strict=True)))
    return round(1 / (1 + dist), 4)


def functional_group_similarity(smiles: str, reference_smiles: str) -> float:
    """Return Jaccard similarity over detected functional-group labels."""
    a = set(present_functional_groups(smiles))
    b = set(present_functional_groups(reference_smiles))
    if not a and not b:
        return 1.0
    return round(len(a & b) / len(a | b), 4) if (a | b) else 0.0


def scaffold_similarity(smiles: str, reference_smiles: str) -> float:
    """Return a simple scaffold similarity flag with generic scaffold fallback."""
    scaffold = murcko_scaffold_smiles(smiles)
    ref_scaffold = murcko_scaffold_smiles(reference_smiles)
    if scaffold and scaffold == ref_scaffold:
        return 1.0
    generic = generic_scaffold_smiles(smiles)
    ref_generic = generic_scaffold_smiles(reference_smiles)
    if generic and generic == ref_generic:
        return 0.7
    return 0.0


def similarity_profile(smiles: str, reference_smiles: str) -> dict[str, float | str]:
    """Return all similarity components used by AZAI ranking."""
    sim = tanimoto_to_reference(smiles, reference_smiles)
    sim["descriptor_similarity"] = descriptor_similarity(smiles, reference_smiles)
    sim["functional_group_similarity"] = functional_group_similarity(smiles, reference_smiles)
    sim["scaffold_similarity"] = scaffold_similarity(smiles, reference_smiles)
    score = (
        0.45 * sim["morgan_tanimoto"]
        + 0.25 * sim["maccs_tanimoto"]
        + 0.15 * sim["descriptor_similarity"]
        + 0.10 * sim["functional_group_similarity"]
        + 0.05 * sim["scaffold_similarity"]
    )
    return {**sim, "azai_similarity_score": round(score, 4)}


def rank_by_similarity(smiles_values: list[str], reference_smiles: str) -> pd.DataFrame:
    """Rank SMILES strings by similarity to a reference molecule."""
    rows = []
    for smiles in smiles_values:
        try:
            desc = calculate_descriptors(smiles)
            rows.append(
                {
                    "smiles": smiles,
                    "canonical_smiles": desc["canonical_smiles"],
                    **similarity_profile(smiles, reference_smiles),
                }
            )
        except ValueError as exc:
            rows.append({"smiles": smiles, "error": str(exc), "azai_similarity_score": 0.0})
    return pd.DataFrame(rows).sort_values("azai_similarity_score", ascending=False)
