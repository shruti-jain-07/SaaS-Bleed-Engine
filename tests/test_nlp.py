import os
import sys
from pathlib import Path

# Add project root to sys.path for test discovery
root_path = Path(__file__).resolve().parent.parent
if str(root_path) not in sys.path:
    sys.path.insert(0, str(root_path))

import pytest
from Backend.App.Services.NLP.preprocess import TextPreprocessor
from Backend.App.Services.NLP.extractor import EntityExtractor
from Backend.App.Services.NLP.risk_engine import ContractRiskEngine


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