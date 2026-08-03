import pytest
from backend.app.services.nlp.extractor import EntityExtractor
from backend.app.services.nlp.preprocess import TextPreprocessor
from backend.app.services.nlp.risk_engine import ContractRiskEngine


def test_text_cleaning():
    raw_text = "Agreement   with  Zoom\n\nAuto - Renew Clause"
    cleaned = TextPreprocessor.clean_text(raw_text)
    assert "auto-renew" in cleaned.lower()


def test_entity_extraction():
    sample_text = (
        "Agreement between Company and AWS. Total amount $25,000. Requires 60"
        " days notice."
    )
    entities = EntityExtractor.extract_entities(sample_text)
    assert entities["contract_value"] == 25000.0
    assert entities["notice_period_days"] == 60


def test_risk_engine():
    entities = {
        "auto_renew": True,
        "notice_period_days": 60,
        "contract_value": 60000.0,
    }
    risk = ContractRiskEngine.evaluate_risk(entities)
    assert risk["risk_level"] == "CRITICAL"