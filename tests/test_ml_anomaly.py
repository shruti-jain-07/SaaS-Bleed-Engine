import pytest
import pandas as pd
from ML.features.builder import FeatureBuilder

def test_feature_builder_extraction():
    data = {
        "transaction_id": ["TXN1", "TXN2"],
        "date": ["2026-01-01", "2026-01-02"],
        "vendor_name": ["Zoom", "Zoom"],
        "amount": [100.0, 500.0],
        "department_id": ["ENG", "ENG"],
        "card_last_four": ["1234", "1234"]
    }
    df = pd.DataFrame(data)
    feature_matrix, processed_df = FeatureBuilder.extract_features(df)

    assert "amount_zscore_vendor" in feature_matrix.columns
    assert "days_since_last_txn" in feature_matrix.columns
    assert len(feature_matrix) == 2