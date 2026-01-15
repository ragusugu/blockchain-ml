import os
import logging
from web3 import Web3
from sqlalchemy import create_engine, text
from datetime import datetime, timezone, timedelta
import shutil
import psutil
import pandas as pd

# Import ETL phases
from extract import extract_block, extract_blocks
from transform import transform_data, validate_data

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Database setup with SQLAlchemy
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/blockchain_db')
try:
    engine = create_engine(DATABASE_URL, echo=False)
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        conn.commit()
    logger.info("Connected to PostgreSQL via SQLAlchemy")
except Exception as e:
    logger.error(f"Failed to connect to PostgreSQL: {e}")
    exit(1)

# Create tables if not exists
def create_tables():
    """Initialize database schema"""
    with engine.connect() as conn:
        # Transaction receipts table
        conn.execute(text('''
        CREATE TABLE IF NOT EXISTS transaction_receipts (
            id SERIAL PRIMARY KEY,
            block_number BIGINT NOT NULL,
            block_hash VARCHAR(66),
            block_timestamp BIGINT,
            tx_hash VARCHAR(66) UNIQUE NOT NULL,
            tx_index INTEGER,
            from_addr VARCHAR(42) NOT NULL,
            to_addr VARCHAR(42),
            value FLOAT8,
            gas BIGINT,
            gas_price FLOAT8,
            gas_used BIGINT,
            cumulative_gas_used BIGINT,
            status SMALLINT,
            contract_addr VARCHAR(42),
            effective_gas_price BIGINT,
            processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''))
        
        # Pipeline state table for incremental processing
        conn.execute(text('''
        CREATE TABLE IF NOT EXISTS pipeline_state (
            id SERIAL PRIMARY KEY,
            last_block BIGINT NOT NULL DEFAULT 0,
            last_processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        '''))
        
        # Insert initial state if not exists
        conn.execute(text('''
        INSERT INTO pipeline_state (last_block) 
        SELECT 0 WHERE NOT EXISTS (SELECT 1 FROM pipeline_state LIMIT 1)
        '''))
        
        conn.commit()
    logger.info("Tables 'transaction_receipts' and 'pipeline_state' ready")


# Robust serializer
def to_serializable(obj):
    """Convert Web3 objects to JSON-serializable format"""
    from hexbytes import HexBytes
    from web3.datastructures import AttributeDict
    
    if isinstance(obj, (HexBytes, bytes)):
        return obj.hex()
    if isinstance(obj, AttributeDict):
        obj = dict(obj)
    if isinstance(obj, dict):
        return {k: to_serializable(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [to_serializable(i) for i in obj]
    if isinstance(obj, (str, int, float, bool)) or obj is None:
        return obj
    return str(obj)

# Connect to Web3
RPC_URL = os.getenv('RPC_URL', "https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu")
try:
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        logger.error("Failed to connect to Web3 RPC")
        exit(1)
    logger.info("Connected to Web3")
except Exception as e:
    logger.error(f"Web3 connection error: {e}")
    exit(1)

# Main ETL Pipeline
def etl_pipeline(block_number=None):
    """
    Execute Extract-Transform-Load pipeline for blockchain data
    
    Args:
        block_number: Specific block to process (default: latest)
    """
    create_tables()
    
    # Get block to process
    try:
        if block_number is None:
            block_number = w3.eth.block_number
        logger.info(f"Processing block: {block_number}")
    except Exception as e:
        logger.error(f"Failed to get block number: {e}")
        return False
    
    # EXTRACT phase
    try:
        rows = extract_block(block_number, w3)
        logger.info(f"Extracted {len(rows)} transactions from block {block_number}")
    except Exception as e:
        logger.error(f"Extract phase failed: {e}")
        return False
    
    if not rows:
        logger.warning(f"No transactions found in block {block_number}")
        return True
    
    # TRANSFORM phase
    try:
        df = transform_data(rows)
        if not validate_data(df):
            logger.error("Data validation failed")
            return False
        logger.info(f"Transformed {len(df)} rows")
    except Exception as e:
        logger.error(f"Transform phase failed: {e}")
        return False
    
    # LOAD phase
    try:
        df.to_sql('transaction_receipts', engine, if_exists='append', index=False)
        logger.info(f"Loaded {len(df)} rows to database")
    except Exception as e:
        logger.error(f"Load phase failed: {e}")
        return False
    
    # STATE phase - update last processed block
    try:
        with engine.connect() as conn:
            conn.execute(text('''
            UPDATE pipeline_state 
            SET last_block = :block_num, updated_at = CURRENT_TIMESTAMP 
            WHERE id = 1
            '''), {"block_num": block_number})
            conn.commit()
        logger.info(f"Updated pipeline_state: last_block = {block_number}")
    except Exception as e:
        logger.error(f"State phase failed: {e}")
        return False
    
    return True

# Fetch latest block and run pipeline
try:
    if etl_pipeline():
        logger.info("ETL Pipeline completed successfully")
    else:
        logger.error("ETL Pipeline failed")
        exit(1)
except Exception as e:
    logger.error(f"Pipeline execution error: {e}")
    exit(1)

# Data retention and cleanup
def cleanup_old_data():
    """Delete records older than 5 days"""
    try:
        five_days_ago = datetime.now(timezone.utc) - timedelta(days=5)
        with engine.connect() as conn:
            result = conn.execute(text(
                "DELETE FROM transaction_receipts WHERE created_at < :cutoff_date"
            ), {"cutoff_date": five_days_ago})
            conn.commit()
            deleted = result.rowcount
            if deleted > 0:
                logger.info(f"Deleted {deleted} records older than 5 days")
    except Exception as e:
        logger.error(f"Failed to delete old records: {e}")

def cleanup_low_disk_space():
    """Delete all data except today's if disk space < 1GB"""
    try:
        disk = psutil.disk_usage('/')
        free_gb = disk.free / (1024**3)
        if free_gb < 1:
            logger.warning(f"Low disk space: {free_gb:.2f} GB free")
            today = datetime.now(timezone.utc).date()
            with engine.connect() as conn:
                conn.execute(text(
                    "DELETE FROM transaction_receipts WHERE DATE(created_at) != :today"
                ), {"today": today})
                conn.commit()
            logger.warning(f"Deleted all records except from {today}")
    except Exception as e:
        logger.error(f"Disk space check failed: {e}")

# Execute cleanup operations
cleanup_old_data()
cleanup_low_disk_space()

# Clean up local receipts directory
receipts_dir = "receipts"
if os.path.exists(receipts_dir):
    try:
        shutil.rmtree(receipts_dir)
        logger.info("Deleted local receipts directory")
    except Exception as e:
        logger.error(f"Failed to delete receipts directory: {e}")

logger.info("Data cleanup completed - Process finished successfully")