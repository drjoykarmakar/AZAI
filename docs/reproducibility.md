# Reproducibility

AZAI v0.9.0 adds lightweight reproducibility manifests for local analyses.

A manifest records:

- AZAI version
- Python version
- platform information
- core package versions
- SHA-256 hashes of input SMILES or local files
- user-selected workflow parameters
- safety scope

The manifest is included in analysis ZIP bundles as `reproducibility_manifest.json`.

## CLI usage

```bash
azai manifest --smiles "CCO" --workflow descriptor_demo --output manifest.json
```

Validate an input CSV before a batch run:

```bash
azai validate --csv molecules.csv --smiles-column smiles --label-column name --output validation_issues.csv
```

## Scientific note

Manifests support auditability and reruns. They do not validate experimental performance, analytical limits of detection, selectivity, or biological activity. Those claims require appropriate experimental evidence.
