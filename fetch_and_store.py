import os
import json
from web3 import Web3
from hexbytes import HexBytes
from web3.datastructures import AttributeDict
import psycopg2
from psycopg2.extras import Json
from datetime import datetime, timezone, timedelta
import shutil
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://user:password@localhost:5432/blockchain_db')
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create table if not exists
cursor.execute('DROP TABLE IF EXISTS transaction_receipts')
cursor.execute('''
CREATE TABLE IF NOT EXISTS transaction_receipts (
    id SERIAL PRIMARY KEY,
    transaction_hash VARCHAR(66) UNIQUE,
    transaction_index INTEGER,
    block_hash VARCHAR(66),
    block_number BIGINT,
    from_address VARCHAR(42),
    to_address VARCHAR(42),
    cumulative_gas_used BIGINT,
    gas_used BIGINT,
    contract_address VARCHAR(42),
    logs JSONB,
    status INTEGER,
    effective_gas_price BIGINT,
    type INTEGER,
    root VARCHAR(66),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
conn.commit()

# Robust serializer
def to_serializable(obj):
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
RPC_URL = "https://eth-mainnet.g.alchemy.com/v2/G09aLwdbZ-zyer6rwNMGu"
w3 = Web3(Web3.HTTPProvider(RPC_URL))
print("Connected:", w3.is_connected())

# Fetch latest block
block_number = w3.eth.block_number
print(f"Latest block number: {block_number}")
block = w3.eth.get_block(block_number, full_transactions=True)

# Process each transaction
for tx in block["transactions"]:
    tx_hash = tx["hash"]
    try:
        receipt = w3.eth.get_transaction_receipt(tx_hash)
        # Insert into DB
        cursor.execute('''
        INSERT INTO transaction_receipts (
            transaction_hash, transaction_index, block_hash, block_number,
            from_address, to_address, cumulative_gas_used, gas_used,
            contract_address, logs, status, effective_gas_price, type, root
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (transaction_hash) DO NOTHING
        ''', (
            receipt['transactionHash'].hex(),
            receipt['transactionIndex'],
            receipt['blockHash'].hex(),
            receipt['blockNumber'],
            receipt['from'],
            receipt.get('to'),  # can be None
            receipt['cumulativeGasUsed'],
            receipt['gasUsed'],
            receipt.get('contractAddress'),  # can be None
            Json(to_serializable(receipt['logs'])),
            receipt['status'],
            receipt.get('effectiveGasPrice'),
            receipt.get('type'),
            receipt.get('root')
        ))
        conn.commit()
        print(f"Saved receipt for {tx_hash.hex()}")
    except Exception as e:
        print(f"Failed to save {tx_hash.hex()}: {e}")
        conn.rollback()  # Rollback to clear aborted transaction

# DB cleanup: Delete records older than 5 days
try:
    five_days_ago = datetime.now(timezone.utc) - timedelta(days=5)
    cursor.execute("DELETE FROM transaction_receipts WHERE created_at < %s", (five_days_ago,))
    deleted_count = cursor.rowcount
    conn.commit()
    print(f"Deleted {deleted_count} records older than 5 days")
except Exception as e:
    print(f"Failed to delete old records: {e}")
    conn.rollback()

# Check disk space: If free space < 1GB, delete all except current date data
import psutil
disk = psutil.disk_usage('/')
free_gb = disk.free / (1024**3)
if free_gb < 1:
    print(f"Low disk space: {free_gb:.2f} GB free. Deleting all data except current date.")
    today = datetime.now(timezone.utc).date()
    cursor.execute("DELETE FROM transaction_receipts WHERE DATE(created_at) != %s", (today,))
    conn.commit()
    print(f"Deleted records not from {today}")

cursor.close()
conn.close()

# Cleanup: Delete local receipts folder after storing in DB
import shutil
receipts_dir = "receipts"
if os.path.exists(receipts_dir):
    print(f"Deleting local receipts directory: {receipts_dir}")
    shutil.rmtree(receipts_dir)
else:
    print("No receipts directory to delete.")

print("Done")