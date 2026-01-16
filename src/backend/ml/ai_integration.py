"""
AI Integration Pipeline
Shows how to integrate fraud detection into ETL workflow
3 different integration points
"""
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from etl.transform import transform_data
from ml.ai_fraud_detector import BlockchainFraudDetector

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AIEnrichedETL:
    """ETL Pipeline with AI fraud detection integrated"""
    
    def __init__(self, detector=None):
        self.detector = detector or BlockchainFraudDetector()
        self.detector.load_or_create_model()
    
    # ============================================================
    # INTEGRATION POINT 1: AFTER TRANSFORM (Easiest & Recommended)
    # ============================================================
    
    def enrich_with_fraud_scores(self, raw_transactions):
        """
        BEST APPROACH FOR REAL-TIME
        
        Flow:
        Extract (raw) → Transform (clean) → AI Enrich (fraud scores) → Output
        
        Advantages:
        ✅ Clean data ready for ML
        ✅ No database needed
        ✅ Works with real-time processor
        ✅ Lightweight & fast
        """
        logger.info("🧠 AI ENRICHMENT (Point 1: After Transform)")
        
        # Step 1: Transform data
        df_clean = transform_data(raw_transactions)
        
        # Step 2: Add fraud scores
        df_enriched = self.detector.predict(df_clean, threshold=0.5)
        
        # Step 3: Add anomaly scores (unsupervised)
        df_enriched = self.detector.anomaly_detection(df_clean, contamination=0.1)
        
        return df_enriched
    
    # ============================================================
    # INTEGRATION POINT 2: BEFORE LOAD (Database Alternative)
    # ============================================================
    
    def filter_before_load(self, raw_transactions, db_insert_normal_only=True):
        """
        BEST APPROACH FOR STORAGE WITH FILTERING
        
        Flow:
        Extract → Transform → AI Filter → Load Only Safe Transactions
        
        Advantages:
        ✅ Keep database clean (only verified data)
        ✅ Save storage (skip suspicious)
        ✅ Faster queries (smaller database)
        ✅ Good for production
        
        Args:
            db_insert_normal_only: Only load normal transactions to DB
        """
        logger.info("🧠 AI FILTERING (Point 2: Before Load)")
        
        df_clean = transform_data(raw_transactions)
        df_enriched = self.detector.predict(df_clean, threshold=0.5)
        
        if db_insert_normal_only:
            normal_transactions = df_enriched[df_enriched['is_fraud'] == 0]
            suspicious_transactions = df_enriched[df_enriched['is_fraud'] == 1]
            
            logger.info(f"✅ {len(normal_transactions)} normal transactions → Database")
            logger.info(f"🚨 {len(suspicious_transactions)} suspicious → Separate analysis")
            
            return {
                'load': normal_transactions,  # To database
                'analyze': suspicious_transactions  # To fraud table
            }
        
        return {'all': df_enriched}
    
    # ============================================================
    # INTEGRATION POINT 3: PARALLEL ANALYSIS (Advanced)
    # ============================================================
    
    def parallel_ai_analysis(self, raw_transactions):
        """
        BEST APPROACH FOR ADVANCED INSIGHTS
        
        Flow (Parallel):
        Extract → Transform ──→ Load to DB
                          └──→ AI Fraud Detection (parallel)
                          └──→ Pattern Analysis (parallel)
                          └──→ Visualization (parallel)
        
        Advantages:
        ✅ Don't wait for AI (non-blocking)
        ✅ Load data immediately
        ✅ AI runs in background
        ✅ Best for production at scale
        """
        logger.info("🧠 PARALLEL AI ANALYSIS (Point 3: Separate Track)")
        
        df_clean = transform_data(raw_transactions)
        
        # These can run in parallel threads/processes
        results = {
            'main_data': df_clean,  # Load to database immediately
            'fraud_scores': self.detector.predict(df_clean),  # Run in parallel
            'anomalies': self.detector.anomaly_detection(df_clean),  # Run in parallel
        }
        
        return results


# ============================================================
# WHICH INTEGRATION POINT TO USE?
# ============================================================

INTEGRATION_GUIDE = """
╔════════════════════════════════════════════════════════════════════════╗
║                  AI INTEGRATION POINTS - QUICK GUIDE                  ║
╠════════════════════════════════════════════════════════════════════════╣
║                                                                        ║
║ 📍 POINT 1: AFTER TRANSFORM (⭐ RECOMMENDED FOR REAL-TIME)             ║
║    Extract → Transform → AI ✨ → Output                              ║
║    When to use:                                                       ║
║      • Real-time data processing                                      ║
║      • No database storage needed                                     ║
║      • Streaming fraud alerts                                         ║
║      • Discord/Webhook notifications                                  ║
║    Example: realtime_processor.py integration                         ║
║                                                                        ║
║ 📍 POINT 2: BEFORE LOAD (⭐ RECOMMENDED FOR STORAGE)                   ║
║    Extract → Transform → AI Filter → Load (safe only)                 ║
║    When to use:                                                       ║
║      • Have PostgreSQL setup                                          ║
║      • Want clean database (no fraud data)                            ║
║      • Store normal transactions only                                 ║
║      • Analyze fraud separately                                       ║
║    Example: main_etl.py with fraud filter                             ║
║                                                                        ║
║ 📍 POINT 3: PARALLEL ANALYSIS (⭐ RECOMMENDED FOR SCALE)               ║
║    Extract → Transform → Load immediately                             ║
║                      └→ AI analysis (background threads)              ║
║    When to use:                                                       ║
║      • High-volume production system                                  ║
║      • Don't want to slow down loading                                ║
║      • AI runs in background                                          ║
║      • Load all data, analyze later                                   ║
║    Example: scheduler.py with threading                               ║
║                                                                        ║
╚════════════════════════════════════════════════════════════════════════╝

QUICK DECISION TREE:

Do you have storage (PostgreSQL)?
├─ NO  → Use POINT 1 (After Transform)
│        Stream + Analyze in real-time
│        No database needed
│
└─ YES → High volume?
         ├─ NO  → Use POINT 2 (Before Load)
         │        Filter & store only safe transactions
         │
         └─ YES → Use POINT 3 (Parallel)
                   Load immediately, AI runs in background

═════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(INTEGRATION_GUIDE)
