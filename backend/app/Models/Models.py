from datetime import datetime
from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String, Text
from backend.app.db.session import Base


class ContractAnalysisModel(Base):
    __tablename__ = "contract_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True, nullable=False)
    vendor_name = Column(String, index=True)
    contract_value = Column(Float)
    notice_period_days = Column(Integer)
    auto_renew = Column(Boolean, default=False)
    risk_level = Column(String, index=True)
    risk_score = Column(Float)
    executive_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)