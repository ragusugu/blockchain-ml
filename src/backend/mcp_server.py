"""
MCP Server for Blockchain RPC Data & AI Fraud Detection

Exposes blockchain tools via the Model Context Protocol so that
LLMs and other MCP clients can:
  - Query transactions, blocks, and balances from Ethereum
  - Run fraud detection on individual transactions
  - Retrieve model status and metrics

Start:
    python -m mcp_server            (stdio transport — default)
    python -m mcp_server --sse      (SSE transport on port 8000)

Requires: fastmcp, web3, scikit-learn
"""
import os
import sys
import json
import logging
from datetime import datetime
from typing import Optional

import pandas as pd
from fastmcp import FastMCP
from web3 import Web3
from web3.exceptions import TransactionNotFound

# ── Ensure the backend package is importable ──────────────────────
_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from config import cfg
from connections import get_web3

logger = logging.getLogger(__name__)

# ── Initialise MCP server ────────────────────────────────────────
mcp = FastMCP(
    "Blockchain ML",
    instructions=(
        "Ethereum blockchain query and AI fraud-detection server. "
        "Use the tools to fetch on-chain data and analyse transactions."
    ),
)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Helper: lazy Web3 accessor
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def _w3() -> Web3:
    """Return a connected Web3 instance or raise."""
    w3 = get_web3()
    if w3 is None:
        raise ConnectionError(
            "Cannot connect to any Ethereum RPC endpoint. "
            f"Tried: {cfg.rpc_candidates}"
        )
    return w3


def _wei_to_ether(wei: int) -> str:
    """Convert wei to ether string with 18-decimal precision."""
    return str(Web3.from_wei(wei, "ether"))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tool 1 — Get latest block number
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.tool()
def get_latest_block_number() -> str:
    """Return the latest Ethereum block number."""
    block_num = _w3().eth.block_number
    return json.dumps({"block_number": block_num})


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tool 2 — Get block details
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.tool()
def get_block(block_number: int, full_transactions: bool = False) -> str:
    """
    Fetch an Ethereum block by number.

    Args:
        block_number: The block height to retrieve.
        full_transactions: If True, include full transaction objects
                           instead of just hashes.
    """
    w3 = _w3()
    block = w3.eth.get_block(block_number, full_transactions=full_transactions)
    result = {
        "number": block.number,
        "hash": block.hash.hex(),
        "parentHash": block.parentHash.hex(),
        "timestamp": block.timestamp,
        "datetime_utc": datetime.utcfromtimestamp(block.timestamp).isoformat(),
        "gasUsed": block.gasUsed,
        "gasLimit": block.gasLimit,
        "baseFeePerGas": getattr(block, "baseFeePerGas", None),
        "miner": block.miner,
        "transaction_count": len(block.transactions),
    }
    if full_transactions:
        result["transactions"] = [
            {
                "hash": tx.hash.hex(),
                "from": tx["from"],
                "to": tx.get("to"),
                "value_eth": _wei_to_ether(tx.value),
                "gas": tx.gas,
                "gasPrice": tx.gasPrice,
            }
            for tx in block.transactions[:50]  # cap at 50 for context window
        ]
    else:
        result["transaction_hashes"] = [
            tx.hex() if isinstance(tx, bytes) else str(tx)
            for tx in block.transactions[:50]
        ]
    return json.dumps(result, default=str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tool 3 — Get transaction details
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.tool()
def get_transaction(tx_hash: str) -> str:
    """
    Retrieve full details for an Ethereum transaction by its hash.

    Args:
        tx_hash: The 0x-prefixed transaction hash.
    """
    w3 = _w3()
    try:
        tx = w3.eth.get_transaction(tx_hash)
    except TransactionNotFound:
        return json.dumps({"error": f"Transaction {tx_hash} not found"})

    receipt = w3.eth.get_transaction_receipt(tx_hash)

    result = {
        "hash": tx.hash.hex(),
        "blockNumber": tx.blockNumber,
        "from": tx["from"],
        "to": tx.get("to"),
        "value_eth": _wei_to_ether(tx.value),
        "gas": tx.gas,
        "gasPrice": tx.gasPrice,
        "nonce": tx.nonce,
        "input_data_length": len(tx.input) if tx.input else 0,
        "status": "success" if receipt.status == 1 else "failed",
        "gasUsed": receipt.gasUsed,
        "effectiveGasPrice": getattr(receipt, "effectiveGasPrice", None),
        "logs_count": len(receipt.logs),
    }
    return json.dumps(result, default=str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tool 4 — Get address balance
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.tool()
def get_address_balance(address: str) -> str:
    """
    Get the ETH balance of an Ethereum address.

    Args:
        address: The 0x-prefixed Ethereum address.
    """
    w3 = _w3()
    checksummed = w3.to_checksum_address(address)
    balance_wei = w3.eth.get_balance(checksummed)
    return json.dumps({
        "address": checksummed,
        "balance_wei": str(balance_wei),
        "balance_eth": _wei_to_ether(balance_wei),
    })


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tool 5 — Get address transaction count (nonce)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.tool()
def get_address_tx_count(address: str) -> str:
    """
    Get the total number of transactions sent from an address.

    Args:
        address: The 0x-prefixed Ethereum address.
    """
    w3 = _w3()
    checksummed = w3.to_checksum_address(address)
    count = w3.eth.get_transaction_count(checksummed)
    return json.dumps({
        "address": checksummed,
        "transaction_count": count,
    })


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tool 6 — Analyse a transaction for fraud
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.tool()
def analyse_transaction_fraud(
    tx_hash: str,
    threshold: float = 0.5,
) -> str:
    """
    Fetch a transaction from the chain and run it through the AI
    fraud-detection model. Returns the fraud probability and risk level.

    Args:
        tx_hash: The 0x-prefixed transaction hash.
        threshold: Probability above which the tx is flagged as fraud (0-1).
    """
    from ml.ai_fraud_detector import BlockchainFraudDetector

    w3 = _w3()

    # 1. Fetch on-chain data
    try:
        tx = w3.eth.get_transaction(tx_hash)
    except TransactionNotFound:
        return json.dumps({"error": f"Transaction {tx_hash} not found"})

    receipt = w3.eth.get_transaction_receipt(tx_hash)
    block = w3.eth.get_block(tx.blockNumber)

    # 2. Build a single-row DataFrame matching the schema the detector expects
    row = {
        "tx_hash": tx.hash.hex(),
        "block_number": tx.blockNumber,
        "from_address": tx["from"],
        "to_address": tx.get("to", "0x0"),
        "value": float(Web3.from_wei(tx.value, "ether")),
        "gas": tx.gas,
        "gas_price": tx.gasPrice,
        "gas_used": receipt.gasUsed,
        "timestamp": block.timestamp,
        "input_data": tx.input.hex() if tx.input else "0x",
        "status": receipt.status,
    }
    df = pd.DataFrame([row])

    # 3. Run through the detector
    detector = BlockchainFraudDetector(model_path=cfg.MODEL_PATH)

    if detector.model is None:
        # No trained model available — fall back to anomaly detection
        result_df = detector.anomaly_detection(df)
        if result_df is None:
            return json.dumps({"error": "Feature extraction failed"})
        rec = result_df.iloc[0]
        return json.dumps({
            "tx_hash": tx_hash,
            "method": "anomaly_detection (no trained model)",
            "anomaly_flag": int(rec.get("anomaly_flag", 0)),
            "anomaly_score": round(float(rec.get("anomaly_score", 0)), 4),
            "transaction": row,
        }, default=str)

    result_df = detector.predict(df, threshold=threshold)
    if result_df is None:
        return json.dumps({"error": "Prediction failed"})

    rec = result_df.iloc[0]
    return json.dumps({
        "tx_hash": tx_hash,
        "method": "random_forest",
        "fraud_probability": round(float(rec["fraud_probability"]), 4),
        "is_fraud": bool(rec["is_fraud"]),
        "risk_level": rec["risk_level"],
        "threshold": threshold,
        "transaction": row,
    }, default=str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Tool 7 — Model info / metrics
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.tool()
def get_model_info() -> str:
    """
    Return the current fraud-detection model's status and performance
    metrics (accuracy, ROC-AUC, training date, etc.).
    """
    from ml.ai_fraud_detector import BlockchainFraudDetector

    detector = BlockchainFraudDetector(model_path=cfg.MODEL_PATH)
    info = {
        "model_path": cfg.MODEL_PATH,
        "model_loaded": detector.model is not None,
        "metrics": getattr(detector, "metrics", {}),
        "feature_names": getattr(detector, "feature_names", []),
    }
    if detector.model is not None:
        info["feature_importance"] = detector.get_feature_importance()
    return json.dumps(info, default=str)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Resource: RPC configuration (read-only context)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
@mcp.resource("config://rpc")
def rpc_config() -> str:
    """Current RPC endpoint configuration."""
    return json.dumps({
        "primary_rpc": cfg.RPC_URL,
        "ankr_rpc": cfg.ANKR_RPC_URL,
        "fallback_urls": cfg.RPC_FALLBACK_URLS,
        "timeout_s": cfg.RPC_TIMEOUT,
        "max_retries": cfg.RPC_MAX_RETRIES,
    })


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  Entrypoint
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def main():
    import argparse

    parser = argparse.ArgumentParser(description="Blockchain ML MCP Server")
    parser.add_argument(
        "--sse", action="store_true",
        help="Run with SSE transport (HTTP) instead of stdio",
    )
    parser.add_argument(
        "--port", type=int, default=8000,
        help="Port for SSE transport (default: 8000)",
    )
    args = parser.parse_args()

    if args.sse:
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
