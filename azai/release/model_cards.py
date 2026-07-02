"""Model card helpers for transparent AZAI releases."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelCard:
    """Minimal model-card representation."""

    name: str
    version: str
    intended_use: str
    limitations: str
    validation_status: str
    safety_notes: str

    def to_markdown(self) -> str:
        """Render the model card as Markdown."""
        return f"""# Model Card: {self.name}\n\n**Version:** {self.version}\n\n## Intended use\n{self.intended_use}\n\n## Validation status\n{self.validation_status}\n\n## Limitations\n{self.limitations}\n\n## Safety notes\n{safety_prefix()} {self.safety_notes}\n"""


def safety_prefix() -> str:
    """Return the common AZAI model-card safety prefix."""
    return "AZAI is for analytical chemistry, public health, forensic detection, and education."


def heuristic_probe_scorer_card() -> ModelCard:
    """Return the built-in heuristic probe scorer model card."""
    return ModelCard(
        name="Heuristic Fluorescent Probe Scorer",
        version="0.6.0",
        intended_use=(
            "Prioritize fluorescent probe concepts for xylazine detection research using transparent, "
            "rule-based components."
        ),
        validation_status=(
            "Not experimentally validated. Scores are prioritization hypotheses and should be checked "
            "against literature and bench experiments."
        ),
        limitations=(
            "Does not predict quantum yield, binding constants, detection limits, metabolic behavior, "
            "or synthetic success. Component scores are interpretable heuristics."
        ),
        safety_notes="Do not use to optimize harmful delivery, abuse potential, or clandestine synthesis.",
    )
