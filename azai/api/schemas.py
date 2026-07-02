"""Pydantic schemas for the AZAI API."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class MoleculeRequest(BaseModel):
    """Single molecule analysis request."""

    smiles: str = Field(..., min_length=1, description="Input molecule as a SMILES string.")
    label: str | None = Field(default=None, description="Optional molecule label.")


class MoleculeAnalysisResponse(BaseModel):
    """Single molecule analysis response."""

    label: str | None
    smiles: str
    descriptors: dict[str, Any]
    functional_groups: list[str]
    interpretation: list[str]
    safety_notice: str


class SimilarityRequest(BaseModel):
    """Batch similarity request against xylazine or another reference molecule."""

    smiles: list[str] = Field(..., min_length=1, description="Candidate molecules as SMILES strings.")
    labels: list[str] | None = Field(default=None, description="Optional labels matching the SMILES list.")
    reference_smiles: str | None = Field(default=None, description="Optional reference SMILES. Defaults to xylazine.")


class ProbeDesignRequest(BaseModel):
    """Probe generation request."""

    target_smiles: str = Field(..., min_length=1, description="Target molecule SMILES.")
    max_candidates: int = Field(default=12, ge=1, le=100)


class LiteratureQueryRequest(BaseModel):
    """Lightweight local literature query request."""

    query: str = Field(..., min_length=1)
    notes: list[str] = Field(default_factory=list, description="Short text notes, abstracts, or paper snippets.")
    top_k: int = Field(default=3, ge=1, le=10)
