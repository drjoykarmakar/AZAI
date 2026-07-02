"""Simple text document parsing for the AZAI literature assistant."""

from __future__ import annotations

from pathlib import Path


def read_text_file(path: str | Path) -> str:
    """Read a UTF-8 compatible text-like document."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(str(p))
    return p.read_text(encoding="utf-8", errors="replace")


def chunk_text(text: str, chunk_size: int = 900, overlap: int = 120) -> list[str]:
    """Split text into overlapping chunks for lightweight retrieval."""
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be larger than overlap.")
    clean = " ".join(text.split())
    if not clean:
        return []
    chunks: list[str] = []
    start = 0
    while start < len(clean):
        end = start + chunk_size
        chunks.append(clean[start:end])
        if end >= len(clean):
            break
        start = end - overlap
    return chunks
