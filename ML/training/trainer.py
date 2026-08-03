import pandas as pd
import joblib
from pathlib import Path
from sklearn.ensemble import IsolationForest
from ML.features.builder import FeatureBuilder

class AnomalyModelTrainer:
    def __init__(self, contamination: float = 0.05, random_state: int = 42):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
            n_jobs=-1
        )

    def train_and_save(self, df: pd.DataFrame, artifact_path: str = "Models/artifacts/isolation_forest.joblib") -> str:
        """
        Extracts features, trains the Isolation Forest model, and serializes the trained artifact.
        """
        # 1. Feature Extraction
        feature_matrix, _ = FeatureBuilder.extract_features(df)

        # 2. Fit Model
        self.model.fit(feature_matrix)

        # 3. Save Artifact
        save_path = Path(artifact_path)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, save_path)

        return str(save_path)