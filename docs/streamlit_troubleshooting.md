# Streamlit troubleshooting

## Duplicate Plotly element IDs

AZAI v1.0.3 adds explicit keys to Plotly chart calls in `app/streamlit_app.py`.
If Streamlit still shows a duplicate `plotly_chart` ID warning, stop the old server with `Ctrl+C`, reinstall the package, and restart from the repository root:

```bash
conda activate azai
cd ~/Downloads/AZAI
python -m pip install -e .
python -m streamlit run app/streamlit_app.py
```

Hard-refresh the browser with `Cmd+Shift+R` on macOS.

## Environment check

Use:

```bash
azai doctor
pytest -q
```

The app should be launched with `python -m streamlit` so it uses the same Python environment that contains RDKit and AZAI.
