from azai.literature.paper_parser import chunk_text
from azai.literature.retriever import TfidfLiteratureRetriever, retrieval_results_frame
from azai.literature.assistant import synthesize_literature_answer


def test_chunk_text_returns_chunks():
    chunks = chunk_text("amine probe fluorescence " * 100, chunk_size=120, overlap=20)
    assert len(chunks) > 1
    assert all(chunks)


def test_tfidf_retriever_finds_relevant_chunk():
    retriever = TfidfLiteratureRetriever()
    retriever.add_documents({"note": "PET fluorescent probes can respond to tertiary amines."})
    results = retriever.search("tertiary amines PET", top_k=1)
    assert results[0].source == "note"
    assert results[0].score >= 0
    frame = retrieval_results_frame(results)
    assert "text" in frame.columns


def test_literature_answer_mentions_question():
    retriever = TfidfLiteratureRetriever()
    retriever.add_documents({"note": "ICT and PET are common mechanisms for amine-responsive probes."})
    results = retriever.search("amine probe mechanisms", top_k=1)
    answer = synthesize_literature_answer("amine probe mechanisms", results)
    assert "Question" in answer
    assert "Recommended next step" in answer
