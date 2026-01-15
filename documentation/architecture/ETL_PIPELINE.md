# Blockchain ETL Pipeline

A production-grade Extract-Transform-Load (ETL) pipeline for blockchain transaction data, built with Web3.py, PostgreSQL, and Pandas.

## Architecture

```
Extract (extract.py)
    ↓
Transform (transform.py)
    ↓
Load (fetch_and_store.py, main_etl.py)
    ↓
State Tracking (pipeline_state table)
```

## Components

### 1. Extract Phase (`extract.py`)
- **Purpose**: Extract raw blockchain data from Ethereum
- **Functions**:
  - `extract_block(block_number, w3)` → List[Dict]
    - Extracts transactions from a single block
    - Retrieves receipts for gas and status info
    - Returns 15 fields per transaction
  - `extract_blocks(start_block, end_block, w3)` → List[Dict]
    - Batch extraction across multiple blocks
- **Output Format**:
  ```python
  {
    "block_number": 12345678,
    "block_hash": "0x...",
    "timestamp": 1699123456,
    "transaction_hash": "0x...",
    "transaction_index": 0,
    "from_address": "0x...",
    "to_address": "0x...",
    "value_eth": 1.5,
    "gas": 21000,
    "gas_price_gwei": 45.2,
    "gas_used": 21000,
    "cumulative_gas_used": 8900000,
    "status": 1,  # 1=success, 0=failed
    "contract_address": "0x..." or None,
    "effective_gas_price": 45000000000
  }
  ```

### 2. Transform Phase (`transform.py`)
- **Purpose**: Clean and normalize extracted data
- **Functions**:
  - `transform_data(rows)` → pandas.DataFrame
    - Converts to DataFrame
    - Enforces data types (int64, float64, int8, etc.)
    - Handles missing values (fills null addresses with "")
    - Renames columns for database compatibility
    - Adds processing timestamp
  - `validate_data(df)` → bool
    - Checks for required columns
    - Validates no critical nulls
    - Returns validation status
- **Transformations**:
  - Column renames: `transaction_hash` → `tx_hash`, etc.
  - Type enforcement: block_number → int64, value_eth → float64
  - Null handling: to_address defaults to ""

### 3. Load Phase (`fetch_and_store.py`, `main_etl.py`)
- **Purpose**: Insert cleaned data into PostgreSQL
- **Method**: SQLAlchemy with Pandas `df.to_sql()`
- **Batch Processing**: Commits multiple blocks at once
- **Conflict Handling**: ON CONFLICT DO NOTHING for duplicate tx_hash
- **Database Tables**:

  **transaction_receipts**:
  ```sql
  CREATE TABLE transaction_receipts (
    id SERIAL PRIMARY KEY,
    block_number BIGINT,
    block_hash VARCHAR(66),
    block_timestamp BIGINT,
    tx_hash VARCHAR(66) UNIQUE,
    tx_index INTEGER,
    from_addr VARCHAR(42),
    to_addr VARCHAR(42),
    value FLOAT8,
    gas BIGINT,
    gas_price FLOAT8,
    gas_used BIGINT,
    cumulative_gas_used BIGINT,
    status SMALLINT,
    contract_addr VARCHAR(42),
    effective_gas_price BIGINT,
    processed_at TIMESTAMP,
    created_at TIMESTAMP
  )
  ```

  **pipeline_state**:
  ```sql
  CREATE TABLE pipeline_state (
    id SERIAL PRIMARY KEY,
    last_block BIGINT,
    last_processed_at TIMESTAMP,
    updated_at TIMESTAMP
  )
  ```

### 4. State Tracking Phase
- **Purpose**: Track incremental processing
- **Table**: `pipeline_state`
- **Logic**:
  1. Read `last_block` on startup
  2. Process blocks from `last_block + 1` to `current_block - 1`
  3. Update `last_block` after successful batch
  4. Enables resume from interruption

## Usage

### Option 1: Simple Single-Block Processing
```bash
# Process latest block
python fetch_and_store.py
```

### Option 2: Batch Processing with Orchestration
```bash
# Process blocks incrementally in batches of 10
python main_etl.py
```

### Option 3: Docker Deployment
```bash
# Build and start services
docker-compose up --build

# View logs
docker-compose logs app

# Stop services
docker-compose down
```

## Configuration

Environment variables (set in `.env` or docker-compose.yml):
```
DATABASE_URL=postgresql://user:password@localhost:5432/blockchain_db
RPC_URL=https://eth-mainnet.g.alchemy.com/v2/YOUR_API_KEY
BATCH_SIZE=10
```

## Data Flow Example

```
Block 24237712
    ↓
Extract: 711 transactions
    {tx_hash, from_addr, to_addr, value_eth, gas_used, status, ...}
    ↓
Transform: Validate & normalize
    - Convert types (int, float, int8)
    - Handle nulls
    - Rename columns
    - Add processed_at timestamp
    ↓
Load: Insert to PostgreSQL
    INSERT INTO transaction_receipts (711 rows)
    ↓
State: Update pipeline_state
    UPDATE pipeline_state SET last_block = 24237712
    ↓
Cleanup: Delete old data (>5 days) if needed
```

## Data Retention Policy

- **Default**: Keep 5 days of data
- **Low Disk**: If free space < 1GB, delete all except today's data
- **Automatic Execution**: Runs after each ETL cycle

## Error Handling

- **Extract errors**: Logs warning, skips failed transactions
- **Transform errors**: Logs error, validates before load
- **Load errors**: Logs error, reverts batch on failure
- **State errors**: Logs error but continues processing
- **Critical failures**: Exit with code 1 and log traceback

## Performance Considerations

- **Batch Size**: Default 10 blocks per run (configurable via `BATCH_SIZE`)
- **Database**: Bulk insert with `df.to_sql()` vs row-by-row
- **Memory**: Loads one batch at a time
- **Concurrent Calls**: Respects RPC rate limits

## Monitoring

Logs include:
- Timestamps for all operations
- Block ranges processed
- Transaction counts
- Error messages with context
- Execution summary

Example:
```
2024-01-15 10:32:45 - root - INFO - Processing blocks 24237700-24237709
2024-01-15 10:32:47 - extract - INFO - Extracted 7834 transactions
2024-01-15 10:32:48 - transform - INFO - Transformed 7834 rows
2024-01-15 10:32:50 - root - INFO - LOAD: Successfully inserted 7834 rows
2024-01-15 10:32:50 - root - INFO - Updated pipeline_state: last_block = 24237709
```

## Database Access

```bash
# Connect to PostgreSQL
psql postgresql://user:password@localhost:5432/blockchain_db

# View latest transactions
SELECT tx_hash, from_addr, to_addr, value, status 
FROM transaction_receipts 
ORDER BY created_at DESC LIMIT 10;

# Check pipeline state
SELECT last_block, last_processed_at FROM pipeline_state;

# Count transactions by status
SELECT status, COUNT(*) FROM transaction_receipts GROUP BY status;
```

## Development

### Testing Extract Phase
```python
from web3 import Web3
from extract import extract_block

w3 = Web3(Web3.HTTPProvider("https://..."))
rows = extract_block(24237712, w3)
print(f"Extracted {len(rows)} transactions")
```

### Testing Transform Phase
```python
from transform import transform_data, validate_data

df = transform_data(rows)
if validate_data(df):
    print("Data valid!")
    print(df.info())
```

### Testing Load Phase (Manual)
```python
from sqlalchemy import create_engine

engine = create_engine("postgresql://user:password@localhost/blockchain_db")
df.to_sql('transaction_receipts', engine, if_exists='append')
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Database connection refused | Check PostgreSQL is running, verify credentials |
| Web3 rate limit errors | Reduce BATCH_SIZE or use higher tier RPC provider |
| Disk space errors | Delete old data via cleanup_old_data() or increase disk |
| Duplicate key errors | Extract handles via ON CONFLICT, check for schema changes |
| Memory issues with large batches | Reduce BATCH_SIZE environment variable |

## Requirements

- Python 3.11+
- PostgreSQL 15+
- Docker & Docker Compose (for containerized deployment)

### Python Packages
```
web3==6.15.1
psycopg2-binary==2.9.9
sqlalchemy==2.0.23
pandas==2.2.0
hexbytes==0.3.1
psutil==5.9.8
python-dotenv==1.0.0
```

## Architecture Benefits

✓ **Modular**: Each phase (E/T/L/S) is independent and testable  
✓ **Scalable**: Batch processing prevents memory issues  
✓ **Recoverable**: State tracking enables resume after failure  
✓ **Monitorable**: Comprehensive logging for debugging  
✓ **Maintainable**: Clear separation of concerns  
✓ **Production-ready**: Error handling, type hints, documentation  

## License

MIT
