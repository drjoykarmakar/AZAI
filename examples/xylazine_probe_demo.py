"""Run an end-to-end AZAI MVP demonstration."""

from pprint import pprint

from azai.fluorescence.fluorophores import FLUOROPHORES
from azai.molecules.similarity import rank_by_similarity
from azai.scoring.probe_score import ProbeConcept, score_probe_concept
from azai.xylazine.reference import XYLAZINE, xylazine_profile


def main() -> None:
    print("AZAI xylazine profile")
    pprint(xylazine_profile())

    examples = [
        XYLAZINE.smiles,
        "CCN(CC)CCOC(=O)c1ccccc1",  # lidocaine-like placeholder
        "CN1CCC23c4c5ccc(O)c4OC2C(O)CC3C1C5",  # morphine-like example
    ]
    print("\nSimilarity ranking")
    print(rank_by_similarity(examples, XYLAZINE.smiles).to_string(index=False))

    concept = ProbeConcept(
        fluorophore="coumarin",
        recognition_group="acidic H-bond donor / amine-recognition motif",
        linker="amide",
        mechanism="PET",
        xylazine_interaction_hypothesis="Xylazine basic centers may modulate PET through protonation-state-sensitive binding.",
    )
    print("\nProbe concept score")
    pprint(score_probe_concept(concept, FLUOROPHORES["coumarin"]))


if __name__ == "__main__":
    main()
