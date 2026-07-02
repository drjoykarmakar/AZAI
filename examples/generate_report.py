"""Generate a Markdown report for xylazine using AZAI."""

from pathlib import Path

from azai.reports.markdown import generate_markdown_report
from azai.xylazine.reference import XYLAZINE


if __name__ == "__main__":
    report = generate_markdown_report(XYLAZINE.smiles)
    out = Path("azai_xylazine_report.md")
    out.write_text(report)
    print(f"Wrote {out}")
