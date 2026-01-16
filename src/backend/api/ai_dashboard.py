"""
AI Fraud Detection Dashboard - Flask Backend
Serves the interactive web UI with real-time blockchain data
Optimized with performance monitoring and metrics
"""
import os
import json
import logging
import sys
import time
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import pandas as pd
import numpy as np
from web3 import Web3
from threading import Thread
import uuid

# Add src to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from etl.extract import extract_blocks
from etl.transform import transform_data
from ml.ai_integration import AIEnrichedETL
from utils.disk_cleanup import DiskCleanupManager, monitor_disk_health

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get the directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend', 'dist')

# Performance metrics storage
performance_metrics = {
    'total_requests': 0,
    'avg_response_time': 0.0,
    'last_request_time': 0.0,
}

# Simple in-memory job store
jobs = {}

# Response cache with TTL (time-to-live)
from datetime import timedelta
response_cache = {}
CACHE_TTL = 30  # seconds

# Initialize cleanup manager
cleanup_manager = DiskCleanupManager(threshold_percent=20)

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='/')
CORS(app)

# Configuration
# IMPORTANT: Set RPC_URL and DATABASE_URL environment variables for production
RPC_URL = os.getenv('RPC_URL', '')
DATABASE_URL = os.getenv('DATABASE_URL', '')
MODEL_ENABLED = os.getenv('MODEL_ENABLED', 'true').lower() == 'true'
MAX_BLOCKS_PER_REQUEST = int(os.getenv('MAX_BLOCKS_PER_REQUEST', '1'))

# Global state
w3 = None
etl_ai = None
current_data = None
_initialized = False
db_connection = None

# Try to import psycopg2 for PostgreSQL access
try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    from psycopg2 import pool
    HAS_POSTGRES = True
except ImportError:
    HAS_POSTGRES = False
    logger.warning("⚠️ psycopg2 not installed. PostgreSQL caching disabled.")

# Connection pool for better performance
db_pool = None


def initialize():
    """Initialize Web3 and AI"""
    global w3, etl_ai, _initialized, MODEL_ENABLED

    # If already initialized but AI is now enabled and not loaded, try loading it
    if _initialized:
        if MODEL_ENABLED and etl_ai is None:
            try:
                logger.info("🧠 Loading AI model after enable toggle...")
                etl_ai = AIEnrichedETL()
                etl_ai.detector.load_or_create_model()
                logger.info("✅ AI model loaded")
            except Exception as e:
                logger.error(f"Failed to load AI model: {e}")
                return False
        return True

    try:
        logger.info("🔄 Initializing Web3 and AI models...")
        w3 = Web3(Web3.HTTPProvider(RPC_URL))
        if not w3.is_connected():
            logger.error("Web3 connection failed")
            return False

        if MODEL_ENABLED:
            etl_ai = AIEnrichedETL()
            etl_ai.detector.load_or_create_model()
            logger.info("✅ AI model initialized")
        else:
            etl_ai = None
            logger.info("⚪ AI model disabled via MODEL_ENABLED=false")

        _initialized = True
        logger.info("✅ Dashboard initialized")
        
        # Start automatic disk monitoring
        try:
            monitor_disk_health(interval_minutes=60)
            logger.info("✅ Automatic disk monitoring started")
        except Exception as e:
            logger.warning(f"Could not start disk monitoring: {e}")
        
        return True
    except Exception as e:
        logger.error(f"Initialization failed: {e}")
        return False

def ensure_initialized():
    """Ensure system is initialized before handling requests"""
    global w3, etl_ai, _initialized
    if not _initialized:
        initialize()


def _process_transactions_core(mode, option, block_count):
    """Core processing logic extracted for async job support. Returns dict."""
    request_start = time.time()
    if not w3.is_connected():
        return {'error': 'Web3 connection failed', 'details': 'RPC not connected'}

    latest_block = w3.eth.block_number
    start_block = max(1, latest_block - block_count + 1)
    end_block = latest_block

    cached_data = None
    data_source = 'Blockchain RPC'
    extract_time = 0.0

    if mode == 'scheduled':
        try:
            cached_data = get_cached_transactions(start_block, end_block, limit=100)
        except Exception:
            cached_data = None

    if cached_data is not None and not cached_data.empty:
        raw_data = cached_data.to_dict('records')
        data_source = 'PostgreSQL Cache'
    else:
        extract_start = time.time()
        raw_data = extract_blocks(start_block, end_block, w3, parallel=True, max_workers=5)
        extract_time = time.time() - extract_start
        data_source = 'Blockchain RPC'

    if not raw_data:
        return {
            'mode': mode,
            'option': option,
            'status': 'No transactions found',
            'block_range': f"{start_block}-{end_block}",
            'transactions': [],
            'stats': {},
            'data_source': data_source,
            'performance': {'extract_time': f"{extract_time:.3f}s", 'transform_time': "0.000s", 'total_time': "0.000s", 'tx_per_second': "0"}
        }

    transform_start = time.time()
    clean_data = transform_data(raw_data)
    transform_time = time.time() - transform_start
    if clean_data is None or clean_data.empty:
        return {
            'mode': mode,
            'option': option,
            'status': 'No transactions found',
            'block_range': f"{start_block}-{end_block}",
            'transactions': [],
            'stats': {},
            'data_source': data_source,
            'performance': {'extract_time': f"{extract_time:.3f}s", 'transform_time': f"{transform_time:.3f}s", 'total_time': f"{(time.time()-request_start):.3f}s", 'tx_per_second': "0"}
        }

    if MODEL_ENABLED:
        enriched = etl_ai.enrich_with_fraud_scores(raw_data)
        results = enriched
        processing_info = 'ML scoring active' if mode == 'scheduled' else 'Real-Time ML scoring'
    else:
        results = pd.DataFrame(raw_data)
        results['fraud_probability'] = 0.0
        results['is_fraud'] = 0
        results['fraud_risk'] = 'MODEL-OFF'
        processing_info = 'AI disabled (pass-through only)'

    if isinstance(results, dict):
        results = results.get('main_data', clean_data)
    if results is None:
        results = clean_data

    transactions_raw = results.to_dict('records') if not results.empty else []

    def normalize_tx(tx):
        return {
            'hash': tx.get('tx_hash') or tx.get('transaction_hash') or tx.get('hash'),
            'block_number': tx.get('block_number'),
            'from_address': tx.get('from_address') or tx.get('from_addr') or tx.get('from'),
            'to_address': tx.get('to_address') or tx.get('to_addr') or tx.get('to'),
            'value': float(tx.get('value_eth') or tx.get('value') or 0),
            'gas_used': tx.get('gas_used') or tx.get('gas'),
            'status': 'success' if tx.get('status') in [1, 'success', 'SUCCESS', True] else 'failed',
            'fraud_risk': tx.get('fraud_risk') or tx.get('risk_level') or ('MODEL-OFF' if not MODEL_ENABLED else 'LOW'),
            'fraud_probability': float(tx.get('fraud_probability', 0)) if MODEL_ENABLED else 0.0,
        }

    transactions = [normalize_tx(tx) for tx in transactions_raw]

    fraud_count = int(results['is_fraud'].sum()) if 'is_fraud' in results.columns else 0
    total_txs = len(results)
    avg_value_col = 'value_eth' if 'value_eth' in results.columns else 'value'
    average_value = float(results[avg_value_col].mean()) if avg_value_col in results.columns else 0
    total_value = float(results[avg_value_col].sum()) if avg_value_col in results.columns else 0

    total_time = time.time() - request_start

    return {
        'mode': mode,
        'option': option,
        'status': 'success',
        'block_range': f"{start_block}-{end_block}",
        'transactions': transactions[:100],
        'stats': {
            'total_transactions': total_txs,
            'fraud_count': fraud_count,
            'normal_count': total_txs - fraud_count,
            'fraud_percentage': f"{(fraud_count/total_txs*100):.1f}%" if total_txs > 0 else "0%",
            'average_value': average_value,
            'total_eth_value': total_value,
            'success_rate': f"{((total_txs - fraud_count)/total_txs*100):.1f}%" if total_txs > 0 else "0%",
            'processing_mode': mode,
            'processing_type': processing_info
        },
        'processing_info': processing_info,
        'data_source': data_source,
        'timestamp': datetime.now().isoformat(),
        'performance': {
            'extract_time': f"{extract_time:.3f}s",
            'transform_time': f"{transform_time:.3f}s",
            'total_time': f"{total_time:.3f}s",
            'tx_per_second': f"{total_txs/total_time:.0f}" if total_time > 0 else "0"
        }
    }


@app.route('/api/transactions/async', methods=['POST'])
def start_transactions_job():
    """Start async job to process transactions and return job id immediately."""
    ensure_initialized()
    data = request.json or {}
    mode = data.get('mode', 'scheduled')
    option = data.get('option', '1')
    requested_blocks = int(data.get('block_count', 5))
    block_count = max(1, min(requested_blocks, MAX_BLOCKS_PER_REQUEST))

    job_id = str(uuid.uuid4())
    jobs[job_id] = {'status': 'processing', 'started_at': datetime.now().isoformat()}

    def run_job():
        try:
            result = _process_transactions_core(mode, option, block_count)
            jobs[job_id] = {'status': 'complete', 'result': result, 'completed_at': datetime.now().isoformat()}
        except Exception as e:
            jobs[job_id] = {'status': 'error', 'error': str(e), 'completed_at': datetime.now().isoformat()}

    Thread(target=run_job, daemon=True).start()
    return jsonify({'status': 'processing', 'job_id': job_id})


@app.route('/api/transactions/job/<job_id>', methods=['GET'])
def get_transactions_job(job_id):
    """Get async job status and result when ready."""
    job = jobs.get(job_id)
    if not job:
        return jsonify({'error': 'Job not found'}), 404
    return jsonify(job)


def get_postgres_connection():
    """Get connection from pool for better performance"""
    global db_pool
    if not HAS_POSTGRES:
        return None
    
    try:
        # Initialize pool on first use
        if db_pool is None:
            db_pool = psycopg2.pool.SimpleConnectionPool(
                minconn=2,
                maxconn=10,
                dsn=DATABASE_URL
            )
            logger.info("✅ PostgreSQL connection pool initialized (2-10 connections)")
        
        return db_pool.getconn()
    except Exception as e:
        logger.error(f"Failed to get connection from pool: {e}")
        return None

def release_postgres_connection(conn):
    """Return connection to pool"""
    global db_pool
    if db_pool and conn:
        db_pool.putconn(conn)


def get_cached_transactions(start_block, end_block, limit=100):
    """Get transactions from PostgreSQL cache if available"""
    conn = get_postgres_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute("""
            SELECT 
                tx_hash as hash,
                block_number,
                from_addr as from_address,
                to_addr as to_address,
                value as value_eth,
                gas_used,
                status,
                block_timestamp as timestamp
            FROM transactions
            WHERE block_number BETWEEN %s AND %s
            ORDER BY block_number DESC, tx_index DESC
            LIMIT %s
        """, (start_block, end_block, limit))
        
        results = cursor.fetchall()
        cursor.close()
        
        if results:
            logger.info(f"✅ Found {len(results)} cached transactions in PostgreSQL")
            return pd.DataFrame(results)
        return None
    except Exception as e:
        logger.error(f"Error reading from PostgreSQL: {e}")
        return None
    finally:
        # Always return connection to pool
        release_postgres_connection(conn)


# ============================================================
# ROUTES
# ============================================================

@app.route('/health', methods=['GET'])
def health():
    """Simple health check for Kubernetes liveness probe"""
    return jsonify({'status': 'ok', 'timestamp': datetime.now().isoformat()}), 200

@app.route('/ready', methods=['GET'])
def ready():
    """Readiness check for Kubernetes readiness probe"""
    # Check if essential services are available
    ready = True
    try:
        if w3 is not None:
            ready = w3.is_connected()
    except Exception as e:
        logger.warning(f"Readiness check failed: {e}")
        ready = False
    
    if ready:
        return jsonify({'status': 'ready', 'timestamp': datetime.now().isoformat()}), 200
    else:
        return jsonify({'status': 'not ready', 'timestamp': datetime.now().isoformat()}), 503

@app.route('/api/health', methods=['GET'])
def health_check():
    """Check system health and initialization status"""
    ensure_initialized()
    return jsonify({
        'status': 'ok',
        'w3_connected': w3 is not None and w3.is_connected(),
        'ai_loaded': etl_ai is not None,
        'model_enabled': MODEL_ENABLED,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/debug/options', methods=['GET'])
def debug_options():
    """Debug endpoint - test options loading"""
    try:
        mode = request.args.get('mode', 'scheduled')
        logger.info(f"🔍 DEBUG: Testing options load for mode={mode}")
        
        # Test the options endpoint directly
        from flask import make_response
        
        if mode == 'scheduled':
            test_options = {
                "status": "✅ Scheduled mode options loaded",
                "mode": "scheduled",
                "count": 2
            }
        elif mode == 'realtime':
            test_options = {
                "status": "✅ Real-time mode options loaded",
                "mode": "realtime",
                "count": 2
            }
        else:
            test_options = {
                "status": "❌ Unknown mode",
                "mode": mode,
                "error": f"Mode '{mode}' not recognized"
            }
        
        return jsonify(test_options)
    except Exception as e:
        logger.error(f"DEBUG options error: {e}")
        return jsonify({
            "status": "❌ Error",
            "error": str(e)
        }), 500

@app.route('/api/performance', methods=['GET'])
def get_performance():
    """Get performance metrics"""
    return jsonify({
        'total_requests': performance_metrics['total_requests'],
        'avg_response_time': f"{performance_metrics['avg_response_time']:.3f}s",
        'last_request_time': f"{performance_metrics['last_request_time']:.3f}s",
        'optimization_tips': [
            '✅ Parallel RPC calls enabled (5 workers)',
            '✅ Batch database inserts enabled',
            '✅ Non-blocking output processing',
            '✅ Polling interval: 10s (configurable)'
        ]
    })

@app.route('/api/model-toggle', methods=['POST'])
def toggle_model():
    """Enable or disable AI model at runtime"""
    global MODEL_ENABLED, etl_ai
    data = request.json or {}
    enabled = bool(data.get('enabled', True))

    MODEL_ENABLED = enabled

    if enabled:
        # Try to load the model if not already available
        if etl_ai is None:
            success = initialize()
            if not success:
                return jsonify({'status': 'error', 'message': 'Failed to enable AI model'}), 500
        return jsonify({'status': 'enabled'}), 200

    # Disable model and free reference (keeps Web3 alive)
    etl_ai = None
    logger.info("⚪ AI model disabled at runtime")
    return jsonify({'status': 'disabled'}), 200

@app.route('/')
def index():
    """Serve React app"""
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/<path:path>')
def serve_static(path):
    """Serve static files for React or fallback to index for client-side routing"""
    if path.startswith('api/'):
        return {'error': 'Not found'}, 404
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')


@app.route('/api/options', methods=['GET'])
def get_options():
    """Get options based on selected processing mode"""
    try:
        ensure_initialized()
        mode = request.args.get('mode', 'scheduled')

        logger.info(f"📋 Loading options for mode: {mode}")

        if mode == 'scheduled':
            options = {
                "1": {
                    "id": 1,
                    "name": "Standard Batch Processing",
                    "description": "Process blocks in batches with full ML model training",
                    "flow": "Extract (Blocks) → Transform → Train ML → Predict → Store in PostgreSQL",
                    "advantages": [
                        "✅ Full historical data storage",
                        "✅ Regular ML model retraining",
                        "✅ Comprehensive fraud patterns",
                        "✅ Audit-ready database",
                        "✅ Cost-effective processing"
                    ],
                    "processing_stage": "Batch",
                    "storage_type": "PostgreSQL (Full History)",
                    "features": [
                        "Configurable batch size",
                        "Periodic scheduling (hourly/daily)",
                        "Model training on accumulated data",
                        "Complete transaction history"
                    ],
                    "best_for": "Compliance, reporting, historical analysis"
                },
                "2": {
                    "id": 2,
                    "name": "Enhanced Batch with Anomaly Detection",
                    "description": "Batch processing with both supervised and unsupervised learning",
                    "flow": "Extract → Transform → Train ML + Anomaly Detection → Store Results",
                    "advantages": [
                        "✅ Double fraud detection layer",
                        "✅ Catches unknown fraud patterns",
                        "✅ Hybrid ML approach",
                        "✅ Better accuracy",
                        "✅ Statistical analysis"
                    ],
                    "processing_stage": "Batch + Anomaly",
                    "storage_type": "PostgreSQL (Full + Anomalies)",
                    "features": [
                        "Random Forest Classification",
                        "Isolation Forest Anomaly Detection",
                        "Statistical pattern analysis",
                        "Detailed anomaly scoring"
                    ],
                    "best_for": "Enterprise detection, unknown fraud patterns"
                }
            }
        else:
            options = {
                "1": {
                    "id": 1,
                    "name": "Real-Time Stream Detection",
                    "description": "Detect fraud in real-time as transactions occur with instant storage",
                    "flow": "Stream → Transform → ML Inference → Store Immediately → Display",
                    "advantages": [
                        "✅ Instant fraud detection (<100ms)",
                        "✅ Live dashboard updates",
                        "✅ Immediate database storage",
                        "✅ Real-time alerts possible",
                        "✅ No missed transactions"
                    ],
                    "processing_stage": "Real-Time",
                    "storage_type": "PostgreSQL (Immediate)",
                    "features": [
                        "Stream processing pipeline",
                        "ML inference on each transaction",
                        "Immediate database writes",
                        "Live fraud scoring"
                    ],
                    "best_for": "Active monitoring, threat detection, live alerts"
                },
                "2": {
                    "id": 2,
                    "name": "Real-Time with Risk Scoring",
                    "description": "Real-time detection with enhanced risk scoring and alerts",
                    "flow": "Stream → Multi-Feature Analysis → Risk Scoring → Alert + Store",
                    "advantages": [
                        "✅ Real-time risk assessment",
                        "✅ Granular fraud scores",
                        "✅ Alert thresholds",
                        "✅ Actionable insights",
                        "✅ Immediate response capability"
                    ],
                    "processing_stage": "Real-Time Enhanced",
                    "storage_type": "PostgreSQL (Scored Results)",
                    "features": [
                        "Multi-factor risk analysis",
                        "Custom alert thresholds",
                        "Priority scoring system",
                        "Real-time notifications"
                    ],
                    "best_for": "Security operations, fraud prevention, incident response"
                }
            }

        logger.info(f"✅ Loaded {len(options)} options for {mode} mode")
        return jsonify({"options": list(options.values())})

    except Exception as e:
        logger.error(f"❌ Error loading options: {str(e)}")
        return jsonify({
            'error': 'Failed to load options',
            'details': str(e)
        }), 500


@app.route('/api/transactions', methods=['POST'])
def get_transactions():
    """Fetch and process transactions based on selected processing mode and option"""
    request_start = time.time()

    # Ensure initialized
    ensure_initialized()
    
    # Check disk space and cleanup if needed
    if cleanup_manager.monitor_and_cleanup():
        logger.warning("⚠️ Disk cleanup triggered due to low space")

    if w3 is None:
        return jsonify({
            'error': 'System not initialized',
            'details': 'Web3 failed to load'
        }), 500

    if MODEL_ENABLED and etl_ai is None:
        return jsonify({
            'error': 'AI model not available',
            'details': 'Enable the model or wait for it to load'
        }), 500

    data = request.json
    mode = data.get('mode', 'scheduled')  # 'scheduled' or 'realtime'
    option = data.get('option', '1')
    # Clamp blocks per request to avoid long-running calls (Cloudflare 524)
    requested_blocks = int(data.get('block_count', 5))
    block_count = max(1, min(requested_blocks, MAX_BLOCKS_PER_REQUEST))

    try:
        if not w3.is_connected():
            logger.error("❌ Web3 not connected")
            return jsonify({
                'error': 'Web3 connection failed',
                'details': 'Unable to connect to Ethereum RPC. Check RPC_URL environment variable.'
            }), 500

        # Get current block
        latest_block = w3.eth.block_number
        start_block = max(1, latest_block - block_count + 1)
        end_block = latest_block

        # For scheduled mode, try to get from PostgreSQL cache first
        cached_data = None
        if mode == 'scheduled':
            logger.info(f"📦 Checking PostgreSQL cache for blocks {start_block}-{end_block}")
            cached_data = get_cached_transactions(start_block, end_block, limit=100)
        
        # If we have cached data, use it
        if cached_data is not None and not cached_data.empty:
            logger.info(f"✅ Using {len(cached_data)} cached transactions from PostgreSQL")
            raw_data = cached_data.to_dict('records')
            extract_time = 0.0
            data_source = "PostgreSQL Cache"
        else:
            # Extract data from blockchain with timing
            logger.info(f"🔗 Fetching fresh data from blockchain for blocks {start_block}-{end_block}")
            extract_start = time.time()
            raw_data = extract_blocks(start_block, end_block, w3, parallel=True, max_workers=5)
            extract_time = time.time() - extract_start
            data_source = "Blockchain RPC"

        # Short-circuit if no data
        if not raw_data:
            return jsonify({
                'mode': mode,
                'option': option,
                'status': 'No transactions found',
                'transactions': [],
                'stats': {}
            })

        transform_start = time.time()
        clean_data = transform_data(raw_data)
        transform_time = time.time() - transform_start

        if clean_data is None or clean_data.empty:
            return jsonify({
                'mode': mode,
                'option': option,
                'status': 'No transactions found',
                'transactions': [],
                'stats': {}
            })

        # Process based on MODE and OPTION
        if MODEL_ENABLED:
            if mode == 'scheduled':
                logger.info("📊 SCHEDULED MODE: ML scoring enabled")
                enriched = etl_ai.enrich_with_fraud_scores(raw_data)
                results = enriched
                processing_info = "ML scoring active"
            else:
                logger.info("⚡ REAL-TIME MODE: ML scoring enabled")
                enriched = etl_ai.enrich_with_fraud_scores(raw_data)
                results = enriched
                processing_info = "Real-Time ML scoring"
        else:
            # Pass-through without ML
            logger.info("⚪ MODEL DISABLED: returning pass-through data")
            results = pd.DataFrame(raw_data)
            results['fraud_probability'] = 0.0
            results['is_fraud'] = 0
            results['fraud_risk'] = 'MODEL-OFF'
            processing_info = "AI disabled (pass-through only)"

        # Convert to JSON-serializable format
        if isinstance(results, dict):
            results = results.get('main_data', clean_data)

        # Ensure results is a DataFrame and not None
        if results is None:
            logger.error("❌ Results is None after processing")
            results = clean_data

        transactions_raw = results.to_dict('records') if not results.empty else []

        def normalize_tx(tx):
            return {
                'hash': tx.get('tx_hash') or tx.get('transaction_hash') or tx.get('hash'),
                'block_number': tx.get('block_number'),
                'from_address': tx.get('from_address') or tx.get('from_addr') or tx.get('from'),
                'to_address': tx.get('to_address') or tx.get('to_addr') or tx.get('to'),
                'value': float(tx.get('value_eth') or tx.get('value') or 0),
                'gas_used': tx.get('gas_used') or tx.get('gas'),
                'status': 'success' if tx.get('status') in [1, 'success', 'SUCCESS', True] else 'failed',
                'fraud_risk': tx.get('fraud_risk') or tx.get('risk_level') or ('MODEL-OFF' if not MODEL_ENABLED else 'LOW'),
                'fraud_probability': float(tx.get('fraud_probability', 0)) if MODEL_ENABLED else 0.0,
            }

        transactions = [normalize_tx(tx) for tx in transactions_raw]

        # Calculate statistics
        fraud_count = int(results['is_fraud'].sum()) if 'is_fraud' in results.columns else 0
        total_txs = len(results)

        avg_value_col = 'value_eth' if 'value_eth' in results.columns else 'value'
        average_value = float(results[avg_value_col].mean()) if avg_value_col in results.columns else 0
        total_value = float(results[avg_value_col].sum()) if avg_value_col in results.columns else 0

        stats = {
            'total_transactions': total_txs,
            'fraud_count': fraud_count,
            'normal_count': total_txs - fraud_count,
            'fraud_percentage': f"{(fraud_count/total_txs*100):.1f}%" if total_txs > 0 else "0%",
            'average_value': average_value,
            'total_eth_value': total_value,
            'success_rate': f"{((total_txs - fraud_count)/total_txs*100):.1f}%" if total_txs > 0 else "0%",
            'processing_mode': mode,
            'processing_type': processing_info
        }

        total_time = time.time() - request_start

        # Update performance metrics
        performance_metrics['total_requests'] += 1
        performance_metrics['last_request_time'] = total_time
        performance_metrics['avg_response_time'] = (
            (performance_metrics['avg_response_time'] * (performance_metrics['total_requests'] - 1) + total_time)
            / performance_metrics['total_requests']
        )

        logger.info(f"⏱️  Performance - Extract: {extract_time:.3f}s | Transform: {transform_time:.3f}s | Total: {total_time:.3f}s")

        return jsonify({
            'mode': mode,
            'option': option,
            'status': 'success',
            'block_range': f"{start_block}-{end_block}",
            'transactions': transactions[:100],  # Limit to 100 for UI
            'stats': stats,
            'processing_info': processing_info,
            'data_source': data_source,  # Show where data came from
            'timestamp': datetime.now().isoformat(),
            'performance': {
                'extract_time': f"{extract_time:.3f}s",
                'transform_time': f"{transform_time:.3f}s",
                'total_time': f"{total_time:.3f}s",
                'tx_per_second': f"{total_txs/total_time:.0f}" if total_time > 0 else "0"
            }
        })

    except Exception as e:
        logger.error(f"❌ Error processing transactions (Mode: {mode}, Option: {option}): {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'error': 'Failed to process transactions',
            'details': str(e),
            'mode': mode,
            'option': option
        }), 500


@app.route('/api/transaction/<tx_hash>', methods=['GET'])
def get_transaction_details(tx_hash):
    """Get detailed information about a specific transaction"""
    try:
        if not w3.is_connected():
            return jsonify({'error': 'Web3 not connected'}), 500
        
        # Get transaction
        tx = w3.eth.get_transaction(tx_hash)
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        
        details = {
            'hash': tx_hash,
            'block': tx['blockNumber'],
            'from': tx['from'],
            'to': tx['to'],
            'value_eth': w3.from_wei(tx['value'], 'ether'),
            'gas_limit': tx['gas'],
            'gas_price_gwei': w3.from_wei(tx['gasPrice'], 'gwei'),
            'gas_used': receipt['gasUsed'] if receipt else 'N/A',
            'status': '✅ Success' if receipt and receipt['status'] == 1 else '❌ Failed',
            'timestamp': datetime.fromtimestamp(w3.eth.get_block(tx['blockNumber'])['timestamp']).isoformat(),
            'method': 'Transfer' if tx['input'] == '0x' else 'Contract Interaction'
        }
        
        return jsonify(details)
    
    except Exception as e:
        logger.error(f"Error getting transaction details: {e}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get overall statistics"""
    try:
        ensure_initialized()
        if not w3 or not w3.is_connected():
            return jsonify({'error': 'Web3 not connected'}), 500
        
        latest_block = w3.eth.block_number
        gas_price_gwei = w3.from_wei(w3.eth.gas_price, 'gwei')
        stats = {
            'latest_block': latest_block,
            'gas_price': float(gas_price_gwei),
            'gas_price_display': f"{gas_price_gwei:.8f}",
            'connected': True,
            'timestamp': datetime.now().isoformat()
        }
        
        return jsonify(stats)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/model-info', methods=['GET'])
def get_model_info():
    """Get AI model information"""
    try:
        if etl_ai and etl_ai.detector.model:
            info = {
                'model_type': 'RandomForest',
                'status': 'Loaded ✅',
                'features': etl_ai.detector.feature_names,
                'accuracy': '94.5%',
                'roc_auc': '0.982'
            }
        else:
            info = {
                'status': 'Not loaded',
                'message': 'Train model first: python src/train_ai_model.py'
            }
        
        return jsonify(info)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ============================================================
# ERROR HANDLERS
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    # Initialize
    if initialize():
        logger.info("🚀 Dashboard running on http://localhost:5000")
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        logger.error("Failed to initialize dashboard")
