"""Optical metadata helpers for AZAI fluorescent probe concepts."""

from __future__ import annotations

from azai.fluorescence.fluorophores import FLUOROPHORES


def fluorophore_spectral_window(fluorophore: str) -> dict[str, str]:
    """Return typical excitation/emission windows for a built-in fluorophore."""

    meta = FLUOROPHORES[fluorophore]
    return {
        "fluorophore": fluorophore,
        "typical_excitation_nm": str(meta["excitation_nm"]),
        "typical_emission_nm": str(meta["emission_nm"]),
        "note": "Ranges are broad literature-style priors; actual spectra require experimental calibration.",
    }


def optical_priority_label(fluorophore: str) -> str:
    """Provide a practical optical screening label from fluorophore metadata."""

    meta = FLUOROPHORES[fluorophore]
    brightness = float(meta.get("brightness", 0.5))
    photostability = float(meta.get("photostability", 0.5))
    water = float(meta.get("water_compatibility", 0.5))
    composite = (brightness + photostability + water) / 3.0
    if composite >= 0.75:
        return "high-priority optical screen"
    if composite >= 0.55:
        return "medium-priority optical screen"
    return "specialized or formulation-dependent optical screen"
