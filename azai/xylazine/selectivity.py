"""Selectivity triage against common interferents."""

from __future__ import annotations

import pandas as pd

from azai.molecules.descriptors import calculate_descriptors
from azai.molecules.similarity import tanimoto_to_reference
from azai.xylazine.interferents import INTERFERENTS
from azai.xylazine.reference import XYLAZINE

_DESCRIPTOR_KEYS = ("molecular_weight", "logp", "tpsa", "hbond_donors", "hbond_acceptors", "rotatable_bonds")


def descriptor_overlap_risk(smiles: str, reference_smiles: str = XYLAZINE.smiles) -> float:
    """Estimate descriptor overlap risk on a 0-100 scale.

    This is a simple normalized distance heuristic for selectivity triage.
    """

    query = calculate_descriptors(smiles)
    ref = calculate_descriptors(reference_smiles)
    ranges = {
        "molecular_weight": 250.0,
        "logp": 6.0,
        "tpsa": 140.0,
        "hbond_donors": 5.0,
        "hbond_acceptors": 10.0,
        "rotatable_bonds": 12.0,
    }
    distance = 0.0
    for key in _DESCRIPTOR_KEYS:
        distance += min(abs(float(query[key]) - float(ref[key])) / ranges[key], 1.0)
    normalized = distance / len(_DESCRIPTOR_KEYS)
    return round(100.0 * (1.0 - normalized), 1)


def interferent_risk_table(reference_smiles: str = XYLAZINE.smiles) -> pd.DataFrame:
    """Return a ranked table of interferent similarity/selectivity risk."""

    rows: list[dict[str, object]] = []
    for item in INTERFERENTS:
        tanimoto_profile = tanimoto_to_reference(item.smiles, reference_smiles)
        tanimoto = float(tanimoto_profile["morgan_tanimoto"])
        descriptor_risk = descriptor_overlap_risk(item.smiles, reference_smiles)
        combined = round((100.0 * tanimoto * 0.6) + (descriptor_risk * 0.4), 1)
        rows.append(
            {
                "name": item.name,
                "category": item.category,
                "smiles": item.smiles,
                "tanimoto_to_xylazine": round(tanimoto, 3),
                "descriptor_overlap_risk": descriptor_risk,
                "combined_selectivity_risk": combined,
                "rationale": item.rationale,
            }
        )
    return pd.DataFrame(rows).sort_values("combined_selectivity_risk", ascending=False).reset_index(drop=True)
