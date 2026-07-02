"""AZAI command-line interface."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from azai import __version__
from azai.fluorescence.probe_builder import generate_probe_candidates
from azai.data.validation import issues_to_frame, validate_smiles_table
from azai.molecules.batch import xylazine_similarity_workup
from azai.molecules.descriptors import calculate_descriptors
from azai.reports.markdown import SAFETY_TEXT, generate_markdown_report
from azai.reproducibility.manifest import build_manifest


def _write_text(path: str | None, text: str) -> None:
    if path:
        Path(path).write_text(text, encoding="utf-8")
    else:
        print(text)


def cmd_analyze(args: argparse.Namespace) -> None:
    """Analyze one molecule and print JSON."""
    payload = {"smiles": args.smiles, "descriptors": calculate_descriptors(args.smiles), "safety_notice": SAFETY_TEXT}
    _write_text(args.output, json.dumps(payload, indent=2, sort_keys=True))


def cmd_similarity(args: argparse.Namespace) -> None:
    """Run xylazine similarity workup for a CSV file."""
    df = pd.read_csv(args.csv)
    results = xylazine_similarity_workup(df, smiles_column=args.smiles_column, label_column=args.label_column)
    if args.output:
        results.to_csv(args.output, index=False)
    else:
        print(results.to_csv(index=False))


def cmd_probes(args: argparse.Namespace) -> None:
    """Generate probe candidates and print JSON."""
    candidates = generate_probe_candidates(args.smiles, max_candidates=args.max_candidates)
    _write_text(args.output, json.dumps(candidates, indent=2, sort_keys=True))


def cmd_report(args: argparse.Namespace) -> None:
    """Generate a Markdown report."""
    report = generate_markdown_report(args.smiles, title=args.title)
    _write_text(args.output, report)



def cmd_validate(args: argparse.Namespace) -> None:
    """Validate a CSV table containing SMILES strings."""
    df = pd.read_csv(args.csv)
    result = validate_smiles_table(df, smiles_column=args.smiles_column, label_column=args.label_column)
    summary = {
        "is_valid": result["is_valid"],
        "valid_rows": result["valid_rows"],
        "invalid_rows": result["invalid_rows"],
    }
    if args.output:
        issues_to_frame(result["issues"]).to_csv(args.output, index=False)
    print(json.dumps(summary, indent=2, sort_keys=True))


def cmd_manifest(args: argparse.Namespace) -> None:
    """Create a reproducibility manifest for an analysis input."""
    files = [args.file] if args.file else None
    manifest = build_manifest(smiles=args.smiles, files=files, parameters={"workflow": args.workflow})
    _write_text(args.output, json.dumps(manifest, indent=2, sort_keys=True))

def build_parser() -> argparse.ArgumentParser:
    """Build the AZAI CLI parser."""
    parser = argparse.ArgumentParser(prog="azai", description="AZAI cheminformatics and probe discovery CLI")
    parser.add_argument("--version", action="version", version=f"AZAI {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    analyze = subparsers.add_parser("analyze", help="Calculate molecular descriptors for one SMILES string")
    analyze.add_argument("--smiles", required=True)
    analyze.add_argument("--output")
    analyze.set_defaults(func=cmd_analyze)

    similarity = subparsers.add_parser("similarity", help="Rank a CSV of molecules by xylazine similarity")
    similarity.add_argument("--csv", required=True)
    similarity.add_argument("--smiles-column", default="smiles")
    similarity.add_argument("--label-column")
    similarity.add_argument("--output")
    similarity.set_defaults(func=cmd_similarity)

    probes = subparsers.add_parser("probes", help="Generate heuristic fluorescent probe candidates")
    probes.add_argument("--smiles", required=True)
    probes.add_argument("--max-candidates", type=int, default=12)
    probes.add_argument("--output")
    probes.set_defaults(func=cmd_probes)

    report = subparsers.add_parser("report", help="Generate a Markdown report")
    report.add_argument("--smiles", required=True)
    report.add_argument("--title", default="AZAI Molecular Intelligence Report")
    report.add_argument("--output")
    report.set_defaults(func=cmd_report)


    validate = subparsers.add_parser("validate", help="Validate a CSV table containing SMILES strings")
    validate.add_argument("--csv", required=True)
    validate.add_argument("--smiles-column", default="smiles")
    validate.add_argument("--label-column")
    validate.add_argument("--output")
    validate.set_defaults(func=cmd_validate)

    manifest = subparsers.add_parser("manifest", help="Create a reproducibility manifest")
    manifest.add_argument("--smiles")
    manifest.add_argument("--file")
    manifest.add_argument("--workflow", default="cli")
    manifest.add_argument("--output")
    manifest.set_defaults(func=cmd_manifest)
    return parser


def main(argv: list[str] | None = None) -> None:
    """Run the CLI."""
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
