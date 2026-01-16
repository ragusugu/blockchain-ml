"""
AI Fraud Detection Module
Detects suspicious blockchain transactions using Machine Learning
Integrates with ETL pipeline for intelligent analysis
"""
import os
import json
import pickle
import logging
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
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
    
    def __init__(self, model_path="fraud_model.pkl"):
        self.model = None
        self.scaler = None
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
    
    def load_or_create_model(self):
        """Load existing model or create new one"""
        if os.path.exists(self.model_path):
            logger.info(f"Loading model from {self.model_path}")
            with open(self.model_path, 'rb') as f:
                saved = pickle.load(f)
                self.model = saved['model']
                self.scaler = saved['scaler']
            return True
        else:
            logger.warning("No model found. Train a model first with train_model()")
            return False
    
    def extract_features(self, transaction_df, address_history_df=None):
        """
        Extract features from transaction data (optimized with vectorization)
        
        Args:
            transaction_df: DataFrame with current transactions
            address_history_df: Historical transaction data (optional)
        
        Returns:
            Feature matrix for model input
        """
        # Vectorized feature extraction for better performance
        features_list = []
        
        for idx, tx in transaction_df.iterrows():
            try:
                from_addr = tx['from_address']
                tx_time = tx['timestamp']
                
                features = {}
                
                # Feature 1: Transaction volume in last 1 hour
                if address_history_df is not None:
                    recent = address_history_df[
                        (address_history_df['from_address'] == from_addr) &
                        (address_history_df['timestamp'] > tx_time - 3600)
                    ]
                    features['tx_volume_1h'] = len(recent)
                    features['avg_value_1h'] = recent['value_eth'].mean() if len(recent) > 0 else tx['value_eth']
                else:
                    features['tx_volume_1h'] = 1
                    features['avg_value_1h'] = tx['value_eth']
                
                # Feature 2: Gas price Z-score
                gas_mean = 50  # Default gwei
                gas_std = 20
                features['gas_price_zscore'] = (tx['gas_price_gwei'] - gas_mean) / gas_std
                
                # Feature 3: Transaction value Z-score
                value_mean = 1.0  # Default ETH
                value_std = 5.0
                features['value_zscore'] = (tx['value_eth'] - value_mean) / value_std
                
                # Feature 4: Address age (simplified)
                if address_history_df is not None and len(address_history_df) > 0:
                    addr_history = address_history_df[address_history_df['from_address'] == from_addr]
                    if len(addr_history) > 0:
                        first_tx_time = addr_history['timestamp'].min()
                        features['address_age_days'] = (datetime.fromtimestamp(tx_time) - datetime.fromtimestamp(first_tx_time)).days
                    else:
                        features['address_age_days'] = 0
                else:
                    # Default: assume new address if no history available (deterministic, not random)
                    features['address_age_days'] = 0
                
                # Feature 5: Unique addresses
                if address_history_df is not None:
                    unique_addrs = address_history_df[
                        address_history_df['from_address'] == from_addr
                    ]['to_address'].nunique()
                else:
                    unique_addrs = 1
                features['unique_addresses'] = unique_addrs
                
                # Feature 6: Time of day
                features['time_of_day'] = datetime.fromtimestamp(tx_time).hour
                
                # Feature 7: Value deviation
                features['value_deviation'] = abs(tx['value_eth'] - value_mean) / value_std
                
                # Feature 8: Gas deviation
                features['gas_deviation'] = abs(tx['gas_price_gwei'] - gas_mean) / gas_std
                
                features_list.append(features)
            
            except Exception as e:
                logger.warning(f"Error extracting features for tx {idx}: {e}")
                continue
        
        features_df = pd.DataFrame(features_list)
        return features_df[self.feature_names] if len(features_df) > 0 else pd.DataFrame()
    
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
                (X['value_zscore'] > 2) & 
                (X['gas_price_zscore'] > 2) |
                (X['tx_volume_1h'] > 100)
            ).astype(int)
            
            # Add some random anomalies
            anomaly_indices = np.random.choice(len(X), size=max(1, len(X)//20), replace=False)
            y[anomaly_indices] = 1
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
        y_pred_proba = self.model.predict_proba(X_test_scaled)[:, 1]
        
        logger.info("\n" + "="*60)
        logger.info("🎯 MODEL PERFORMANCE")
        logger.info("="*60)
        logger.info(f"Accuracy: {self.model.score(X_test_scaled, y_test):.3f}")
        logger.info(f"ROC-AUC: {roc_auc_score(y_test, y_pred_proba):.3f}")
        logger.info("\nClassification Report:")
        logger.info(classification_report(y_test, y_pred, target_names=['Normal', 'Fraud']))
        logger.info("="*60 + "\n")
        
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
        fraud_probs = self.model.predict_proba(X_scaled)[:, 1]
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
        """Save model to disk"""
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler
            }, f)
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
                    'block': int(row['block_number']),
                    'from': str(row['from_address']),
                    'to': str(row['to_address']),
                    'value': float(row['value_eth']),
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
