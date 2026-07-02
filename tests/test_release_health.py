"""Tests for AZAI stable release helpers."""

from __future__ import annotations

import json
from pathlib import Path

from fastapi.testclient import TestClient

from azai import __version__
from azai.api.main import app
from azai.cli.main import main
from azai.release.health import health_markdown, health_report
from azai.release.notes import stable_release_summary


def test_health_report_is_json_ready() -> None:
    report = health_report()
    assert report["project"] == "AZAI"
    assert report["version"] == __version__
    assert report["status"] in {"ok", "fail"}
    assert any(check["name"] == "safety.statement" for check in report["checks"])
    json.dumps(report)


def test_health_markdown_contains_table() -> None:
    text = health_markdown()
    assert "AZAI Release Health Report" in text
    assert "| Check | Status | Detail |" in text


def test_release_summary_endpoint() -> None:
    client = TestClient(app)
    response = client.get("/release/summary")
    assert response.status_code == 200
    payload = response.json()
    assert payload["version"] == __version__
    assert "core_capabilities" in payload


def test_cli_doctor_and_release_notes(tmp_path: Path) -> None:
    health_path = tmp_path / "health.md"
    main(["doctor", "--markdown", "--output", str(health_path)])
    assert "Release Health" in health_path.read_text()

    notes_path = tmp_path / "release.md"
    main(["release-notes", "--output", str(notes_path)])
    assert "Stable Research MVP" in notes_path.read_text()


def test_stable_release_summary_lists_limits() -> None:
    summary = stable_release_summary()
    assert summary["version"] == __version__
    assert summary["limits"]
