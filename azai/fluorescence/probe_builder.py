"""Rule-based fluorescent probe concept generation for AZAI."""

from __future__ import annotations

from dataclasses import asdict, dataclass

from azai.fluorescence.experiment_plan import recommended_experiment_plan
from azai.fluorescence.fluorophores import FLUOROPHORES
from azai.fluorescence.linkers import LINKERS
from azai.fluorescence.recognition import RECOGNITION_MOTIFS
from azai.fluorescence.spectra import fluorophore_spectral_window, optical_priority_label
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
    spectral_window: str
    optical_priority: str
    synthetic_feasibility: str
    selectivity_concern: str
    total_score: float
    confidence: str
    next_experiment: str


RECOGNITION_GROUPS: tuple[str, ...] = tuple(motif.name for motif in RECOGNITION_MOTIFS)


def _best_mechanism(fluorophore: str, compatible: tuple[str, ...] = ()) -> str:
    mechanisms = list(FLUOROPHORES[fluorophore].get("mechanisms", []))
    preferred = ["PET", "ICT", "turn-on fluorescence", "ratiometric response", "aggregation-induced emission"]
    compatible_set = set(compatible)
    for item in preferred:
        if item in mechanisms and (not compatible_set or item in compatible_set):
            return item
    for item in mechanisms:
        if not compatible_set or item in compatible_set:
            return str(item)
    return mechanisms[0] if mechanisms else "turn-on fluorescence"


def _linker_for_fluorophore(fluorophore: str, rank: int) -> object:
    common = list(FLUOROPHORES[fluorophore].get("common_linkers", []))
    for common_name in common:
        for linker in LINKERS:
            if linker.name.lower() in str(common_name).lower() or str(common_name).lower() in linker.name.lower():
                return linker
    return LINKERS[rank % len(LINKERS)]


def generate_probe_concepts(limit: int = 16) -> list[dict[str, object]]:
    """Generate ranked, transparent fluorescent probe hypotheses.

    The output is intended for research planning and literature review. Scores are
    heuristic prioritization values, not experimentally validated predictions.
    """

    concepts: list[GeneratedProbeConcept] = []
    for fluorophore, meta in FLUOROPHORES.items():
        for motif_index, motif in enumerate(RECOGNITION_MOTIFS):
            mechanism = _best_mechanism(fluorophore, motif.compatible_mechanisms)
            linker = _linker_for_fluorophore(fluorophore, motif_index)
            hypothesis = (
                f"Xylazine contains {', '.join(motif.target_features)}; the '{motif.name}' motif is a testable "
                "analytical recognition hypothesis rather than a validated binding claim."
            )
            concept = ProbeConcept(fluorophore, motif.name, linker.name, mechanism, hypothesis)
            score = score_probe_concept(
                concept,
                meta,
                motif_prior=motif.score_prior,
                linker_accessibility=linker.synthetic_accessibility,
            )
            spectrum = fluorophore_spectral_window(fluorophore)
            plan = recommended_experiment_plan(
                float(score["total_score"]),
                mechanism,
                "; ".join(motif.selectivity_risks),
            )
            generated = GeneratedProbeConcept(
                fluorophore=fluorophore,
                recognition_group=motif.name,
                linker=linker.name,
                mechanism=mechanism,
                xylazine_interaction_hypothesis=hypothesis,
                predicted_optical_behavior=(
                    f"Likely {mechanism}-associated signal modulation; validate with pH-controlled titration."
                ),
                spectral_window=f"Ex {spectrum['typical_excitation_nm']} / Em {spectrum['typical_emission_nm']}",
                optical_priority=optical_priority_label(fluorophore),
                synthetic_feasibility="higher" if float(score["component_scores"]["synthetic_accessibility"]) >= 72 else "moderate",
                selectivity_concern="; ".join(motif.selectivity_risks),
                total_score=float(score["total_score"]),
                confidence=str(score["confidence"]),
                next_experiment=plan[2],
            )
            concepts.append(generated)
    ranked = sorted((asdict(item) for item in concepts), key=lambda row: row["total_score"], reverse=True)
    return ranked[:limit]


def generate_probe_candidates(target_smiles: str | None = None, max_candidates: int = 16) -> list[dict[str, object]]:
    """Compatibility wrapper for target-aware probe generation.

    The v0.8.0 API accepts a target SMILES for future expansion. The current
    heuristic engine is xylazine-focused and uses the target only as explicit
    user context; no unsupported target-specific performance claims are made.
    """
    candidates = generate_probe_concepts(limit=max_candidates)
    for candidate in candidates:
        candidate["target_smiles"] = target_smiles or "xylazine-focused reference context"
    return candidates
