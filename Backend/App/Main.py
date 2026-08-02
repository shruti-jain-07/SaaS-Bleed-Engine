"""
SaaS Bleed Engine - API Entrypoint
"""

from fastapi import FastAPI

app = FastAPI(
    title="SaaS Bleed Engine API",
    description="Enterprise engine for identifying SaaS overspend, anomalous vendor charges, and contract loopholes.",
    version="0.1.0"
)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "SaaS-Bleed-Engine"}
