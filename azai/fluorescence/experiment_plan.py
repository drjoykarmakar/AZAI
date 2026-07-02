"""Experiment prioritization helpers for AZAI probe hypotheses."""

from __future__ import annotations


def recommended_experiment_plan(score: float, mechanism: str, selectivity_risk: str) -> list[str]:
    """Return a concise staged experiment plan for a probe concept.

    This function proposes analytical validation steps only. It does not provide
    synthesis instructions or optimize pharmacological activity.
    """

    plan = [
        "Prepare a literature review table for the fluorophore, mechanism, and recognition motif.",
        "Run buffered blank, pH-only, and solvent-ratio controls before analyte testing.",
        "Perform UV-vis and fluorescence titration with xylazine reference material under documented analytical conditions.",
    ]
    if mechanism in {"PET", "ICT", "ratiometric response"}:
        plan.append("Collect excitation/emission scans to distinguish intensity-only artifacts from spectral shifts.")
    if "amine" in selectivity_risk.lower() or score < 72:
        plan.append("Screen the interferent panel early, especially common amines and alpha-2 agonist analogs.")
    else:
        plan.append("Proceed to a small matrix-tolerance screen after confirming signal linearity.")
    plan.append("Document limits: heuristic score, no validated sensitivity/selectivity until calibration data exist.")
    return plan
