"""Generate an AZAI docking-ready ligand export bundle."""

from pathlib import Path

from azai.docking.prepare_ligand import ligand_package_zip
from azai.xylazine.reference import XYLAZINE


def main() -> None:
    out = Path("azai_xylazine_ligand_export.zip")
    out.write_bytes(ligand_package_zip(XYLAZINE.smiles, name="xylazine"))
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
