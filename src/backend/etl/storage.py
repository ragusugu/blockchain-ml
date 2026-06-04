"""
Shared storage helpers for transformed blockchain transactions.
"""
import logging
from datetime import datetime

import numpy as np
import pandas as pd
from sqlalchemy import text

from config import cfg
from connections import get_db_engine

logger = logging.getLogger(__name__)

TRANSACTION_RECEIPT_COLUMNS = [
    'block_number', 'block_hash', 'block_timestamp', 'tx_hash', 'tx_index',
    'from_addr', 'to_addr', 'value', 'gas', 'gas_price', 'gas_used',
    'cumulative_gas_used', 'status', 'contract_addr', 'effective_gas_price'
]

CREATE_TRANSACTION_RECEIPTS_SQL = """
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
"""


def _db_value(value):
    """Convert pandas/numpy missing values into DB-friendly None."""
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, pd.Timestamp):
        return value.to_pydatetime()
    return value


def persist_transformed_transactions(df, engine=None, batch_size=1000):
    """
    Persist transformed transaction rows to PostgreSQL.

    Returns the number of inserted rows. Duplicate tx_hash values are skipped.
    """
    if not cfg.STORE_BATCH_RESULTS:
        logger.debug("Transaction persistence disabled by STORE_BATCH_RESULTS=false")
        return 0
    if df is None or df.empty:
        return 0

    engine = engine or get_db_engine()
    if not engine:
        logger.warning("No database engine available; skipping transaction persistence")
        return 0

    rows = []
    for _, row in df.iterrows():
        if not row.get('tx_hash'):
            continue
        record = {col: _db_value(row.get(col)) for col in TRANSACTION_RECEIPT_COLUMNS}
        record['processed_at'] = _db_value(row.get('processed_at')) or datetime.utcnow()
        rows.append(record)

    if not rows:
        return 0

    placeholders = ', '.join([f":{col}" for col in TRANSACTION_RECEIPT_COLUMNS])
    columns = ', '.join(TRANSACTION_RECEIPT_COLUMNS)
    insert_sql = text(f"""
        INSERT INTO transaction_receipts ({columns}, processed_at, created_at)
        VALUES ({placeholders}, :processed_at, CURRENT_TIMESTAMP)
        ON CONFLICT (tx_hash) DO NOTHING
    """)

    inserted = 0
    try:
        with engine.begin() as conn:
            conn.execute(text(CREATE_TRANSACTION_RECEIPTS_SQL))
            for i in range(0, len(rows), batch_size):
                result = conn.execute(insert_sql, rows[i:i + batch_size])
                inserted += result.rowcount or 0
        logger.info("Stored %s streamed transaction(s) to PostgreSQL", inserted)
        return inserted
    except Exception as exc:
        logger.warning("Could not persist transformed transactions: %s", exc)
        return 0
