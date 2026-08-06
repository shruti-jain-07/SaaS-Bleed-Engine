import re
from typing import Any, Dict, List
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session
from backend.app.models.models import ContractAnalysisModel


class QueryEngine:

    @staticmethod
    def parse_and_query(
        query_str: str,
        db: Session,
        limit: int = 10,
        offset: int = 0,
        sort_by: str = "id",
        sort_order: str = "asc",
    ) -> List[Dict[str, Any]]:
        """Parses natural language query filters and fetches paginated/sorted contract records from DB."""
        query_str_clean = query_str.lower().strip()
        db_query = db.query(ContractAnalysisModel)

        # 1. Filter by risk level keyword
        for risk in ["critical", "high", "medium", "low"]:
            if risk in query_str_clean:
                db_query = db_query.filter(
                    ContractAnalysisModel.risk_level == risk.upper()
                )
                break

        # 2. Filter by contract value threshold
        value_match = re.search(
            r"(?:over|>|above|greater than)\s*\$?(\d+(?:\.\d+)?)",
            query_str_clean,
        )
        if value_match:
            min_val = float(value_match.group(1))
            db_query = db_query.filter(
                ContractAnalysisModel.contract_value >= min_val
            )

        # 3. Filter by notice period days
        notice_match = re.search(r"(\d+)\s*(?:days|day)", query_str_clean)
        if notice_match:
            days = int(notice_match.group(1))
            db_query = db_query.filter(
                ContractAnalysisModel.notice_period_days == days
            )

        # 4. Fallback keyword search on vendor_name if primary filters didn't narrow down results
        if not db_query.count() and query_str_clean:
            db_query = db.query(ContractAnalysisModel).filter(
                ContractAnalysisModel.vendor_name.ilike(
                    f"%{query_str_clean}%"
                )
            )

        # 5. Dynamic Sorting
        sort_column = getattr(ContractAnalysisModel, sort_by, ContractAnalysisModel.id)
        if sort_order.lower() == "desc":
            db_query = db_query.order_by(desc(sort_column))
        else:
            db_query = db_query.order_by(asc(sort_column))

        # 6. Pagination Execution
        results = db_query.offset(offset).limit(limit).all()

        return [
            {
                "id": c.id,
                "filename": c.filename,
                "vendor_name": c.vendor_name,
                "contract_value": c.contract_value,
                "notice_period_days": c.notice_period_days,
                "auto_renew": c.auto_renew,
                "risk_level": c.risk_level,
                "risk_score": c.risk_score,
                "executive_summary": c.executive_summary,
            }
            for c in results
        ]