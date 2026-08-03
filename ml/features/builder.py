import pandas as pd
import numpy as np

class FeatureBuilder:
    @staticmethod
    def extract_features(df: pd.DataFrame):
        processed_df = df.copy()
        
        # Date sorting & conversion
        processed_df['date'] = pd.to_datetime(processed_df['date'])
        processed_df = processed_df.sort_values('date').reset_index(drop=True)
        
        # 1. Vendor Z-Score Baseline
        vendor_stats = processed_df.groupby('vendor_name')['amount'].agg(['mean', 'std']).reset_index()
        processed_df = processed_df.merge(vendor_stats, on='vendor_name', how='left')
        
        processed_df['std'] = processed_df['std'].fillna(0).replace(0, 1.0)
        processed_df['amount_zscore_vendor'] = (processed_df['amount'] - processed_df['mean']) / processed_df['std']
        
        # 2. Days Since Last Transaction
        processed_df['days_since_last_txn'] = (
            processed_df.groupby('vendor_name')['date']
            .diff()
            .dt.total_seconds() / (24 * 3600)
        ).fillna(0)
        
        # 3. Department Spend Ratio
        dept_total = processed_df.groupby('department_id')['amount'].transform('sum')
        processed_df['dept_spend_ratio'] = processed_df['amount'] / (dept_total.replace(0, 1.0))

        # Select model features
        feature_cols = ['amount', 'amount_zscore_vendor', 'days_since_last_txn', 'dept_spend_ratio']
        feature_matrix = processed_df[feature_cols].copy()
        
        return feature_matrix, processed_df