"""Transparent fluorescent probe scoring."""

from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class ProbeConcept:
    fluorophore: str
    recognition_group: str
    linker: str
    mechanism: str
    xylazine_interaction_hypothesis: str


@dataclass(frozen=True)
class ProbeScore:
    total_score: float
    component_scores: dict[str, float]
    explanation: list[str]
    confidence: str
    recommended_next_experiment: str


def score_probe_concept(concept: ProbeConcept, fluorophore_meta: dict[str, object]) -> dict[str, object]:
    """Score a probe concept with explicit heuristic components.

    The model is intentionally transparent and should be considered hypothesis generation,
    not validated prediction.
    """
    mechanisms = set(fluorophore_meta.get("mechanisms", []))
    recognition = 78.0 if "amine" in concept.recognition_group.lower() or "acid" in concept.recognition_group.lower() else 58.0
    response = 76.0 if concept.mechanism in mechanisms else 55.0
    synthetic = 100 * float(fluorophore_meta.get("synthetic_accessibility", 0.5))
    aqueous = 100 * float(fluorophore_meta.get("water_compatibility", 0.5))
    sensitivity = 70.0 if concept.mechanism in {"PET", "ICT", "turn-on fluorescence"} else 60.0
    selectivity = 62.0 if "amine" in concept.recognition_group.lower() else 68.0
    novelty = 60.0
    safety = 75.0
    interpretability = 85.0

    components = {
        "xylazine_recognition_potential": recognition,
        "fluorescence_response_probability": response,
        "synthetic_accessibility": synthetic,
        "selectivity_vs_interferents": selectivity,
        "aqueous_compatibility": aqueous,
        "expected_sensitivity": sensitivity,
        "novelty": novelty,
        "safety_and_practicality": safety,
        "medicinal_chemistry_interpretability": interpretability,
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
        "Selectivity against other basic amines requires experimental validation.",
        "No claim of analytical performance is made without calibration data.",
    ]
    confidence = "medium" if total >= 70 else "low-to-medium"
    result = ProbeScore(
        total_score=round(total, 1),
        component_scores={k: round(v, 1) for k, v in components.items()},
        explanation=explanation,
        confidence=confidence,
        recommended_next_experiment="Run UV-vis/fluorescence titration with xylazine and interferent panel at relevant pH values.",
    )
    return asdict(result)
