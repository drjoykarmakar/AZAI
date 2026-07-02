import zipfile
from io import BytesIO

from azai.export.bundle import build_analysis_bundle
from azai.reports.html import molecule_report_html


def test_html_report_contains_title():
    html = molecule_report_html("CCO")
    assert "<!doctype html>" in html.lower()
    assert "AZAI" in html


def test_bundle_contains_expected_files():
    data = build_analysis_bundle("CCO")
    with zipfile.ZipFile(BytesIO(data)) as archive:
        names = set(archive.namelist())
    assert "AZAI_report.md" in names
    assert "AZAI_report.html" in names
    assert "descriptors.json" in names
    assert "interferent_risk.csv" in names
