import pandas as pd
import joblib
from pathlib import Path
from typing import Dict, Any, List
from ML.features.builder import FeatureBuilder

class AnomalyDetector:
    def __init__(self, artifact_path: str = "Models/artifacts/isolation_forest.joblib"):
        self.artifact_path = Path(artifact_path)
        self.model = None
        self._load_model()

    def _load_model(self):
        if self.artifact_path.exists():
            self.model = joblib.load(self.artifact_path)
        else:
            raise FileNotFoundError(f"Model artifact not found at {self.artifact_path}. Train model first.")

    def detect_anomalies(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Runs inference on input transactions and returns scored anomalies.
        """
        if df.empty:
            return []

        # 1. Feature Extraction
        feature_matrix, processed_df = FeatureBuilder.extract_features(df)

        # 2. Predict Anomaly Labels (-1 for anomaly, 1 for normal)
        predictions = self.model.predict(feature_matrix)
        
        # 3. Decision Function (Lower score = higher anomaly probability)
        scores = self.model.decision_function(feature_matrix)

        processed_df['is_anomaly'] = predictions == -1
        processed_df['anomaly_score'] = scores

        # Filter and structure anomalies
        anomalies_df = processed_df[processed_df['is_anomaly']].copy()
        
        anomalies = []
        for _, row in anomalies_df.iterrows():
            anomalies.append({
                "transaction_id": str(row["transaction_id"]),
                "vendor_name": str(row["vendor_name"]),
                "amount": float(row["amount"]),
                "anomaly_score": float(row["anomaly_score"]),
                "department_id": str(row["department_id"]),
                "flag_reason": "Statistical outlier in vendor amount, department spend ratio, or billing frequency"
            })

        return anomalies