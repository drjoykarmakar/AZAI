# AZAI API

AZAI v0.8.0 adds a conservative FastAPI service for local molecular analysis, xylazine similarity ranking, fluorescent probe concept generation, local literature retrieval, and Markdown report generation.

## Run locally

```bash
uvicorn azai.api.main:app --reload
```

Then open the interactive API docs at `http://127.0.0.1:8000/docs`.

## Endpoints

- `GET /health` — service status and AZAI version
- `GET /safety` — project safety notice
- `GET /xylazine/profile` — built-in xylazine profile
- `POST /molecule/analyze` — descriptor, functional-group, and interpretation output
- `POST /similarity/xylazine` — rank molecules by similarity to xylazine or an optional reference
- `POST /probe/design` — generate transparent fluorescent probe concepts
- `POST /literature/query` — retrieve relevant text from user-provided notes
- `POST /report/markdown` — generate a Markdown molecular report

## Example request

```bash
curl -X POST http://127.0.0.1:8000/molecule/analyze \
  -H "Content-Type: application/json" \
  -d '{"smiles":"CC1=Nc2ccccc2SC1(C)C","label":"example"}'
```

## Safety boundary

The API is for local analytical chemistry research, molecular characterization, public health, and education. It does not provide clandestine synthesis, harmful optimization, or misuse-oriented guidance.

## Stable release endpoints

AZAI v1.0.0 adds release metadata endpoints:

- `GET /health` returns a JSON health report for the local installation.
- `GET /release/summary` returns the stable MVP scope and scientific limitations.

These endpoints are designed for local reproducibility checks and deployment smoke tests.
