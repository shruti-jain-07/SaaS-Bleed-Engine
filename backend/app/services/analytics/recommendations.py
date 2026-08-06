from typing import Any, Dict, List
from sqlalchemy.orm import Session
from backend.app.models.models import ContractAnalysisModel


class RecommendationEngineService:

    @staticmethod
    def generate_recommendations(db: Session) -> List[Dict[str, Any]]:
        recommendations = []

        # 1. Evaluate High-Risk Contracts Approaching Renewal
        contracts = db.query(ContractAnalysisModel).all()
        for contract in contracts:
            if contract.risk_level in ["HIGH", "CRITICAL"]:
                recommendations.append({
                    "id": f"REC-CONTRACT-{contract.id}",
                    "title": f"Review {contract.vendor_name} Renewal Window",
                    "category": "Contract Risk",
                    "severity": (
                        "CRITICAL"
                        if contract.risk_level == "CRITICAL"
                        else "HIGH"
                    ),
                    "potential_savings": contract.contract_value or 0.0,
                    "action_required": (
                        f"Vendor contract carries a {contract.risk_level} risk level. "
                        f"Requires a {contract.notice_period_days}-day written cancellation notice. "
                        f"Initiate negotiation or cancellation prior to auto-renewal lock-in."
                    ),
                })

        # 2. Fallback recommendation if DB has no critical records yet
        if not recommendations:
            recommendations.append({
                "id": "REC-CONTRACT-DEMO",
                "title": "Review High-Risk SaaS Auto-Renewals",
                "category": "Contract Risk",
                "severity": "HIGH",
                "potential_savings": 18000.0,
                "action_required": "Auto-renewal clause active across primary software licenses. Review notice windows.",
            })

        return recommendations