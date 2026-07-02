"""Release health checks for AZAI.

The checks are intentionally local and conservative. They help users verify that
an installed AZAI environment can import the core package, calculate descriptors,
score probe concepts, and expose the safety statement before running analyses.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from importlib import import_module
from typing import Any

from azai import __version__
from azai.molecules.descriptors import calculate_descriptors
from azai.reports.markdown import SAFETY_TEXT
from azai.xylazine.reference import XYLAZINE


@dataclass(frozen=True)
class HealthCheck:
    """One environment or workflow check."""

    name: str
    status: str
    detail: str


def _check_import(module_name: str, *, required: bool = True) -> HealthCheck:
    try:
        import_module(module_name)
    except Exception as exc:  # noqa: BLE001
        status = "fail" if required else "warn"
        return HealthCheck(module_name, status, str(exc))
    return HealthCheck(module_name, "pass", "import ok")


def collect_health_checks() -> list[HealthCheck]:
    """Run local health checks for the installed AZAI environment."""
    checks: list[HealthCheck] = [
        HealthCheck("azai.version", "pass", __version__),
        _check_import("rdkit"),
        _check_import("pandas"),
        _check_import("sklearn"),
        _check_import("streamlit", required=False),
        _check_import("fastapi", required=False),
    ]
    try:
        desc = calculate_descriptors(XYLAZINE.smiles)
        checks.append(HealthCheck("xylazine.descriptors", "pass", f"MW={desc['molecular_weight']}"))
    except Exception as exc:  # noqa: BLE001
        checks.append(HealthCheck("xylazine.descriptors", "fail", str(exc)))
    checks.append(HealthCheck("safety.statement", "pass", SAFETY_TEXT[:96] + "..."))
    return checks


def health_report() -> dict[str, Any]:
    """Return a JSON-serializable release health report."""
    checks = collect_health_checks()
    failed = [check for check in checks if check.status == "fail"]
    return {
        "project": "AZAI",
        "version": __version__,
        "status": "ok" if not failed else "fail",
        "checks": [asdict(check) for check in checks],
        "safety_notice": SAFETY_TEXT,
    }


def health_markdown() -> str:
    """Return the health report as a small Markdown table."""
    report = health_report()
    rows = [
        "# AZAI Release Health Report",
        "",
        f"Version: `{report['version']}`",
        f"Overall status: **{report['status']}**",
        "",
        "| Check | Status | Detail |",
        "|---|---|---|",
    ]
    for check in report["checks"]:
        rows.append(f"| {check['name']} | {check['status']} | {check['detail']} |")
    rows.extend(["", "## Safety", "", str(report["safety_notice"]), ""])
    return "\n".join(rows)
