"""Build reproducibility manifests for AZAI analyses.

The manifest is intentionally lightweight and local-first. It records package
versions, platform information, input hashes, and user-selected analysis
parameters so reports can be reviewed and rerun later.
"""

from __future__ import annotations

import hashlib
import json
import platform
import sys
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from importlib import metadata
from pathlib import Path
from typing import Any

from azai import __version__

CORE_PACKAGES = ["azai", "rdkit", "pandas", "numpy", "scikit-learn", "streamlit", "fastapi"]


@dataclass
class ReproducibilityManifest:
    """Serializable metadata that describes an AZAI run."""

    project: str = "AZAI"
    azai_version: str = __version__
    created_utc: str = field(default_factory=lambda: datetime.now(UTC).isoformat())
    python_version: str = field(default_factory=lambda: sys.version.split()[0])
    platform: str = field(default_factory=platform.platform)
    packages: dict[str, str] = field(default_factory=dict)
    inputs: dict[str, str] = field(default_factory=dict)
    parameters: dict[str, Any] = field(default_factory=dict)
    safety_scope: str = (
        "Analytical chemistry, public health research, molecular characterization, "
        "fluorescent probe discovery, and education only."
    )


def _package_version(package_name: str) -> str:
    """Return installed package version or a readable missing marker."""
    if package_name == "azai":
        return __version__
    try:
        return metadata.version(package_name)
    except metadata.PackageNotFoundError:
        return "not-installed"


def sha256_text(text: str) -> str:
    """Return a SHA-256 hash for a text input."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str | Path) -> str:
    """Return a SHA-256 hash for a local file."""
    file_path = Path(path)
    digest = hashlib.sha256()
    with file_path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def build_manifest(
    *,
    smiles: str | None = None,
    files: list[str | Path] | None = None,
    parameters: dict[str, Any] | None = None,
    packages: list[str] | None = None,
) -> dict[str, Any]:
    """Build a JSON-serializable reproducibility manifest.

    Parameters
    ----------
    smiles:
        Optional SMILES string analyzed in the run. The manifest stores its hash
        rather than treating it as a validated structure.
    files:
        Optional files used as user inputs, such as CSVs or notes.
    parameters:
        Analysis settings to capture, such as fingerprint radius or thresholds.
    packages:
        Package names to record. Defaults to AZAI's core runtime stack.
    """
    package_names = packages or CORE_PACKAGES
    manifest = ReproducibilityManifest(parameters=parameters or {})
    manifest.packages = {name: _package_version(name) for name in package_names}

    if smiles is not None:
        manifest.inputs["smiles_sha256"] = sha256_text(smiles)
        manifest.inputs["smiles_length"] = str(len(smiles))

    for file_path in files or []:
        path = Path(file_path)
        if path.exists() and path.is_file():
            manifest.inputs[str(path)] = sha256_file(path)

    return asdict(manifest)


def write_manifest(path: str | Path, manifest: dict[str, Any]) -> Path:
    """Write a manifest dictionary as formatted JSON and return the path."""
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")
    return output_path
