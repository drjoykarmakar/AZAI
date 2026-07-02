"""Tests for the AZAI API and CLI."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from fastapi.testclient import TestClient

from azai.api.main import app
from azai.cli.main import main
from azai.xylazine.reference import XYLAZINE


def test_api_health_and_analyze() -> None:
    client = TestClient(app)
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "ok"

    response = client.post("/molecule/analyze", json={"smiles": XYLAZINE.smiles, "label": "xylazine"})
    assert response.status_code == 200
    payload = response.json()
    assert payload["descriptors"]["molecular_weight"] > 100
    assert "safety_notice" in payload


def test_api_similarity_and_probe_design() -> None:
    client = TestClient(app)
    response = client.post("/similarity/xylazine", json={"smiles": [XYLAZINE.smiles], "labels": ["xylazine"]})
    assert response.status_code == 200
    assert response.json()["results"][0]["label"] == "xylazine"

    probes = client.post("/probe/design", json={"target_smiles": XYLAZINE.smiles, "max_candidates": 3})
    assert probes.status_code == 200
    assert len(probes.json()["candidates"]) == 3


def test_api_literature_query() -> None:
    client = TestClient(app)
    response = client.post(
        "/literature/query",
        json={"query": "tertiary amine probes", "notes": ["PET probes can respond to tertiary amines."], "top_k": 1},
    )
    assert response.status_code == 200
    assert response.json()["results"][0]["source"] == "note_1"


def test_cli_analyze_and_report(tmp_path: Path) -> None:
    json_path = tmp_path / "analysis.json"
    main(["analyze", "--smiles", XYLAZINE.smiles, "--output", str(json_path)])
    payload = json.loads(json_path.read_text())
    assert payload["descriptors"]["molecular_weight"] > 100

    report_path = tmp_path / "report.md"
    main(["report", "--smiles", XYLAZINE.smiles, "--output", str(report_path)])
    assert "Safety statement" in report_path.read_text()


def test_cli_similarity(tmp_path: Path) -> None:
    csv_path = tmp_path / "molecules.csv"
    pd.DataFrame({"name": ["xylazine"], "smiles": [XYLAZINE.smiles]}).to_csv(csv_path, index=False)
    out_path = tmp_path / "similarity.csv"
    main([
        "similarity",
        "--csv",
        str(csv_path),
        "--smiles-column",
        "smiles",
        "--label-column",
        "name",
        "--output",
        str(out_path),
    ])
    assert "morgan_tanimoto" in out_path.read_text()
