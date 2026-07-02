"""Transparent drug-likeness and assay-friendliness utilities."""

from azai.molecules.descriptors import calculate_descriptors, rule_of_five_flags


def assay_friendliness_score(smiles: str) -> dict[str, object]:
    """Return a simple 0-100 score for early analytical assay tractability."""
    d = calculate_descriptors(smiles)
    score = 100
    penalties: list[str] = []
    if float(d["logp"]) > 4:
        score -= 20
        penalties.append("high logP may reduce aqueous compatibility")
    if float(d["tpsa"]) > 140:
        score -= 15
        penalties.append("very high TPSA may complicate membrane or partitioning assumptions")
    if int(d["rotatable_bonds"]) > 10:
        score -= 10
        penalties.append("many rotatable bonds may increase conformational uncertainty")
    score -= 10 * len(rule_of_five_flags(smiles)["violations"])
    return {"score": max(score, 0), "penalties": penalties, "descriptors": d}
