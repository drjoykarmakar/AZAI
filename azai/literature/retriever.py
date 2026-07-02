"""A lightweight local literature retriever using TF-IDF.

This fallback retriever keeps AZAI useful without large model downloads. Optional
sentence-transformer or ChromaDB integrations can be added later behind the same interface.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from azai.literature.paper_parser import chunk_text, read_text_file


@dataclass(frozen=True)
class RetrievedChunk:
    source: str
    chunk_id: int
    score: float
    text: str


class TfidfLiteratureRetriever:
    """Small local retriever for notes, abstracts, and text exports."""

    def __init__(self) -> None:
        self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
        self.chunks: list[RetrievedChunk] = []
        self._matrix = None

    def add_documents(self, documents: dict[str, str]) -> None:
        """Add named raw-text documents to the index."""
        chunks: list[RetrievedChunk] = []
        for source, text in documents.items():
            for idx, chunk in enumerate(chunk_text(text)):
                chunks.append(RetrievedChunk(source=source, chunk_id=idx, score=0.0, text=chunk))
        if not chunks:
            raise ValueError("No text chunks were provided.")
        self.chunks = chunks
        self._matrix = self.vectorizer.fit_transform([chunk.text for chunk in self.chunks])

    def add_paths(self, paths: list[str | Path]) -> None:
        """Read and index local text files."""
        documents = {Path(path).name: read_text_file(path) for path in paths}
        self.add_documents(documents)

    def search(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Return the most relevant text chunks for a query."""
        if self._matrix is None:
            raise ValueError("No documents have been indexed.")
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self._matrix).ravel()
        order = scores.argsort()[::-1][:top_k]
        return [
            RetrievedChunk(
                source=self.chunks[i].source,
                chunk_id=self.chunks[i].chunk_id,
                score=round(float(scores[i]), 4),
                text=self.chunks[i].text,
            )
            for i in order
        ]


def retrieval_results_frame(results: list[RetrievedChunk]) -> pd.DataFrame:
    """Convert retrieval results to a DataFrame."""
    return pd.DataFrame([r.__dict__ for r in results])
