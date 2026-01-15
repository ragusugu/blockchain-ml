"""
Extract Phase of ETL Pipeline
Converts blockchain data into flat rows for processing
"""
import logging

logger = logging.getLogger(__name__)


def extract_block(block_number, w3):
    """
    Extract transaction data from a block.
    
    Args:
        block_number: Block number to extract
        w3: Web3 instance
    
    Returns:
        List of dictionaries with transaction data
    """
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
        return rows

    except Exception as e:
        logger.error(f"Failed to extract block {block_number}: {e}")
        return []


def extract_blocks(start_block, end_block, w3):
    """
    Extract data from multiple blocks.
    
    Args:
        start_block: Starting block number
        end_block: Ending block number (inclusive)
        w3: Web3 instance
    
    Returns:
        List of all transaction rows from blocks
    """
    all_rows = []
    
    for block_num in range(start_block, end_block + 1):
        rows = extract_block(block_num, w3)
        all_rows.extend(rows)
    
    logger.info(f"Extracted {len(all_rows)} total transactions from blocks {start_block}-{end_block}")
    return all_rows