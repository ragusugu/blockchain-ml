"""
AI Model Training Script
Train fraud detection model on blockchain data
Generates synthetic training data for demo
"""
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from backend.ml.ai_fraud_detector import BlockchainFraudDetector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def generate_random_hex(length):
    """Generate random hex string"""
    return ''.join(np.random.choice(list('0123456789abcdef'), size=length))


def generate_synthetic_transactions(n_transactions=5000, fraud_rate=0.05):
    """
    Generate synthetic blockchain transaction data for training
    
    Args:
        n_transactions: Number of transactions to generate
        fraud_rate: Percentage of fraudulent transactions (0-1)
    
    Returns:
        DataFrame with transaction data
    """
    logger.info(f"📊 Generating {n_transactions} synthetic transactions...")
    
    np.random.seed(42)
    data = []
    
    # Generate legitimate transactions
    n_normal = int(n_transactions * (1 - fraud_rate))
    for i in range(n_normal):
        data.append({
            'block_number': 19000 + (i // 300),
            'block_hash': f"0x{generate_random_hex(64)}",
            'timestamp': int((datetime.now() - timedelta(days=90)).timestamp()) + i * 1200,
            'transaction_hash': f"0x{generate_random_hex(64)}",
            'transaction_index': i % 300,
            'from_address': f"0x{generate_random_hex(40)}",
            'to_address': f"0x{generate_random_hex(40)}",
            'value_eth': np.random.exponential(1.0),  # Most transactions are small
            'gas': np.random.choice([21000, 65000, 100000, 200000]),
            'gas_price_gwei': np.random.normal(50, 15),
            'gas_used': np.random.randint(21000, 200000),
            'cumulative_gas_used': np.random.randint(1000000, 30000000),
            'status': 1,  # Success
            'contract_address': None,
            'effective_gas_price': np.random.normal(50, 15),
        })
    
    # Generate fraudulent transactions (abnormal patterns)
    n_fraud = n_transactions - n_normal
    for i in range(n_fraud):
        # Fraud pattern: High value + High gas price + Unusual time
        data.append({
            'block_number': 19000 + ((n_normal + i) // 300),
            'block_hash': f"0x{generate_random_hex(64)}",
            'timestamp': int((datetime.now() - timedelta(days=90)).timestamp()) + (n_normal + i) * 1200,
            'transaction_hash': f"0x{generate_random_hex(64)}",
            'transaction_index': (n_normal + i) % 300,
            'from_address': f"0x{generate_random_hex(40)}",
            'to_address': f"0x{generate_random_hex(40)}",
            'value_eth': np.random.exponential(50.0),  # Much higher values
            'gas': np.random.choice([21000, 65000, 100000, 200000]),
            'gas_price_gwei': np.random.normal(150, 50),  # Much higher gas price
            'gas_used': np.random.randint(100000, 300000),
            'cumulative_gas_used': np.random.randint(1000000, 30000000),
            'status': np.random.choice([0, 1], p=[0.3, 0.7]),  # Higher failure rate
            'contract_address': None,
            'effective_gas_price': np.random.normal(150, 50),
        })
    
    df = pd.DataFrame(data)
    logger.info(f"✅ Generated {len(df)} transactions ({n_fraud} fraudulent)")
    
    return df


def main():
    """Train fraud detection model"""
    
    logger.info("🚀 BLOCKCHAIN FRAUD DETECTION - MODEL TRAINING")
    logger.info("="*60)
    
    # Step 1: Generate training data
    df_train = generate_synthetic_transactions(n_transactions=5000, fraud_rate=0.05)
    
    # Step 2: Initialize detector
    detector = BlockchainFraudDetector(model_path="fraud_model.pkl")
    
    # Step 3: Train model
    detector.train_model(df_train)
    
    # Step 4: Get feature importance
    importance = detector.get_feature_importance()
    
    # Step 5: Test on new data
    logger.info("\n🧪 TESTING MODEL ON NEW DATA")
    logger.info("="*60)
    
    df_test = generate_synthetic_transactions(n_transactions=1000, fraud_rate=0.10)
    results = detector.predict(df_test, threshold=0.5)
    
    logger.info(f"\n📊 Prediction Results:")
    logger.info(f"  Total: {len(results)}")
    logger.info(f"  Flagged as fraud: {results['is_fraud'].sum()}")
    logger.info(f"  Flagged as normal: {(results['is_fraud'] == 0).sum()}")
    logger.info(f"  Fraud probability range: {results['fraud_probability'].min():.3f} - {results['fraud_probability'].max():.3f}")
    
    # Step 6: Anomaly detection
    logger.info("\n🔍 ANOMALY DETECTION (Unsupervised)")
    logger.info("="*60)
    
    anomaly_results = detector.anomaly_detection(df_test, contamination=0.10)
    logger.info(f"Anomalies detected: {anomaly_results['anomaly_flag'].sum()}")
    
    # Step 7: Generate report
    logger.info("\n📋 GENERATING REPORT")
    logger.info("="*60)
    
    report = detector.generate_report(results, output_file="fraud_report.json")
    logger.info(f"Fraud rate: {report['fraud_rate']*100:.2f}%")
    logger.info(f"Average fraud probability: {report['avg_fraud_probability']:.3f}")
    
    logger.info("\n✅ TRAINING COMPLETE!")
    logger.info("="*60)
    logger.info(f"Model saved to: fraud_model.pkl")
    logger.info(f"Report saved to: fraud_report.json")
    logger.info("="*60)


if __name__ == "__main__":
    main()
