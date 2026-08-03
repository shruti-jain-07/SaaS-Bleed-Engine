import re
from typing import Any, Dict, List
from sqlalchemy.orm import Session
from backend.app.models.models import ContractAnalysisModel


class QueryEngine:

    @staticmethod
    def parse_and_query(query_str: str, db: Session) -> List[Dict[str, Any]]:
        """Parses simple natural language queries and filters contract records in DB."""
        query_str_clean = query_str.lower().strip()
        db_query = db.query(ContractAnalysisModel)

        # 1. Check for risk level keyword
        for risk in ["critical", "high", "medium", "low"]:
            if risk in query_str_clean:
                db_query = db_query.filter(
                    ContractAnalysisModel.risk_level == risk.upper()
                )
                break

        # 2. Check for value threshold (e.g., "over 10000" or "> 5000")
        value_match = re.search(
            r"(?:over|>|above|greater than)\s*\$?(\d+(?:\.\d+)?)",
            query_str_clean,
        )
        if value_match:
            min_val = float(value_match.group(1))
            db_query = db_query.filter(
                ContractAnalysisModel.contract_value >= min_val
            )

        # 3. Check for notice period (e.g., "30 days", "60 days notice")
        notice_match = re.search(r"(\d+)\s*(?:days|day)", query_str_clean)
        if notice_match:
            days = int(notice_match.group(1))
            db_query = db_query.filter(
                ContractAnalysisModel.notice_period_days == days
            )

        # 4. Fallback search on vendor_name or filename
        results = db_query.all()

        # If no specific filters matched, try a vendor string search
        if not results and query_str_clean:
            results = (
                db.query(ContractAnalysisModel)
                .filter(
                    ContractAnalysisModel.vendor_name.ilike(
                        f"%{query_str_clean}%"
                    )
                )
                .all()
            )

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