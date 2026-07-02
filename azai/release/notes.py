"""Release note helpers for AZAI."""

from __future__ import annotations

from azai import __version__


def stable_release_summary() -> dict[str, object]:
    """Return a concise summary of the AZAI v1 release scope."""
    return {
        "version": __version__,
        "release": "Stable research MVP",
        "core_capabilities": [
            "RDKit molecular descriptors and fingerprints",
            "xylazine reference profile and similarity ranking",
            "fluorescent probe concept generation and heuristic scoring",
            "interferent risk triage",
            "local literature-note retrieval",
            "Streamlit dashboard, CLI, FastAPI, reports, and exports",
            "reproducibility manifests and validation utilities",
        ],
        "limits": [
            "No experimentally validated probe-performance claims are made by default.",
            "Docking exports prepare files; they do not calculate or validate binding scores.",
            "All scoring is transparent and intended for prioritization, not proof.",
        ],
    }


def stable_release_markdown() -> str:
    """Return Markdown release notes for the stable MVP."""
    summary = stable_release_summary()
    lines = [
        f"# AZAI {summary['version']} — Stable Research MVP",
        "",
        "AZAI v1.0.0 packages the core platform into a reproducible open-source research MVP.",
        "",
        "## Included capabilities",
        "",
    ]
    lines.extend(f"- {item}" for item in summary["core_capabilities"])
    lines.extend(["", "## Scientific limits", ""])
    lines.extend(f"- {item}" for item in summary["limits"])
    lines.extend(["", "## Recommended citation", "", "Cite the GitHub repository and the exact commit or release tag used.", ""])
    return "\n".join(lines)
