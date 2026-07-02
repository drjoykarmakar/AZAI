# Literature Assistant

AZAI v0.4.0 includes a lightweight local literature assistant. It indexes pasted notes, abstracts, and text exports with TF-IDF and retrieves relevant chunks for a question.

This first version is intentionally simple:

- no cloud services are required;
- no external model downloads are required;
- answers are grounded in retrieved local chunks;
- output is framed as a reading aid, not a final literature review.

Future versions can add PDF parsing, sentence-transformer embeddings, ChromaDB, and richer citation management.

## Example

```bash
python examples/literature_assistant_demo.py
```

## Safety and scientific limits

The assistant should be used for analytical chemistry, public health research, fluorescent probe discovery, and medicinal chemistry education. It should not be used to develop harmful synthesis workflows or optimize abuse potential.
