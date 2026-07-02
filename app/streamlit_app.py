"""AZAI Streamlit application."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from azai.fluorescence.fluorophores import FLUOROPHORES
from azai.fluorescence.probe_builder import generate_probe_concepts
from azai.molecules.descriptors import calculate_descriptors
from azai.molecules.plots import descriptor_radar, similarity_bar_chart
from azai.molecules.similarity import rank_by_similarity
from azai.molecules.visualization import mol_image
from azai.reports.markdown import molecule_report_markdown
from azai.scoring.probe_score import ProbeConcept, score_probe_concept
from azai.xylazine.reference import XYLAZINE, xylazine_profile
from azai.xylazine.selectivity import interferent_risk_table

st.set_page_config(page_title="AZAI", page_icon="🧪", layout="wide")

st.title("AZAI: AI-Driven Xylazine Analytics and Innovation")
st.caption("Open-source molecular intelligence and fluorescent probe discovery for xylazine detection research.")
st.warning(
    "Safety: AZAI is for analytical chemistry, public health research, forensic detection, and education. "
    "It does not provide illicit synthesis instructions or optimize abuse potential. Scores are heuristic research hypotheses."
)

profile_tab, analyze_tab, analog_tab, probe_tab, selectivity_tab, report_tab = st.tabs(
    [
        "Xylazine Profile",
        "Molecule Analyzer",
        "Analog Explorer",
        "Probe Designer",
        "Interferent Risk",
        "Report Generator",
    ]
)

with profile_tab:
    profile = xylazine_profile()
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image(mol_image(XYLAZINE.smiles), caption="Xylazine 2D structure")
    with col2:
        st.subheader("Reference profile")
        st.write(profile["description"])
        st.dataframe(pd.DataFrame([profile["descriptors"]]), use_container_width=True)
        st.plotly_chart(descriptor_radar(profile["descriptors"]), use_container_width=True)
        st.write("Functional group alerts")
        st.json(profile["functional_group_alerts"])
        st.write("Medicinal chemistry interpretation")
        st.info(profile["interpretation"])

with analyze_tab:
    smiles = st.text_input("Input SMILES", value=XYLAZINE.smiles)
    if smiles:
        try:
            descriptors = calculate_descriptors(smiles)
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(mol_image(smiles), caption="Input molecule")
            with col2:
                st.dataframe(pd.DataFrame([descriptors]), use_container_width=True)
                st.plotly_chart(descriptor_radar(descriptors), use_container_width=True)
            st.subheader("Similarity to xylazine")
            st.dataframe(rank_by_similarity([smiles], XYLAZINE.smiles), use_container_width=True)
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))

with analog_tab:
    st.subheader("Rank molecules by xylazine similarity")
    st.write("Upload a CSV with a `smiles` column. Optional columns such as `name` are preserved when possible.")
    upload = st.file_uploader("Upload CSV", type=["csv"], key="analog_upload")
    example_df = pd.DataFrame(
        {
            "name": ["xylazine", "lidocaine", "clonidine"],
            "smiles": [XYLAZINE.smiles, "CCN(CC)CC(=O)NC1=C(C=CC=C1C)C", "C1=CC(=C(C(=C1)Cl)NC2=NCCN2)Cl"],
        }
    )
    st.download_button("Download example CSV", example_df.to_csv(index=False), "azai_example_analogs.csv")
    if upload:
        df = pd.read_csv(upload)
    else:
        df = example_df
    if "smiles" not in df.columns:
        st.error("CSV must contain a 'smiles' column.")
    else:
        ranked = rank_by_similarity(df["smiles"].dropna().astype(str).tolist(), XYLAZINE.smiles)
        if "name" in df.columns and len(df) == len(ranked):
            ranked.insert(0, "label", df["name"].astype(str).tolist())
        st.dataframe(ranked, use_container_width=True)
        st.plotly_chart(similarity_bar_chart(ranked), use_container_width=True)
        st.download_button("Download ranked CSV", ranked.to_csv(index=False), "azai_similarity_results.csv")

with probe_tab:
    st.subheader("Rule-based fluorescent probe designer")
    generated = pd.DataFrame(generate_probe_concepts())
    st.dataframe(generated, use_container_width=True)
    st.download_button("Download generated probe concepts", generated.to_csv(index=False), "azai_probe_concepts.csv")

    st.divider()
    st.subheader("Manual probe scoring")
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

with selectivity_tab:
    st.subheader("Interferent comparison")
    risk = interferent_risk_table()
    st.dataframe(risk, use_container_width=True)
    st.caption("Combined risk is a heuristic blend of fingerprint similarity and descriptor overlap, not a validated selectivity prediction.")
    st.download_button("Download interferent risk table", risk.to_csv(index=False), "azai_interferent_risk.csv")

with report_tab:
    st.subheader("Markdown report generator")
    report_smiles = st.text_input("Report molecule SMILES", value=XYLAZINE.smiles, key="report_smiles")
    try:
        report = molecule_report_markdown(report_smiles, title="AZAI Molecular Analysis Report")
        st.download_button("Download Markdown report", report, "azai_report.md")
        st.code(report, language="markdown")
    except Exception as exc:  # noqa: BLE001
        st.error(str(exc))
