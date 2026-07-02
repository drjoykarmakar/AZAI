"""Markdown report generation for AZAI analyses."""

from collections.abc import Sequence
from datetime import UTC, datetime

import pandas as pd

from azai.molecules.descriptors import calculate_descriptors, medicinal_interpretation
from azai.xylazine.reference import XYLAZINE

SAFETY_TEXT = (
    "AZAI is for analytical chemistry, public health research, molecular characterization, "
    "fluorescent probe discovery, and medicinal chemistry education. It must not be used to "
    "optimize xylazine potency, abuse potential, harmful delivery, clandestine synthesis, or "
    "illicit drug production. Scores are computational hypotheses unless experimentally validated."
)


def descriptor_markdown(smiles: str) -> str:
    """Return a Markdown table of descriptors."""
    desc = calculate_descriptors(smiles)
    rows = ["| Descriptor | Value |", "|---|---:|"]
    for key, value in desc.items():
        rows.append(f"| {key} | {value} |")
    return "\n".join(rows)


def generate_markdown_report(
    smiles: str,
    title: str = "AZAI Molecular Intelligence Report",
    similarity_results: pd.DataFrame | None = None,
    probe_rows: Sequence[dict[str, object]] | None = None,
) -> str:
    """Create a conservative scientific Markdown report."""
    desc = calculate_descriptors(smiles)
    notes = medicinal_interpretation(desc)
    report = [
        f"# {title}",
        "",
        f"Generated: {datetime.now(UTC).strftime('%Y-%m-%d %H:%M UTC')}",
        "",
        "## Input molecule",
        "",
        f"SMILES: `{smiles}`",
        f"Canonical SMILES: `{desc['canonical_smiles']}`",
        "",
        "## Descriptor summary",
        "",
        descriptor_markdown(smiles),
        "",
        "## Interpretation",
        "",
        *[f"- {note}" for note in notes],
        "",
        "## Xylazine reference",
        "",
        f"Reference SMILES: `{XYLAZINE.smiles}`",
        "",
    ]
    if similarity_results is not None and not similarity_results.empty:
        report.extend(["## Similarity results", "", similarity_results.to_markdown(index=False), ""])
    if probe_rows:
        report.extend(["## Probe candidates", "", pd.DataFrame(probe_rows).to_markdown(index=False), ""])
    report.extend([
        "## Limitations",
        "",
        "- Descriptor, similarity, and probe scores are heuristic prioritization aids.",
        "- AZAI does not replace experimental validation, analytical calibration, or safety review.",
        "- Literature-backed claims should be added with citations as the project matures.",
        "",
        "## Safety statement",
        "",
        SAFETY_TEXT,
        "",
    ])
    return "\n".join(report)
