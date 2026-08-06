from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ContractUploadResponse(BaseModel):
    id: int
    filename: str
    vendor_name: Optional[str] = None
    contract_value: Optional[float] = None
    notice_period_days: Optional[int] = None
    auto_renew: bool = False
    risk_level: str
    risk_score: float
    executive_summary: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)