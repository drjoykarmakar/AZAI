"""Run the lightweight AZAI local literature assistant demo."""

from pathlib import Path

from azai.literature.assistant import synthesize_literature_answer
from azai.literature.retriever import TfidfLiteratureRetriever

ROOT = Path(__file__).resolve().parents[1]
notes = ROOT / "data" / "examples" / "literature_notes.txt"

retriever = TfidfLiteratureRetriever()
retriever.add_paths([notes])
question = "What probe mechanisms are suitable for tertiary amines?"
results = retriever.search(question, top_k=3)
print(synthesize_literature_answer(question, results))
