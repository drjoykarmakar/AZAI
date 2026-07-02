"""FastAPI application for AZAI.

The API is intentionally conservative: it exposes cheminformatics analysis,
similarity ranking, heuristic probe concept generation, and local text retrieval.
It does not provide experimental protocols or synthesis instructions.
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException

from azai import __version__
from azai.api.schemas import (
    LiteratureQueryRequest,
    MoleculeAnalysisResponse,
    MoleculeRequest,
    ProbeDesignRequest,
    SimilarityRequest,
)
from azai.fluorescence.experiment_plan import recommended_experiment_plan
from azai.fluorescence.probe_builder import generate_probe_candidates
from azai.literature.retriever import retrieve_relevant_chunks
from azai.molecules.descriptors import calculate_descriptors, medicinal_interpretation
from azai.molecules.functional_groups import present_functional_groups
from azai.molecules.similarity import rank_by_similarity
from azai.reports.markdown import SAFETY_TEXT, generate_markdown_report
from azai.xylazine.reference import XYLAZINE, xylazine_profile

app = FastAPI(
    title="AZAI API",
    version=__version__,
    description="AI-Driven Xylazine Analytics and Innovation API for analytical chemistry research.",
)


@app.get("/health")
def health() -> dict[str, str]:
    """Return service health and package version."""
    return {"status": "ok", "version": __version__}


@app.get("/safety")
def safety() -> dict[str, str]:
    """Return the project safety statement."""
    return {"safety_notice": SAFETY_TEXT}


@app.get("/xylazine/profile")
def get_xylazine_profile() -> dict[str, object]:
    """Return the built-in xylazine molecular profile."""
    return xylazine_profile()


@app.post("/molecule/analyze", response_model=MoleculeAnalysisResponse)
def analyze_molecule(request: MoleculeRequest) -> MoleculeAnalysisResponse:
    """Calculate descriptors and interpretation for a molecule."""
    try:
        descriptors = calculate_descriptors(request.smiles)
    except Exception as exc:  # noqa: BLE001 - convert RDKit/parsing details into API error
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return MoleculeAnalysisResponse(
        label=request.label,
        smiles=request.smiles,
        descriptors=descriptors,
        functional_groups=present_functional_groups(request.smiles),
        interpretation=medicinal_interpretation(descriptors),
        safety_notice=SAFETY_TEXT,
    )


@app.post("/similarity/xylazine")
def similarity_to_xylazine(request: SimilarityRequest) -> dict[str, object]:
    """Rank molecules by fingerprint similarity to xylazine or a supplied reference."""
    reference = request.reference_smiles or XYLAZINE.smiles
    try:
        ranked = rank_by_similarity(request.smiles, reference)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    if request.labels:
        ranked.insert(0, "label", request.labels[: len(ranked)])
    return {"reference_smiles": reference, "results": ranked.to_dict(orient="records"), "safety_notice": SAFETY_TEXT}


@app.post("/probe/design")
def design_probes(request: ProbeDesignRequest) -> dict[str, object]:
    """Generate and prioritize transparent fluorescent probe concepts."""
    try:
        candidates = generate_probe_candidates(request.target_smiles, max_candidates=request.max_candidates)
        top = candidates[0] if candidates else {}
        experiments = recommended_experiment_plan(float(top.get("total_score", 0)), str(top.get("mechanism", "")), str(top.get("selectivity_concern", "")))
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"candidates": candidates, "experiment_plan": experiments, "safety_notice": SAFETY_TEXT}


@app.post("/literature/query")
def literature_query(request: LiteratureQueryRequest) -> dict[str, object]:
    """Retrieve relevant local text snippets from user-provided notes."""
    if not request.notes:
        return {"query": request.query, "results": [], "note": "No notes were supplied.", "safety_notice": SAFETY_TEXT}
    results = retrieve_relevant_chunks(request.query, request.notes, top_k=request.top_k)
    return {"query": request.query, "results": results, "safety_notice": SAFETY_TEXT}


@app.post("/report/markdown")
def report_markdown(request: MoleculeRequest) -> dict[str, str]:
    """Generate a Markdown report for a molecule."""
    try:
        report = generate_markdown_report(request.smiles, title=f"AZAI Report: {request.label or 'Molecule'}")
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"markdown": report, "safety_notice": SAFETY_TEXT}
