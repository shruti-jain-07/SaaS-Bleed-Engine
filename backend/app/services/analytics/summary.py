from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.app.models.models import ContractAnalysisModel
from backend.app.db.repository import TransactionRepository


class AnalyticsService:
    @staticmethod
    def get_dashboard_summary(db: Session) -> Dict[str, Any]:
        """
        Aggregates transaction and contract intelligence metrics
        for executive dashboard reporting.
        """
        # Fetch transactions via repository
        repo = TransactionRepository(db)
        transactions = repo.get_all_transactions()

        total_spend = sum(t.amount for t in transactions) if transactions else 0.0
        total_transactions = len(transactions)

        # Fetch contract analysis records
        contracts = db.query(ContractAnalysisModel).all()
        total_contracts = len(contracts)
        
        risk_breakdown = {
            "LOW": 0,
            "MEDIUM": 0,
            "HIGH": 0,
            "CRITICAL": 0
        }
        
        high_risk_contract_count = 0
        total_contract_value = 0.0

        for contract in contracts:
            level = (contract.risk_level or "LOW").upper()
            if level in risk_breakdown:
                risk_breakdown[level] += 1
            
            if level in ["HIGH", "CRITICAL"]:
                high_risk_contract_count += 1
                
            if contract.contract_value:
                total_contract_value += contract.contract_value

        return {
            "total_saas_spend": round(total_spend, 2),
            "total_transactions": total_transactions,
            "total_analyzed_contracts": total_contracts,
            "total_contract_value": round(total_contract_value, 2),
            "high_risk_contracts_count": high_risk_contract_count,
            "contract_risk_distribution": risk_breakdown
        }