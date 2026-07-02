"""Recognition motif library for xylazine-oriented fluorescent probe hypotheses."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class RecognitionMotif:
    """A transparent recognition hypothesis for analytical probe design."""

    name: str
    description: str
    target_features: tuple[str, ...]
    compatible_mechanisms: tuple[str, ...]
    selectivity_risks: tuple[str, ...]
    water_strategy: str
    score_prior: float


RECOGNITION_MOTIFS: tuple[RecognitionMotif, ...] = (
    RecognitionMotif(
        name="protonation-state amine microenvironment",
        description="Local acidic/H-bonding environment designed to respond to the basic xylazine amine without claiming specific binding.",
        target_features=("basic amine", "heteroatom-rich ring", "pH-sensitive charge state"),
        compatible_mechanisms=("PET", "ICT", "turn-on fluorescence", "ratiometric response"),
        selectivity_risks=("common tertiary amines", "alpha-2 agonists", "buffer pH shifts"),
        water_strategy="include sulfonate, carboxylate, PEG, or zwitterionic solubilizing groups in later optimization",
        score_prior=0.78,
    ),
    RecognitionMotif(
        name="aryl hydrophobic pocket mimic",
        description="Hydrophobic/aromatic environment intended to exploit xylazine aryl character while monitoring nonspecific uptake.",
        target_features=("aromatic ring", "hydrophobic surface", "soft heteroatom context"),
        compatible_mechanisms=("ICT", "FRET", "turn-off fluorescence", "aggregation-induced emission"),
        selectivity_risks=("lidocaine", "fentanyl", "other aromatic amines"),
        water_strategy="pair hydrophobic recognition with external ionic solubilizers to avoid aggregation artifacts",
        score_prior=0.66,
    ),
    RecognitionMotif(
        name="dual H-bond / ion-pair motif",
        description="Balanced H-bond donor/acceptor and ion-pair environment for broad first-pass screening of xylazine-like features.",
        target_features=("basic amine", "H-bond acceptors", "imino/heteroatom motif"),
        compatible_mechanisms=("PET", "turn-on fluorescence", "ratiometric response"),
        selectivity_risks=("morphine/naloxone", "biological amines", "salt concentration"),
        water_strategy="test in buffered water/acetonitrile gradients before biological matrices",
        score_prior=0.72,
    ),
    RecognitionMotif(
        name="cation microenvironment motif",
        description="Crown-ether-inspired or polyanionic microenvironment for charge-sensitive response to protonated amines.",
        target_features=("protonated amine", "cationic analyte fraction", "charge-density changes"),
        compatible_mechanisms=("PET", "turn-on fluorescence", "aggregation-induced emission"),
        selectivity_risks=("triethylamine", "primary/secondary amines", "ionic strength"),
        water_strategy="measure pH and ionic-strength controls alongside analyte titrations",
        score_prior=0.62,
    ),
)


def recognition_motif_table() -> list[dict[str, object]]:
    """Return recognition motifs as serializable dictionaries."""

    return [asdict(item) for item in RECOGNITION_MOTIFS]


def get_recognition_motif(name: str) -> RecognitionMotif:
    """Get a recognition motif by name."""

    for motif in RECOGNITION_MOTIFS:
        if motif.name == name:
            return motif
    raise KeyError(f"Unknown recognition motif: {name}")
