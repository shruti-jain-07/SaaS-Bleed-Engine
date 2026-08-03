from sqlalchemy import Column, Integer, String, Float, Boolean, Text, DateTime
from datetime import datetime
from Backend.App.DB.Session import Base


class ContractAnalysisModel(Base):
    __tablename__ = "contract_analysis"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    vendor_name = Column(String, index=True)
    contract_value = Column(Float)
    notice_period_days = Column(Integer)
    auto_renew = Column(Boolean)
    risk_level = Column(String)
    risk_score = Column(Integer)
    executive_summary = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)