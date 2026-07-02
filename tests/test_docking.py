from azai.docking.prepare_ligand import ligand_package_zip, prepare_ligand_package
from azai.docking.prepare_receptor import receptor_preparation_checklist
from azai.docking.vina_runner import build_vina_command
from azai.xylazine.reference import XYLAZINE


def test_prepare_ligand_package_contains_blocks():
    package = prepare_ligand_package(XYLAZINE.smiles, name="xylazine")
    assert package.canonical_smiles
    assert "M  END" in package.sdf_block
    assert "ATOM" in package.pdb_block or "HETATM" in package.pdb_block
    assert "PDBQT PLACEHOLDER" in package.pdbqt_placeholder


def test_ligand_package_zip_has_bytes():
    data = ligand_package_zip(XYLAZINE.smiles, name="xylazine")
    assert isinstance(data, bytes)
    assert len(data) > 1000


def test_receptor_checklist_and_vina_command():
    checklist = receptor_preparation_checklist()
    assert any("protonation" in item.lower() for item in checklist)
    command = build_vina_command("rec.pdbqt", "lig.pdbqt", "out.pdbqt", (1, 2, 3), (20, 20, 20))
    assert command[0] == "vina"
    assert "--center_x" in command
