"""Similarity search utilities."""

import pandas as pd

from azai.molecules.descriptors import calculate_descriptors
from azai.molecules.fingerprints import maccs_fingerprint, morgan_fingerprint, tanimoto


def tanimoto_to_reference(smiles: str, reference_smiles: str) -> dict[str, float]:
    """Calculate Morgan and MACCS Tanimoto similarity to a reference molecule."""
    return {
        "morgan_tanimoto": round(tanimoto(morgan_fingerprint(smiles), morgan_fingerprint(reference_smiles)), 4),
        "maccs_tanimoto": round(tanimoto(maccs_fingerprint(smiles), maccs_fingerprint(reference_smiles)), 4),
    }


def rank_by_similarity(smiles_values: list[str], reference_smiles: str) -> pd.DataFrame:
    """Rank SMILES strings by similarity to a reference molecule."""
    rows = []
    ref_desc = calculate_descriptors(reference_smiles)
    for smiles in smiles_values:
        try:
            sim = tanimoto_to_reference(smiles, reference_smiles)
            desc = calculate_descriptors(smiles)
            descriptor_distance = abs(float(desc["molecular_weight"]) - float(ref_desc["molecular_weight"])) / 300
            score = 0.55 * sim["morgan_tanimoto"] + 0.35 * sim["maccs_tanimoto"] + 0.10 * max(0, 1 - descriptor_distance)
            rows.append({"smiles": smiles, **sim, "descriptor_distance": round(descriptor_distance, 4), "azai_similarity_score": round(score, 4)})
        except ValueError as exc:
            rows.append({"smiles": smiles, "error": str(exc), "azai_similarity_score": 0.0})
    return pd.DataFrame(rows).sort_values("azai_similarity_score", ascending=False)
