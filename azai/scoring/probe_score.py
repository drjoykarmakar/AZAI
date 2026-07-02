"""Transparent fluorescent probe scoring."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ProbeConcept:
    """Minimal probe concept inputs used by the heuristic scorer."""

    fluorophore: str
    recognition_group: str
    linker: str
    mechanism: str
    xylazine_interaction_hypothesis: str


@dataclass(frozen=True)
class ProbeScore:
    """Transparent probe score object."""

    total_score: float
    component_scores: dict[str, float]
    explanation: list[str]
    confidence: str
    recommended_next_experiment: str


def _bounded(value: float, low: float = 0.0, high: float = 100.0) -> float:
    return max(low, min(high, value))


def score_probe_concept(
    concept: ProbeConcept,
    fluorophore_meta: dict[str, object],
    *,
    motif_prior: float | None = None,
    linker_accessibility: float | None = None,
) -> dict[str, object]:
    """Score a probe concept with explicit heuristic components.

    The model is intentionally transparent and should be considered hypothesis
    generation, not validated prediction. Optional motif/linker priors are used
    by the v0.7 probe design engine but default to v0.6-compatible behavior.
    """

    mechanisms = set(fluorophore_meta.get("mechanisms", []))
    text = f"{concept.recognition_group} {concept.xylazine_interaction_hypothesis}".lower()

    motif_bonus = 100.0 * motif_prior if motif_prior is not None else 0.0
    recognition = 58.0
    if any(term in text for term in ["amine", "proton", "cation", "ion-pair"]):
        recognition += 16.0
    if any(term in text for term in ["aromatic", "hydrophobic", "aryl"]):
        recognition += 6.0
    if any(term in text for term in ["h-bond", "hydrogen", "heteroatom"]):
        recognition += 5.0
    if motif_prior is not None:
        recognition = (recognition * 0.7) + (motif_bonus * 0.3)

    response = 76.0 if concept.mechanism in mechanisms else 55.0
    if concept.mechanism in {"PET", "ICT", "ratiometric response", "turn-on fluorescence"}:
        response += 4.0

    synthetic_base = 100 * float(fluorophore_meta.get("synthetic_accessibility", 0.5))
    if linker_accessibility is not None:
        synthetic = (synthetic_base * 0.65) + (100.0 * linker_accessibility * 0.35)
    else:
        synthetic = synthetic_base

    aqueous = 100 * float(fluorophore_meta.get("water_compatibility", 0.5))
    if any(term in concept.linker.lower() for term in ["peg", "sulfon", "carbox", "zwitter"]):
        aqueous += 8.0
    elif any(term in concept.linker.lower() for term in ["alkyl", "aryl", "pyrene"]):
        aqueous -= 8.0

    sensitivity = 70.0 if concept.mechanism in {"PET", "ICT", "turn-on fluorescence"} else 60.0
    if float(fluorophore_meta.get("brightness", 0.5)) >= 0.8:
        sensitivity += 6.0

    selectivity = 64.0
    if "broad" in text or "common amine" in text:
        selectivity -= 6.0
    if "dual" in text or "aryl" in text or "hydrophobic" in text:
        selectivity += 4.0
    if "protonation" in text or "cation" in text:
        selectivity -= 3.0

    novelty = 60.0
    if concept.mechanism in {"ratiometric response", "aggregation-induced emission"}:
        novelty += 8.0
    if concept.fluorophore.lower() in {"bodipy", "naphthalimide", "cyanine"}:
        novelty += 4.0

    safety = 75.0
    if concept.fluorophore.lower() in {"pyrene", "cyanine"}:
        safety -= 5.0

    interpretability = 85.0
    if concept.mechanism in {"PET", "ICT", "turn-on fluorescence", "ratiometric response"}:
        interpretability += 3.0

    components = {
        "xylazine_recognition_potential": _bounded(recognition),
        "fluorescence_response_probability": _bounded(response),
        "synthetic_accessibility": _bounded(synthetic),
        "selectivity_vs_interferents": _bounded(selectivity),
        "aqueous_compatibility": _bounded(aqueous),
        "expected_sensitivity": _bounded(sensitivity),
        "novelty": _bounded(novelty),
        "safety_and_practicality": _bounded(safety),
        "medicinal_chemistry_interpretability": _bounded(interpretability),
    }
    weights = {
        "xylazine_recognition_potential": 0.18,
        "fluorescence_response_probability": 0.17,
        "synthetic_accessibility": 0.12,
        "selectivity_vs_interferents": 0.13,
        "aqueous_compatibility": 0.10,
        "expected_sensitivity": 0.10,
        "novelty": 0.07,
        "safety_and_practicality": 0.06,
        "medicinal_chemistry_interpretability": 0.07,
    }
    total = sum(components[k] * weights[k] for k in weights)
    explanation = [
        f"{concept.fluorophore} was scored using transparent heuristic rules.",
        f"Recognition hypothesis: {concept.xylazine_interaction_hypothesis}",
        f"Mechanism compatibility considered: {concept.mechanism}.",
        "Selectivity against other basic amines requires experimental validation.",
        "No claim of analytical performance is made without calibration data.",
    ]
    confidence = "medium" if total >= 72 else "low-to-medium"
    result = ProbeScore(
        total_score=round(total, 1),
        component_scores={k: round(v, 1) for k, v in components.items()},
        explanation=explanation,
        confidence=confidence,
        recommended_next_experiment="Run UV-vis/fluorescence titration with xylazine and interferent panel at relevant pH values.",
    )
    return asdict(result)
