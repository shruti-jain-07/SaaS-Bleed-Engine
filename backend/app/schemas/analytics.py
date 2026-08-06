from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class RiskDistributionSchema(BaseModel):
    CRITICAL: int = 0
    HIGH: int = 0
    MEDIUM: int = 0
    LOW: int = 0


class AnalyticsSummaryResponse(BaseModel):
    total_saas_spend: float = 0.0
    total_transactions: int = 0
    total_analyzed_contracts: int = 0
    total_contract_value: float = 0.0
    high_risk_contracts_count: int = 0
    contract_risk_distribution: RiskDistributionSchema = Field(
        default_factory=RiskDistributionSchema
    )


class ContractSearchResultResponse(BaseModel):
    id: int
    filename: str
    vendor_name: Optional[str] = None
    contract_value: Optional[float] = None
    notice_period_days: Optional[int] = None
    auto_renew: Optional[bool] = False
    risk_level: Optional[str] = None
    risk_score: Optional[float] = None
    executive_summary: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)