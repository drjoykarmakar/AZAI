# AZAI v1.0.0 stable release

AZAI v1.0.0 is a stable research MVP for xylazine-centered molecular intelligence and fluorescent probe discovery.

## What stable means here

Stable means the core software workflows are organized, tested, documented, and reusable:

- RDKit descriptors and fingerprints
- xylazine profile and similarity ranking
- probe concept generation and heuristic scoring
- selectivity triage
- local literature-note retrieval
- Streamlit, CLI, and FastAPI interfaces
- Markdown, HTML, ZIP, and manifest exports
- release health checks

It does not mean that heuristic probe scores, docking outputs, or selectivity estimates are experimentally validated.

## Health checks

Run:

```bash
azai doctor --markdown
```

The command verifies core imports, descriptor calculation, package version, and safety metadata.

## Release notes

Run:

```bash
azai release-notes
```

Use the output as a starting point for GitHub releases.
