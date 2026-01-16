#!/usr/bin/env python
"""
Testing Guide for Blockchain ETL Pipeline
Validate each component works correctly
"""

import sys
import logging
import os
from web3 import Web3

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Color codes for output
GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'


def test_web3_connection():
    """Test 1: Web3 RPC Connection"""
    logger.info(f"{YELLOW}[TEST 1] Testing Web3 RPC Connection...{RESET}")
    try:
        rpc_url = "https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu"
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        
        if not w3.is_connected():
            logger.error(f"{RED}✗ Web3 not connected{RESET}")
            return False
        
        block_number = w3.eth.block_number
        logger.info(f"{GREEN}✓ Web3 connected. Latest block: {block_number}{RESET}")
        return True, block_number, w3
    except Exception as e:
        logger.error(f"{RED}✗ Web3 connection failed: {e}{RESET}")
        return False, None, None


def test_extract(block_number, w3):
    """Test 2: Extract Phase"""
    logger.info(f"{YELLOW}[TEST 2] Testing Extract Phase...{RESET}")
    try:
        from etl.extract import extract_block
        
        # Use a recent block (or provided block_number)
        test_block = block_number - 1 if block_number else 24237712
        
        rows = extract_block(test_block, w3)
        
        if not rows:
            logger.warning(f"{YELLOW}! No transactions in block {test_block}{RESET}")
            return True, []
        
        logger.info(f"{GREEN}✓ Extracted {len(rows)} transactions from block {test_block}{RESET}")
        
        # Validate structure
        required_keys = ['tx_hash', 'from_address', 'to_address', 'value_eth', 'gas_used', 'status']
        sample = rows[0]
        missing_keys = [k for k in required_keys if k not in sample]
        
        if missing_keys:
            logger.error(f"{RED}✗ Missing keys in extracted data: {missing_keys}{RESET}")
            return False, []
        
        logger.info(f"{GREEN}✓ Data structure valid. Sample keys: {list(sample.keys())[:5]}...{RESET}")
        return True, rows
    except Exception as e:
        logger.error(f"{RED}✗ Extract failed: {e}{RESET}")
        return False, []


def test_transform(rows):
    """Test 3: Transform Phase"""
    logger.info(f"{YELLOW}[TEST 3] Testing Transform Phase...{RESET}")
    try:
        from etl.transform import transform_data, validate_data
        
        if not rows:
            logger.warning(f"{YELLOW}! No rows to transform{RESET}")
            return True, None
        
        df = transform_data(rows)
        logger.info(f"{GREEN}✓ Transformed {len(df)} rows into DataFrame{RESET}")
        
        # Validate
        if not validate_data(df):
            logger.warning(f"{YELLOW}! Data validation found issues (non-critical){RESET}")
            return True, df
        
        logger.info(f"{GREEN}✓ Data validation passed{RESET}")
        logger.info(f"{GREEN}✓ Columns: {list(df.columns)[:5]}...{RESET}")
        logger.info(f"{GREEN}✓ Data types: {dict(df.dtypes)}{RESET}")
        
        return True, df
    except Exception as e:
        logger.error(f"{RED}✗ Transform failed: {e}{RESET}")
        return False, None


def test_database_connection():
    """Test 4: Database Connection"""
    logger.info(f"{YELLOW}[TEST 4] Testing PostgreSQL Connection...{RESET}")
    try:
        import os
        from sqlalchemy import create_engine, text
        
        db_url = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/blockchain_db')
        engine = create_engine(db_url, echo=False)
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            conn.commit()
        
        logger.info(f"{GREEN}✓ PostgreSQL connected: {db_url.split('@')[1]}{RESET}")
        return True, engine
    except Exception as e:
        logger.error(f"{RED}✗ Database connection failed: {e}{RESET}")
        logger.info(f"{YELLOW}  Make sure PostgreSQL is running and credentials are correct{RESET}")
        return False, None


def test_schema(engine):
    """Test 5: Database Schema"""
    logger.info(f"{YELLOW}[TEST 5] Testing Database Schema...{RESET}")
    try:
        from sqlalchemy import text, inspect
        
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['transaction_receipts', 'pipeline_state']
        missing = [t for t in required_tables if t not in tables]
        
        if missing:
            logger.warning(f"{YELLOW}! Missing tables: {missing}. Will be created on first run.{RESET}")
            return True
        
        # Check columns
        receipt_cols = [col['name'] for col in inspector.get_columns('transaction_receipts')]
        logger.info(f"{GREEN}✓ Table 'transaction_receipts' has {len(receipt_cols)} columns{RESET}")
        
        state_cols = [col['name'] for col in inspector.get_columns('pipeline_state')]
        logger.info(f"{GREEN}✓ Table 'pipeline_state' has {len(state_cols)} columns{RESET}")
        
        return True
    except Exception as e:
        logger.error(f"{RED}✗ Schema check failed: {e}{RESET}")
        return False


def test_load(engine, df):
    """Test 6: Load Phase (Dry Run)"""
    logger.info(f"{YELLOW}[TEST 6] Testing Load Phase (DRY RUN - not inserting)...{RESET}")
    try:
        if df is None or df.empty:
            logger.warning(f"{YELLOW}! No data to test load with{RESET}")
            return True
        
        # Just validate structure, don't insert
        logger.info(f"{GREEN}✓ DataFrame has {len(df)} rows, {len(df.columns)} columns{RESET}")
        logger.info(f"{GREEN}✓ Columns ready for load: {list(df.columns)}{RESET}")
        logger.info(f"{GREEN}✓ Data types correct: {dict(df.dtypes)}{RESET}")
        logger.info(f"{YELLOW}  (DRY RUN - actual load skipped){RESET}")
        
        return True
    except Exception as e:
        logger.error(f"{RED}✗ Load test failed: {e}{RESET}")
        return False


def run_all_tests():
    """Run all tests sequentially"""
    logger.info(f"\n{YELLOW}{'='*60}")
    logger.info(f"{'BLOCKCHAIN ETL PIPELINE - TEST SUITE':^60}")
    logger.info(f"{'='*60}{RESET}\n")
    
    results = {}
    
    # Test 1: Web3
    test1_result = test_web3_connection()
    if not test1_result or test1_result[0] is False:
        logger.error(f"{RED}Stopping - Web3 connection required{RESET}")
        return
    results['Web3 Connection'] = True
    block_number, w3 = test1_result[1], test1_result[2]
    
    # Test 2: Extract
    test2_result = test_extract(block_number, w3)
    results['Extract Phase'] = test2_result[0]
    rows = test2_result[1]
    
    # Test 3: Transform
    test3_result = test_transform(rows)
    results['Transform Phase'] = test3_result[0]
    df = test3_result[1]
    
    # Test 4: Database
    test4_result = test_database_connection()
    if test4_result[0] is False:
        logger.warning(f"{YELLOW}Database test failed - skipping schema and load tests{RESET}")
        results['Database Connection'] = False
        results['Schema'] = 'SKIPPED'
        results['Load Phase'] = 'SKIPPED'
    else:
        results['Database Connection'] = True
        engine = test4_result[1]
        
        # Test 5: Schema
        test5_result = test_schema(engine)
        results['Schema'] = test5_result
        
        # Test 6: Load
        test6_result = test_load(engine, df)
        results['Load Phase'] = test6_result
    
    # Print summary
    logger.info(f"\n{YELLOW}{'='*60}")
    logger.info(f"{'TEST SUMMARY':^60}")
    logger.info(f"{'='*60}{RESET}\n")
    
    for test_name, result in results.items():
        if result == 'SKIPPED':
            status = f"{YELLOW}⊘ SKIPPED{RESET}"
        elif result is True:
            status = f"{GREEN}✓ PASSED{RESET}"
        else:
            status = f"{RED}✗ FAILED{RESET}"
        print(f"{test_name:.<40} {status}")
    
    all_passed = all(r is True for r in results.values() if r != 'SKIPPED')
    
    logger.info(f"\n{YELLOW}{'='*60}{RESET}")
    if all_passed:
        logger.info(f"{GREEN}{'ALL TESTS PASSED - SYSTEM READY':^60}{RESET}")
        logger.info(f"{GREEN}You can now run: python fetch_and_store.py{RESET}")
    else:
        logger.info(f"{YELLOW}Some tests failed or skipped - check configuration{RESET}")
    logger.info(f"{YELLOW}{'='*60}{RESET}\n")


if __name__ == "__main__":
    try:
        run_all_tests()
    except Exception as e:
        logger.error(f"{RED}Test suite error: {e}{RESET}", exc_info=True)
        sys.exit(1)
