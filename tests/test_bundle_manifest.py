import zipfile
from io import BytesIO

from azai.export.bundle import build_analysis_bundle


def test_bundle_includes_reproducibility_manifest():
    payload = build_analysis_bundle("CCO")
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        assert "reproducibility_manifest.json" in archive.namelist()
        manifest = archive.read("reproducibility_manifest.json").decode("utf-8")
        assert "analysis_bundle" in manifest
