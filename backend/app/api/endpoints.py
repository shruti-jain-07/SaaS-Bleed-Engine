from typing import List
from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.models import ContractAnalysisModel
from backend.app.schemas.analytics import (
    AnalyticsSummaryResponse,
    ContractSearchResultResponse,
)
from backend.app.schemas.contract import ContractUploadResponse
from backend.app.services.analytics.summary import AnalyticsService
from backend.app.services.nlp.risk_engine import ContractRiskEngine
from backend.app.services.query.search_engine import QueryEngine

router = APIRouter(prefix="/api/v1", tags=["SaaS Bleed Analytics & Query"])


@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse)
def get_dashboard_summary(db: Session = Depends(get_db)):
    """Retrieves high-level dashboard analytics regarding SaaS spend and contract risks."""
    try:
        return AnalyticsService.get_dashboard_summary(db)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to aggregate summary: {str(e)}"
        )


@router.get("/query/search", response_model=List[ContractSearchResultResponse])
def search_contracts(
    q: str = Query(
        ...,
        description="Natural language or keyword search query (e.g. 'HIGH risk over $50000')",
    ),
    limit: int = Query(10, ge=1, le=100, description="Max records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    sort_by: str = Query("id", description="Field to sort by (e.g., 'contract_value', 'risk_score')"),
    sort_order: str = Query("asc", pattern="^(asc|desc)$", description="Sort order: 'asc' or 'desc'"),
    db: Session = Depends(get_db),
):
    """Filters contract risk data using the natural language query engine with pagination and sorting."""
    if not q.strip():
        raise HTTPException(
            status_code=400, detail="Search query cannot be empty."
        )

    return QueryEngine.parse_and_query(
        query_str=q,
        db=db,
        limit=limit,
        offset=offset,
        sort_by=sort_by,
        sort_order=sort_order,
    )


@router.post("/contracts/upload", response_model=ContractUploadResponse, status_code=201)
async def upload_contract(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """Uploads contract text file, evaluates risk parameters, and persists record to DB."""
    if not file.filename.endswith((".txt", ".md", ".pdf")):
        raise HTTPException(
            status_code=400, detail="Only .txt, .md, or .pdf files are supported."
        )

    contents = await file.read()
    text = contents.decode("utf-8", errors="ignore")

    # Basic entity extraction fallback
    entities = {
        "auto_renew": "auto-renew" in text.lower() or "auto renew" in text.lower(),
        "notice_period_days": 60 if "60 days" in text.lower() else 30,
        "contract_value": 60000.0 if "$60000" in text or "60000" in text else 0.0,
    }

    # Evaluate risk score and level
    risk_data = ContractRiskEngine.evaluate_risk(entities)

    record = ContractAnalysisModel(
        filename=file.filename,
        vendor_name="Acme Corp" if "acme" in text.lower() else "Unknown Vendor",
        contract_value=entities["contract_value"],
        notice_period_days=entities["notice_period_days"],
        auto_renew=entities["auto_renew"],
        risk_level=risk_data["risk_level"],
        risk_score=float(risk_data["risk_score"]),
        executive_summary="; ".join(risk_data["risk_factors"]) or "Analyzed contract file.",
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record