"""Linker library for transparent fluorescent probe concept generation."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class LinkerOption:
    """A linker hypothesis with qualitative design tradeoffs."""

    name: str
    polarity: str
    flexibility: str
    synthetic_accessibility: float
    rationale: str
    caution: str


LINKERS: tuple[LinkerOption, ...] = (
    LinkerOption("amide", "moderate", "low-to-moderate", 0.82, "robust connector with predictable polarity", "amide formation conditions and hydrolysis stability must be checked"),
    LinkerOption("alkyl", "low", "moderate", 0.72, "simple spacer for first-pass SAR around distance/flexibility", "can reduce water compatibility and increase nonspecific hydrophobic response"),
    LinkerOption("PEG-like", "high", "moderate", 0.68, "improves aqueous handling and reduces aggregation risk", "may weaken analyte-probe proximity and lower response"),
    LinkerOption("sulfonamide", "moderate-to-high", "low", 0.74, "useful for amine-associated recognition environments", "can introduce nonspecific interactions with many basic analytes"),
    LinkerOption("triazole", "moderate", "low", 0.66, "modular click-compatible design element", "metal catalyst residues and photophysics should be controlled"),
)


def linker_table() -> list[dict[str, object]]:
    """Return linkers as serializable dictionaries."""

    return [asdict(item) for item in LINKERS]


def get_linker(name: str) -> LinkerOption:
    """Get a linker by name."""

    for linker in LINKERS:
        if linker.name == name:
            return linker
    raise KeyError(f"Unknown linker: {name}")
