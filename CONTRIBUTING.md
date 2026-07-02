# Contributing to AZAI

Thank you for helping improve AZAI. The project welcomes contributions in cheminformatics, analytical chemistry, fluorescent probe design, documentation, examples, and software engineering.

## Good first contributions

- Add descriptor tests or edge cases.
- Improve Streamlit pages.
- Add curated, cited fluorophore metadata.
- Add small public-domain example datasets.
- Improve documentation and tutorials.

## Scientific standards

- Do not add unsupported performance claims.
- Label heuristic scores and placeholder datasets clearly.
- Include citations for curated scientific facts.
- Keep the focus on detection, characterization, public health, and education.

## Development workflow

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pre-commit install
pytest
```

Before opening a pull request, run:

```bash
ruff check .
ruff format .
pytest
```
