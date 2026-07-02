"""Create downloadable AZAI analysis bundles."""

from __future__ import annotations

import json
import zipfile
from io import BytesIO

import pandas as pd

from azai.molecules.descriptors import calculate_descriptors
from azai.reports.html import molecule_report_html
from azai.reports.markdown import generate_markdown_report
from azai.xylazine.selectivity import interferent_risk_table


def build_analysis_bundle(smiles: str, title: str = "AZAI Molecular Intelligence Report") -> bytes:
    """Return a ZIP archive containing report and machine-readable outputs."""
    descriptors = calculate_descriptors(smiles)
    risk = interferent_risk_table(smiles)
    markdown = generate_markdown_report(smiles, title=title, similarity_results=risk)
    html = molecule_report_html(smiles, title=title)
    descriptor_json = json.dumps(descriptors, indent=2, sort_keys=True)
    descriptor_csv = pd.DataFrame([descriptors]).to_csv(index=False)

    buffer = BytesIO()
    with zipfile.ZipFile(buffer, mode="w", compression=zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("AZAI_report.md", markdown)
        archive.writestr("AZAI_report.html", html)
        archive.writestr("descriptors.json", descriptor_json)
        archive.writestr("descriptors.csv", descriptor_csv)
        archive.writestr("interferent_risk.csv", risk.to_csv(index=False))
        archive.writestr(
            "SAFETY.txt",
            "AZAI is for analytical chemistry, public health, forensic detection, and education. "
            "Outputs are computational hypotheses and require experimental validation.\n",
        )
    return buffer.getvalue()
