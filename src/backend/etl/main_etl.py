"""
Main ETL Orchestration Script
Coordinates Extract → Transform → Load → State tracking pipeline
Optimized with parallel processing and batch writes
"""
import os
import logging
import sys
import time
from web3 import Web3
from sqlalchemy import create_engine, text
from datetime import datetime, timezone
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import ETL phases
from etl.extract import extract_blocks
from etl.transform import transform_data, validate_data

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/blockchain_db')
RPC_URL = os.getenv('RPC_URL', "https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu")
BATCH_SIZE = int(os.getenv('BATCH_SIZE', '10'))  # Process X blocks per run


class BlockchainETL:
    """Main ETL orchestrator for blockchain data pipeline"""
    
    def __init__(self):
        self.engine = None
        self.w3 = None
        self.processed_blocks = 0
        self.processed_transactions = 0
        self.failed_blocks = 0
    
    def initialize(self):
        """Initialize database and Web3 connections"""
        try:
            # SQLAlchemy engine
            self.engine = create_engine(DATABASE_URL, echo=False)
            with self.engine.connect() as conn:
                conn.execute(text("SELECT 1"))
                conn.commit()
            logger.info("Connected to PostgreSQL")
        except Exception as e:
            logger.error(f"Database connection failed: {e}")
            return False
        
        try:
            # Web3 connection
            self.w3 = Web3(Web3.HTTPProvider(RPC_URL))
            if not self.w3.is_connected():
                logger.error("Web3 connection failed")
                return False
            logger.info(f"Connected to Web3 - Latest block: {self.w3.eth.block_number}")
        except Exception as e:
            logger.error(f"Web3 initialization failed: {e}")
            return False
        
        self._create_tables()
        return True
    
    def _create_tables(self):
        """Create database schema if not exists"""
        with self.engine.connect() as conn:
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
            
            # Pipeline state table
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
        logger.info("Database schema initialized")
    
    def get_last_processed_block(self):
        """Retrieve last processed block from pipeline_state"""
        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(
                    "SELECT last_block FROM pipeline_state WHERE id = 1"
                ))
                row = result.fetchone()
                last_block = row[0] if row else 0
            logger.info(f"Last processed block: {last_block}")
            return last_block
        except Exception as e:
            logger.error(f"Failed to get last processed block: {e}")
            return 0
    
    def update_pipeline_state(self, block_number):
        """Update last processed block in pipeline_state"""
        try:
            with self.engine.connect() as conn:
                conn.execute(text('''
                UPDATE pipeline_state 
                SET last_block = :block_num, updated_at = CURRENT_TIMESTAMP 
                WHERE id = 1
                '''), {"block_num": block_number})
                conn.commit()
            logger.info(f"Updated pipeline_state: last_block = {block_number}")
        except Exception as e:
            logger.error(f"Failed to update pipeline_state: {e}")
    
    def extract_phase(self, start_block, end_block):
        """Extract phase: Get blockchain data"""
        try:
            logger.info(f"EXTRACT: Processing blocks {start_block}-{end_block}")
            rows = extract_blocks(start_block, end_block, self.w3)
            logger.info(f"EXTRACT: Extracted {len(rows)} transactions")
            return rows
        except Exception as e:
            logger.error(f"EXTRACT failed: {e}")
            self.failed_blocks += (end_block - start_block + 1)
            return []
    
    def transform_phase(self, rows):
        """Transform phase: Clean and normalize data"""
        try:
            logger.info(f"TRANSFORM: Processing {len(rows)} rows")
            df = transform_data(rows)
            
            if not validate_data(df):
                logger.warning("TRANSFORM: Data validation failed")
                return None
            
            logger.info(f"TRANSFORM: Validated {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"TRANSFORM failed: {e}")
            return None
    
    def load_phase(self, df, batch_size=1000):
        """
        Load phase: Insert data into database with optimized batching
        
        Args:
            df: DataFrame to load
            batch_size: Number of rows per batch insert
        """
        try:
            if df is None or df.empty:
                logger.warning("LOAD: No data to load")
                return 0
            
            load_start = time.time()
            logger.info(f"LOAD: Inserting {len(df)} rows (batch size: {batch_size})")
            
            # Batch insert for better performance
            rows_inserted = 0
            for i in range(0, len(df), batch_size):
                batch = df.iloc[i:i+batch_size]
                batch.to_sql('transaction_receipts', self.engine, if_exists='append', index=False)
                rows_inserted += len(batch)
                logger.debug(f"LOAD: Inserted batch {i//batch_size + 1}/{(len(df)-1)//batch_size + 1}")
            
            elapsed = time.time() - load_start
            logger.info(f"✅ LOAD: Successfully inserted {rows_inserted} rows in {elapsed:.2f}s")
            return rows_inserted
        except Exception as e:
            logger.error(f"LOAD failed: {e}")
            return 0
    
    def process_blocks(self, start_block=None, end_block=None):
        """
        Process blocks through ETL pipeline
        
        Args:
            start_block: Block to start from (default: last_processed + 1)
            end_block: Block to end at (default: latest - 1)
        """
        # Determine block range
        last_block = self.get_last_processed_block()
        
        if start_block is None:
            start_block = last_block + 1
        
        if end_block is None:
            end_block = self.w3.eth.block_number - 1
        
        if start_block > end_block:
            logger.info("No new blocks to process")
            return True
        
        logger.info(f"Processing {end_block - start_block + 1} blocks "
                   f"(from {start_block} to {end_block})")
        
        # Process blocks in batches
        current_block = start_block
        while current_block <= end_block:
            batch_end = min(current_block + BATCH_SIZE - 1, end_block)
            
            # EXTRACT
            rows = self.extract_phase(current_block, batch_end)
            if not rows:
                logger.warning(f"Batch {current_block}-{batch_end}: No data extracted")
                current_block = batch_end + 1
                continue
            
            # TRANSFORM
            df = self.transform_phase(rows)
            if df is None:
                logger.error(f"Batch {current_block}-{batch_end}: Transform failed")
                current_block = batch_end + 1
                continue
            
            # LOAD
            loaded_count = self.load_phase(df)
            
            # STATE: Update tracking
            if loaded_count > 0:
                self.update_pipeline_state(batch_end)
                self.processed_blocks += (batch_end - current_block + 1)
                self.processed_transactions += loaded_count
            
            current_block = batch_end + 1
        
        return True
    
    def print_summary(self):
        """Print ETL execution summary"""
        logger.info("="*60)
        logger.info("ETL Pipeline Summary")
        logger.info(f"  Blocks processed: {self.processed_blocks}")
        logger.info(f"  Transactions loaded: {self.processed_transactions}")
        logger.info(f"  Failed blocks: {self.failed_blocks}")
        logger.info("="*60)


def main():
    """Main entry point"""
    etl = BlockchainETL()
    
    try:
        if not etl.initialize():
            logger.error("Failed to initialize ETL")
            return 1
        
        # Process blocks
        if not etl.process_blocks():
            logger.error("ETL pipeline failed")
            return 1
        
        etl.print_summary()
        logger.info("ETL pipeline completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
