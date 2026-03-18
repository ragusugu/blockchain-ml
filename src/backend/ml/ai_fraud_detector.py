"""
AI Fraud Detection Module
Detects suspicious blockchain transactions using Machine Learning
Integrates with ETL pipeline for intelligent analysis
"""
import os
import json
import hashlib
import logging
import numpy as np
import pandas as pd
import joblib
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

logger = logging.getLogger(__name__)


class BlockchainFraudDetector:
    """
    AI-powered fraud/anomaly detection for blockchain transactions
    
    Features used:
    - Transaction volume from address
    - Gas price anomalies
    - Address behavior patterns
    - Time-based patterns
    - Value transfer anomalies
    """
    
    def __init__(self, model_path: str = "fraud_model.pkl"):
        self.model = None
        self.scaler = None
        self.metrics = {}
        self.model_path = model_path
        self.feature_names = [
            'tx_volume_1h',      # Transactions in last 1 hour
            'avg_value_1h',      # Average ETH value in last 1h
            'gas_price_zscore',  # Z-score of gas price
            'value_zscore',      # Z-score of transaction value
            'address_age_days',  # Days since first transaction
            'unique_addresses',  # Unique addresses interacted with
            'time_of_day',       # Hour of day (0-23)
            'value_deviation',   # Deviation from user's average
            'gas_deviation'      # Deviation from network average
        ]
        # Auto-load model if the file exists
        self.load_or_create_model()
    
    def load_or_create_model(self):
        """Load existing model or create new one (supports both joblib and legacy pickle)"""
        if os.path.exists(self.model_path):
            logger.info(f"Loading model from {self.model_path}")
            try:
                saved = joblib.load(self.model_path)
            except Exception:
                # Fallback for legacy pickle files
                import pickle
                with open(self.model_path, 'rb') as f:
                    saved = pickle.load(f)
                logger.info("Loaded legacy pickle model — will re-save as joblib")
                self.model = saved['model']
                self.scaler = saved['scaler']
                self.metrics = saved.get('metrics', {})
                self._save_model()  # Re-save in joblib format
                return True
            self.model = saved['model']
            self.scaler = saved['scaler']
            self.metrics = saved.get('metrics', {})
            return True
        else:
            logger.warning("No model found. Train a model first with train_model()")
            return False
    
    def extract_features(self, transaction_df, address_history_df=None):
        """
        Extract features from transaction data using vectorized pandas operations.
        
        Args:
            transaction_df: DataFrame with current transactions
            address_history_df: Historical transaction data (optional)
        
        Returns:
            Feature matrix for model input
        """
        df = transaction_df.copy()
        
        # Normalize column names — handle both naming conventions
        if 'from_address' not in df.columns and 'from_addr' in df.columns:
            df['from_address'] = df['from_addr']
        if 'to_address' not in df.columns and 'to_addr' in df.columns:
            df['to_address'] = df['to_addr']
        if 'timestamp' not in df.columns and 'block_timestamp' in df.columns:
            df['timestamp'] = df['block_timestamp']
        if 'value_eth' not in df.columns and 'value' in df.columns:
            df['value_eth'] = df['value']
        if 'gas_price_gwei' not in df.columns and 'gas_price' in df.columns:
            df['gas_price_gwei'] = df['gas_price']

        # Drop rows missing critical fields
        required = ['from_address', 'timestamp']
        for col in required:
            if col not in df.columns:
                logger.error(f"Missing required column: {col}")
                return pd.DataFrame()
        
        df = df.dropna(subset=required)
        df['timestamp'] = pd.to_numeric(df['timestamp'], errors='coerce')
        df = df.dropna(subset=['timestamp'])
        
        if df.empty:
            return pd.DataFrame()

        # Baseline stats (for production, compute from recent network data)
        GAS_MEAN, GAS_STD = 50.0, 20.0
        VALUE_MEAN, VALUE_STD = 1.0, 5.0

        # Vectorized feature computation
        gas_price = df['gas_price_gwei'].fillna(0).astype(float)
        value_eth = df['value_eth'].fillna(0).astype(float)

        features = pd.DataFrame(index=df.index)
        features['gas_price_zscore'] = (gas_price - GAS_MEAN) / max(GAS_STD, 1e-6)
        features['value_zscore'] = (value_eth - VALUE_MEAN) / max(VALUE_STD, 1e-6)
        features['value_deviation'] = (value_eth - VALUE_MEAN).abs() / max(VALUE_STD, 1e-6)
        features['gas_deviation'] = (gas_price - GAS_MEAN).abs() / max(GAS_STD, 1e-6)
        features['time_of_day'] = pd.to_datetime(df['timestamp'], unit='s').dt.hour

        # History-dependent features (default when no history)
        if address_history_df is not None and not address_history_df.empty:
            hist = address_history_df.copy()
            ts_col = 'timestamp' if 'timestamp' in hist.columns else 'block_timestamp' if 'block_timestamp' in hist.columns else None
            
            if ts_col and 'from_address' in hist.columns:
                # Pre-compute per-address aggregates for speed
                addr_groups = hist.groupby('from_address')
                vol_1h = {}
                avg_1h = {}
                age_days = {}
                unique_addrs = {}
                
                for addr, group in addr_groups:
                    vol_1h[addr] = len(group)  # Simplified — full 1h window requires per-tx join
                    avg_1h[addr] = group['value_eth'].mean() if 'value_eth' in group.columns else 0
                    age_days[addr] = max(0, (group[ts_col].max() - group[ts_col].min()) / 86400)
                    unique_addrs[addr] = group['to_address'].nunique() if 'to_address' in group.columns else 1
                
                features['tx_volume_1h'] = df['from_address'].map(vol_1h).fillna(1).astype(int)
                features['avg_value_1h'] = df['from_address'].map(avg_1h).fillna(value_eth)
                features['address_age_days'] = df['from_address'].map(age_days).fillna(0).astype(int)
                features['unique_addresses'] = df['from_address'].map(unique_addrs).fillna(1).astype(int)
            else:
                features['tx_volume_1h'] = 1
                features['avg_value_1h'] = value_eth
                features['address_age_days'] = 0
                features['unique_addresses'] = 1
        else:
            features['tx_volume_1h'] = 1
            features['avg_value_1h'] = value_eth
            features['address_age_days'] = 0
            features['unique_addresses'] = 1

        # Reorder to match expected feature names
        try:
            return features[self.feature_names]
        except KeyError as e:
            logger.error(f"Missing feature columns: {e}")
            return pd.DataFrame()
    
    def train_model(self, transactions_df, labels_df=None):
        """
        Train fraud detection model
        
        Args:
            transactions_df: Transaction data with all details
            labels_df: Known fraud labels (1=fraud, 0=normal)
        """
        logger.info("🧠 Training fraud detection model...")
        
        # Extract features
        X = self.extract_features(transactions_df)
        
        if X.empty:
            logger.error("❌ Could not extract features")
            return False
        
        # Generate synthetic labels if not provided
        if labels_df is None:
            logger.info("Generating synthetic training data (for demo)...")
            # Simple heuristic: flag high value + high gas price + new address
            y = (
                ((X['value_zscore'] > 2) & 
                (X['gas_price_zscore'] > 2)) |
                (X['tx_volume_1h'] > 100)
            ).astype(int)
            
            # Add deterministic anomalies based on feature combinations (reproducible)
            # Flag transactions with extreme deviations
            anomaly_mask = (
                (X['value_deviation'] > 3) | 
                (X['gas_deviation'] > 3) |
                ((X['tx_volume_1h'] > 50) & (X['address_age_days'] < 1))
            )
            y = (y | anomaly_mask).astype(int)
        else:
            y = labels_df
        
        logger.info(f"Training on {len(X)} samples, {y.sum()} fraud cases ({y.mean()*100:.1f}%)")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train RandomForest
        logger.info("Training RandomForest classifier...")
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=15,
            min_samples_split=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        proba = self.model.predict_proba(X_test_scaled)
        # Guard against single-class splits where predict_proba returns 1 column
        if proba.shape[1] >= 2:
            y_pred_proba = proba[:, 1]
        else:
            y_pred_proba = proba[:, 0]
        
        logger.info("\n" + "="*60)
        logger.info("🎯 MODEL PERFORMANCE")
        logger.info("="*60)
        accuracy = self.model.score(X_test_scaled, y_test)
        # roc_auc requires both classes present
        if len(set(y_test)) < 2:
            roc_auc = 0.0
        else:
            roc_auc = roc_auc_score(y_test, y_pred_proba)
        logger.info(f"Accuracy: {accuracy:.3f}")
        logger.info(f"ROC-AUC: {roc_auc:.3f}")
        logger.info("\nClassification Report:")
        if len(set(y_test)) >= 2:
            logger.info(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))
        else:
            logger.info(classification_report(y_test, y_pred))
        logger.info("="*60 + "\n")
        
        # Store metrics alongside model
        self.metrics = {
            'accuracy': round(accuracy, 4),
            'roc_auc': round(roc_auc, 4),
            'train_samples': len(X_train),
            'test_samples': len(X_test),
            'fraud_rate': round(float(y.mean()), 4),
            'trained_at': datetime.now().isoformat(),
        }
        
        # Save model
        self._save_model()
        
        return True
    
    def predict(self, transaction_df, threshold=0.5):
        """
        Predict fraud probability for transactions (optimized with batch processing)
        
        Args:
            transaction_df: Transaction data
            threshold: Probability threshold for flagging as fraud (0-1)
        
        Returns:
            DataFrame with predictions and fraud flags
        """
        if self.model is None:
            logger.error("❌ Model not trained. Call train_model() first")
            return None
        
        # Batch processing for efficiency
        X = self.extract_features(transaction_df)
        
        if X.empty:
            logger.error("❌ Could not extract features")
            return None
        
        # Scale and predict
        X_scaled = self.scaler.transform(X)
        proba = self.model.predict_proba(X_scaled)
        fraud_probs = proba[:, 1] if proba.shape[1] >= 2 else proba[:, 0]
        fraud_flags = (fraud_probs >= threshold).astype(int)
        
        # Create results DataFrame
        results = transaction_df.copy()
        results['fraud_probability'] = fraud_probs
        results['is_fraud'] = fraud_flags
        results['risk_level'] = results['fraud_probability'].apply(
            lambda x: 'CRITICAL' if x > 0.8 else 'HIGH' if x > 0.6 else 'MEDIUM' if x > 0.4 else 'LOW'
        )
        
        return results
    
    def anomaly_detection(self, transaction_df, contamination=0.1):
        """
        Alternative: Unsupervised anomaly detection using IsolationForest
        
        Args:
            transaction_df: Transaction data
            contamination: Expected fraction of anomalies (0-1)
        
        Returns:
            DataFrame with anomaly scores
        """
        logger.info("🔍 Running unsupervised anomaly detection...")
        
        # Extract features
        X = self.extract_features(transaction_df)
        
        if X.empty:
            logger.error("❌ Could not extract features")
            return None
        
        # Scale
        X_scaled = self.scaler.fit_transform(X) if self.scaler else StandardScaler().fit_transform(X)
        
        # IsolationForest
        iso_forest = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_jobs=-1
        )
        anomaly_flags = iso_forest.fit_predict(X_scaled)
        anomaly_scores = iso_forest.score_samples(X_scaled)
        
        # Create results
        results = transaction_df.copy()
        results['anomaly_flag'] = (anomaly_flags == -1).astype(int)  # -1 = anomaly
        results['anomaly_score'] = -anomaly_scores  # Normalize to 0-1
        
        logger.info(f"Detected {results['anomaly_flag'].sum()} anomalies ({results['anomaly_flag'].mean()*100:.1f}%)")
        
        return results
    
    def _save_model(self):
        """Save model to disk using joblib (safer than pickle)"""
        payload = {
            'model': self.model,
            'scaler': self.scaler,
            'metrics': getattr(self, 'metrics', {}),
        }
        joblib.dump(payload, self.model_path)
        logger.info(f"✅ Model saved to {self.model_path}")
    

    
    def get_feature_importance(self):
        """Get feature importance from trained model"""
        if self.model is None:
            logger.error("❌ Model not trained")
            return None
        
        importance_dict = dict(zip(self.feature_names, self.model.feature_importances_))
        sorted_importance = sorted(importance_dict.items(), key=lambda x: x[1], reverse=True)
        
        logger.info("\n🎯 FEATURE IMPORTANCE")
        logger.info("="*40)
        for feature, importance in sorted_importance:
            logger.info(f"{feature:25s}: {importance:.3f}")
        logger.info("="*40 + "\n")
        
        return importance_dict
    
    def generate_report(self, results_df, output_file="fraud_report.json"):
        """Generate detailed fraud report"""
        suspicious = results_df[results_df['is_fraud'] == 1]
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_transactions': len(results_df),
            'suspicious_transactions': len(suspicious),
            'fraud_rate': float(len(suspicious) / len(results_df)) if len(results_df) > 0 else 0,
            'risk_distribution': results_df['risk_level'].value_counts().to_dict(),
            'avg_fraud_probability': float(results_df['fraud_probability'].mean()),
            'high_risk': [
                {
                    'block': int(row.get('block_number', 0)),
                    'from': str(row.get('from_address') or row.get('from_addr', '')),
                    'to': str(row.get('to_address') or row.get('to_addr', '')),
                    'value': float(row.get('value_eth') or row.get('value', 0)),
                    'fraud_prob': float(row['fraud_probability']),
                    'risk': row['risk_level']
                }
                for idx, row in suspicious.iterrows()
            ][:10]  # Top 10
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"✅ Report saved to {output_file}")
        return report
