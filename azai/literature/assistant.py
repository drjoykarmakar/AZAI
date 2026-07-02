"""Conservative answer synthesis over retrieved AZAI literature chunks."""

from __future__ import annotations

from azai.literature.retriever import RetrievedChunk


def synthesize_literature_answer(question: str, chunks: list[RetrievedChunk]) -> str:
    """Create a retrieval-grounded draft answer without pretending to know more than the index."""
    if not chunks:
        return "No relevant local literature chunks were retrieved. Add notes, abstracts, or papers first."
    lines = [
        f"Question: {question}",
        "",
        "Retrieval-grounded summary:",
        "The local index suggests the following points. Treat this as a starting point for reading, not a final literature review.",
    ]
    for idx, chunk in enumerate(chunks[:3], start=1):
        excerpt = chunk.text[:420].strip()
        lines.append(f"{idx}. Source {chunk.source}, chunk {chunk.chunk_id}, relevance {chunk.score}: {excerpt}")
    lines.extend(
        [
            "",
            "Recommended next step: inspect the cited source chunks, verify mechanisms in the primary literature, and avoid making performance claims without experimental validation.",
        ]
    )
    return "\n".join(lines)
