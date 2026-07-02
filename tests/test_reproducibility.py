from pathlib import Path

from azai.reproducibility.manifest import build_manifest, sha256_text, write_manifest


def test_manifest_contains_hash_and_version(tmp_path: Path):
    manifest = build_manifest(smiles="CCO", parameters={"workflow": "test"})
    assert manifest["project"] == "AZAI"
    assert "azai" in manifest["packages"]
    assert manifest["inputs"]["smiles_sha256"] == sha256_text("CCO")
    assert manifest["parameters"]["workflow"] == "test"

    path = write_manifest(tmp_path / "manifest.json", manifest)
    assert path.exists()
    assert "AZAI" in path.read_text(encoding="utf-8")
