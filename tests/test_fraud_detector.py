"""
Tests for AI Fraud Detector — feature extraction & prediction
"""
import pytest
import numpy as np
import pandas as pd
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src', 'backend'))

from ml.ai_fraud_detector import BlockchainFraudDetector


def _make_transaction_df(n=50):
    """Generate a small synthetic transaction DataFrame."""
    np.random.seed(42)
    data = []
    for i in range(n):
        data.append({
            'block_number': 19000000 + i,
            'timestamp': 1700000000 + i * 12,
            'from_address': f'0x{"aa" * 20}',
            'to_address': f'0x{"bb" * 20}',
            'value_eth': np.random.exponential(1.0),
            'gas_price_gwei': np.random.normal(50, 15),
            'gas_used': 21000,
            'status': 1,
        })
    return pd.DataFrame(data)


class TestFeatureExtraction:
    """Tests for extract_features()"""

    def test_returns_correct_columns(self):
        detector = BlockchainFraudDetector()
        df = _make_transaction_df(10)
        features = detector.extract_features(df)
        assert list(features.columns) == detector.feature_names

    def test_correct_row_count(self):
        detector = BlockchainFraudDetector()
        df = _make_transaction_df(20)
        features = detector.extract_features(df)
        assert len(features) == 20

    def test_empty_df_returns_empty(self):
        detector = BlockchainFraudDetector()
        features = detector.extract_features(pd.DataFrame())
        assert features.empty

    def test_no_nans_in_output(self):
        detector = BlockchainFraudDetector()
        df = _make_transaction_df(10)
        features = detector.extract_features(df)
        assert not features.isnull().any().any()


class TestTrainAndPredict:
    """Tests for train_model() and predict()"""

    def test_train_and_predict_roundtrip(self):
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as f:
            model_path = f.name

        try:
            detector = BlockchainFraudDetector(model_path=model_path)
            df = _make_transaction_df(100)
            
            # Train
            success = detector.train_model(df)
            assert success is True
            assert detector.model is not None
            assert detector.scaler is not None
            assert os.path.exists(model_path)
            
            # Metrics should be recorded
            assert 'accuracy' in detector.metrics
            assert 'roc_auc' in detector.metrics
            
            # Predict
            results = detector.predict(df, threshold=0.5)
            assert results is not None
            assert 'fraud_probability' in results.columns
            assert 'is_fraud' in results.columns
            assert 'risk_level' in results.columns
            assert len(results) == len(df)

        finally:
            if os.path.exists(model_path):
                os.unlink(model_path)

    def test_save_load_roundtrip_joblib(self):
        """Verify model saves/loads correctly via joblib"""
        with tempfile.NamedTemporaryFile(suffix='.pkl', delete=False) as f:
            model_path = f.name

        try:
            # Train & save
            d1 = BlockchainFraudDetector(model_path=model_path)
            df = _make_transaction_df(100)
            d1.train_model(df)
            
            # Load into fresh detector
            d2 = BlockchainFraudDetector(model_path=model_path)
            loaded = d2.load_or_create_model()
            assert loaded is True
            assert d2.model is not None
            assert d2.metrics.get('accuracy') == d1.metrics.get('accuracy')

        finally:
            if os.path.exists(model_path):
                os.unlink(model_path)


class TestAnomalyDetection:
    """Tests for anomaly_detection()"""

    def test_anomaly_detection_returns_results(self):
        detector = BlockchainFraudDetector()
        df = _make_transaction_df(50)
        # Need scaler for anomaly detection
        detector.scaler = None  # Will create fresh one
        results = detector.anomaly_detection(df, contamination=0.1)
        assert results is not None
        assert 'anomaly_flag' in results.columns
        assert 'anomaly_score' in results.columns
