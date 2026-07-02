"""Docking-ready ligand preparation utilities.

The MVP prepares transparent ligand exports for downstream tools. It does not run docking
or claim binding predictions. PDBQT generation is intentionally marked as a lightweight
placeholder because chemically rigorous PDBQT typing normally requires Open Babel,
Meeko, AutoDockTools, or an equivalent external workflow.
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

from rdkit import Chem
from rdkit.Chem import AllChem

from azai.molecules.descriptors import calculate_descriptors
from azai.molecules.standardize import canonical_smiles, mol_from_smiles


@dataclass(frozen=True)
class DockingLigandPackage:
    """Container for ligand export artifacts."""

    canonical_smiles: str
    sdf_block: str
    mol_block: str
    pdb_block: str
    pdbqt_placeholder: str
    metadata: dict[str, float | int | str]


def embed_ligand_3d(smiles: str, random_seed: int = 61453) -> Chem.Mol:
    """Return an RDKit molecule with hydrogens and optimized 3D coordinates."""
    mol = Chem.AddHs(mol_from_smiles(smiles))
    status = AllChem.EmbedMolecule(mol, randomSeed=random_seed)
    if status != 0:
        status = AllChem.EmbedMolecule(mol, randomSeed=random_seed, useRandomCoords=True)
    if status != 0:
        raise ValueError("RDKit could not generate 3D coordinates for this molecule.")
    try:
        AllChem.MMFFOptimizeMolecule(mol, maxIters=500)
        force_field = "MMFF94"
    except Exception:  # noqa: BLE001
        AllChem.UFFOptimizeMolecule(mol, maxIters=500)
        force_field = "UFF"
    mol.SetProp("AZAI_3D_FORCE_FIELD", force_field)
    return mol


def mol_to_sdf_block(mol: Chem.Mol, name: str = "AZAI_ligand") -> str:
    """Return an SDF block with the molecule name and properties."""
    mol = Chem.Mol(mol)
    mol.SetProp("_Name", name)
    return Chem.MolToMolBlock(mol) + "$$$$\n"


def mol_to_pdb_block(mol: Chem.Mol) -> str:
    """Return a PDB block for a 3D ligand."""
    return Chem.MolToPDBBlock(mol)


def pdbqt_placeholder_from_pdb(pdb_block: str) -> str:
    """Return a clearly labeled PDBQT placeholder for external conversion workflows."""
    header = (
        "REMARK AZAI PDBQT PLACEHOLDER\n"
        "REMARK Convert the accompanying SDF/PDB with Meeko, Open Babel, or AutoDockTools for production docking.\n"
        "REMARK Example: mk_prepare_ligand.py -i ligand.sdf -o ligand.pdbqt\n"
        "REMARK AZAI does not assign AutoDock atom types in this placeholder file.\n"
    )
    return header + pdb_block


def prepare_ligand_package(smiles: str, name: str = "azai_ligand") -> DockingLigandPackage:
    """Prepare docking-oriented ligand export artifacts from SMILES."""
    mol3d = embed_ligand_3d(smiles)
    descriptors = calculate_descriptors(smiles)
    metadata: dict[str, float | int | str] = {
        "name": name,
        "canonical_smiles": canonical_smiles(smiles),
        "force_field": mol3d.GetProp("AZAI_3D_FORCE_FIELD"),
        "molecular_weight": descriptors["molecular_weight"],
        "logp": descriptors["logp"],
        "tpsa": descriptors["tpsa"],
        "rotatable_bonds": descriptors["rotatable_bonds"],
    }
    mol_block = Chem.MolToMolBlock(mol3d)
    pdb_block = mol_to_pdb_block(mol3d)
    return DockingLigandPackage(
        canonical_smiles=str(metadata["canonical_smiles"]),
        sdf_block=mol_to_sdf_block(mol3d, name=name),
        mol_block=mol_block,
        pdb_block=pdb_block,
        pdbqt_placeholder=pdbqt_placeholder_from_pdb(pdb_block),
        metadata=metadata,
    )


def ligand_package_zip(smiles: str, name: str = "azai_ligand") -> bytes:
    """Return a ZIP containing SDF, MOL, PDB, placeholder PDBQT, and metadata."""
    package = prepare_ligand_package(smiles, name=name)
    metadata_text = "\n".join(f"{key}: {value}" for key, value in package.metadata.items()) + "\n"
    buffer = BytesIO()
    with ZipFile(buffer, "w", ZIP_DEFLATED) as zf:
        zf.writestr(f"{name}.sdf", package.sdf_block)
        zf.writestr(f"{name}.mol", package.mol_block)
        zf.writestr(f"{name}.pdb", package.pdb_block)
        zf.writestr(f"{name}.pdbqt.placeholder", package.pdbqt_placeholder)
        zf.writestr("README_docking_export.txt", docking_export_readme())
        zf.writestr("metadata.txt", metadata_text)
    return buffer.getvalue()


def docking_export_readme() -> str:
    """Return usage notes for the docking export bundle."""
    return """# AZAI docking ligand export\n\nThis bundle contains RDKit-generated 3D ligand files for downstream docking workflows.\n\nIncluded files:\n- ligand.sdf: preferred input for Meeko/Open Babel conversion\n- ligand.mol: MOL block with 3D coordinates\n- ligand.pdb: PDB coordinates for visualization\n- ligand.pdbqt.placeholder: not production PDBQT; convert externally before docking\n\nRecommended next step:\nUse Meeko, Open Babel, or AutoDockTools to assign protonation state, charges, torsions, and AutoDock atom types.\n\nSafety note:\nAZAI exports are intended for analytical chemistry, molecular characterization, and education.\n"""
