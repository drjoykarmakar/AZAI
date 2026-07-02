# AZAI

**Current release:** v1.0.3

**AI-Driven Xylazine Analytics and Innovation**

[![CI](https://github.com/drjoykarmakar/AZAI/actions/workflows/ci.yml/badge.svg)](https://github.com/drjoykarmakar/AZAI/actions/workflows/ci.yml)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.21129540.svg)](https://doi.org/10.5281/zenodo.21129540)
[![ORCID](https://img.shields.io/badge/ORCID-0000--0002--8232--5639-A6CE39?logo=orcid)](https://orcid.org/0000-0002-8232-5639)
![Python](https://img.shields.io/badge/python-3.11%2B-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![RDKit](https://img.shields.io/badge/RDKit-cheminformatics-green)
![Status](https://img.shields.io/badge/status-v1.0.3%20stable%20research%20MVP-brightgreen)

> **AZAI is an open-source AI platform for xylazine-focused molecular intelligence and fluorescent probe discovery.**

<p align="center">
  <img src="app/assets/azai_logo_placeholder.svg" alt="AZAI logo placeholder" width="160" />
</p>

## Mission

AZAI helps researchers analyze xylazine and related molecular structures, prioritize fluorescent probe concepts, and generate transparent, reproducible cheminformatics reports for analytical chemistry and medicinal chemistry education.

## Safety statement

AZAI is intended for analytical chemistry, public health research, forensic detection, molecular characterization, fluorescent probe discovery, and medicinal chemistry education. It must not be used to optimize xylazine potency, abuse potential, harmful delivery, clandestine synthesis, or illicit drug production. All scores are computational prioritization hypotheses unless experimentally validated.

## What is included in v1.0.3

- RDKit molecule loading and standardization helpers
- Xylazine reference profile and curated reference molecule table
- Expanded molecular descriptors, Morgan fingerprints, and MACCS fingerprints
- Functional group detection and Murcko scaffold utilities
- Xylazine similarity ranking for CSV inputs
- Built-in fluorophore, recognition motif, and linker libraries
- Transparent fluorescent probe concept generation and 0-100 heuristic scoring
- Interferent selectivity-risk triage and probe-adjusted risk matrix
- Descriptor interpretation and explainability helpers
- Local TF-IDF literature-note retrieval assistant
- Markdown, HTML, ZIP, and reproducibility-manifest exports
- Docking-ready RDKit 3D ligand export bundle
- Streamlit dashboard, FastAPI service, and `azai` CLI
- Release health checks, model-card utilities, docs, examples, tests, Docker, CI, and citation metadata

## Repository architecture

```text
AZAI/
├── azai/                  # Python package
│   ├── molecules/         # descriptors, fingerprints, similarity, scaffolds, visualization
│   ├── xylazine/          # xylazine reference data, database, selectivity
│   ├── fluorescence/      # fluorophores, recognition motifs, linkers, probe concepts
│   ├── scoring/           # transparent probe scoring and ranking
│   ├── reports/           # Markdown and HTML reports
│   ├── docking/           # ligand export and docking workflow helpers
│   ├── api/               # FastAPI service
│   ├── cli/               # command-line interface
│   └── release/           # health checks, model cards, release notes
├── app/                   # Streamlit web app
├── examples/              # runnable example scripts
├── tests/                 # pytest tests
├── docs/                  # project documentation
└── data/                  # placeholder and reference data folders
```

## Installation

```bash
git clone https://github.com/drjoykarmakar/AZAI.git
cd AZAI
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -e ".[dev]"
```

RDKit is often easiest to install with conda/mamba:

```bash
mamba env create -f environment.yml
mamba activate azai
pip install -e ".[dev]"
```

## Quickstart

```bash
pytest
streamlit run app/streamlit_app.py
azai doctor --markdown
azai analyze --smiles "CC1=Nc2ccccc2SC1(C)C"
azai report --smiles "CC1=Nc2ccccc2SC1(C)C" --output azai_report.md
```

Run the local API:

```bash
uvicorn azai.api.main:app --reload
```

Open the API docs at `http://127.0.0.1:8000/docs`.

## Example Python use

```python
from azai.xylazine.reference import XYLAZINE, xylazine_profile
from azai.molecules.descriptors import calculate_descriptors
from azai.molecules.similarity import similarity_profile
from azai.reports.markdown import generate_markdown_report
from azai.release.health import health_report

print(health_report()["status"])
print(xylazine_profile())
print(calculate_descriptors(XYLAZINE.smiles))
print(similarity_profile("CN1CCN(CC1)C2=Nc3ccccc3S2", XYLAZINE.smiles))
print(generate_markdown_report(XYLAZINE.smiles)[:500])
```

## Methodology summary

AZAI starts with transparent cheminformatics baselines. Molecules are parsed with RDKit, converted into descriptors and fingerprints, compared with similarity metrics, screened with explicit functional-group and scaffold rules, and scored with interpretable heuristics. Probe scores are not experimental predictions; they are prioritization hypotheses designed to guide literature review and early experiments.

## Stable release scope

AZAI v1.0.3 is a stable research MVP. It includes a working package, web app, API, CLI, tests, documentation, reports, export bundles, and reproducibility tooling. It intentionally avoids unsupported claims about probe performance, biological activity, docking scores, or experimental validation.

## Roadmap

- **v1.1:** richer reference data with explicit literature citations
- **v1.2:** validated datasets and benchmark notebooks when suitable public data are available
- **v1.3:** embedding-based literature assistant as an optional extra
- **v1.4:** expanded explainable AI modules and model cards
- **v2.0:** broader analytical-chemistry platform beyond xylazine-centered examples

## Contributing

Contributions are welcome. Good first issues include adding descriptor tests, improving Streamlit pages, extending fluorophore metadata, adding example datasets, and writing documentation. Please keep all contributions aligned with analytical chemistry, public health, safety, and education.

## Author

**Dr. Joy Karmakar**  
Founder & Principal Developer — NarcoticSense AI  
Founder — DyeMind

- Website: <https://www.dyemind.com>
- ORCID: <https://orcid.org/0000-0002-8232-5639>
- GitHub: <https://github.com/drjoykarmakar>

## Research interests

- Artificial Intelligence for Spectroscopy
- Fluorescence Spectroscopy
- Raman Spectroscopy
- Chemometrics
- Analytical Chemistry
- Molecular Sensing
- Intelligent Sensor Development
- Scientific Machine Learning
- Explainable Artificial Intelligence
- Multimodal Spectroscopic Analysis

## Citation

If AZAI supports your work, please cite the archived software release:

> Karmakar, J. (2026). *AZAI: AI-Driven Xylazine Analytics and Innovation* (v1.0.3). Zenodo. <https://doi.org/10.5281/zenodo.21129540>

BibTeX:

```bibtex
@software{karmakar_azai_2026,
  author  = {Karmakar, Joy},
  title   = {AZAI: AI-Driven Xylazine Analytics and Innovation},
  version = {v1.0.3},
  year    = {2026},
  publisher = {Zenodo},
  doi     = {10.5281/zenodo.21129540},
  url     = {https://doi.org/10.5281/zenodo.21129540}
}
```

A `CITATION.cff` file is included so GitHub can display citation metadata.
