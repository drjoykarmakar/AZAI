# Release checklist

Before tagging a release:

1. Run the full test suite with `python -m pytest -q`.
2. Confirm the Streamlit app launches locally.
3. Run at least one CLI descriptor, similarity, report, validation, and manifest command.
4. Check that README examples match the current version.
5. Confirm safety language is present in reports and export bundles.
6. Create a GitHub release with a clear changelog entry.
7. Avoid performance claims unless backed by documented validation data.

Recommended v1.0 gates:

- passing CI
- Docker build verified
- documentation site builds
- example data clearly labeled as examples
- model cards completed for heuristic and ML components
- citation metadata up to date
