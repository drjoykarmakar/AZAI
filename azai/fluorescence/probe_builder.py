"""Rule-based fluorescent probe concept generation for AZAI."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from azai.fluorescence.fluorophores import FLUOROPHORES
from azai.scoring.probe_score import ProbeConcept, score_probe_concept


@dataclass(frozen=True)
class GeneratedProbeConcept:
    """A transparent probe hypothesis generated from simple chemical rules."""

    fluorophore: str
    recognition_group: str
    linker: str
    mechanism: str
    xylazine_interaction_hypothesis: str
    predicted_optical_behavior: str
    synthetic_feasibility: str
    selectivity_concern: str
    total_score: float
    confidence: str


RECOGNITION_GROUPS: tuple[str, ...] = (
    "acidic H-bond donor / protonated-amine recognition motif",
    "aryl-sulfonamide environment-sensitive amine-recognition motif",
    "boronic-acid-adjacent polar recognition motif",
    "crown-ether-inspired cation microenvironment motif",
)


def _best_mechanism(fluorophore: str) -> str:
    mechanisms = list(FLUOROPHORES[fluorophore].get("mechanisms", []))
    preferred = ["PET", "ICT", "turn-on fluorescence", "ratiometric response"]
    for item in preferred:
        if item in mechanisms:
            return item
    return mechanisms[0] if mechanisms else "turn-on fluorescence"


def generate_probe_concepts(limit: int = 12) -> list[dict[str, object]]:
    """Generate ranked, transparent fluorescent probe hypotheses.

    The output is intended for research planning and literature review. Scores are
    heuristic prioritization values, not experimentally validated predictions.
    """

    concepts: list[GeneratedProbeConcept] = []
    for fluorophore, meta in FLUOROPHORES.items():
        mechanism = _best_mechanism(fluorophore)
        linker = str(list(meta.get("common_linkers", ["short alkyl linker"]))[0])
        recognition = RECOGNITION_GROUPS[0]
        hypothesis = (
            "Xylazine contains a basic heterocyclic amine and an aromatic imino-thiourea-like motif; "
            "a protonation-state-sensitive recognition environment may produce a measurable optical response."
        )
        concept = ProbeConcept(fluorophore, recognition, linker, mechanism, hypothesis)
        score = score_probe_concept(concept, meta)
        generated = GeneratedProbeConcept(
            fluorophore=fluorophore,
            recognition_group=recognition,
            linker=linker,
            mechanism=mechanism,
            xylazine_interaction_hypothesis=hypothesis,
            predicted_optical_behavior=(
                f"Likely {mechanism}-associated signal modulation; validate with pH-controlled titration."
            ),
            synthetic_feasibility=(
                "higher" if float(meta.get("synthetic_accessibility", 0.5)) >= 0.7 else "moderate"
            ),
            selectivity_concern="Basic amines and alpha-2 agonist analogs may cause nonspecific response.",
            total_score=float(score["total_score"]),
            confidence=str(score["confidence"]),
        )
        concepts.append(generated)
    ranked = sorted((asdict(item) for item in concepts), key=lambda row: row["total_score"], reverse=True)
    return ranked[:limit]
