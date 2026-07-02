# Docking-ready ligand export

AZAI v0.6.0 adds RDKit-based 3D ligand exports for downstream docking workflows.

The export bundle includes:

- SDF with 3D coordinates
- MOL block
- PDB file
- clearly labeled PDBQT placeholder
- metadata file
- docking export README

AZAI does **not** claim docking predictions in this release. PDBQT files require external tools such as Meeko, Open Babel, or AutoDockTools to assign atom types, torsions, and charges.

Recommended workflow:

1. Generate an AZAI ligand export bundle.
2. Inspect protonation state and 3D geometry.
3. Convert SDF to production PDBQT externally.
4. Prepare receptor with a documented protocol.
5. Validate docking using known ligands when possible.
6. Report software versions, grid box, scoring assumptions, and limitations.

Safety: docking utilities are intended for analytical chemistry, molecular characterization, education, and reproducible computational workflow preparation.
