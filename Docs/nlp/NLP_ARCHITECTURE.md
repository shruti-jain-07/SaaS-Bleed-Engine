# Contract Intelligence & NLP Engine Architecture

## Overview
The Contract Intelligence module extracts structured entities, evaluates legal risk exposure, and generates executive summaries from uploaded SaaS vendor contract PDFs.

## Pipeline Components
1. **Text Ingestion (`pdf_loader.py`):** Uses PyMuPDF (`fitz`) to extract text layers from PDFs with OCR fallback detection.
2. **Preprocessing (`preprocess.py`):** Cleans control characters, standardizes whitespace, and normalizes legal terminology.
3. **Entity Extraction (`extractor.py`):** Employs regex heuristics to isolate vendor names, contract values, notice periods, and auto-renewal clauses.
4. **Risk Scoring Engine (`risk_engine.py`):** Calculates legal lock-in risk scores (LOW, MEDIUM, HIGH, CRITICAL) based on terms.
5. **Executive Summarizer (`summarizer.py`):** Synthesizes extracted metadata into concise summaries.
6. **API Endpoint (`Backend/App/API/Endpoints.py`):** Exposes `POST /contracts/analyze` and persists results to SQLite/PostgreSQL.