from azai.reports.markdown import generate_markdown_report
from azai.xylazine.reference import XYLAZINE


def test_report_contains_safety_statement():
    report = generate_markdown_report(XYLAZINE.smiles)
    assert "Safety statement" in report
    assert "Descriptor summary" in report
