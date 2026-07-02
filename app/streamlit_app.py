"""AZAI Streamlit MVP app."""

import pandas as pd
import streamlit as st

from azai.fluorescence.fluorophores import FLUOROPHORES
from azai.molecules.descriptors import calculate_descriptors
from azai.molecules.similarity import rank_by_similarity
from azai.molecules.visualization import mol_image
from azai.scoring.probe_score import ProbeConcept, score_probe_concept
from azai.xylazine.reference import XYLAZINE, xylazine_profile

st.set_page_config(page_title="AZAI", page_icon="🧪", layout="wide")
st.title("AZAI: AI-Driven Xylazine Analytics and Innovation")
st.caption("Open-source molecular intelligence and fluorescent probe discovery for xylazine detection research.")

st.warning(
    "Safety: AZAI is for analytical chemistry, public health research, forensic detection, and education. "
    "It does not provide illicit synthesis instructions or optimize abuse potential."
)

tab_profile, tab_analyze, tab_probe = st.tabs(["Xylazine Profile", "Molecule Analyzer", "Probe Scoring"])

with tab_profile:
    profile = xylazine_profile()
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(mol_image(XYLAZINE.smiles), caption="Xylazine 2D structure")
    with col2:
        st.subheader("Reference profile")
        st.write(profile["description"])
        st.dataframe(pd.DataFrame([profile["descriptors"]]), use_container_width=True)
        st.write("Functional group alerts")
        st.write(profile["functional_group_alerts"])
        st.write("Medicinal chemistry interpretation")
        st.write(profile["interpretation"])

with tab_analyze:
    smiles = st.text_input("Input SMILES", value=XYLAZINE.smiles)
    if smiles:
        try:
            st.image(mol_image(smiles), caption="Input molecule")
            st.dataframe(pd.DataFrame([calculate_descriptors(smiles)]), use_container_width=True)
            st.subheader("Similarity to xylazine")
            st.dataframe(rank_by_similarity([smiles], XYLAZINE.smiles), use_container_width=True)
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))

    upload = st.file_uploader("Upload CSV with a 'smiles' column", type=["csv"])
    if upload:
        df = pd.read_csv(upload)
        if "smiles" not in df.columns:
            st.error("CSV must contain a 'smiles' column.")
        else:
            ranked = rank_by_similarity(df["smiles"].dropna().astype(str).tolist(), XYLAZINE.smiles)
            st.dataframe(ranked, use_container_width=True)
            st.download_button("Download ranked CSV", ranked.to_csv(index=False), "azai_similarity_results.csv")

with tab_probe:
    fluorophore = st.selectbox("Fluorophore", sorted(FLUOROPHORES))
    mechanism = st.selectbox("Mechanism", FLUOROPHORES[fluorophore]["mechanisms"])
    recognition_group = st.text_input("Recognition group", value="acidic H-bond donor / amine-recognition motif")
    linker = st.text_input("Linker", value=str(FLUOROPHORES[fluorophore]["common_linkers"][0]))
    hypothesis = st.text_area(
        "Xylazine interaction hypothesis",
        value="Basic and heteroatom-rich xylazine motif may interact through protonation-state-sensitive H-bonding and ion-pair recognition.",
    )
    concept = ProbeConcept(fluorophore, recognition_group, linker, mechanism, hypothesis)
    score = score_probe_concept(concept, FLUOROPHORES[fluorophore])
    st.metric("AZAI probe score", score["total_score"])
    st.json(score)
