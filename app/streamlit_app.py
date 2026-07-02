"""AZAI Streamlit application."""

from __future__ import annotations

import pandas as pd
import streamlit as st

from azai.fluorescence.fluorophores import FLUOROPHORES
from azai.fluorescence.probe_builder import generate_probe_concepts
from azai.molecules.descriptors import calculate_descriptors
from azai.models.explainability import descriptor_contribution_table
from azai.molecules.plots import descriptor_radar, similarity_bar_chart
from azai.molecules.similarity import rank_by_similarity
from azai.molecules.visualization import mol_image
from azai.reports.markdown import generate_markdown_report
from azai.literature.retriever import TfidfLiteratureRetriever, retrieval_results_frame
from azai.literature.assistant import synthesize_literature_answer
from azai.scoring.probe_score import ProbeConcept, score_probe_concept
from azai.xylazine.reference import XYLAZINE, xylazine_profile
from azai.xylazine.selectivity import interferent_risk_table
from azai.export.bundle import build_analysis_bundle
from azai.reports.html import molecule_report_html
from azai.xylazine.database import reference_table

st.set_page_config(page_title="AZAI", page_icon="🧪", layout="wide")

st.title("AZAI: AI-Driven Xylazine Analytics and Innovation")
st.caption("Open-source molecular intelligence and fluorescent probe discovery for xylazine detection research.")
st.warning(
    "Safety: AZAI is for analytical chemistry, public health research, forensic detection, and education. "
    "It does not provide illicit synthesis instructions or optimize abuse potential. Scores are heuristic research hypotheses."
)

profile_tab, analyze_tab, analog_tab, probe_tab, selectivity_tab, explain_tab, lit_tab, ref_tab, report_tab = st.tabs(
    [
        "Xylazine Profile",
        "Molecule Analyzer",
        "Analog Explorer",
        "Probe Designer",
        "Interferent Risk",
        "Explainability",
        "Literature Assistant",
        "Reference DB",
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


with explain_tab:
    st.subheader("Transparent descriptor explanations")
    explain_smiles = st.text_input("SMILES to explain", value=XYLAZINE.smiles, key="explain_smiles")
    try:
        explain_desc = calculate_descriptors(explain_smiles)
        col1, col2 = st.columns([1, 2])
        with col1:
            st.image(mol_image(explain_smiles), caption="Explained molecule")
        with col2:
            contribution = descriptor_contribution_table(explain_desc)
            st.dataframe(contribution, use_container_width=True)
            st.caption(
                "These are rule-based interpretation notes, not causal model attributions. "
                "Future AZAI models will add validated feature attribution when experimental datasets are available."
            )
    except Exception as exc:  # noqa: BLE001
        st.error(str(exc))

with lit_tab:
    st.subheader("Local literature assistant")
    st.write(
        "Paste notes, abstracts, or exported text from papers. AZAI builds a local TF-IDF index "
        "and returns retrieval-grounded excerpts. PDF parsing and embedding search are planned next."
    )
    default_notes = """Fluorescent probes for amines often use PET or ICT mechanisms where protonation or binding changes electron transfer.
Tertiary amines can be challenging selectivity targets because many forensic and biological interferents contain basic amines.
Xylazine contains an aromatic ring system and basic nitrogen-rich features that may support hydrophobic, H-bonding, and protonation-state-sensitive recognition hypotheses."""
    literature_text = st.text_area("Local notes or abstracts", value=default_notes, height=180)
    question = st.text_input("Question", value="What probe mechanisms are suitable for tertiary amines?")
    if st.button("Search local literature"):
        try:
            retriever = TfidfLiteratureRetriever()
            retriever.add_documents({"user_notes": literature_text})
            chunks = retriever.search(question, top_k=5)
            st.dataframe(retrieval_results_frame(chunks), use_container_width=True)
            st.code(synthesize_literature_answer(question, chunks), language="markdown")
        except Exception as exc:  # noqa: BLE001
            st.error(str(exc))

with ref_tab:
    st.subheader("Curated reference molecules")
    st.write(
        "Small transparent molecule set for xylazine-centered analytical chemistry demos. "
        "This is not a validated forensic database."
    )
    refs = reference_table()
    st.dataframe(refs, use_container_width=True)
    st.download_button("Download reference CSV", refs.to_csv(index=False), "azai_reference_molecules.csv")


with report_tab:
    st.subheader("Scientific report and export bundle")
    report_smiles = st.text_input("Report molecule SMILES", value=XYLAZINE.smiles, key="report_smiles")
    try:
        report = generate_markdown_report(report_smiles, title="AZAI Molecular Analysis Report")
        html_report = molecule_report_html(report_smiles, title="AZAI Molecular Analysis Report")
        bundle = build_analysis_bundle(report_smiles, title="AZAI Molecular Analysis Report")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.download_button("Download Markdown", report, "azai_report.md")
        with col2:
            st.download_button("Download HTML", html_report, "azai_report.html")
        with col3:
            st.download_button("Download full ZIP bundle", bundle, "azai_analysis_bundle.zip")
        st.code(report, language="markdown")
    except Exception as exc:  # noqa: BLE001
        st.error(str(exc))
