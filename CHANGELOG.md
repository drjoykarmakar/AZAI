# Changelog

## v0.2.0 - Professional project scaffold

- Added citation, contribution, conduct, security, changelog, issue templates, and PR template.
- Added expanded descriptor utilities, rule-of-five screening, scaffold extraction, functional group detection, and reference interferents.
- Added report generation helper and improved package metadata.

## v0.1.0 - Core cheminformatics MVP

- Initial RDKit descriptor, fingerprint, similarity, xylazine reference, probe scoring, Streamlit app, Docker, and CI scaffold.

## [0.3.0] - Professional UI and selectivity triage

### Added
- Multi-tab Streamlit dashboard with analog explorer, probe designer, interferent risk, and report generator.
- Rule-based fluorescent probe concept generator.
- Interferent reference panel and descriptor-overlap selectivity triage.
- Plotly descriptor radar charts and similarity bar charts.
- Additional tests for probe generation and selectivity logic.

### Notes
- All probe and selectivity scores remain transparent heuristics for research prioritization only.

## 0.4.0 - Local intelligence and explainability

### Added
- Lightweight TF-IDF literature assistant for local notes, abstracts, and text exports.
- Retrieval-grounded answer synthesis with conservative uncertainty language.
- Descriptor explanation table for transparent molecule interpretation.
- Baseline descriptor-based regression utilities for user-supplied toy or experimental datasets.
- Feature-importance helper for supported baseline models.
- New Streamlit tabs for Explainability and Literature Assistant.
- Example scripts for baseline modeling and literature retrieval.
- Additional tests for literature retrieval, baseline modeling, and explainability.

### Notes
- Literature retrieval uses local TF-IDF by default so AZAI remains runnable without large model downloads.
- Baseline models are exploratory tools and are not validated QSAR models unless users provide appropriate external validation.

## [0.7.0] - Fluorescent probe design engine

### Added
- Recognition motif library for xylazine-oriented analytical probe hypotheses.
- Linker library with polarity, flexibility, accessibility, rationale, and cautions.
- Spectral-window helpers and optical-priority labels for built-in fluorophores.
- Experiment prioritization helper for validation planning.
- Probe-adjusted interferent selectivity matrix.
- Expanded Streamlit Probe Designer and Interferent Risk workflows.
- New probe-design documentation and tests.

### Notes
- All probe scores remain transparent heuristic research hypotheses, not experimentally validated analytical performance claims.

## [0.6.0] - Docking export and model-card polish

### Added
- RDKit 3D ligand export utilities for SDF, MOL, PDB, and placeholder PDBQT workflows.
- Docking export ZIP bundles for downstream Meeko/Open Babel/AutoDockTools preparation.
- Receptor preparation checklist and AutoDock Vina command builder.
- Model-card utilities and heuristic probe scorer model card.
- Streamlit docking export tab.
- Docking and model-card documentation.
- Additional tests for docking utilities and model cards.

### Notes
- AZAI does not run or validate docking predictions in this release. PDBQT exports are clearly labeled placeholders requiring external preparation.
