# Fluorescent probe design engine

AZAI v0.7.0 expands the fluorescent probe workflow from a single ranked table into a transparent design engine.

The engine combines four explicit hypothesis layers:

1. **Fluorophore metadata**: broad excitation/emission ranges, brightness, photostability, aqueous compatibility, and common mechanisms.
2. **Recognition motifs**: xylazine-oriented analytical recognition hypotheses such as protonation-state amine microenvironments and dual H-bond/ion-pair motifs.
3. **Linker options**: qualitative linker tradeoffs for polarity, flexibility, synthetic accessibility, and potential artifacts.
4. **Experiment planning**: recommended analytical validation steps, pH controls, interferent panels, and limitations.

Scores are heuristic prioritization values. They are not validated limits of detection, selectivity factors, binding constants, or performance claims.

## Built-in motifs

- Protonation-state amine microenvironment
- Aryl hydrophobic pocket mimic
- Dual H-bond / ion-pair motif
- Cation microenvironment motif

## Built-in linkers

- Amide
- Alkyl
- PEG-like
- Sulfonamide
- Triazole

## Recommended validation sequence

1. Literature review table for the fluorophore and response mechanism.
2. Blank, pH-only, solvent-ratio, and buffer controls.
3. UV-vis and fluorescence titration with documented analytical conditions.
4. Interferent panel screening against common amines and alpha-2 agonist analogs.
5. Matrix tolerance only after basic signal behavior is confirmed.

AZAI intentionally focuses on detection and analytical chemistry. It does not provide synthesis instructions for illicit production or optimize harmful pharmacological activity.
