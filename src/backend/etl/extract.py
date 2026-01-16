"""
Extract Phase of ETL Pipeline
Converts blockchain data into flat rows for processing
Optimized for parallel RPC calls, batch processing, and caching
"""
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
from functools import lru_cache
import time
import hashlib

logger = logging.getLogger(__name__)

# Performance tracking
_request_times = []

# Cache for block data (prevents redundant RPC calls)
_block_cache = {}


def extract_block(block_number, w3):
    """
    Extract transaction data from a block (with caching).
    
    Args:
        block_number: Block number to extract
        w3: Web3 instance
    
    Returns:
        List of dictionaries with transaction data
    """
    # Check cache first
    cache_key = f"block_{block_number}"
    if cache_key in _block_cache:
        logger.debug(f"Using cached data for block {block_number}")
        return _block_cache[cache_key]
    
    try:
        block = w3.eth.get_block(block_number, full_transactions=True)
        rows = []

        for tx in block.get("transactions", []):
            try:
                # Get transaction receipt for additional data
                receipt = w3.eth.get_transaction_receipt(tx["hash"])
                
                rows.append({
                    "block_number": block.get("number"),
                    "block_hash": block.get("hash").hex() if block.get("hash") else None,
                    "timestamp": block.get("timestamp"),
                    "transaction_hash": tx.get("hash").hex() if tx.get("hash") else None,
                    "transaction_index": tx.get("transactionIndex"),
                    "from_address": tx.get("from"),
                    "to_address": tx.get("to"),
                    "value_eth": float(w3.from_wei(tx.get("value", 0), "ether")),
                    "gas": tx.get("gas"),
                    "gas_price_gwei": float(w3.from_wei(tx.get("gasPrice", 0), "gwei")),
                    "gas_used": receipt.get("gasUsed"),
                    "cumulative_gas_used": receipt.get("cumulativeGasUsed"),
                    "status": receipt.get("status"),  # 1 = success, 0 = failed
                    "contract_address": receipt.get("contractAddress"),
                    "effective_gas_price": receipt.get("effectiveGasPrice"),
                })
            except Exception as e:
                logger.warning(f"Failed to extract transaction {tx.get('hash', 'unknown')}: {e}")
                continue

        logger.info(f"Extracted {len(rows)} transactions from block {block_number}")
        
        # Cache the result (limit cache size to 100 blocks)
        if len(_block_cache) > 100:
            _block_cache.pop(next(iter(_block_cache)))  # Remove oldest
        _block_cache[cache_key] = rows
        
        return rows

    except Exception as e:
        logger.error(f"Failed to extract block {block_number}: {e}")
        return []


def extract_blocks(start_block, end_block, w3, parallel=True, max_workers=5):
    """
    Extract data from multiple blocks with parallel optimization.
    
    Args:
        start_block: Starting block number
        end_block: Ending block number (inclusive)
        w3: Web3 instance
        parallel: Use parallel extraction (default True for speed)
        max_workers: Number of parallel threads (default 5)
    
    Returns:
        List of all transaction rows from blocks
    """
    start_time = time.time()
    all_rows = []
    
    block_nums = list(range(start_block, end_block + 1))
    
    if parallel and len(block_nums) > 1:
        # Parallel extraction using ThreadPoolExecutor
        logger.info(f"🚀 Parallel extraction: {len(block_nums)} blocks with {max_workers} workers")
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(extract_block, block_num, w3): block_num for block_num in block_nums}
            
            for future in as_completed(futures):
                block_num = futures[future]
                try:
                    rows = future.result()
                    all_rows.extend(rows)
                except Exception as e:
                    logger.error(f"Failed to extract block {block_num}: {e}")
    else:
        # Sequential fallback
        for block_num in block_nums:
            rows = extract_block(block_num, w3)
            all_rows.extend(rows)
    
    elapsed = time.time() - start_time
    logger.info(f"✅ Extracted {len(all_rows)} transactions from {len(block_nums)} blocks in {elapsed:.2f}s")
    
    # Performance metrics
    if elapsed > 0:
        tx_per_sec = len(all_rows) / elapsed
        logger.info(f"📊 Performance: {tx_per_sec:.0f} tx/sec, {elapsed/len(block_nums):.2f}s/block")
    
    return all_rows