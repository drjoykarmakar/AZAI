"""Vina command builder.

This module builds commands but does not execute docking by default. Keeping execution
explicit avoids accidental black-box results and encourages reproducible protocol notes.
"""

from __future__ import annotations


def build_vina_command(
    receptor_pdbqt: str,
    ligand_pdbqt: str,
    out_pdbqt: str,
    center: tuple[float, float, float],
    size: tuple[float, float, float],
    exhaustiveness: int = 8,
) -> list[str]:
    """Build an AutoDock Vina command as a list of CLI arguments."""
    cx, cy, cz = center
    sx, sy, sz = size
    return [
        "vina",
        "--receptor",
        receptor_pdbqt,
        "--ligand",
        ligand_pdbqt,
        "--out",
        out_pdbqt,
        "--center_x",
        str(cx),
        "--center_y",
        str(cy),
        "--center_z",
        str(cz),
        "--size_x",
        str(sx),
        "--size_y",
        str(sy),
        "--size_z",
        str(sz),
        "--exhaustiveness",
        str(exhaustiveness),
    ]
