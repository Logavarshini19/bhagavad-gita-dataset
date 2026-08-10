# Bhagavad Gita — Dataset & Gita Advisor

A simple pipeline and demo app that converts annotated Bhagavad Gita PDFs into a semantic knowledge graph and a FAISS-backed retriever + Streamlit UI that produces short, Gita‑inspired guidance.

Languages: English, Tamil, Sanskrit

## High level flow

```
                 OFFLINE PIPELINE
                 
Gita PDFs
   ↓
Poppler / OCR
   ↓
Text extraction
   ↓
Cleaning + structuring
   ↓
Annotations
   ↓
gemini_data.json
   ↓
   ├──────────────→ RDF Knowledge Graph
   │                 ↓
   │              TTL
   │
   └──────────────→ Sentence Transformer
                       ↓
                  Embeddings
                       ↓
                 L2 Normalize
                       ↓
                  FAISS HNSW
                       ↓
                    Index


                 ONLINE PIPELINE

User Question
      ↓
Sentence Transformer
      ↓
Query Embedding
      ↓
L2 Normalize
      ↓
FAISS HNSW Search
      ↓
Top-K Relevant Verses
      ↓
Advisor / Optional LLM
      ↓
Contextual Answer
      ↓
Streamlit
```

## Stack
- Language: Python
- UI: Streamlit
- Retrieval: FAISS (HNSW), Sentence-Transformers (local SBERT) or OpenAI embeddings (optional)
- Knowledge Graph: RDF/Turtle (rdflib)

## Quick start
1. Create and activate a virtualenv:
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```
2. Install dependencies:
```bash
pip install -r requirements.txt
# Note: rdflib is used by populate.py but not listed in requirements.txt — if missing, install:
pip install rdflib
```
3. Make sure gemini_data.json is present at the repo root (it is in this repo). If quick_retriever.py uses absolute paths (e.g. `d:/Bhagavad Gita/gemini_data.json`), edit quick_retriever.py or set DATAFILE/INDEX_DIR to point to the local files.

4. Run the Streamlit demo UI (recommended):
```bash
streamlit run app_streamlit.py
```
Or run the alternate UI:
```bash
streamlit run app.py
```

## Environment variables
- OPENAI_API_KEY: optional — if set and USE_OPENAI is enabled, the repo will call OpenAI embeddings (EMB_MODEL = `text-embedding-4`).
- USE_OPENAI: optional flag; quick_retriever sets it automatically if OPENAI_API_KEY is present.

## Models & similarity
- Local transformer: Sentence-Transformers `all-mpnet-base-v2` (used if available).
- OpenAI embedding model (optional): `text-embedding-4` (used when OPENAI_API_KEY is set).
- FAISS index: HNSW (`faiss.IndexHNSWFlat`) built over L2‑normalized vectors. Because vectors are normalized (`faiss.normalize_L2`), retrieval behaves like cosine similarity.

## Important files
- gemini_data.json — annotated verses (source data)
- Bhagavad_Gita.ttl, Bhagavad_Gita_Ontology.owx — ontology/schema
- populate.py — build RDF knowledge graph from gemini_data.json → TTL
- quick_retriever.py — embedding backends, FAISS index build/load, retrieval and small rule-based advisor
- app_streamlit.py / app.py — Streamlit frontends
- bhagavad-gita-populated-final.ttl — output TTL produced by populate.py

## Notes / suggestions
- quick_retriever.py contains hardcoded Windows paths for DATAFILE and INDEX_DIR. For portability, change them to relative paths (e.g., `Path("./gemini_data.json")`) or read them from environment variables.
- rdflib is required by populate.py; add it to requirements.txt if you plan to run the population step.
- The advisor logic in quick_retriever.py is rule-based (no generation LLM). If you want richer answers, you can plug an LLM (OpenAI, Ollama, local HF) after retrieval.

## Want this README improved?
If you want, I can:
- add step-by-step developer tasks (how to regenerate the TTL or rebuild FAISS index),
- modify quick_retriever.py to use relative paths and environment vars,
- add an example .env and a small gita_advisor.py wrapper to make `app.py` work out of the box.

---
Generated and added to the repository by an automated assistant.
