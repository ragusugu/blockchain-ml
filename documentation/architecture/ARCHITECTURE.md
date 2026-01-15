# System Architecture

## Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Blockchain ETL Pipeline                       │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────┐
│  Ethereum RPC    │  https://eth-mainnet.g.alchemy.com/v2/...
│   (Alchemy)      │
└────────┬─────────┘
         │ web3.py
         │ get_block(), get_transaction_receipt()
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EXTRACT PHASE (extract.py)                    │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ extract_block(block_number, w3)                          │   │
│  │  ├─ fetch block from RPC                                │   │
│  │  ├─ for each transaction: get receipt                   │   │
│  │  └─ return List[Dict] with 15 fields                    │   │
│  │                                                          │   │
│  │ extract_blocks(start, end, w3)                           │   │
│  │  ├─ iterate blocks start to end                         │   │
│  │  └─ aggregate all transaction rows                      │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────┬────────────────────────────────────────────────────────┘
         │ List[Dict]
         │ 711 transactions with 15 fields each
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                  TRANSFORM PHASE (transform.py)                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ transform_data(rows)                                     │   │
│  │  ├─ DataFrame(rows)                                      │   │
│  │  ├─ type enforcement (int64, float64, int8)              │   │
│  │  ├─ null handling (.fillna())                            │   │
│  │  ├─ column renames (tx_hash, from_addr, etc)            │   │
│  │  ├─ add processed_at timestamp                           │   │
│  │  └─ return DataFrame                                     │   │
│  │                                                          │   │
│  │ validate_data(df)                                        │   │
│  │  ├─ check required columns exist                         │   │
│  │  ├─ check no critical nulls                              │   │
│  │  └─ return bool (valid/invalid)                          │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────┬────────────────────────────────────────────────────────┘
         │ pandas.DataFrame
         │ 711 rows × 18 columns, all types correct
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    LOAD PHASE (fetch_and_store.py)               │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ df.to_sql('transaction_receipts', engine,                │   │
│  │            if_exists='append', index=False)              │   │
│  │                                                          │   │
│  │  ├─ SQLAlchemy engine.connect()                          │   │
│  │  ├─ Bulk insert (711 rows at once)                       │   │
│  │  ├─ Handle duplicates (ON CONFLICT DO NOTHING)           │   │
│  │  └─ Commit to PostgreSQL                                 │   │
│  │                                                          │   │
│  │ OR: main_etl.py with batching                            │   │
│  │  ├─ Process 10 blocks at a time                          │   │
│  │  ├─ Loop: Extract → Transform → Load → State             │   │
│  │  └─ Summary report on completion                         │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────┬────────────────────────────────────────────────────────┘
         │ INSERT INTO transaction_receipts
         │ 711 rows committed
         ▼
┌─────────────────────────────────────────────────────────────────┐
│                   STATE PHASE (pipeline_state)                   │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │ UPDATE pipeline_state SET                                │   │
│  │   last_block = 24237712,                                 │   │
│  │   updated_at = CURRENT_TIMESTAMP                         │   │
│  │                                                          │   │
│  │ Result:                                                  │   │
│  │  ├─ next run starts from block 24237713                  │   │
│  │  ├─ enables resumption after failure                     │   │
│  │  └─ tracks processing history                            │   │
│  └──────────────────────────────────────────────────────────┘   │
└────────┬────────────────────────────────────────────────────────┘
         │ UPDATE pipeline_state
         │ last_block=24237712
         ▼
┌────────────────────────────────────────────────────────────────────┐
│                      PostgreSQL Database                            │
│  ┌───────────────────────────────┐    ┌──────────────────────────┐ │
│  │  transaction_receipts         │    │   pipeline_state         │ │
│  │  ┌─────────────────────────┐  │    │  ┌──────────────────────┐│ │
│  │  │ id (PK)                 │  │    │  │ id (PK)              ││ │
│  │  │ tx_hash (UNIQUE)        │  │    │  │ last_block           ││ │
│  │  │ block_number            │  │    │  │ last_processed_at    ││ │
│  │  │ from_addr, to_addr      │  │    │  │ updated_at           ││ │
│  │  │ value (ETH)             │  │    │  └──────────────────────┘│ │
│  │  │ gas, gas_used           │  │    │                          │ │
│  │  │ status (1=success)      │  │    │  Current State:          │ │
│  │  │ processed_at            │  │    │  last_block = 24237712   │ │
│  │  │ created_at              │  │    │  Ready for next run      │ │
│  │  │ ... (18 total columns)  │  │    │                          │ │
│  │  │                         │  │    │                          │ │
│  │  │ Data: 711+ rows         │  │    │                          │ │
│  │  │ Size: ~500KB (growth)   │  │    │                          │ │
│  │  └─────────────────────────┘  │    │                          │ │
│  └───────────────────────────────┘    └──────────────────────────┘ │
│                                                                      │
│  Queries:                                                            │
│  SELECT COUNT(*) FROM transaction_receipts;                         │
│  SELECT * FROM transaction_receipts WHERE status=0;                 │
│  SELECT last_block FROM pipeline_state;                             │
└────────────────────────────────────────────────────────────────────┘
```

## Data Transformation Flow

```
RAW EXTRACT
──────────
{
  "hash": HexBytes("0xabc123..."),
  "from": "0x123...",
  "to": "0x456...",
  "value": 1500000000000000000,  ← Wei format
  "gas": 21000,
  "gasPrice": 45000000000,       ← Wei format
  ... receipt fields ...
}

         ↓ transform_data()

CLEAN TRANSFORM  
───────────────
{
  "tx_hash": "0xabc123...",
  "from_addr": "0x123...",
  "to_addr": "0x456...",
  "value": 1.5,                 ← Ether format
  "gas": 21000,
  "gas_price": 45.0,            ← Gwei format
  "status": 1,                  ← Normalized
  "processed_at": 2024-01-15... ← Added timestamp
}

         ↓ df.to_sql()

DATABASE INSERT
───────────────
INSERT INTO transaction_receipts VALUES (
  NULL,                           -- id (auto)
  24237712,                       -- block_number
  "0xabc...",                     -- tx_hash
  "0x123...",                     -- from_addr
  ... rest of columns ...
  NOW()                           -- created_at
)

         ↓ Update state

PIPELINE STATE
──────────────
UPDATE pipeline_state SET
  last_block = 24237712,
  updated_at = NOW()
  WHERE id = 1

Result: Next run will start from block 24237713
```

## Batch Processing Workflow

```
main_etl.py Orchestration
═════════════════════════

Iteration 1:
┌─────────────────────────────────────────────────┐
│ Blocks 24237700-24237709 (BATCH_SIZE=10)       │
├─────────────────────────────────────────────────┤
│ EXTRACT  → 78,340 transactions                 │
│ TRANSFORM → DataFrame validated                │
│ LOAD → INSERT 78,340 rows                       │
│ STATE → last_block = 24237709                   │
└─────────────────────────────────────────────────┘

Iteration 2:
┌─────────────────────────────────────────────────┐
│ Blocks 24237710-24237719 (BATCH_SIZE=10)       │
├─────────────────────────────────────────────────┤
│ EXTRACT  → 79,102 transactions                 │
│ TRANSFORM → DataFrame validated                │
│ LOAD → INSERT 79,102 rows                       │
│ STATE → last_block = 24237719                   │
└─────────────────────────────────────────────────┘

Summary on Completion:
  Blocks processed: 20
  Transactions loaded: 157,442
  Failed blocks: 0
```

## Error Handling Path

```
Normal Flow: Extract → Transform → Load → State ✓

Error in Extract:
  Catch exception
  Log warning
  Skip transaction
  Continue with others ✓

Error in Transform:
  Catch exception  
  Log error
  Skip batch
  Try next batch ✓

Error in Load:
  Catch exception
  Log error
  Rollback transaction
  Try again or skip ✓

Error in State:
  Catch exception
  Log error
  Continue (data still saved) ⚠

Critical Error (DB connection):
  Log error
  Exit with code 1
  ✗ STOP - requires manual intervention
```

## Deployment Architecture

```
docker-compose.yml
│
├─ PostgreSQL Service
│  ├─ Image: postgres:15
│  ├─ Port: 5432
│  ├─ Env: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB
│  ├─ Volume: postgres_data (persistent)
│  └─ Status: Ready for connections
│
└─ App Service
   ├─ Build: Dockerfile (Python 3.11-slim)
   ├─ Dependencies: web3, pandas, sqlalchemy, psycopg2
   ├─ Cmd: python fetch_and_store.py (or main_etl.py)
   ├─ Env: DATABASE_URL, RPC_URL, BATCH_SIZE
   ├─ Links: postgres (network connection)
   └─ Status: Running ETL periodically
```

## File Dependency Graph

```
main_etl.py
  ├─ imports: extract, transform, sqlalchemy
  ├─ calls: extract_blocks()
  ├─ calls: transform_data(), validate_data()
  └─ uses: PostgreSQL engine

fetch_and_store.py
  ├─ imports: extract, transform, sqlalchemy
  ├─ calls: extract_block()
  ├─ calls: transform_data(), validate_data()
  └─ uses: PostgreSQL engine

extract.py (standalone)
  ├─ imports: logging, web3
  ├─ defines: extract_block(), extract_blocks()
  └─ returns: List[Dict]

transform.py (standalone)
  ├─ imports: logging, pandas, datetime
  ├─ defines: transform_data(), validate_data()
  └─ returns: DataFrame

requirements.txt
  ├─ web3==6.15.1
  ├─ psycopg2-binary==2.9.9
  ├─ sqlalchemy==2.0.23
  ├─ pandas==2.2.0
  └─ ... others

Dockerfile
  ├─ FROM: python:3.11-slim
  ├─ COPY: requirements.txt
  ├─ RUN: pip install -r requirements.txt
  └─ CMD: python fetch_and_store.py
```

## State Tracking Logic

```
Application Start
      ↓
┌─────────────────────────────────────┐
│ Read pipeline_state                 │
│ Get last_block (default: 0)         │
└──────────┬──────────────────────────┘
           ↓
         If last_block = 0:
           Process from block 1 (or configurable start)
         
         If last_block = 24237712:
           Process from block 24237713
      
      ↓
┌─────────────────────────────────────┐
│ Get current latest block from RPC    │
│ last_block=24237712, latest=24237750 │
└──────────┬──────────────────────────┘
           ↓
      Process blocks:
      24237713 → 24237749 (37 blocks)
      
      ↓
┌─────────────────────────────────────┐
│ Process in batches (BATCH_SIZE=10)  │
│ Batch 1: 24237713-24237722          │
│ Batch 2: 24237723-24237732          │
│ Batch 3: 24237733-24237742          │
│ Batch 4: 24237743-24237749          │
└──────────┬──────────────────────────┘
           ↓
      After each batch:
      ┌─────────────────────────────────┐
      │ UPDATE pipeline_state           │
      │ SET last_block = batch_end_block│
      │ SET updated_at = NOW()          │
      └─────────────────────────────────┘
           ↓
      Result: If application crashes,
              next run automatically resumes
              from last successful block
```

---

This architecture enables:
- **Scalability**: Modular phases, batch processing
- **Reliability**: Error handling, state tracking, resumption
- **Observability**: Logging at each phase
- **Maintainability**: Clean separation of concerns
