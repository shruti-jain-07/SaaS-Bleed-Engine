# SaaS Bleed Engine

An enterprise financial middleware solution designed to detect software spending anomalies, analyze vendor contracts for hidden terms or auto-renewals, and optimize SaaS cost efficiency.

---

## Architecture Overview

* **Data Layer:** Pandas data ingestion pipeline handling transaction logs, vendor rosters, and usage datasets.
* **ML Module (`/ML`):** Unsupervised anomaly detection via Scikit-Learn for identifying unusual spend spikes and recurring overcharges.
* **NLP Module (`/NLP`):** PDF text extraction via PyMuPDF coupled with LLM evaluation for contract terms and renewal clauses.
* **API Layer (`/Backend`):** FastAPI backend orchestrating data parsing, inference runs, and dashboard responses.

---

## Repository Structure

```text
ÃÄÄ Backend/    # FastAPI Application & API Endpoints
ÃÄÄ ML/         # Anomaly Detection Algorithms & Models
ÃÄÄ NLP/        # Contract Parsing & NLP Services
ÃÄÄ Data/       # Raw & Processed Datasets (Git-ignored)
ÃÄÄ Models/     # Model Checkpoints (Git-ignored)
ÀÄÄ Tests/      # Automated Tests
```
