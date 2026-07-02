# AZAI CLI

AZAI v0.8.0 includes a command-line interface for reproducible analysis workflows.

## Commands

```bash
azai --version
azai analyze --smiles "CC1=Nc2ccccc2SC1(C)C"
azai similarity --csv data/reference/azai_reference_molecules.csv --smiles-column smiles --label-column name --output similarity.csv
azai probes --smiles "CC1=Nc2ccccc2SC1(C)C" --max-candidates 8 --output probes.json
azai report --smiles "CC1=Nc2ccccc2SC1(C)C" --output azai_report.md
```

The CLI prints JSON, CSV, or Markdown outputs that can be versioned, shared, and included in reproducible notebooks.

## Stable release commands

AZAI v1.0.0 adds release-oriented utilities:

```bash
azai doctor --markdown
azai doctor --output azai_health.json
azai release-notes --output AZAI_v1_release_notes.md
```

`azai doctor` verifies local imports, descriptor calculation, version metadata, and safety metadata. Optional interface dependencies may be reported as warnings in minimal environments.
