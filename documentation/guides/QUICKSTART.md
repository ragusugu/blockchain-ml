# Quick Start Guide - Blockchain ETL Pipeline

## Project Structure
```
blockchain-ml/
├── extract.py              # Extract phase - fetches block data
├── transform.py            # Transform phase - cleans & normalizes data
├── fetch_and_store.py      # Simple single-block ETL execution
├── main_etl.py             # Full orchestration with batching
├── requirements.txt        # Python dependencies
├── Dockerfile              # Container image definition
├── docker-compose.yml      # Multi-container orchestration
├── ETL_PIPELINE.md         # Complete documentation
├── 01_block_data.ipynb     # Original notebook (reference)
└── receipts/               # Local receipt files (auto-cleaned)
```

## 1-Minute Setup

### Docker (Recommended)
```bash
# Start everything
docker-compose up --build

# View logs
docker-compose logs -f app

# Stop
docker-compose down
```

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run single block ETL
python fetch_and_store.py

# Or run batch ETL
python main_etl.py
```

## What Each File Does

| File | Purpose | Run Command |
|------|---------|-------------|
| `fetch_and_store.py` | Process latest block, quick testing | `python fetch_and_store.py` |
| `main_etl.py` | Production batch processing, incremental | `python main_etl.py` |
| `extract.py` | Get blockchain data (used by both above) | Imported, not run directly |
| `transform.py` | Clean data with Pandas (used by both) | Imported, not run directly |

## ETL Pipeline Flow

```
Your Request
    ↓
extract.py: Get block transactions from Ethereum RPC
    (711 transactions from block 24237712)
    ↓
transform.py: Clean & normalize with Pandas
    (Convert types, handle nulls, rename columns)
    ↓
fetch_and_store.py/main_etl.py: Insert to PostgreSQL
    (df.to_sql() bulk insert → transaction_receipts table)
    ↓
pipeline_state: Track progress
    (Save last_block for resumption)
    ↓
Database Ready: Query your data!
    SELECT * FROM transaction_receipts;
```

## Key Features

✅ **Extract**: Blockchain RPC → flat transaction data  
✅ **Transform**: Type conversion, null handling, validation  
✅ **Load**: Bulk insert with SQLAlchemy + Pandas  
✅ **State**: Track last block for incremental processing  
✅ **Resilient**: Error handling, logging, retry capable  
✅ **Scalable**: Batch processing, configurable BATCH_SIZE  

## Configuration

```bash
# Set environment variables (or edit docker-compose.yml)
export DATABASE_URL="postgresql://user:password@localhost:5432/blockchain_db"
export RPC_URL="https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY"
export BATCH_SIZE="10"
```

## Database Credentials

```
Host: localhost
Port: 5432
Database: blockchain_db
Username: user
Password: password
```

**Connect:**
```bash
psql postgresql://user:password@localhost:5432/blockchain_db
```

## Verify It Works

```bash
# 1. Start Docker
docker-compose up --build

# 2. Check logs (should see "ETL Pipeline completed successfully")
docker-compose logs app

# 3. Connect to database
docker-compose exec postgres psql -U user -d blockchain_db

# 4. Query data
SELECT COUNT(*) FROM transaction_receipts;
SELECT * FROM pipeline_state;
```

## Common Commands

```bash
# View app logs in real-time
docker-compose logs -f app

# View database logs
docker-compose logs -f postgres

# Stop all services
docker-compose down

# Remove everything including data
docker-compose down -v

# Rebuild after code changes
docker-compose up --build

# Run bash inside container
docker-compose exec app bash

# Access database CLI
docker-compose exec postgres psql -U user -d blockchain_db
```

## Data Examples

### Transaction Record
```json
{
  "block_number": 24237712,
  "tx_hash": "0xabc123...",
  "from_addr": "0x123...",
  "to_addr": "0x456...",
  "value": 1.5,
  "gas_used": 21000,
  "status": 1,
  "created_at": "2024-01-15 10:32:50"
}
```

### Pipeline State
```
last_block: 24237712
last_processed_at: 2024-01-15 10:32:50
```

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `psql: connection refused` | Check `docker-compose logs postgres` |
| `Web3 connection failed` | Verify RPC_URL is correct |
| `Duplicate key error` | Already processed block - check pipeline_state |
| `Out of memory` | Reduce BATCH_SIZE environment variable |
| `Disk full` | Cleanup deletes data >5 days automatically |

## Performance

- **Extract**: ~100 blocks/min (depends on RPC)
- **Transform**: ~50k rows/sec (Pandas)
- **Load**: ~10k rows/sec (PostgreSQL)
- **Default Batch**: 10 blocks (~7k transactions)
- **Memory**: ~50MB per batch at default size

## Next Steps

1. **Monitor**: Check logs regularly
2. **Customize**: Adjust BATCH_SIZE, retention policy
3. **Query**: Build analytics on transaction_receipts
4. **Scale**: Add more batches, archive old data
5. **Integrate**: Connect BI tools (Grafana, Tableau, etc.)

## Support

Check [ETL_PIPELINE.md](ETL_PIPELINE.md) for complete documentation.
